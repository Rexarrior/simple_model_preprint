from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.metadata
import json
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Iterable

from .bounds import AggregateMetrics, compute_aggregates
from .exact_solver import ExactSolution, solve_exact
from .figures import build_main_figures
from .provenance import git_provenance
from .schema import Scenario, load_scenario
from .simulator import simulate_baseline
from .validator import ScheduleValidation, validate_schedule

EXACT_TIME_LIMIT_SECONDS = 300.0
EXACT_RANDOM_SEED = 0
EXACT_WORKERS = 1


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def article_scenario_dir() -> Path:
    return project_root() / "scenarios" / "article"


def scenario_paths(directory: Path) -> list[Path]:
    return sorted((*directory.glob("*.yaml"), *directory.glob("*.yml")))


def load_scenarios(directory: Path) -> list[Scenario]:
    paths = scenario_paths(directory)
    if not paths:
        raise RuntimeError(f"no YAML scenarios found in {directory}")
    return [load_scenario(path) for path in paths]


def _format_decimal(value: Decimal | None) -> str:
    if value is None:
        return ""
    return format(value, "f")


def _assert_close(
    actual: Decimal,
    expected: Decimal,
    tolerance: Decimal,
    *,
    label: str,
) -> None:
    if abs(actual - expected) > tolerance:
        raise RuntimeError(f"{label}: got {actual}, expected {expected}")


def _schedule_status(
    scenario: Scenario,
    validation: ScheduleValidation,
    schedule_id: str,
) -> str:
    schedule = scenario.schedule_by_id[schedule_id]
    if validation.valid != schedule.expected_valid:
        return "MISMATCH"
    return "VALID" if validation.valid else "EXPECTED_INVALID"


def validate_scenarios(directory: Path) -> int:
    failures = 0
    for scenario in load_scenarios(directory):
        metrics = compute_aggregates(scenario)
        print(
            f"{scenario.scenario_id}: B4={_format_decimal(metrics.b4)}, "
            f"L4={_format_decimal(metrics.l4)}, "
            f"critical_path={'->'.join(metrics.critical_path_l4)}"
        )
        for schedule in scenario.schedules:
            validation = validate_schedule(scenario, schedule)
            status = _schedule_status(scenario, validation, schedule.schedule_id)
            print(f"  {schedule.schedule_id}: {status}")
            if status == "MISMATCH":
                failures += 1
            for issue in validation.issues:
                print(f"    {issue.code}: {issue.message}")
    return failures


def _dependency_versions() -> dict[str, str]:
    versions: dict[str, str] = {}
    for distribution in ("matplotlib", "ortools", "PyYAML", "pytest"):
        try:
            versions[distribution] = importlib.metadata.version(distribution)
        except importlib.metadata.PackageNotFoundError:
            versions[distribution] = "not-installed"
    return versions


def _file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _validate_article_schedule(
    scenario: Scenario,
) -> tuple[ScheduleValidation, Decimal]:
    schedule = scenario.schedule_by_id["article_schedule"]
    validation = validate_schedule(scenario, schedule)
    if not validation.valid or validation.metrics is None:
        details = "; ".join(issue.message for issue in validation.issues)
        raise RuntimeError(f"{scenario.scenario_id}: invalid article schedule: {details}")
    if schedule.expected_makespan is not None:
        _assert_close(
            validation.metrics.makespan,
            schedule.expected_makespan,
            scenario.tolerance,
            label=f"{scenario.scenario_id} article makespan",
        )
    if schedule.expected_queue is not None:
        _assert_close(
            validation.metrics.queue_time,
            schedule.expected_queue,
            scenario.tolerance,
            label=f"{scenario.scenario_id} article queue",
        )
    return validation, validation.metrics.makespan


def _run_exact_and_validate(scenario: Scenario) -> ExactSolution:
    solution = solve_exact(
        scenario,
        time_limit_seconds=EXACT_TIME_LIMIT_SECONDS,
        random_seed=EXACT_RANDOM_SEED,
        workers=EXACT_WORKERS,
    )
    if solution.status != "OPTIMAL" or solution.objective is None:
        raise RuntimeError(
            f"{scenario.scenario_id}: exact solver returned {solution.status}"
        )
    if solution.schedule is None:
        raise RuntimeError(f"{scenario.scenario_id}: solver returned no schedule")
    validation = validate_schedule(scenario, solution.schedule)
    if not validation.valid:
        details = "; ".join(issue.message for issue in validation.issues)
        raise RuntimeError(
            f"{scenario.scenario_id}: exported exact schedule is invalid: {details}"
        )
    return solution


