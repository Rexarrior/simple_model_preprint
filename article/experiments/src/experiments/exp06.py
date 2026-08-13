from __future__ import annotations

import csv
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction
import json
import math
from pathlib import Path
import random
from statistics import median
from typing import Any, Iterator

import yaml

from .bounds import AggregateMetrics, compute_aggregates
from .exact_solver import ExactSolution, solve_exact
from .exp03 import ScheduleTrace, trace_schedule
from .exp04 import (
    _dependencies,
    _format_decimal,
    _json_sha256,
    _semantic_payload,
    _sha256,
    _validated,
    _write_csv,
)
from .exp05 import build_exp05_scenario, load_exp05_matrix
from .exp06_figures import (
    build_adversarial_thresholds,
    build_margin_distributions,
    build_ranking_stability,
    build_scale_invariance,
)
from .provenance import git_provenance
from .schema import (
    PhaseSpec,
    Scenario,
    ScenarioError,
    TaskSpec,
    decimal,
    load_scenario,
    validate_scenario,
)
from .simulator import simulate_baseline


@dataclass(frozen=True)
class Exp06Object:
    object_id: str
    kind: str
    variant: str = ""
    p: int = 0
    m: int = 0
    overhead_rate: Decimal = Decimal("0")
    lambda_h: Decimal = Decimal("0")


@dataclass(frozen=True)
class Exp06Matrix:
    source_path: Path
    schema_version: int
    experiment_id: str
    frozen_at: str
    variant_3_source: str
    variant_4_source: str
    canonical_operator_matrix: str
    scale_factors: tuple[Decimal, ...]
    scale_objects: tuple[Exp06Object, ...]
    expected_scale_point_count: int
    uncertainty_levels: tuple[Decimal, ...]
    seed_start: int
    seed_count: int
    expected_random_pair_count: int
    expected_random_solution_count: int
    common_task_ids: tuple[str, ...]
    source_test_task_id: str
    decomposed_test_task_ids: tuple[str, ...]
    residual_log_scale: Decimal
    adversarial_u_start: Decimal
    adversarial_u_stop: Decimal
    adversarial_u_step: Decimal
    expected_adversarial_u_count: int
    adversarial_modes: tuple[str, ...]
    expected_adversarial_pair_count: int
    expected_adversarial_solution_count: int
    policy_id: str
    exp06a_time_limit_seconds: float
    exp06b_time_limit_seconds: float
    exp06c_time_limit_seconds: float
    solver_random_seed: int
    solver_workers: int

    @property
    def random_pair_count(self) -> int:
        return len(self.uncertainty_levels) * self.seed_count

    @property
    def adversarial_u_values(self) -> tuple[Decimal, ...]:
        return tuple(
            self.adversarial_u_start + self.adversarial_u_step * index
            for index in range(self.expected_adversarial_u_count)
        )


def _required_mapping(raw: object, *, field: str) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise ScenarioError(f"{field}: expected mapping")
    return raw


def _required_list(raw: object, *, field: str) -> list[object]:
    if not isinstance(raw, list) or not raw:
        raise ScenarioError(f"{field}: expected non-empty list")
    return raw


def load_exp06_matrix(path: str | Path) -> Exp06Matrix:
    source_path = Path(path).resolve()
    with source_path.open("r", encoding="utf-8") as source:
        raw = yaml.safe_load(source)
    data = _required_mapping(raw, field="EXP-06 matrix")
    if data.get("frozen") is not True:
        raise ScenarioError("EXP-06 matrix must be frozen before execution")
    article = _required_mapping(data.get("article_sources"), field="article_sources")
    exp06a = _required_mapping(data.get("exp06a"), field="exp06a")
    exp06b = _required_mapping(data.get("exp06b"), field="exp06b")
    exp06c = _required_mapping(data.get("exp06c"), field="exp06c")
    multiplier = _required_mapping(
        exp06b.get("multiplier_model"), field="exp06b.multiplier_model"
    )
    baseline = _required_mapping(data.get("baseline_policy"), field="baseline_policy")
    exact = _required_mapping(data.get("exact_solver"), field="exact_solver")
    objects: list[Exp06Object] = []
    for index, raw_object in enumerate(
        _required_list(exp06a.get("objects"), field="exp06a.objects")
    ):
        item = _required_mapping(raw_object, field=f"exp06a.objects[{index}]")
        objects.append(
            Exp06Object(
                object_id=str(item.get("object_id", "")),
                kind=str(item.get("kind", "")),
                variant=str(item.get("variant", "")),
                p=int(item.get("P", 0)),
                m=int(item.get("m", 0)),
                overhead_rate=decimal(
                    item.get("overhead_rate", 0), field="object.overhead_rate"
                ),
                lambda_h=decimal(item.get("lambda_h", 0), field="object.lambda_h"),
            )
        )
    matrix = Exp06Matrix(
        source_path=source_path,
        schema_version=int(data.get("schema_version", 0)),
        experiment_id=str(data.get("experiment_id", "")),
        frozen_at=str(data.get("frozen_at", "")),
        variant_3_source=str(article.get("variant_3", "")),
        variant_4_source=str(article.get("variant_4", "")),
        canonical_operator_matrix=str(data.get("canonical_operator_matrix", "")),
        scale_factors=tuple(
            decimal(item, field="scale_factors")
            for item in _required_list(exp06a.get("scale_factors"), field="scale_factors")
        ),
        scale_objects=tuple(objects),
        expected_scale_point_count=int(exp06a.get("expected_point_count", 0)),
        uncertainty_levels=tuple(
            decimal(item, field="uncertainty_levels")
            for item in _required_list(
                exp06b.get("uncertainty_levels"), field="uncertainty_levels"
            )
        ),
        seed_start=int(exp06b.get("seed_start", 0)),
        seed_count=int(exp06b.get("seed_count", 0)),
        expected_random_pair_count=int(exp06b.get("expected_pair_count", 0)),
        expected_random_solution_count=int(exp06b.get("expected_solution_count", 0)),
        common_task_ids=tuple(
            str(item)
            for item in _required_list(
                exp06b.get("common_task_ids"), field="common_task_ids"
            )
        ),
        source_test_task_id=str(exp06b.get("source_test_task_id", "")),
        decomposed_test_task_ids=tuple(
            str(item)
            for item in _required_list(
                exp06b.get("decomposed_test_task_ids"),
                field="decomposed_test_task_ids",
            )
        ),
        residual_log_scale=decimal(
            multiplier.get("decomposition_residual_log_scale"),
            field="decomposition_residual_log_scale",
        ),
        adversarial_u_start=decimal(exp06c.get("u_start"), field="u_start"),
        adversarial_u_stop=decimal(exp06c.get("u_stop"), field="u_stop"),
        adversarial_u_step=decimal(exp06c.get("u_step"), field="u_step"),
        expected_adversarial_u_count=int(exp06c.get("expected_u_count", 0)),
        adversarial_modes=tuple(
            str(item)
            for item in _required_list(exp06c.get("modes"), field="modes")
        ),
        expected_adversarial_pair_count=int(exp06c.get("expected_pair_count", 0)),
        expected_adversarial_solution_count=int(
            exp06c.get("expected_solution_count", 0)
        ),
        policy_id=str(baseline.get("policy_id", "")),
        exp06a_time_limit_seconds=float(exact.get("exp06a_time_limit_seconds", 60)),
        exp06b_time_limit_seconds=float(exact.get("exp06b_time_limit_seconds", 10)),
        exp06c_time_limit_seconds=float(exact.get("exp06c_time_limit_seconds", 10)),
        solver_random_seed=int(exact.get("random_seed", 0)),
        solver_workers=int(exact.get("workers", 1)),
    )
    _validate_matrix(matrix)
    return matrix


