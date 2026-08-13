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
import numpy as np


LAMBDA_VALUES = ("0", "0.5", "1")
OVERHEAD_RATES = ("0", "0.025", "0.05", "0.10", "0.20")
RATE_COLORS = {
    "0": "#222222",
    "0.025": "#0072B2",
    "0.05": "#009E73",
    "0.10": "#E69F00",
    "0.20": "#D55E00",
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


def build_decomposition_curves(
    curve_rows: list[dict[str, str]],
    output_stem: Path,
) -> tuple[Path, Path]:
    figure, axes = plt.subplots(1, 3, figsize=(18, 6), constrained_layout=True)
    for axis, lambda_h in zip(axes, LAMBDA_VALUES, strict=True):
        for overhead_rate in OVERHEAD_RATES:
            selected = sorted(
                [
                    row
                    for row in curve_rows
                    if row["curve_overhead_rate"] == overhead_rate
                    and row["curve_lambda_h"] == (
                        "shared" if overhead_rate == "0" else lambda_h
                    )
                ],
                key=lambda row: int(row["m"]),
            )
            if not selected:
                continue
            m_values = [int(row["m"]) for row in selected]
            exact_values = [float(row["T_star"]) for row in selected]
            bound_values = [float(row["B4"]) for row in selected]
            color = RATE_COLORS[overhead_rate]
            axis.plot(
                m_values,
                exact_values,
                color=color,
                marker="o",
                linewidth=2,
                label=rf"$r_o={overhead_rate}$",
            )
            axis.plot(
                m_values,
                bound_values,
                color=color,
                linestyle="--",
                linewidth=1.2,
                alpha=0.72,
            )
        axis.set_title(rf"Human overhead share $\lambda_h={lambda_h}$", fontweight="bold")
        axis.set_xlabel("Parallel subtasks, $m$")
        axis.set_ylabel("Makespan or bound, hours")
        axis.set_xticks([1, 2, 3, 4, 6, 8])
        axis.grid(color="#DDDDDD", linewidth=0.7)
        axis.set_axisbelow(True)
    axes[0].legend(frameon=False, ncol=2)
    figure.suptitle(
        r"EXP-04B decomposition: solid $T^*$, dashed $B_4$",
        fontsize=14,
        fontweight="bold",
    )
    return _save_figure(figure, output_stem)


def build_optimal_granularity_map(
    summaries: list[dict[str, str]],
    output_stem: Path,
) -> tuple[Path, Path]:
    positive_rates = OVERHEAD_RATES[1:]
    values = np.zeros((len(positive_rates), len(LAMBDA_VALUES)))
    labels: list[list[str]] = [
        ["" for _ in LAMBDA_VALUES] for _ in positive_rates
    ]
    by_key = {
        (row["overhead_rate"], row["lambda_h"]): row
        for row in summaries
        if row["overhead_rate"] != "0"
    }
    for row_index, overhead_rate in enumerate(positive_rates):
        for column_index, lambda_h in enumerate(LAMBDA_VALUES):
            row = by_key[(overhead_rate, lambda_h)]
            optimum = int(row["minimizing_m_T_star"])
            values[row_index, column_index] = optimum
            labels[row_index][column_index] = (
                f"m*={optimum}\nT*={float(row['minimum_T_star']):.2f}\n"
                f"U={'yes' if row['interior_U_shape_T_star'] == 'true' else 'no'}"
            )

    figure, axis = plt.subplots(figsize=(9, 6.5), constrained_layout=True)
    image = axis.imshow(values, cmap="viridis", vmin=1, vmax=8, aspect="auto")
    for row_index in range(values.shape[0]):
        for column_index in range(values.shape[1]):
            text_color = "white" if values[row_index, column_index] >= 4 else "black"
            axis.text(
                column_index,
                row_index,
                labels[row_index][column_index],
                ha="center",
                va="center",
                color=text_color,
                fontsize=10,
                fontweight="bold",
            )
    axis.set_xticks(range(len(LAMBDA_VALUES)), labels=LAMBDA_VALUES)
    axis.set_yticks(range(len(positive_rates)), labels=positive_rates)
    axis.set_xlabel(r"Human overhead share, $\lambda_h$")
    axis.set_ylabel(r"Overhead rate, $r_o$")
    axis.set_title(
        "EXP-04B: exact minimizing granularity on positive-overhead slices",
        fontweight="bold",
    )
    colorbar = figure.colorbar(image, ax=axis, ticks=[1, 2, 3, 4, 6, 8])
    colorbar.set_label(r"Minimizing $m$ for proven $T^*$")
    return _save_figure(figure, output_stem)
