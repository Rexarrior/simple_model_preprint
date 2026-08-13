from decimal import Decimal
from pathlib import Path

from experiments.bounds import compute_aggregates
from experiments.exact_solver import solve_exact
from experiments.exp02 import (
    build_exp02_scenario,
    c_multiplier,
    gamma_multiplier,
    iter_exp02_cases,
    load_exp02_matrix,
)
from experiments.simulator import simulate_baseline
from experiments.validator import validate_schedule


MATRIX_PATH = (
    Path(__file__).parents[1] / "scenarios" / "canonical" / "exp02_matrix.yaml"
)


def test_exp02_matrix_is_frozen_and_has_70_unique_points() -> None:
    matrix = load_exp02_matrix(MATRIX_PATH)
    cases = list(iter_exp02_cases(matrix))
    assert matrix.point_count == len(cases) == 70
    assert len({case.scenario.scenario_id for case in cases}) == 70
    assert len(
        {
            (
                case.object_spec.object_id,
                case.regime.c_model,
                case.regime.gamma_model,
                case.regime.human_share,
                case.agent_count,
            )
            for case in cases
        }
    ) == 70


def test_exp02_scaling_multipliers_match_frozen_formulas() -> None:
    assert c_multiplier("C0", 12) == Decimal("1")
    assert c_multiplier("C1", 1) == Decimal("1.000")
    assert c_multiplier("C1", 4) == Decimal("1.210")
    assert c_multiplier("C1", 12) == Decimal("2.210")
    assert gamma_multiplier("gamma0", 12) == Decimal("1")
    assert gamma_multiplier("gamma1", 1) == Decimal("1.00")
    assert gamma_multiplier("gamma1", 12) == Decimal("2.10")


def test_practical_object_preserves_total_work_and_applies_human_share() -> None:
    matrix = load_exp02_matrix(MATRIX_PATH)
    object_spec = next(item for item in matrix.objects if item.object_id == "practical_v4")
    regimes = {
        item.regime_id: item
        for item in matrix.regimes
        if item.c_model == "C0" and item.gamma_model == "gamma0"
    }
    scenarios = [
        build_exp02_scenario(
            matrix,
            object_spec=object_spec,
            regime=regimes[regime_id],
            agent_count=4,
        )
        for regime_id in ("c0_g0_rh10", "c0_g0_rh25", "c0_g0_rh50")
    ]
    total_work = [compute_aggregates(scenario).w4 for scenario in scenarios]
    assert total_work[0] == total_work[1] == total_work[2]
    for scenario, expected_share in zip(
        scenarios,
        (Decimal("0.10"), Decimal("0.25"), Decimal("0.50")),
        strict=True,
    ):
        assert all(task.h / task.k == expected_share for task in scenario.tasks)


def test_canonical_object_keeps_fork_join_and_profile() -> None:
    matrix = load_exp02_matrix(MATRIX_PATH)
    object_spec = next(item for item in matrix.objects if item.object_id == "fork_join_n4")
    regime = next(item for item in matrix.regimes if item.regime_id == "c0_g0_rh25")
    scenario = build_exp02_scenario(
        matrix,
        object_spec=object_spec,
        regime=regime,
        agent_count=4,
    )
    assert len(scenario.tasks) == 4
    assert scenario.tasks[0].predecessors == ()
    assert scenario.tasks[1].predecessors == ("t01",)
    assert scenario.tasks[2].predecessors == ("t01",)
    assert scenario.tasks[3].predecessors == ("t02", "t03")
    assert [phase.resource for phase in scenario.tasks[0].phases] == [
        "human",
        "agent",
        "human",
        "agent",
        "human",
        "agent",
        "human",
    ]


def test_exp02_clean_practical_slice_reaches_critical_path_at_p2() -> None:
    matrix = load_exp02_matrix(MATRIX_PATH)
    object_spec = next(item for item in matrix.objects if item.object_id == "practical_v4")
    regime = next(item for item in matrix.regimes if item.regime_id == "c0_g0_rh25")
    scenario = build_exp02_scenario(
        matrix,
        object_spec=object_spec,
        regime=regime,
        agent_count=2,
    )
    aggregate = compute_aggregates(scenario)
    assert aggregate.active_branches == ("critical_path",)
    assert aggregate.b4 == Decimal("36.70000")

    exact = solve_exact(scenario, time_limit_seconds=10, workers=1)
    assert exact.status == "OPTIMAL"
    assert exact.objective == aggregate.b4
    assert exact.schedule is not None
    assert validate_schedule(scenario, exact.schedule).valid

    baseline = simulate_baseline(scenario)
    baseline_validation = validate_schedule(scenario, baseline)
    assert baseline_validation.valid
    assert baseline_validation.metrics is not None
    assert baseline_validation.metrics.makespan >= exact.objective
