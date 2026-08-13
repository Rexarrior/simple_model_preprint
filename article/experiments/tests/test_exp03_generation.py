from decimal import Decimal
from pathlib import Path

from experiments.bounds import compute_aggregates
from experiments.exact_solver import solve_exact
from experiments.exp03 import (
    build_exp03_scenario,
    iter_exp03_cases,
    load_exp03_matrix,
    trace_schedule,
)
from experiments.simulator import simulate_baseline
from experiments.validator import validate_schedule


MATRIX_PATH = (
    Path(__file__).parents[1] / "scenarios" / "canonical" / "exp03_matrix.yaml"
)


def test_exp03_matrix_is_frozen_and_has_32_unique_points() -> None:
    matrix = load_exp03_matrix(MATRIX_PATH)
    cases = list(iter_exp03_cases(matrix))
    assert matrix.point_count == len(cases) == 32
    assert len({case.scenario.scenario_id for case in cases}) == 32


def test_exp03_profiles_preserve_all_pairing_aggregates() -> None:
    matrix = load_exp03_matrix(MATRIX_PATH)
    values = []
    for profile in matrix.phase_profiles:
        scenario = build_exp03_scenario(
            matrix,
            topology="fork_join",
            agent_count=4,
            human_share=Decimal("0.50"),
            phase_profile=profile,
        )
        aggregate = compute_aggregates(scenario)
        values.append(
            (
                aggregate.a,
                aggregate.h,
                aggregate.w4,
                aggregate.l4,
                aggregate.b4,
            )
        )
    assert values[0] == values[1] == values[2] == values[3]


def test_front_loaded_profile_uses_frozen_90_10_human_split() -> None:
    matrix = load_exp03_matrix(MATRIX_PATH)
    scenario = build_exp03_scenario(
        matrix,
        topology="two_layer",
        agent_count=2,
        human_share=Decimal("0.25"),
        phase_profile="front_loaded",
    )
    task = scenario.tasks[0]
    human = [phase.base_duration for phase in task.phases if phase.resource == "human"]
    agent = [phase.base_duration for phase in task.phases if phase.resource == "agent"]
    assert len(human) == 2
    assert len(agent) == 1
    assert human[0] / sum(human) == Decimal("0.90")
    assert human[1] / sum(human) == Decimal("0.10")


def test_exp03_trace_matches_validator_queue_metrics() -> None:
    matrix = load_exp03_matrix(MATRIX_PATH)
    scenario = build_exp03_scenario(
        matrix,
        topology="fork_join",
        agent_count=2,
        human_share=Decimal("0.50"),
        phase_profile="alternating_sync",
    )
    schedule = simulate_baseline(scenario)
    validation = validate_schedule(scenario, schedule)
    assert validation.valid
    assert validation.metrics is not None
    trace = trace_schedule(
        scenario,
        schedule,
        validation,
        schedule_kind="baseline",
    )
    assert trace.queue_time == validation.metrics.queue_time
    assert trace.blocked_agent_time == validation.metrics.blocked_agent_time
    assert trace.blocked_any_time == validation.metrics.blocked_any_time
    assert (
        abs(trace.mean_queue_length * trace.makespan - trace.queue_time)
        < Decimal("1e-25")
    )
    assert trace.maximum_queue_length <= scenario.p
    assert trace.full_agent_stop_time >= 0


def test_exp03_small_exact_point_is_optimal_and_exported_schedule_is_valid() -> None:
    matrix = load_exp03_matrix(MATRIX_PATH)
    scenario = build_exp03_scenario(
        matrix,
        topology="two_layer",
        agent_count=2,
        human_share=Decimal("0.25"),
        phase_profile="front_loaded",
    )
    exact = solve_exact(scenario, time_limit_seconds=10, workers=1)
    assert exact.status == "OPTIMAL"
    assert exact.objective is not None
    assert exact.schedule is not None
    validation = validate_schedule(scenario, exact.schedule)
    assert validation.valid
    assert exact.objective >= compute_aggregates(scenario).b4