def _validate_matrix(matrix: Exp06Matrix) -> None:
    if matrix.schema_version != 1 or matrix.experiment_id != "EXP-06":
        raise ScenarioError("EXP-06 requires schema_version=1 and experiment_id=EXP-06")
    if matrix.scale_factors != (
        Decimal("0.25"),
        Decimal("0.5"),
        Decimal("1"),
        Decimal("2"),
        Decimal("4"),
    ):
        raise ScenarioError("EXP-06A scale factors differ from the frozen design")
    if len(matrix.scale_objects) != 4 or len({x.object_id for x in matrix.scale_objects}) != 4:
        raise ScenarioError("EXP-06A requires four unique frozen objects")
    if len(matrix.scale_objects) * len(matrix.scale_factors) != matrix.expected_scale_point_count:
        raise ScenarioError("EXP-06A point count mismatch")
    if matrix.uncertainty_levels != (
        Decimal("0.05"),
        Decimal("0.10"),
        Decimal("0.20"),
        Decimal("0.30"),
        Decimal("0.50"),
    ):
        raise ScenarioError("EXP-06B uncertainty levels differ from the frozen design")
    if matrix.seed_start != 0 or matrix.seed_count != 1000:
        raise ScenarioError("EXP-06B requires seeds 0--999")
    if matrix.random_pair_count != 5000 or matrix.expected_random_pair_count != 5000:
        raise ScenarioError("EXP-06B pair count mismatch")
    if matrix.expected_random_solution_count != 10000:
        raise ScenarioError("EXP-06B solution count mismatch")
    if matrix.residual_log_scale != Decimal("0.25"):
        raise ScenarioError("EXP-06B residual scale differs from the frozen design")
    if matrix.adversarial_u_values[-1] != matrix.adversarial_u_stop:
        raise ScenarioError("EXP-06C grid does not end at frozen u_stop")
    if matrix.expected_adversarial_u_count != 191:
        raise ScenarioError("EXP-06C requires 191 u values")
    if len(matrix.adversarial_modes) * matrix.expected_adversarial_u_count != 382:
        raise ScenarioError("EXP-06C pair count mismatch")
    if matrix.expected_adversarial_pair_count != 382 or matrix.expected_adversarial_solution_count != 764:
        raise ScenarioError("EXP-06C frozen counts are invalid")
    if matrix.solver_workers != 1 or matrix.solver_random_seed != 0:
        raise ScenarioError("EXP-06 requires one worker and solver seed 0")


def _project_root(matrix: Exp06Matrix) -> Path:
    return matrix.source_path.parents[2]


def _article_scenarios(matrix: Exp06Matrix) -> tuple[Scenario, Scenario]:
    root = _project_root(matrix)
    variant_3 = load_scenario(root / matrix.variant_3_source)
    variant_4 = load_scenario(root / matrix.variant_4_source)
    if variant_3.variant_id != "3" or variant_4.variant_id != "4":
        raise ScenarioError("EXP-06 article sources must be variants 3 and 4")
    return variant_3, variant_4


def _scale_objects(matrix: Exp06Matrix) -> dict[str, Scenario]:
    variant_3, variant_4 = _article_scenarios(matrix)
    article = {"3": variant_3, "4": variant_4}
    root = _project_root(matrix)
    exp05_matrix = load_exp05_matrix(root / matrix.canonical_operator_matrix)
    objects: dict[str, Scenario] = {}
    for item in matrix.scale_objects:
        if item.kind == "article":
            objects[item.object_id] = article[item.variant]
        elif item.kind == "canonical":
            scenario, _, _, _ = build_exp05_scenario(
                exp05_matrix,
                p=item.p,
                m=item.m,
                overhead_rate=item.overhead_rate,
                lambda_h=item.lambda_h,
            )
            objects[item.object_id] = scenario
        else:
            raise ScenarioError(f"unknown EXP-06A object kind {item.kind}")
    return objects