def _run_baseline_and_validate(scenario: Scenario) -> ScheduleValidation:
    schedule = simulate_baseline(scenario)
    validation = validate_schedule(scenario, schedule)
    if not validation.valid or validation.metrics is None:
        details = "; ".join(issue.message for issue in validation.issues)
        raise RuntimeError(
            f"{scenario.scenario_id}: baseline schedule is invalid: {details}"
        )
    return validation


def _result_row(
    scenario: Scenario,
    metrics: AggregateMetrics,
    article_validation: ScheduleValidation,
    baseline_validation: ScheduleValidation,
    solution: ExactSolution,
) -> dict[str, str]:
    assert article_validation.metrics is not None
    assert baseline_validation.metrics is not None
    assert solution.objective is not None
    baseline_gap = baseline_validation.metrics.makespan - solution.objective
    return {
        "scenario_id": scenario.scenario_id,
        "variant_id": scenario.variant_id,
        "T_h": _format_decimal(metrics.t_h),
        "A": _format_decimal(metrics.a),
        "H": _format_decimal(metrics.h),
        "W3": _format_decimal(metrics.w3),
        "L3": _format_decimal(metrics.l3),
        "W4": _format_decimal(metrics.w4),
        "L4": _format_decimal(metrics.l4),
        "W4_over_P": _format_decimal(metrics.work_branch),
        "gamma_H": _format_decimal(metrics.human_branch),
        "B4": _format_decimal(metrics.b4),
        "active_branches": ",".join(metrics.active_branches),
        "critical_path": "->".join(metrics.critical_path_l4),
        "article_makespan": _format_decimal(article_validation.metrics.makespan),
        "article_queue": _format_decimal(article_validation.metrics.queue_time),
        "article_blocked_any": _format_decimal(
            article_validation.metrics.blocked_any_time
        ),
        "baseline_makespan": _format_decimal(
            baseline_validation.metrics.makespan
        ),
        "baseline_queue": _format_decimal(baseline_validation.metrics.queue_time),
        "baseline_gap_to_optimum": _format_decimal(baseline_gap),
        "baseline_relative_gap": _format_decimal(
            (baseline_gap / solution.objective).quantize(Decimal("0.000001"))
            if solution.objective != 0 else Decimal("0")
        ),
        "solver_status": solution.status,
        "solver_time_limit_seconds": f"{EXACT_TIME_LIMIT_SECONDS:g}",
        "solver_random_seed": str(EXACT_RANDOM_SEED),
        "solver_workers": str(EXACT_WORKERS),
        "T_star": _format_decimal(solution.objective),
        "solver_best_bound": _format_decimal(solution.best_bound),
        "solver_gap": _format_decimal(solution.relative_gap),
        "solver_wall_time_seconds": f"{solution.wall_time:.6f}",
    }


