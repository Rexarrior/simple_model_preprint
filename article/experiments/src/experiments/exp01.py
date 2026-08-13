from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
import hashlib
import importlib.metadata
import json
from pathlib import Path
from statistics import median
from typing import Any

from .bounds import AggregateMetrics, compute_aggregates
from .exact_solver import ExactSolution, solve_exact
from .exp01_figures import build_counterexample_gantt, build_exp01_gap_figure
from .generators import Exp01Case, Exp01Matrix, iter_exp01_cases, load_exp01_matrix
from .provenance import git_provenance
from .schema import Scenario, ScheduleSpec
from .simulator import simulate_baseline
from .validator import ScheduleValidation, validate_schedule


@dataclass(frozen=True)
class _Counterexample:
    case: Exp01Case
    aggregate: AggregateMetrics
    exact: ExactSolution
    exact_validation: ScheduleValidation
    baseline_schedule: ScheduleSpec
    baseline_validation: ScheduleValidation


def _format_decimal(value: Decimal | None) -> str:
    return "" if value is None else format(value, "f")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _json_sha256(payload: object) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


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


def _schedule_payload(schedule: ScheduleSpec) -> dict[str, Any]:
    return {
        "schedule_id": schedule.schedule_id,
        "assignments": [
            {
                "task_id": item.task_id,
                "agent": item.agent,
                "assigned_at": _format_decimal(item.assigned_at),
            }
            for item in schedule.assignments
        ],
        "phases": [
            {
                "task_id": item.task_id,
                "phase_id": item.phase_id,
                "agent": item.agent,
                "start": _format_decimal(item.start),
                "end": _format_decimal(item.end),
            }
            for item in schedule.phases
        ],
    }


def _validated(schedule: ScheduleSpec, scenario: Scenario, *, label: str) -> ScheduleValidation:
    validation = validate_schedule(scenario, schedule)
    if not validation.valid or validation.metrics is None:
        details = "; ".join(issue.message for issue in validation.issues)
        raise RuntimeError(f"{scenario.scenario_id}: invalid {label}: {details}")
    return validation


def _row_for_case(
    case: Exp01Case,
    aggregate: AggregateMetrics,
    baseline_validation: ScheduleValidation,
    exact: ExactSolution,
    exact_validation: ScheduleValidation,
) -> dict[str, str]:
    assert baseline_validation.metrics is not None
    assert exact_validation.metrics is not None
    assert exact.objective is not None
    tightness_gap = exact.objective - aggregate.b4
    baseline_gap = baseline_validation.metrics.makespan - exact.objective
    scenario_payload = _scenario_payload(case.scenario)
    return {
        "experiment_id": "EXP-01",
        "scenario_id": case.scenario.scenario_id,
        "scenario_sha256": _json_sha256(scenario_payload),
        "topology": case.topology,
        "task_count": str(case.task_count),
        "agent_count": str(case.agent_count),
        "human_share": _format_decimal(case.human_share),
        "phase_profile": case.phase_profile,
        "time_unit": _format_decimal(case.scenario.time_unit),
        "T_h": _format_decimal(aggregate.t_h),
        "A": _format_decimal(aggregate.a),
        "H": _format_decimal(aggregate.h),
        "W4": _format_decimal(aggregate.w4),
        "L4": _format_decimal(aggregate.l4),
        "W4_over_P": _format_decimal(aggregate.work_branch),
        "gamma_H": _format_decimal(aggregate.human_branch),
        "B4": _format_decimal(aggregate.b4),
        "active_branches": ",".join(aggregate.active_branches),
        "critical_path": "->".join(aggregate.critical_path_l4),
        "baseline_makespan": _format_decimal(baseline_validation.metrics.makespan),
        "baseline_queue": _format_decimal(baseline_validation.metrics.queue_time),
        "baseline_blocked_any": _format_decimal(
            baseline_validation.metrics.blocked_any_time
        ),
        "baseline_gap_to_optimum": _format_decimal(baseline_gap),
        "baseline_relative_gap": _format_decimal(
            baseline_gap / exact.objective if exact.objective else Decimal("0")
        ),
        "solver_status": exact.status,
        "solver_objective": _format_decimal(exact.objective),
        "solver_best_bound": _format_decimal(exact.best_bound),
        "solver_gap": _format_decimal(exact.relative_gap),
        "solver_wall_time_seconds": f"{exact.wall_time:.6f}",
        "exact_queue": _format_decimal(exact_validation.metrics.queue_time),
        "exact_blocked_any": _format_decimal(exact_validation.metrics.blocked_any_time),
        "tightness_gap": _format_decimal(tightness_gap),
        "tightness_relative_gap": _format_decimal(
            tightness_gap / aggregate.b4 if aggregate.b4 else Decimal("0")
        ),
    }