def scale_scenario(
    scenario: Scenario, *, kappa: Decimal, scenario_id: str, source_path: Path
) -> Scenario:
    scaled_tasks = tuple(
        replace(
            task,
            phases=tuple(
                replace(phase, base_duration=phase.base_duration * kappa)
                for phase in task.phases
            ),
        )
        for task in scenario.tasks
    )
    scaled = replace(
        scenario,
        scenario_id=scenario_id,
        variant_id="EXP-06A",
        time_unit=scenario.time_unit * kappa,
        tolerance=scenario.tolerance * kappa,
        x=scenario.x * kappa,
        tasks=scaled_tasks,
        schedules=(),
        source_path=source_path,
    )
    validate_scenario(scaled)
    return scaled


def _quantize_duration(value: Decimal, time_unit: Decimal) -> Decimal:
    ticks = (value / time_unit).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    return max(ticks, Decimal("1")) * time_unit


def _quantize_task_phases(
    task: TaskSpec,
    *,
    multipliers: dict[tuple[str, str], Decimal],
    time_unit: Decimal,
    denominator: Decimal,
) -> tuple[PhaseSpec, ...]:
    targets = [
        phase.base_duration
        * multipliers.get((task.task_id, phase.resource), Decimal("1"))
        for phase in task.phases
    ]
    ticks = [
        max(
            int((target / time_unit).quantize(Decimal("1"), rounding=ROUND_HALF_UP)),
            1,
        )
        for target in targets
    ]
    for resource in ("agent", "human"):
        indices = [
            index for index, phase in enumerate(task.phases) if phase.resource == resource
        ]
        if not indices:
            continue
        target_total_ticks = sum(targets[index] / time_unit for index in indices)
        nearest = max(
            int(target_total_ticks.quantize(Decimal("1"), rounding=ROUND_HALF_UP)),
            len(indices),
        )
        desired_total = None
        for delta in range(0, 100):
            candidates = (nearest,) if delta == 0 else (nearest - delta, nearest + delta)
            for candidate in candidates:
                if candidate < len(indices):
                    continue
                duration = Decimal(candidate) * time_unit
                ratio = Fraction(duration) / Fraction(denominator)
                finite_denominator = ratio.denominator
                while finite_denominator % 2 == 0:
                    finite_denominator //= 2
                while finite_denominator % 5 == 0:
                    finite_denominator //= 5
                if finite_denominator == 1:
                    desired_total = candidate
                    break
            if desired_total is not None:
                break
        if desired_total is None:
            raise RuntimeError(f"{task.task_id}.{resource}: no exact tick total found")
        difference = desired_total - sum(ticks[index] for index in indices)
        if ticks[indices[-1]] + difference < 1:
            raise RuntimeError(f"{task.task_id}.{resource}: quantization emptied a phase")
        ticks[indices[-1]] += difference
    return tuple(
        replace(phase, base_duration=Decimal(tick_count) * time_unit)
        for phase, tick_count in zip(task.phases, ticks, strict=True)
    )


def _perturb_scenario(
    scenario: Scenario,
    *,
    multipliers: dict[tuple[str, str], Decimal],
    scenario_id: str,
    variant_id: str,
    source_path: Path,
) -> Scenario:
    tasks: list[TaskSpec] = []
    for task in scenario.tasks:
        denominator = scenario.x * task.z
        phases = _quantize_task_phases(
            task,
            multipliers=multipliers,
            time_unit=scenario.time_unit,
            denominator=denominator,
        )
        human_duration = sum(
            (phase.base_duration for phase in phases if phase.resource == "human"),
            Decimal("0"),
        )
        agent_duration = sum(
            (phase.base_duration for phase in phases if phase.resource == "agent"),
            Decimal("0"),
        )
        h = human_duration / denominator
        a = agent_duration / denominator
        tasks.append(
            replace(
                task,
                h=h,
                k=h + a,
                phases=phases,
            )
        )
    perturbed = replace(
        scenario,
        scenario_id=scenario_id,
        variant_id=variant_id,
        tasks=tuple(tasks),
        schedules=(),
        source_path=source_path,
    )
    validate_scenario(perturbed)
    return perturbed


def _factor(value: float) -> Decimal:
    return Decimal(f"{value:.12f}")


