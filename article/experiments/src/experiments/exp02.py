from __future__ import annotations

import csv
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from decimal import Decimal
import hashlib
import importlib.metadata
import json
from pathlib import Path
from typing import Any, Iterator

import yaml

from .bounds import AggregateMetrics, compute_aggregates
from .exact_solver import ExactSolution, solve_exact
from .exp02_figures import build_active_constraint_map, build_scaling_curve
from .generators import build_exp01_scenario, load_exp01_matrix
from .provenance import git_provenance
from .schema import (
    PhaseSpec,
    Scenario,
    ScenarioError,
    ScheduleSpec,
    TaskSpec,
    decimal,
    load_scenario,
    validate_scenario,
)
from .simulator import simulate_baseline
from .validator import ScheduleValidation, validate_schedule


@dataclass(frozen=True)
class Exp02Object:
    object_id: str
    source: str
    construction: str
    phase_profile: str
    topology: str | None = None
    task_count: int | None = None
    task_weight_cycle: tuple[Decimal, ...] = ()


@dataclass(frozen=True)
class Exp02Regime:
    regime_id: str
    slice_id: str
    c_model: str
    gamma_model: str
    human_share: Decimal


@dataclass(frozen=True)
class Exp02Matrix:
    source_path: Path
    schema_version: int
    experiment_id: str
    frozen_at: str
    expected_point_count: int
    objects: tuple[Exp02Object, ...]
    agent_counts: tuple[int, ...]
    human_shares: tuple[Decimal, ...]
    time_unit: Decimal
    tolerance: Decimal
    regimes: tuple[Exp02Regime, ...]
    policy_id: str
    solver_time_limit_seconds: float
    solver_random_seed: int
    solver_workers: int

    @property
    def point_count(self) -> int:
        return len(self.objects) * len(self.regimes) * len(self.agent_counts)


@dataclass(frozen=True)
class Exp02Case:
    object_spec: Exp02Object
    regime: Exp02Regime
    agent_count: int
    scenario: Scenario


def _required_list(raw: object, *, field: str) -> list[object]:
    if not isinstance(raw, list) or not raw:
        raise ScenarioError(f"{field}: expected non-empty list")
    return raw


def _required_mapping(raw: object, *, field: str) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise ScenarioError(f"{field}: expected mapping")
    return raw


def load_exp02_matrix(path: str | Path) -> Exp02Matrix:
    source_path = Path(path).resolve()
    with source_path.open("r", encoding="utf-8") as source:
        raw = yaml.safe_load(source)
    data = _required_mapping(raw, field="EXP-02 matrix")
    if data.get("frozen") is not True:
        raise ScenarioError("EXP-02 matrix must be frozen before execution")

    objects: list[Exp02Object] = []
    for index, item in enumerate(_required_list(data.get("objects"), field="objects")):
        spec = _required_mapping(item, field=f"objects[{index}]")
        objects.append(
            Exp02Object(
                object_id=str(spec.get("object_id", "")),
                source=str(spec.get("source", "")),
                construction=str(spec.get("construction", "")),
                phase_profile=str(spec.get("phase_profile", "")),
                topology=(
                    str(spec["topology"]) if spec.get("topology") is not None else None
                ),
                task_count=(
                    int(spec["task_count"])
                    if spec.get("task_count") is not None
                    else None
                ),
                task_weight_cycle=tuple(
                    decimal(value, field=f"objects[{index}].task_weight_cycle")
                    for value in spec.get("task_weight_cycle", [])
                ),
            )
        )

    regimes: list[Exp02Regime] = []
    for index, item in enumerate(_required_list(data.get("regimes"), field="regimes")):
        spec = _required_mapping(item, field=f"regimes[{index}]")
        regimes.append(
            Exp02Regime(
                regime_id=str(spec.get("regime_id", "")),
                slice_id=str(spec.get("slice_id", "")),
                c_model=str(spec.get("c_model", "")),
                gamma_model=str(spec.get("gamma_model", "")),
                human_share=decimal(
                    spec.get("human_share"), field=f"regimes[{index}].human_share"
                ),
            )
        )

    exact = _required_mapping(data.get("exact_solver"), field="exact_solver")
    baseline = _required_mapping(data.get("baseline_policy"), field="baseline_policy")
    matrix = Exp02Matrix(
        source_path=source_path,
        schema_version=int(data.get("schema_version", 0)),
        experiment_id=str(data.get("experiment_id", "")),
        frozen_at=str(data.get("frozen_at", "")),
        expected_point_count=int(data.get("expected_point_count", 0)),
        objects=tuple(objects),
        agent_counts=tuple(
            int(item)
            for item in _required_list(data.get("agent_counts"), field="agent_counts")
        ),
        human_shares=tuple(
            decimal(item, field="human_shares")
            for item in _required_list(data.get("human_shares"), field="human_shares")
        ),
        time_unit=decimal(data.get("time_unit"), field="time_unit"),
        tolerance=decimal(data.get("tolerance"), field="tolerance"),
        regimes=tuple(regimes),
        policy_id=str(baseline.get("policy_id", "")),
        solver_time_limit_seconds=float(exact.get("time_limit_seconds", 60)),
        solver_random_seed=int(exact.get("random_seed", 0)),
        solver_workers=int(exact.get("workers", 1)),
    )
    _validate_matrix(matrix)
    return matrix


