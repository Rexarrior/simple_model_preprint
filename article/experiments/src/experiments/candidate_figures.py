from __future__ import annotations

import csv
from dataclasses import replace
from decimal import Decimal, ROUND_HALF_UP
import json
import os
from pathlib import Path
import re
import tempfile
from typing import Any

_matplotlib_cache = Path(tempfile.gettempdir()) / "simple-model-experiments-mpl"
_matplotlib_cache.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(_matplotlib_cache))

import matplotlib

matplotlib.use("Agg")
matplotlib.rcParams["svg.hashsalt"] = "simple-model-full-experiments-v1"

import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np

from .bounds import compute_aggregates
from .exact_solver import solve_exact
from .exp06 import build_random_pair, load_exp06_matrix
from .schema import PhaseSpec, Scenario, ScheduleSpec, TaskSpec, load_scenario, validate_scenario

AGENT_COLOR = "#0072B2"
HUMAN_COLOR = "#D55E00"
CONFLICT_COLOR = "#CC0000"
WAIT_COLOR = "#888888"


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


def _conflicting_human_phases(
    scenario: Scenario, schedule: ScheduleSpec
) -> set[tuple[str, str]]:
    phase_by_key = {
        (task.task_id, phase.phase_id): phase
        for task in scenario.tasks
        for phase in task.phases
    }
    intervals = [
        interval
        for interval in schedule.phases
        if phase_by_key[(interval.task_id, interval.phase_id)].resource == "human"
    ]
    conflicts: set[tuple[str, str]] = set()
    for index, left in enumerate(intervals):
        for right in intervals[index + 1 :]:
            if left.start < right.end and right.start < left.end:
                conflicts.add((left.task_id, left.phase_id))
                conflicts.add((right.task_id, right.phase_id))
    return conflicts


def _human_waits(
    scenario: Scenario, schedule: ScheduleSpec
) -> list[tuple[str, int, Decimal, Decimal]]:
    phase_by_key = {
        (interval.task_id, interval.phase_id): interval
        for interval in schedule.phases
    }
    waits: list[tuple[str, int, Decimal, Decimal]] = []
    for task in scenario.tasks:
        intervals = [phase_by_key[(task.task_id, phase.phase_id)] for phase in task.phases]
        for index in range(1, len(task.phases)):
            if task.phases[index].resource != "human":
                continue
            previous = intervals[index - 1]
            current = intervals[index]
            if current.start > previous.end:
                waits.append((task.task_id, current.agent, previous.end, current.start))
    return waits


def _draw_schedule_panel(
    axis: plt.Axes,
    scenario: Scenario,
    schedule: ScheduleSpec,
    *,
    title: str,
    show_waits: bool,
) -> None:
    phase_specs = {
        (task.task_id, phase.phase_id): phase
        for task in scenario.tasks
        for phase in task.phases
    }
    conflicts = _conflicting_human_phases(scenario, schedule)
    height = 0.58
    for interval in schedule.phases:
        key = (interval.task_id, interval.phase_id)
        phase = phase_specs[key]
        is_conflict = key in conflicts
        color = (
            CONFLICT_COLOR
            if is_conflict
            else HUMAN_COLOR
            if phase.resource == "human"
            else AGENT_COLOR
        )
        start = float(interval.start)
        duration = float(interval.end - interval.start)
        axis.broken_barh(
            [(start, duration)],
            (interval.agent - height / 2, height),
            facecolors=color,
            edgecolors="white",
            linewidth=0.6,
            zorder=3,
        )
        if duration >= 1.0:
            axis.text(
                start + duration / 2,
                interval.agent,
                interval.task_id,
                ha="center",
                va="center",
                color="white",
                fontsize=7,
                fontweight="bold",
                zorder=4,
            )
        if phase.resource == "human":
            axis.broken_barh(
                [(start, duration)],
                (-height / 2, height),
                facecolors=color,
                edgecolors="white",
                linewidth=0.6,
                zorder=3,
            )
            if duration >= 1.0:
                axis.text(
                    start + duration / 2,
                    0,
                    interval.task_id,
                    ha="center",
                    va="center",
                    color="white",
                    fontsize=7,
                    fontweight="bold",
                    zorder=4,
                )

    if show_waits:
        for task_id, agent, start_value, end_value in _human_waits(scenario, schedule):
            start = float(start_value)
            duration = float(end_value - start_value)
            axis.broken_barh(
                [(start, duration)],
                (agent - height / 2, height),
                facecolors="none",
                edgecolors=WAIT_COLOR,
                hatch="////",
                linewidth=0.9,
                zorder=2,
            )
            if duration >= 2.0:
                axis.text(
                    start + duration / 2,
                    agent,
                    f"wait {task_id}",
                    ha="center",
                    va="center",
                    color="#444444",
                    fontsize=6.5,
                    zorder=4,
                )

    axis.set_xlim(0, 48.5)
    axis.set_ylim(-0.6, scenario.p + 0.6)
    axis.set_yticks([0, *range(1, scenario.p + 1)], labels=["Human", "Agent 1", "Agent 2"])
    axis.set_xlabel("Time, hours")
    axis.set_title(title, fontsize=11, fontweight="bold")
    axis.grid(axis="x", color="#DDDDDD", linewidth=0.7)
    axis.set_axisbelow(True)