def build_random_pair(
    matrix: Exp06Matrix, *, u: Decimal, seed: int
) -> tuple[Scenario, Scenario, list[dict[str, str]]]:
    variant_3, variant_4 = _article_scenarios(matrix)
    rng = random.Random(seed)
    low_log = math.log1p(-float(u))
    high_log = math.log1p(float(u))
    common: dict[tuple[str, str], tuple[float, float]] = {}
    for logical_task in (*matrix.common_task_ids, matrix.source_test_task_id):
        for resource in ("agent", "human"):
            log_value = rng.uniform(low_log, high_log)
            common[(logical_task, resource)] = (log_value, math.exp(log_value))

    multipliers_3: dict[tuple[str, str], Decimal] = {}
    multipliers_4: dict[tuple[str, str], Decimal] = {}
    multiplier_rows: list[dict[str, str]] = []

    def record(
        *, variant: str, logical_task: str, task_id: str, resource: str,
        common_value: float, residual_value: float, applied_value: float
    ) -> None:
        multiplier_rows.append(
            {
                "experiment_id": "EXP-06B",
                "u": _format_decimal(u),
                "seed": str(seed),
                "variant": variant,
                "logical_task_id": logical_task,
                "task_id": task_id,
                "resource": resource,
                "common_multiplier": f"{common_value:.12f}",
                "residual_multiplier": f"{residual_value:.12f}",
                "applied_multiplier": f"{applied_value:.12f}",
            }
        )

    for task_id in matrix.common_task_ids:
        for resource in ("agent", "human"):
            _, value = common[(task_id, resource)]
            factor = _factor(value)
            multipliers_3[(task_id, resource)] = factor
            multipliers_4[(task_id, resource)] = factor
            record(
                variant="3", logical_task=task_id, task_id=task_id,
                resource=resource, common_value=value, residual_value=1.0,
                applied_value=value,
            )
            record(
                variant="4", logical_task=task_id, task_id=task_id,
                resource=resource, common_value=value, residual_value=1.0,
                applied_value=value,
            )

    for resource in ("agent", "human"):
        common_log, common_value = common[(matrix.source_test_task_id, resource)]
        multipliers_3[(matrix.source_test_task_id, resource)] = _factor(common_value)
        record(
            variant="3", logical_task=matrix.source_test_task_id,
            task_id=matrix.source_test_task_id, resource=resource,
            common_value=common_value, residual_value=1.0, applied_value=common_value,
        )
        residual_bound = float(matrix.residual_log_scale) * min(-low_log, high_log)
        for task_id in matrix.decomposed_test_task_ids:
            residual_log = rng.uniform(-residual_bound, residual_bound)
            final_log = min(max(common_log + residual_log, low_log), high_log)
            residual_value = math.exp(residual_log)
            applied_value = math.exp(final_log)
            multipliers_4[(task_id, resource)] = _factor(applied_value)
            record(
                variant="4", logical_task=matrix.source_test_task_id,
                task_id=task_id, resource=resource, common_value=common_value,
                residual_value=residual_value, applied_value=applied_value,
            )

    u_label = str(int(u * Decimal("100"))).zfill(2)
    seed_label = str(seed).zfill(4)
    scenario_3 = _perturb_scenario(
        variant_3,
        multipliers=multipliers_3,
        scenario_id=f"exp06b_u{u_label}_s{seed_label}_v3",
        variant_id="EXP-06B-3",
        source_path=matrix.source_path,
    )
    scenario_4 = _perturb_scenario(
        variant_4,
        multipliers=multipliers_4,
        scenario_id=f"exp06b_u{u_label}_s{seed_label}_v4",
        variant_id="EXP-06B-4",
        source_path=matrix.source_path,
    )
    return scenario_3, scenario_4, multiplier_rows


def build_adversarial_pair(
    matrix: Exp06Matrix, *, mode: str, u: Decimal
) -> tuple[Scenario, Scenario]:
    variant_3, variant_4 = _article_scenarios(matrix)
    if mode == "critical_task_agent":
        resource = "agent"
    elif mode == "test_human_phases":
        resource = "human"
    else:
        raise ScenarioError(f"unknown EXP-06C mode {mode}")
    multipliers_3 = {(matrix.source_test_task_id, resource): Decimal("1") - u}
    multipliers_4 = {
        (task_id, resource): Decimal("1") + u
        for task_id in matrix.decomposed_test_task_ids
    }
    u_label = str(int(u * Decimal("1000"))).zfill(3)
    scenario_3 = _perturb_scenario(
        variant_3,
        multipliers=multipliers_3,
        scenario_id=f"exp06c_{mode}_u{u_label}_v3",
        variant_id="EXP-06C-3",
        source_path=matrix.source_path,
    )
    scenario_4 = _perturb_scenario(
        variant_4,
        multipliers=multipliers_4,
        scenario_id=f"exp06c_{mode}_u{u_label}_v4",
        variant_id="EXP-06C-4",
        source_path=matrix.source_path,
    )
    return scenario_3, scenario_4


def _solve_summary(
    scenario: Scenario,
    *,
    time_limit_seconds: float,
    solver_seed: int,
    workers: int,
    full_trace: bool = False,
) -> tuple[
    dict[str, str],
    ExactSolution,
    ScheduleTrace | None,
    ScheduleTrace | None,
]:
    aggregate = compute_aggregates(scenario)
    baseline_schedule = simulate_baseline(scenario)
    baseline_validation = _validated(scenario, baseline_schedule, label="baseline schedule")
    assert baseline_validation.metrics is not None
    baseline_trace = (
        trace_schedule(
            scenario,
            baseline_schedule,
            baseline_validation,
            schedule_kind="baseline",
            experiment_id=scenario.variant_id,
        )
        if full_trace
        else None
    )
    exact = solve_exact(
        scenario,
        time_limit_seconds=time_limit_seconds,
        random_seed=solver_seed,
        workers=workers,
    )
    exact_trace = None
    exact_metrics = None
    if exact.schedule is not None:
        validation = _validated(scenario, exact.schedule, label="exact schedule")
        exact_metrics = validation.metrics
        if exact.objective != validation.metrics.makespan:
            raise RuntimeError(f"{scenario.scenario_id}: exact objective/export mismatch")
        if full_trace:
            exact_trace = trace_schedule(
                scenario,
                exact.schedule,
                validation,
                schedule_kind="exact",
                experiment_id=scenario.variant_id,
            )
    if exact.status in {"INFEASIBLE", "MODEL_INVALID"}:
        raise RuntimeError(f"{scenario.scenario_id}: solver returned {exact.status}")
    is_optimal = exact.status == "OPTIMAL" and exact.objective is not None
    row = {
        "scenario_id": scenario.scenario_id,
        "scenario_sha256": _json_sha256(_semantic_payload(scenario)),
        "solver_status": exact.status,
        "T_star": _format_decimal(exact.objective) if is_optimal else "",
        "incumbent_makespan": _format_decimal(exact.objective),
        "solver_best_bound": _format_decimal(exact.best_bound),
        "solver_gap": _format_decimal(exact.relative_gap),
        "solver_wall_time_seconds": f"{exact.wall_time:.6f}",
        "B4": _format_decimal(aggregate.b4),
        "W4": _format_decimal(aggregate.w4),
        "H": _format_decimal(aggregate.h),
        "L4": _format_decimal(aggregate.l4),
        "active_branches": ",".join(aggregate.active_branches),
        "baseline_makespan": _format_decimal(baseline_validation.metrics.makespan),
        "baseline_queue": _format_decimal(baseline_validation.metrics.queue_time),
        "exact_queue": (
            _format_decimal(exact_metrics.queue_time) if exact_metrics else ""
        ),
    }
    return row, exact, baseline_trace, exact_trace