def run_exp00(output_directory: Path) -> tuple[Path, Path, tuple[Path, ...]]:
    scenarios = load_scenarios(article_scenario_dir())
    output_directory.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, str]] = []
    scenario_manifest: list[dict[str, str]] = []
    for scenario in scenarios:
        metrics = compute_aggregates(scenario)
        article_validation, article_makespan = _validate_article_schedule(scenario)
        if "original_invalid_schedule" in scenario.schedule_by_id:
            invalid = validate_schedule(
                scenario,
                scenario.schedule_by_id["original_invalid_schedule"],
            )
            if invalid.valid or not any(
                issue.code == "human_overlap" for issue in invalid.issues
            ):
                raise RuntimeError(
                    f"{scenario.scenario_id}: original schedule must fail human overlap"
                )

        solution = _run_exact_and_validate(scenario)
        baseline_validation = _run_baseline_and_validate(scenario)
        _assert_close(
            solution.objective,
            metrics.b4,
            scenario.tolerance,
            label=f"{scenario.scenario_id} T*=B4",
        )
        _assert_close(
            article_makespan,
            solution.objective,
            scenario.tolerance,
            label=f"{scenario.scenario_id} article T=T*",
        )
        rows.append(
            _result_row(
                scenario,
                metrics,
                article_validation,
                baseline_validation,
                solution,
            )
        )
        scenario_manifest.append(
            {
                "scenario_id": scenario.scenario_id,
                "path": str(scenario.source_path.relative_to(project_root())),
                "sha256": _file_hash(scenario.source_path),
            }
        )

    summary_path = output_directory / "exp00_summary.csv"
    with summary_path.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(
            target,
            fieldnames=list(rows[0]),
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)

    figure_paths = build_main_figures(
        article_scenario_dir(),
        project_root() / "figures",
    )
    manifest_path = output_directory / "exp00_manifest.json"
    implementation_paths = sorted(
        (project_root() / "src" / "experiments").glob("*.py")
    ) + [project_root() / "pyproject.toml", project_root() / "uv.lock"]
    manifest = {
        "experiment_id": "EXP-00",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "command": "uv run python -m experiments run --experiment EXP-00",
        **git_provenance(project_root()),
        "dependencies": _dependency_versions(),
        "solver": {
            "time_limit_seconds": EXACT_TIME_LIMIT_SECONDS,
            "random_seed": EXACT_RANDOM_SEED,
            "workers": EXACT_WORKERS,
        },
        "baseline_policy": {
            "ready_tasks": "bottom_level_desc,weight_desc,task_id",
            "human_queue": "request_time,bottom_level_desc,task_id,phase_index",
        },
        "implementation": [
            {
                "path": str(path.relative_to(project_root())),
                "sha256": _file_hash(path),
            }
            for path in implementation_paths
        ],
        "scenarios": scenario_manifest,
        "summary": str(summary_path.relative_to(project_root())),
        "figures": [
            {
                "path": str(path.relative_to(project_root())),
                "sha256": _file_hash(path),
            }
            for path in figure_paths
        ],
    }
    with manifest_path.open("w", encoding="utf-8") as target:
        json.dump(manifest, target, ensure_ascii=False, indent=2)
        target.write("\n")
    return summary_path, manifest_path, figure_paths


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m experiments",
        description="Computational experiments for simple_model_full",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        default=article_scenario_dir(),
    )
    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("--experiment", required=True)
    run_parser.add_argument(
        "--output",
        type=Path,
        default=project_root() / "results",
    )
    run_parser.add_argument(
        "--stage",
        choices=["all", "development", "confirmatory"],
        default="all",
        help="EXP-08 stage; ignored by earlier experiments",
    )
    figures_parser = subparsers.add_parser("figures")
    figures_parser.add_argument("--set", required=True, choices=["main", "candidates"])
    figures_parser.add_argument(
        "--output",
        type=Path,
        default=project_root() / "figures",
    )
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(list(argv) if argv is not None else None)
    if args.command == "validate":
        return 1 if validate_scenarios(args.path.resolve()) else 0
    if args.command == "run":
        if args.experiment == "EXP-00":
            summary_path, manifest_path, figure_paths = run_exp00(
                args.output.resolve()
            )
            print(f"wrote {summary_path}")
            print(f"wrote {manifest_path}")
            for path in figure_paths:
                print(f"wrote {path}")
            return 0
        if args.experiment == "EXP-01":
            from .exp01 import run_exp01

            for path in run_exp01(project_root(), args.output.resolve()):
                print(f"wrote {path}")
            return 0
        if args.experiment == "EXP-02":
            from .exp02 import run_exp02

            for path in run_exp02(project_root(), args.output.resolve()):
                print(f"wrote {path}")
            return 0
        if args.experiment == "EXP-03":
            from .exp03 import run_exp03

            for path in run_exp03(project_root(), args.output.resolve()):
                print(f"wrote {path}")
            return 0
        if args.experiment == "EXP-04":
            from .exp04 import run_exp04

            for path in run_exp04(project_root(), args.output.resolve()):
                print(f"wrote {path}")
            return 0
        if args.experiment == "EXP-05":
            from .exp05 import run_exp05

            for path in run_exp05(project_root(), args.output.resolve()):
                print(f"wrote {path}")
            return 0
        if args.experiment == "EXP-06":
            from .exp06 import run_exp06

            for path in run_exp06(project_root(), args.output.resolve()):
                print(f"wrote {path}")
            return 0
        if args.experiment == "EXP-07":
            from .exp07 import run_exp07

            for path in run_exp07(project_root(), args.output.resolve()):
                print(f"wrote {path}")
            return 0
        if args.experiment == "EXP-08":
            from .exp08 import run_exp08

            for path in run_exp08(
                project_root(), args.output.resolve(), stage=args.stage
            ):
                print(f"wrote {path}")
            return 0
        raise SystemExit(f"experiment {args.experiment} is not implemented")
    if args.command == "figures":
        if args.set == "main":
            outputs = build_main_figures(
                article_scenario_dir(),
                args.output.resolve(),
            )
        else:
            from .candidate_figures import build_candidate_figures

            outputs = build_candidate_figures(
                project_root(),
                args.output.resolve(),
                project_root() / "results",
            )
        for output in outputs:
            print(f"wrote {output}")
        return 0
    raise AssertionError(f"unhandled command {args.command}")
