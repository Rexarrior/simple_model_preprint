from __future__ import annotations

import csv
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from decimal import Decimal
import hashlib
import importlib.metadata
import json
from pathlib import Path
from statistics import median
from typing import Any, Iterator

import yaml

from .bounds import AggregateMetrics, compute_aggregates
from .exact_solver import ExactSolution, solve_exact
from .exp03_figures import build_profile_effects, build_queue_timeline
from .generators import build_exp01_scenario, load_exp01_matrix
from .provenance import git_provenance
from .schema import (
    Scenario,
    ScenarioError,
    ScheduleSpec,
    decimal,
    validate_scenario,
)
from .simulator import simulate_baseline
from .validator import ScheduleValidation, validate_schedule


@dataclass(frozen=True)
class Exp03Matrix:
    source_path: Path
    schema_version: int
    experiment_id: str
    frozen_at: str
    expected_point_count: int
    source_matrix: str
    topologies: tuple[str, ...]
    task_count: int
    agent_counts: tuple[int, ...]
    human_shares: tuple[Decimal, ...]
    phase_profiles: tuple[str, ...]
    reference_profile: str
    time_unit: Decimal
    tolerance: Decimal
    task_weight_cycle: tuple[Decimal, ...]
    c: Decimal
    gamma: Decimal
    policy_id: str
    solver_time_limit_seconds: float
    solver_random_seed: int
    solver_workers: int

    @property
    def point_count(self) -> int:
        return (
            len(self.topologies)
            * len(self.agent_counts)
            * len(self.human_shares)
            * len(self.phase_profiles)
        )


@dataclass(frozen=True)
class Exp03Case:
    topology: str
    agent_count: int
    human_share: Decimal
    phase_profile: str
    scenario: Scenario


@dataclass(frozen=True)
class ScheduleTrace:
    makespan: Decimal
    queue_time: Decimal
    blocked_any_time: Decimal
    blocked_agent_time: Decimal
    full_agent_stop_time: Decimal
    maximum_queue_length: int
    mean_queue_length: Decimal
    human_request_count: int
    phase_rows: tuple[dict[str, str], ...]
    event_rows: tuple[dict[str, str], ...]


def _required_list(raw: object, *, field: str) -> list[object]:
    if not isinstance(raw, list) or not raw:
        raise ScenarioError(f"{field}: expected non-empty list")
    return raw


def _required_mapping(raw: object, *, field: str) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise ScenarioError(f"{field}: expected mapping")
    return raw


def load_exp03_matrix(path: str | Path) -> Exp03Matrix:
    source_path = Path(path).resolve()
    with source_path.open("r", encoding="utf-8") as source:
        raw = yaml.safe_load(source)
    data = _required_mapping(raw, field="EXP-03 matrix")
    if data.get("frozen") is not True:
        raise ScenarioError("EXP-03 matrix must be frozen before execution")
    exact = _required_mapping(data.get("exact_solver"), field="exact_solver")
    baseline = _required_mapping(data.get("baseline_policy"), field="baseline_policy")
    matrix = Exp03Matrix(
        source_path=source_path,
        schema_version=int(data.get("schema_version", 0)),
        experiment_id=str(data.get("experiment_id", "")),
        frozen_at=str(data.get("frozen_at", "")),
        expected_point_count=int(data.get("expected_point_count", 0)),
        source_matrix=str(data.get("source_matrix", "")),
        topologies=tuple(
            str(item)
            for item in _required_list(data.get("topologies"), field="topologies")
        ),
        task_count=int(data.get("task_count", 0)),
        agent_counts=tuple(
            int(item)
            for item in _required_list(data.get("agent_counts"), field="agent_counts")
        ),
        human_shares=tuple(
            decimal(item, field="human_shares")
            for item in _required_list(data.get("human_shares"), field="human_shares")
        ),
        phase_profiles=tuple(
            str(item)
            for item in _required_list(
                data.get("phase_profiles"), field="phase_profiles"
            )
        ),
        reference_profile=str(data.get("reference_profile", "")),
        time_unit=decimal(data.get("time_unit"), field="time_unit"),
        tolerance=decimal(data.get("tolerance"), field="tolerance"),
        task_weight_cycle=tuple(
            decimal(item, field="task_weight_cycle")
            for item in _required_list(
                data.get("task_weight_cycle"), field="task_weight_cycle"
            )
        ),
        c=decimal(data.get("c"), field="c"),
        gamma=decimal(data.get("gamma"), field="gamma"),
        policy_id=str(baseline.get("policy_id", "")),
        solver_time_limit_seconds=float(exact.get("time_limit_seconds", 60)),
        solver_random_seed=int(exact.get("random_seed", 0)),
        solver_workers=int(exact.get("workers", 1)),
    )
    _validate_matrix(matrix)
    return matrix


