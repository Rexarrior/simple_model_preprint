from decimal import Decimal
from pathlib import Path

import pytest

from experiments.bounds import compute_aggregates
from experiments.exact_solver import solve_exact
from experiments.generators import (
    build_exp01_scenario,
    iter_exp01_cases,
    load_exp01_matrix,
)
from experiments.simulator import simulate_baseline
from experiments.validator import validate_schedule

MATRIX_PATH = (
    Path(__file__).parents[1] / "scenarios" / "canonical" / "exp01_matrix.yaml"
)


def test_exp01_matrix_is_frozen_and_has_90_unique_points() -> None:
    matrix = load_exp01_matrix(MATRIX_PATH)
    cases = list(iter_exp01_cases(matrix))
    assert matrix.point_count == len(cases) == 90
    assert len({case.scenario.scenario_id for case in cases}) == 90


@pytest.mark.parametrize(
    "topology",
    ["chain", "independent", "fork_join", "diamond", "two_layer"],
)
def test_profiles_preserve_aggregates(topology: str) -> None:
    matrix = load_exp01_matrix(MATRIX_PATH)
    aggregates = []
    scenarios = []
    for profile in matrix.phase_profiles:
        scenario = build_exp01_scenario(
            matrix,
            topology=topology,
            task_count=8,
            agent_count=4,
            human_share=Decimal("0.25"),
            phase_profile=profile,
        )
        scenarios.append(scenario)
        value = compute_aggregates(scenario)
        aggregates.append((value.a, value.h, value.w4, value.l4, value.b4))
    assert aggregates[0] == aggregates[1] == aggregates[2]
    assert sum(
        phase.resource == "human"
        for phase in scenarios[1].tasks[0].phases
    ) == 4
    assert sum(
        phase.resource == "human"
        for phase in scenarios[2].tasks[0].phases
    ) == 4


def test_small_exp01_counterexample_is_exact_and_baseline_is_feasible() -> None:
    matrix = load_exp01_matrix(MATRIX_PATH)
    scenario = build_exp01_scenario(
        matrix,
        topology="independent",
        task_count=4,
        agent_count=2,
        human_share=Decimal("0.50"),
        phase_profile="alternating_sync",
    )
    aggregate = compute_aggregates(scenario)
    exact = solve_exact(scenario, time_limit_seconds=10, workers=1)
    assert exact.status == "OPTIMAL"
    assert exact.objective is not None
    assert exact.objective > aggregate.b4
    assert exact.schedule is not None
    exact_validation = validate_schedule(scenario, exact.schedule)
    assert exact_validation.valid, exact_validation.issues

    baseline = simulate_baseline(scenario)
    baseline_validation = validate_schedule(scenario, baseline)
    assert baseline_validation.valid, baseline_validation.issues
    assert baseline_validation.metrics is not None
    assert baseline_validation.metrics.makespan >= exact.objective
