from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from .bounds import compute_aggregates
from .schema import PhaseInterval, Scenario, ScheduleSpec


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    message: str


@dataclass(frozen=True)
class ScheduleMetrics:
    makespan: Decimal
    queue_time: Decimal
    blocked_agent_time: Decimal
    blocked_any_time: Decimal
    human_busy_time: Decimal


@dataclass(frozen=True)
class ScheduleValidation:
    valid: bool
    issues: tuple[ValidationIssue, ...]
    metrics: ScheduleMetrics | None


def _overlap_issues(
    intervals: list[tuple[Decimal, Decimal, str]],
    *,
    code: str,
    resource_name: str,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    intervals.sort(key=lambda item: (item[0], item[1], item[2]))
    if not intervals:
        return issues
    previous_start, previous_end, previous_label = intervals[0]
    for start, end, label in intervals[1:]:
        if start < previous_end:
            issues.append(
                ValidationIssue(
                    code,
                    f"{resource_name}: {previous_label} [{previous_start}, {previous_end}) "
                    f"overlaps {label} [{start}, {end})",
                )
            )
            if end > previous_end:
                previous_start, previous_end, previous_label = start, end, label
        else:
            previous_start, previous_end, previous_label = start, end, label
    return issues


def _union_duration(intervals: list[tuple[Decimal, Decimal]]) -> Decimal:
    if not intervals:
        return Decimal("0")
    ordered = sorted(intervals)
    total = Decimal("0")
    current_start, current_end = ordered[0]
    for start, end in ordered[1:]:
        if start <= current_end:
            current_end = max(current_end, end)
        else:
            total += current_end - current_start
            current_start, current_end = start, end
    return total + current_end - current_start


def validate_schedule(
    scenario: Scenario,
    schedule: ScheduleSpec,
) -> ScheduleValidation:
    issues: list[ValidationIssue] = []
    tasks = scenario.task_by_id
    expected = {
        (task.task_id, phase.phase_id): phase
        for task in scenario.tasks
        for phase in task.phases
    }
    provided: dict[tuple[str, str], PhaseInterval] = {}

    for interval in schedule.phases:
        key = (interval.task_id, interval.phase_id)
        if key in provided:
            issues.append(
                ValidationIssue("duplicate_phase", f"phase {key} appears more than once")
            )
            continue
        provided[key] = interval
        if key not in expected:
            issues.append(
                ValidationIssue("unknown_phase", f"phase {key} is not in scenario")
            )
            continue
        if interval.agent < 1 or interval.agent > scenario.p:
            issues.append(
                ValidationIssue(
                    "invalid_agent",
                    f"phase {key} uses agent {interval.agent}, expected 1..{scenario.p}",
                )
            )
        if interval.end <= interval.start:
            issues.append(
                ValidationIssue(
                    "invalid_interval",
                    f"phase {key} must have end greater than start",
                )
            )
            continue
        expected_duration = scenario.effective_phase_duration(expected[key])
        if interval.end - interval.start != expected_duration:
            issues.append(
                ValidationIssue(
                    "duration_mismatch",
                    f"phase {key} duration {interval.end - interval.start}, "
                    f"expected {expected_duration}",
                )
            )
        for endpoint_name, endpoint in (("start", interval.start), ("end", interval.end)):
            try:
                scenario.to_ticks(
                    endpoint,
                    field=f"schedule {schedule.schedule_id} {key} {endpoint_name}",
                )
            except ValueError as error:
                issues.append(ValidationIssue("time_grid", str(error)))

    missing = sorted(set(expected) - set(provided))
    for key in missing:
        issues.append(ValidationIssue("missing_phase", f"phase {key} is missing"))

    if missing or any(issue.code in {"unknown_phase", "duplicate_phase"} for issue in issues):
        return ScheduleValidation(False, tuple(issues), None)

    task_intervals: dict[str, list[PhaseInterval]] = {}
    task_spans: dict[str, tuple[Decimal, Decimal, int]] = {}
    blocked_intervals: list[tuple[Decimal, Decimal]] = []
    queue_time = Decimal("0")
    human_intervals: list[tuple[Decimal, Decimal, str]] = []
    human_busy = Decimal("0")

    assignments = {assignment.task_id: assignment for assignment in schedule.assignments}
    if len(assignments) != len(schedule.assignments):
        issues.append(
            ValidationIssue("duplicate_assignment", "task assignments must be unique")
        )
    for task in scenario.tasks:
        intervals = [provided[(task.task_id, phase.phase_id)] for phase in task.phases]
        task_intervals[task.task_id] = intervals
        assignment = assignments.get(task.task_id)
        if assignment is None:
            issues.append(
                ValidationIssue(
                    "missing_assignment",
                    f"task {task.task_id} has no assignment record",
                )
            )
            assignment_time = intervals[0].start
            assignment_agent = intervals[0].agent
        else:
            assignment_time = assignment.assigned_at
            assignment_agent = assignment.agent
            try:
                scenario.to_ticks(
                    assignment_time,
                    field=(
                        f"schedule {schedule.schedule_id} task {task.task_id} "
                        "assigned_at"
                    ),
                )
            except ValueError as error:
                issues.append(ValidationIssue("time_grid", str(error)))
            if assignment_agent < 1 or assignment_agent > scenario.p:
                issues.append(
                    ValidationIssue(
                        "invalid_agent",
                        f"task {task.task_id} assignment uses agent {assignment_agent}",
                    )
                )
            if intervals[0].start < assignment_time:
                issues.append(
                    ValidationIssue(
                        "assignment_time",
                        f"task {task.task_id} starts before it is assigned",
                    )
                )
            if intervals[0].agent != assignment_agent:
                issues.append(
                    ValidationIssue(
                        "agent_reassignment",
                        f"task {task.task_id} assignment agent {assignment_agent} "
                        f"differs from phase agent {intervals[0].agent}",
                    )
                )
        agents = {interval.agent for interval in intervals}
        if len(agents) != 1:
            issues.append(
                ValidationIssue(
                    "agent_reassignment",
                    f"task {task.task_id} uses agents {sorted(agents)}",
                )
            )
        if (
            task.phases[0].resource == "human"
            and intervals[0].start > assignment_time
        ):
            queue_time += intervals[0].start - assignment_time
            blocked_intervals.append((assignment_time, intervals[0].start))

        for index in range(1, len(intervals)):
            previous = intervals[index - 1]
            current = intervals[index]
            if current.start < previous.end:
                issues.append(
                    ValidationIssue(
                        "phase_order",
                        f"task {task.task_id}: {current.phase_id} starts before "
                        f"{previous.phase_id} ends",
                    )
                )
            phase_spec = task.phases[index]
            if phase_spec.resource == "human" and current.start > previous.end:
                queue_time += current.start - previous.end
                blocked_intervals.append((previous.end, current.start))

        start = assignment_time
        end = intervals[-1].end
        task_spans[task.task_id] = (start, end, assignment_agent)
        for phase_spec, interval in zip(task.phases, intervals, strict=True):
            if phase_spec.resource == "human":
                human_intervals.append(
                    (interval.start, interval.end, f"{task.task_id}.{phase_spec.phase_id}")
                )
                human_busy += interval.end - interval.start

    for task in scenario.tasks:
        task_start = task_spans[task.task_id][0]
        for predecessor in task.predecessors:
            predecessor_end = task_spans[predecessor][1]
            if task_start < predecessor_end:
                issues.append(
                    ValidationIssue(
                        "precedence",
                        f"task {task.task_id} starts at {task_start} before "
                        f"predecessor {predecessor} ends at {predecessor_end}",
                    )
                )

    for agent in range(1, scenario.p + 1):
        spans = [
            (start, end, task_id)
            for task_id, (start, end, task_agent) in task_spans.items()
            if task_agent == agent
        ]
        issues.extend(
            _overlap_issues(
                spans,
                code="agent_overlap",
                resource_name=f"agent {agent}",
            )
        )

    issues.extend(
        _overlap_issues(
            human_intervals,
            code="human_overlap",
            resource_name="human",
        )
    )

    makespan = max(interval.end for interval in schedule.phases)
    metrics = ScheduleMetrics(
        makespan=makespan,
        queue_time=queue_time,
        blocked_agent_time=queue_time,
        blocked_any_time=_union_duration(blocked_intervals),
        human_busy_time=human_busy,
    )
    bounds = compute_aggregates(scenario)
    if makespan + scenario.tolerance < bounds.b4:
        issues.append(
            ValidationIssue(
                "lower_bound",
                f"makespan {makespan} is below B4={bounds.b4}",
            )
        )
    occupancy_bound = (bounds.w4 + queue_time) / Decimal(scenario.p)
    if makespan + scenario.tolerance < occupancy_bound:
        issues.append(
            ValidationIssue(
                "queue_bound",
                f"makespan {makespan} is below (W4+Q)/P={occupancy_bound}",
            )
        )
    return ScheduleValidation(not issues, tuple(issues), metrics)
