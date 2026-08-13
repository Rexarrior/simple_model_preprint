from decimal import Decimal
from pathlib import Path

from experiments.bounds import compute_aggregates
from experiments.exp06 import (
    _run_exp06a,
    build_adversarial_pair,
    build_random_pair,
    load_exp06_matrix,
)


MATRIX_PATH = (
    Path(__file__).parents[1] / "scenarios" / "canonical" / "exp06_matrix.yaml"
)


def test_exp06_frozen_counts() -> None:
    matrix = load_exp06_matrix(MATRIX_PATH)
    assert len(matrix.scale_objects) * len(matrix.scale_factors) == 20
    assert matrix.random_pair_count == 5000
    assert matrix.expected_random_solution_count == 10000
    assert len(matrix.adversarial_u_values) == 191
    assert matrix.adversarial_u_values[0] == Decimal("0")
    assert matrix.adversarial_u_values[-1] == Decimal("0.95")
    assert len(matrix.adversarial_modes) * len(matrix.adversarial_u_values) == 382


def test_exp06a_all_frozen_objects_scale_exactly() -> None:
    matrix = load_exp06_matrix(MATRIX_PATH)
    rows, phases, events = _run_exp06a(matrix)
    assert len(rows) == 20
    assert all(row["solver_status"] == "OPTIMAL" for row in rows)
    assert phases
    assert events
    for object_id in {row["object_id"] for row in rows}:
        selected = [row for row in rows if row["object_id"] == object_id]
        reference = next(row for row in selected if row["kappa"] == "1")
        for row in selected:
            kappa = Decimal(row["kappa"])
            assert Decimal(row["T_star"]) == Decimal(reference["T_star"]) * kappa
            assert Decimal(row["B4"]) == Decimal(reference["B4"]) * kappa


def test_exp06b_pair_is_deterministic_paired_and_bounded() -> None:
    matrix = load_exp06_matrix(MATRIX_PATH)
    first_3, first_4, first_rows = build_random_pair(
        matrix, u=Decimal("0.20"), seed=17
    )
    second_3, second_4, second_rows = build_random_pair(
        matrix, u=Decimal("0.20"), seed=17
    )
    assert first_3 == second_3
    assert first_4 == second_4
    assert first_rows == second_rows
    assert len(first_rows) == 32
    assert all(
        Decimal("0.8") <= Decimal(row["applied_multiplier"]) <= Decimal("1.2")
        for row in first_rows
    )
    for task_id in matrix.common_task_ids:
        for resource in ("agent", "human"):
            task_3 = first_3.task_by_id[task_id]
            task_4 = first_4.task_by_id[task_id]
            durations_3 = [
                phase.base_duration
                for phase in task_3.phases
                if phase.resource == resource
            ]
            durations_4 = [
                phase.base_duration
                for phase in task_4.phases
                if phase.resource == resource
            ]
            assert durations_3 == durations_4


def test_exp06b_preserves_positive_consistent_task_coefficients() -> None:
    matrix = load_exp06_matrix(MATRIX_PATH)
    for u in matrix.uncertainty_levels:
        scenario_3, scenario_4, _ = build_random_pair(matrix, u=u, seed=999)
        for scenario in (scenario_3, scenario_4):
            for task in scenario.tasks:
                human = sum(
                    phase.base_duration
                    for phase in task.phases
                    if phase.resource == "human"
                )
                agent = sum(
                    phase.base_duration
                    for phase in task.phases
                    if phase.resource == "agent"
                )
                assert task.k > task.h > 0
                assert scenario.x * task.z * task.h == human
                assert scenario.x * task.z * task.a == agent


def test_exp06c_moves_only_selected_test_resource_in_adverse_direction() -> None:
    matrix = load_exp06_matrix(MATRIX_PATH)
    scenario_3, scenario_4 = build_adversarial_pair(
        matrix, mode="critical_task_agent", u=Decimal("0.20")
    )
    base_3, base_4 = build_adversarial_pair(
        matrix, mode="critical_task_agent", u=Decimal("0")
    )
    assert compute_aggregates(scenario_3).w4 < compute_aggregates(base_3).w4
    assert compute_aggregates(scenario_4).w4 > compute_aggregates(base_4).w4
    for task_id in matrix.common_task_ids:
        assert scenario_3.task_by_id[task_id] == base_3.task_by_id[task_id]
        assert scenario_4.task_by_id[task_id] == base_4.task_by_id[task_id]
