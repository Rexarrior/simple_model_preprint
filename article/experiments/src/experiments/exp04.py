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
from .exp03 import ScheduleTrace, trace_schedule
from .exp04_figures import build_decomposition_curves, build_optimal_granularity_map
from .generators import build_exp01_scenario, load_exp01_matrix
from .provenance import git_provenance
from .schema import (
    PhaseSpec,
    Scenario,
    ScenarioError,
    ScheduleSpec,
    TaskSpec,
    decimal,
    validate_scenario,
)
from .simulator import simulate_baseline
from .validator import ScheduleValidation, validate_schedule


@dataclass(frozen=True)
class Exp04Parameters:
    m: int
    overhead_rate: Decimal
    lambda_h: Decimal

    @property
    def label(self) -> str:
        return (
            f"m={self.m},r_o={format(self.overhead_rate, 'f')},"
            f"lambda_h={format(self.lambda_h, 'f')}"
        )


@dataclass(frozen=True)
class Exp04Matrix:
    source_path: Path
    schema_version: int
    experiment_id: str
    frozen_at: str
    exp04a_source_results: str
    exp04a_variants: tuple[str, ...]
    source_matrix: str
    topology: str
    task_count: int
    agent_count: int
    human_share: Decimal
    phase_profile: str
    selected_task_id: str
    selected_quality_gate_id: str
    base_effort: Decimal
    time_unit: Decimal
    tolerance: Decimal
    m_values: tuple[int, ...]
    overhead_rates: tuple[Decimal, ...]
    human_overhead_shares: tuple[Decimal, ...]
    raw_combination_count: int
    expected_unique_point_count: int
    c: Decimal
    gamma: Decimal
    policy_id: str
    solver_time_limit_seconds: float
    solver_random_seed: int
    solver_workers: int

    @property
    def point_count(self) -> int:
        return (
            len(self.m_values)
            * len(self.overhead_rates)
            * len(self.human_overhead_shares)
        )


@dataclass(frozen=True)
class Exp04Case:
    parameters: Exp04Parameters
    aliases: tuple[Exp04Parameters, ...]
    semantic_sha256: str
    scenario: Scenario
    total_overhead: Decimal
    human_overhead: Decimal
    agent_overhead: Decimal


def _required_mapping(raw: object, *, field: str) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise ScenarioError(f"{field}: expected mapping")
    return raw


def _required_list(raw: object, *, field: str) -> list[object]:
    if not isinstance(raw, list) or not raw:
        raise ScenarioError(f"{field}: expected non-empty list")
    return raw


def load_exp04_matrix(path: str | Path) -> Exp04Matrix:
    source_path = Path(path).resolve()
    with source_path.open("r", encoding="utf-8") as source:
        raw = yaml.safe_load(source)
    data = _required_mapping(raw, field="EXP-04 matrix")
    if data.get("frozen") is not True:
        raise ScenarioError("EXP-04 matrix must be frozen before execution")
    exp04a = _required_mapping(data.get("exp04a"), field="exp04a")
    exp04b = _required_mapping(data.get("exp04b"), field="exp04b")
    exact = _required_mapping(data.get("exact_solver"), field="exact_solver")
    baseline = _required_mapping(data.get("baseline_policy"), field="baseline_policy")
    matrix = Exp04Matrix(
        source_path=source_path,
        schema_version=int(data.get("schema_version", 0)),
        experiment_id=str(data.get("experiment_id", "")),
        frozen_at=str(data.get("frozen_at", "")),
        exp04a_source_results=str(exp04a.get("source_results", "")),
        exp04a_variants=tuple(
            str(item)
            for item in _required_list(exp04a.get("variants"), field="exp04a.variants")
        ),
        source_matrix=str(exp04b.get("source_matrix", "")),
        topology=str(exp04b.get("topology", "")),
        task_count=int(exp04b.get("task_count", 0)),
        agent_count=int(exp04b.get("agent_count", 0)),
        human_share=decimal(exp04b.get("human_share"), field="human_share"),
        phase_profile=str(exp04b.get("phase_profile", "")),
        selected_task_id=str(exp04b.get("selected_task_id", "")),
        selected_quality_gate_id=str(exp04b.get("selected_quality_gate_id", "")),
        base_effort=decimal(exp04b.get("base_effort"), field="base_effort"),
        time_unit=decimal(exp04b.get("time_unit"), field="time_unit"),
        tolerance=decimal(exp04b.get("tolerance"), field="tolerance"),
        m_values=tuple(
            int(item)
            for item in _required_list(exp04b.get("m_values"), field="m_values")
        ),
        overhead_rates=tuple(
            decimal(item, field="overhead_rates")
            for item in _required_list(
                exp04b.get("overhead_rates"), field="overhead_rates"
            )
        ),
        human_overhead_shares=tuple(
            decimal(item, field="human_overhead_shares")
            for item in _required_list(
                exp04b.get("human_overhead_shares"),
                field="human_overhead_shares",
            )
        ),
        raw_combination_count=int(exp04b.get("raw_combination_count", 0)),
        expected_unique_point_count=int(
            exp04b.get("expected_unique_point_count", 0)
        ),
        c=decimal(data.get("c"), field="c"),
        gamma=decimal(data.get("gamma"), field="gamma"),
        policy_id=str(baseline.get("policy_id", "")),
        solver_time_limit_seconds=float(exact.get("time_limit_seconds", 120)),
        solver_random_seed=int(exact.get("random_seed", 0)),
        solver_workers=int(exact.get("workers", 1)),
    )
    _validate_matrix(matrix)
    return matrix


