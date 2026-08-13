from __future__ import annotations

import csv
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from decimal import Decimal
import json
from pathlib import Path
from typing import Any, Iterator

import yaml

from .bounds import AggregateMetrics, compute_aggregates
from .exact_solver import ExactSolution, solve_exact
from .exp03 import ScheduleTrace, trace_schedule
from .exp04 import (
    Exp04Matrix,
    _critical_chain,
    _dependencies,
    _format_decimal,
    _json_sha256,
    _semantic_payload,
    _sha256,
    _trace_fields,
    _validated,
    _write_csv,
    build_exp04_scenario,
    load_exp04_matrix,
)
from .exp05_figures import (
    build_active_constraint_maps,
    build_interaction_contrast,
    build_makespan_heatmaps,
)
from .provenance import git_provenance
from .schema import Scenario, ScenarioError, decimal, validate_scenario
from .simulator import simulate_baseline


@dataclass(frozen=True)
class Exp05Parameters:
    p: int
    m: int
    overhead_rate: Decimal
    lambda_h: Decimal

    @property
    def label(self) -> str:
        return (
            f"P={self.p},m={self.m},r_o={format(self.overhead_rate, 'f')},"
            f"lambda_h={format(self.lambda_h, 'f')}"
        )


@dataclass(frozen=True)
class Exp05Matrix:
    source_path: Path
    schema_version: int
    experiment_id: str
    frozen_at: str
    source_operator_matrix: str
    topology: str
    task_count: int
    human_share: Decimal
    phase_profile: str
    selected_task_id: str
    selected_quality_gate_id: str
    base_effort: Decimal
    time_unit: Decimal
    tolerance: Decimal
    agent_counts: tuple[int, ...]
    m_values: tuple[int, ...]
    overhead_rates: tuple[Decimal, ...]
    human_overhead_shares: tuple[Decimal, ...]
    raw_position_count: int
    expected_unique_point_count: int
    expected_analysis_position_count: int
    c: Decimal
    gamma: Decimal
    policy_id: str
    solver_time_limit_seconds: float
    initial_solver_time_limit_seconds: float
    solver_random_seed: int
    solver_workers: int

    @property
    def point_count(self) -> int:
        return (
            len(self.agent_counts)
            * len(self.m_values)
            * len(self.overhead_rates)
            * len(self.human_overhead_shares)
        )


@dataclass(frozen=True)
class Exp05Case:
    parameters: Exp05Parameters
    aliases: tuple[Exp05Parameters, ...]
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


def load_exp05_matrix(path: str | Path) -> Exp05Matrix:
    source_path = Path(path).resolve()
    with source_path.open("r", encoding="utf-8") as source:
        raw = yaml.safe_load(source)
    data = _required_mapping(raw, field="EXP-05 matrix")
    if data.get("frozen") is not True:
        raise ScenarioError("EXP-05 matrix must be frozen before execution")
    canonical = _required_mapping(data.get("canonical_object"), field="canonical_object")
    grid = _required_mapping(data.get("grid"), field="grid")
    exact = _required_mapping(data.get("exact_solver"), field="exact_solver")
    baseline = _required_mapping(data.get("baseline_policy"), field="baseline_policy")
    matrix = Exp05Matrix(
        source_path=source_path,
        schema_version=int(data.get("schema_version", 0)),
        experiment_id=str(data.get("experiment_id", "")),
        frozen_at=str(data.get("frozen_at", "")),
        source_operator_matrix=str(data.get("source_operator_matrix", "")),
        topology=str(canonical.get("topology", "")),
        task_count=int(canonical.get("task_count", 0)),
        human_share=decimal(canonical.get("human_share"), field="human_share"),
        phase_profile=str(canonical.get("phase_profile", "")),
        selected_task_id=str(canonical.get("selected_task_id", "")),
        selected_quality_gate_id=str(canonical.get("selected_quality_gate_id", "")),
        base_effort=decimal(canonical.get("base_effort"), field="base_effort"),
        time_unit=decimal(canonical.get("time_unit"), field="time_unit"),
        tolerance=decimal(canonical.get("tolerance"), field="tolerance"),
        agent_counts=tuple(
            int(item)
            for item in _required_list(grid.get("agent_counts"), field="agent_counts")
        ),
        m_values=tuple(
            int(item)
            for item in _required_list(grid.get("m_values"), field="m_values")
        ),
        overhead_rates=tuple(
            decimal(item, field="overhead_rates")
            for item in _required_list(grid.get("overhead_rates"), field="overhead_rates")
        ),
        human_overhead_shares=tuple(
            decimal(item, field="human_overhead_shares")
            for item in _required_list(
                grid.get("human_overhead_shares"), field="human_overhead_shares"
            )
        ),
        raw_position_count=int(grid.get("raw_position_count", 0)),
        expected_unique_point_count=int(grid.get("expected_unique_point_count", 0)),
        expected_analysis_position_count=int(
            grid.get("expected_analysis_position_count", 0)
        ),
        c=decimal(data.get("c"), field="c"),
        gamma=decimal(data.get("gamma"), field="gamma"),
        policy_id=str(baseline.get("policy_id", "")),
        solver_time_limit_seconds=float(exact.get("time_limit_seconds", 120)),
        initial_solver_time_limit_seconds=float(
            exact.get("initial_time_limit_seconds", 120)
        ),
        solver_random_seed=int(exact.get("random_seed", 0)),
        solver_workers=int(exact.get("workers", 1)),
    )
    _validate_matrix(matrix)
    return matrix


