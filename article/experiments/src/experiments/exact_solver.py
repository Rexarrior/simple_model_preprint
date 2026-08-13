from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_CEILING

from ortools.sat.python import cp_model

from .bounds import compute_aggregates
from .schema import PhaseInterval, Scenario, ScheduleSpec, TaskAssignment


@dataclass(frozen=True)
class ExactSolution:
    status: str
    objective: Decimal | None
    best_bound: Decimal | None
    relative_gap: Decimal | None
    wall_time: float
    schedule: ScheduleSpec | None


@dataclass
class _TaskVariables:
    starts: list[cp_model.IntVar]
    ends: list[cp_model.IntVar]
    agent_literals: list[cp_model.IntVar]
    span_size: cp_model.IntVar


def _status_name(status: cp_model.CpSolverStatus) -> str:
    names = {
        cp_model.OPTIMAL: "OPTIMAL",
        cp_model.FEASIBLE: "FEASIBLE",
        cp_model.INFEASIBLE: "INFEASIBLE",
        cp_model.MODEL_INVALID: "MODEL_INVALID",
        cp_model.UNKNOWN: "UNKNOWN",
    }
    return names.get(status, f"STATUS_{status}")


def solve_exact(
    scenario: Scenario,
    *,
    time_limit_seconds: float = 300.0,
    random_seed: int = 0,
    workers: int = 1,
) -> ExactSolution:
    model = cp_model.CpModel()
    horizon = sum(
        scenario.to_ticks(
            scenario.effective_phase_duration(phase),
            field=f"{task.task_id}.{phase.phase_id}",
        )
        for task in scenario.tasks
        for phase in task.phases
    )
    task_variables: dict[str, _TaskVariables] = {}
    human_intervals: list[cp_model.IntervalVar] = []
    agent_spans: list[list[cp_model.IntervalVar]] = [
        [] for _ in range(scenario.p)
    ]

    for task in scenario.tasks:
        starts: list[cp_model.IntVar] = []
        ends: list[cp_model.IntVar] = []
        for phase in task.phases:
            duration = scenario.to_ticks(
                scenario.effective_phase_duration(phase),
                field=f"{task.task_id}.{phase.phase_id}",
            )
            start = model.new_int_var(0, horizon, f"start_{task.task_id}_{phase.phase_id}")
            end = model.new_int_var(0, horizon, f"end_{task.task_id}_{phase.phase_id}")
            interval = model.new_interval_var(
                start,
                duration,
                end,
                f"phase_{task.task_id}_{phase.phase_id}",
            )
            starts.append(start)
            ends.append(end)
            if phase.resource == "human":
                human_intervals.append(interval)

        for index in range(1, len(starts)):
            model.add(starts[index] >= ends[index - 1])

        span_size = model.new_int_var(1, horizon, f"span_size_{task.task_id}")
        model.add(span_size == ends[-1] - starts[0])
        literals: list[cp_model.IntVar] = []
        for agent in range(scenario.p):
            literal = model.new_bool_var(f"task_{task.task_id}_agent_{agent + 1}")
            span = model.new_optional_interval_var(
                starts[0],
                span_size,
                ends[-1],
                literal,
                f"span_{task.task_id}_agent_{agent + 1}",
            )
            agent_spans[agent].append(span)
            literals.append(literal)
        model.add_exactly_one(literals)
        task_variables[task.task_id] = _TaskVariables(
            starts=starts,
            ends=ends,
            agent_literals=literals,
            span_size=span_size,
        )

    if human_intervals:
        model.add_no_overlap(human_intervals)
    for spans in agent_spans:
        model.add_no_overlap(spans)

    for task in scenario.tasks:
        variables = task_variables[task.task_id]
        for predecessor in task.predecessors:
            model.add(
                variables.starts[0]
                >= task_variables[predecessor].ends[-1]
            )

    makespan = model.new_int_var(0, horizon, "makespan")
    model.add_max_equality(
        makespan,
        [variables.ends[-1] for variables in task_variables.values()],
    )
    lower_bound = int(
        (compute_aggregates(scenario).b4 / scenario.time_unit).to_integral_value(
            rounding=ROUND_CEILING,
        )
    )
    model.add(makespan >= lower_bound)
    model.minimize(makespan)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit_seconds
    solver.parameters.num_search_workers = workers
    solver.parameters.random_seed = random_seed
    status_code = solver.solve(model)
    status = _status_name(status_code)
    if status_code not in {cp_model.OPTIMAL, cp_model.FEASIBLE}:
        return ExactSolution(
            status=status,
            objective=None,
            best_bound=None,
            relative_gap=None,
            wall_time=solver.wall_time,
            schedule=None,
        )

    objective_ticks = int(round(solver.objective_value))
    best_bound_ticks = Decimal(str(solver.best_objective_bound))
    objective = scenario.from_ticks(objective_ticks)
    best_bound = best_bound_ticks * scenario.time_unit
    relative_gap = (
        Decimal("0")
        if objective == 0
        else (objective - best_bound) / objective
    )
    phase_intervals: list[PhaseInterval] = []
    assignments: list[TaskAssignment] = []
    for task in scenario.tasks:
        variables = task_variables[task.task_id]
        agent = next(
            index + 1
            for index, literal in enumerate(variables.agent_literals)
            if solver.value(literal)
        )
        assignments.append(
            TaskAssignment(
                task_id=task.task_id,
                agent=agent,
                assigned_at=scenario.from_ticks(solver.value(variables.starts[0])),
            )
        )
        for phase, start, end in zip(
            task.phases,
            variables.starts,
            variables.ends,
            strict=True,
        ):
            phase_intervals.append(
                PhaseInterval(
                    task_id=task.task_id,
                    phase_id=phase.phase_id,
                    agent=agent,
                    start=scenario.from_ticks(solver.value(start)),
                    end=scenario.from_ticks(solver.value(end)),
                )
            )
    schedule = ScheduleSpec(
        schedule_id="exact_solution",
        expected_valid=True,
        expected_makespan=objective,
        expected_queue=None,
        phases=tuple(phase_intervals),
        assignments=tuple(assignments),
    )
    return ExactSolution(
        status=status,
        objective=objective,
        best_bound=best_bound,
        relative_gap=relative_gap,
        wall_time=solver.wall_time,
        schedule=schedule,
    )
