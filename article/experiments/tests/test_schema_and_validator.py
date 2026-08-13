from dataclasses import replace
from decimal import Decimal
from pathlib import Path

import pytest

from experiments.bounds import compute_aggregates
from experiments.exact_solver import solve_exact
from experiments.schema import (
    PhaseSpec,
    Scenario,
    ScenarioError,
    TaskSpec,
    load_scenario,
)
from experiments.validator import validate_schedule

SCENARIO_DIR = Path(__file__).parents[1] / "scenarios" / "article"


def test_all_article_times_are_exact_ticks() -> None:
    for path in sorted(SCENARIO_DIR.glob("*.yaml")):
        scenario = load_scenario(path)
        for task in scenario.tasks:
            for phase in task.phases:
                duration = scenario.effective_phase_duration(phase)
                ticks = scenario.to_ticks(duration, field=phase.phase_id)
                assert scenario.from_ticks(ticks) == duration


def test_validator_rejects_agent_reassignment() -> None:
    scenario = load_scenario(SCENARIO_DIR / "variant_3.yaml")
    schedule = scenario.schedule_by_id["article_schedule"]
    phases = list(schedule.phases)
    target = next(
        index
        for index, interval in enumerate(phases)
        if interval.task_id == "1" and interval.phase_id == "review"
    )
    phases[target] = replace(phases[target], agent=2)
    invalid = replace(schedule, phases=tuple(phases))
    validation = validate_schedule(scenario, invalid)
    assert not validation.valid
    assert any(issue.code == "agent_reassignment" for issue in validation.issues)


def test_validator_rejects_missing_phase() -> None:
    scenario = load_scenario(SCENARIO_DIR / "variant_4.yaml")
    schedule = scenario.schedule_by_id["article_schedule"]
    invalid = replace(schedule, phases=schedule.phases[:-1])
    validation = validate_schedule(scenario, invalid)
    assert not validation.valid
    assert any(issue.code == "missing_phase" for issue in validation.issues)


def test_time_grid_rejects_non_divisible_values() -> None:
    scenario = load_scenario(SCENARIO_DIR / "variant_2.yaml")
    with pytest.raises(ScenarioError):
        scenario.to_ticks(Decimal("0.03"), field="bad")


def test_exact_solver_rounds_fractional_b4_up_to_the_time_grid() -> None:
    tasks = tuple(
        TaskSpec(
            task_id=str(index),
            name=f"Task {index}",
            z=Decimal("1"),
            k=Decimal("1"),
            h=Decimal("0"),
            predecessors=(),
            phases=(PhaseSpec("work", "agent", Decimal("1")),),
        )
        for index in range(1, 4)
    )
    scenario = Scenario(
        schema_version=1,
        scenario_id="fractional-b4-regression",
        variant_id="fractional-b4-regression",
        time_unit=Decimal("1"),
        tolerance=Decimal("0"),
        x=Decimal("1"),
        p=2,
        c=Decimal("1"),
        gamma=Decimal("1"),
        tasks=tasks,
        schedules=(),
        source_path=Path("fractional-b4-regression.yaml"),
    )

    assert compute_aggregates(scenario).b4 == Decimal("1.5")
    solution = solve_exact(scenario, time_limit_seconds=10)
    assert solution.status == "OPTIMAL"
    assert solution.objective == Decimal("2")