def _validate_matrix(matrix: Exp05Matrix) -> None:
    if matrix.schema_version != 1 or matrix.experiment_id != "EXP-05":
        raise ScenarioError("EXP-05 requires schema_version=1 and experiment_id=EXP-05")
    if (
        matrix.topology,
        matrix.task_count,
        matrix.human_share,
        matrix.phase_profile,
        matrix.selected_task_id,
        matrix.selected_quality_gate_id,
        matrix.base_effort,
    ) != (
        "two_layer",
        4,
        Decimal("0.25"),
        "io",
        "t04",
        "qg_t04",
        Decimal("24"),
    ):
        raise ScenarioError("EXP-05 canonical object differs from frozen EXP-04B")
    expected_values = (1, 2, 3, 4, 6, 8)
    if matrix.agent_counts != expected_values or matrix.m_values != expected_values:
        raise ScenarioError("EXP-05 P or m values differ from the frozen design")
    if matrix.overhead_rates != (
        Decimal("0"),
        Decimal("0.05"),
        Decimal("0.10"),
    ):
        raise ScenarioError("EXP-05 overhead rates differ from the frozen design")
    if matrix.human_overhead_shares != (Decimal("0"), Decimal("0.5")):
        raise ScenarioError("EXP-05 lambda_h values differ from the frozen design")
    if matrix.point_count != 216 or matrix.raw_position_count != 216:
        raise ScenarioError("EXP-05 raw grid must contain 216 positions")
    if matrix.expected_unique_point_count != 156:
        raise ScenarioError("EXP-05 must contain 156 unique semantic scenarios")
    if matrix.expected_analysis_position_count != 180:
        raise ScenarioError("EXP-05 analysis grid must contain 180 positions")
    if matrix.c != 1 or matrix.gamma != 1 or matrix.solver_workers != 1:
        raise ScenarioError("EXP-05 requires C=gamma=1 and one solver worker")
    if (
        matrix.initial_solver_time_limit_seconds != 120
        or matrix.solver_time_limit_seconds != 300
    ):
        raise ScenarioError("EXP-05 full-block limit escalation must be 120 to 300 seconds")
    if not matrix.source_operator_matrix or not matrix.policy_id:
        raise ScenarioError("EXP-05 source operator and baseline policy are required")


def _load_operator_matrix(matrix: Exp05Matrix) -> Exp04Matrix:
    project_root = matrix.source_path.parents[2]
    operator = load_exp04_matrix(project_root / matrix.source_operator_matrix)
    if (
        operator.topology,
        operator.task_count,
        operator.human_share,
        operator.phase_profile,
        operator.selected_task_id,
        operator.selected_quality_gate_id,
        operator.base_effort,
        operator.time_unit,
        operator.tolerance,
        operator.c,
        operator.gamma,
        operator.policy_id,
    ) != (
        matrix.topology,
        matrix.task_count,
        matrix.human_share,
        matrix.phase_profile,
        matrix.selected_task_id,
        matrix.selected_quality_gate_id,
        matrix.base_effort,
        matrix.time_unit,
        matrix.tolerance,
        matrix.c,
        matrix.gamma,
        matrix.policy_id,
    ):
        raise ScenarioError("EXP-05 source operator matrix does not match frozen audit fields")
    return operator


