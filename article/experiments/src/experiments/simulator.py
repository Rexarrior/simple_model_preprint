from __future__ import annotations

from decimal import Decimal

from .schema import (
    PhaseInterval,
    Scenario,
    ScheduleSpec,
    TaskAssignment,
    topological_task_ids,
)


def _task_weights(scenario: Scenario) -> dict[str, Decimal]:
    return {
        task.task_id: sum(
            (scenario.effective_phase_duration(phase) for phase in task.phases),
            Decimal("0"),
        )
        for task in scenario.tasks
    }


def _bottom_levels(scenario: Scenario) -> dict[str, Decimal]:
    weights = _task_weights(scenario)
    successors: dict[str, list[str]] = {
        task.task_id: [] for task in scenario.tasks
    }
    for task in scenario.tasks:
        for predecessor in task.predecessors:
            successors[predecessor].append(task.task_id)

    bottom_levels: dict[str, Decimal] = {}
    for task_id in reversed(topological_task_ids(scenario)):
        tail = max(
            (bottom_levels[successor] for successor in successors[task_id]),
            default=Decimal("0"),
        )
        bottom_levels[task_id] = weights[task_id] + tail
    return bottom_levels


def simulate_baseline(scenario: Scenario) -> ScheduleSpec:
    """Build a deterministic non-preemptive M4 list schedule.

    Ready tasks are ranked by decreasing bottom level, then decreasing task
    weight and task id. Human requests use FCFS; bottom level and identifiers
    break simultaneous-request ties.
    """

    tasks = scenario.task_by_id
    weights = _task_weights(scenario)
    bottom_levels = _bottom_levels(scenario)

    def task_key(task_id: str) -> tuple[Decimal, Decimal, str]:
        return (-bottom_levels[task_id], -weights[task_id], task_id)

    assignments: dict[str, TaskAssignment] = {}
    agent_tasks: dict[int, str | None] = {
        agent: None for agent in range(1, scenario.p + 1)
    }
    completed: set[str] = set()
    phase_cursor: dict[str, int] = {}
    running_agent: dict[str, tuple[int, Decimal]] = {}
    running_human: tuple[str, int, Decimal] | None = None
    human_queue: list[tuple[Decimal, str, int]] = []
    intervals: list[PhaseInterval] = []

    now = Decimal("0")

    def offer_next_phase(task_id: str, request_time: Decimal) -> None:
        phase_index = phase_cursor[task_id]
        phase = tasks[task_id].phases[phase_index]
        if phase.resource == "human":
            human_queue.append((request_time, task_id, phase_index))
            return
        duration = scenario.effective_phase_duration(phase)
        end = request_time + duration
        running_agent[task_id] = (phase_index, end)
        intervals.append(
            PhaseInterval(
                task_id=task_id,
                phase_id=phase.phase_id,
                agent=assignments[task_id].agent,
                start=request_time,
                end=end,
            )
        )

    def assign_ready_tasks(assignment_time: Decimal) -> None:
        ready = sorted(
            (
                task.task_id
                for task in scenario.tasks
                if task.task_id not in assignments
                and all(item in completed for item in task.predecessors)
            ),
            key=task_key,
        )
        free_agents = [
            agent for agent, task_id in agent_tasks.items() if task_id is None
        ]
        for task_id, agent in zip(ready, free_agents, strict=False):
            assignment = TaskAssignment(task_id, agent, assignment_time)
            assignments[task_id] = assignment
            agent_tasks[agent] = task_id
            phase_cursor[task_id] = 0
            offer_next_phase(task_id, assignment_time)

    def start_human_if_possible(start_time: Decimal) -> None:
        nonlocal running_human
        if running_human is not None or not human_queue:
            return
        human_queue.sort(
            key=lambda item: (
                item[0],
                -bottom_levels[item[1]],
                item[1],
                item[2],
            )
        )
        _, task_id, phase_index = human_queue.pop(0)
        phase = tasks[task_id].phases[phase_index]
        duration = scenario.effective_phase_duration(phase)
        end = start_time + duration
        running_human = (task_id, phase_index, end)
        intervals.append(
            PhaseInterval(
                task_id=task_id,
                phase_id=phase.phase_id,
                agent=assignments[task_id].agent,
                start=start_time,
                end=end,
            )
        )

    assign_ready_tasks(now)
    start_human_if_possible(now)

    while len(completed) < len(scenario.tasks):
        event_times = [end for _, end in running_agent.values()]
        if running_human is not None:
            event_times.append(running_human[2])
        if not event_times:
            remaining = sorted(set(tasks) - completed)
            raise RuntimeError(f"baseline scheduler deadlocked on tasks {remaining}")
        now = min(event_times)

        finished: set[str] = set()
        for task_id, (phase_index, end) in list(running_agent.items()):
            if end != now:
                continue
            del running_agent[task_id]
            phase_cursor[task_id] = phase_index + 1
            finished.add(task_id)

        if running_human is not None and running_human[2] == now:
            task_id, phase_index, _ = running_human
            running_human = None
            phase_cursor[task_id] = phase_index + 1
            finished.add(task_id)

        continuing: list[str] = []
        for task_id in finished:
            if phase_cursor[task_id] == len(tasks[task_id].phases):
                completed.add(task_id)
                agent_tasks[assignments[task_id].agent] = None
            else:
                continuing.append(task_id)

        for task_id in sorted(continuing, key=task_key):
            offer_next_phase(task_id, now)

        assign_ready_tasks(now)
        start_human_if_possible(now)

    phase_order = {
        (task.task_id, phase.phase_id): index
        for task in scenario.tasks
        for index, phase in enumerate(task.phases)
    }
    intervals.sort(
        key=lambda item: (
            item.start,
            item.end,
            item.task_id,
            phase_order[(item.task_id, item.phase_id)],
        )
    )
    return ScheduleSpec(
        schedule_id="deterministic_baseline",
        expected_valid=True,
        expected_makespan=None,
        expected_queue=None,
        phases=tuple(intervals),
        assignments=tuple(
            assignments[task_id]
            for task_id in sorted(assignments, key=task_key)
        ),
    )
