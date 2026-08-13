from __future__ import annotations

from decimal import Decimal
import os
from pathlib import Path
from statistics import median
import tempfile

_matplotlib_cache = Path(tempfile.gettempdir()) / "simple-model-experiments-mpl"
_matplotlib_cache.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(_matplotlib_cache))

import matplotlib

matplotlib.use("Agg")
matplotlib.rcParams["svg.hashsalt"] = "simple-model-full-experiments-v1"

import matplotlib.pyplot as plt
from matplotlib.patches import Patch

from .bounds import compute_aggregates
from .schema import Scenario, ScheduleSpec
from .validator import validate_schedule

TOPOLOGIES = ("chain", "independent", "fork_join", "diamond", "two_layer")
PROFILE_STYLE = {
    "io": ("#0072B2", "o", "IO"),
    "alternating_sync": ("#D55E00", "s", "Alternating sync"),
    "alternating_staggered": ("#009E73", "^", "Alternating staggered"),
}
AGENT_COLOR = "#0072B2"
HUMAN_COLOR = "#D55E00"
WAIT_COLOR = "#999999"


def _save_figure(figure: plt.Figure, output_stem: Path) -> tuple[Path, Path]:
    output_stem.parent.mkdir(parents=True, exist_ok=True)
    svg = output_stem.with_suffix(".svg")
    png = output_stem.with_suffix(".png")
    figure.savefig(svg, bbox_inches="tight", metadata={"Date": None})
    svg.write_text(
        "\n".join(
            line.rstrip()
            for line in svg.read_text(encoding="utf-8").splitlines()
        )
        + "\n",
        encoding="utf-8",
    )
    figure.savefig(png, dpi=180, bbox_inches="tight")
    plt.close(figure)
    return svg, png


def build_exp01_gap_figure(
    rows: list[dict[str, str]],
    output_stem: Path,
) -> tuple[Path, Path]:
    figure, axes = plt.subplots(1, 2, figsize=(14, 5.8), constrained_layout=True)
    profile_offsets = {
        "io": -0.22,
        "alternating_sync": 0.0,
        "alternating_staggered": 0.22,
    }
    for profile, (color, marker, label) in PROFILE_STYLE.items():
        profile_rows = [row for row in rows if row["phase_profile"] == profile]
        for topology_index, topology in enumerate(TOPOLOGIES):
            selected = [row for row in profile_rows if row["topology"] == topology]
            x_values: list[float] = []
            tightness_values: list[float] = []
            heuristic_values: list[float] = []
            for row in selected:
                task_component = {"4": -0.035, "8": 0.0, "12": 0.035}[
                    row["task_count"]
                ]
                p_component = -0.012 if row["agent_count"] == "2" else 0.012
                x_values.append(
                    topology_index
                    + profile_offsets[profile]
                    + task_component
                    + p_component
                )
                tightness_values.append(float(row["tightness_relative_gap"]) * 100)
                heuristic_values.append(float(row["baseline_relative_gap"]) * 100)
            axes[0].scatter(
                x_values,
                tightness_values,
                s=24,
                alpha=0.42,
                color=color,
                marker=marker,
                edgecolors="none",
                label=label if topology_index == 0 else None,
            )
            axes[1].scatter(
                x_values,
                heuristic_values,
                s=24,
                alpha=0.42,
                color=color,
                marker=marker,
                edgecolors="none",
                label=label if topology_index == 0 else None,
            )
            if selected:
                center = topology_index + profile_offsets[profile]
                axes[0].plot(
                    [center - 0.07, center + 0.07],
                    [median(tightness_values)] * 2,
                    color=color,
                    linewidth=3,
                )
                axes[1].plot(
                    [center - 0.07, center + 0.07],
                    [median(heuristic_values)] * 2,
                    color=color,
                    linewidth=3,
                )

    titles = (
        "Lower-bound tightness gap\n$100(T^*/B_4-1)$",
        "Baseline heuristic gap\n$100(T(\\pi_{base})/T^*-1)$",
    )
    labels = ("Gap to $B_4$, %", "Gap to optimum, %")
    tick_labels = ("Chain", "Independent", "Fork–join", "Diamond", "Two-layer")
    for axis, title, ylabel in zip(axes, titles, labels, strict=True):
        axis.axhline(0, color="#555555", linewidth=1)
        axis.set_title(title, fontsize=12, fontweight="bold")
        axis.set_ylabel(ylabel)
        axis.set_xticks(range(len(TOPOLOGIES)), labels=tick_labels, rotation=18)
        axis.grid(axis="y", color="#DDDDDD", linewidth=0.7)
        axis.set_axisbelow(True)
    axes[0].legend(loc="upper left", frameon=False)
    figure.suptitle(
        "EXP-01: structural bound and scheduling policy are separate effects",
        fontsize=14,
        fontweight="bold",
    )
    return _save_figure(figure, output_stem)


