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


COLORS = {
    "practical_variant_3": "#0072B2",
    "practical_variant_4": "#D55E00",
    "canonical_m1": "#009E73",
    "canonical_m3_mixed_overhead": "#CC79A7",
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


def build_scale_invariance(
    rows: list[dict[str, str]], output_stem: Path
) -> tuple[Path, Path]:
    figure, axes = plt.subplots(1, 2, figsize=(14, 5.5), constrained_layout=True)
    object_ids = tuple(dict.fromkeys(row["object_id"] for row in rows))
    for object_id in object_ids:
        selected = sorted(
            [row for row in rows if row["object_id"] == object_id],
            key=lambda row: float(row["kappa"]),
        )
        kappa = [float(row["kappa"]) for row in selected]
        reference = next(row for row in selected if row["kappa"] == "1")
        color = COLORS[object_id]
        exact_ratio = [float(row["T_star"]) / float(reference["T_star"]) for row in selected]
        baseline_ratio = [
            float(row["baseline_makespan"]) / float(reference["baseline_makespan"])
            for row in selected
        ]
        axes[0].plot(kappa, exact_ratio, marker="o", color=color, label=object_id)
        axes[0].plot(kappa, baseline_ratio, marker="x", linestyle="--", color=color, alpha=0.75)
        exact_queue_reference = float(reference["exact_queue"])
        if exact_queue_reference > 0:
            queue_ratio = [
                float(row["exact_queue"]) / exact_queue_reference for row in selected
            ]
            axes[1].plot(kappa, queue_ratio, marker="o", color=color, label=object_id)
        baseline_queue_reference = float(reference["baseline_queue"])
        if baseline_queue_reference > 0:
            queue_ratio = [
                float(row["baseline_queue"]) / baseline_queue_reference
                for row in selected
            ]
            axes[1].plot(
                kappa,
                queue_ratio,
                marker="x",
                linestyle="--",
                color=color,
                alpha=0.75,
            )
    for axis, title in zip(
        axes,
        ("Makespan scaling", "Queue scaling (non-zero references)"),
        strict=True,
    ):
        axis.plot([0.25, 4], [0.25, 4], color="#222222", linewidth=1.2, label="ideal y=κ")
        axis.set_xscale("log", base=2)
        axis.set_yscale("log", base=2)
        axis.set_xticks([0.25, 0.5, 1, 2, 4], labels=["0.25", "0.5", "1", "2", "4"])
        axis.set_yticks([0.25, 0.5, 1, 2, 4], labels=["0.25", "0.5", "1", "2", "4"])
        axis.set_xlabel(r"Common scale $\kappa$")
        axis.set_ylabel("Metric / metric at κ=1")
        axis.set_title(title, fontweight="bold")
        axis.grid(color="#DDDDDD", linewidth=0.7)
        axis.set_axisbelow(True)
    axes[0].legend(frameon=False, fontsize=8)
    figure.suptitle("EXP-06A: common-scale invariance", fontsize=15, fontweight="bold")
    return _save_figure(figure, output_stem)


def build_ranking_stability(
    summary_rows: list[dict[str, str]], output_stem: Path
) -> tuple[Path, Path]:
    selected = sorted(summary_rows, key=lambda row: float(row["u"]))
    u = np.array([float(row["u"]) for row in selected])
    probability = np.array([float(row["reversal_share"]) for row in selected])
    error = np.array([float(row["monte_carlo_se"]) for row in selected])
    zero_event_upper = np.array(
        [
            float(row["zero_event_one_sided_95_upper"])
            if row["zero_event_one_sided_95_upper"]
            else np.nan
            for row in selected
        ]
    )
    median_margin = np.array([float(row["median_margin_T3_minus_T4"]) for row in selected])
    q05 = np.array([float(row["q05_margin"]) for row in selected])
    q95 = np.array([float(row["q95_margin"]) for row in selected])

    figure, axes = plt.subplots(1, 2, figsize=(13, 5.5), constrained_layout=True)
    axes[0].errorbar(
        u,
        probability,
        yerr=error,
        marker="o",
        color="#D55E00",
        capsize=4,
        linewidth=2,
        label="observed share ± MC SE",
    )
    if np.isfinite(zero_event_upper).any():
        axes[0].plot(
            u,
            zero_event_upper,
            marker="^",
            linestyle="--",
            color="#0072B2",
            label="one-sided 95% upper for zero events",
        )
    upper_limit = max(
        float(np.nanmax(probability + error)),
        float(np.nanmax(zero_event_upper)) if np.isfinite(zero_event_upper).any() else 0,
        0.001,
    )
    axes[0].set_ylim(0, upper_limit * 1.25)
    axes[0].set_xlabel("Uncertainty level, $u$")
    axes[0].set_ylabel("Ranking reversal share")
    axes[0].set_title("Variant 4 ceases to dominate", fontweight="bold")
    axes[0].grid(color="#DDDDDD", linewidth=0.7)
    axes[0].legend(frameon=False, fontsize=8)

    axes[1].plot(u, median_margin, marker="o", color="#0072B2", label="median")
    axes[1].fill_between(u, q05, q95, color="#56B4E9", alpha=0.35, label="5–95%")
    axes[1].axhline(0, color="#222222", linewidth=1)
    axes[1].set_xlabel("Uncertainty level, $u$")
    axes[1].set_ylabel(r"$T_3^*-T_4^*$, hours")
    axes[1].set_title("Paired exact margin", fontweight="bold")
    axes[1].grid(color="#DDDDDD", linewidth=0.7)
    axes[1].legend(frameon=False)
    figure.suptitle("EXP-06B: ranking stability under paired errors", fontsize=15, fontweight="bold")
    return _save_figure(figure, output_stem)


def build_margin_distributions(
    pair_rows: list[dict[str, str]], output_stem: Path
) -> tuple[Path, Path]:
    levels = tuple(dict.fromkeys(row["u"] for row in pair_rows))
    values = [
        [float(row["margin_T3_minus_T4"]) for row in pair_rows if row["u"] == level]
        for level in levels
    ]
    figure, axis = plt.subplots(figsize=(10, 6), constrained_layout=True)
    box = axis.boxplot(values, tick_labels=levels, patch_artist=True, showfliers=False)
    for patch in box["boxes"]:
        patch.set_facecolor("#56B4E9")
        patch.set_alpha(0.7)
    axis.axhline(0, color="#222222", linewidth=1)
    axis.set_xlabel("Uncertainty level, $u$")
    axis.set_ylabel(r"Paired exact margin $T_3^*-T_4^*$, hours")
    axis.set_title("EXP-06B: distribution of the decomposition advantage", fontweight="bold")
    axis.grid(axis="y", color="#DDDDDD", linewidth=0.7)
    return _save_figure(figure, output_stem)


def build_adversarial_thresholds(
    pair_rows: list[dict[str, str]], output_stem: Path
) -> tuple[Path, Path]:
    figure, axis = plt.subplots(figsize=(10, 6), constrained_layout=True)
    labels = {
        "critical_task_agent": "Agent phase of test task",
        "test_human_phases": "Human phases of test task",
    }
    colors = {"critical_task_agent": "#0072B2", "test_human_phases": "#D55E00"}
    for mode in labels:
        selected = sorted(
            [row for row in pair_rows if row["mode"] == mode],
            key=lambda row: float(row["u"]),
        )
        axis.plot(
            [float(row["u"]) for row in selected],
            [float(row["margin_T3_minus_T4"]) for row in selected],
            color=colors[mode],
            linewidth=2,
            label=labels[mode],
        )
    axis.axhline(0, color="#222222", linewidth=1)
    axis.set_xlabel("Adversarial box radius, $u$")
    axis.set_ylabel(r"$T_3^*-T_4^*$, hours")
    axis.set_title("EXP-06C: adverse boundary perturbations", fontweight="bold")
    axis.grid(color="#DDDDDD", linewidth=0.7)
    axis.legend(frameon=False)
    return _save_figure(figure, output_stem)