def _validate_matrix(matrix: Exp02Matrix) -> None:
    if matrix.schema_version != 1 or matrix.experiment_id != "EXP-02":
        raise ScenarioError("EXP-02 matrix requires schema_version=1 and experiment_id=EXP-02")
    if tuple(item.object_id for item in matrix.objects) != (
        "practical_v4",
        "fork_join_n4",
    ):
        raise ScenarioError("EXP-02 must contain the frozen practical and fork-join objects")
    if matrix.agent_counts != (1, 2, 3, 4, 6, 8, 12):
        raise ScenarioError("EXP-02 agent counts differ from the frozen design")
    if matrix.human_shares != (Decimal("0.10"), Decimal("0.25"), Decimal("0.50")):
        raise ScenarioError("EXP-02 human shares differ from the frozen design")
    expected_regimes = {
        "c0_g0_rh10",
        "c0_g0_rh25",
        "c0_g0_rh50",
        "c1_g0_rh25",
        "c0_g1_rh25",
    }
    if {item.regime_id for item in matrix.regimes} != expected_regimes:
        raise ScenarioError("EXP-02 regimes differ from the frozen design")
    if len({item.regime_id for item in matrix.regimes}) != len(matrix.regimes):
        raise ScenarioError("EXP-02 regime identifiers must be unique")
    if any(item.human_share not in matrix.human_shares for item in matrix.regimes):
        raise ScenarioError("EXP-02 regime uses an undeclared human share")
    if any(item.c_model not in {"C0", "C1"} for item in matrix.regimes):
        raise ScenarioError("EXP-02 supports only C0 and C1")
    if any(item.gamma_model not in {"gamma0", "gamma1"} for item in matrix.regimes):
        raise ScenarioError("EXP-02 supports only gamma0 and gamma1")
    if matrix.time_unit <= 0 or matrix.tolerance < 0:
        raise ScenarioError("EXP-02 time unit or tolerance is invalid")
    if matrix.solver_workers != 1:
        raise ScenarioError("EXP-02 exact runs are frozen to one worker")
    if not matrix.policy_id:
        raise ScenarioError("EXP-02 baseline policy_id is required")
    if matrix.point_count != matrix.expected_point_count:
        raise ScenarioError(
            f"EXP-02 point count mismatch: expected {matrix.expected_point_count}, "
            f"got {matrix.point_count}"
        )


def c_multiplier(model: str, p: int) -> Decimal:
    slots = Decimal(p)
    if model == "C0":
        return Decimal("1")
    if model == "C1":
        return (
            Decimal("1")
            + Decimal("0.05") * (slots - 1)
            + Decimal("0.005") * slots * (slots - 1)
        )
    raise ScenarioError(f"unknown C model {model}")


def gamma_multiplier(model: str, p: int) -> Decimal:
    slots = Decimal(p)
    if model == "gamma0":
        return Decimal("1")
    if model == "gamma1":
        return Decimal("1") + Decimal("0.10") * (slots - 1)
    raise ScenarioError(f"unknown gamma model {model}")


def _rescaled_phases(
    source_task: TaskSpec,
    *,
    agent_total: Decimal,
    human_total: Decimal,
) -> tuple[PhaseSpec, ...]:
    source_totals = {
        resource: sum(
            (
                phase.base_duration
                for phase in source_task.phases
                if phase.resource == resource
            ),
            Decimal("0"),
        )
        for resource in ("agent", "human")
    }
    targets = {"agent": agent_total, "human": human_total}
    phases: list[PhaseSpec] = []
    for phase in source_task.phases:
        source_total = source_totals[phase.resource]
        if source_total <= 0:
            raise ScenarioError(
                f"task {source_task.task_id}: cannot rescale empty {phase.resource} phases"
            )
        phases.append(
            PhaseSpec(
                phase_id=phase.phase_id,
                resource=phase.resource,
                base_duration=targets[phase.resource]
                * phase.base_duration
                / source_total,
            )
        )
    return tuple(phases)