def _wait_intervals(
    scenario: Scenario,
    schedule: ScheduleSpec,
) -> list[tuple[str, int, Decimal, Decimal]]:
    by_key = {
        (interval.task_id, interval.phase_id): interval
        for interval in schedule.phases
    }
    assignments = {
        assignment.task_id: assignment for assignment in schedule.assignments
    }
    waits: list[tuple[str, int, Decimal, Decimal]] = []
    for task in scenario.tasks:
        intervals = [by_key[(task.task_id, phase.phase_id)] for phase in task.phases]
        assignment = assignments[task.task_id]
        if task.phases[0].resource == "human" and intervals[0].start > assignment.assigned_at:
            waits.append(
                (task.task_id, assignment.agent, assignment.assigned_at, intervals[0].start)
            )
        for index in range(1, len(task.phases)):
            current_phase = task.phases[index]
            previous = intervals[index - 1]
            current = intervals[index]
            if current_phase.resource == "human" and current.start > previous.end:
                waits.append((task.task_id, current.agent, previous.end, current.start))
    return waits


def build_counterexample_gantt(
    scenario: Scenario,
    schedule: ScheduleSpec,
    output_stem: Path,
) -> tuple[Path, Path]:
    validation = validate_schedule(scenario, schedule)
    if not validation.valid or validation.metrics is None:
        details = "; ".join(issue.message for issue in validation.issues)
        raise ValueError(f"cannot plot invalid counterexample schedule: {details}")
    aggregate = compute_aggregates(scenario)
    makespan = validation.metrics.makespan
    height = 0.64
    figure_height = max(4.8, 1.0 + 0.85 * (scenario.p + 1))
    figure, axis = plt.subplots(
        figsize=(14, figure_height),
        constrained_layout=True,
    )
    phase_by_key = {
        (task.task_id, phase.phase_id): phase
        for task in scenario.tasks
        for phase in task.phases
    }

    for interval in schedule.phases:
        phase = phase_by_key[(interval.task_id, interval.phase_id)]
        color = HUMAN_COLOR if phase.resource == "human" else AGENT_COLOR
        start = float(interval.start)
        duration = float(interval.end - interval.start)
        y = float(interval.agent)
        axis.broken_barh(
            [(start, duration)],
            (y - height / 2, height),
            facecolors=color,
            edgecolors="white",
            linewidth=0.6,
            zorder=3,
        )
        if duration >= max(0.7, float(makespan) / 45):
            axis.text(
                start + duration / 2,
                y,
                interval.task_id,
                ha="center",
                va="center",
                color="white",
                fontsize=7.5,
                fontweight="bold",
                zorder=4,
            )

    for task_id, agent, start_value, end_value in _wait_intervals(scenario, schedule):
        start = float(start_value)
        duration = float(end_value - start_value)
        axis.broken_barh(
            [(start, duration)],
            (agent - height / 2, height),
            facecolors="none",
            edgecolors=WAIT_COLOR,
            hatch="////",
            linewidth=0.8,
            zorder=2,
        )

    for interval in schedule.phases:
        phase = phase_by_key[(interval.task_id, interval.phase_id)]
        if phase.resource != "human":
            continue
        start = float(interval.start)
        duration = float(interval.end - interval.start)
        axis.broken_barh(
            [(start, duration)],
            (-height / 2, height),
            facecolors=HUMAN_COLOR,
            edgecolors="white",
            linewidth=0.6,
            zorder=3,
        )
        if duration >= max(0.7, float(makespan) / 45):
            axis.text(
                start + duration / 2,
                0,
                interval.task_id,
                ha="center",
                va="center",
                color="white",
                fontsize=7.5,
                fontweight="bold",
                zorder=4,
            )

    axis.axvline(float(aggregate.b4), color="#CC79A7", linestyle="--", linewidth=2)
    axis.text(
        float(aggregate.b4),
        scenario.p + 0.55,
        f"$B_4={aggregate.b4:g}$",
        ha="right",
        va="bottom",
        color="#9B4F82",
        fontsize=9,
    )
    axis.set_yticks(
        list(range(0, scenario.p + 1)),
        labels=["Human"] + [f"Agent {agent}" for agent in range(1, scenario.p + 1)],
    )
    axis.set_xlim(0, float(makespan) * 1.03)
    axis.set_ylim(-0.7, scenario.p + 0.8)
    axis.set_xlabel("Time, hours")
    axis.grid(axis="x", color="#DDDDDD", linewidth=0.7)
    axis.set_axisbelow(True)
    axis.set_title(
        f"Minimal EXP-01 counterexample: {scenario.scenario_id}\n"
        f"$B_4={aggregate.b4:g}$ h, $T^*={makespan:g}$ h, "
        f"$Q={validation.metrics.queue_time:g}$ h",
        fontsize=12,
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
                label="Waiting; agent slot retained",
            ),
            Patch(facecolor="#CC79A7", label="$B_4$"),
        ],
        loc="upper center",
        bbox_to_anchor=(0.5, -0.14),
        ncol=4,
        frameon=False,
    )
    return _save_figure(figure, output_stem)
