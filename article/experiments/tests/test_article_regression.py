import hashlib
from decimal import Decimal
from pathlib import Path

import pytest

from experiments.bounds import compute_aggregates
from experiments.exact_solver import solve_exact
from experiments.figures import build_main_figures
from experiments.schema import load_scenario
from experiments.simulator import simulate_baseline
from experiments.validator import validate_schedule

SCENARIO_DIR = Path(__file__).parents[1] / "scenarios" / "article"

EXPECTED = {
    "variant_2.yaml": {
        "A": Decimal("21.4"),
        "H": Decimal("38.4"),
        "W4": Decimal("59.8"),
        "L4": Decimal("47.8"),
        "B4": Decimal("47.8"),
        "Q": Decimal("22.2"),
    },
    "variant_3.yaml": {
        "A": Decimal("34.6"),
        "H": Decimal("19.0"),
        "W4": Decimal("53.6"),
        "L4": Decimal("43.2"),
        "B4": Decimal("43.2"),
        "Q": Decimal("0"),
    },
    "variant_4.yaml": {
        "A": Decimal("34.6"),
        "H": Decimal("19.0"),
        "W4": Decimal("53.6"),
        "L4": Decimal("36.7"),
        "B4": Decimal("36.7"),
        "Q": Decimal("4.3"),
    },
}


@pytest.mark.parametrize("filename", sorted(EXPECTED))
def test_article_aggregates_and_schedules(filename: str) -> None:
    scenario = load_scenario(SCENARIO_DIR / filename)
    expected = EXPECTED[filename]
    metrics = compute_aggregates(scenario)
    assert metrics.t_h == Decimal("76")
    assert metrics.a == expected["A"]
    assert metrics.h == expected["H"]
    assert metrics.w4 == expected["W4"]
    assert metrics.l4 == expected["L4"]
    assert metrics.b4 == expected["B4"]

    schedule = scenario.schedule_by_id["article_schedule"]
    validation = validate_schedule(scenario, schedule)
    assert validation.valid, validation.issues
    assert validation.metrics is not None
    assert validation.metrics.makespan == expected["B4"]
    assert validation.metrics.queue_time == expected["Q"]
    assert validation.metrics.human_busy_time == expected["H"]


def test_original_variant_2_schedule_is_rejected_by_m4() -> None:
    scenario = load_scenario(SCENARIO_DIR / "variant_2.yaml")
    schedule = scenario.schedule_by_id["original_invalid_schedule"]
    validation = validate_schedule(scenario, schedule)
    assert not validation.valid
    assert any(issue.code == "human_overlap" for issue in validation.issues)


@pytest.mark.parametrize("filename", sorted(EXPECTED))
def test_exact_solver_reaches_article_lower_bound(filename: str) -> None:
    scenario = load_scenario(SCENARIO_DIR / filename)
    metrics = compute_aggregates(scenario)
    solution = solve_exact(scenario, time_limit_seconds=30)
    assert solution.status == "OPTIMAL"
    assert solution.objective == metrics.b4
    assert solution.best_bound == metrics.b4
    assert solution.relative_gap == 0
    assert solution.schedule is not None
    validation = validate_schedule(scenario, solution.schedule)
    assert validation.valid, validation.issues
    assert validation.metrics is not None
    assert validation.metrics.makespan == solution.objective


@pytest.mark.parametrize("filename", sorted(EXPECTED))
def test_deterministic_baseline_is_feasible(filename: str) -> None:
    scenario = load_scenario(SCENARIO_DIR / filename)
    first = simulate_baseline(scenario)
    second = simulate_baseline(scenario)
    assert first == second
    validation = validate_schedule(scenario, first)
    assert validation.valid, validation.issues
    assert validation.metrics is not None
    assert validation.metrics.makespan >= EXPECTED[filename]["B4"]


def test_variant_2_baseline_exposes_fcfs_queue_cost() -> None:
    scenario = load_scenario(SCENARIO_DIR / "variant_2.yaml")
    validation = validate_schedule(scenario, simulate_baseline(scenario))
    assert validation.valid, validation.issues
    assert validation.metrics is not None
    assert validation.metrics.makespan == Decimal("48.6")
    assert validation.metrics.queue_time == Decimal("12.2")


def test_main_figures_are_generated(tmp_path: Path) -> None:
    first = build_main_figures(SCENARIO_DIR, tmp_path / "first")
    second = build_main_figures(SCENARIO_DIR, tmp_path / "second")
    assert len(first) == len(second) == 4
    for output, repeated in zip(first, second, strict=True):
        assert output.exists()
        assert output.stat().st_size > 1000
        assert hashlib.sha256(output.read_bytes()).digest() == hashlib.sha256(
            repeated.read_bytes()
        ).digest()
