from __future__ import annotations

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
from matplotlib.lines import Line2D
from matplotlib.patches import Patch


PROFILE_ORDER = ("front_loaded", "alternating_sync", "alternating_staggered")
PROFILE_STYLE = {
    "front_loaded": ("#0072B2", "o", "Front-loaded"),
    "alternating_sync": ("#D55E00", "s", "Alternating sync"),
    "alternating_staggered": ("#009E73", "^", "Alternating staggered"),
}


def _float_or_nan(value: str) -> float:
    return float(value) if value else float("nan")


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


def build_profile_effects(
    pairs: list[dict[str, str]],
    output_stem: Path,
) -> tuple[Path, Path]:
    categories = sorted(
        {
            (row["topology"], row["agent_count"], row["human_share"])
            for row in pairs
        }
    )
    labels = [
        f"{topology.replace('_', '–')}\nP={p}, $r_h$={share}"
        for topology, p, share in categories
    ]
    offsets = {
        "front_loaded": -0.20,
        "alternating_sync": 0.0,
        "alternating_staggered": 0.20,
    }
    panels = (
        ("delta_T_star_to_IO", r"$\Delta T^*$, hours", "Exact makespan"),
        ("delta_exact_queue_to_IO", r"$\Delta Q$, agent-hours", "Exact queue"),
        (
            "delta_exact_full_agent_stop_to_IO",
            "Change in full-stop time, hours",
            "All agent slots stopped",
        ),
    )
    figure, axes = plt.subplots(1, 3, figsize=(18, 6.5), constrained_layout=True)
    for axis, (field, ylabel, title) in zip(axes, panels, strict=True):
        for profile in PROFILE_ORDER:
            color, marker, profile_label = PROFILE_STYLE[profile]
            selected = {
                (row["topology"], row["agent_count"], row["human_share"]): row
                for row in pairs
                if row["phase_profile"] == profile
            }
            x_values = [index + offsets[profile] for index in range(len(categories))]
            y_values = [_float_or_nan(selected[category][field]) for category in categories]
            axis.scatter(
                x_values,
                y_values,
                color=color,
                marker=marker,
                s=42,
                label=profile_label,
                zorder=3,
            )
        axis.axhline(0, color="#555555", linewidth=1)
        axis.set_title(title, fontweight="bold")
        axis.set_ylabel(ylabel)
        axis.set_xticks(range(len(categories)), labels=labels, rotation=28, ha="right")
        axis.grid(axis="y", color="#DDDDDD", linewidth=0.7)
        axis.set_axisbelow(True)
    axes[0].legend(frameon=False)
    figure.suptitle(
        "EXP-03: paired phase-profile effects relative to IO",
        fontsize=14,
        fontweight="bold",
    )
    return _save_figure(figure, output_stem)


def _timeline_rows(
    events: list[dict[str, str]],
    scenario_id: str,
) -> list[dict[str, str]]:
    return sorted(
        [
            row
            for row in events
            if row["scenario_id"] == scenario_id
            and row["schedule_kind"] == "exact"
        ],
        key=lambda row: float(row["start"]),
    )


def build_queue_timeline(
    pairs: list[dict[str, str]],
    events: list[dict[str, str]],
    selected_pair_id: str,
    output_stem: Path,
) -> tuple[Path, Path]:
    pair = next(row for row in pairs if row["pair_id"] == selected_pair_id)
    scenario_specs = (
        (pair["io_scenario_id"], "IO reference"),
        (pair["profile_scenario_id"], pair["phase_profile"].replace("_", " ").title()),
    )
    figure, axes = plt.subplots(2, 1, figsize=(15, 8.5), constrained_layout=True)
    for axis, (scenario_id, label) in zip(axes, scenario_specs, strict=True):
        selected = _timeline_rows(events, scenario_id)
        if not selected:
            raise ValueError(f"no exact timeline events for {scenario_id}")
        starts = [float(row["start"]) for row in selected]
        ends = [float(row["end"]) for row in selected]
        queue = [int(row["human_queue_length"]) for row in selected]
        active_agents = [int(row["active_agent_phases"]) for row in selected]
        edges = [starts[0], *ends]
        axis.stairs(
            queue,
            edges,
            color="#D55E00",
            linewidth=2,
            label="Waiting for human",
        )
        axis.stairs(
            active_agents,
            edges,
            color="#0072B2",
            linewidth=1.8,
            label="Active agent phases",
        )
        for row in selected:
            if row["full_agent_stop"] != "true":
                continue
            axis.axvspan(
                float(row["start"]),
                float(row["end"]),
                color="#CC79A7",
                alpha=0.22,
                linewidth=0,
            )
        axis.set_title(f"{label}: {scenario_id}", fontweight="bold")
        axis.set_ylabel("Tasks / slots")
        axis.set_ylim(-0.1, int(pair["agent_count"]) + 0.5)
        axis.set_yticks(range(int(pair["agent_count"]) + 1))
        axis.grid(color="#DDDDDD", linewidth=0.7)
        axis.set_axisbelow(True)
    axes[-1].set_xlabel("Time, hours")
    axes[0].legend(
        handles=[
            Line2D([], [], color="#D55E00", linewidth=2, label="Waiting for human"),
            Line2D([], [], color="#0072B2", linewidth=2, label="Active agent phases"),
            Patch(
                facecolor="#CC79A7",
                alpha=0.3,
                label="All occupied slots have no active agent phase",
            ),
        ],
        frameon=False,
        ncol=3,
    )
    figure.suptitle(
        "EXP-03 selected same-bound pair: queue and full-agent-stop intervals\n"
        rf"$B_4={pair['B4']}$ h; $\Delta T^*={pair['delta_T_star_to_IO']}$ h",
        fontsize=14,
        fontweight="bold",
    )
    return _save_figure(figure, output_stem)
