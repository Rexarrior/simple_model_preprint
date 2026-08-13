from __future__ import annotations

import csv
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


COLORS = {"wide_layered": "#0072B2", "mixed": "#009E73", "chain_like": "#D55E00"}


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def _save(figure: plt.Figure, stem: Path) -> tuple[Path, Path]:
    stem.parent.mkdir(parents=True, exist_ok=True)
    svg = stem.with_suffix(".svg")
    png = stem.with_suffix(".png")
    figure.savefig(svg, bbox_inches="tight", metadata={"Date": None})
    svg.write_text("\n".join(line.rstrip() for line in svg.read_text(encoding="utf-8").splitlines()) + "\n", encoding="utf-8")
    figure.savefig(png, dpi=180, bbox_inches="tight")
    plt.close(figure)
    return svg, png


def _allocation_coverage(graphs: list[dict[str, str]], stem: Path) -> tuple[Path, Path]:
    figure, axes = plt.subplots(1, 2, figsize=(13, 5.4), constrained_layout=True)
    for topology, color in COLORS.items():
        selected = [row for row in graphs if row["topology_family"] == topology]
        axes[0].scatter(
            [float(row["rho_l"]) for row in selected],
            [float(row["rho_h_low"]) for row in selected],
            s=16, alpha=0.32, color=color, marker="o", edgecolors="none",
            label=f"{topology}: low",
        )
        axes[0].scatter(
            [float(row["rho_l"]) for row in selected],
            [float(row["rho_h_high"]) for row in selected],
            s=16, alpha=0.32, color=color, marker="^", edgecolors="none",
            label=f"{topology}: high",
        )
    axes[0].axhline(0.30, color="#555555", linestyle="--", linewidth=0.8)
    axes[0].axhline(0.70, color="#555555", linestyle="--", linewidth=0.8)
    axes[0].set_xlabel(r"Structural path share $L/W$")
    axes[0].set_ylabel(r"Actual human concentration $H_{P_0}/H$")
    axes[0].set_title("Exact paired allocation targets", fontweight="bold")
    axes[0].grid(color="#E5E5E5", linewidth=0.6)
    axes[0].legend(frameon=False, fontsize=7, ncol=2)

    task_counts = (8, 16, 32, 64)
    unique = [sum(row["task_count"] == str(n) and row["path_multiplicity"] == "unique" for row in graphs) for n in task_counts]
    tied = [sum(row["task_count"] == str(n) and row["path_multiplicity"] == "tied" for row in graphs) for n in task_counts]
    axes[1].bar(range(4), unique, color="#56B4E9", label="unique P0")
    axes[1].bar(range(4), tied, bottom=unique, color="#CC79A7", label="tied longest paths")
    axes[1].set_xticks(range(4), labels=[str(item) for item in task_counts])
    axes[1].set_xlabel("Task count, N")
    axes[1].set_ylabel("Confirmatory graph bases")
    axes[1].set_title("Reference-path multiplicity", fontweight="bold")
    axes[1].grid(axis="y", color="#E5E5E5", linewidth=0.6)
    axes[1].legend(frameon=False)
    figure.suptitle("EXP-08: confirmatory allocation design", fontsize=15, fontweight="bold")
    return _save(figure, stem)


def _schedule_effects(pairs: list[dict[str, str]], stem: Path) -> tuple[Path, Path]:
    selected = [row for row in pairs if row["pair_type"] == "schedule_policy"]
    figure, axes = plt.subplots(1, 2, figsize=(13, 5.6), constrained_layout=True, sharey=True)
    for axis, profile in zip(axes, ("io", "equal_alternating"), strict=True):
        values = [
            [float(row["delta_makespan_normalized"]) for row in selected if row["phase_profile"] == profile and row["P"] == str(p)]
            for p in (1, 4, 8)
        ]
        boxes = axis.boxplot(values, tick_labels=["P=1", "P=4", "P=8"], patch_artist=True, showfliers=False)
        for patch, color in zip(boxes["boxes"], ("#999999", "#0072B2", "#009E73"), strict=True):
            patch.set_facecolor(color)
            patch.set_alpha(0.75)
        axis.axhspan(-0.01, 0.01, color="#F0E442", alpha=0.22, label="±0.01 margin")
        axis.axhline(0, color="#222222", linewidth=1)
        axis.set_title(profile.replace("_", " "), fontweight="bold")
        axis.set_xlabel("Agent slots")
        axis.grid(axis="y", color="#E5E5E5", linewidth=0.6)
        axis.legend(frameon=False, fontsize=8)
    axes[0].set_ylabel(r"$(T_{high}-T_{low})/B_4$")
    figure.suptitle("EXP-08B: high versus low human concentration", fontsize=15, fontweight="bold")
    return _save(figure, stem)


def _critical_path_effects(pairs: list[dict[str, str]], stem: Path) -> tuple[Path, Path]:
    selected = [row for row in pairs if row["pair_type"] == "differentiated_slowdown"]
    figure, axes = plt.subplots(1, 2, figsize=(13, 5.4), constrained_layout=True)
    data = [
        [float(row["delta_reference_path_length_normalized"]) for row in selected if row["topology_family"] == topology]
        for topology in COLORS
    ]
    boxes = axes[0].boxplot(data, tick_labels=["wide", "mixed", "chain-like"], patch_artist=True, showfliers=False)
    for patch, color in zip(boxes["boxes"], COLORS.values(), strict=True):
        patch.set_facecolor(color)
        patch.set_alpha(0.75)
    axes[0].axhline(0, color="#222222", linewidth=1)
    axes[0].set_ylabel(r"$\Delta L(P_0)/B_{4,low}$")
    axes[0].set_title("Frozen reference-path growth", fontweight="bold")
    axes[0].grid(axis="y", color="#E5E5E5", linewidth=0.6)

    stable = sum(row["path_stable"] == "true" for row in selected)
    switched = len(selected) - stable
    axes[1].bar([0, 1], [stable, switched], color=["#009E73", "#D55E00"], width=0.62)
    axes[1].set_xticks([0, 1], labels=["P0 stable", "path switch"])
    axes[1].set_ylabel("Graph bases")
    axes[1].set_title("Global longest-path status", fontweight="bold")
    axes[1].grid(axis="y", color="#E5E5E5", linewidth=0.6)
    figure.suptitle("EXP-08C: differentiated human slowdown", fontsize=15, fontweight="bold")
    return _save(figure, stem)


def build_exp08_figures(graphs_path: Path, pairs_path: Path, output_directory: Path) -> tuple[Path, ...]:
    graphs = _read(graphs_path)
    pairs = _read(pairs_path)
    return (
        *_allocation_coverage(graphs, output_directory / "exp08_allocation_coverage"),
        *_schedule_effects(pairs, output_directory / "exp08_schedule_effects"),
        *_critical_path_effects(pairs, output_directory / "exp08_critical_path_effects"),
    )