def _validate_matrix(matrix: Exp03Matrix) -> None:
    if matrix.schema_version != 1 or matrix.experiment_id != "EXP-03":
        raise ScenarioError("EXP-03 requires schema_version=1 and experiment_id=EXP-03")
    if matrix.topologies != ("fork_join", "two_layer"):
        raise ScenarioError("EXP-03 topologies differ from the frozen design")
    if matrix.task_count != 4:
        raise ScenarioError("EXP-03 is frozen at N=4")
    if matrix.agent_counts != (2, 4):
        raise ScenarioError("EXP-03 agent counts differ from the frozen design")
    if matrix.human_shares != (Decimal("0.25"), Decimal("0.50")):
        raise ScenarioError("EXP-03 human shares differ from the frozen design")
    expected_profiles = (
        "io",
        "front_loaded",
        "alternating_sync",
        "alternating_staggered",
    )
    if matrix.phase_profiles != expected_profiles or matrix.reference_profile != "io":
        raise ScenarioError("EXP-03 phase profiles differ from the frozen design")
    if matrix.c != 1 or matrix.gamma != 1:
        raise ScenarioError("EXP-03 requires C0=gamma0=1")
    if matrix.solver_workers != 1:
        raise ScenarioError("EXP-03 exact runs are frozen to one worker")
    if not matrix.policy_id or not matrix.source_matrix:
        raise ScenarioError("EXP-03 source matrix and policy_id are required")
    if matrix.point_count != matrix.expected_point_count:
        raise ScenarioError(
            f"EXP-03 point count mismatch: expected {matrix.expected_point_count}, "
            f"got {matrix.point_count}"
        )


def build_exp03_scenario(
    matrix: Exp03Matrix,
    *,
    topology: str,
    agent_count: int,
    human_share: Decimal,
    phase_profile: str,
) -> Scenario:
    project_root = matrix.source_path.parents[2]
    source_matrix = load_exp01_matrix(project_root / matrix.source_matrix)
    if source_matrix.task_weight_cycle != matrix.task_weight_cycle:
        raise ScenarioError("EXP-03 task weights differ from the referenced EXP-01 matrix")
    base = build_exp01_scenario(
        source_matrix,
        topology=topology,
        task_count=matrix.task_count,
        agent_count=agent_count,
        human_share=human_share,
        phase_profile=phase_profile,
    )
    human_label = int(human_share * Decimal(100))
    scenario = replace(
        base,
        scenario_id=(
            f"exp03_{topology}_n{matrix.task_count}_p{agent_count}_"
            f"rh{human_label:02d}_{phase_profile}"
        ),
        variant_id="EXP-03",
        time_unit=matrix.time_unit,
        tolerance=matrix.tolerance,
        c=matrix.c,
        gamma=matrix.gamma,
        source_path=matrix.source_path,
    )
    validate_scenario(scenario)
    return scenario


