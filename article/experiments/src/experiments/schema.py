from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Literal

import yaml

ResourceType = Literal["agent", "human"]


class ScenarioError(ValueError):
    """Raised when a scenario violates schema v1."""


def decimal(value: Any, *, field: str) -> Decimal:
    if isinstance(value, bool):
        raise ScenarioError(f"{field}: boolean is not a decimal")
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError) as error:
        raise ScenarioError(f"{field}: invalid decimal {value!r}") from error
    if not result.is_finite():
        raise ScenarioError(f"{field}: value must be finite")
    return result


@dataclass(frozen=True)
class PhaseSpec:
    phase_id: str
    resource: ResourceType
    base_duration: Decimal


@dataclass(frozen=True)
class TaskSpec:
    task_id: str
    name: str
    z: Decimal
    k: Decimal
    h: Decimal
    predecessors: tuple[str, ...]
    phases: tuple[PhaseSpec, ...]
    quality_gate_id: str = ""

    @property
    def a(self) -> Decimal:
        return self.k - self.h


@dataclass(frozen=True)
class PhaseInterval:
    task_id: str
    phase_id: str
    agent: int
    start: Decimal
    end: Decimal


@dataclass(frozen=True)
class TaskAssignment:
    task_id: str
    agent: int
    assigned_at: Decimal


@dataclass(frozen=True)
class ScheduleSpec:
    schedule_id: str
    expected_valid: bool
    expected_makespan: Decimal | None
    expected_queue: Decimal | None
    phases: tuple[PhaseInterval, ...]
    assignments: tuple[TaskAssignment, ...] = ()


@dataclass(frozen=True)
class Scenario:
    schema_version: int
    scenario_id: str
    variant_id: str
    time_unit: Decimal
    tolerance: Decimal
    x: Decimal
    p: int
    c: Decimal
    gamma: Decimal
    tasks: tuple[TaskSpec, ...]
    schedules: tuple[ScheduleSpec, ...]
    source_path: Path

    @property
    def task_by_id(self) -> dict[str, TaskSpec]:
        return {task.task_id: task for task in self.tasks}

    @property
    def schedule_by_id(self) -> dict[str, ScheduleSpec]:
        return {schedule.schedule_id: schedule for schedule in self.schedules}

    def to_ticks(self, value: Decimal, *, field: str) -> int:
        ticks = value / self.time_unit
        integral = ticks.to_integral_value()
        if ticks != integral:
            raise ScenarioError(
                f"{field}: {value} is not divisible by time_unit={self.time_unit}"
            )
        return int(integral)

    def from_ticks(self, ticks: int | float) -> Decimal:
        return Decimal(str(ticks)) * self.time_unit

    def effective_phase_duration(self, phase: PhaseSpec) -> Decimal:
        multiplier = self.c if phase.resource == "agent" else self.gamma
        return phase.base_duration * multiplier


def _require_mapping(raw: Any, *, field: str) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise ScenarioError(f"{field}: expected mapping")
    return raw


def _require_list(raw: Any, *, field: str) -> list[Any]:
    if not isinstance(raw, list):
        raise ScenarioError(f"{field}: expected list")
    return raw


def _load_phase(raw: Any, *, task_id: str, index: int) -> PhaseSpec:
    data = _require_mapping(raw, field=f"tasks.{task_id}.phases[{index}]")
    phase_id = str(data.get("phase_id", "")).strip()
    resource = str(data.get("resource", "")).strip()
    if not phase_id:
        raise ScenarioError(f"tasks.{task_id}.phases[{index}].phase_id is required")
    if resource not in {"agent", "human"}:
        raise ScenarioError(
            f"tasks.{task_id}.phases[{index}].resource must be agent or human"
        )
    duration = decimal(
        data.get("base_duration"),
        field=f"tasks.{task_id}.phases[{index}].base_duration",
    )
    if duration <= 0:
        raise ScenarioError(
            f"tasks.{task_id}.phases[{index}].base_duration must be positive"
        )
    return PhaseSpec(phase_id, resource, duration)  # type: ignore[arg-type]