def _validate_matrix(matrix: Exp04Matrix) -> None:
    if matrix.schema_version != 1 or matrix.experiment_id != "EXP-04":
        raise ScenarioError("EXP-04 requires schema_version=1 and experiment_id=EXP-04")
    if (
        matrix.topology,
        matrix.task_count,
        matrix.agent_count,
        matrix.human_share,
        matrix.phase_profile,
    ) != ("two_layer", 4, 4, Decimal("0.25"), "io"):
        raise ScenarioError("EXP-04B canonical base differs from the frozen design")
    if matrix.selected_task_id != "t04" or not matrix.selected_quality_gate_id:
        raise ScenarioError("EXP-04B selected task or quality gate is invalid")
    if matrix.m_values != (1, 2, 3, 4, 6, 8):
        raise ScenarioError("EXP-04B m values differ from the frozen design")
    if matrix.overhead_rates != (
        Decimal("0"),
        Decimal("0.025"),
        Decimal("0.05"),
        Decimal("0.10"),
        Decimal("0.20"),
    ):
        raise ScenarioError("EXP-04B overhead rates differ from the frozen design")
    if matrix.human_overhead_shares != (
        Decimal("0"),
        Decimal("0.5"),
        Decimal("1"),
    ):
        raise ScenarioError("EXP-04B lambda_h values differ from the frozen design")
    if matrix.point_count != 90 or matrix.raw_combination_count != 90:
        raise ScenarioError("EXP-04B raw matrix must contain 90 combinations")
    if matrix.expected_unique_point_count != 66:
        raise ScenarioError("EXP-04B frozen unique point count must be 66")
    if matrix.c != 1 or matrix.gamma != 1 or matrix.solver_workers != 1:
        raise ScenarioError("EXP-04B requires C=gamma=1 and one solver worker")


def _base_scenario(matrix: Exp04Matrix) -> Scenario:
    project_root = matrix.source_path.parents[2]
    source_matrix = load_exp01_matrix(project_root / matrix.source_matrix)
    scenario = build_exp01_scenario(
        source_matrix,
        topology=matrix.topology,
        task_count=matrix.task_count,
        agent_count=matrix.agent_count,
        human_share=matrix.human_share,
        phase_profile=matrix.phase_profile,
    )
    selected = scenario.task_by_id[matrix.selected_task_id]
    if selected.quality_gate_id != matrix.selected_quality_gate_id:
        raise ScenarioError("EXP-04B source quality gate differs from the matrix")
    if sum((phase.base_duration for phase in selected.phases), Decimal("0")) != matrix.base_effort:
        raise ScenarioError("EXP-04B selected-task effort differs from the matrix")
    aggregate = compute_aggregates(scenario)
    if matrix.selected_task_id not in aggregate.critical_path_l4:
        raise ScenarioError("EXP-04B selected task is not on the frozen critical path")
    return scenario


def _task_from_durations(
    *,
    task_id: str,
    name: str,
    predecessors: tuple[str, ...],
    agent_duration: Decimal,
    human_duration: Decimal,
    phases: tuple[PhaseSpec, ...],
    quality_gate_id: str,
) -> TaskSpec:
    total = agent_duration + human_duration
    if total <= 0:
        raise ScenarioError(f"EXP-04B task {task_id} has zero total duration")
    return TaskSpec(
        task_id=task_id,
        name=name,
        z=Decimal("1"),
        k=total,
        h=human_duration,
        predecessors=predecessors,
        phases=phases,
        quality_gate_id=quality_gate_id,
    )