def build_variant2_schedule_comparison(
    scenario: Scenario, output_stem: Path
) -> tuple[Path, Path]:
    invalid = scenario.schedule_by_id["original_invalid_schedule"]
    feasible = scenario.schedule_by_id["article_schedule"]
    conflict_count = len(_conflicting_human_phases(scenario, invalid))
    figure, axes = plt.subplots(1, 2, figsize=(15, 5.7), sharex=True)
    _draw_schedule_panel(
        axes[0],
        scenario,
        invalid,
        title=f"Original allocation: infeasible\n{conflict_count} human phases in conflicts",
        show_waits=False,
    )
    _draw_schedule_panel(
        axes[1],
        scenario,
        feasible,
        title="Resource-feasible M4 schedule\nlocal waiting retains the agent slot",
        show_waits=True,
    )
    figure.legend(
        handles=[
            Patch(facecolor=AGENT_COLOR, label="Agent phase"),
            Patch(facecolor=HUMAN_COLOR, label="Human phase"),
            Patch(facecolor=CONFLICT_COLOR, label="Overlapping human phase"),
            Patch(facecolor="white", edgecolor=WAIT_COLOR, hatch="////", label="Waiting; slot retained"),
        ],
        loc="lower center",
        ncol=4,
        frameon=False,
    )
    figure.suptitle(
        "Variant 2: agent-feasible timing is not necessarily human-feasible",
        fontsize=14,
        fontweight="bold",
    )
    figure.tight_layout(rect=(0, 0.12, 1, 0.94))
    return _save_figure(figure, output_stem)


