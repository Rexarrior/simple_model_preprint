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


COLORS = {
    "wide_layered": "#0072B2",
    "mixed": "#009E73",
    "chain_like": "#D55E00",
}


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def _save(figure: plt.Figure, stem: Path) -> tuple[Path, Path]:
    stem.parent.mkdir(parents=True, exist_ok=True)
    svg = stem.with_suffix(".svg")
    png = stem.with_suffix(".png")
    figure.savefig(svg, bbox_inches="tight", metadata={"Date": None})
    svg.write_text(
        "\n".join(line.rstrip() for line in svg.read_text(encoding="utf-8").splitlines()) + "\n",
        encoding="utf-8",
    )
    figure.savefig(png, dpi=180, bbox_inches="tight")
    plt.close(figure)
    return svg, png


def build_design_coverage(dag_rows: list[dict[str, str]], stem: Path) -> tuple[Path, Path]:
    figure, axes = plt.subplots(1, 2, figsize=(13, 5.6), constrained_layout=True)
    markers = {"homogeneous": "o", "lognormal": "^"}
    for topology, color in COLORS.items():
        for weight_type, marker in markers.items():
            selected = [
                row for row in dag_rows
                if row["topology_family"] == topology and row["weight_type"] == weight_type
            ]
            axes[0].scatter(
                [float(row["rho_l"]) for row in selected],
                [float(row["rho_h_cp"]) for row in selected],
                s=16,
                alpha=0.28,
                color=color,
                marker=marker,
                edgecolors="none",
                label=f"{topology}, {weight_type}",
            )
    for value in (0.30, 0.60):
        axes[0].axvline(value, color="#888888", linewidth=0.8, linestyle="--")
        axes[0].axhline(value, color="#888888", linewidth=0.8, linestyle="--")
    axes[0].set_xlabel(r"Critical-path share $\rho_L=L_4/W_4$")
    axes[0].set_ylabel(r"Human concentration $\rho_H^{cp}=H_{cp}/H$")
    axes[0].set_title("Accepted DAGs and frozen bins", fontweight="bold")
    axes[0].grid(color="#E5E5E5", linewidth=0.6)
    axes[0].legend(frameon=False, fontsize=7, ncol=2)

    task_counts = (8, 16, 32, 64)
    topologies = tuple(COLORS)
    width = 0.22
    for index, topology in enumerate(topologies):
        counts = [sum(row["task_count"] == str(task_count) and row["topology_family"] == topology for row in dag_rows) for task_count in task_counts]
        positions = [item + (index - 1) * width for item in range(len(task_counts))]
        axes[1].bar(positions, counts, width=width, color=COLORS[topology], label=topology)
    axes[1].set_xticks(range(len(task_counts)), labels=[str(item) for item in task_counts])
    axes[1].set_xlabel("Task count, N")
    axes[1].set_ylabel("Accepted DAGs")
    axes[1].set_title("Balanced accepted sample", fontweight="bold")
    axes[1].grid(axis="y", color="#E5E5E5", linewidth=0.6)
    axes[1].legend(frameon=False, fontsize=8)
    figure.suptitle("EXP-07: synthetic-design coverage", fontsize=15, fontweight="bold")
    return _save(figure, stem)


def _box(axis: plt.Axes, values: list[list[float]], labels: list[str], *, color: str, ylabel: str, title: str) -> None:
    boxes = axis.boxplot(values, tick_labels=labels, patch_artist=True, showfliers=False)
    for patch in boxes["boxes"]:
        patch.set_facecolor(color)
        patch.set_alpha(0.72)
    axis.axhline(0, color="#222222", linewidth=1)
    axis.set_ylabel(ylabel)
    axis.set_title(title, fontweight="bold")
    axis.grid(axis="y", color="#E5E5E5", linewidth=0.6)
    axis.tick_params(axis="x", labelrotation=15)


def build_claim_effects(pair_rows: list[dict[str, str]], stem: Path) -> tuple[Path, Path]:
    primary = [row for row in pair_rows if row["estimator"] in {"baseline_policy", "lower_bound"}]
    figure, axes = plt.subplots(2, 2, figsize=(14, 10), constrained_layout=True)
    c1 = [row for row in primary if row["claim"] == "C1"]
    _box(
        axes[0, 0],
        [[float(row["paired_effect"]) for row in c1 if row["topology_family"] == topology] for topology in COLORS],
        ["wide", "mixed", "chain-like"],
        color="#56B4E9",
        ylabel="Δ relative tightness",
        title="C1: sync − staggered",
    )
    c2 = [row for row in primary if row["claim"] == "C2"]
    _box(
        axes[0, 1],
        [
            [float(row["paired_effect"]) for row in c2 if row["metric"].endswith("agent_cost")],
            [float(row["paired_effect"]) for row in c2 if row["metric"].endswith("human_cost")],
        ],
        ["agent cost", "human cost"],
        color="#E69F00",
        ylabel=r"$P_{opt,cost}-P_{opt,base}$",
        title="C2: policy-optimal P shift",
    )
    c3 = [row for row in primary if row["claim"] == "C3"]
    _box(
        axes[1, 0],
        [
            [float(row["paired_effect"]) for row in c3 if row["metric"] == "decomposition_interaction"],
            [float(row["paired_effect"]) for row in c3 if row["metric"] == "overhead_attenuation"],
        ],
        ["P interaction", "overhead attenuation"],
        color="#009E73",
        ylabel="Paired makespan contrast",
        title="C3: decomposition contrasts",
    )
    c4 = [row for row in primary if row["claim"] == "C4"]
    low: list[float] = []
    high: list[float] = []
    for row in c4:
        fields = dict(item.split("=") for item in row["detail"].split("; "))
        low.append(float(fields["low"]))
        high.append(float(fields["high"]))
    axes[1, 1].bar([0, 1], [sum(low) / len(low), sum(high) / len(high)], color=["#999999", "#CC79A7"], width=0.62)
    axes[1, 1].set_xticks([0, 1], labels=[r"low $\rho_H^{cp}$", r"high $\rho_H^{cp}$"])
    axes[1, 1].set_ylim(0, 1)
    axes[1, 1].set_ylabel("Human branch active frequency")
    axes[1, 1].set_title("C4: active lower-bound branch", fontweight="bold")
    axes[1, 1].grid(axis="y", color="#E5E5E5", linewidth=0.6)
    figure.suptitle("EXP-07: confirmatory paired effects", fontsize=15, fontweight="bold")
    return _save(figure, stem)


def build_exp07_figures(dags_path: Path, pairs_path: Path, output_directory: Path) -> tuple[Path, ...]:
    dag_rows = _read_csv(dags_path)
    pair_rows = _read_csv(pairs_path)
    return (
        *build_design_coverage(dag_rows, output_directory / "exp07_design_coverage"),
        *build_claim_effects(pair_rows, output_directory / "exp07_claim_effects"),
    )
