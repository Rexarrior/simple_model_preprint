from __future__ import annotations

from decimal import Decimal
import os
from pathlib import Path
import tempfile

_matplotlib_cache = Path(tempfile.gettempdir()) / "simple-model-experiments-mpl"
_matplotlib_cache.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(_matplotlib_cache))

import matplotlib

matplotlib.use("Agg")
matplotlib.rcParams["svg.hashsalt"] = "simple-model-full-experiments-v1"

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Patch

from .bounds import compute_aggregates
from .schema import PhaseInterval, Scenario, ScheduleSpec, load_scenario
from .validator import validate_schedule

AGENT_COLOR = "#0072B2"
HUMAN_COLOR = "#D55E00"
WAIT_COLOR = "#999999"
CRITICAL_COLOR = "#0072B2"
OTHER_COLOR = "#777777"


def _normalize_svg(path: Path) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    path.write_text(
        "\n".join(line.rstrip() for line in lines) + "\n",
        encoding="utf-8",
    )


def _task_weight(scenario: Scenario, task_id: str) -> Decimal:
    task = scenario.task_by_id[task_id]
    return scenario.x * task.z * (
        scenario.c * task.a + scenario.gamma * task.h
    )


def _draw_dag(
    axis: plt.Axes,
    scenario: Scenario,
    positions: dict[str, tuple[float, float]],
    *,
    title: str,
) -> None:
    metrics = compute_aggregates(scenario)
    critical_edges = set(
        zip(
            metrics.critical_path_l4[:-1],
            metrics.critical_path_l4[1:],
            strict=True,
        )
    )
    for task in scenario.tasks:
        target = positions[task.task_id]
        for predecessor in task.predecessors:
            source = positions[predecessor]
            critical = (predecessor, task.task_id) in critical_edges
            arrow = FancyArrowPatch(
                source,
                target,
                arrowstyle="-|>",
                mutation_scale=12,
                linewidth=2.4 if critical else 1.2,
                color=CRITICAL_COLOR if critical else "#BBBBBB",
                shrinkA=23,
                shrinkB=23,
                zorder=1,
            )
            axis.add_patch(arrow)

    critical_nodes = set(metrics.critical_path_l4)
    for task_id, (x, y) in positions.items():
        critical = task_id in critical_nodes
        axis.scatter(
            [x],
            [y],
            s=1450,
            facecolor="#DDEEFF" if critical else "#F2F2F2",
            edgecolor=CRITICAL_COLOR if critical else OTHER_COLOR,
            linewidth=2.4 if critical else 1.2,
            zorder=2,
        )
        weight = _task_weight(scenario, task_id)
        axis.text(
            x,
            y,
            f"{task_id}\n{weight:g} h",
            ha="center",
            va="center",
            fontsize=9,
            zorder=3,
        )

    axis.set_title(
        f"{title}\n$L_4={metrics.l4:g}$ h",
        fontsize=12,
        fontweight="bold",
    )
    axis.set_xlim(-0.6, 4.6)
    axis.set_ylim(-0.8, 3.8)
    axis.set_aspect("equal")
    axis.axis("off")


def build_dag_comparison(
    scenario_3: Scenario,
    scenario_4: Scenario,
    output_stem: Path,
) -> tuple[Path, Path]:
    figure, axes = plt.subplots(1, 2, figsize=(12, 5.2), constrained_layout=True)
    positions_3 = {
        "1": (0, 2),
        "2": (1, 2),
        "3": (2, 2),
        "4": (3, 2),
        "6": (4, 2),
        "5": (1, 0),
        "7": (2.5, 0),
    }
    positions_4 = {
        "1": (0, 2),
        "2": (1, 2),
        "3": (2, 2),
        "4": (3, 2),
        "6c": (4, 2),
        "5": (1, 0),
        "7": (2.5, 0),
        "6b": (2, 3.25),
        "6a": (3.1, 3.25),
    }
    _draw_dag(axes[0], scenario_3, positions_3, title="Variant 3: coarse tests")
    _draw_dag(axes[1], scenario_4, positions_4, title="Variant 4: decomposed tests")
    figure.suptitle(
        "Critical path before and after decomposition",
        fontsize=14,
        fontweight="bold",
    )
    output_stem.parent.mkdir(parents=True, exist_ok=True)
    svg = output_stem.with_suffix(".svg")
    png = output_stem.with_suffix(".png")
    figure.savefig(svg, bbox_inches="tight", metadata={"Date": None})
    _normalize_svg(svg)
    figure.savefig(png, dpi=180, bbox_inches="tight")
    plt.close(figure)
    return svg, png


def _wait_intervals(
    scenario: Scenario,
    schedule: ScheduleSpec,
) -> list[tuple[str, int, Decimal, Decimal]]:
    by_key = {
        (interval.task_id, interval.phase_id): interval
        for interval in schedule.phases
    }
    waits: list[tuple[str, int, Decimal, Decimal]] = []
    assignments = {
        assignment.task_id: assignment for assignment in schedule.assignments
    }
    for task in scenario.tasks:
        intervals = [by_key[(task.task_id, phase.phase_id)] for phase in task.phases]
        assignment = assignments.get(task.task_id)
        if (
            assignment is not None
            and task.phases[0].resource == "human"
            and intervals[0].start > assignment.assigned_at
        ):
            waits.append(
                (
                    task.task_id,
                    assignment.agent,
                    assignment.assigned_at,
                    intervals[0].start,
                )
            )
        for index in range(1, len(task.phases)):
            phase = task.phases[index]
            previous = intervals[index - 1]
            current = intervals[index]
            if phase.resource == "human" and current.start > previous.end:
                waits.append(
                    (task.task_id, current.agent, previous.end, current.start)
                )
    return waits