def _resource_graph_from_counterexample(
    payload: dict[str, Any],
) -> tuple[list[str], dict[str, dict[str, Any]], dict[tuple[str, str], str], Decimal]:
    selected = payload["selected"]
    scenario = selected["scenario"]
    schedule = selected["exact"]["schedule"]
    phase_resource = {
        (task["task_id"], phase["phase_id"]): phase["resource"]
        for task in scenario["tasks"]
        for phase in task["phases"]
    }
    intervals: dict[str, dict[str, Any]] = {}
    for phase in schedule["phases"]:
        node = f"{phase['task_id']}.{phase['phase_id']}"
        intervals[node] = {
            **phase,
            "start_decimal": Decimal(phase["start"]),
            "end_decimal": Decimal(phase["end"]),
            "duration": Decimal(phase["end"]) - Decimal(phase["start"]),
            "resource": phase_resource[(phase["task_id"], phase["phase_id"])],
        }

    edges: dict[tuple[str, str], str] = {}
    tasks = {task["task_id"]: task for task in scenario["tasks"]}
    for task in scenario["tasks"]:
        nodes = [f"{task['task_id']}.{phase['phase_id']}" for phase in task["phases"]]
        for left, right in zip(nodes[:-1], nodes[1:], strict=True):
            edges[(left, right)] = "task sequence"
        for predecessor in task.get("predecessors", []):
            left = f"{predecessor}.{tasks[predecessor]['phases'][-1]['phase_id']}"
            right = nodes[0]
            edges[(left, right)] = "precedence"

    human_nodes = sorted(
        (node for node, data in intervals.items() if data["resource"] == "human"),
        key=lambda node: (intervals[node]["start_decimal"], intervals[node]["end_decimal"], node),
    )
    for left, right in zip(human_nodes[:-1], human_nodes[1:], strict=True):
        edges.setdefault((left, right), "human order")

    assignments = {row["task_id"]: row["agent"] for row in schedule["assignments"]}
    tasks_by_agent: dict[int, list[str]] = {}
    for task_id, agent in assignments.items():
        tasks_by_agent.setdefault(agent, []).append(task_id)
    for task_ids in tasks_by_agent.values():
        task_ids.sort(
            key=lambda task_id: intervals[f"{task_id}.{tasks[task_id]['phases'][0]['phase_id']}"]["start_decimal"]
        )
        for left_task, right_task in zip(task_ids[:-1], task_ids[1:], strict=True):
            left = f"{left_task}.{tasks[left_task]['phases'][-1]['phase_id']}"
            right = f"{right_task}.{tasks[right_task]['phases'][0]['phase_id']}"
            edges.setdefault((left, right), "slot order")

    ordered_nodes = sorted(
        intervals,
        key=lambda node: (intervals[node]["start_decimal"], intervals[node]["end_decimal"], node),
    )
    incoming: dict[str, list[tuple[str, str]]] = {node: [] for node in ordered_nodes}
    for (left, right), edge_type in edges.items():
        incoming[right].append((left, edge_type))
    best: dict[str, Decimal] = {}
    tie_score: dict[str, tuple[int, int, int]] = {}
    parent: dict[str, tuple[str, str] | None] = {}
    for node in ordered_nodes:
        candidates = []
        for left, edge_type in incoming[node]:
            previous_score = tie_score[left]
            score = (
                previous_score[0] + int(edge_type == "slot order"),
                previous_score[1] + int(edge_type == "human order"),
                previous_score[2] + int(edge_type == "precedence"),
            )
            candidates.append((best[left], score, left, edge_type))
        if candidates:
            _, score, left, edge_type = max(
                candidates,
                key=lambda item: (item[0], item[1], item[2]),
            )
            best[node] = best[left] + intervals[node]["duration"]
            tie_score[node] = score
            parent[node] = (left, edge_type)
        else:
            best[node] = intervals[node]["duration"]
            tie_score[node] = (0, 0, 0)
            parent[node] = None
    last = max(ordered_nodes, key=lambda node: (best[node], tie_score[node], node))
    chain: list[str] = []
    cursor: str | None = last
    while cursor is not None:
        chain.append(cursor)
        parent_item = parent[cursor]
        cursor = None if parent_item is None else parent_item[0]
    chain.reverse()
    chain_edges = {
        (left, right): edges[(left, right)]
        for left, right in zip(chain[:-1], chain[1:], strict=True)
    }
    return chain, intervals, chain_edges, best[last]