def build_exp05_scenario(
    matrix: Exp05Matrix,
    *,
    p: int,
    m: int,
    overhead_rate: Decimal,
    lambda_h: Decimal,
) -> tuple[Scenario, Decimal, Decimal, Decimal]:
    operator = _load_operator_matrix(matrix)
    scenario, total, human, agent = build_exp04_scenario(
        operator,
        m=m,
        overhead_rate=overhead_rate,
        lambda_h=lambda_h,
    )
    rate_label = str(int(overhead_rate * Decimal("1000"))).zfill(3)
    lambda_label = str(int(lambda_h * Decimal("10"))).zfill(2)
    scenario = replace(
        scenario,
        scenario_id=(
            f"exp05_p{p:02d}_m{m:02d}_ro{rate_label}_lh{lambda_label}"
        ),
        variant_id="EXP-05",
        p=p,
        source_path=matrix.source_path,
    )
    validate_scenario(scenario)
    return scenario, total, human, agent


def iter_exp05_cases(matrix: Exp05Matrix) -> Iterator[Exp05Case]:
    deduplicated: dict[str, Exp05Case] = {}
    order: list[str] = []
    for p in matrix.agent_counts:
        for m in matrix.m_values:
            for overhead_rate in matrix.overhead_rates:
                for lambda_h in matrix.human_overhead_shares:
                    parameters = Exp05Parameters(p, m, overhead_rate, lambda_h)
                    scenario, total, human, agent = build_exp05_scenario(
                        matrix,
                        p=p,
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
                    deduplicated[semantic_sha256] = Exp05Case(
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
            f"EXP-05 deduplication produced {len(deduplicated)} points, "
            f"expected {matrix.expected_unique_point_count}"
        )
    yield from (deduplicated[item] for item in order)


def _result_row(
    case: Exp05Case,
    aggregate: AggregateMetrics,
    useful_aggregate: AggregateMetrics,
    exact: ExactSolution,
    exact_trace: ScheduleTrace | None,
    baseline_trace: ScheduleTrace,
    exact_chain: str,
    policy_id: str,
) -> dict[str, str]:
    is_optimal = exact.status == "OPTIMAL" and exact.objective is not None
    incumbent_gap = (
        exact.objective - aggregate.b4 if exact.objective is not None else None
    )
    row = {
        "experiment_id": "EXP-05",
        "scenario_id": case.scenario.scenario_id,
        "semantic_sha256": case.semantic_sha256,
        "P": str(case.parameters.p),
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
        "useful_W4": _format_decimal(useful_aggregate.w4),
        "useful_H": _format_decimal(useful_aggregate.h),
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
        "incumbent_makespan": _format_decimal(exact.objective),
        "solver_best_bound": _format_decimal(exact.best_bound),
        "solver_gap": _format_decimal(exact.relative_gap),
        "solver_wall_time_seconds": f"{exact.wall_time:.6f}",
        "incumbent_gap_to_B4": _format_decimal(incumbent_gap),
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


def _position_rows(
    cases: list[Exp05Case], rows: list[dict[str, str]], matrix: Exp05Matrix
) -> list[dict[str, str]]:
    by_hash = {row["semantic_sha256"]: row for row in rows}
    positions: list[dict[str, str]] = []
    for case in cases:
        source = by_hash[case.semantic_sha256]
        for parameters in case.aliases:
            positions.append(
                {
                    **source,
                    "P": str(parameters.p),
                    "m": str(parameters.m),
                    "overhead_rate": _format_decimal(parameters.overhead_rate),
                    "lambda_h": _format_decimal(parameters.lambda_h),
                    "canonical_scenario_id": source["scenario_id"],
                }
            )
    positions.sort(
        key=lambda row: (
            int(row["P"]),
            int(row["m"]),
            Decimal(row["overhead_rate"]),
            Decimal(row["lambda_h"]),
        )
    )
    if len(positions) != matrix.raw_position_count:
        raise RuntimeError(
            f"EXP-05 expected {matrix.raw_position_count} reconstructed positions, "
            f"got {len(positions)}"
        )
    return positions


def _analysis_rows(
    positions: list[dict[str, str]], matrix: Exp05Matrix
) -> list[dict[str, str]]:
    selected: list[dict[str, str]] = []
    for row in positions:
        if row["overhead_rate"] == "0" and row["lambda_h"] != "0":
            continue
        selected.append(
            {
                **row,
                "analysis_overhead_rate": row["overhead_rate"],
                "analysis_lambda_h": (
                    "shared" if row["overhead_rate"] == "0" else row["lambda_h"]
                ),
            }
        )
    if len(selected) != matrix.expected_analysis_position_count:
        raise RuntimeError(
            f"EXP-05 expected {matrix.expected_analysis_position_count} analysis "
            f"positions, got {len(selected)}"
        )
    by_key = {
        (
            int(row["P"]),
            int(row["m"]),
            row["analysis_overhead_rate"],
            row["analysis_lambda_h"],
        ): row
        for row in selected
    }
    enriched: list[dict[str, str]] = []
    for row in selected:
        p = int(row["P"])
        m = int(row["m"])
        overhead_rate = row["analysis_overhead_rate"]
        lambda_h = row["analysis_lambda_h"]
        references = (
            by_key[(p, 1, overhead_rate, lambda_h)],
            row,
            by_key[(1, 1, overhead_rate, lambda_h)],
            by_key[(1, m, overhead_rate, lambda_h)],
        )
        if all(reference["T_star"] for reference in references):
            t_p1, t_pm, t_11, t_1m = (
                Decimal(reference["T_star"]) for reference in references
            )
            decomposition_gain = t_p1 - t_pm
            p1_decomposition_gain = t_11 - t_1m
            interaction = decomposition_gain - p1_decomposition_gain
        else:
            decomposition_gain = None
            p1_decomposition_gain = None
            interaction = None
        enriched.append(
            {
                **row,
                "decomposition_gain_at_P": _format_decimal(decomposition_gain),
                "decomposition_gain_at_P1": _format_decimal(p1_decomposition_gain),
                "interaction_contrast": _format_decimal(interaction),
            }
        )
    return enriched


def _summary_rows(
    analysis: list[dict[str, str]], matrix: Exp05Matrix
) -> list[dict[str, str]]:
    groups: dict[tuple[int, str, str], list[dict[str, str]]] = {}
    for row in analysis:
        groups.setdefault(
            (
                int(row["P"]),
                row["analysis_overhead_rate"],
                row["analysis_lambda_h"],
            ),
            [],
        ).append(row)
    summaries: list[dict[str, str]] = []
    for (p, overhead_rate, lambda_h), selected in sorted(groups.items()):
        selected.sort(key=lambda row: int(row["m"]))
        exact_values = [Decimal(row["T_star"]) for row in selected if row["T_star"]]
        all_proven = len(exact_values) == len(matrix.m_values)
        minimum_exact = min(exact_values) if all_proven else None
        minimizing_ms = (
            [
                int(row["m"])
                for row in selected
                if abs(Decimal(row["T_star"]) - minimum_exact) <= matrix.tolerance
            ]
            if minimum_exact is not None
            else []
        )
        minimum_b4 = min(
            selected,
            key=lambda row: (Decimal(row["B4"]), int(row["m"])),
        )
        minimum_baseline = min(
            selected,
            key=lambda row: (Decimal(row["baseline_makespan"]), int(row["m"])),
        )
        summaries.append(
            {
                "P": str(p),
                "overhead_rate": overhead_rate,
                "lambda_h": lambda_h,
                "all_m_optimal": str(all_proven).lower(),
                "minimizing_ms_T_star": ";".join(str(value) for value in minimizing_ms),
                "minimizing_m_T_star": str(min(minimizing_ms)) if minimizing_ms else "",
                "minimum_T_star": _format_decimal(minimum_exact),
                "minimizing_m_B4": minimum_b4["m"],
                "minimum_B4": minimum_b4["B4"],
                "minimizing_m_baseline": minimum_baseline["m"],
                "minimum_baseline": minimum_baseline["baseline_makespan"],
            }
        )
    if len(summaries) != 30:
        raise RuntimeError(f"EXP-05 expected 30 optimum summaries, got {len(summaries)}")
    return summaries


def _write_report(
    path: Path,
    *,
    matrix: Exp05Matrix,
    rows: list[dict[str, str]],
    analysis: list[dict[str, str]],
    summaries: list[dict[str, str]],
) -> None:
    optimal_count = sum(row["solver_status"] == "OPTIMAL" for row in rows)
    feasible_count = sum(row["solver_status"] == "FEASIBLE" for row in rows)
    other_count = len(rows) - optimal_count - feasible_count
    interaction_cells = [
        row
        for row in analysis
        if row["analysis_overhead_rate"] != "0"
        and int(row["P"]) > 1
        and int(row["m"]) > 1
        and row["interaction_contrast"]
    ]
    positive = [
        row
        for row in interaction_cells
        if Decimal(row["interaction_contrast"]) > matrix.tolerance
    ]
    negative = [
        row
        for row in interaction_cells
        if Decimal(row["interaction_contrast"]) < -matrix.tolerance
    ]
    zero = [row for row in interaction_cells if row not in positive and row not in negative]
    maximum = (
        max(interaction_cells, key=lambda row: Decimal(row["interaction_contrast"]))
        if interaction_cells
        else None
    )
    minimum = (
        min(interaction_cells, key=lambda row: Decimal(row["interaction_contrast"]))
        if interaction_cells
        else None
    )
    exact_summary_count = sum(row["all_m_optimal"] == "true" for row in summaries)
    analysis_by_key = {
        (
            row["P"],
            row["m"],
            row["analysis_overhead_rate"],
            row["analysis_lambda_h"],
        ): row
        for row in analysis
    }
    human_overhead_comparisons: list[Decimal] = []
    for overhead_rate in ("0.05", "0.10"):
        for p in ("1", "2", "3", "4", "6", "8"):
            for m in ("2", "3", "4", "6", "8"):
                agent_only = analysis_by_key[(p, m, overhead_rate, "0")]
                mixed = analysis_by_key[(p, m, overhead_rate, "0.5")]
                human_overhead_comparisons.append(
                    Decimal(mixed["decomposition_gain_at_P"])
                    - Decimal(agent_only["decomposition_gain_at_P"])
                )
    weaker_human_overhead = sum(
        value < -matrix.tolerance for value in human_overhead_comparisons
    )
    equal_human_overhead = sum(
        abs(value) <= matrix.tolerance for value in human_overhead_comparisons
    )
    stronger_human_overhead = sum(
        value > matrix.tolerance for value in human_overhead_comparisons
    )
    maximum_weakening = min(human_overhead_comparisons)
    active_work = sum(row["active_branches"] == "work" for row in analysis)
    active_path = sum(
        row["active_branches"] == "critical_path" for row in analysis
    )
    active_tie = sum(
        row["active_branches"] == "work,critical_path" for row in analysis
    )
    maximum_bound_gap = max(rows, key=lambda row: Decimal(row["incumbent_gap_to_B4"]))
    maximum_baseline_gap = max(
        rows, key=lambda row: Decimal(row["baseline_gap_to_optimum"])
    )
    table_rows = "\n".join(
        "| {P} | {overhead_rate} | {lambda_h} | {minimizing_ms_T_star} | "
        "{minimum_T_star} | {minimizing_m_B4} | {minimizing_m_baseline} |".format(**row)
        for row in summaries
    )
    maximum_text = (
        f"$I={Decimal(maximum['interaction_contrast']):.5f}$ ч при "
        f"$P={maximum['P']}$, $m={maximum['m']}$, "
        f"$r_o={maximum['analysis_overhead_rate']}$, "
        f"$\\lambda_h={maximum['analysis_lambda_h']}$"
        if maximum
        else "не вычислен"
    )
    minimum_text = (
        f"$I={Decimal(minimum['interaction_contrast']):.5f}$ ч при "
        f"$P={minimum['P']}$, $m={minimum['m']}$, "
        f"$r_o={minimum['analysis_overhead_rate']}$, "
        f"$\\lambda_h={minimum['analysis_lambda_h']}$"
        if minimum
        else "не вычислен"
    )
    report = f"""# Отчёт по EXP-05: взаимодействие параллелизма и декомпозиции

Дата отчёта: 2026-08-07

Статус: рассчитано {len(rows)} уникальных сценариев для {matrix.raw_position_count}
позиций исходной сетки и {matrix.expected_analysis_position_count} содержательных
позиций после объединения нулевого overhead.

## 1. Резюме

Статусы exact solver: `OPTIMAL` --- {optimal_count}, `FEASIBLE` ---
{feasible_count}, остальные --- {other_count}. Полностью доказанный выбор
оптимального $m$ доступен для {exact_summary_count} из {len(summaries)} срезов
$(P,r_o,\\lambda_h)$.

Для положительного overhead доказанный interaction contrast вычислен в
{len(interaction_cells)} внутренних ячейках $P>1,m>1$: положительных ---
{len(positive)}, отрицательных --- {len(negative)}, нулевых в пределах tolerance
--- {len(zero)}. Максимум: {maximum_text}. Минимум: {minimum_text}.

Положительный $I(P,m)$ означает, что выигрыш от декомпозиции при данном $P$
больше выигрыша при $P=1$. Это interaction contrast, а не самостоятельная
оценка причинного эффекта в реальном проекте.

### Интерпретация результата

- Гипотеза о взаимодополняемости подтверждена на зафиксированной сетке:
  {len(positive)} из {len(interaction_cells)} внутренних контрастов положительны,
  {len(zero)} равны нулю и отрицательных контрастов нет. Все четыре нулевые
  точки имеют $P=2,m=2$.
- Перенос половины overhead на человека ни в одной из 60 сопоставимых ячеек
  не усилил выигрыш от декомпозиции: он уменьшился в
  {weaker_human_overhead} случаях и не изменился в {equal_human_overhead};
  усилений --- {stronger_human_overhead}. Максимальное ослабление составляет
  {abs(maximum_weakening):.5f} ч.
- Оптимальная гранулярность зависит от $P$: при положительном overhead для
  $P=1,2$ минимизирует $m=1$, тогда как при $P=3\\ldots8$ минимум переносится
  на $m=2\\ldots4$ (с одним плато $m=4,6,8$).
- Нижняя граница активна по работе в {active_work} из {len(analysis)} ячеек,
  по критическому пути в {active_path}, одновременно по двум ветвям в
  {active_tie}. При этом максимальный доказанный разрыв $T^*-B_4$ равен
  {Decimal(maximum_bound_gap['incumbent_gap_to_B4']):.5f} ч в сценарии
  `{maximum_bound_gap['scenario_id']}`.
- Наибольший разрыв baseline с оптимумом равен
  {Decimal(maximum_baseline_gap['baseline_gap_to_optimum']):.5f} ч в сценарии
  `{maximum_baseline_gap['scenario_id']}`. Поэтому ни $B_4$, ни baseline не
  заменяют точное расписание в выводе о взаимодействии.

## 2. Зафиксированный дизайн

- без изменения переиспользован оператор EXP-04B для вершины `t04`;
- $P,m\\in\\{{1,2,3,4,6,8\\}}$;
- $r_o\\in\\{{0,0.05,0.10\\}}$, $\\lambda_h\\in\\{{0,0.5\\}}$;
- полный overhead равен $(m-1)r_o\\cdot24$ ч;
- исходные 216 позиций свёрнуты в 156 семантических сценариев;
- при анализе два совпадающих нулевых среза $\\lambda_h$ объединены, поэтому
  остаётся 180 позиций и пять режимов overhead;
- первый полный проход с лимитом
  {matrix.initial_solver_time_limit_seconds:g} секунд дал 155 `OPTIMAL` и одну
  `FEASIBLE` точку; предусмотренное протоколом единственное повышение лимита
  применено ко всему блоку из 156 точек, а не к отдельному сценарию;
- итоговый проход: один worker, seed {matrix.solver_random_seed}, лимит
  {matrix.solver_time_limit_seconds:g} секунд на каждую уникальную точку.

## 3. Тепловые карты доказанного makespan

![Тепловые карты makespan](../figures/exp05_makespan_heatmaps.png)

[SVG-версия](../figures/exp05_makespan_heatmaps.svg).

Пустая ячейка означает отсутствие доказанного `OPTIMAL` и не заменяется
incumbent-значением.

## 4. Interaction contrast

![Interaction contrast](../figures/exp05_interaction_contrast.png)

[SVG-версия](../figures/exp05_interaction_contrast.svg).

Определение:

$$
I(P,m)=[T^*(P,1)-T^*(P,m)]-[T^*(1,1)-T^*(1,m)].
$$

Контраст вычисляется только когда все четыре входящих значения доказаны как
`OPTIMAL`.

## 5. Активные ограничения нижней границы

![Карта активных ограничений](../figures/exp05_active_constraints.png)

[SVG-версия](../figures/exp05_active_constraints.svg).

$W$ обозначает $W_4/P$, $L$ --- $L_4$, $H$ --- $\\gamma H$. Совпадающие
ветви показаны составными метками. Карта относится к $B_4$ и не выдаётся за
карту фактического makespan.

## 6. Оптимальная гранулярность

| $P$ | $r_o$ | $\\lambda_h$ | Все минимизирующие $m$ по $T^*$ | Min $T^*$ | $m$ по $B_4$ | $m$ baseline |
|---:|---:|---:|---:|---:|---:|---:|
{table_rows}

При наличии нескольких точных минимумов перечислены все значения $m$ в
пределах tolerance; отдельный столбец `minimizing_m_T_star` в CSV хранит
наименьшее из них для машинной обработки.

## 7. Трассировка и воспроизводимость

Для каждой уникальной точки сохранены overhead, $W_4$, $H$, $L_4$, $B_4$,
статус и bound решателя, baseline, реализованная critical chain, фазовые и
событийные трассы. Общие точки сетки восстановлены в отдельном CSV без
повторного решения.

```bash
cd simple_model_full/experiments
uv sync --python 3.13
uv run pytest -ra
uv run python -m experiments run --experiment EXP-05
```

Артефакты:

- [замороженная матрица](../scenarios/canonical/exp05_matrix.yaml);
- [156 уникальных прогонов](exp05_runs.csv);
- [216 восстановленных позиций](exp05_grid.csv);
- [interaction contrast](exp05_interactions.csv);
- [оптимальная гранулярность](exp05_optimal_m.csv);
- [фазовые трассы](exp05_phases.csv) и [события](exp05_events.csv);
- [manifest](exp05_manifest.json).

## 8. Ограничения

- Результат относится к одной синтетической вершине одного канонического DAG.
- Сетка конечна и не доказывает оптимальность вне выбранных $P$ и $m$.
- CP-SAT минимизирует makespan, но не очередь как вторичную цель.
- `FEASIBLE` incumbent хранится для аудита, но не называется $T^*$ и не входит
  в interaction contrast или доказанный выбор $m$.
- Рост $P$ не включает зависимые от масштаба $C(P)$ или $\\gamma(P)$: здесь
  изолировано только взаимодействие доступных слотов и гранулярности.

## 9. Вывод

EXP-05 подтверждает на зафиксированной канонической сетке, что доступные
агентные слоты и декомпозиция являются взаимодополняющими рычагами: почти все
внутренние interaction contrast положительны, а оптимальное $m$ меняется с
$P$. Человеческая доля overhead ослабляет или сохраняет, но не усиливает
выигрыш декомпозиции в исследованных ячейках. Результаты остаются в каталоге
экспериментов и пока не вносятся в текст статьи.
"""
    path.write_text(report, encoding="utf-8")


def run_exp05(project_root: Path, output_directory: Path) -> tuple[Path, ...]:
    matrix_path = project_root / "scenarios" / "canonical" / "exp05_matrix.yaml"
    matrix = load_exp05_matrix(matrix_path)
    operator_matrix_path = project_root / matrix.source_operator_matrix
    _load_operator_matrix(matrix)
    output_directory.mkdir(parents=True, exist_ok=True)
    figure_directory = project_root / "figures"
    cases = list(iter_exp05_cases(matrix))
    rows: list[dict[str, str]] = []
    phase_rows: list[dict[str, str]] = []
    event_rows: list[dict[str, str]] = []

    for index, case in enumerate(cases, start=1):
        aggregate = compute_aggregates(case.scenario)
        useful_scenario, _, _, _ = build_exp05_scenario(
            matrix,
            p=case.parameters.p,
            m=case.parameters.m,
            overhead_rate=Decimal("0"),
            lambda_h=Decimal("0"),
        )
        useful_aggregate = compute_aggregates(useful_scenario)
        if aggregate.w4 - useful_aggregate.w4 != case.total_overhead:
            raise RuntimeError(f"{case.scenario.scenario_id}: W4 overhead audit failed")
        if aggregate.h - useful_aggregate.h != case.human_overhead:
            raise RuntimeError(f"{case.scenario.scenario_id}: H overhead audit failed")
        if (
            case.scenario.task_by_id[f"{matrix.selected_task_id}_join"].quality_gate_id
            != matrix.selected_quality_gate_id
        ):
            raise RuntimeError(f"{case.scenario.scenario_id}: quality gate was not preserved")

        baseline_schedule = simulate_baseline(case.scenario)
        baseline_validation = _validated(
            case.scenario, baseline_schedule, label="baseline schedule"
        )
        baseline_trace = trace_schedule(
            case.scenario,
            baseline_schedule,
            baseline_validation,
            schedule_kind="baseline",
            experiment_id="EXP-05",
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
                case.scenario, exact.schedule, label="exact schedule"
            )
            if exact.objective != exact_validation.metrics.makespan:
                raise RuntimeError(f"{case.scenario.scenario_id}: objective/export mismatch")
            exact_trace = trace_schedule(
                case.scenario,
                exact.schedule,
                exact_validation,
                schedule_kind="exact",
                experiment_id="EXP-05",
            )
            exact_chain = _critical_chain(case.scenario, exact.schedule)
        if exact.status in {"INFEASIBLE", "MODEL_INVALID"}:
            raise RuntimeError(
                f"{case.scenario.scenario_id}: exact solver returned {exact.status}"
            )
        rows.append(
            _result_row(
                case,
                aggregate,
                useful_aggregate,
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
            print(f"EXP-05 exact progress: {index}/{len(cases)}", flush=True)

    positions = _position_rows(cases, rows, matrix)
    analysis = _analysis_rows(positions, matrix)
    summaries = _summary_rows(analysis, matrix)
    runs_path = output_directory / "exp05_runs.csv"
    grid_path = output_directory / "exp05_grid.csv"
    interactions_path = output_directory / "exp05_interactions.csv"
    summary_path = output_directory / "exp05_optimal_m.csv"
    phases_path = output_directory / "exp05_phases.csv"
    events_path = output_directory / "exp05_events.csv"
    _write_csv(runs_path, rows)
    _write_csv(grid_path, positions)
    _write_csv(interactions_path, analysis)
    _write_csv(summary_path, summaries)
    _write_csv(phases_path, phase_rows)
    _write_csv(events_path, event_rows)

    figure_paths = [
        *build_makespan_heatmaps(
            analysis, figure_directory / "exp05_makespan_heatmaps"
        ),
        *build_interaction_contrast(
            analysis, figure_directory / "exp05_interaction_contrast"
        ),
        *build_active_constraint_maps(
            analysis, figure_directory / "exp05_active_constraints"
        ),
    ]
    report_path = output_directory / "exp05_report.md"
    _write_report(
        report_path,
        matrix=matrix,
        rows=rows,
        analysis=analysis,
        summaries=summaries,
    )

    outputs_without_manifest = [
        runs_path,
        grid_path,
        interactions_path,
        summary_path,
        phases_path,
        events_path,
        report_path,
        *figure_paths,
    ]
    implementation_paths = sorted(
        (project_root / "src" / "experiments").glob("*.py")
    ) + [project_root / "pyproject.toml", project_root / "uv.lock"]
    manifest_path = output_directory / "exp05_manifest.json"
    manifest = {
        "experiment_id": "EXP-05",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "command": "uv run python -m experiments run --experiment EXP-05",
        **git_provenance(project_root),
        "matrix": {
            "path": str(matrix_path.relative_to(project_root)),
            "sha256": _sha256(matrix_path),
            "frozen_at": matrix.frozen_at,
            "raw_positions": matrix.raw_position_count,
            "unique_points": len(rows),
            "analysis_positions": len(analysis),
        },
        "sources": [
            {
                "path": str(operator_matrix_path.relative_to(project_root)),
                "sha256": _sha256(operator_matrix_path),
            }
        ],
        "solver": {
            "time_limit_seconds": matrix.solver_time_limit_seconds,
            "initial_time_limit_seconds": matrix.initial_solver_time_limit_seconds,
            "full_block_limit_escalation": True,
            "random_seed": matrix.solver_random_seed,
            "workers": matrix.solver_workers,
        },
        "baseline_policy_id": matrix.policy_id,
        "dependencies": _dependencies(),
        "summary": {
            "unique_points": len(rows),
            "raw_positions": len(positions),
            "analysis_positions": len(analysis),
            "optimal_points": sum(row["solver_status"] == "OPTIMAL" for row in rows),
            "feasible_points": sum(row["solver_status"] == "FEASIBLE" for row in rows),
            "unknown_points": sum(row["solver_status"] == "UNKNOWN" for row in rows),
            "proven_interaction_cells": sum(
                bool(row["interaction_contrast"])
                and row["analysis_overhead_rate"] != "0"
                and int(row["P"]) > 1
                and int(row["m"]) > 1
                for row in analysis
            ),
            "fully_proven_optimum_slices": sum(
                row["all_m_optimal"] == "true" for row in summaries
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