def _load_task(raw: Any, *, index: int) -> TaskSpec:
    data = _require_mapping(raw, field=f"tasks[{index}]")
    task_id = str(data.get("task_id", "")).strip()
    if not task_id:
        raise ScenarioError(f"tasks[{index}].task_id is required")
    phases = tuple(
        _load_phase(phase, task_id=task_id, index=phase_index)
        for phase_index, phase in enumerate(
            _require_list(data.get("phases"), field=f"tasks.{task_id}.phases")
        )
    )
    if not phases:
        raise ScenarioError(f"tasks.{task_id}.phases must not be empty")
    predecessors = tuple(
        str(item)
        for item in _require_list(
            data.get("predecessors", []),
            field=f"tasks.{task_id}.predecessors",
        )
    )
    return TaskSpec(
        task_id=task_id,
        name=str(data.get("name", task_id)),
        z=decimal(data.get("z"), field=f"tasks.{task_id}.z"),
        k=decimal(data.get("k"), field=f"tasks.{task_id}.k"),
        h=decimal(data.get("h"), field=f"tasks.{task_id}.h"),
        predecessors=predecessors,
        phases=phases,
        quality_gate_id=str(data.get("quality_gate_id", task_id)).strip(),
    )


def _load_interval(raw: Any, *, schedule_id: str, index: int) -> PhaseInterval:
    data = _require_mapping(raw, field=f"schedules.{schedule_id}.phases[{index}]")
    return PhaseInterval(
        task_id=str(data.get("task_id", "")),
        phase_id=str(data.get("phase_id", "")),
        agent=int(data.get("agent")),
        start=decimal(
            data.get("start"),
            field=f"schedules.{schedule_id}.phases[{index}].start",
        ),
        end=decimal(
            data.get("end"),
            field=f"schedules.{schedule_id}.phases[{index}].end",
        ),
    )


def _load_assignment(raw: Any, *, schedule_id: str, index: int) -> TaskAssignment:
    data = _require_mapping(
        raw,
        field=f"schedules.{schedule_id}.assignments[{index}]",
    )
    return TaskAssignment(
        task_id=str(data.get("task_id", "")),
        agent=int(data.get("agent")),
        assigned_at=decimal(
            data.get("assigned_at"),
            field=f"schedules.{schedule_id}.assignments[{index}].assigned_at",
        ),
    )


def _load_schedule(schedule_id: str, raw: Any) -> ScheduleSpec:
    data = _require_mapping(raw, field=f"schedules.{schedule_id}")
    expected_makespan = data.get("expected_makespan")
    expected_queue = data.get("expected_queue")
    phases = tuple(
        _load_interval(interval, schedule_id=schedule_id, index=index)
        for index, interval in enumerate(
            _require_list(
                data.get("phases"),
                field=f"schedules.{schedule_id}.phases",
            )
        )
    )
    assignments_raw = data.get("assignments")
    if assignments_raw is None:
        first_by_task: dict[str, PhaseInterval] = {}
        for interval in phases:
            current = first_by_task.get(interval.task_id)
            if current is None or interval.start < current.start:
                first_by_task[interval.task_id] = interval
        assignments = tuple(
            TaskAssignment(
                task_id=task_id,
                agent=interval.agent,
                assigned_at=interval.start,
            )
            for task_id, interval in sorted(first_by_task.items())
        )
    else:
        assignments = tuple(
            _load_assignment(item, schedule_id=schedule_id, index=index)
            for index, item in enumerate(
                _require_list(
                    assignments_raw,
                    field=f"schedules.{schedule_id}.assignments",
                )
            )
        )
    return ScheduleSpec(
        schedule_id=schedule_id,
        expected_valid=bool(data.get("expected_valid", True)),
        expected_makespan=(
            decimal(
                expected_makespan,
                field=f"schedules.{schedule_id}.expected_makespan",
            )
            if expected_makespan is not None
            else None
        ),
        expected_queue=(
            decimal(expected_queue, field=f"schedules.{schedule_id}.expected_queue")
            if expected_queue is not None
            else None
        ),
        phases=phases,
        assignments=assignments,
    )