def build_exp04_scenario(
    matrix: Exp04Matrix,
    *,
    m: int,
    overhead_rate: Decimal,
    lambda_h: Decimal,
) -> tuple[Scenario, Decimal, Decimal, Decimal]:
    base = _base_scenario(matrix)
    selected = base.task_by_id[matrix.selected_task_id]
    if tuple(phase.resource for phase in selected.phases) != (
        "human",
        "agent",
        "human",
    ):
        raise ScenarioError("EXP-04B selected task must have an IO phase profile")
    useful_input_human = selected.phases[0].base_duration
    useful_agent = selected.phases[1].base_duration
    useful_final_human = selected.phases[2].base_duration
    total_overhead = Decimal(m - 1) * overhead_rate * matrix.base_effort
    human_overhead = total_overhead * lambda_h
    agent_overhead = total_overhead - human_overhead
    input_human_overhead = human_overhead / Decimal(2)
    join_human_overhead = human_overhead - input_human_overhead
    input_agent_overhead = agent_overhead / Decimal(2)
    join_agent_overhead = agent_overhead - input_agent_overhead

    part_ids = tuple(f"{selected.task_id}_part_{index:02d}" for index in range(1, m + 1))
    join_id = f"{selected.task_id}_join"
    per_part_human = (
        useful_input_human + input_human_overhead
    ) / Decimal(m)
    per_part_agent = (useful_agent + input_agent_overhead) / Decimal(m)
    parts = [
        _task_from_durations(
            task_id=part_id,
            name=f"Decomposed {selected.name}, part {index}/{m}",
            predecessors=selected.predecessors,
            agent_duration=per_part_agent,
            human_duration=per_part_human,
            phases=(
                PhaseSpec("specification", "human", per_part_human),
                PhaseSpec("implementation", "agent", per_part_agent),
            ),
            quality_gate_id=f"{matrix.selected_quality_gate_id}_part_{index:02d}",
        )
        for index, part_id in enumerate(part_ids, start=1)
    ]
    join_human = useful_final_human + join_human_overhead
    join_phases: list[PhaseSpec] = []
    if join_agent_overhead > 0:
        join_phases.append(
            PhaseSpec("integration", "agent", join_agent_overhead)
        )
    join_phases.append(PhaseSpec("acceptance", "human", join_human))
    join = _task_from_durations(
        task_id=join_id,
        name=f"Integration and acceptance for {selected.name}",
        predecessors=part_ids,
        agent_duration=join_agent_overhead,
        human_duration=join_human,
        phases=tuple(join_phases),
        quality_gate_id=matrix.selected_quality_gate_id,
    )

    tasks: list[TaskSpec] = []
    for task in base.tasks:
        if task.task_id == selected.task_id:
            tasks.extend(parts)
            tasks.append(join)
            continue
        predecessors = tuple(
            join_id if item == selected.task_id else item
            for item in task.predecessors
        )
        tasks.append(replace(task, predecessors=predecessors))
    rate_label = str(int(overhead_rate * Decimal("1000"))).zfill(3)
    lambda_label = str(int(lambda_h * Decimal("10"))).zfill(2)
    scenario = Scenario(
        schema_version=1,
        scenario_id=(
            f"exp04b_m{m:02d}_ro{rate_label}_lh{lambda_label}"
        ),
        variant_id="EXP-04B",
        time_unit=matrix.time_unit,
        tolerance=matrix.tolerance,
        x=Decimal("1"),
        p=matrix.agent_count,
        c=matrix.c,
        gamma=matrix.gamma,
        tasks=tuple(tasks),
        schedules=(),
        source_path=matrix.source_path,
    )
    validate_scenario(scenario)
    return scenario, total_overhead, human_overhead, agent_overhead


def _format_decimal(value: Decimal | None) -> str:
    return "" if value is None else format(value, "f")


def _canonical_decimal(value: Decimal) -> str:
    return format(value.normalize(), "f")