def _counterexample_key(item: _Counterexample) -> tuple[int, Decimal, str]:
    return (
        item.case.task_count,
        item.aggregate.w4,
        item.case.scenario.scenario_id,
    )


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


def _paired_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    grouped: dict[tuple[str, str, str, str], dict[str, dict[str, str]]] = {}
    for row in rows:
        if row["phase_profile"] == "io":
            continue
        key = (
            row["topology"],
            row["task_count"],
            row["agent_count"],
            row["human_share"],
        )
        grouped.setdefault(key, {})[row["phase_profile"]] = row

    paired: list[dict[str, str]] = []
    for key, profiles in sorted(grouped.items()):
        sync = profiles["alternating_sync"]
        staggered = profiles["alternating_staggered"]
        for invariant in ("A", "H", "W4", "L4", "B4"):
            if Decimal(sync[invariant]) != Decimal(staggered[invariant]):
                raise RuntimeError(f"paired invariant {invariant} differs for {key}")
        sync_tightness = Decimal(sync["tightness_relative_gap"])
        staggered_tightness = Decimal(staggered["tightness_relative_gap"])
        sync_objective = Decimal(sync["solver_objective"])
        staggered_objective = Decimal(staggered["solver_objective"])
        paired.append(
            {
                "topology": key[0],
                "task_count": key[1],
                "agent_count": key[2],
                "human_share": key[3],
                "A": sync["A"],
                "H": sync["H"],
                "W4": sync["W4"],
                "L4": sync["L4"],
                "B4": sync["B4"],
                "sync_T_star": sync["solver_objective"],
                "staggered_T_star": staggered["solver_objective"],
                "delta_T_star_sync_minus_staggered": _format_decimal(
                    sync_objective - staggered_objective
                ),
                "sync_tightness_relative_gap": sync["tightness_relative_gap"],
                "staggered_tightness_relative_gap": staggered[
                    "tightness_relative_gap"
                ],
                "delta_tightness_sync_minus_staggered": _format_decimal(
                    sync_tightness - staggered_tightness
                ),
                "sync_baseline_relative_gap": sync["baseline_relative_gap"],
                "staggered_baseline_relative_gap": staggered[
                    "baseline_relative_gap"
                ],
            }
        )
    return paired


def _profile_summary(rows: list[dict[str, str]], tolerance: Decimal) -> list[dict[str, Any]]:
    summaries: list[dict[str, Any]] = []
    for profile in ("io", "alternating_sync", "alternating_staggered"):
        selected = [row for row in rows if row["phase_profile"] == profile]
        tightness = [Decimal(row["tightness_relative_gap"]) for row in selected]
        heuristic = [Decimal(row["baseline_relative_gap"]) for row in selected]
        summaries.append(
            {
                "profile": profile,
                "points": len(selected),
                "counterexamples": sum(
                    Decimal(row["tightness_gap"]) > tolerance for row in selected
                ),
                "median_tightness": median(tightness),
                "max_tightness": max(tightness),
                "median_heuristic": median(heuristic),
                "max_heuristic": max(heuristic),
            }
        )
    return summaries


def _percent(value: Decimal) -> str:
    return f"{value * Decimal(100):.3f}"