def _float(value: Decimal) -> float:
    return float(value)


def build_variant_2_gantt(
    scenario: Scenario,
    schedule: ScheduleSpec,
    output_stem: Path,
) -> tuple[Path, Path]:
    validation = validate_schedule(scenario, schedule)
    if not validation.valid or validation.metrics is None:
        details = "; ".join(issue.message for issue in validation.issues)
        raise ValueError(f"cannot plot invalid schedule: {details}")
    metrics = validation.metrics
    figure, axis = plt.subplots(figsize=(13, 5.5), constrained_layout=True)
    lane_y = {1: 2.0, 2: 1.0}
    height = 0.62
    phase_by_key = {
        (task.task_id, phase.phase_id): phase
        for task in scenario.tasks
        for phase in task.phases
    }

    for interval in schedule.phases:
        phase = phase_by_key[(interval.task_id, interval.phase_id)]
        color = HUMAN_COLOR if phase.resource == "human" else AGENT_COLOR
        start = _float(interval.start)
        duration = _float(interval.end - interval.start)
        y = lane_y[interval.agent]
        axis.broken_barh(
            [(start, duration)],
            (y - height / 2, height),
            facecolors=color,
            edgecolors="white",
            linewidth=0.8,
            zorder=3,
        )
        if duration >= 0.7:
            axis.text(
                start + duration / 2,
                y,
                interval.task_id,
                ha="center",
                va="center",
                color="white",
                fontsize=8,
                fontweight="bold",
                zorder=4,
            )

    waits = _wait_intervals(scenario, schedule)
    for task_id, agent, start_value, end_value in waits:
        start = _float(start_value)
        duration = _float(end_value - start_value)
        y = lane_y[agent]
        axis.broken_barh(
            [(start, duration)],
            (y - height / 2, height),
            facecolors="none",
            edgecolors=WAIT_COLOR,
            hatch="////",
            linewidth=1.0,
            zorder=2,
        )
        axis.text(
            start + duration / 2,
            y,
            f"queue {task_id}",
            ha="center",
            va="center",
            color="#444444",
            fontsize=8,
            zorder=4,
        )

    human_y = 0.0
    for interval in schedule.phases:
        phase = phase_by_key[(interval.task_id, interval.phase_id)]
        if phase.resource != "human":
            continue
        start = _float(interval.start)
        duration = _float(interval.end - interval.start)
        axis.broken_barh(
            [(start, duration)],
            (human_y - height / 2, height),
            facecolors=HUMAN_COLOR,
            edgecolors="white",
            linewidth=0.8,
            zorder=3,
        )
        if duration >= 0.7:
            axis.text(
                start + duration / 2,
                human_y,
                interval.task_id,
                ha="center",
                va="center",
                color="white",
                fontsize=8,
                fontweight="bold",
                zorder=4,
            )

    axis.set_yticks([0, 1, 2], labels=["Human", "Agent 2", "Agent 1"])
    axis.set_xlabel("Time, hours")
    axis.set_xlim(0, _float(metrics.makespan) + 0.7)
    axis.set_ylim(-0.65, 2.65)
    axis.grid(axis="x", color="#DDDDDD", linewidth=0.7)
    axis.set_axisbelow(True)
    axis.set_title(
        "Variant 2: feasible M4 schedule with local blocking\n"
        f"$T(\\pi_2)={metrics.makespan:g}$ h, "
        f"$Q(\\pi_2)={metrics.queue_time:g}$ h",
        fontsize=13,
        fontweight="bold",
    )
    axis.legend(
        handles=[
            Patch(facecolor=AGENT_COLOR, label="Agent phase"),
            Patch(facecolor=HUMAN_COLOR, label="Human phase"),
            Patch(
                facecolor="white",
                edgecolor=WAIT_COLOR,
                hatch="////",
                label="Waiting for human; slot retained",
            ),
        ],
        loc="upper center",
        bbox_to_anchor=(0.5, -0.16),
        ncol=3,
        frameon=False,
    )
    output_stem.parent.mkdir(parents=True, exist_ok=True)
    svg = output_stem.with_suffix(".svg")
    png = output_stem.with_suffix(".png")
    figure.savefig(svg, bbox_inches="tight", metadata={"Date": None})
    _normalize_svg(svg)
    figure.savefig(png, dpi=180, bbox_inches="tight")
    plt.close(figure)
    return svg, png


def build_main_figures(
    scenario_directory: Path,
    output_directory: Path,
) -> tuple[Path, ...]:
    scenario_2 = load_scenario(scenario_directory / "variant_2.yaml")
    scenario_3 = load_scenario(scenario_directory / "variant_3.yaml")
    scenario_4 = load_scenario(scenario_directory / "variant_4.yaml")
    outputs: list[Path] = []
    outputs.extend(
        build_dag_comparison(
            scenario_3,
            scenario_4,
            output_directory / "exp00_dag_variants_3_4",
        )
    )
    outputs.extend(
        build_variant_2_gantt(
            scenario_2,
            scenario_2.schedule_by_id["article_schedule"],
            output_directory / "exp00_gantt_variant_2",
        )
    )
    return tuple(outputs)