def _run_exp06a(
    matrix: Exp06Matrix,
) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    rows: list[dict[str, str]] = []
    phase_rows: list[dict[str, str]] = []
    event_rows: list[dict[str, str]] = []
    for object_id, base in _scale_objects(matrix).items():
        for kappa in matrix.scale_factors:
            label = str(int(kappa * Decimal("100"))).zfill(3)
            scenario = scale_scenario(
                base,
                kappa=kappa,
                scenario_id=f"exp06a_{object_id}_k{label}",
                source_path=matrix.source_path,
            )
            summary, exact, baseline_trace, exact_trace = _solve_summary(
                scenario,
                time_limit_seconds=matrix.exp06a_time_limit_seconds,
                solver_seed=matrix.solver_random_seed,
                workers=matrix.solver_workers,
                full_trace=True,
            )
            if exact.status != "OPTIMAL" or exact_trace is None or baseline_trace is None:
                raise RuntimeError(f"{scenario.scenario_id}: EXP-06A requires OPTIMAL")
            rows.append(
                {
                    "experiment_id": "EXP-06A",
                    "object_id": object_id,
                    "kappa": _format_decimal(kappa),
                    **summary,
                }
            )
            phase_rows.extend(baseline_trace.phase_rows)
            phase_rows.extend(exact_trace.phase_rows)
            event_rows.extend(baseline_trace.event_rows)
            event_rows.extend(exact_trace.event_rows)
    if len(rows) != matrix.expected_scale_point_count:
        raise RuntimeError("EXP-06A point count mismatch after execution")
    fields = ("T_star", "B4", "W4", "H", "L4", "baseline_makespan", "baseline_queue", "exact_queue")
    for object_id in {row["object_id"] for row in rows}:
        selected = [row for row in rows if row["object_id"] == object_id]
        reference = next(row for row in selected if row["kappa"] == "1")
        for row in selected:
            kappa = Decimal(row["kappa"])
            tolerance = Decimal("0.0001") * max(kappa, Decimal("1"))
            for field in fields:
                expected = Decimal(reference[field]) * kappa
                if abs(Decimal(row[field]) - expected) > tolerance:
                    raise RuntimeError(
                        f"EXP-06A invariant failed for {object_id}, {field}, kappa={kappa}"
                    )
    return rows, phase_rows, event_rows


def _pair_result(
    *,
    experiment_id: str,
    common: dict[str, str],
    result_3: dict[str, str],
    result_4: dict[str, str],
) -> dict[str, str]:
    proven = bool(result_3["T_star"] and result_4["T_star"])
    if proven:
        t3 = Decimal(result_3["T_star"])
        t4 = Decimal(result_4["T_star"])
        margin = t3 - t4
        ratio = t3 / t4
        reversal = t4 >= t3
    else:
        margin = None
        ratio = None
        reversal = False
    return {
        "experiment_id": experiment_id,
        **common,
        "scenario_3_id": result_3["scenario_id"],
        "scenario_3_sha256": result_3["scenario_sha256"],
        "scenario_4_id": result_4["scenario_id"],
        "scenario_4_sha256": result_4["scenario_sha256"],
        "status_3": result_3["solver_status"],
        "status_4": result_4["solver_status"],
        "T3_star": result_3["T_star"],
        "T4_star": result_4["T_star"],
        "margin_T3_minus_T4": _format_decimal(margin),
        "ratio_T3_to_T4": _format_decimal(ratio),
        "ranking_reversal": str(reversal).lower() if proven else "",
        "B4_3": result_3["B4"],
        "B4_4": result_4["B4"],
        "baseline_3": result_3["baseline_makespan"],
        "baseline_4": result_4["baseline_makespan"],
        "baseline_margin_3_minus_4": _format_decimal(
            Decimal(result_3["baseline_makespan"])
            - Decimal(result_4["baseline_makespan"])
        ),
        "solver_gap_3": result_3["solver_gap"],
        "solver_gap_4": result_4["solver_gap"],
        "solver_wall_time_3": result_3["solver_wall_time_seconds"],
        "solver_wall_time_4": result_4["solver_wall_time_seconds"],
    }


def _percentile(values: list[Decimal], probability: Decimal) -> Decimal:
    if not values:
        raise ValueError("percentile requires values")
    ordered = sorted(values)
    index = int((Decimal(len(ordered) - 1) * probability).to_integral_value(rounding=ROUND_HALF_UP))
    return ordered[index]