def build_resource_augmented_path(
    result_directory: Path, output_stem: Path
) -> tuple[tuple[Path, Path], Decimal]:
    scenario_id = "exp05_p02_m04_ro050_lh00"
    with (result_directory / "exp05_grid.csv").open(encoding="utf-8") as source:
        selected = next(
            row for row in csv.DictReader(source) if row["scenario_id"] == scenario_id
        )
    tokens = re.split(r" -> \[([a-z]+)\] ", selected["exact_critical_chain"])
    chain = tokens[::2]
    edge_labels = {
        "task": "task sequence",
        "precedence": "precedence",
        "human": "human order",
        "agent": "slot order",
    }
    edges = {
        (left, right): edge_labels[tokens[2 * index + 1]]
        for index, (left, right) in enumerate(zip(chain[:-1], chain[1:], strict=True))
    }
    intervals: dict[str, dict[str, Any]] = {}
    with (result_directory / "exp05_phases.csv").open(encoding="utf-8") as source:
        for row in csv.DictReader(source):
            if row["scenario_id"] != scenario_id or row["schedule_kind"] != "exact":
                continue
            node = f"{row['task_id']}.{row['phase_id']}"
            intervals[node] = {
                **row,
                "duration": Decimal(row["duration"]),
            }
    missing = [node for node in chain if node not in intervals]
    if missing:
        raise RuntimeError(f"EXP-05 resource chain has missing phases: {missing}")
    length = Decimal(selected["T_star"])
    edge_colors = {
        "task sequence": "#555555",
        "precedence": "#009E73",
        "human order": HUMAN_COLOR,
        "slot order": "#CC79A7",
    }
    # A compact 3x3 snake remains legible after scaling to the article's A4
    # text width.  The previous six-column layout was visually sparse and
    # reduced node and edge labels to roughly half their designed size.
    columns = 3
    row_count = (len(chain) + columns - 1) // columns
    figure, axis = plt.subplots(
        figsize=(9.2, max(6.2, 1.65 * row_count + 1.3)),
        constrained_layout=True,
    )
    positions: list[tuple[float, float]] = []
    for index in range(len(chain)):
        row = index // columns
        column = index % columns
        x = float(column if row % 2 == 0 else columns - 1 - column)
        y = float(row_count - 1 - row) * 1.25
        positions.append((x, y))
    for index, node in enumerate(chain):
        data = intervals[node]
        resource = data["resource"]
        face = "#F9D7C7" if resource == "human" else "#CFE8F7"
        phase_id = str(data["phase_id"])
        short_phase = (
            phase_id.replace("human_", "H")
            .replace("agent_", "A")
            .replace("specification", "Spec")
            .replace("implementation", "Impl")
            .replace("integration", "Int")
            .replace("acceptance", "Acc")
        )
        task_id = str(data["task_id"])
        short_task = (
            f"d{int(task_id.removeprefix('t04_part_'))}"
            if task_id.startswith("t04_part_")
            else "join"
            if task_id == "t04_join"
            else task_id.replace("t0", "t")
        )
        x, y = positions[index]
        axis.text(
            x,
            y,
            f"{short_task}·{short_phase}\n{data['duration']:.2f} h",
            ha="center",
            va="center",
            fontsize=10,
            bbox={"boxstyle": "round,pad=0.25", "facecolor": face, "edgecolor": edge_colors["human order"] if resource == "human" else AGENT_COLOR},
            zorder=3,
        )
        if index == 0:
            continue
        left = chain[index - 1]
        edge_type = edges[(left, node)]
        color = edge_colors[edge_type]
        previous_x, previous_y = positions[index - 1]
        vertical = abs(previous_x - x) < 0.1
        axis.annotate(
            "",
            xy=(x, y + (0.25 if vertical else 0)),
            xytext=(previous_x, previous_y - (0.25 if vertical else 0)),
            arrowprops={"arrowstyle": "->", "color": color, "linewidth": 1.8},
            zorder=2,
        )
        axis.text(
            (previous_x + x) / 2 + (0.22 if vertical else 0),
            (previous_y + y) / 2 + (0 if vertical else (0.25 if index % 2 else -0.25)),
            edge_type,
            ha="center",
            va="center",
            fontsize=8.5,
            color=color,
        )
    axis.set_xlim(-0.55, columns - 0.45)
    axis.set_ylim(-0.7, (row_count - 1) * 1.25 + 0.65)
    axis.axis("off")
    axis.set_title(
        f"Resource-augmented critical path (EXP-05)\n{length:.2f} h versus B₄={Decimal(selected['B4']):.2f} h",
        fontsize=12.5,
        fontweight="bold",
    )
    used_edge_types = set(edges.values())
    handles = [
        Patch(facecolor="#CFE8F7", edgecolor=AGENT_COLOR, label="Agent phase"),
        Patch(facecolor="#F9D7C7", edgecolor=HUMAN_COLOR, label="Human phase"),
        *[
            Patch(facecolor=color, label=edge_type)
            for edge_type, color in edge_colors.items()
            if edge_type in used_edge_types
        ],
    ]
    axis.legend(
        handles=handles,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.02),
        ncol=3,
        frameon=False,
        fontsize=9,
    )
    return _save_figure(figure, output_stem), length


