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


OBJECT_ORDER = ("practical_v4", "fork_join_n4")
OBJECT_LABELS = {
    "practical_v4": "Practical variant 4 structure",
    "fork_join_n4": "Canonical fork–join, N=4",
}
REGIME_ORDER = (
    "c0_g0_rh10",
    "c0_g0_rh25",
    "c0_g0_rh50",
    "c1_g0_rh25",
    "c0_g1_rh25",
)
REGIME_LABELS = {
    "c0_g0_rh10": r"$C_0,\gamma_0,r_h=0.10$",
    "c0_g0_rh25": r"$C_0,\gamma_0,r_h=0.25$",
    "c0_g0_rh50": r"$C_0,\gamma_0,r_h=0.50$",
    "c1_g0_rh25": r"$C_1,\gamma_0,r_h=0.25$",
    "c0_g1_rh25": r"$C_0,\gamma_1,r_h=0.25$",
}
BRANCH_COLORS = {
    "work": "#56B4E9",
    "critical_path": "#009E73",
    "human": "#E69F00",
    "tie": "#CC79A7",
}


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


def _ordered(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return sorted(rows, key=lambda row: int(row["agent_count"]))


def build_scaling_curve(
    rows: list[dict[str, str]],
    output_stem: Path,
) -> tuple[Path, Path]:
    figure, axes = plt.subplots(1, 2, figsize=(15, 6.2), constrained_layout=True)
    for axis, object_id in zip(axes, OBJECT_ORDER, strict=True):
        selected = _ordered(
            [
                row
                for row in rows
                if row["object_id"] == object_id
                and row["regime_id"] == "c0_g0_rh25"
            ]
        )
        p_values = [int(row["agent_count"]) for row in selected]
        exact_label = (
            r"$T^*$"
            if all(row["solver_status"] == "OPTIMAL" for row in selected)
            else "Exact incumbent"
        )
        series = (
            ("W4_over_P", r"$W_4/P$", "#56B4E9", "--", "o", 1.5),
            ("L4", r"$L_4$", "#009E73", "--", "s", 1.5),
            ("gamma_H", r"$\gamma H$", "#E69F00", "--", "^", 1.5),
            ("B4", r"$B_4$", "#222222", "-", "", 2.4),
            ("exact_makespan", exact_label, "#CC79A7", "-", "D", 2.2),
            (
                "baseline_makespan",
                r"$T(\pi_{base})$",
                "#777777",
                ":",
                "x",
                1.8,
            ),
        )
        for field, label, color, linestyle, marker, width in series:
            values = [float(row[field]) for row in selected]
            axis.plot(
                p_values,
                values,
                label=label,
                color=color,
                linestyle=linestyle,
                marker=marker,
                linewidth=width,
                markersize=5.5,
            )
        axis.set_title(OBJECT_LABELS[object_id], fontweight="bold")
        axis.set_xlabel("Agent slots, $P$")
        axis.set_ylabel("Makespan or bound, hours")
        axis.set_xticks(p_values)
        axis.grid(color="#DDDDDD", linewidth=0.7)
        axis.set_axisbelow(True)
    axes[0].legend(frameon=False, ncol=2, loc="best")
    figure.suptitle(
        r"EXP-02 clean scaling slice: $C_0,\gamma_0,r_h=0.25$",
        fontsize=14,
        fontweight="bold",
    )
    return _save_figure(figure, output_stem)


def _branch_color(active_branches: str) -> str:
    branches = [item for item in active_branches.split(",") if item]
    if len(branches) != 1:
        return BRANCH_COLORS["tie"]
    return BRANCH_COLORS[branches[0]]


def build_active_constraint_map(
    rows: list[dict[str, str]],
    output_stem: Path,
) -> tuple[Path, Path]:
    figure, axes = plt.subplots(
        len(REGIME_ORDER),
        len(OBJECT_ORDER),
        figsize=(15, 16),
        sharex="col",
        constrained_layout=True,
    )
    for row_index, regime_id in enumerate(REGIME_ORDER):
        for column_index, object_id in enumerate(OBJECT_ORDER):
            axis = axes[row_index][column_index]
            selected = _ordered(
                [
                    row
                    for row in rows
                    if row["object_id"] == object_id
                    and row["regime_id"] == regime_id
                ]
            )
            positions = list(range(len(selected)))
            p_values = [int(row["agent_count"]) for row in selected]
            for position, row in zip(positions, selected, strict=True):
                axis.axvspan(
                    position - 0.5,
                    position + 0.5,
                    color=_branch_color(row["active_branches"]),
                    alpha=0.15,
                    linewidth=0,
                )
            exact_label = (
                r"$T^*$"
                if all(row["solver_status"] == "OPTIMAL" for row in selected)
                else "Exact incumbent"
            )
            axis.plot(
                positions,
                [float(row["exact_makespan"]) for row in selected],
                color="#CC79A7",
                marker="D",
                linewidth=2,
                markersize=4.5,
                label=exact_label,
            )
            axis.plot(
                positions,
                [float(row["baseline_makespan"]) for row in selected],
                color="#666666",
                linestyle=":",
                marker="x",
                linewidth=1.5,
                markersize=4.5,
                label=r"$T(\pi_{base})$",
            )
            axis.plot(
                positions,
                [float(row["B4"]) for row in selected],
                color="#222222",
                linewidth=1.8,
                label=r"$B_4$",
            )
            if row_index == 0:
                axis.set_title(OBJECT_LABELS[object_id], fontweight="bold")
            if column_index == 0:
                axis.set_ylabel(REGIME_LABELS[regime_id] + "\nHours")
            axis.set_xticks(positions, labels=p_values)
            axis.grid(axis="y", color="#DDDDDD", linewidth=0.6)
            axis.set_axisbelow(True)
    for axis in axes[-1]:
        axis.set_xlabel("Agent slots, $P$")

    handles = [
        Line2D([], [], color="#CC79A7", marker="D", label=r"$T^*$ / incumbent"),
        Line2D([], [], color="#666666", linestyle=":", marker="x", label="Baseline"),
        Line2D([], [], color="#222222", label=r"$B_4$"),
        Patch(facecolor=BRANCH_COLORS["work"], alpha=0.3, label=r"active $W_4/P$"),
        Patch(
            facecolor=BRANCH_COLORS["critical_path"],
            alpha=0.3,
            label=r"active $L_4$",
        ),
        Patch(facecolor=BRANCH_COLORS["human"], alpha=0.3, label=r"active $\gamma H$"),
        Patch(facecolor=BRANCH_COLORS["tie"], alpha=0.3, label="active-branch tie"),
    ]
    figure.legend(
        handles=handles,
        loc="outside lower center",
        ncol=4,
        frameon=False,
    )
    figure.suptitle(
        "EXP-02: active lower-bound branch and achieved makespan",
        fontsize=14,
        fontweight="bold",
    )
    return _save_figure(figure, output_stem)