def _build_practical_scenario(
    matrix: Exp02Matrix,
    object_spec: Exp02Object,
    regime: Exp02Regime,
    agent_count: int,
) -> Scenario:
    project_root = matrix.source_path.parents[2]
    source = load_scenario(project_root / object_spec.source)
    tasks: list[TaskSpec] = []
    for task in source.tasks:
        human_coefficient = task.k * regime.human_share
        agent_coefficient = task.k - human_coefficient
        tasks.append(
            TaskSpec(
                task_id=task.task_id,
                name=task.name,
                z=task.z,
                k=task.k,
                h=human_coefficient,
                predecessors=task.predecessors,
                phases=_rescaled_phases(
                    task,
                    agent_total=source.x * task.z * agent_coefficient,
                    human_total=source.x * task.z * human_coefficient,
                ),
                quality_gate_id=task.quality_gate_id,
            )
        )
    scenario = Scenario(
        schema_version=1,
        scenario_id=(
            f"exp02_{object_spec.object_id}_{regime.regime_id}_p{agent_count:02d}"
        ),
        variant_id="EXP-02-practical-v4",
        time_unit=matrix.time_unit,
        tolerance=matrix.tolerance,
        x=source.x,
        p=agent_count,
        c=c_multiplier(regime.c_model, agent_count),
        gamma=gamma_multiplier(regime.gamma_model, agent_count),
        tasks=tuple(tasks),
        schedules=(),
        source_path=matrix.source_path,
    )
    validate_scenario(scenario)
    return scenario


def _build_fork_join_scenario(
    matrix: Exp02Matrix,
    object_spec: Exp02Object,
    regime: Exp02Regime,
    agent_count: int,
) -> Scenario:
    project_root = matrix.source_path.parents[2]
    source_matrix = load_exp01_matrix(project_root / object_spec.source)
    if object_spec.topology is None or object_spec.task_count is None:
        raise ScenarioError("canonical EXP-02 object requires topology and task_count")
    if object_spec.task_weight_cycle != source_matrix.task_weight_cycle:
        raise ScenarioError(
            "canonical EXP-02 task weights differ from the referenced EXP-01 matrix"
        )
    base = build_exp01_scenario(
        source_matrix,
        topology=object_spec.topology,
        task_count=object_spec.task_count,
        agent_count=agent_count,
        human_share=regime.human_share,
        phase_profile=object_spec.phase_profile,
    )
    scenario = replace(
        base,
        scenario_id=(
            f"exp02_{object_spec.object_id}_{regime.regime_id}_p{agent_count:02d}"
        ),
        variant_id="EXP-02-canonical-fork-join",
        time_unit=matrix.time_unit,
        tolerance=matrix.tolerance,
        c=c_multiplier(regime.c_model, agent_count),
        gamma=gamma_multiplier(regime.gamma_model, agent_count),
        source_path=matrix.source_path,
    )
    validate_scenario(scenario)
    return scenario


def build_exp02_scenario(
    matrix: Exp02Matrix,
    *,
    object_spec: Exp02Object,
    regime: Exp02Regime,
    agent_count: int,
) -> Scenario:
    if object_spec.object_id == "practical_v4":
        return _build_practical_scenario(matrix, object_spec, regime, agent_count)
    if object_spec.object_id == "fork_join_n4":
        return _build_fork_join_scenario(matrix, object_spec, regime, agent_count)
    raise ScenarioError(f"unknown EXP-02 object {object_spec.object_id}")


def iter_exp02_cases(matrix: Exp02Matrix) -> Iterator[Exp02Case]:
    for object_spec in matrix.objects:
        for regime in matrix.regimes:
            for agent_count in matrix.agent_counts:
                yield Exp02Case(
                    object_spec=object_spec,
                    regime=regime,
                    agent_count=agent_count,
                    scenario=build_exp02_scenario(
                        matrix,
                        object_spec=object_spec,
                        regime=regime,
                        agent_count=agent_count,
                    ),
                )


def _format_decimal(value: Decimal | None) -> str:
    return "" if value is None else format(value, "f")


def _ratio(numerator: Decimal, denominator: Decimal) -> str:
    if denominator == 0:
        return "0"
    return _format_decimal((numerator / denominator).quantize(Decimal("0.000001")))


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _scenario_payload(scenario: Scenario) -> dict[str, Any]:
    return {
        "schema_version": scenario.schema_version,
        "scenario_id": scenario.scenario_id,
        "time_unit": _format_decimal(scenario.time_unit),
        "tolerance": _format_decimal(scenario.tolerance),
        "x": _format_decimal(scenario.x),
        "p": scenario.p,
        "c": _format_decimal(scenario.c),
        "gamma": _format_decimal(scenario.gamma),
        "tasks": [
            {
                "task_id": task.task_id,
                "z": _format_decimal(task.z),
                "k": _format_decimal(task.k),
                "h": _format_decimal(task.h),
                "predecessors": list(task.predecessors),
                "phases": [
                    {
                        "phase_id": phase.phase_id,
                        "resource": phase.resource,
                        "base_duration": _format_decimal(phase.base_duration),
                    }
                    for phase in task.phases
                ],
            }
            for task in scenario.tasks
        ],
    }