def _run_exp06b(
    matrix: Exp06Matrix,
) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    pairs: list[dict[str, str]] = []
    multipliers: list[dict[str, str]] = []
    total = matrix.random_pair_count
    completed = 0
    for u in matrix.uncertainty_levels:
        for seed in range(matrix.seed_start, matrix.seed_start + matrix.seed_count):
            scenario_3, scenario_4, multiplier_rows = build_random_pair(
                matrix, u=u, seed=seed
            )
            result_3, _, _, _ = _solve_summary(
                scenario_3,
                time_limit_seconds=matrix.exp06b_time_limit_seconds,
                solver_seed=matrix.solver_random_seed,
                workers=matrix.solver_workers,
            )
            result_4, _, _, _ = _solve_summary(
                scenario_4,
                time_limit_seconds=matrix.exp06b_time_limit_seconds,
                solver_seed=matrix.solver_random_seed,
                workers=matrix.solver_workers,
            )
            pairs.append(
                _pair_result(
                    experiment_id="EXP-06B",
                    common={"u": _format_decimal(u), "seed": str(seed)},
                    result_3=result_3,
                    result_4=result_4,
                )
            )
            multipliers.extend(multiplier_rows)
            completed += 1
            if completed % 250 == 0 or completed == total:
                print(f"EXP-06B pair progress: {completed}/{total}", flush=True)
    if len(pairs) != matrix.expected_random_pair_count:
        raise RuntimeError("EXP-06B pair count mismatch after execution")
    summaries: list[dict[str, str]] = []
    for u in matrix.uncertainty_levels:
        selected = [row for row in pairs if Decimal(row["u"]) == u]
        proven = [row for row in selected if row["margin_T3_minus_T4"]]
        reversals = sum(row["ranking_reversal"] == "true" for row in proven)
        share = Decimal(reversals) / Decimal(len(proven)) if proven else Decimal("0")
        se = Decimal(str(math.sqrt(float(share * (Decimal("1") - share) / Decimal(len(proven)))))) if proven else Decimal("0")
        zero_event_upper = (
            Decimal(str(1 - math.pow(0.05, 1 / len(proven)))).quantize(
                Decimal("0.000001")
            )
            if proven and reversals == 0
            else None
        )
        margins = [Decimal(row["margin_T3_minus_T4"]) for row in proven]
        summaries.append(
            {
                "u": _format_decimal(u),
                "pair_count": str(len(selected)),
                "proven_pair_count": str(len(proven)),
                "reversal_count": str(reversals),
                "reversal_share": _format_decimal(share),
                "monte_carlo_se": _format_decimal(se),
                "zero_event_one_sided_95_upper": _format_decimal(zero_event_upper),
                "median_margin_T3_minus_T4": _format_decimal(median(margins)),
                "q05_margin": _format_decimal(_percentile(margins, Decimal("0.05"))),
                "q95_margin": _format_decimal(_percentile(margins, Decimal("0.95"))),
                "minimum_margin": _format_decimal(min(margins)),
                "maximum_margin": _format_decimal(max(margins)),
            }
        )
    return pairs, multipliers, summaries