def load_scenario(path: str | Path) -> Scenario:
    source_path = Path(path).resolve()
    with source_path.open("r", encoding="utf-8") as source:
        raw = yaml.safe_load(source)
    data = _require_mapping(raw, field="scenario")
    tasks = tuple(
        _load_task(task, index=index)
        for index, task in enumerate(_require_list(data.get("tasks"), field="tasks"))
    )
    schedules_raw = _require_mapping(data.get("schedules", {}), field="schedules")
    schedules = tuple(
        _load_schedule(str(schedule_id), schedule)
        for schedule_id, schedule in schedules_raw.items()
    )
    scenario = Scenario(
        schema_version=int(data.get("schema_version", 0)),
        scenario_id=str(data.get("scenario_id", "")).strip(),
        variant_id=str(data.get("variant_id", "")).strip(),
        time_unit=decimal(data.get("time_unit"), field="time_unit"),
        tolerance=decimal(data.get("tolerance", "0"), field="tolerance"),
        x=decimal(data.get("x"), field="x"),
        p=int(data.get("p")),
        c=decimal(data.get("c", "1"), field="c"),
        gamma=decimal(data.get("gamma", "1"), field="gamma"),
        tasks=tasks,
        schedules=schedules,
        source_path=source_path,
    )
    validate_scenario(scenario)
    return scenario


def validate_scenario(scenario: Scenario) -> None:
    if scenario.schema_version != 1:
        raise ScenarioError(
            f"schema_version must be 1, got {scenario.schema_version}"
        )
    if not scenario.scenario_id or not scenario.variant_id:
        raise ScenarioError("scenario_id and variant_id are required")
    if scenario.time_unit <= 0 or scenario.tolerance < 0:
        raise ScenarioError("time_unit must be positive and tolerance non-negative")
    if scenario.x <= 0 or scenario.p <= 0:
        raise ScenarioError("x and p must be positive")
    if scenario.c < 1 or scenario.gamma < 1:
        raise ScenarioError("c and gamma must be at least 1")
    if not scenario.tasks:
        raise ScenarioError("tasks must not be empty")

    task_ids = [task.task_id for task in scenario.tasks]
    if len(task_ids) != len(set(task_ids)):
        raise ScenarioError("task_id values must be unique")
    known = set(task_ids)
    for task in scenario.tasks:
        if task.z <= 0 or task.k < 0 or task.h < 0 or task.h > task.k:
            raise ScenarioError(
                f"task {task.task_id}: require z>0 and 0<=h<=k"
            )
        if task.task_id in task.predecessors:
            raise ScenarioError(f"task {task.task_id}: self-dependency")
        unknown = set(task.predecessors) - known
        if unknown:
            raise ScenarioError(
                f"task {task.task_id}: unknown predecessors {sorted(unknown)}"
            )
        phase_ids = [phase.phase_id for phase in task.phases]
        if len(phase_ids) != len(set(phase_ids)):
            raise ScenarioError(f"task {task.task_id}: duplicate phase_id")

        expected_agent = task.z * scenario.x * task.a
        expected_human = task.z * scenario.x * task.h
        actual_agent = sum(
            (phase.base_duration for phase in task.phases if phase.resource == "agent"),
            Decimal("0"),
        )
        actual_human = sum(
            (phase.base_duration for phase in task.phases if phase.resource == "human"),
            Decimal("0"),
        )
        if actual_agent != expected_agent or actual_human != expected_human:
            raise ScenarioError(
                f"task {task.task_id}: phase sums agent={actual_agent}, "
                f"human={actual_human}; expected agent={expected_agent}, "
                f"human={expected_human}"
            )
        for phase in task.phases:
            scenario.to_ticks(
                scenario.effective_phase_duration(phase),
                field=f"task {task.task_id} phase {phase.phase_id}",
            )

    _topological_task_ids(scenario)
    schedule_ids = [schedule.schedule_id for schedule in scenario.schedules]
    if len(schedule_ids) != len(set(schedule_ids)):
        raise ScenarioError("schedule_id values must be unique")


def _topological_task_ids(scenario: Scenario) -> tuple[str, ...]:
    predecessors = {
        task.task_id: set(task.predecessors) for task in scenario.tasks
    }
    successors: dict[str, set[str]] = {task.task_id: set() for task in scenario.tasks}
    for task in scenario.tasks:
        for predecessor in task.predecessors:
            successors[predecessor].add(task.task_id)
    ready = sorted(task_id for task_id, items in predecessors.items() if not items)
    order: list[str] = []
    while ready:
        task_id = ready.pop(0)
        order.append(task_id)
        for successor in sorted(successors[task_id]):
            predecessors[successor].remove(task_id)
            if not predecessors[successor]:
                ready.append(successor)
                ready.sort()
    if len(order) != len(scenario.tasks):
        raise ScenarioError("task graph contains a cycle")
    return tuple(order)


def topological_task_ids(scenario: Scenario) -> tuple[str, ...]:
    return _topological_task_ids(scenario)
