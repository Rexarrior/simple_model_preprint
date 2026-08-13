from decimal import Decimal
from pathlib import Path

from experiments.bounds import compute_aggregates
from experiments.exact_solver import solve_exact
from experiments.exp04 import (
    build_exp04_scenario,
    iter_exp04_cases,
    load_exp04_matrix,
)
from experiments.validator import validate_schedule


MATRIX_PATH = (
    Path(__file__).parents[1] / "scenarios" / "canonical" / "exp04_matrix.yaml"
)


def test_exp04_matrix_deduplicates_90_combinations_to_66_scenarios() -> None:
    matrix = load_exp04_matrix(MATRIX_PATH)
    cases = list(iter_exp04_cases(matrix))
    assert matrix.point_count == 90
    assert len(cases) == 66
    assert sum(len(case.aliases) for case in cases) == 90
    assert len({case.semantic_sha256 for case in cases}) == 66
    m1 = next(case for case in cases if case.parameters.m == 1)
    assert len(m1.aliases) == 15
    m2_zero = next(
        case
        for case in cases
        if case.parameters.m == 2 and case.parameters.overhead_rate == 0
    )
    assert len(m2_zero.aliases) == 3


def test_exp04_zero_overhead_preserves_useful_work_and_quality_gate() -> None:
    matrix = load_exp04_matrix(MATRIX_PATH)
    scenarios = []
    for m in matrix.m_values:
        scenario, total, human, agent = build_exp04_scenario(
            matrix,
            m=m,
            overhead_rate=Decimal("0"),
            lambda_h=Decimal("0"),
        )
        scenarios.append(scenario)
        assert total == human == agent == 0
        assert scenario.task_by_id["t04_join"].quality_gate_id == "qg_t04"
        assert sum(
            task.quality_gate_id == "qg_t04" for task in scenario.tasks
        ) == 1
    aggregates = [compute_aggregates(scenario) for scenario in scenarios]
    assert all(value.w4 == Decimal("60") for value in aggregates)
    assert all(value.h == Decimal("15") for value in aggregates)


def test_exp04_overhead_is_fully_partitioned_between_resources() -> None:
    matrix = load_exp04_matrix(MATRIX_PATH)
    scenario, total, human, agent = build_exp04_scenario(
        matrix,
        m=4,
        overhead_rate=Decimal("0.10"),
        lambda_h=Decimal("0.5"),
    )
    aggregate = compute_aggregates(scenario)
    assert total == Decimal("7.20")
    assert human == agent == Decimal("3.600")
    assert aggregate.w4 == Decimal("67.200")
    assert aggregate.h == Decimal("18.600")


def test_exp04_small_reference_point_is_exact_and_valid() -> None:
    matrix = load_exp04_matrix(MATRIX_PATH)
    scenario, _, _, _ = build_exp04_scenario(
        matrix,
        m=1,
        overhead_rate=Decimal("0"),
        lambda_h=Decimal("0"),
    )
    exact = solve_exact(scenario, time_limit_seconds=10, workers=1)
    assert exact.status == "OPTIMAL"
    assert exact.objective is not None
    assert exact.schedule is not None
    validation = validate_schedule(scenario, exact.schedule)
    assert validation.valid
    assert exact.objective >= compute_aggregates(scenario).b4