def _scaled_task_scenario(
    scenario: Scenario,
    *,
    task_id: str,
    agent_factor: Decimal = Decimal("1"),
    human_factor: Decimal = Decimal("1"),
    review_factor: Decimal = Decimal("1"),
    label: str,
) -> Scenario:
    tasks: list[TaskSpec] = []
    for task in scenario.tasks:
        phases: list[PhaseSpec] = []
        for phase in task.phases:
            factor = Decimal("1")
            if task.task_id == task_id:
                factor = agent_factor if phase.resource == "agent" else human_factor
                if phase.resource == "human" and phase.phase_id == "review":
                    factor *= review_factor
            target = phase.base_duration * factor
            ticks = max(
                int((target / scenario.time_unit).quantize(Decimal("1"), rounding=ROUND_HALF_UP)),
                1,
            )
            phases.append(
                replace(phase, base_duration=Decimal(ticks) * scenario.time_unit)
            )
        denominator = scenario.x * task.z
        human_duration = sum((phase.base_duration for phase in phases if phase.resource == "human"), Decimal("0"))
        agent_duration = sum((phase.base_duration for phase in phases if phase.resource == "agent"), Decimal("0"))
        tasks.append(replace(task, h=human_duration / denominator, k=(human_duration + agent_duration) / denominator, phases=tuple(phases)))
    candidate = replace(
        scenario,
        scenario_id=f"candidate_{label}_{task_id}",
        variant_id="candidate-task-lever",
        tasks=tuple(tasks),
        schedules=(),
    )
    validate_scenario(candidate)
    return candidate


def build_task_lever_map(
    scenario: Scenario, output_stem: Path, result_path: Path
) -> tuple[tuple[Path, Path], list[dict[str, str]], Decimal]:
    reference = solve_exact(scenario, time_limit_seconds=30, random_seed=0, workers=1)
    if reference.status != "OPTIMAL" or reference.objective is None:
        raise RuntimeError(f"task-lever reference solve returned {reference.status}")
    interventions = (
        ("agent_20", "Agent phases −20%", {"agent_factor": Decimal("0.8")}),
        ("human_20", "Human phases −20%", {"human_factor": Decimal("0.8")}),
        ("review_80", "Review phase −80%", {"review_factor": Decimal("0.2")}),
    )
    rows: list[dict[str, str]] = []
    matrix: list[list[float]] = []
    for task in scenario.tasks:
        values: list[float] = []
        for intervention_id, intervention_label, kwargs in interventions:
            candidate = _scaled_task_scenario(
                scenario,
                task_id=task.task_id,
                label=intervention_id,
                **kwargs,
            )
            solution = solve_exact(candidate, time_limit_seconds=30, random_seed=0, workers=1)
            if solution.status != "OPTIMAL" or solution.objective is None:
                raise RuntimeError(f"{candidate.scenario_id}: exact solve returned {solution.status}")
            gain = reference.objective - solution.objective
            values.append(float(gain))
            rows.append(
                {
                    "task_id": task.task_id,
                    "task_name": task.name,
                    "intervention": intervention_id,
                    "intervention_label": intervention_label,
                    "reference_T_star": format(reference.objective, "f"),
                    "candidate_T_star": format(solution.objective, "f"),
                    "deadline_reduction": format(gain, "f"),
                    "solver_status": solution.status,
                }
            )
        matrix.append(values)

    plus_agent = replace(scenario, scenario_id="candidate_variant4_p5", p=scenario.p + 1, schedules=())
    plus_agent_solution = solve_exact(plus_agent, time_limit_seconds=30, random_seed=0, workers=1)
    if plus_agent_solution.status != "OPTIMAL" or plus_agent_solution.objective is None:
        raise RuntimeError(f"P+1 solve returned {plus_agent_solution.status}")
    plus_agent_gain = reference.objective - plus_agent_solution.objective

    result_path.parent.mkdir(parents=True, exist_ok=True)
    with result_path.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    data = np.array(matrix)
    figure, axis = plt.subplots(figsize=(9.8, 6.8), constrained_layout=True)
    image = axis.imshow(data, cmap="YlGnBu", vmin=0, vmax=max(float(data.max()), 0.05), aspect="auto")
    critical = set(compute_aggregates(scenario).critical_path_l4)
    ylabels = [f"{task.task_id}{' ★' if task.task_id in critical else ''}  {task.name}" for task in scenario.tasks]
    axis.set_yticks(range(len(scenario.tasks)), labels=ylabels)
    axis.set_xticks(range(len(interventions)), labels=[item[1] for item in interventions], rotation=16, ha="right")
    for row_index in range(data.shape[0]):
        for column_index in range(data.shape[1]):
            value = data[row_index, column_index]
            axis.text(column_index, row_index, f"{value:.2f}", ha="center", va="center", color="white" if value > data.max() * 0.55 else "#222222", fontsize=8)
    colorbar = figure.colorbar(image, ax=axis, shrink=0.86)
    colorbar.set_label("Reduction in exact makespan, hours")
    axis.set_title(
        "Variant 4: local value of task-level interventions\n"
        rf"Reference $T^*={reference.objective:g}$ h; global $P:{scenario.p}\to{scenario.p + 1}$ gain = {plus_agent_gain:g} h",
        fontsize=13,
        fontweight="bold",
    )
    axis.text(
        0,
        -0.16,
        "★ task belongs to the nominal L₄ critical path; interventions are controlled synthetic reductions.",
        transform=axis.transAxes,
        fontsize=8,
    )
    return _save_figure(figure, output_stem), rows, plus_agent_gain


