from __future__ import annotations

from decimal import Decimal
from pathlib import Path

from experiments.candidate_figures import (
    _conflicting_human_phases,
    _write_candidate_report,
    build_probabilistic_fan,
    build_resource_augmented_path,
    build_task_lever_map,
    build_variant2_schedule_comparison,
)
from experiments.schema import load_scenario


PROJECT_ROOT = Path(__file__).parents[1]
SCENARIO_DIRECTORY = PROJECT_ROOT / "scenarios" / "article"
RESULT_DIRECTORY = PROJECT_ROOT / "results"


def test_variant2_comparison_marks_human_conflicts(tmp_path: Path) -> None:
    scenario = load_scenario(SCENARIO_DIRECTORY / "variant_2.yaml")
    invalid = scenario.schedule_by_id["original_invalid_schedule"]
    assert len(_conflicting_human_phases(scenario, invalid)) == 5
    outputs = build_variant2_schedule_comparison(scenario, tmp_path / "gantt")
    assert all(path.is_file() and path.stat().st_size > 0 for path in outputs)


def test_resource_augmented_path_matches_selected_optimum(tmp_path: Path) -> None:
    outputs, length = build_resource_augmented_path(
        RESULT_DIRECTORY,
        tmp_path / "resource_path",
    )
    assert length == Decimal("36.45000")
    assert all(path.is_file() and path.stat().st_size > 0 for path in outputs)


def test_task_lever_map_preserves_expected_zero_agent_gain(tmp_path: Path) -> None:
    scenario = load_scenario(SCENARIO_DIRECTORY / "variant_4.yaml")
    outputs, rows, plus_agent_gain = build_task_lever_map(
        scenario,
        tmp_path / "lever_map",
        tmp_path / "lever_rows.csv",
    )
    assert plus_agent_gain == Decimal("0.00")
    assert any(row["deadline_reduction"] == "0.00" for row in rows)
    assert any(Decimal(row["deadline_reduction"]) > 0 for row in rows)
    assert all(path.is_file() and path.stat().st_size > 0 for path in outputs)


def test_probability_fan_small_reproducible_run(tmp_path: Path) -> None:
    outputs, rows = build_probabilistic_fan(
        PROJECT_ROOT,
        tmp_path / "fan",
        tmp_path / "fan.csv",
        sample_count=2,
    )
    assert len(rows) == 12
    assert {row["solver_status"] for row in rows} == {"OPTIMAL"}
    assert all(path.is_file() and path.stat().st_size > 0 for path in outputs)


def test_candidate_report_preserves_applied_decisions(tmp_path: Path) -> None:
    report = _write_candidate_report(
        tmp_path / "candidate_report.md",
        resource_path_length=Decimal("36.45"),
        plus_agent_gain=Decimal("0.00"),
        sample_count=100,
    )
    content = report.read_text(encoding="utf-8")
    assert "## Decision applied" in content
    assert "## Recommendation" not in content
    assert "included in the computational-results" in content
