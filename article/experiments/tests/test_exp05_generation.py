from decimal import Decimal
from pathlib import Path

from experiments.bounds import compute_aggregates
from experiments.exact_solver import solve_exact
from experiments.exp05 import (
    _analysis_rows,
    _position_rows,
    build_exp05_scenario,
    iter_exp05_cases,
    load_exp05_matrix,
)
from experiments.validator import validate_schedule


MATRIX_PATH = (
    Path(__file__).parents[1] / "scenarios" / "canonical" / "exp05_matrix.yaml"
)


def test_exp05_matrix_deduplicates_216_positions_to_156_scenarios() -> None:
    matrix = load_exp05_matrix(MATRIX_PATH)
    cases = list(iter_exp05_cases(matrix))
    assert matrix.point_count == 216
    assert len(cases) == 156
    assert sum(len(case.aliases) for case in cases) == 216
    assert len({case.semantic_sha256 for case in cases}) == 156
    for p in matrix.agent_counts:
        m1 = next(
            case
            for case in cases
            if case.parameters.p == p and case.parameters.m == 1
        )
        assert len(m1.aliases) == 6
        m2_zero = next(
            case
            for case in cases
            if case.parameters.p == p
            and case.parameters.m == 2
            and case.parameters.overhead_rate == 0
        )
        assert len(m2_zero.aliases) == 2


def test_exp05_zero_overhead_preserves_work_and_quality_gate() -> None:
    matrix = load_exp05_matrix(MATRIX_PATH)
    for p in matrix.agent_counts:
        for m in matrix.m_values:
            scenario, total, human, agent = build_exp05_scenario(
                matrix,
                p=p,
                m=m,
                overhead_rate=Decimal("0"),
                lambda_h=Decimal("0"),
            )
            aggregate = compute_aggregates(scenario)
            assert total == human == agent == 0
            assert aggregate.w4 == Decimal("60")
            assert aggregate.h == Decimal("15")
            assert scenario.p == p
            assert scenario.task_by_id["t04_join"].quality_gate_id == "qg_t04"
            assert sum(
                task.quality_gate_id == "qg_t04" for task in scenario.tasks
            ) == 1


def test_exp05_overhead_is_independent_of_p_and_partitioned() -> None:
    matrix = load_exp05_matrix(MATRIX_PATH)
    aggregates = []
    for p in (1, 4, 8):
        scenario, total, human, agent = build_exp05_scenario(
            matrix,
            p=p,
            m=4,
            overhead_rate=Decimal("0.10"),
            lambda_h=Decimal("0.5"),
        )
        aggregate = compute_aggregates(scenario)
        aggregates.append(aggregate)
        assert total == Decimal("7.20")
        assert human == agent == Decimal("3.600")
        assert aggregate.w4 == Decimal("67.200")
        assert aggregate.h == Decimal("18.600")
    assert {aggregate.w4 for aggregate in aggregates} == {Decimal("67.200")}


def test_exp05_reconstructs_grid_and_interaction_formula() -> None:
    matrix = load_exp05_matrix(MATRIX_PATH)
    cases = list(iter_exp05_cases(matrix))
    rows = [
        {
            "semantic_sha256": case.semantic_sha256,
            "scenario_id": case.scenario.scenario_id,
            "T_star": format(
                Decimal("100")
                - Decimal(2 * case.parameters.p * case.parameters.m),
                "f",
            ),
        }
        for case in cases
    ]
    positions = _position_rows(cases, rows, matrix)
    analysis = _analysis_rows(positions, matrix)
    assert len(positions) == 216
    assert len(analysis) == 180
    selected = next(
        row
        for row in analysis
        if row["P"] == "4"
        and row["m"] == "3"
        and row["analysis_overhead_rate"] == "0.10"
        and row["analysis_lambda_h"] == "0.5"
    )
    assert Decimal(selected["interaction_contrast"]) == Decimal("12")


def test_exp05_small_reference_point_is_exact_and_valid() -> None:
    matrix = load_exp05_matrix(MATRIX_PATH)
    scenario, _, _, _ = build_exp05_scenario(
        matrix,
        p=1,
        m=1,
        overhead_rate=Decimal("0"),
        lambda_h=Decimal("0"),
    )
    exact = solve_exact(scenario, time_limit_seconds=10, workers=1)
    assert exact.status == "OPTIMAL"
    assert exact.objective is not None
    assert exact.schedule is not None
    assert validate_schedule(scenario, exact.schedule).valid
    assert exact.objective >= compute_aggregates(scenario).b4
