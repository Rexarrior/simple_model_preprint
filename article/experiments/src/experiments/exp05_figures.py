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
from matplotlib.colors import BoundaryNorm, ListedColormap, TwoSlopeNorm
from matplotlib.patches import Patch
import numpy as np


P_VALUES = (1, 2, 3, 4, 6, 8)
M_VALUES = (1, 2, 3, 4, 6, 8)
REGIMES = (
    ("0", "shared"),
    ("0.05", "0"),
    ("0.05", "0.5"),
    ("0.10", "0"),
    ("0.10", "0.5"),
)
POSITIVE_REGIMES = REGIMES[1:]


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


def _selected(
    rows: list[dict[str, str]], overhead_rate: str, lambda_h: str
) -> list[dict[str, str]]:
    return [
        row
        for row in rows
        if row["analysis_overhead_rate"] == overhead_rate
        and row["analysis_lambda_h"] == lambda_h
    ]


def _matrix(
    rows: list[dict[str, str]], field: str
) -> np.ndarray:
    by_key = {(int(row["P"]), int(row["m"])): row for row in rows}
    values = np.full((len(P_VALUES), len(M_VALUES)), np.nan)
    for row_index, p in enumerate(P_VALUES):
        for column_index, m in enumerate(M_VALUES):
            value = by_key[(p, m)][field]
            if value:
                values[row_index, column_index] = float(value)
    return values


def _regime_title(overhead_rate: str, lambda_h: str) -> str:
    if overhead_rate == "0":
        return r"$r_o=0$ (shared $\lambda_h$)"
    return rf"$r_o={overhead_rate},\ \lambda_h={lambda_h}$"


def build_makespan_heatmaps(
    rows: list[dict[str, str]], output_stem: Path
) -> tuple[Path, Path]:
    matrices = [
        _matrix(_selected(rows, overhead_rate, lambda_h), "T_star")
        for overhead_rate, lambda_h in REGIMES
    ]
    finite = np.concatenate([matrix[np.isfinite(matrix)] for matrix in matrices])
    lower, upper = float(finite.min()), float(finite.max())
    figure, axes = plt.subplots(2, 3, figsize=(16, 10), constrained_layout=True)
    image = None
    for axis, matrix, (overhead_rate, lambda_h) in zip(
        axes.flat, matrices, REGIMES, strict=False
    ):
        image = axis.imshow(
            matrix,
            cmap="viridis",
            vmin=lower,
            vmax=upper,
            aspect="auto",
        )
        for row_index in range(matrix.shape[0]):
            for column_index in range(matrix.shape[1]):
                if not np.isfinite(matrix[row_index, column_index]):
                    label = "n/a"
                    color = "black"
                else:
                    label = f"{matrix[row_index, column_index]:.1f}"
                    midpoint = lower + (upper - lower) / 2
                    color = "white" if matrix[row_index, column_index] < midpoint else "black"
                axis.text(
                    column_index,
                    row_index,
                    label,
                    ha="center",
                    va="center",
                    fontsize=8.5,
                    color=color,
                )
        axis.set_xticks(range(len(M_VALUES)), labels=M_VALUES)
        axis.set_yticks(range(len(P_VALUES)), labels=P_VALUES)
        axis.set_xlabel("Parallel subtasks, $m$")
        axis.set_ylabel("Agent slots, $P$")
        axis.set_title(_regime_title(overhead_rate, lambda_h), fontweight="bold")
    axes.flat[-1].axis("off")
    assert image is not None
    colorbar = figure.colorbar(image, ax=list(axes.flat[:-1]), shrink=0.86)
    colorbar.set_label(r"Proven $T^*$, hours")
    figure.suptitle(
        r"EXP-05: exact makespan over parallelism and granularity",
        fontsize=15,
        fontweight="bold",
    )
    return _save_figure(figure, output_stem)