def _json_sha256(payload: object) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _validated(
    scenario: Scenario,
    schedule: ScheduleSpec,
    *,
    label: str,
) -> ScheduleValidation:
    validation = validate_schedule(scenario, schedule)
    if not validation.valid or validation.metrics is None:
        details = "; ".join(issue.message for issue in validation.issues)
        raise RuntimeError(f"{scenario.scenario_id}: invalid {label}: {details}")
    return validation


def _waiting_intervals(
    scenario: Scenario,
    schedule: ScheduleSpec,
) -> list[tuple[Decimal, Decimal]]:
    by_key = {
        (interval.task_id, interval.phase_id): interval for interval in schedule.phases
    }
    assignments = {item.task_id: item for item in schedule.assignments}
    waits: list[tuple[Decimal, Decimal]] = []
    for task in scenario.tasks:
        intervals = [by_key[(task.task_id, phase.phase_id)] for phase in task.phases]
        assignment = assignments[task.task_id]
        if task.phases[0].resource == "human" and intervals[0].start > assignment.assigned_at:
            waits.append((assignment.assigned_at, intervals[0].start))
        for index in range(1, len(task.phases)):
            if task.phases[index].resource != "human":
                continue
            previous = intervals[index - 1]
            current = intervals[index]
            if current.start > previous.end:
                waits.append((previous.end, current.start))
    return waits


def _max_queue(intervals: list[tuple[Decimal, Decimal]]) -> int:
    events: list[tuple[Decimal, int]] = []
    for start, end in intervals:
        events.append((start, 1))
        events.append((end, -1))
    queued = 0
    maximum = 0
    for _, delta in sorted(events, key=lambda item: (item[0], item[1])):
        queued += delta
        maximum = max(maximum, queued)
    return maximum


def _schedule_metrics(
    scenario: Scenario,
    schedule: ScheduleSpec,
    validation: ScheduleValidation,
) -> dict[str, str]:
    assert validation.metrics is not None
    makespan = validation.metrics.makespan
    agent_busy = sum(
        (
            scenario.effective_phase_duration(phase)
            for task in scenario.tasks
            for phase in task.phases
            if phase.resource == "agent"
        ),
        Decimal("0"),
    )
    phase_by_task: dict[str, list[Decimal]] = {}
    for interval in schedule.phases:
        phase_by_task.setdefault(interval.task_id, []).append(interval.end)
    assignments = {item.task_id: item for item in schedule.assignments}
    occupied = sum(
        (
            max(phase_by_task[task.task_id]) - assignments[task.task_id].assigned_at
            for task in scenario.tasks
        ),
        Decimal("0"),
    )
    capacity = Decimal(scenario.p) * makespan
    return {
        "makespan": _format_decimal(makespan),
        "queue_time": _format_decimal(validation.metrics.queue_time),
        "blocked_any": _format_decimal(validation.metrics.blocked_any_time),
        "max_human_queue": str(_max_queue(_waiting_intervals(scenario, schedule))),
        "agent_productive_utilization": _ratio(agent_busy, capacity),
        "agent_slot_utilization": _ratio(occupied, capacity),
        "human_utilization": _ratio(validation.metrics.human_busy_time, makespan),
    }