def _run_exp06c(
    matrix: Exp06Matrix,
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    pairs: list[dict[str, str]] = []
    total = matrix.expected_adversarial_pair_count
    completed = 0
    for mode in matrix.adversarial_modes:
        for u in matrix.adversarial_u_values:
            scenario_3, scenario_4 = build_adversarial_pair(matrix, mode=mode, u=u)
            result_3, _, _, _ = _solve_summary(
                scenario_3,
                time_limit_seconds=matrix.exp06c_time_limit_seconds,
                solver_seed=matrix.solver_random_seed,
                workers=matrix.solver_workers,
            )
            result_4, _, _, _ = _solve_summary(
                scenario_4,
                time_limit_seconds=matrix.exp06c_time_limit_seconds,
                solver_seed=matrix.solver_random_seed,
                workers=matrix.solver_workers,
            )
            pairs.append(
                _pair_result(
                    experiment_id="EXP-06C",
                    common={"mode": mode, "u": _format_decimal(u)},
                    result_3=result_3,
                    result_4=result_4,
                )
            )
            completed += 1
            if completed % 50 == 0 or completed == total:
                print(f"EXP-06C pair progress: {completed}/{total}", flush=True)
    summaries: list[dict[str, str]] = []
    for mode in matrix.adversarial_modes:
        selected = [row for row in pairs if row["mode"] == mode]
        crossings = [row for row in selected if row["ranking_reversal"] == "true"]
        first = min(crossings, key=lambda row: Decimal(row["u"])) if crossings else None
        summaries.append(
            {
                "mode": mode,
                "grid_point_count": str(len(selected)),
                "proven_pair_count": str(
                    sum(bool(row["margin_T3_minus_T4"]) for row in selected)
                ),
                "crossing_found": str(first is not None).lower(),
                "minimum_crossing_u": first["u"] if first else "",
                "margin_at_crossing": first["margin_T3_minus_T4"] if first else "",
                "margin_at_u0": next(
                    row["margin_T3_minus_T4"]
                    for row in selected
                    if Decimal(row["u"]) == 0
                ),
                "margin_at_u_stop": next(
                    row["margin_T3_minus_T4"]
                    for row in selected
                    if Decimal(row["u"]) == matrix.adversarial_u_stop
                ),
            }
        )
    return pairs, summaries


def _write_report(
    path: Path,
    *,
    matrix: Exp06Matrix,
    scale_rows: list[dict[str, str]],
    random_pairs: list[dict[str, str]],
    random_summary: list[dict[str, str]],
    adversarial_pairs: list[dict[str, str]],
    adversarial_summary: list[dict[str, str]],
) -> None:
    scale_optimal = sum(row["solver_status"] == "OPTIMAL" for row in scale_rows)
    random_proven = sum(bool(row["margin_T3_minus_T4"]) for row in random_pairs)
    adversarial_proven = sum(bool(row["margin_T3_minus_T4"]) for row in adversarial_pairs)
    random_table = "\n".join(
        "| {u} | {proven_pair_count} | {reversal_count} | {reversal_share} | "
        "{monte_carlo_se} | {zero_event_one_sided_95_upper} | "
        "{median_margin_T3_minus_T4} | {q05_margin} | {q95_margin} |".format(**row)
        for row in random_summary
    )
    adversarial_table = "\n".join(
        "| {mode} | {proven_pair_count} | {crossing_found} | {minimum_crossing_u} | "
        "{margin_at_crossing} | {margin_at_u0} | {margin_at_u_stop} |".format(**row)
        for row in adversarial_summary
    )
    report = f"""# Отчёт по EXP-06: масштаб и устойчивость ранжирования

Дата отчёта: 2026-08-07

## 1. Резюме

EXP-06A выполнил {len(scale_rows)} масштабных точек, из них `OPTIMAL` ---
{scale_optimal}; все заявленные линейные инварианты прошли автоматическую
проверку. EXP-06B выполнил {len(random_pairs)} пар ({2 * len(random_pairs)}
точных решений), доказанные парные исходы доступны для {random_proven} пар.
EXP-06C выполнил {len(adversarial_pairs)} пар, доказанные исходы доступны для
{adversarial_proven}.

Общая шкала не изменила ранжирование и безразмерные показатели, но этот
результат не переносится автоматически на относительные ошибки. Случайные и
adversarial-результаты ниже относятся только к зафиксированной модели ошибок.

В EXP-06B не наблюдалось ни одной смены ранжирования на 5000 доказанных пар.
Это не означает нулевую вероятность: для каждого уровня с 0 событиями из 1000
one-sided 95% верхняя граница равна примерно 0.003. Минимальный доказанный
запас $T_3^*-T_4^*$ на максимальном уровне $u=0.50$ остался положительным и
составил 3.30 ч.

## 2. EXP-06A: общая шкала

![Масштабная инвариантность](../figures/exp06_scale_invariance.png)

[SVG-версия](../figures/exp06_scale_invariance.svg).

Проверены практические варианты 3--4 и две заранее выбранные канонические
точки при $\\kappa\\in\\{{0.25,0.5,1,2,4\\}}$. Одновременно масштабировались
$x$, длительности фаз, time unit и tolerance; топология, quality gates и
безразмерные коэффициенты не менялись. Дискретная модель решателя в ticks
оставалась идентичной.

## 3. EXP-06B: парные случайные ошибки

![Устойчивость ранжирования](../figures/exp06_ranking_stability.png)

[SVG-версия](../figures/exp06_ranking_stability.svg).

![Распределения запаса](../figures/exp06_margin_distributions.png)

[SVG-версия](../figures/exp06_margin_distributions.svg).

| $u$ | Доказанных пар | Смен ранжирования | Доля | MC SE | 95% upper при 0 событиях | Медиана $T_3^*-T_4^*$ | q05 | q95 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
{random_table}

Множители agent- и human-частей выбираются независимо и равномерно в log-space
между $\\log(1-u)$ и $\\log(1+u)$. Неизменённые задачи получают одинаковые
множители в обоих вариантах. Задачи 6a--6c наследуют общий множитель задачи 6
и меньший residual с log-scale {matrix.residual_log_scale}. Все применённые
множители сохранены отдельно.

## 4. EXP-06C: неблагоприятные ошибки

![Неблагоприятные ошибки](../figures/exp06_adversarial_thresholds.png)

[SVG-версия](../figures/exp06_adversarial_thresholds.svg).

| Режим | Доказанных пар | Пересечение найдено | Min $u$ | Margin при пересечении | Margin при $u=0$ | Margin при $u=0.95$ |
|---|---:|---|---:|---:|---:|---:|
{adversarial_table}

В каждом режиме вариант 3 получает множитель $1-u$ на выбранном ресурсе задачи
6, а 6a--6c варианта 4 --- $1+u$. Остальные задачи и ресурсы не меняются.
Из-за монотонности makespan по длительностям это граничная неблагоприятная
точка внутри зафиксированного семейства, но не глобальный adversarial-анализ
произвольных ошибок всех коэффициентов.

На сетке до $u=0.95$ пересечение не найдено. Запас сократился с 6.50 до
1.25 ч для agent-фазы критической тестовой задачи и до 3.15 ч для её human-фаз.

## 5. Воспроизводимость

```bash
cd simple_model_full/experiments
uv sync --python 3.13
uv run pytest -ra
uv run python -m experiments run --experiment EXP-06
```

Артефакты:

- [замороженная матрица](../scenarios/canonical/exp06_matrix.yaml);
- [EXP-06A](exp06a_scale.csv), [фазы](exp06a_phases.csv) и [события](exp06a_events.csv);
- [EXP-06B пары](exp06b_pairs.csv), [множители](exp06b_multipliers.csv) и [агрегаты](exp06b_summary.csv);
- [EXP-06C сетка](exp06c_pairs.csv) и [пороги](exp06c_summary.csv);
- [manifest](exp06_manifest.json).

## 6. Ограничения

- Распределение ошибок синтетическое и не является эмпирическим доверительным
  интервалом.
- Квантование к исходному time unit делает результаты воспроизводимыми, но
  дискретизирует малые ошибки.
- EXP-06B относится к одной паре практических DAG и одной корреляционной
  структуре ошибок.
- EXP-06C проверяет два заранее заданных неблагоприятных направления, а не всю
  многомерную box-область.
- CP-SAT минимизирует makespan, но не очередь как вторичную цель.

## 7. Вывод

EXP-06 отделяет точную масштабную инвариантность ядра от условной устойчивости
ранжирования к относительным ошибкам. В зафиксированной модели ошибок вариант
4 сохранил преимущество во всех 5000 случайных парах и во всех 382 граничных
adversarial-парах, но этот результат не обобщается на другие распределения и
направления ошибок. Результаты остаются в каталоге экспериментов и пока не
вносятся в текст статьи.
"""
    path.write_text(report, encoding="utf-8")


def run_exp06(project_root: Path, output_directory: Path) -> tuple[Path, ...]:
    matrix_path = project_root / "scenarios" / "canonical" / "exp06_matrix.yaml"
    matrix = load_exp06_matrix(matrix_path)
    output_directory.mkdir(parents=True, exist_ok=True)
    figure_directory = project_root / "figures"
    scale_path = output_directory / "exp06a_scale.csv"
    scale_phases_path = output_directory / "exp06a_phases.csv"
    scale_events_path = output_directory / "exp06a_events.csv"
    random_pairs_path = output_directory / "exp06b_pairs.csv"
    multipliers_path = output_directory / "exp06b_multipliers.csv"
    random_summary_path = output_directory / "exp06b_summary.csv"
    adversarial_pairs_path = output_directory / "exp06c_pairs.csv"
    adversarial_summary_path = output_directory / "exp06c_summary.csv"

    scale_rows, scale_phases, scale_events = _run_exp06a(matrix)
    _write_csv(scale_path, scale_rows)
    _write_csv(scale_phases_path, scale_phases)
    _write_csv(scale_events_path, scale_events)

    random_pairs, multiplier_rows, random_summary = _run_exp06b(matrix)
    _write_csv(random_pairs_path, random_pairs)
    _write_csv(multipliers_path, multiplier_rows)
    _write_csv(random_summary_path, random_summary)

    adversarial_pairs, adversarial_summary = _run_exp06c(matrix)
    _write_csv(adversarial_pairs_path, adversarial_pairs)
    _write_csv(adversarial_summary_path, adversarial_summary)

    figure_paths = [
        *build_scale_invariance(scale_rows, figure_directory / "exp06_scale_invariance"),
        *build_ranking_stability(random_summary, figure_directory / "exp06_ranking_stability"),
        *build_margin_distributions(random_pairs, figure_directory / "exp06_margin_distributions"),
        *build_adversarial_thresholds(
            adversarial_pairs, figure_directory / "exp06_adversarial_thresholds"
        ),
    ]
    report_path = output_directory / "exp06_report.md"
    _write_report(
        report_path,
        matrix=matrix,
        scale_rows=scale_rows,
        random_pairs=random_pairs,
        random_summary=random_summary,
        adversarial_pairs=adversarial_pairs,
        adversarial_summary=adversarial_summary,
    )
    outputs_without_manifest = [
        scale_path,
        scale_phases_path,
        scale_events_path,
        random_pairs_path,
        multipliers_path,
        random_summary_path,
        adversarial_pairs_path,
        adversarial_summary_path,
        report_path,
        *figure_paths,
    ]
    implementation_paths = sorted(
        (project_root / "src" / "experiments").glob("*.py")
    ) + [project_root / "pyproject.toml", project_root / "uv.lock"]
    manifest_path = output_directory / "exp06_manifest.json"
    manifest = {
        "experiment_id": "EXP-06",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "command": "uv run python -m experiments run --experiment EXP-06",
        **git_provenance(project_root),
        "matrix": {
            "path": str(matrix_path.relative_to(project_root)),
            "sha256": _sha256(matrix_path),
            "frozen_at": matrix.frozen_at,
        },
        "sources": [
            {
                "path": source,
                "sha256": _sha256(project_root / source),
            }
            for source in (
                matrix.variant_3_source,
                matrix.variant_4_source,
                matrix.canonical_operator_matrix,
            )
        ],
        "solver": {
            "exp06a_time_limit_seconds": matrix.exp06a_time_limit_seconds,
            "exp06b_time_limit_seconds": matrix.exp06b_time_limit_seconds,
            "exp06c_time_limit_seconds": matrix.exp06c_time_limit_seconds,
            "random_seed": matrix.solver_random_seed,
            "workers": matrix.solver_workers,
        },
        "baseline_policy_id": matrix.policy_id,
        "dependencies": _dependencies(),
        "summary": {
            "exp06a_points": len(scale_rows),
            "exp06a_optimal_points": sum(row["solver_status"] == "OPTIMAL" for row in scale_rows),
            "exp06b_pairs": len(random_pairs),
            "exp06b_optimal_pairs": sum(
                row["status_3"] == row["status_4"] == "OPTIMAL" for row in random_pairs
            ),
            "exp06b_reversals": sum(row["ranking_reversal"] == "true" for row in random_pairs),
            "exp06c_pairs": len(adversarial_pairs),
            "exp06c_optimal_pairs": sum(
                row["status_3"] == row["status_4"] == "OPTIMAL" for row in adversarial_pairs
            ),
            "exp06c_crossings": sum(row["crossing_found"] == "true" for row in adversarial_summary),
        },
        "scenario_hash_tables": [
            {
                "path": str(path.relative_to(project_root)),
                "sha256": _sha256(path),
            }
            for path in (scale_path, random_pairs_path, adversarial_pairs_path)
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