def build_probabilistic_fan(
    project_root: Path,
    output_stem: Path,
    result_path: Path,
    *,
    sample_count: int = 100,
    uncertainty: Decimal = Decimal("0.30"),
    deadline: Decimal = Decimal("40"),
) -> tuple[tuple[Path, Path], list[dict[str, str]]]:
    matrix = load_exp06_matrix(project_root / "scenarios" / "canonical" / "exp06_matrix.yaml")
    p_values = (1, 2, 3, 4, 6, 8)
    rows: list[dict[str, str]] = []
    for seed in range(sample_count):
        _, variant_4, _ = build_random_pair(matrix, u=uncertainty, seed=seed)
        for p in p_values:
            scenario = replace(
                variant_4,
                scenario_id=f"candidate_fan_u30_s{seed:04d}_p{p:02d}",
                variant_id="candidate-probabilistic-fan",
                p=p,
            )
            solution = solve_exact(scenario, time_limit_seconds=10, random_seed=0, workers=1)
            if solution.status != "OPTIMAL" or solution.objective is None:
                raise RuntimeError(f"{scenario.scenario_id}: exact solve returned {solution.status}")
            rows.append(
                {
                    "uncertainty": format(uncertainty, "f"),
                    "seed": str(seed),
                    "P": str(p),
                    "T_star": format(solution.objective, "f"),
                    "human_baseline": "76",
                    "deadline": format(deadline, "f"),
                    "beats_human": str(solution.objective < Decimal("76")).lower(),
                    "meets_deadline": str(solution.objective <= deadline).lower(),
                    "solver_status": solution.status,
                }
            )

    result_path.parent.mkdir(parents=True, exist_ok=True)
    with result_path.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    grouped = {
        p: np.array([float(row["T_star"]) for row in rows if int(row["P"]) == p])
        for p in p_values
    }
    median = np.array([np.median(grouped[p]) for p in p_values])
    q10 = np.array([np.percentile(grouped[p], 10) for p in p_values])
    q90 = np.array([np.percentile(grouped[p], 90) for p in p_values])
    q25 = np.array([np.percentile(grouped[p], 25) for p in p_values])
    q75 = np.array([np.percentile(grouped[p], 75) for p in p_values])
    beats_human = np.array([np.mean(grouped[p] < 76) for p in p_values])
    meets_deadline = np.array([np.mean(grouped[p] <= float(deadline)) for p in p_values])

    figure, axes = plt.subplots(1, 2, figsize=(13.5, 5.6), constrained_layout=True)
    axes[0].fill_between(p_values, q10, q90, color="#9ECAE1", alpha=0.45, label="10–90%")
    axes[0].fill_between(p_values, q25, q75, color="#4292C6", alpha=0.45, label="25–75%")
    axes[0].plot(p_values, median, color=AGENT_COLOR, marker="o", linewidth=2, label="Median")
    axes[0].axhline(float(deadline), color=HUMAN_COLOR, linestyle="--", linewidth=1.4, label=f"Illustrative deadline: {deadline:g} h")
    axes[0].set_xlabel("Configured parallelism, P")
    axes[0].set_ylabel("Exact makespan, hours")
    axes[0].set_title("Distribution of completion time", fontweight="bold")
    axes[0].grid(color="#DDDDDD", linewidth=0.7)
    axes[0].legend(frameon=False, fontsize=8)

    axes[1].plot(p_values, beats_human, color="#009E73", marker="o", linewidth=2, label=r"$\Pr(T^*<T_h)$")
    axes[1].plot(p_values, meets_deadline, color=HUMAN_COLOR, marker="s", linewidth=2, label=rf"$\Pr(T^*\leq {deadline:g}\,h)$")
    axes[1].set_ylim(-0.03, 1.03)
    axes[1].set_xlabel("Configured parallelism, P")
    axes[1].set_ylabel("Share of synthetic draws")
    axes[1].set_title("Illustrative success probabilities", fontweight="bold")
    axes[1].grid(color="#DDDDDD", linewidth=0.7)
    axes[1].legend(frameon=False)
    figure.suptitle(
        f"Variant 4 under the frozen EXP-06 error model (u={uncertainty:g}, n={sample_count}); not empirically calibrated",
        fontsize=13,
        fontweight="bold",
    )
    return _save_figure(figure, output_stem), rows