def _result_row(
    case: Exp02Case,
    aggregate: AggregateMetrics,
    baseline: ScheduleValidation,
    baseline_schedule: ScheduleSpec,
    exact: ExactSolution,
    exact_validation: ScheduleValidation | None,
    policy_id: str,
) -> dict[str, str]:
    assert baseline.metrics is not None
    baseline_values = _schedule_metrics(case.scenario, baseline_schedule, baseline)
    exact_values = (
        _schedule_metrics(case.scenario, exact.schedule, exact_validation)
        if exact.schedule is not None and exact_validation is not None
        else {
            "makespan": "",
            "queue_time": "",
            "blocked_any": "",
            "max_human_queue": "",
            "agent_productive_utilization": "",
            "agent_slot_utilization": "",
            "human_utilization": "",
        }
    )
    objective = exact.objective
    is_optimal = exact.status == "OPTIMAL" and objective is not None
    exact_gap = objective - aggregate.b4 if objective is not None else None
    baseline_gap = (
        baseline.metrics.makespan - objective if is_optimal and objective is not None else None
    )
    return {
        "experiment_id": "EXP-02",
        "scenario_id": case.scenario.scenario_id,
        "scenario_sha256": _json_sha256(_scenario_payload(case.scenario)),
        "object_id": case.object_spec.object_id,
        "phase_profile": case.object_spec.phase_profile,
        "regime_id": case.regime.regime_id,
        "slice_id": case.regime.slice_id,
        "policy_id": policy_id,
        "agent_count": str(case.agent_count),
        "human_share": _format_decimal(case.regime.human_share),
        "c_model": case.regime.c_model,
        "C": _format_decimal(case.scenario.c),
        "gamma_model": case.regime.gamma_model,
        "gamma": _format_decimal(case.scenario.gamma),
        "W4": _format_decimal(aggregate.w4),
        "L4": _format_decimal(aggregate.l4),
        "W4_over_P": _format_decimal(aggregate.work_branch),
        "gamma_H": _format_decimal(aggregate.human_branch),
        "B4": _format_decimal(aggregate.b4),
        "active_branches": ",".join(aggregate.active_branches),
        "critical_path": "->".join(aggregate.critical_path_l4),
        "solver_status": exact.status,
        "exact_makespan": exact_values["makespan"],
        "T_star": exact_values["makespan"] if is_optimal else "",
        "solver_best_bound": _format_decimal(exact.best_bound),
        "solver_gap": _format_decimal(exact.relative_gap),
        "solver_wall_time_seconds": f"{exact.wall_time:.6f}",
        "exact_gap_to_B4": _format_decimal(exact_gap),
        "exact_relative_gap_to_B4": (
            _ratio(exact_gap, aggregate.b4) if exact_gap is not None else ""
        ),
        "exact_queue": exact_values["queue_time"],
        "exact_blocked_any": exact_values["blocked_any"],
        "exact_max_human_queue": exact_values["max_human_queue"],
        "exact_agent_productive_utilization": exact_values[
            "agent_productive_utilization"
        ],
        "exact_agent_slot_utilization": exact_values["agent_slot_utilization"],
        "exact_human_utilization": exact_values["human_utilization"],
        "baseline_makespan": baseline_values["makespan"],
        "baseline_gap_to_optimum": _format_decimal(baseline_gap),
        "baseline_relative_gap": (
            _ratio(baseline_gap, objective)
            if baseline_gap is not None and objective is not None
            else ""
        ),
        "baseline_queue": baseline_values["queue_time"],
        "baseline_blocked_any": baseline_values["blocked_any"],
        "baseline_max_human_queue": baseline_values["max_human_queue"],
        "baseline_agent_productive_utilization": baseline_values[
            "agent_productive_utilization"
        ],
        "baseline_agent_slot_utilization": baseline_values["agent_slot_utilization"],
        "baseline_human_utilization": baseline_values["human_utilization"],
        "delta_T_star_to_next_P": "",
        "delta_baseline_to_next_P": "",
    }


def _add_marginal_gains(rows: list[dict[str, str]]) -> None:
    grouped: dict[tuple[str, str], list[dict[str, str]]] = {}
    for row in rows:
        grouped.setdefault((row["object_id"], row["regime_id"]), []).append(row)
    for selected in grouped.values():
        selected.sort(key=lambda row: int(row["agent_count"]))
        for current, following in zip(selected, selected[1:]):
            if current["T_star"] and following["T_star"]:
                current["delta_T_star_to_next_P"] = _format_decimal(
                    Decimal(current["T_star"]) - Decimal(following["T_star"])
                )
            current["delta_baseline_to_next_P"] = _format_decimal(
                Decimal(current["baseline_makespan"])
                - Decimal(following["baseline_makespan"])
            )


def _argmin(rows: list[dict[str, str]], field: str) -> dict[str, str]:
    return min(rows, key=lambda row: (Decimal(row[field]), int(row["agent_count"])))


def _active_transitions(rows: list[dict[str, str]]) -> str:
    selected = sorted(rows, key=lambda row: int(row["agent_count"]))
    transitions: list[str] = []
    previous = None
    for row in selected:
        active = row["active_branches"].replace(",", "+")
        if active != previous:
            transitions.append(f"P{row['agent_count']}:{active}")
            previous = active
    return ";".join(transitions)