def _semantic_payload(scenario: Scenario) -> dict[str, Any]:
    return {
        "schema_version": scenario.schema_version,
        "time_unit": _canonical_decimal(scenario.time_unit),
        "tolerance": _canonical_decimal(scenario.tolerance),
        "x": _canonical_decimal(scenario.x),
        "p": scenario.p,
        "c": _canonical_decimal(scenario.c),
        "gamma": _canonical_decimal(scenario.gamma),
        "tasks": [
            {
                "task_id": task.task_id,
                "z": _canonical_decimal(task.z),
                "k": _canonical_decimal(task.k),
                "h": _canonical_decimal(task.h),
                "quality_gate_id": task.quality_gate_id,
                "predecessors": list(task.predecessors),
                "phases": [
                    {
                        "phase_id": phase.phase_id,
                        "resource": phase.resource,
                        "base_duration": _canonical_decimal(phase.base_duration),
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


def iter_exp04_cases(matrix: Exp04Matrix) -> Iterator[Exp04Case]:
    deduplicated: dict[str, Exp04Case] = {}
    order: list[str] = []
    for m in matrix.m_values:
        for overhead_rate in matrix.overhead_rates:
            for lambda_h in matrix.human_overhead_shares:
                parameters = Exp04Parameters(m, overhead_rate, lambda_h)
                scenario, total, human, agent = build_exp04_scenario(
                    matrix,
                    m=m,
                    overhead_rate=overhead_rate,
                    lambda_h=lambda_h,
                )
                semantic_sha256 = _json_sha256(_semantic_payload(scenario))
                if semantic_sha256 in deduplicated:
                    current = deduplicated[semantic_sha256]
                    deduplicated[semantic_sha256] = replace(
                        current,
                        aliases=(*current.aliases, parameters),
                    )
                    continue
                order.append(semantic_sha256)
                deduplicated[semantic_sha256] = Exp04Case(
                    parameters=parameters,
                    aliases=(parameters,),
                    semantic_sha256=semantic_sha256,
                    scenario=scenario,
                    total_overhead=total,
                    human_overhead=human,
                    agent_overhead=agent,
                )
    if len(deduplicated) != matrix.expected_unique_point_count:
        raise RuntimeError(
            f"EXP-04B deduplication produced {len(deduplicated)} points, "
            f"expected {matrix.expected_unique_point_count}"
        )
    yield from (deduplicated[item] for item in order)


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


def _critical_chain(scenario: Scenario, schedule: ScheduleSpec) -> str:
    by_key = {
        (interval.task_id, interval.phase_id): interval
        for interval in schedule.phases
    }
    specs = {
        (task.task_id, phase.phase_id): phase
        for task in scenario.tasks
        for phase in task.phases
    }
    assignments = {item.task_id: item for item in schedule.assignments}
    predecessors: dict[tuple[str, str], list[tuple[tuple[str, str], str]]] = {
        key: [] for key in by_key
    }
    for task in scenario.tasks:
        keys = [(task.task_id, phase.phase_id) for phase in task.phases]
        for previous, current in zip(keys, keys[1:]):
            if by_key[previous].end == by_key[current].start:
                predecessors[current].append((previous, "task"))
        first = keys[0]
        for predecessor_id in task.predecessors:
            predecessor_task = scenario.task_by_id[predecessor_id]
            last = (predecessor_id, predecessor_task.phases[-1].phase_id)
            if by_key[last].end == by_key[first].start:
                predecessors[first].append((last, "precedence"))

    human_keys = sorted(
        (key for key, phase in specs.items() if phase.resource == "human"),
        key=lambda key: (by_key[key].start, by_key[key].end, key),
    )
    for previous, current in zip(human_keys, human_keys[1:]):
        if by_key[previous].end == by_key[current].start:
            predecessors[current].append((previous, "human"))

    by_agent: dict[int, list[str]] = {}
    for task_id, assignment in assignments.items():
        by_agent.setdefault(assignment.agent, []).append(task_id)
    for task_ids in by_agent.values():
        task_ids.sort(key=lambda task_id: assignments[task_id].assigned_at)
        for previous_id, current_id in zip(task_ids, task_ids[1:]):
            previous_task = scenario.task_by_id[previous_id]
            current_task = scenario.task_by_id[current_id]
            previous = (previous_id, previous_task.phases[-1].phase_id)
            current = (current_id, current_task.phases[0].phase_id)
            if by_key[previous].end == by_key[current].start:
                predecessors[current].append((previous, "agent"))

    ordered = sorted(by_key, key=lambda key: (by_key[key].end, by_key[key].start, key))
    scores: dict[tuple[str, str], Decimal] = {}
    chains: dict[tuple[str, str], list[tuple[tuple[str, str], str | None]]] = {}
    for key in ordered:
        interval = by_key[key]
        duration = interval.end - interval.start
        candidates = predecessors[key]
        if not candidates:
            scores[key] = duration
            chains[key] = [(key, None)]
            continue
        previous, edge = max(
            candidates,
            key=lambda item: (scores[item[0]], item[1], item[0]),
        )
        scores[key] = scores[previous] + duration
        chains[key] = [*chains[previous], (key, edge)]
    makespan = max(interval.end for interval in schedule.phases)
    ending = [key for key, interval in by_key.items() if interval.end == makespan]
    last = max(ending, key=lambda key: (scores[key], key))
    return " -> ".join(
        (
            f"{key[0]}.{key[1]}"
            if edge is None
            else f"[{edge}] {key[0]}.{key[1]}"
        )
        for key, edge in chains[last]
    )


def _trace_fields(prefix: str, trace: ScheduleTrace | None) -> dict[str, str]:
    if trace is None:
        return {
            f"{prefix}_makespan": "",
            f"{prefix}_queue": "",
            f"{prefix}_blocked_any": "",
            f"{prefix}_full_agent_stop": "",
            f"{prefix}_maximum_queue_length": "",
        }
    return {
        f"{prefix}_makespan": _format_decimal(trace.makespan),
        f"{prefix}_queue": _format_decimal(trace.queue_time),
        f"{prefix}_blocked_any": _format_decimal(trace.blocked_any_time),
        f"{prefix}_full_agent_stop": _format_decimal(trace.full_agent_stop_time),
        f"{prefix}_maximum_queue_length": str(trace.maximum_queue_length),
    }


def _result_row(
    case: Exp04Case,
    aggregate: AggregateMetrics,
    base_aggregate: AggregateMetrics,
    exact: ExactSolution,
    exact_trace: ScheduleTrace | None,
    baseline_trace: ScheduleTrace,
    exact_chain: str,
    policy_id: str,
) -> dict[str, str]:
    is_optimal = exact.status == "OPTIMAL" and exact.objective is not None
    exact_gap = exact.objective - aggregate.b4 if exact.objective is not None else None
    row = {
        "experiment_id": "EXP-04B",
        "scenario_id": case.scenario.scenario_id,
        "semantic_sha256": case.semantic_sha256,
        "m": str(case.parameters.m),
        "overhead_rate": _format_decimal(case.parameters.overhead_rate),
        "lambda_h": _format_decimal(case.parameters.lambda_h),
        "alias_count": str(len(case.aliases)),
        "aliases": ";".join(item.label for item in case.aliases),
        "policy_id": policy_id,
        "task_count": str(len(case.scenario.tasks)),
        "total_overhead": _format_decimal(case.total_overhead),
        "human_overhead": _format_decimal(case.human_overhead),
        "agent_overhead": _format_decimal(case.agent_overhead),
        "useful_W4": _format_decimal(base_aggregate.w4),
        "useful_H": _format_decimal(base_aggregate.h),
        "W4": _format_decimal(aggregate.w4),
        "H": _format_decimal(aggregate.h),
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
        "exact_critical_chain": exact_chain,
        "baseline_gap_to_optimum": (
            _format_decimal(baseline_trace.makespan - exact.objective)
            if is_optimal and exact.objective is not None
            else ""
        ),
    }
    row.update(_trace_fields("exact", exact_trace))
    row.update(_trace_fields("baseline", baseline_trace))
    return row


def _curve_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    base = next(row for row in rows if row["m"] == "1")
    curves: list[dict[str, str]] = []
    zero_rows = [row for row in rows if row["overhead_rate"] == "0"]
    for row in zero_rows:
        curves.append(
            {**row, "curve_overhead_rate": "0", "curve_lambda_h": "shared"}
        )
    for overhead_rate in ("0.025", "0.05", "0.10", "0.20"):
        for lambda_h in ("0", "0.5", "1"):
            curves.append(
                {
                    **base,
                    "curve_overhead_rate": overhead_rate,
                    "curve_lambda_h": lambda_h,
                }
            )
            for row in rows:
                if (
                    row["m"] != "1"
                    and row["overhead_rate"] == overhead_rate
                    and row["lambda_h"] == lambda_h
                ):
                    curves.append(
                        {
                            **row,
                            "curve_overhead_rate": overhead_rate,
                            "curve_lambda_h": lambda_h,
                        }
                    )
    if len(curves) != 78:
        raise RuntimeError(f"EXP-04B expected 78 curve positions, got {len(curves)}")
    return curves


def _summary_rows(curves: list[dict[str, str]], tolerance: Decimal) -> list[dict[str, str]]:
    groups: dict[tuple[str, str], list[dict[str, str]]] = {}
    for row in curves:
        groups.setdefault(
            (row["curve_overhead_rate"], row["curve_lambda_h"]), []
        ).append(row)
    summaries: list[dict[str, str]] = []
    for (overhead_rate, lambda_h), selected in groups.items():
        selected.sort(key=lambda row: int(row["m"]))
        if not all(row["T_star"] for row in selected):
            minimum_exact = None
        else:
            minimum_exact = min(
                selected,
                key=lambda row: (Decimal(row["T_star"]), int(row["m"])),
            )
        minimum_b4 = min(
            selected,
            key=lambda row: (Decimal(row["B4"]), int(row["m"])),
        )
        minimum_baseline = min(
            selected,
            key=lambda row: (Decimal(row["baseline_makespan"]), int(row["m"])),
        )
        exact_values = [Decimal(row["T_star"]) for row in selected] if minimum_exact else []
        exact_minimum = min(exact_values) if exact_values else None
        minimizing_ms = (
            [int(row["m"]) for row in selected if Decimal(row["T_star"]) == exact_minimum]
            if exact_minimum is not None
            else []
        )
        interior_u = bool(
            exact_minimum is not None
            and any(m not in {1, 8} for m in minimizing_ms)
            and exact_values[0] > exact_minimum + tolerance
            and exact_values[-1] > exact_minimum + tolerance
        )
        summaries.append(
            {
                "overhead_rate": overhead_rate,
                "lambda_h": lambda_h,
                "minimizing_m_B4": minimum_b4["m"],
                "minimum_B4": minimum_b4["B4"],
                "minimizing_m_T_star": minimum_exact["m"] if minimum_exact else "",
                "minimum_T_star": minimum_exact["T_star"] if minimum_exact else "",
                "minimizing_m_baseline": minimum_baseline["m"],
                "minimum_baseline": minimum_baseline["baseline_makespan"],
                "interior_U_shape_T_star": str(interior_u).lower(),
                "T_star_at_m1": selected[0]["T_star"],
                "T_star_at_m8": selected[-1]["T_star"],
                "m8_minus_minimum_T_star": (
                    _format_decimal(exact_values[-1] - exact_minimum)
                    if exact_minimum is not None
                    else ""
                ),
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


def _exp04a_rows(matrix: Exp04Matrix, project_root: Path) -> list[dict[str, str]]:
    source_path = project_root / matrix.exp04a_source_results
    with source_path.open(newline="", encoding="utf-8") as source:
        source_rows = list(csv.DictReader(source))
    selected = [row for row in source_rows if row["variant_id"] in matrix.exp04a_variants]
    if len(selected) != 2 or not all(row["solver_status"] == "OPTIMAL" for row in selected):
        raise RuntimeError("EXP-04A source rows are missing or not OPTIMAL")
    selected.sort(key=lambda row: row["variant_id"])
    reference = Decimal(selected[0]["T_star"])
    return [
        {
            "experiment_id": "EXP-04A",
            "source_experiment": "EXP-00",
            "variant_id": row["variant_id"],
            "decomposition_level": "0" if row["variant_id"] == "3" else "1",
            "P": "4",
            "overhead": "0",
            "W4": row["W4"],
            "L4": row["L4"],
            "B4": row["B4"],
            "T_star": row["T_star"],
            "delta_T_star_from_variant_3": _format_decimal(
                Decimal(row["T_star"]) - reference
            ),
            "solver_status": row["solver_status"],
        }
        for row in selected
    ]


def _dependencies() -> dict[str, str]:
    versions: dict[str, str] = {}
    for distribution in ("matplotlib", "ortools", "PyYAML", "pytest"):
        try:
            versions[distribution] = importlib.metadata.version(distribution)
        except importlib.metadata.PackageNotFoundError:
            versions[distribution] = "not-installed"
    return versions


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_report(
    path: Path,
    *,
    matrix: Exp04Matrix,
    exp04a: list[dict[str, str]],
    rows: list[dict[str, str]],
    summaries: list[dict[str, str]],
) -> None:
    optimal_count = sum(row["solver_status"] == "OPTIMAL" for row in rows)
    u_rows = [row for row in summaries if row["interior_U_shape_T_star"] == "true"]
    zero = next(row for row in summaries if row["overhead_rate"] == "0")
    summary_lines = "\n".join(
        "| {rate} | {lambda_h} | {m_b4} | {m_exact} | {m_base} | {minimum} | {u} | {growth} |".format(
            rate=row["overhead_rate"],
            lambda_h=row["lambda_h"],
            m_b4=row["minimizing_m_B4"],
            m_exact=row["minimizing_m_T_star"] or "—",
            m_base=row["minimizing_m_baseline"],
            minimum=row["minimum_T_star"] or "—",
            u="да" if row["interior_U_shape_T_star"] == "true" else "нет",
            growth=row["m8_minus_minimum_T_star"] or "—",
        )
        for row in summaries
    )
    report = rf"""# Отчёт по EXP-04: контролируемая декомпозиция

Дата отчёта: 2026-08-07

Статус: EXP-04A оформлен из доказанных результатов EXP-00; EXP-04B выполнен на
{len(rows)} уникальных сценариях и {len(summaries)} кривых параметров.

## 1. Резюме

Все {optimal_count} из {len(rows)} уникальных точек EXP-04B доказаны как
`OPTIMAL`. Внутренний U-образный минимум доказанного $T^*$ обнаружен в
{len(u_rows)} из {len(summaries)} кривых. Нулевой overhead даёт минимизирующее
$m={zero['minimizing_m_T_star']}$ и $T^*={zero['minimum_T_star']}$ ч.

Практическая пара EXP-04A подтверждает только структурное сокращение
$43.2\to36.7$ ч при нулевом overhead. Она не используется как доказательство
общей U-образной зависимости.

## 2. Зафиксированный оператор EXP-04B

- база: two-layer $N=4$, $P=4$, IO, $r_h=0.25$;
- декомпозируется критическая sink-вершина `t04` с усилием 24 ч;
- её входная human-фаза и agent-работа делятся между $m$ параллельными
  подзадачами, финальная приёмка переносится на join;
- полный overhead равен $(m-1)r_o\cdot24$;
- половина overhead распределяется поровну по входам подзадач, половина
  добавляется на join; $\lambda_h$ задаёт human-долю;
- исходный quality gate `qg_t04` сохраняется на join;
- $m\in\{{1,2,3,4,6,8\}}$, $r_o\in\{{0,0.025,0.05,0.10,0.20\}}$,
  $\lambda_h\in\{{0,0.5,1\}}$.

Из 90 комбинаций получено 66 уникальных сценариев. При $m=1$ overhead равен
нулю для всех $r_o,\lambda_h$; при $r_o=0$ три значения $\lambda_h$ также
совпадают. Для построения 13 содержательных кривых общая точка $m=1$
переиспользуется, поэтому на рисунке 78 позиций, но только 66 решений.

## 3. Практическое сравнение EXP-04A

| Вариант | Уровень декомпозиции | $L_4$ | $B_4$ | $T^*$ | Изменение к варианту 3 |
|---|---:|---:|---:|---:|---:|
| 3 | 0 | {exp04a[0]['L4']} | {exp04a[0]['B4']} | {exp04a[0]['T_star']} | {exp04a[0]['delta_T_star_from_variant_3']} |
| 4 | 1 | {exp04a[1]['L4']} | {exp04a[1]['B4']} | {exp04a[1]['T_star']} | {exp04a[1]['delta_T_star_from_variant_3']} |

## 4. U-кривые точного makespan

![Кривые декомпозиции EXP-04B](../figures/exp04_decomposition_curves.png)

[SVG-версия](../figures/exp04_decomposition_curves.svg).

Сплошные линии показывают только доказанный $T^*$, пунктирные — $B_4$.
Нулевой overhead сообщается отдельно; три панели разделяют агентный, смешанный
и человеческий overhead и не соединяют разные $r_o$ или $\lambda_h$.

## 5. Оптимальная гранулярность

![Карта оптимальной гранулярности](../figures/exp04_optimal_granularity.png)

[SVG-версия](../figures/exp04_optimal_granularity.svg).

| $r_o$ | $\lambda_h$ | $m$ для min $B_4$ | $m$ для min $T^*$ | $m$ baseline | Min $T^*$ | U у $T^*$ | $T^*(8)-\min T^*$ |
|---:|---:|---:|---:|---:|---:|---|---:|
{summary_lines}

U-образность считается подтверждённой только если минимум $T^*$ лежит внутри
сетки, а значения при $m=1$ и $m=8$ превышают его больше tolerance. Минимум
только у $B_4$ или baseline таким результатом не считается.

## 6. Трассировка overhead и расписаний

Для каждой точки сохранены total/human/agent overhead, $W_4$, $H$, $L_4$,
очередь, полная остановка слотов и реализованная exact critical chain. Проверки
требуют тождеств $W_4-W_4^{{useful}}=overhead$ и
$H-H^{{useful}}=\lambda_h\,overhead$. При $r_o=0$ полезная agent- и
human-работа сохраняются точно для любого $m$.

## 7. Воспроизводимость

```bash
cd simple_model_full/experiments
uv sync --python 3.13
uv run pytest -ra
uv run python -m experiments run --experiment EXP-04
```

Артефакты:

- [замороженная матрица](../scenarios/canonical/exp04_matrix.yaml);
- [EXP-04A](exp04a_summary.csv);
- [66 точных прогонов EXP-04B](exp04b_runs.csv);
- [оптимальная гранулярность](exp04b_optimal_m.csv);
- [фазовые трассы](exp04b_phases.csv) и [события](exp04b_events.csv);
- [manifest](exp04_manifest.json).

## 8. Ограничения

- Оператор и overhead синтетические; исследована одна критическая вершина
  одного канонического DAG.
- CP-SAT минимизирует makespan, но не очередь как вторичную цель.
- Join сохраняет полезную финальную приёмку, поэтому $m=1$ является
  семантической декомпозированной базой, а не побайтово тем же DAG.
- U-образный минимум на конечной сетке не доказывает оптимальность для всех
  целых $m$ вне $\{{1,2,3,4,6,8\}}$.

## 9. Вывод

EXP-04 разделяет практический структурный эффект и канонический оператор с
полностью трассируемым overhead. Результаты остаются в каталоге экспериментов и
пока не вносятся в текст статьи.
"""
    path.write_text(report, encoding="utf-8")


def run_exp04(project_root: Path, output_directory: Path) -> tuple[Path, ...]:
    matrix_path = project_root / "scenarios" / "canonical" / "exp04_matrix.yaml"
    matrix = load_exp04_matrix(matrix_path)
    source_matrix_path = project_root / matrix.source_matrix
    exp04a_source_path = project_root / matrix.exp04a_source_results
    output_directory.mkdir(parents=True, exist_ok=True)
    figure_directory = project_root / "figures"
    exp04a = _exp04a_rows(matrix, project_root)
    base_aggregate = compute_aggregates(_base_scenario(matrix))
    cases = list(iter_exp04_cases(matrix))
    rows: list[dict[str, str]] = []
    phase_rows: list[dict[str, str]] = []
    event_rows: list[dict[str, str]] = []

    for index, case in enumerate(cases, start=1):
        aggregate = compute_aggregates(case.scenario)
        if aggregate.w4 - base_aggregate.w4 != case.total_overhead:
            raise RuntimeError(f"{case.scenario.scenario_id}: W4 overhead audit failed")
        if aggregate.h - base_aggregate.h != case.human_overhead:
            raise RuntimeError(f"{case.scenario.scenario_id}: H overhead audit failed")
        if (
            case.scenario.task_by_id[f"{matrix.selected_task_id}_join"].quality_gate_id
            != matrix.selected_quality_gate_id
        ):
            raise RuntimeError(f"{case.scenario.scenario_id}: quality gate was not preserved")

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
            experiment_id="EXP-04B",
        )
        exact = solve_exact(
            case.scenario,
            time_limit_seconds=matrix.solver_time_limit_seconds,
            random_seed=matrix.solver_random_seed,
            workers=matrix.solver_workers,
        )
        exact_trace = None
        exact_chain = ""
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
                experiment_id="EXP-04B",
            )
            exact_chain = _critical_chain(case.scenario, exact.schedule)
        if exact.status not in {"OPTIMAL", "FEASIBLE"}:
            raise RuntimeError(
                f"{case.scenario.scenario_id}: exact solver returned {exact.status}"
            )
        rows.append(
            _result_row(
                case,
                aggregate,
                base_aggregate,
                exact,
                exact_trace,
                baseline_trace,
                exact_chain,
                matrix.policy_id,
            )
        )
        phase_rows.extend(baseline_trace.phase_rows)
        event_rows.extend(baseline_trace.event_rows)
        if exact_trace is not None:
            phase_rows.extend(exact_trace.phase_rows)
            event_rows.extend(exact_trace.event_rows)
        if index % 10 == 0 or index == len(cases):
            print(f"EXP-04B exact progress: {index}/{len(cases)}", flush=True)

    curves = _curve_rows(rows)
    summaries = _summary_rows(curves, matrix.tolerance)
    exp04a_path = output_directory / "exp04a_summary.csv"
    runs_path = output_directory / "exp04b_runs.csv"
    summary_path = output_directory / "exp04b_optimal_m.csv"
    phases_path = output_directory / "exp04b_phases.csv"
    events_path = output_directory / "exp04b_events.csv"
    _write_csv(exp04a_path, exp04a)
    _write_csv(runs_path, rows)
    _write_csv(summary_path, summaries)
    _write_csv(phases_path, phase_rows)
    _write_csv(events_path, event_rows)

    figure_paths = [
        *build_decomposition_curves(
            curves,
            figure_directory / "exp04_decomposition_curves",
        ),
        *build_optimal_granularity_map(
            summaries,
            figure_directory / "exp04_optimal_granularity",
        ),
    ]
    report_path = output_directory / "exp04_report.md"
    _write_report(
        report_path,
        matrix=matrix,
        exp04a=exp04a,
        rows=rows,
        summaries=summaries,
    )

    outputs_without_manifest = [
        exp04a_path,
        runs_path,
        summary_path,
        phases_path,
        events_path,
        report_path,
        *figure_paths,
    ]
    implementation_paths = sorted(
        (project_root / "src" / "experiments").glob("*.py")
    ) + [project_root / "pyproject.toml", project_root / "uv.lock"]
    manifest_path = output_directory / "exp04_manifest.json"
    manifest = {
        "experiment_id": "EXP-04",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "command": "uv run python -m experiments run --experiment EXP-04",
        **git_provenance(project_root),
        "matrix": {
            "path": str(matrix_path.relative_to(project_root)),
            "sha256": _sha256(matrix_path),
            "frozen_at": matrix.frozen_at,
            "raw_combinations": matrix.raw_combination_count,
            "unique_points": len(rows),
            "curve_positions": len(curves),
        },
        "sources": [
            {
                "path": str(source_matrix_path.relative_to(project_root)),
                "sha256": _sha256(source_matrix_path),
            },
            {
                "path": str(exp04a_source_path.relative_to(project_root)),
                "sha256": _sha256(exp04a_source_path),
            },
        ],
        "solver": {
            "time_limit_seconds": matrix.solver_time_limit_seconds,
            "random_seed": matrix.solver_random_seed,
            "workers": matrix.solver_workers,
        },
        "baseline_policy_id": matrix.policy_id,
        "dependencies": _dependencies(),
        "summary": {
            "exp04a_points": len(exp04a),
            "exp04b_unique_points": len(rows),
            "optimal_points": sum(row["solver_status"] == "OPTIMAL" for row in rows),
            "feasible_points": sum(row["solver_status"] == "FEASIBLE" for row in rows),
            "parameter_curves": len(summaries),
            "exact_U_shaped_curves": sum(
                row["interior_U_shape_T_star"] == "true" for row in summaries
            ),
        },
        "scenario_hashes": [
            {
                "scenario_id": row["scenario_id"],
                "semantic_sha256": row["semantic_sha256"],
                "aliases": row["aliases"].split(";"),
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