def _write_report(
    path: Path,
    *,
    matrix: Exp01Matrix,
    rows: list[dict[str, str]],
    paired: list[dict[str, str]],
    minimal: _Counterexample | None,
    figure_paths: tuple[Path, ...],
) -> None:
    counterexample_rows = [
        row for row in rows if Decimal(row["tightness_gap"]) > matrix.tolerance
    ]
    maximum = max(
        rows,
        key=lambda row: (Decimal(row["tightness_relative_gap"]), row["scenario_id"]),
    )
    summaries = _profile_summary(rows, matrix.tolerance)
    positive_delta = sum(
        Decimal(row["delta_tightness_sync_minus_staggered"]) > matrix.tolerance
        for row in paired
    )
    negative_delta = sum(
        Decimal(row["delta_tightness_sync_minus_staggered"]) < -matrix.tolerance
        for row in paired
    )
    equal_delta = len(paired) - positive_delta - negative_delta
    chain_rows = [row for row in rows if row["topology"] == "chain"]
    other_rows = [row for row in rows if row["topology"] != "chain"]
    chain_attained = sum(
        Decimal(row["tightness_gap"]) <= matrix.tolerance for row in chain_rows
    )
    other_attained = sum(
        Decimal(row["tightness_gap"]) <= matrix.tolerance for row in other_rows
    )
    task_count_label = ",".join(str(value) for value in matrix.task_counts)

    summary_lines = "\n".join(
        "| {profile} | {points} | {counterexamples} | {median} | {maximum} | {heuristic} |".format(
            profile=item["profile"],
            points=item["points"],
            counterexamples=item["counterexamples"],
            median=_percent(item["median_tightness"]),
            maximum=_percent(item["max_tightness"]),
            heuristic=_percent(item["median_heuristic"]),
        )
        for item in summaries
    )
    counterexample_section = ""
    if minimal is not None:
        assert minimal.exact.objective is not None
        assert minimal.exact_validation.metrics is not None
        minimal_gap = minimal.exact.objective - minimal.aggregate.b4
        counterexample_section = rf"""
## 5. Выбранный контрпример

По заранее зафиксированному порядку `(task_count, total_work, scenario_id)`
для иллюстрации выбран `{minimal.case.scenario.scenario_id}`:

- топология: `{minimal.case.topology}`;
- $N={minimal.case.task_count}$, $P={minimal.case.agent_count}$,
  $r_h={minimal.case.human_share}$;
- профиль: `{minimal.case.phase_profile}`;
- $B_4={minimal.aggregate.b4}$ ч;
- $T^*={minimal.exact.objective}$ ч;
- абсолютный разрыв: {minimal_gap} ч;
- относительный разрыв: {_percent(minimal_gap / minimal.aggregate.b4)}%;
- очередь точного расписания: {minimal.exact_validation.metrics.queue_time} агент-часа.

![Выбранный контрпример EXP-01](../figures/exp01_counterexample_gantt.png)

[SVG-версия](../figures/exp01_counterexample_gantt.svg) и
[машиночитаемое расписание](exp01_counterexample.json).

Пунктирная линия отмечает $B_4$. Разница между ней и фактическим завершением
возникает из-за ресурсного порядка повторных human-фаз и удержания агентных
слотов во время ожиданий. Это дополнительная ресурсная критическая цепочка,
которой нет в трёх агрегатных ветвях $B_4$.
"""

    report = rf"""# Отчёт по EXP-01: точность $B_4$ и роль очереди

Дата отчёта: 2026-08-07

Статус: полная замороженная матрица, {len(rows)} точек.

## 1. Резюме

Все {len(rows)} точек решены CP-SAT до статуса `OPTIMAL`. Контрпримеры с
$T^*>B_4$ найдены в {len(counterexample_rows)} точках. Максимальный
относительный разрыв равен {_percent(Decimal(maximum['tightness_relative_gap']))}%
в сценарии `{maximum['scenario_id']}`.

Эксперимент подтверждает, что $B_4$ является структурной нижней границей, но не
универсально достижимым сроком: повторные запросы к единому человеческому
ресурсу создают ресурсные цепочки и блокируют агентные слоты. Одновременно gap
baseline остаётся отдельной величиной и не должен смешиваться с разрывом
$T^*-B_4$.

## 2. Зафиксированная матрица

- топологии: chain, independent, fork--join, diamond, two-layer;
- $N\in\{{{task_count_label}\}}$;
- $P\in\{{2,4\}}$;
- $r_h\in\{{0.10,0.25,0.50\}}$;
- профили: IO, alternating-sync, alternating-staggered;
- $C=\gamma=1$;
- {len(rows)} точек, random seed 0, один worker, лимит 60 секунд на точку.

Исходная матрица содержала 270 точек с $N\in\{{4,8,12\}}$. После 76
доказанных точек первый сценарий
`exp01_independent_n8_p2_rh25_alternating_sync` завершился со статусом
`FEASIBLE` на общем 60-секундном лимите. По заранее объявленному правилу размер
был уменьшен глобально до $N=4$; индивидуальный лимит не увеличивался. Исходная
матрица и запись остановки сохранены как pilot-артефакты.

Веса задач повторяют цикл 6, 12, 18 и 24 часа. Sync и staggered имеют одинаковые
DAG, $A$, $H$, $W_4$, $L_4$ и четыре human-запроса на задачу. Отличаются только
длительности трёх agent-сегментов: равные доли против циклической перестановки
долей $1/6$, $2/6$, $3/6$.

## 3. Основные результаты

| Профиль | Точек | $T^*>B_4$ | Медианный tightness gap, % | Максимальный gap, % | Медианный gap baseline, % |
|---|---:|---:|---:|---:|---:|
{summary_lines}

Граница достигнута в {chain_attained} из {len(chain_rows)} цепочечных точек и
в {other_attained} из {len(other_rows)} точек остальных топологий. Это позволяет
проверить гипотезу о большей достижимости $B_4$ на цепочках без подбора матрицы
после просмотра результатов.

## 4. Tightness gap и эвристический gap

![Разрывы EXP-01](../figures/exp01_gaps.png)

[SVG-версия](../figures/exp01_gaps.svg).

Левая панель показывает $100(T^*/B_4-1)$ — свойство границы и экземпляра.
Правая панель показывает $100(T(\pi_{{base}})/T^*-1)$ — потерю конкретной
политики планирования. Нулевая точка слева не означает оптимальности baseline,
а большой gap baseline не доказывает неточность $B_4$.

В {len(paired)} контролируемых парах sync/staggered синхронный профиль дал
больший tightness gap в {positive_delta} случаях, меньший — в {negative_delta},
одинаковый — в {equal_delta}. Полные парные результаты сохранены отдельно и
не агрегируются с IO, где другое число human-запросов.
{counterexample_section}
## 6. Воспроизводимость

```bash
cd simple_model_full/experiments
uv sync --python 3.13
uv run pytest -ra
uv run python -m experiments run --experiment EXP-01
```

Артефакты:

- [замороженная матрица](../scenarios/canonical/exp01_matrix.yaml);
- [исходная pilot-матрица на 270 точек](../scenarios/canonical/exp01_matrix_270_pilot.yaml);
- [запись срабатывания лимита](../scenarios/canonical/exp01_pilot_limit.json);
- [все {len(rows)} точных прогонов](exp01_runs.csv);
- [{len(paired)} пар sync/staggered](exp01_profile_pairs.csv);
- [выбранный контрпример](exp01_counterexample.json);
- [manifest](exp01_manifest.json).

## 7. Ограничения

- Веса и человеческие доли синтетические и не являются оценками реальной
  команды.
- Рассматриваются детерминированные длительности, один человек и локальная
  блокировка без переиспользования занятого слота.
- Использован один цикл весов и по одному детерминированному DAG каждого типа.
- Результат показывает существование и частоту разрыва на заявленной матрице,
  но не задаёт распределение эффекта на случайных графах.

## 8. Вывод

EXP-01 отделяет два механизма: недостижимость структурной границы из-за
ресурсной критической цепочки и потерю выбранной эвристики относительно
доказанного оптимума. Результаты пока остаются в каталоге экспериментов и в
текст статьи не вносятся.
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


def run_exp01(project_root: Path, output_directory: Path) -> tuple[Path, ...]:
    matrix_path = project_root / "scenarios" / "canonical" / "exp01_matrix.yaml"
    matrix = load_exp01_matrix(matrix_path)
    pilot_matrix_path = (
        project_root / "scenarios" / "canonical" / "exp01_matrix_270_pilot.yaml"
    )
    pilot_limit_path = (
        project_root / "scenarios" / "canonical" / "exp01_pilot_limit.json"
    )
    output_directory.mkdir(parents=True, exist_ok=True)
    figure_directory = project_root / "figures"
    cases = list(iter_exp01_cases(matrix))
    rows: list[dict[str, str]] = []
    counterexamples: list[_Counterexample] = []

    for index, case in enumerate(cases, start=1):
        aggregate = compute_aggregates(case.scenario)
        baseline_schedule = simulate_baseline(case.scenario)
        baseline_validation = _validated(
            baseline_schedule,
            case.scenario,
            label="baseline schedule",
        )
        exact = solve_exact(
            case.scenario,
            time_limit_seconds=matrix.solver_time_limit_seconds,
            random_seed=matrix.solver_random_seed,
            workers=matrix.solver_workers,
        )
        if exact.status != "OPTIMAL" or exact.objective is None or exact.schedule is None:
            raise RuntimeError(
                f"{case.scenario.scenario_id}: exact solver returned {exact.status}"
            )
        exact_validation = _validated(exact.schedule, case.scenario, label="exact schedule")
        if exact_validation.metrics is None or exact_validation.metrics.makespan != exact.objective:
            raise RuntimeError(f"{case.scenario.scenario_id}: objective/export mismatch")
        rows.append(
            _row_for_case(
                case,
                aggregate,
                baseline_validation,
                exact,
                exact_validation,
            )
        )
        if exact.objective > aggregate.b4 + matrix.tolerance:
            counterexamples.append(
                _Counterexample(
                    case=case,
                    aggregate=aggregate,
                    exact=exact,
                    exact_validation=exact_validation,
                    baseline_schedule=baseline_schedule,
                    baseline_validation=baseline_validation,
                )
            )
        if index % 15 == 0 or index == len(cases):
            print(f"EXP-01 exact progress: {index}/{len(cases)}", flush=True)

    runs_path = output_directory / "exp01_runs.csv"
    _write_csv(runs_path, rows)
    paired = _paired_rows(rows)
    pairs_path = output_directory / "exp01_profile_pairs.csv"
    _write_csv(pairs_path, paired)

    minimal = min(counterexamples, key=_counterexample_key) if counterexamples else None
    counterexample_path = output_directory / "exp01_counterexample.json"
    counterexample_payload: dict[str, Any] = {
        "experiment_id": "EXP-01",
        "selection_rule": "minimum (task_count, total_work, scenario_id) among T_star > B4 + tolerance",
        "counterexample_count": len(counterexamples),
        "selected": None,
    }
    if minimal is not None:
        assert minimal.exact.schedule is not None
        assert minimal.exact.objective is not None
        assert minimal.exact_validation.metrics is not None
        assert minimal.baseline_validation.metrics is not None
        counterexample_payload["selected"] = {
            "scenario": _scenario_payload(minimal.case.scenario),
            "aggregates": {
                "W4": _format_decimal(minimal.aggregate.w4),
                "L4": _format_decimal(minimal.aggregate.l4),
                "W4_over_P": _format_decimal(minimal.aggregate.work_branch),
                "gamma_H": _format_decimal(minimal.aggregate.human_branch),
                "B4": _format_decimal(minimal.aggregate.b4),
            },
            "exact": {
                "status": minimal.exact.status,
                "T_star": _format_decimal(minimal.exact.objective),
                "best_bound": _format_decimal(minimal.exact.best_bound),
                "gap": _format_decimal(minimal.exact.relative_gap),
                "queue": _format_decimal(minimal.exact_validation.metrics.queue_time),
                "schedule": _schedule_payload(minimal.exact.schedule),
            },
            "baseline": {
                "makespan": _format_decimal(
                    minimal.baseline_validation.metrics.makespan
                ),
                "queue": _format_decimal(minimal.baseline_validation.metrics.queue_time),
                "schedule": _schedule_payload(minimal.baseline_schedule),
            },
        }
    counterexample_path.write_text(
        json.dumps(counterexample_payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    figure_paths: list[Path] = list(
        build_exp01_gap_figure(rows, figure_directory / "exp01_gaps")
    )
    if minimal is not None and minimal.exact.schedule is not None:
        figure_paths.extend(
            build_counterexample_gantt(
                minimal.case.scenario,
                minimal.exact.schedule,
                figure_directory / "exp01_counterexample_gantt",
            )
        )

    report_path = output_directory / "exp01_report.md"
    _write_report(
        report_path,
        matrix=matrix,
        rows=rows,
        paired=paired,
        minimal=minimal,
        figure_paths=tuple(figure_paths),
    )

    outputs_without_manifest = [
        runs_path,
        pairs_path,
        counterexample_path,
        report_path,
        *figure_paths,
    ]
    implementation_paths = sorted(
        (project_root / "src" / "experiments").glob("*.py")
    ) + [project_root / "pyproject.toml", project_root / "uv.lock"]
    manifest_path = output_directory / "exp01_manifest.json"
    manifest = {
        "experiment_id": "EXP-01",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "command": "uv run python -m experiments run --experiment EXP-01",
        **git_provenance(project_root),
        "matrix": {
            "path": str(matrix_path.relative_to(project_root)),
            "sha256": _sha256(matrix_path),
            "frozen_at": matrix.frozen_at,
            "point_count": matrix.point_count,
        },
        "pilot_reduction": {
            "matrix_path": str(pilot_matrix_path.relative_to(project_root)),
            "matrix_sha256": _sha256(pilot_matrix_path),
            "limit_record_path": str(pilot_limit_path.relative_to(project_root)),
            "limit_record_sha256": _sha256(pilot_limit_path),
        },
        "solver": {
            "time_limit_seconds": matrix.solver_time_limit_seconds,
            "random_seed": matrix.solver_random_seed,
            "workers": matrix.solver_workers,
        },
        "dependencies": _dependencies(),
        "summary": {
            "optimal_points": sum(row["solver_status"] == "OPTIMAL" for row in rows),
            "counterexamples": len(counterexamples),
            "paired_comparisons": len(paired),
            "selected_counterexample": (
                minimal.case.scenario.scenario_id if minimal is not None else None
            ),
        },
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