def _summary_rows(
    rows: list[dict[str, str]],
    matrix: Exp02Matrix,
) -> list[dict[str, str]]:
    grouped: dict[tuple[str, str], list[dict[str, str]]] = {}
    for row in rows:
        grouped.setdefault((row["object_id"], row["regime_id"]), []).append(row)
    summaries: list[dict[str, str]] = []
    for (object_id, regime_id), selected in grouped.items():
        selected.sort(key=lambda row: int(row["agent_count"]))
        minimum_b4 = _argmin(selected, "B4")
        minimum_baseline = _argmin(selected, "baseline_makespan")
        all_optimal = all(row["solver_status"] == "OPTIMAL" for row in selected)
        minimum_exact = _argmin(selected, "T_star") if all_optimal else None
        last_exact = Decimal(selected[-1]["T_star"]) if all_optimal else None
        min_exact_value = Decimal(minimum_exact["T_star"]) if minimum_exact else None
        finite = bool(
            minimum_exact
            and int(minimum_exact["agent_count"]) < max(matrix.agent_counts)
            and last_exact is not None
            and min_exact_value is not None
            and last_exact > min_exact_value + matrix.tolerance
        )
        summaries.append(
            {
                "object_id": object_id,
                "regime_id": regime_id,
                "c_model": selected[0]["c_model"],
                "gamma_model": selected[0]["gamma_model"],
                "human_share": selected[0]["human_share"],
                "optimal_points": str(
                    sum(row["solver_status"] == "OPTIMAL" for row in selected)
                ),
                "minimizing_P_B4": minimum_b4["agent_count"],
                "minimum_B4": minimum_b4["B4"],
                "minimizing_P_T_star": (
                    minimum_exact["agent_count"] if minimum_exact else ""
                ),
                "minimum_T_star": minimum_exact["T_star"] if minimum_exact else "",
                "minimizing_P_baseline": minimum_baseline["agent_count"],
                "minimum_baseline": minimum_baseline["baseline_makespan"],
                "observed_finite_optimum_T_star": str(finite).lower(),
                "T_star_at_P1": selected[0]["T_star"],
                "T_star_at_P12": selected[-1]["T_star"],
                "P12_minus_minimum_T_star": (
                    _format_decimal(last_exact - min_exact_value)
                    if last_exact is not None and min_exact_value is not None
                    else ""
                ),
                "active_branch_transitions": _active_transitions(selected),
            }
        )
    return summaries


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise RuntimeError(f"cannot write empty result table {path}")
    with path.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(
            target,
            fieldnames=list(rows[0]),
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def _percent(value: Decimal) -> str:
    return f"{value * Decimal(100):.3f}"


def _write_report(
    path: Path,
    *,
    matrix: Exp02Matrix,
    rows: list[dict[str, str]],
    summaries: list[dict[str, str]],
) -> None:
    optimal_count = sum(row["solver_status"] == "OPTIMAL" for row in rows)
    exact_rows = [row for row in rows if row["T_star"]]
    maximum_gap = max(
        exact_rows,
        key=lambda row: (Decimal(row["exact_relative_gap_to_B4"]), row["scenario_id"]),
    )
    finite = [
        row for row in summaries if row["observed_finite_optimum_T_star"] == "true"
    ]
    summary_lines = "\n".join(
        "| {object_id} | {regime_id} | {p_b4} | {p_exact} | {p_base} | {finite} | {transitions} |".format(
            object_id=row["object_id"],
            regime_id=row["regime_id"],
            p_b4=row["minimizing_P_B4"],
            p_exact=row["minimizing_P_T_star"] or "—",
            p_base=row["minimizing_P_baseline"],
            finite="да" if row["observed_finite_optimum_T_star"] == "true" else "нет",
            transitions=row["active_branch_transitions"],
        )
        for row in summaries
    )
    finite_lines = (
        "\n".join(
            f"- `{row['object_id']}`, `{row['regime_id']}`: "
            f"$P^*={row['minimizing_P_T_star']}$, "
            f"$T^*={row['minimum_T_star']}$ ч; при $P=12$ срок "
            f"на {row['P12_minus_minimum_T_star']} ч больше минимума."
            for row in finite
        )
        if finite
        else "- На заявленной сетке внутренний минимум $T^*$ не обнаружен."
    )
    report = rf"""# Отчёт по EXP-02: масштабирование по числу агентов

Дата отчёта: 2026-08-07

Статус: полная замороженная матрица, {len(rows)} уникальных точек.

## 1. Резюме

До статуса `OPTIMAL` доказаны {optimal_count} из {len(rows)} точек. Exact и
baseline сохранены раздельно; ни один результат `FEASIBLE` не обозначается как
$T^*$. Максимальный доказанный разрыв $T^*/B_4-1$ равен
{_percent(Decimal(maximum_gap['exact_relative_gap_to_B4']))}% в сценарии
`{maximum_gap['scenario_id']}`.

Эксперимент показывает три разных механизма формы кривой: насыщение на
критическом пути или человеческом ресурсе при $C_0,\gamma_0$, рост агентной
работы при $C_1$ и рост длительности человеческих фаз при $\gamma_1$. Активная
ветвь $B_4$ и фактический оптимум сообщаются отдельно, поскольку очередь может
оставлять положительный tightness gap.

## 2. Зафиксированный дизайн

- объекты: структура практического варианта 4 и канонический fork--join при
  $N=4$ с весами 6, 12, 18 и 24;
- для fork--join зафиксирован профиль `alternating-sync` из EXP-01;
- $P\in\{{1,2,3,4,6,8,12\}}$;
- уникальные режимы: три значения $r_h$ при $C_0,\gamma_0$, один срез
  $C_1,\gamma_0,r_h=0.25$ и один срез $C_0,\gamma_1,r_h=0.25$;
- $C_1(P)=1+0.05(P-1)+0.005P(P-1)$;
- $\gamma_1(P)=1+0.10(P-1)$;
- один worker, seed 0, общий лимит 60 секунд на точку.

Практический объект сохраняет DAG, $Z_i$ и полную работу $k_i$ варианта 4, но
доли $r_h$ пересобраны по общему правилу матрицы. Поэтому его часы являются
сценарной чувствительностью структуры примера, а не новой эмпирической оценкой.
Центральная точка $C_0,\gamma_0,r_h=0.25$ общая для двух срезов и не дублируется.

## 3. Кривая чистого масштабирования

![Кривая масштабирования EXP-02](../figures/exp02_scaling_curve.png)

[SVG-версия](../figures/exp02_scaling_curve.svg).

На рисунке соединены только точки одного режима
$C_0,\gamma_0,r_h=0.25$ и одной политики. Три цветные пунктирные линии — ветви
$W_4/P$, $L_4$ и $\gamma H$; чёрная линия — их максимум $B_4$; отдельно
показаны доказанный $T^*$ и срок фиксированной baseline-политики.

## 4. Активные ограничения и конечные минимумы

![Карта активных ограничений EXP-02](../figures/exp02_active_constraints.png)

[SVG-версия](../figures/exp02_active_constraints.svg).

Фон каждой точки кодирует активную ветвь нижней границы. Каждая малая панель
содержит только один набор $C$, $\gamma$, $r_h$ и `policy_id`, поэтому линии не
смешивают разные сценарные условия.

| Объект | Режим | $P$ для min $B_4$ | $P$ для min $T^*$ | $P$ baseline | Внутренний минимум $T^*$ | Переходы активной ветви |
|---|---|---:|---:|---:|---|---|
{summary_lines}

Под «внутренним минимумом» понимается минимум не на правой границе сетки, после
которого доказанный срок к $P=12$ вырос больше tolerance. Обнаруженные случаи:

{finite_lines}

Полные предельные выигрыши $\Delta_P=T(P)-T(P_{{next}})$ сохранены для exact и
baseline в основной таблице. Отрицательное значение означает ухудшение при
переходе к следующему заранее заданному числу агентов.

## 5. Загрузка ресурсов

Для каждого расписания сохранены три разные величины:

- productive agent utilization — доля ёмкости $P\,T$, занятая agent-фазами;
- agent-slot utilization — доля ёмкости, в которой слот удерживается задачей,
  включая human-фазы и ожидание;
- human utilization — занятость единственного человеческого ресурса.

Также сохранены суммарное ожидание, время хотя бы одной блокировки и
максимальное число одновременно ожидающих human-фаз. Эти показатели не
включаются в $W_4$, $L_4$ или $B_4$.

## 6. Воспроизводимость

```bash
cd simple_model_full/experiments
uv sync --python 3.13
uv run pytest -ra
uv run python -m experiments run --experiment EXP-02
```

Артефакты:

- [замороженная матрица](../scenarios/canonical/exp02_matrix.yaml);
- [все {len(rows)} прогона](exp02_runs.csv);
- [минимизирующее число агентов и переходы режимов](exp02_optimal_p.csv);
- [manifest](exp02_manifest.json).

## 7. Ограничения

- $C_1$, $\gamma_1$ и значения $r_h$ — синтетические уровни чувствительности,
  а не оценки реальной команды.
- Исследованы два фиксированных DAG; результат не является распределением по
  семейству графов.
- Длительности детерминированы, человеческий ресурс имеет мощность 1, а
  ожидающая задача локально удерживает агентный слот.
- Минимум на конечной сетке не доказывает оптимальность для всех целых $P$ вне
  $\{{1,2,3,4,6,8,12\}}$.

## 8. Вывод

EXP-02 даёт воспроизводимую кривую масштабирования, явно разделяет структурную
границу, точный makespan и baseline и проверяет наличие конечного оптимума на
заранее объявленных уровнях накладных расходов. Результаты остаются в каталоге
экспериментов и пока не вносятся в текст статьи.
"""
    path.write_text(report, encoding="utf-8")


def _dependencies() -> dict[str, str]:
    versions: dict[str, str] = {}
    for distribution in ("matplotlib", "ortools", "PyYAML", "pytest"):
        try:
            versions[distribution] = importlib.metadata.version(distribution)
        except importlib.metadata.PackageNotFoundError:
            versions[distribution] = "not-installed"
    return versions


def run_exp02(project_root: Path, output_directory: Path) -> tuple[Path, ...]:
    matrix_path = project_root / "scenarios" / "canonical" / "exp02_matrix.yaml"
    matrix = load_exp02_matrix(matrix_path)
    output_directory.mkdir(parents=True, exist_ok=True)
    figure_directory = project_root / "figures"
    rows: list[dict[str, str]] = []
    cases = list(iter_exp02_cases(matrix))

    for index, case in enumerate(cases, start=1):
        aggregate = compute_aggregates(case.scenario)
        baseline_schedule = simulate_baseline(case.scenario)
        baseline_validation = _validated(
            case.scenario,
            baseline_schedule,
            label="baseline schedule",
        )
        exact = solve_exact(
            case.scenario,
            time_limit_seconds=matrix.solver_time_limit_seconds,
            random_seed=matrix.solver_random_seed,
            workers=matrix.solver_workers,
        )
        exact_validation = None
        if exact.schedule is not None:
            exact_validation = _validated(
                case.scenario,
                exact.schedule,
                label="exact schedule",
            )
            if exact.objective != exact_validation.metrics.makespan:
                raise RuntimeError(f"{case.scenario.scenario_id}: objective/export mismatch")
        if exact.status not in {"OPTIMAL", "FEASIBLE"}:
            raise RuntimeError(
                f"{case.scenario.scenario_id}: exact solver returned {exact.status}"
            )
        rows.append(
            _result_row(
                case,
                aggregate,
                baseline_validation,
                baseline_schedule,
                exact,
                exact_validation,
                matrix.policy_id,
            )
        )
        if index % 10 == 0 or index == len(cases):
            print(f"EXP-02 exact progress: {index}/{len(cases)}", flush=True)

    _add_marginal_gains(rows)
    summaries = _summary_rows(rows, matrix)
    runs_path = output_directory / "exp02_runs.csv"
    summary_path = output_directory / "exp02_optimal_p.csv"
    _write_csv(runs_path, rows)
    _write_csv(summary_path, summaries)

    figure_paths = [
        *build_scaling_curve(rows, figure_directory / "exp02_scaling_curve"),
        *build_active_constraint_map(
            rows,
            figure_directory / "exp02_active_constraints",
        ),
    ]
    report_path = output_directory / "exp02_report.md"
    _write_report(
        report_path,
        matrix=matrix,
        rows=rows,
        summaries=summaries,
    )

    outputs_without_manifest = [runs_path, summary_path, report_path, *figure_paths]
    implementation_paths = sorted(
        (project_root / "src" / "experiments").glob("*.py")
    ) + [project_root / "pyproject.toml", project_root / "uv.lock"]
    manifest_path = output_directory / "exp02_manifest.json"
    manifest = {
        "experiment_id": "EXP-02",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "command": "uv run python -m experiments run --experiment EXP-02",
        **git_provenance(project_root),
        "matrix": {
            "path": str(matrix_path.relative_to(project_root)),
            "sha256": _sha256(matrix_path),
            "frozen_at": matrix.frozen_at,
            "point_count": matrix.point_count,
        },
        "solver": {
            "time_limit_seconds": matrix.solver_time_limit_seconds,
            "random_seed": matrix.solver_random_seed,
            "workers": matrix.solver_workers,
        },
        "baseline_policy_id": matrix.policy_id,
        "dependencies": _dependencies(),
        "summary": {
            "points": len(rows),
            "optimal_points": sum(row["solver_status"] == "OPTIMAL" for row in rows),
            "feasible_points": sum(row["solver_status"] == "FEASIBLE" for row in rows),
            "observed_finite_optima": sum(
                row["observed_finite_optimum_T_star"] == "true"
                for row in summaries
            ),
        },
        "scenario_hashes": [
            {
                "scenario_id": row["scenario_id"],
                "sha256": row["scenario_sha256"],
            }
            for row in rows
        ],
        "implementation": [
            {
                "path": str(path.relative_to(project_root)),
                "sha256": _sha256(path),
            }
            for path in implementation_paths
        ],
        "outputs": [
            {
                "path": str(path.relative_to(project_root)),
                "sha256": _sha256(path),
            }
            for path in outputs_without_manifest
        ],
    }
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return tuple([*outputs_without_manifest, manifest_path])