def iter_exp03_cases(matrix: Exp03Matrix) -> Iterator[Exp03Case]:
    for topology in matrix.topologies:
        for agent_count in matrix.agent_counts:
            for human_share in matrix.human_shares:
                for phase_profile in matrix.phase_profiles:
                    yield Exp03Case(
                        topology=topology,
                        agent_count=agent_count,
                        human_share=human_share,
                        phase_profile=phase_profile,
                        scenario=build_exp03_scenario(
                            matrix,
                            topology=topology,
                            agent_count=agent_count,
                            human_share=human_share,
                            phase_profile=phase_profile,
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


def trace_schedule(
    scenario: Scenario,
    schedule: ScheduleSpec,
    validation: ScheduleValidation,
    *,
    schedule_kind: str,
    experiment_id: str = "EXP-03",
) -> ScheduleTrace:
    if validation.metrics is None:
        raise ValueError("cannot trace a schedule without validated metrics")
    phase_specs = {
        (task.task_id, phase.phase_id): phase
        for task in scenario.tasks
        for phase in task.phases
    }
    by_key = {
        (interval.task_id, interval.phase_id): interval for interval in schedule.phases
    }
    assignments = {item.task_id: item for item in schedule.assignments}
    waits: list[tuple[str, str, int, Decimal, Decimal]] = []
    phase_rows: list[dict[str, str]] = []
    human_request_count = 0

    for task in scenario.tasks:
        intervals = [by_key[(task.task_id, phase.phase_id)] for phase in task.phases]
        for index, (phase, interval) in enumerate(
            zip(task.phases, intervals, strict=True)
        ):
            request_time: Decimal | None = None
            waiting_before = Decimal("0")
            if phase.resource == "human":
                human_request_count += 1
                request_time = (
                    assignments[task.task_id].assigned_at
                    if index == 0
                    else intervals[index - 1].end
                )
                waiting_before = interval.start - request_time
                if waiting_before > 0:
                    waits.append(
                        (
                            task.task_id,
                            phase.phase_id,
                            interval.agent,
                            request_time,
                            interval.start,
                        )
                    )
            phase_rows.append(
                {
                    "experiment_id": experiment_id,
                    "scenario_id": scenario.scenario_id,
                    "schedule_kind": schedule_kind,
                    "record_type": "phase",
                    "task_id": task.task_id,
                    "phase_id": phase.phase_id,
                    "agent": str(interval.agent),
                    "resource": phase.resource,
                    "start": _format_decimal(interval.start),
                    "end": _format_decimal(interval.end),
                    "duration": _format_decimal(interval.end - interval.start),
                    "request_time": _format_decimal(request_time),
                    "waiting_before": _format_decimal(waiting_before),
                }
            )

    for task_id, phase_id, agent, start, end in waits:
        phase_rows.append(
            {
                "experiment_id": experiment_id,
                "scenario_id": scenario.scenario_id,
                "schedule_kind": schedule_kind,
                "record_type": "wait",
                "task_id": task_id,
                "phase_id": phase_id,
                "agent": str(agent),
                "resource": "human_queue",
                "start": _format_decimal(start),
                "end": _format_decimal(end),
                "duration": _format_decimal(end - start),
                "request_time": _format_decimal(start),
                "waiting_before": _format_decimal(end - start),
            }
        )

    task_spans = {
        task.task_id: (
            assignments[task.task_id].assigned_at,
            max(by_key[(task.task_id, phase.phase_id)].end for phase in task.phases),
        )
        for task in scenario.tasks
    }
    boundaries = {Decimal("0"), validation.metrics.makespan}
    for interval in schedule.phases:
        boundaries.update((interval.start, interval.end))
    for start, end in task_spans.values():
        boundaries.update((start, end))
    for _, _, _, start, end in waits:
        boundaries.update((start, end))
    ordered = sorted(boundaries)

    event_rows: list[dict[str, str]] = []
    full_agent_stop_time = Decimal("0")
    queue_area = Decimal("0")
    blocked_any_time = Decimal("0")
    maximum_queue_length = 0
    for start, end in zip(ordered, ordered[1:]):
        if end <= start:
            continue
        active_agent_phases = sum(
            interval.start <= start < interval.end
            and phase_specs[(interval.task_id, interval.phase_id)].resource == "agent"
            for interval in schedule.phases
        )
        active_human_phases = sum(
            interval.start <= start < interval.end
            and phase_specs[(interval.task_id, interval.phase_id)].resource == "human"
            for interval in schedule.phases
        )
        human_queue_length = sum(
            wait_start <= start < wait_end
            for _, _, _, wait_start, wait_end in waits
        )
        occupied_slots = sum(
            span_start <= start < span_end for span_start, span_end in task_spans.values()
        )
        full_agent_stop = occupied_slots == scenario.p and active_agent_phases == 0
        duration = end - start
        if full_agent_stop:
            full_agent_stop_time += duration
        if human_queue_length:
            blocked_any_time += duration
        queue_area += Decimal(human_queue_length) * duration
        maximum_queue_length = max(maximum_queue_length, human_queue_length)
        event_rows.append(
            {
                "experiment_id": experiment_id,
                "scenario_id": scenario.scenario_id,
                "schedule_kind": schedule_kind,
                "start": _format_decimal(start),
                "end": _format_decimal(end),
                "duration": _format_decimal(duration),
                "active_agent_phases": str(active_agent_phases),
                "active_human_phases": str(active_human_phases),
                "human_queue_length": str(human_queue_length),
                "occupied_agent_slots": str(occupied_slots),
                "free_agent_slots": str(scenario.p - occupied_slots),
                "full_agent_stop": str(full_agent_stop).lower(),
            }
        )

    if queue_area != validation.metrics.queue_time:
        raise RuntimeError(
            f"{scenario.scenario_id}: timeline queue area {queue_area} differs "
            f"from validated Q={validation.metrics.queue_time}"
        )
    if blocked_any_time != validation.metrics.blocked_any_time:
        raise RuntimeError(
            f"{scenario.scenario_id}: timeline blocked-any time differs from validator"
        )
    return ScheduleTrace(
        makespan=validation.metrics.makespan,
        queue_time=validation.metrics.queue_time,
        blocked_any_time=validation.metrics.blocked_any_time,
        blocked_agent_time=validation.metrics.blocked_agent_time,
        full_agent_stop_time=full_agent_stop_time,
        maximum_queue_length=maximum_queue_length,
        mean_queue_length=(
            queue_area / validation.metrics.makespan
            if validation.metrics.makespan
            else Decimal("0")
        ),
        human_request_count=human_request_count,
        phase_rows=tuple(phase_rows),
        event_rows=tuple(event_rows),
    )


def _trace_fields(prefix: str, trace: ScheduleTrace | None) -> dict[str, str]:
    if trace is None:
        return {
            f"{prefix}_makespan": "",
            f"{prefix}_queue": "",
            f"{prefix}_blocked_any": "",
            f"{prefix}_blocked_agent_time": "",
            f"{prefix}_full_agent_stop": "",
            f"{prefix}_maximum_queue_length": "",
            f"{prefix}_mean_queue_length": "",
        }
    return {
        f"{prefix}_makespan": _format_decimal(trace.makespan),
        f"{prefix}_queue": _format_decimal(trace.queue_time),
        f"{prefix}_blocked_any": _format_decimal(trace.blocked_any_time),
        f"{prefix}_blocked_agent_time": _format_decimal(trace.blocked_agent_time),
        f"{prefix}_full_agent_stop": _format_decimal(trace.full_agent_stop_time),
        f"{prefix}_maximum_queue_length": str(trace.maximum_queue_length),
        f"{prefix}_mean_queue_length": _format_decimal(
            trace.mean_queue_length.quantize(Decimal("0.000001"))
        ),
    }


def _result_row(
    case: Exp03Case,
    aggregate: AggregateMetrics,
    exact: ExactSolution,
    exact_trace: ScheduleTrace | None,
    baseline_trace: ScheduleTrace,
    policy_id: str,
) -> dict[str, str]:
    is_optimal = exact.status == "OPTIMAL" and exact.objective is not None
    exact_gap = exact.objective - aggregate.b4 if exact.objective is not None else None
    baseline_gap = (
        baseline_trace.makespan - exact.objective
        if is_optimal and exact.objective is not None
        else None
    )
    row = {
        "experiment_id": "EXP-03",
        "scenario_id": case.scenario.scenario_id,
        "scenario_sha256": _json_sha256(_scenario_payload(case.scenario)),
        "topology": case.topology,
        "task_count": str(len(case.scenario.tasks)),
        "agent_count": str(case.agent_count),
        "human_share": _format_decimal(case.human_share),
        "phase_profile": case.phase_profile,
        "policy_id": policy_id,
        "human_request_count": str(
            sum(
                phase.resource == "human"
                for task in case.scenario.tasks
                for phase in task.phases
            )
        ),
        "A": _format_decimal(aggregate.a),
        "H": _format_decimal(aggregate.h),
        "W4": _format_decimal(aggregate.w4),
        "L4": _format_decimal(aggregate.l4),
        "W4_over_P": _format_decimal(aggregate.work_branch),
        "gamma_H": _format_decimal(aggregate.human_branch),
        "B4": _format_decimal(aggregate.b4),
        "active_branches": ",".join(aggregate.active_branches),
        "critical_path": "->".join(aggregate.critical_path_l4),
        "solver_status": exact.status,
        "T_star": _format_decimal(exact.objective) if is_optimal else "",
        "solver_best_bound": _format_decimal(exact.best_bound),
        "solver_gap": _format_decimal(exact.relative_gap),
        "solver_wall_time_seconds": f"{exact.wall_time:.6f}",
        "exact_gap_to_B4": _format_decimal(exact_gap),
        "exact_relative_gap_to_B4": (
            _ratio(exact_gap, aggregate.b4) if exact_gap is not None else ""
        ),
        "baseline_gap_to_optimum": _format_decimal(baseline_gap),
        "baseline_relative_gap": (
            _ratio(baseline_gap, exact.objective)
            if baseline_gap is not None and exact.objective is not None
            else ""
        ),
    }
    row.update(_trace_fields("exact", exact_trace))
    row.update(_trace_fields("baseline", baseline_trace))
    return row


def _paired_rows(
    rows: list[dict[str, str]],
    matrix: Exp03Matrix,
) -> list[dict[str, str]]:
    grouped: dict[tuple[str, str, str], dict[str, dict[str, str]]] = {}
    for row in rows:
        key = (row["topology"], row["agent_count"], row["human_share"])
        grouped.setdefault(key, {})[row["phase_profile"]] = row
    paired: list[dict[str, str]] = []
    for key, profiles in sorted(grouped.items()):
        reference = profiles[matrix.reference_profile]
        for profile in matrix.phase_profiles:
            if profile == matrix.reference_profile:
                continue
            current = profiles[profile]
            for invariant in ("A", "H", "W4", "L4", "B4"):
                if Decimal(current[invariant]) != Decimal(reference[invariant]):
                    raise RuntimeError(
                        f"EXP-03 paired invariant {invariant} differs for {key}, {profile}"
                    )
            exact_delta = (
                Decimal(current["T_star"]) - Decimal(reference["T_star"])
                if current["T_star"] and reference["T_star"]
                else None
            )
            pair_id = (
                f"{key[0]}_p{key[1]}_rh{int(Decimal(key[2]) * 100)}_"
                f"{profile}_vs_io"
            )
            paired.append(
                {
                    "pair_id": pair_id,
                    "topology": key[0],
                    "agent_count": key[1],
                    "human_share": key[2],
                    "phase_profile": profile,
                    "io_scenario_id": reference["scenario_id"],
                    "profile_scenario_id": current["scenario_id"],
                    "A": current["A"],
                    "H": current["H"],
                    "W4": current["W4"],
                    "L4": current["L4"],
                    "B4": current["B4"],
                    "same_B4": str(current["B4"] == reference["B4"]).lower(),
                    "io_T_star": reference["T_star"],
                    "profile_T_star": current["T_star"],
                    "delta_T_star_to_IO": _format_decimal(exact_delta),
                    "io_exact_queue": reference["exact_queue"],
                    "profile_exact_queue": current["exact_queue"],
                    "delta_exact_queue_to_IO": _format_decimal(
                        Decimal(current["exact_queue"])
                        - Decimal(reference["exact_queue"])
                    ),
                    "io_exact_blocked_any": reference["exact_blocked_any"],
                    "profile_exact_blocked_any": current["exact_blocked_any"],
                    "delta_exact_blocked_any_to_IO": _format_decimal(
                        Decimal(current["exact_blocked_any"])
                        - Decimal(reference["exact_blocked_any"])
                    ),
                    "io_exact_full_agent_stop": reference["exact_full_agent_stop"],
                    "profile_exact_full_agent_stop": current[
                        "exact_full_agent_stop"
                    ],
                    "delta_exact_full_agent_stop_to_IO": _format_decimal(
                        Decimal(current["exact_full_agent_stop"])
                        - Decimal(reference["exact_full_agent_stop"])
                    ),
                    "io_baseline_makespan": reference["baseline_makespan"],
                    "profile_baseline_makespan": current["baseline_makespan"],
                    "delta_baseline_makespan_to_IO": _format_decimal(
                        Decimal(current["baseline_makespan"])
                        - Decimal(reference["baseline_makespan"])
                    ),
                    "io_baseline_queue": reference["baseline_queue"],
                    "profile_baseline_queue": current["baseline_queue"],
                    "delta_baseline_queue_to_IO": _format_decimal(
                        Decimal(current["baseline_queue"])
                        - Decimal(reference["baseline_queue"])
                    ),
                    "io_human_request_count": reference["human_request_count"],
                    "profile_human_request_count": current["human_request_count"],
                }
            )
    return paired


def _sync_staggered_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    grouped: dict[tuple[str, str, str], dict[str, dict[str, str]]] = {}
    for row in rows:
        key = (row["topology"], row["agent_count"], row["human_share"])
        grouped.setdefault(key, {})[row["phase_profile"]] = row
    comparisons: list[dict[str, str]] = []
    for key, profiles in sorted(grouped.items()):
        sync = profiles["alternating_sync"]
        staggered = profiles["alternating_staggered"]
        for invariant in ("A", "H", "W4", "L4", "B4", "human_request_count"):
            if sync[invariant] != staggered[invariant]:
                raise RuntimeError(
                    f"EXP-03 sync/staggered invariant {invariant} differs for {key}"
                )
        comparisons.append(
            {
                "topology": key[0],
                "agent_count": key[1],
                "human_share": key[2],
                "human_request_count": sync["human_request_count"],
                "A": sync["A"],
                "H": sync["H"],
                "W4": sync["W4"],
                "L4": sync["L4"],
                "B4": sync["B4"],
                "sync_T_star": sync["T_star"],
                "staggered_T_star": staggered["T_star"],
                "delta_T_star_sync_minus_staggered": _format_decimal(
                    Decimal(sync["T_star"]) - Decimal(staggered["T_star"])
                ),
                "sync_exact_queue": sync["exact_queue"],
                "staggered_exact_queue": staggered["exact_queue"],
                "delta_exact_queue_sync_minus_staggered": _format_decimal(
                    Decimal(sync["exact_queue"]) - Decimal(staggered["exact_queue"])
                ),
                "sync_exact_full_agent_stop": sync["exact_full_agent_stop"],
                "staggered_exact_full_agent_stop": staggered[
                    "exact_full_agent_stop"
                ],
                "delta_exact_full_stop_sync_minus_staggered": _format_decimal(
                    Decimal(sync["exact_full_agent_stop"])
                    - Decimal(staggered["exact_full_agent_stop"])
                ),
                "sync_baseline_makespan": sync["baseline_makespan"],
                "staggered_baseline_makespan": staggered["baseline_makespan"],
                "delta_baseline_sync_minus_staggered": _format_decimal(
                    Decimal(sync["baseline_makespan"])
                    - Decimal(staggered["baseline_makespan"])
                ),
            }
        )
    return comparisons


def _select_pairs(
    paired: list[dict[str, str]],
    tolerance: Decimal,
) -> tuple[list[dict[str, str]], dict[str, str]]:
    counterexamples = [
        row
        for row in paired
        if row["same_B4"] == "true"
        and row["delta_T_star_to_IO"]
        and abs(Decimal(row["delta_T_star_to_IO"])) > tolerance
    ]
    ordered_counterexamples = sorted(
        counterexamples,
        key=lambda row: (
            -abs(Decimal(row["delta_T_star_to_IO"])),
            row["profile_scenario_id"],
        ),
    )
    if ordered_counterexamples:
        timeline = ordered_counterexamples[0]
    else:
        timeline = min(
            paired,
            key=lambda row: (
                -abs(Decimal(row["delta_exact_queue_to_IO"])),
                row["profile_scenario_id"],
            ),
        )
    return ordered_counterexamples, timeline


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


def _profile_summary(
    paired: list[dict[str, str]],
    tolerance: Decimal,
) -> list[dict[str, str]]:
    summaries: list[dict[str, str]] = []
    for profile in ("front_loaded", "alternating_sync", "alternating_staggered"):
        selected = [row for row in paired if row["phase_profile"] == profile]
        effects = [Decimal(row["delta_T_star_to_IO"]) for row in selected]
        queue_effects = [Decimal(row["delta_exact_queue_to_IO"]) for row in selected]
        stop_effects = [
            Decimal(row["delta_exact_full_agent_stop_to_IO"]) for row in selected
        ]
        summaries.append(
            {
                "profile": profile,
                "pairs": str(len(selected)),
                "different_T_star": str(sum(abs(value) > tolerance for value in effects)),
                "negative_T_star": str(sum(value < -tolerance for value in effects)),
                "positive_T_star": str(sum(value > tolerance for value in effects)),
                "median_delta_T_star": _format_decimal(median(effects)),
                "minimum_delta_T_star": _format_decimal(min(effects)),
                "maximum_delta_T_star": _format_decimal(max(effects)),
                "median_delta_exact_queue": _format_decimal(median(queue_effects)),
                "median_delta_exact_full_agent_stop": _format_decimal(
                    median(stop_effects)
                ),
            }
        )
    return summaries


def _write_report(
    path: Path,
    *,
    matrix: Exp03Matrix,
    rows: list[dict[str, str]],
    paired: list[dict[str, str]],
    sync_staggered: list[dict[str, str]],
    counterexamples: list[dict[str, str]],
    timeline_pair: dict[str, str],
) -> None:
    optimal_count = sum(row["solver_status"] == "OPTIMAL" for row in rows)
    summaries = _profile_summary(paired, matrix.tolerance)
    front_loaded_differences = sum(
        row["phase_profile"] == "front_loaded"
        and abs(Decimal(row["delta_T_star_to_IO"])) > matrix.tolerance
        for row in paired
    )
    sync_slower = sum(
        Decimal(row["delta_T_star_sync_minus_staggered"]) > matrix.tolerance
        for row in sync_staggered
    )
    sync_faster = sum(
        Decimal(row["delta_T_star_sync_minus_staggered"]) < -matrix.tolerance
        for row in sync_staggered
    )
    sync_equal = len(sync_staggered) - sync_slower - sync_faster
    summary_lines = "\n".join(
        "| {profile} | {pairs} | {different} | {negative} | {positive} | {median} | {minimum} | {maximum} | {queue} | {stop} |".format(
            profile=row["profile"],
            pairs=row["pairs"],
            different=row["different_T_star"],
            negative=row["negative_T_star"],
            positive=row["positive_T_star"],
            median=row["median_delta_T_star"],
            minimum=row["minimum_delta_T_star"],
            maximum=row["maximum_delta_T_star"],
            queue=row["median_delta_exact_queue"],
            stop=row["median_delta_exact_full_agent_stop"],
        )
        for row in summaries
    )
    if counterexamples:
        selected = counterexamples[0]
        criterion_text = rf"""Найдены {len(counterexamples)} из {len(paired)} пар с одинаковым $B_4$ и
разным доказанным $T^*$. По заранее зафиксированному правилу максимального
$|\Delta T^*|$ выбрана пара `{selected['pair_id']}`:

- $B_4={selected['B4']}$ ч;
- $T^*_{{IO}}={selected['io_T_star']}$ ч;
- $T^*_{{profile}}={selected['profile_T_star']}$ ч;
- $\Delta T^*={selected['delta_T_star_to_IO']}$ ч;
- $\Delta Q={selected['delta_exact_queue_to_IO']}$ агент-часа;
- изменение времени полной остановки всех слотов:
  {selected['delta_exact_full_agent_stop_to_IO']} ч.

Таким образом, критерий содержательного результата EXP-03 выполнен: одинаковые
$A$, $H$, $W_4$, $L_4$ и $B_4$ не определяют фактический оптимум без
расположения human-фаз."""
    else:
        criterion_text = rf"""Ни одна из {len(paired)} пар не дала разности
$T^*$ больше tolerance при одинаковом $B_4$. Гипотеза о влиянии профиля на
оптимум для двух выбранных DAG отклоняется; серия сохраняется как отрицательный
результат. Для timeline выбрана максимальная по $|\Delta Q|$ пара
`{timeline_pair['pair_id']}`."""

    report = rf"""# Отчёт по EXP-03: расположение человеческих фаз

Дата отчёта: 2026-08-07

Статус: полная замороженная матрица, {len(rows)} точки и {len(paired)} парных
сравнения с IO.

## 1. Резюме

Для {optimal_count} из {len(rows)} точек доказан статус `OPTIMAL`. Во всех
парах сохранены DAG, $A$, $H$, $W_4$, $L_4$, $C$, $\gamma$ и $B_4$; меняются
только расположение human-фаз и, для alternating-профилей, число запросов.

{criterion_text}

## 2. Зафиксированный дизайн

- DAG: fork--join и two-layer из замороженного EXP-01, $N=4$;
- $P\in\{{2,4\}}$, $r_h\in\{{0.25,0.50\}}$;
- профили: IO (50/50 human-времени), front-loaded (90/10),
  alternating-sync и alternating-staggered;
- $C_0=\gamma_0=1$;
- IO используется как reference внутри каждой пары;
- exact: один worker, seed 0, общий лимит 60 секунд на точку.

IO и front-loaded содержат по два human-запроса на задачу. Alternating-профили
содержат по четыре; sync делит agent-время одинаково, staggered циклически
переставляет доли $1/6$, $2/6$, $3/6$.

В {front_loaded_differences} из 8 сравнений front-loaded/IO доказанный оптимум
различается при одинаковом числе запросов. Следовательно, наличие эффекта нельзя
объяснить только удвоением числа human-фаз в alternating-профилях.

## 3. Парные эффекты относительно IO

![Парные эффекты EXP-03](../figures/exp03_profile_effects.png)

[SVG-версия](../figures/exp03_profile_effects.svg).

| Профиль | Пар | $\Delta T^*\ne0$ | Меньше IO | Больше IO | Медиана $\Delta T^*$ | Min | Max | Медиана $\Delta Q$ | Медиана изменения полной остановки |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
{summary_lines}

Отрицательное $\Delta T^*$ означает, что профиль завершает тот же DAG быстрее
IO; положительное — медленнее. Эти эффекты не смешиваются с gap baseline:
соответствующие разности фиксированной политики сохранены отдельными столбцами.

В {len(sync_staggered)} прямых парах sync/staggered совпадают также число и
размер human-фаз. Sync дал больший $T^*$ в {sync_slower} случаях, меньший — в
{sync_faster}, одинаковый — в {sync_equal}. Полные результаты сохранены в
[отдельной таблице](exp03_sync_staggered_pairs.csv).

## 4. Очередь и полная остановка слотов

![Очередь и блокировки EXP-03](../figures/exp03_queue_blocking.png)

[SVG-версия](../figures/exp03_queue_blocking.svg).

На timeline показана пара `{timeline_pair['pair_id']}`. Оранжевая
ступенчатая линия — число задач, ожидающих человеческий ресурс; синяя — число
выполняемых agent-фаз. Розовый фон отмечает интервалы, когда все $P$ слотов
удерживаются задачами, но ни на одном не выполняется agent-фаза. Это
операционное определение «полной остановки» зафиксировано до запуска.

Blocked agent-time совпадает с площадью под длиной human-очереди и с $Q$ по
контракту модели. Время с хотя бы одной блокировкой считается как длина
объединения интервалов ожидания и хранится отдельно от суммы ожиданий.

## 5. Воспроизводимость

```bash
cd simple_model_full/experiments
uv sync --python 3.13
uv run pytest -ra
uv run python -m experiments run --experiment EXP-03
```

Артефакты:

- [замороженная матрица](../scenarios/canonical/exp03_matrix.yaml);
- [все {len(rows)} прогона](exp03_runs.csv);
- [{len(paired)} парных сравнения](exp03_profile_pairs.csv);
- [{len(sync_staggered)} прямых пар sync/staggered](exp03_sync_staggered_pairs.csv);
- [фазы и интервалы ожидания](exp03_phases.csv);
- [временные состояния ресурсов и очереди](exp03_events.csv);
- [выбранная пара](exp03_counterexample.json);
- [manifest](exp03_manifest.json).

## 6. Ограничения

- Параметры и веса синтетические; исследованы только два фиксированных DAG.
- Длительности детерминированы, человек имеет мощность 1, ожидающая задача
  удерживает агентный слот.
- CP-SAT минимизирует makespan, но не использует очередь как вторичную цель.
  Поэтому exact-метрики очереди описывают детерминированно возвращённое
  оптимальное расписание при одном worker и seed 0, а не минимум очереди среди
  всех расписаний с тем же $T^*$.
- Разность между alternating и IO одновременно включает изменение числа
  human-запросов; чистое влияние синхронизации оценивается сравнением sync и
  staggered в отдельной таблице результатов, а не сравнением с IO в изоляции.

## 7. Вывод

EXP-03 проверяет фазовый механизм без изменения агрегатной работы и нижней
границы. Результаты остаются в каталоге экспериментов и пока не вносятся в
текст статьи.
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


def run_exp03(project_root: Path, output_directory: Path) -> tuple[Path, ...]:
    matrix_path = project_root / "scenarios" / "canonical" / "exp03_matrix.yaml"
    matrix = load_exp03_matrix(matrix_path)
    source_matrix_path = project_root / matrix.source_matrix
    output_directory.mkdir(parents=True, exist_ok=True)
    figure_directory = project_root / "figures"
    rows: list[dict[str, str]] = []
    phase_rows: list[dict[str, str]] = []
    event_rows: list[dict[str, str]] = []
    cases = list(iter_exp03_cases(matrix))

    for index, case in enumerate(cases, start=1):
        aggregate = compute_aggregates(case.scenario)
        baseline_schedule = simulate_baseline(case.scenario)
        baseline_validation = _validated(
            case.scenario,
            baseline_schedule,
            label="baseline schedule",
        )
        baseline_trace = trace_schedule(
            case.scenario,
            baseline_schedule,
            baseline_validation,
            schedule_kind="baseline",
        )
        exact = solve_exact(
            case.scenario,
            time_limit_seconds=matrix.solver_time_limit_seconds,
            random_seed=matrix.solver_random_seed,
            workers=matrix.solver_workers,
        )
        exact_trace = None
        if exact.schedule is not None:
            exact_validation = _validated(
                case.scenario,
                exact.schedule,
                label="exact schedule",
            )
            if exact.objective != exact_validation.metrics.makespan:
                raise RuntimeError(f"{case.scenario.scenario_id}: objective/export mismatch")
            exact_trace = trace_schedule(
                case.scenario,
                exact.schedule,
                exact_validation,
                schedule_kind="exact",
            )
        if exact.status not in {"OPTIMAL", "FEASIBLE"}:
            raise RuntimeError(
                f"{case.scenario.scenario_id}: exact solver returned {exact.status}"
            )
        rows.append(
            _result_row(
                case,
                aggregate,
                exact,
                exact_trace,
                baseline_trace,
                matrix.policy_id,
            )
        )
        phase_rows.extend(baseline_trace.phase_rows)
        event_rows.extend(baseline_trace.event_rows)
        if exact_trace is not None:
            phase_rows.extend(exact_trace.phase_rows)
            event_rows.extend(exact_trace.event_rows)
        if index % 8 == 0 or index == len(cases):
            print(f"EXP-03 exact progress: {index}/{len(cases)}", flush=True)

    paired = _paired_rows(rows, matrix)
    sync_staggered = _sync_staggered_rows(rows)
    counterexamples, timeline_pair = _select_pairs(paired, matrix.tolerance)
    runs_path = output_directory / "exp03_runs.csv"
    pairs_path = output_directory / "exp03_profile_pairs.csv"
    sync_staggered_path = output_directory / "exp03_sync_staggered_pairs.csv"
    phases_path = output_directory / "exp03_phases.csv"
    events_path = output_directory / "exp03_events.csv"
    _write_csv(runs_path, rows)
    _write_csv(pairs_path, paired)
    _write_csv(sync_staggered_path, sync_staggered)
    _write_csv(phases_path, phase_rows)
    _write_csv(events_path, event_rows)

    counterexample_path = output_directory / "exp03_counterexample.json"
    counterexample_payload = {
        "experiment_id": "EXP-03",
        "selection_rule": (
            "maximum abs(delta_T_star_to_IO), then profile_scenario_id, "
            "among same-B4 pairs above tolerance"
        ),
        "counterexample_count": len(counterexamples),
        "selected_counterexample": counterexamples[0] if counterexamples else None,
        "timeline_pair": timeline_pair,
    }
    counterexample_path.write_text(
        json.dumps(counterexample_payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    figure_paths = [
        *build_profile_effects(paired, figure_directory / "exp03_profile_effects"),
        *build_queue_timeline(
            paired,
            event_rows,
            timeline_pair["pair_id"],
            figure_directory / "exp03_queue_blocking",
        ),
    ]
    report_path = output_directory / "exp03_report.md"
    _write_report(
        report_path,
        matrix=matrix,
        rows=rows,
        paired=paired,
        sync_staggered=sync_staggered,
        counterexamples=counterexamples,
        timeline_pair=timeline_pair,
    )

    outputs_without_manifest = [
        runs_path,
        pairs_path,
        sync_staggered_path,
        phases_path,
        events_path,
        counterexample_path,
        report_path,
        *figure_paths,
    ]
    implementation_paths = sorted(
        (project_root / "src" / "experiments").glob("*.py")
    ) + [project_root / "pyproject.toml", project_root / "uv.lock"]
    manifest_path = output_directory / "exp03_manifest.json"
    manifest = {
        "experiment_id": "EXP-03",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "command": "uv run python -m experiments run --experiment EXP-03",
        **git_provenance(project_root),
        "matrix": {
            "path": str(matrix_path.relative_to(project_root)),
            "sha256": _sha256(matrix_path),
            "frozen_at": matrix.frozen_at,
            "point_count": matrix.point_count,
        },
        "source_matrix": {
            "path": str(source_matrix_path.relative_to(project_root)),
            "sha256": _sha256(source_matrix_path),
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
            "paired_comparisons": len(paired),
            "sync_staggered_comparisons": len(sync_staggered),
            "same_bound_different_optimum_pairs": len(counterexamples),
            "front_loaded_same_requests_different_optimum_pairs": sum(
                row["phase_profile"] == "front_loaded"
                and abs(Decimal(row["delta_T_star_to_IO"])) > matrix.tolerance
                for row in paired
            ),
            "selected_counterexample": (
                counterexamples[0]["pair_id"] if counterexamples else None
            ),
            "timeline_pair": timeline_pair["pair_id"],
        },
        "scenario_hashes": [
            {"scenario_id": row["scenario_id"], "sha256": row["scenario_sha256"]}
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