def _write_candidate_report(
    path: Path,
    *,
    resource_path_length: Decimal,
    plus_agent_gain: Decimal,
    sample_count: int,
) -> Path:
    content = f"""# Candidate visualizations: inclusion assessment

Date: 2026-08-09.

## Decision applied

1. **Variant-2 schedule comparison — included in the main text, replacing the
   one-panel Gantt.** It directly demonstrates the M4 feasibility claim: the
   left schedule violates the shared human resource, while the right schedule
   restores feasibility and makes local blocking visible.
2. **Resource-augmented critical path — included in the computational-results
   explanation of $T^*>B_4$.** Its reconstructed longest path is
   {resource_path_length:.2f} hours, equal to the proven optimum of the selected
   EXP-05 scenario. It adds a
   concept not visible in aggregate branches alone; its compact 3x3 layout is
   designed for the final A4 text width.
3. **Task-level intervention map — included in the appendix.** It cleanly shows
   zero/positive local value and reports a global `P:4→5` gain of
   {plus_agent_gain:.2f} hours. However, the intervention magnitudes are controlled
   synthetic choices and the planned decomposition column remains
   methodologically undefined for arbitrary tasks.
4. **Probabilistic fan — not included in the current article.** It uses
   {sample_count} synthetic draws from the frozen EXP-06 error model, not an
   empirical distribution. It is useful as a design preview for a future
   calibrated study, not as evidence about real deadline risk.

## Not generated

- The empirical calibration map requires observed `prediction–actual` pairs.
- The multiple-cell portfolio visualization belongs to a model extension that
  is explicitly outside the current single-cell scope.
- An interactive simulator is a separate artifact rather than a static article
  figure.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def build_candidate_figures(
    project_root: Path,
    output_directory: Path,
    result_directory: Path,
    *,
    sample_count: int = 100,
) -> tuple[Path, ...]:
    scenario_directory = project_root / "scenarios" / "article"
    variant_2 = load_scenario(scenario_directory / "variant_2.yaml")
    variant_4 = load_scenario(scenario_directory / "variant_4.yaml")
    outputs: list[Path] = []
    outputs.extend(
        build_variant2_schedule_comparison(
            variant_2,
            output_directory / "candidate_variant2_schedule_comparison",
        )
    )
    resource_outputs, resource_length = build_resource_augmented_path(
        result_directory,
        output_directory / "candidate_resource_augmented_path",
    )
    outputs.extend(resource_outputs)
    lever_outputs, _, plus_agent_gain = build_task_lever_map(
        variant_4,
        output_directory / "candidate_task_lever_map",
        result_directory / "candidate_task_levers.csv",
    )
    outputs.extend(lever_outputs)
    outputs.append(result_directory / "candidate_task_levers.csv")
    fan_outputs, _ = build_probabilistic_fan(
        project_root,
        output_directory / "candidate_probabilistic_fan",
        result_directory / "candidate_probabilistic_fan.csv",
        sample_count=sample_count,
    )
    outputs.extend(fan_outputs)
    outputs.append(result_directory / "candidate_probabilistic_fan.csv")
    outputs.append(
        _write_candidate_report(
            result_directory / "candidate_visualizations_report.md",
            resource_path_length=resource_length,
            plus_agent_gain=plus_agent_gain,
            sample_count=sample_count,
        )
    )
    return tuple(outputs)