def build_interaction_contrast(
    rows: list[dict[str, str]], output_stem: Path
) -> tuple[Path, Path]:
    matrices = [
        _matrix(_selected(rows, overhead_rate, lambda_h), "interaction_contrast")
        for overhead_rate, lambda_h in POSITIVE_REGIMES
    ]
    finite = np.concatenate([matrix[np.isfinite(matrix)] for matrix in matrices])
    limit = max(abs(float(finite.min())), abs(float(finite.max())), 1e-9)
    norm = TwoSlopeNorm(vmin=-limit, vcenter=0, vmax=limit)
    figure, axes = plt.subplots(2, 2, figsize=(13, 10), constrained_layout=True)
    image = None
    for axis, matrix, (overhead_rate, lambda_h) in zip(
        axes.flat, matrices, POSITIVE_REGIMES, strict=True
    ):
        image = axis.imshow(matrix, cmap="RdBu_r", norm=norm, aspect="auto")
        for row_index in range(matrix.shape[0]):
            for column_index in range(matrix.shape[1]):
                value = matrix[row_index, column_index]
                label = "n/a" if not np.isfinite(value) else f"{value:+.2f}"
                color = "white" if np.isfinite(value) and abs(value) > limit * 0.55 else "black"
                axis.text(
                    column_index,
                    row_index,
                    label,
                    ha="center",
                    va="center",
                    fontsize=8.5,
                    color=color,
                )
        axis.set_xticks(range(len(M_VALUES)), labels=M_VALUES)
        axis.set_yticks(range(len(P_VALUES)), labels=P_VALUES)
        axis.set_xlabel("Parallel subtasks, $m$")
        axis.set_ylabel("Agent slots, $P$")
        axis.set_title(_regime_title(overhead_rate, lambda_h), fontweight="bold")
    assert image is not None
    colorbar = figure.colorbar(image, ax=list(axes.flat), shrink=0.88)
    colorbar.set_label(r"Interaction contrast $I(P,m)$, hours")
    figure.suptitle(
        "EXP-05: interaction of agent parallelism and decomposition",
        fontsize=15,
        fontweight="bold",
    )
    return _save_figure(figure, output_stem)


_BRANCH_CODES = {
    "work": "W",
    "critical_path": "L",
    "human": "H",
}
_CATEGORIES = ("W", "L", "H", "W+L", "W+H", "L+H", "W+L+H")
_COLORS = ("#0072B2", "#E69F00", "#CC79A7", "#56B4E9", "#009E73", "#D55E00", "#666666")


def _branch_label(raw: str) -> str:
    present = set(raw.split(",")) if raw else set()
    return "+".join(
        _BRANCH_CODES[name]
        for name in ("work", "critical_path", "human")
        if name in present
    )


def build_active_constraint_maps(
    rows: list[dict[str, str]], output_stem: Path
) -> tuple[Path, Path]:
    cmap = ListedColormap(_COLORS)
    norm = BoundaryNorm(np.arange(-0.5, len(_CATEGORIES) + 0.5), cmap.N)
    figure, axes = plt.subplots(2, 3, figsize=(16, 10), constrained_layout=True)
    for axis, (overhead_rate, lambda_h) in zip(axes.flat, REGIMES, strict=False):
        selected = _selected(rows, overhead_rate, lambda_h)
        by_key = {(int(row["P"]), int(row["m"])): row for row in selected}
        values = np.zeros((len(P_VALUES), len(M_VALUES)))
        labels: list[list[str]] = [["" for _ in M_VALUES] for _ in P_VALUES]
        for row_index, p in enumerate(P_VALUES):
            for column_index, m in enumerate(M_VALUES):
                label = _branch_label(by_key[(p, m)]["active_branches"])
                values[row_index, column_index] = _CATEGORIES.index(label)
                labels[row_index][column_index] = label
        axis.imshow(values, cmap=cmap, norm=norm, aspect="auto")
        for row_index in range(values.shape[0]):
            for column_index in range(values.shape[1]):
                axis.text(
                    column_index,
                    row_index,
                    labels[row_index][column_index],
                    ha="center",
                    va="center",
                    fontsize=9,
                    fontweight="bold",
                    color="white" if values[row_index, column_index] in {0, 2, 5, 6} else "black",
                )
        axis.set_xticks(range(len(M_VALUES)), labels=M_VALUES)
        axis.set_yticks(range(len(P_VALUES)), labels=P_VALUES)
        axis.set_xlabel("Parallel subtasks, $m$")
        axis.set_ylabel("Agent slots, $P$")
        axis.set_title(_regime_title(overhead_rate, lambda_h), fontweight="bold")
    axes.flat[-1].axis("off")
    legend = [
        Patch(facecolor=color, label=label)
        for label, color in zip(_CATEGORIES, _COLORS, strict=True)
    ]
    axes.flat[-1].legend(
        handles=legend,
        title=r"Active branches of $B_4$",
        loc="center",
        frameon=False,
        ncol=2,
    )
    figure.suptitle(
        r"EXP-05: active lower-bound constraints ($W$, $L$, $H$)",
        fontsize=15,
        fontweight="bold",
    )
    return _save_figure(figure, output_stem)
