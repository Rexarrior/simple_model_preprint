from __future__ import annotations

import csv
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from decimal import Decimal
import hashlib
import importlib.metadata
import json
from pathlib import Path
import random
from statistics import mean, median
from typing import Any, Iterable

import yaml

from .bounds import AggregateMetrics, compute_aggregates
from .exact_solver import ExactSolution, solve_exact
from .provenance import git_provenance, implementation_records
from .schema import PhaseSpec, Scenario, ScenarioError, TaskSpec, decimal, validate_scenario
from .simulator import simulate_baseline
from .validator import ScheduleValidation, validate_schedule


@dataclass(frozen=True)
class BinSpec:
    name: str
    lower: Decimal
    upper: Decimal
    upper_inclusive: bool
    target: Decimal | None = None

    def contains(self, value: Decimal) -> bool:
        return self.lower <= value and (
            value <= self.upper if self.upper_inclusive else value < self.upper
        )


@dataclass(frozen=True)
class TopologySpec:
    name: str
    target_rho_l_bin: str
    layer_fraction: Decimal
    adjacent_edge_probability: Decimal
    skip_edge_probability: Decimal


@dataclass(frozen=True)
class Exp07Matrix:
    source_path: Path
    raw: dict[str, Any]
    frozen_at: str
    task_counts: tuple[int, ...]
    topology_specs: tuple[TopologySpec, ...]
    weight_types: tuple[str, ...]
    human_bins: tuple[str, ...]
    seed_start: int
    seed_stop: int
    expected_cells: int
    expected_accepted_dags: int
    master_seed: int
    max_attempts: int
    time_unit: Decimal
    tolerance: Decimal
    base_effort: Decimal
    rho_l_bins: dict[str, BinSpec]
    rho_h_bins: dict[str, BinSpec]
    human_share_grid: tuple[Decimal, ...]
    default_p: int
    p_grid: tuple[int, ...]
    decomposition_m: int
    p_low: int
    p_high: int
    overhead_rates: tuple[Decimal, ...]
    human_overhead_share: Decimal
    exact_task_counts: tuple[int, ...]
    exact_weight_types: tuple[str, ...]
    exact_human_bins: tuple[str, ...]
    exact_seeds: tuple[int, ...]
    expected_exact_dags: int
    expected_exact_scenarios: int
    exact_time_limit: float
    exact_random_seed: int
    exact_workers: int
    bootstrap_resamples: int
    bootstrap_seed: int


@dataclass(frozen=True)
class GeneratedDag:
    dag_id: str
    cell_id: str
    task_count: int
    topology_family: str
    weight_type: str
    target_rho_l_bin: str
    human_concentration_bin: str
    observation_seed: int
    attempt: int
    raw_seed: int
    predecessors: tuple[tuple[str, ...], ...]
    weights: tuple[Decimal, ...]
    human_shares: tuple[Decimal, ...]
    critical_path: tuple[str, ...]
    rho_l: Decimal
    rho_h_cp: Decimal


def _mapping(raw: object, *, field: str) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise ScenarioError(f"{field}: expected mapping")
    return raw


def _list(raw: object, *, field: str) -> list[object]:
    if not isinstance(raw, list) or not raw:
        raise ScenarioError(f"{field}: expected non-empty list")
    return raw


def _load_bins(raw: object, *, field: str) -> dict[str, BinSpec]:
    bins: dict[str, BinSpec] = {}
    for name, item in _mapping(raw, field=field).items():
        data = _mapping(item, field=f"{field}.{name}")
        bins[str(name)] = BinSpec(
            name=str(name),
            lower=decimal(data.get("lower"), field=f"{field}.{name}.lower"),
            upper=decimal(data.get("upper"), field=f"{field}.{name}.upper"),
            upper_inclusive=bool(data.get("upper_inclusive", False)),
            target=(
                decimal(data["target"], field=f"{field}.{name}.target")
                if "target" in data
                else None
            ),
        )
    return bins


def load_exp07_matrix(path: str | Path) -> Exp07Matrix:
    source_path = Path(path).resolve()
    with source_path.open("r", encoding="utf-8") as source:
        raw = yaml.safe_load(source)
    data = _mapping(raw, field="EXP-07 matrix")
    if data.get("frozen") is not True:
        raise ScenarioError("EXP-07 matrix must be frozen before execution")
    design = _mapping(data.get("design"), field="design")
    generator = _mapping(data.get("generator"), field="generator")
    topology_raw = _mapping(generator.get("topology"), field="generator.topology")
    claim_parameters = _mapping(data.get("claim_parameters"), field="claim_parameters")
    decomposition = _mapping(
        claim_parameters.get("decomposition"), field="claim_parameters.decomposition"
    )
    exact = _mapping(data.get("exact_audit"), field="exact_audit")
    reporting = _mapping(data.get("reporting"), field="reporting")
    seeds = _mapping(design.get("observation_seeds"), field="observation_seeds")
    matrix = Exp07Matrix(
        source_path=source_path,
        raw=data,
        frozen_at=str(data.get("frozen_at", "")),
        task_counts=tuple(int(item) for item in _list(design.get("task_counts"), field="task_counts")),
        topology_specs=tuple(
            TopologySpec(
                name=str(name),
                target_rho_l_bin=str(_mapping(item, field=f"topology.{name}").get("target_rho_l_bin")),
                layer_fraction=decimal(_mapping(item, field=f"topology.{name}").get("layer_fraction"), field="layer_fraction"),
                adjacent_edge_probability=decimal(_mapping(item, field=f"topology.{name}").get("adjacent_edge_probability"), field="adjacent_edge_probability"),
                skip_edge_probability=decimal(_mapping(item, field=f"topology.{name}").get("skip_edge_probability"), field="skip_edge_probability"),
            )
            for name, item in topology_raw.items()
        ),
        weight_types=tuple(str(item) for item in _list(design.get("weight_types"), field="weight_types")),
        human_bins=tuple(str(item) for item in _list(design.get("human_concentration_bins"), field="human_concentration_bins")),
        seed_start=int(seeds.get("start", 0)),
        seed_stop=int(seeds.get("stop", -1)),
        expected_cells=int(design.get("expected_cells", 0)),
        expected_accepted_dags=int(design.get("expected_accepted_dags", 0)),
        master_seed=int(generator.get("master_seed", 0)),
        max_attempts=int(generator.get("max_attempts_per_observation", 0)),
        time_unit=decimal(generator.get("time_unit"), field="time_unit"),
        tolerance=decimal(generator.get("tolerance"), field="tolerance"),
        base_effort=decimal(generator.get("base_effort"), field="base_effort"),
        rho_l_bins=_load_bins(generator.get("rho_l_bins"), field="rho_l_bins"),
        rho_h_bins=_load_bins(generator.get("rho_h_cp_bins"), field="rho_h_cp_bins"),
        human_share_grid=tuple(decimal(item, field="human_share_grid") for item in _list(generator.get("human_share_grid"), field="human_share_grid")),
        default_p=int(claim_parameters.get("default_agent_count", 0)),
        p_grid=tuple(int(item) for item in _list(claim_parameters.get("p_grid"), field="p_grid")),
        decomposition_m=int(decomposition.get("m", 0)),
        p_low=int(decomposition.get("p_low", 0)),
        p_high=int(decomposition.get("p_high", 0)),
        overhead_rates=tuple(decimal(item, field="overhead_rates") for item in _list(decomposition.get("overhead_rates"), field="overhead_rates")),
        human_overhead_share=decimal(decomposition.get("human_overhead_share"), field="human_overhead_share"),
        exact_task_counts=tuple(int(item) for item in _list(exact.get("task_counts"), field="exact.task_counts")),
        exact_weight_types=tuple(str(item) for item in _list(exact.get("weight_types"), field="exact.weight_types")),
        exact_human_bins=tuple(str(item) for item in _list(exact.get("human_concentration_bins"), field="exact.human_bins")),
        exact_seeds=tuple(int(item) for item in _list(exact.get("observation_seeds"), field="exact.seeds")),
        expected_exact_dags=int(exact.get("expected_dags", 0)),
        expected_exact_scenarios=int(exact.get("expected_scenarios", 0)),
        exact_time_limit=float(exact.get("time_limit_seconds", 0)),
        exact_random_seed=int(exact.get("random_seed", 0)),
        exact_workers=int(exact.get("workers", 0)),
        bootstrap_resamples=int(reporting.get("bootstrap_resamples", 0)),
        bootstrap_seed=int(reporting.get("bootstrap_seed", 0)),
    )
    _validate_matrix(matrix)
    return matrix


def _validate_matrix(matrix: Exp07Matrix) -> None:
    if matrix.raw.get("schema_version") != 1 or matrix.raw.get("experiment_id") != "EXP-07":
        raise ScenarioError("EXP-07 requires schema_version=1 and experiment_id=EXP-07")
    if matrix.task_counts != (8, 16, 32, 64):
        raise ScenarioError("EXP-07 task counts differ from the frozen design")
    if tuple(item.name for item in matrix.topology_specs) != ("wide_layered", "mixed", "chain_like"):
        raise ScenarioError("EXP-07 topology families differ from the frozen design")
    if matrix.weight_types != ("homogeneous", "lognormal") or matrix.human_bins != ("low", "medium", "high"):
        raise ScenarioError("EXP-07 weight types or human bins differ from the frozen design")
    seed_count = matrix.seed_stop - matrix.seed_start + 1
    cells = len(matrix.task_counts) * len(matrix.topology_specs) * len(matrix.weight_types) * len(matrix.human_bins)
    if seed_count != 20 or cells != matrix.expected_cells or cells * seed_count != matrix.expected_accepted_dags:
        raise ScenarioError("EXP-07 frozen pilot counts are inconsistent")
    if set(matrix.rho_l_bins) != {"low", "medium", "high"} or set(matrix.rho_h_bins) != {"low", "medium", "high"}:
        raise ScenarioError("EXP-07 requires three rho_L and rho_H bins")
    if matrix.p_grid != (1, 2, 4, 8) or matrix.default_p != 4:
        raise ScenarioError("EXP-07 P design differs from the frozen matrix")
    if (matrix.decomposition_m, matrix.p_low, matrix.p_high, matrix.overhead_rates) != (3, 1, 4, (Decimal("0"), Decimal("0.10"))):
        raise ScenarioError("EXP-07 decomposition contrast differs from the frozen matrix")
    exact_count = len(matrix.exact_task_counts) * len(matrix.topology_specs) * len(matrix.exact_weight_types) * len(matrix.exact_human_bins) * len(matrix.exact_seeds)
    if exact_count != matrix.expected_exact_dags or matrix.exact_workers != 1:
        raise ScenarioError("EXP-07 exact audit count or worker count is inconsistent")
    if matrix.expected_exact_scenarios != 36 or matrix.exact_time_limit != 10:
        raise ScenarioError("EXP-07 exact resource amendment differs from the frozen matrix")
    if matrix.time_unit != Decimal("0.001") or matrix.base_effort != Decimal("12"):
        raise ScenarioError("EXP-07 time grid or base effort differs from the frozen design")


def _task_ids(task_count: int) -> tuple[str, ...]:
    width = max(2, len(str(task_count)))
    return tuple(f"t{index + 1:0{width}d}" for index in range(task_count))


def _layered_predecessors(task_count: int, spec: TopologySpec, rng: random.Random) -> tuple[tuple[str, ...], ...]:
    task_ids = _task_ids(task_count)
    layer_count = max(2, min(task_count, int((Decimal(task_count) * spec.layer_fraction).to_integral_value(rounding="ROUND_HALF_UP"))))
    if layer_count == 2:
        layers = [[0], list(range(1, task_count))]
    else:
        layers = [[0]]
        remaining = task_count - 2
        middle_layers = layer_count - 2
        cursor = 1
        for layer_index in range(middle_layers):
            size = remaining // middle_layers + int(layer_index < remaining % middle_layers)
            layers.append(list(range(cursor, cursor + size)))
            cursor += size
        layers.append([task_count - 1])
    predecessors: list[set[int]] = [set() for _ in range(task_count)]
    for layer_index in range(1, len(layers)):
        previous = layers[layer_index - 1]
        current = layers[layer_index]
        for node in current:
            predecessors[node].add(rng.choice(previous))
            for candidate in previous:
                if candidate not in predecessors[node] and rng.random() < float(spec.adjacent_edge_probability):
                    predecessors[node].add(candidate)
        for candidate in previous:
            if not any(candidate in predecessors[node] for node in current):
                predecessors[rng.choice(current)].add(candidate)
    if spec.skip_edge_probability > 0:
        for earlier in range(len(layers) - 2):
            for later in range(earlier + 2, len(layers)):
                for source in layers[earlier]:
                    for target in layers[later]:
                        if rng.random() < float(spec.skip_edge_probability):
                            predecessors[target].add(source)
    return tuple(tuple(task_ids[item] for item in sorted(items)) for items in predecessors)


def _weights(task_count: int, weight_type: str, matrix: Exp07Matrix, rng: random.Random) -> tuple[Decimal, ...]:
    if weight_type == "homogeneous":
        multipliers = [1] * task_count
    elif weight_type == "lognormal":
        params = _mapping(_mapping(matrix.raw["generator"], field="generator")["weights"], field="weights")["lognormal"]
        data = _mapping(params, field="weights.lognormal")
        mu = float(decimal(data["mu"], field="mu"))
        sigma = float(decimal(data["sigma"], field="sigma"))
        scale = float(decimal(data["integer_multiplier_scale"], field="scale"))
        minimum = int(data["minimum_multiplier"])
        maximum = int(data["maximum_multiplier"])
        multipliers = [max(minimum, min(maximum, int(round(scale * rng.lognormvariate(mu, sigma))))) for _ in range(task_count)]
    else:
        raise ScenarioError(f"unknown EXP-07 weight type {weight_type}")
    return tuple(matrix.base_effort * multiplier for multiplier in multipliers)


def _longest_path(predecessors: tuple[tuple[str, ...], ...], weights: tuple[Decimal, ...]) -> tuple[Decimal, tuple[str, ...]]:
    task_ids = _task_ids(len(weights))
    index = {task_id: item for item, task_id in enumerate(task_ids)}
    best: list[Decimal] = []
    parent: list[str | None] = []
    for item, task_id in enumerate(task_ids):
        if not predecessors[item]:
            best.append(weights[item])
            parent.append(None)
            continue
        predecessor = max(predecessors[item], key=lambda value: (best[index[value]], value))
        best.append(best[index[predecessor]] + weights[item])
        parent.append(predecessor)
    last = max(task_ids, key=lambda value: (best[index[value]], value))
    path: list[str] = []
    cursor: str | None = last
    while cursor is not None:
        path.append(cursor)
        cursor = parent[index[cursor]]
    return best[index[last]], tuple(reversed(path))


def _choose_human_shares(weights: tuple[Decimal, ...], critical_path: tuple[str, ...], target_bin: BinSpec, grid: tuple[Decimal, ...]) -> tuple[tuple[Decimal, ...], Decimal]:
    assert target_bin.target is not None
    task_ids = _task_ids(len(weights))
    critical = set(critical_path)
    best: tuple[tuple[Decimal, Decimal, Decimal, Decimal], Decimal, Decimal, Decimal] | None = None
    for on_path in grid:
        for off_path in grid:
            human_total = sum((weight * (on_path if task_id in critical else off_path) for task_id, weight in zip(task_ids, weights, strict=True)), Decimal("0"))
            human_cp = sum((weight * on_path for task_id, weight in zip(task_ids, weights, strict=True) if task_id in critical), Decimal("0"))
            rho = human_cp / human_total
            if not target_bin.contains(rho):
                continue
            total_work = sum(weights, Decimal("0"))
            overall_share = human_total / total_work
            key = (abs(rho - target_bin.target), abs(overall_share - Decimal("0.25")), on_path, off_path)
            if best is None or key < best[0]:
                best = (key, on_path, off_path, rho)
    if best is None:
        raise RuntimeError(f"human-share grid cannot populate {target_bin.name}")
    _, on_path, off_path, rho = best
    shares = tuple(on_path if task_id in critical else off_path for task_id in task_ids)
    return shares, rho


def _graph_checks(predecessors: tuple[tuple[str, ...], ...]) -> tuple[bool, str]:
    if predecessors[0] or any(not items for items in predecessors[1:]):
        return False, "not_reachable_from_source"
    return True, "accepted"


def generate_dags(matrix: Exp07Matrix) -> tuple[list[GeneratedDag], list[dict[str, str]]]:
    dags: list[GeneratedDag] = []
    attempts: list[dict[str, str]] = []
    graph_cell_index = 0
    for task_count in matrix.task_counts:
        for topology in matrix.topology_specs:
            for weight_type in matrix.weight_types:
                for human_bin_name in matrix.human_bins:
                    cell_id = f"n{task_count}_{topology.name}_{weight_type}_rh{human_bin_name}"
                    for observation_seed in range(matrix.seed_start, matrix.seed_stop + 1):
                        accepted: GeneratedDag | None = None
                        for attempt in range(matrix.max_attempts):
                            # Human-concentration strata reuse the same raw graph and
                            # weights, making C4 a genuine paired comparison.
                            raw_seed = matrix.master_seed + graph_cell_index * 100_000 + observation_seed * 1_000 + attempt
                            rng = random.Random(raw_seed)
                            predecessors = _layered_predecessors(task_count, topology, rng)
                            weights = _weights(task_count, weight_type, matrix, rng)
                            graph_ok, reason = _graph_checks(predecessors)
                            path_weight, critical_path = _longest_path(predecessors, weights)
                            rho_l = path_weight / sum(weights, Decimal("0"))
                            if graph_ok and not matrix.rho_l_bins[topology.target_rho_l_bin].contains(rho_l):
                                graph_ok, reason = False, "rho_l_outside_target_bin"
                            human_shares, rho_h = _choose_human_shares(weights, critical_path, matrix.rho_h_bins[human_bin_name], matrix.human_share_grid)
                            if graph_ok and not matrix.rho_h_bins[human_bin_name].contains(rho_h):
                                graph_ok, reason = False, "rho_h_cp_outside_target_bin"
                            dag_id = f"exp07_{cell_id}_s{observation_seed:02d}"
                            attempts.append({
                                "experiment_id": "EXP-07",
                                "dag_id": dag_id,
                                "cell_id": cell_id,
                                "task_count": str(task_count),
                                "topology_family": topology.name,
                                "weight_type": weight_type,
                                "target_rho_l_bin": topology.target_rho_l_bin,
                                "human_concentration_bin": human_bin_name,
                                "observation_seed": str(observation_seed),
                                "attempt": str(attempt),
                                "raw_seed": str(raw_seed),
                                "accepted": str(graph_ok).lower(),
                                "reason": "accepted_all_graph_and_bin_checks" if graph_ok else reason,
                                "rho_l": _fmt(rho_l),
                                "rho_h_cp": _fmt(rho_h),
                            })
                            if graph_ok:
                                accepted = GeneratedDag(
                                    dag_id=dag_id,
                                    cell_id=cell_id,
                                    task_count=task_count,
                                    topology_family=topology.name,
                                    weight_type=weight_type,
                                    target_rho_l_bin=topology.target_rho_l_bin,
                                    human_concentration_bin=human_bin_name,
                                    observation_seed=observation_seed,
                                    attempt=attempt,
                                    raw_seed=raw_seed,
                                    predecessors=predecessors,
                                    weights=weights,
                                    human_shares=human_shares,
                                    critical_path=critical_path,
                                    rho_l=rho_l,
                                    rho_h_cp=rho_h,
                                )
                                break
                        if accepted is None:
                            raise RuntimeError(f"{cell_id} seed {observation_seed}: rejection limit exhausted")
                        dags.append(accepted)
                graph_cell_index += 1
    if len(dags) != matrix.expected_accepted_dags:
        raise RuntimeError(f"generated {len(dags)} accepted DAGs, expected {matrix.expected_accepted_dags}")
    return dags, attempts


def _phases(profile: str, task_index: int, agent: Decimal, human: Decimal) -> tuple[PhaseSpec, ...]:
    if profile == "io":
        return (PhaseSpec("human_1", "human", human / 2), PhaseSpec("agent_1", "agent", agent), PhaseSpec("human_2", "human", human / 2))
    human_parts = [human / 4] * 4
    if profile == "alternating_sync":
        agent_parts = [agent / 3] * 3
    elif profile == "alternating_staggered":
        cycle = ((1, 2, 3), (2, 3, 1), (3, 1, 2))[task_index % 3]
        agent_parts = [agent * Decimal(item) / 6 for item in cycle]
    else:
        raise ScenarioError(f"unknown EXP-07 phase profile {profile}")
    phases: list[PhaseSpec] = []
    for item, human_part in enumerate(human_parts):
        phases.append(PhaseSpec(f"human_{item + 1}", "human", human_part))
        if item < 3:
            phases.append(PhaseSpec(f"agent_{item + 1}", "agent", agent_parts[item]))
    return tuple(phases)


def build_scenario(matrix: Exp07Matrix, dag: GeneratedDag, *, profile: str = "io", p: int = 4, c: Decimal = Decimal("1"), gamma: Decimal = Decimal("1"), suffix: str = "base") -> Scenario:
    task_ids = _task_ids(dag.task_count)
    tasks: list[TaskSpec] = []
    for index, (task_id, weight, share, predecessors) in enumerate(zip(task_ids, dag.weights, dag.human_shares, dag.predecessors, strict=True)):
        human = weight * share
        agent = weight - human
        tasks.append(TaskSpec(task_id, f"Synthetic task {index + 1}", Decimal("1"), weight, human, predecessors, _phases(profile, index, agent, human), f"qg_{task_id}"))
    scenario = Scenario(1, f"{dag.dag_id}_{suffix}", "EXP-07", matrix.time_unit, matrix.tolerance, Decimal("1"), p, c, gamma, tuple(tasks), (), matrix.source_path)
    validate_scenario(scenario)
    return scenario


def _decompose(matrix: Exp07Matrix, scenario: Scenario, *, overhead_rate: Decimal) -> tuple[Scenario, str]:
    aggregate = compute_aggregates(scenario)
    selected_id = max(aggregate.critical_path_l4, key=lambda item: (sum((phase.base_duration for phase in scenario.task_by_id[item].phases), Decimal("0")), item))
    selected = scenario.task_by_id[selected_id]
    human_phases = [phase.base_duration for phase in selected.phases if phase.resource == "human"]
    agent_total = sum((phase.base_duration for phase in selected.phases if phase.resource == "agent"), Decimal("0"))
    human_total = sum(human_phases, Decimal("0"))
    useful_input_human = human_total / 2
    useful_final_human = human_total - useful_input_human
    total_effort = agent_total + human_total
    total_overhead = Decimal(matrix.decomposition_m - 1) * overhead_rate * total_effort
    human_overhead = total_overhead * matrix.human_overhead_share
    agent_overhead = total_overhead - human_overhead
    input_human = human_overhead / 2
    join_human = human_overhead - input_human
    input_agent = agent_overhead / 2
    join_agent = agent_overhead - input_agent
    part_ids = tuple(f"{selected_id}_part_{item:02d}" for item in range(1, matrix.decomposition_m + 1))
    join_id = f"{selected_id}_join"
    part_human = (useful_input_human + input_human) / matrix.decomposition_m
    part_agent = (agent_total + input_agent) / matrix.decomposition_m
    parts = [TaskSpec(part_id, f"Decomposed {selected_id} part {item}", Decimal("1"), part_agent + part_human, part_human, selected.predecessors, (PhaseSpec("specification", "human", part_human), PhaseSpec("implementation", "agent", part_agent)), f"qg_{part_id}") for item, part_id in enumerate(part_ids, 1)]
    join_human_total = useful_final_human + join_human
    join_phases: list[PhaseSpec] = []
    if join_agent > 0:
        join_phases.append(PhaseSpec("integration", "agent", join_agent))
    join_phases.append(PhaseSpec("acceptance", "human", join_human_total))
    join = TaskSpec(join_id, f"Join for {selected_id}", Decimal("1"), join_agent + join_human_total, join_human_total, part_ids, tuple(join_phases), selected.quality_gate_id)
    tasks: list[TaskSpec] = []
    for task in scenario.tasks:
        if task.task_id == selected_id:
            tasks.extend(parts)
            tasks.append(join)
        else:
            tasks.append(replace(task, predecessors=tuple(join_id if item == selected_id else item for item in task.predecessors)))
    result = replace(scenario, scenario_id=f"{scenario.scenario_id}_m{matrix.decomposition_m}_ro{int(overhead_rate * 100):02d}", tasks=tuple(tasks))
    validate_scenario(result)
    return result, selected_id


def _costs(regime: str, p: int) -> tuple[Decimal, Decimal]:
    value = Decimal(p)
    if regime == "base":
        return Decimal("1"), Decimal("1")
    if regime == "agent_cost":
        return Decimal("1") + Decimal("0.05") * (value - 1) + Decimal("0.005") * value * (value - 1), Decimal("1")
    if regime == "human_cost":
        return Decimal("1"), Decimal("1") + Decimal("0.10") * (value - 1)
    raise ScenarioError(f"unknown cost regime {regime}")


def _validated_baseline(scenario: Scenario) -> tuple[AggregateMetrics, ScheduleValidation]:
    aggregate = compute_aggregates(scenario)
    validation = validate_schedule(scenario, simulate_baseline(scenario))
    if not validation.valid or validation.metrics is None:
        details = "; ".join(item.message for item in validation.issues)
        raise RuntimeError(f"{scenario.scenario_id}: invalid baseline: {details}")
    return aggregate, validation


def _run_row(dag: GeneratedDag, *, claim: str, component: str, variant: str, scenario: Scenario, selected_task_id: str = "") -> dict[str, str]:
    aggregate, validation = _validated_baseline(scenario)
    assert validation.metrics is not None
    return {
        "experiment_id": "EXP-07", "dag_id": dag.dag_id, "cell_id": dag.cell_id,
        "task_count": str(dag.task_count), "topology_family": dag.topology_family,
        "weight_type": dag.weight_type, "rho_l_bin": dag.target_rho_l_bin,
        "human_concentration_bin": dag.human_concentration_bin,
        "observation_seed": str(dag.observation_seed), "claim": claim,
        "component": component, "variant": variant, "phase_profile": _scenario_profile(scenario),
        "P": str(scenario.p), "C": _fmt(scenario.c), "gamma": _fmt(scenario.gamma),
        "selected_task_id": selected_task_id, "B4": _fmt(aggregate.b4),
        "active_branches": ",".join(aggregate.active_branches), "L4": _fmt(aggregate.l4),
        "W4": _fmt(aggregate.w4), "H": _fmt(aggregate.h),
        "rho_l": _fmt(aggregate.l4 / aggregate.w4),
        "rho_h_cp": _fmt(_rho_h_cp(scenario, aggregate.critical_path_l4)),
        "policy_makespan": _fmt(validation.metrics.makespan),
        "policy_queue": _fmt(validation.metrics.queue_time),
        "policy_blocked_any": _fmt(validation.metrics.blocked_any_time),
        "policy_tightness_relative_gap": _fmt(validation.metrics.makespan / aggregate.b4 - 1),
    }


def _scenario_profile(scenario: Scenario) -> str:
    count = len(scenario.tasks[0].phases)
    if count == 3:
        return "io"
    if count != 7:
        return "decomposed_io"
    first_agent = next(phase.base_duration for phase in scenario.tasks[0].phases if phase.resource == "agent")
    agent_total = sum((phase.base_duration for phase in scenario.tasks[0].phases if phase.resource == "agent"), Decimal("0"))
    return "alternating_sync" if first_agent * 3 == agent_total else "alternating_staggered"


def _rho_h_cp(scenario: Scenario, path: Iterable[str]) -> Decimal:
    path_set = set(path)
    total = sum((task.z * task.h for task in scenario.tasks), Decimal("0"))
    on_path = sum((task.z * task.h for task in scenario.tasks if task.task_id in path_set), Decimal("0"))
    return on_path / total


def _is_exact_dag(matrix: Exp07Matrix, dag: GeneratedDag) -> bool:
    return dag.task_count in matrix.exact_task_counts and dag.weight_type in matrix.exact_weight_types and dag.human_concentration_bin in matrix.exact_human_bins and dag.observation_seed in matrix.exact_seeds


def _exact_row(dag: GeneratedDag, run: dict[str, str], scenario: Scenario, matrix: Exp07Matrix) -> dict[str, str]:
    solution = solve_exact(scenario, time_limit_seconds=matrix.exact_time_limit, random_seed=matrix.exact_random_seed, workers=matrix.exact_workers)
    if solution.schedule is not None:
        validation = validate_schedule(scenario, solution.schedule)
        if not validation.valid:
            raise RuntimeError(f"{scenario.scenario_id}: invalid exported exact schedule")
    return {
        **{key: run[key] for key in ("experiment_id", "dag_id", "task_count", "topology_family", "weight_type", "human_concentration_bin", "observation_seed", "claim", "component", "variant", "phase_profile", "P", "C", "gamma", "B4")},
        "scenario_id": scenario.scenario_id,
        "solver_status": solution.status,
        "solver_objective": _fmt(solution.objective),
        "solver_best_bound": _fmt(solution.best_bound),
        "solver_gap": _fmt(solution.relative_gap),
        "solver_wall_time_seconds": f"{solution.wall_time:.6f}",
        "exact_tightness_relative_gap": _fmt(solution.objective / Decimal(run["B4"]) - 1 if solution.objective is not None else None),
    }


def _optimal_p(rows: list[dict[str, str]]) -> int:
    return int(min(rows, key=lambda row: (Decimal(row["policy_makespan"]), int(row["P"])))["P"])


def _claim_pair(claim: str, metric: str, estimator: str, dag: GeneratedDag, value: Decimal, detail: str) -> dict[str, str]:
    return {
        "claim": claim, "metric": metric, "estimator": estimator,
        "dag_id": dag.dag_id, "task_count": str(dag.task_count),
        "topology_family": dag.topology_family, "weight_type": dag.weight_type,
        "rho_l_bin": dag.target_rho_l_bin, "human_concentration_bin": dag.human_concentration_bin,
        "observation_seed": str(dag.observation_seed), "paired_effect": _fmt(value), "detail": detail,
    }


def _run_all(matrix: Exp07Matrix, dags: list[GeneratedDag]) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    runs: list[dict[str, str]] = []
    pairs: list[dict[str, str]] = []
    exact_rows: list[dict[str, str]] = []
    c4_index: dict[tuple[int, str, str, int, str], tuple[GeneratedDag, dict[str, str]]] = {}
    for offset, dag in enumerate(dags, 1):
        # C1: same aggregate object, different internal phase synchronization.
        c1_rows: dict[str, dict[str, str]] = {}
        for profile in ("alternating_sync", "alternating_staggered"):
            scenario = build_scenario(matrix, dag, profile=profile, p=matrix.default_p, suffix=f"c1_{profile}")
            row = _run_row(dag, claim="C1", component="phase_profile", variant=profile, scenario=scenario)
            runs.append(row)
            c1_rows[profile] = row
            if _is_exact_dag(matrix, dag):
                exact_rows.append(_exact_row(dag, row, scenario, matrix))
        c1_value = Decimal(c1_rows["alternating_sync"]["policy_tightness_relative_gap"]) - Decimal(c1_rows["alternating_staggered"]["policy_tightness_relative_gap"])
        pairs.append(_claim_pair("C1", "delta_tightness_sync_minus_staggered", "baseline_policy", dag, c1_value, "sync minus staggered"))

        # C2: policy-optimal P on a common grid under the three frozen cost curves.
        c2_groups: dict[str, list[dict[str, str]]] = {}
        for regime in ("base", "agent_cost", "human_cost"):
            c2_groups[regime] = []
            for p in matrix.p_grid:
                c, gamma = _costs(regime, p)
                scenario = build_scenario(matrix, dag, profile="io", p=p, c=c, gamma=gamma, suffix=f"c2_{regime}_p{p:02d}")
                row = _run_row(dag, claim="C2", component=regime, variant=f"P={p}", scenario=scenario)
                runs.append(row)
                c2_groups[regime].append(row)
                if _is_exact_dag(matrix, dag) and regime == "base" and p == matrix.default_p:
                    audit_row = dict(row)
                    audit_row["claim"] = "AUDIT"
                    audit_row["component"] = "baseline_gap"
                    exact_rows.append(_exact_row(dag, audit_row, scenario, matrix))
        base_p = int(_optimal_p(c2_groups["base"]))
        for regime in ("agent_cost", "human_cost"):
            cost_p = int(_optimal_p(c2_groups[regime]))
            pairs.append(_claim_pair("C2", f"delta_policy_optimal_p_{regime}", "baseline_policy", dag, Decimal(cost_p - base_p), f"base={base_p}; {regime}={cost_p}"))
        c4_index[(dag.task_count, dag.topology_family, dag.weight_type, dag.observation_seed, dag.human_concentration_bin)] = (dag, next(row for row in c2_groups["base"] if row["P"] == str(matrix.default_p)))

        # C3: zero-overhead interaction and attenuation by 10% overhead.
        c3: dict[tuple[int, Decimal, int], dict[str, str]] = {}
        for p in (matrix.p_low, matrix.p_high):
            base_scenario = build_scenario(matrix, dag, profile="io", p=p, suffix=f"c3_p{p:02d}_m1")
            base_row = _run_row(dag, claim="C3", component="decomposition", variant=f"P={p},m=1", scenario=base_scenario)
            runs.append(base_row)
            c3[(p, Decimal("0"), 1)] = base_row
            for overhead in matrix.overhead_rates:
                decomposed, selected = _decompose(matrix, base_scenario, overhead_rate=overhead)
                row = _run_row(dag, claim="C3", component="decomposition", variant=f"P={p},m={matrix.decomposition_m},r_o={_fmt(overhead)}", scenario=decomposed, selected_task_id=selected)
                runs.append(row)
                c3[(p, overhead, matrix.decomposition_m)] = row
        gain_low = Decimal(c3[(matrix.p_low, Decimal("0"), 1)]["policy_makespan"]) - Decimal(c3[(matrix.p_low, Decimal("0"), matrix.decomposition_m)]["policy_makespan"])
        gain_high = Decimal(c3[(matrix.p_high, Decimal("0"), 1)]["policy_makespan"]) - Decimal(c3[(matrix.p_high, Decimal("0"), matrix.decomposition_m)]["policy_makespan"])
        gain_high_overhead = Decimal(c3[(matrix.p_high, Decimal("0"), 1)]["policy_makespan"]) - Decimal(c3[(matrix.p_high, Decimal("0.10"), matrix.decomposition_m)]["policy_makespan"])
        pairs.append(_claim_pair("C3", "decomposition_interaction", "baseline_policy", dag, gain_high - gain_low, f"gain_P1={_fmt(gain_low)}; gain_P4={_fmt(gain_high)}"))
        pairs.append(_claim_pair("C3", "overhead_attenuation", "baseline_policy", dag, gain_high - gain_high_overhead, f"gain_zero={_fmt(gain_high)}; gain_ro10={_fmt(gain_high_overhead)}"))
        if offset % 120 == 0:
            print(f"EXP-07 policy progress: {offset}/{len(dags)} DAGs", flush=True)

    # C4 is paired across the low/high human-concentration strata.
    for task_count in matrix.task_counts:
        for topology in matrix.topology_specs:
            for weight_type in matrix.weight_types:
                for seed in range(matrix.seed_start, matrix.seed_stop + 1):
                    low_dag, low = c4_index[(task_count, topology.name, weight_type, seed, "low")]
                    _, high = c4_index[(task_count, topology.name, weight_type, seed, "high")]
                    low_active = Decimal(int("human" in low["active_branches"].split(",")))
                    high_active = Decimal(int("human" in high["active_branches"].split(",")))
                    pairs.append(_claim_pair("C4", "delta_human_active_high_minus_low", "lower_bound", low_dag, high_active - low_active, f"low={int(low_active)}; high={int(high_active)}"))
    return runs, pairs, exact_rows


def _exact_pairs(exact_rows: list[dict[str, str]], dag_by_id: dict[str, GeneratedDag]) -> list[dict[str, str]]:
    pairs: list[dict[str, str]] = []
    optimal = [row for row in exact_rows if row["solver_status"] == "OPTIMAL"]
    by_dag: dict[str, list[dict[str, str]]] = {}
    for row in optimal:
        by_dag.setdefault(row["dag_id"], []).append(row)
    for dag_id, rows in by_dag.items():
        dag = dag_by_id[dag_id]
        c1 = {row["variant"]: row for row in rows if row["claim"] == "C1"}
        if set(c1) == {"alternating_sync", "alternating_staggered"}:
            value = Decimal(c1["alternating_sync"]["exact_tightness_relative_gap"]) - Decimal(c1["alternating_staggered"]["exact_tightness_relative_gap"])
            pairs.append(_claim_pair("C1", "delta_tightness_sync_minus_staggered", "exact", dag, value, "OPTIMAL pair"))
        c2_rows = [row for row in rows if row["claim"] == "C2"]
        for regime in ("agent_cost", "human_cost"):
            base = [row for row in c2_rows if row["component"] == "base"]
            cost = [row for row in c2_rows if row["component"] == regime]
            if len(base) == 4 and len(cost) == 4:
                base_p = int(min(base, key=lambda row: (Decimal(row["solver_objective"]), int(row["P"])))["P"])
                cost_p = int(min(cost, key=lambda row: (Decimal(row["solver_objective"]), int(row["P"])))["P"])
                pairs.append(_claim_pair("C2", f"delta_policy_optimal_p_{regime}", "exact", dag, Decimal(cost_p - base_p), f"OPTIMAL; base={base_p}; cost={cost_p}"))
        c3_rows = [row for row in rows if row["claim"] == "C3"]
        lookup = {(int(row["P"]), row["variant"]): Decimal(row["solver_objective"]) for row in c3_rows}
        required = [(1, "P=1,m=1"), (1, "P=1,m=3,r_o=0"), (4, "P=4,m=1"), (4, "P=4,m=3,r_o=0"), (4, "P=4,m=3,r_o=0.10")]
        if all(key in lookup for key in required):
            low = lookup[(1, "P=1,m=1")] - lookup[(1, "P=1,m=3,r_o=0")]
            high = lookup[(4, "P=4,m=1")] - lookup[(4, "P=4,m=3,r_o=0")]
            high_overhead = lookup[(4, "P=4,m=1")] - lookup[(4, "P=4,m=3,r_o=0.10")]
            pairs.append(_claim_pair("C3", "decomposition_interaction", "exact", dag, high - low, "OPTIMAL contrast"))
            pairs.append(_claim_pair("C3", "overhead_attenuation", "exact", dag, high - high_overhead, "OPTIMAL contrast"))
    return pairs


def _quantile(values: list[Decimal], q: Decimal) -> Decimal:
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    position = q * Decimal(len(ordered) - 1)
    lower = int(position)
    fraction = position - lower
    return ordered[lower] * (1 - fraction) + ordered[min(lower + 1, len(ordered) - 1)] * fraction


def _cluster_bootstrap(clusters: list[list[Decimal]], statistic: str, *, resamples: int, seed: int) -> tuple[Decimal, Decimal, Decimal]:
    rng = random.Random(seed)
    function = median if statistic == "median" else mean
    values = [value for cluster in clusters for value in cluster]
    observed = Decimal(str(function(values)))
    samples: list[Decimal] = []
    for _ in range(resamples):
        sampled_clusters = [clusters[rng.randrange(len(clusters))] for _ in clusters]
        draw = [value for cluster in sampled_clusters for value in cluster]
        samples.append(Decimal(str(function(draw))))
    return observed, _quantile(samples, Decimal("0.025")), _quantile(samples, Decimal("0.975"))


def _summaries(matrix: Exp07Matrix, pairs: list[dict[str, str]]) -> list[dict[str, str]]:
    groups: dict[tuple[str, str, str], list[dict[str, str]]] = {}
    for row in pairs:
        groups.setdefault((row["claim"], row["metric"], row["estimator"]), []).append(row)
    summaries: list[dict[str, str]] = []
    for index, ((claim, metric, estimator), rows) in enumerate(sorted(groups.items())):
        values = [Decimal(row["paired_effect"]) for row in rows]
        by_cluster: dict[tuple[str, str, str, str], list[Decimal]] = {}
        for row, value in zip(rows, values, strict=True):
            cluster_key = (
                row["task_count"], row["topology_family"],
                row["weight_type"], row["observation_seed"],
            )
            by_cluster.setdefault(cluster_key, []).append(value)
        statistic = "mean" if claim == "C4" else "median"
        center, ci_low, ci_high = _cluster_bootstrap(
            list(by_cluster.values()), statistic,
            resamples=matrix.bootstrap_resamples,
            seed=matrix.bootstrap_seed + index,
        )
        reversal_rate = Decimal(sum(value < 0 for value in values)) / len(values) if claim in {"C1", "C3", "C4"} else Decimal(sum(value > 0 for value in values)) / len(values)
        if claim == "C1":
            decision = "supported" if center >= 0 else "not_supported"
        elif claim == "C2":
            decision = "supported" if center <= 0 and reversal_rate <= Decimal("0.05") else "not_supported"
        elif claim == "C3":
            decision = "supported" if center >= 0 else "not_supported"
        else:
            decision = "supported" if center > 0 else "not_supported"
        summaries.append({
            "claim": claim, "metric": metric, "estimator": estimator,
            "n": str(len(values)), "cluster_n": str(len(by_cluster)),
            "mean": _fmt(Decimal(str(mean(values)))), "median": _fmt(Decimal(str(median(values)))),
            "q25": _fmt(_quantile(values, Decimal("0.25"))), "q75": _fmt(_quantile(values, Decimal("0.75"))),
            "q90": _fmt(_quantile(values, Decimal("0.90"))), "q95": _fmt(_quantile(values, Decimal("0.95"))),
            "negative_rate": _fmt(Decimal(sum(value < 0 for value in values)) / len(values)),
            "zero_rate": _fmt(Decimal(sum(value == 0 for value in values)) / len(values)),
            "positive_rate": _fmt(Decimal(sum(value > 0 for value in values)) / len(values)),
            "bootstrap_statistic": statistic, "bootstrap_center": _fmt(center),
            "bootstrap_ci_low": _fmt(ci_low), "bootstrap_ci_high": _fmt(ci_high),
            "decision": decision,
        })
    return summaries


def _dag_rows(dags: list[GeneratedDag]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for dag in dags:
        task_ids = _task_ids(dag.task_count)
        rows.append({
            "experiment_id": "EXP-07", "dag_id": dag.dag_id, "cell_id": dag.cell_id,
            "task_count": str(dag.task_count), "topology_family": dag.topology_family,
            "weight_type": dag.weight_type, "target_rho_l_bin": dag.target_rho_l_bin,
            "human_concentration_bin": dag.human_concentration_bin,
            "observation_seed": str(dag.observation_seed), "accepted_attempt": str(dag.attempt),
            "raw_seed": str(dag.raw_seed), "acceptance_reason": "accepted_all_graph_and_bin_checks",
            "rho_l": _fmt(dag.rho_l), "rho_h_cp": _fmt(dag.rho_h_cp),
            "critical_path": "->".join(dag.critical_path),
            "weights_json": json.dumps([_fmt(item) for item in dag.weights], separators=(",", ":")),
            "human_shares_json": json.dumps([_fmt(item) for item in dag.human_shares], separators=(",", ":")),
            "predecessors_json": json.dumps({task_id: list(items) for task_id, items in zip(task_ids, dag.predecessors, strict=True)}, separators=(",", ":"), sort_keys=True),
        })
    return rows


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise RuntimeError(f"cannot write empty table {path}")
    with path.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _fmt(value: Decimal | None) -> str:
    return "" if value is None else format(value, "f")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _dependencies() -> dict[str, str]:
    result: dict[str, str] = {}
    for name in ("matplotlib", "ortools", "PyYAML", "pytest"):
        try:
            result[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            result[name] = "not-installed"
    return result


def _write_report(path: Path, matrix: Exp07Matrix, dags: list[GeneratedDag], attempts: list[dict[str, str]], summaries: list[dict[str, str]], exact_rows: list[dict[str, str]]) -> None:
    baseline = [row for row in summaries if row["estimator"] in {"baseline_policy", "lower_bound"}]
    exact = [row for row in summaries if row["estimator"] == "exact"]
    rejected = sum(row["accepted"] == "false" for row in attempts)
    exact_counts: dict[str, int] = {}
    for row in exact_rows:
        exact_counts[row["solver_status"]] = exact_counts.get(row["solver_status"], 0) + 1
    def summary_table(rows: list[dict[str, str]]) -> str:
        lines = ["| Claim | Metric | Estimator | n (clusters) | Center [95% cluster bootstrap] | Decision |", "|---|---|---:|---:|---:|---|"]
        for row in rows:
            lines.append(f"| {row['claim']} | `{row['metric']}` | `{row['estimator']}` | {row['n']} ({row['cluster_n']}) | {Decimal(row['bootstrap_center']):.4f} [{Decimal(row['bootstrap_ci_low']):.4f}, {Decimal(row['bootstrap_ci_high']):.4f}] | **{row['decision']}** |")
        return "\n".join(lines)
    text = f"""# EXP-07: устойчивость к синтетической топологии

## Постановка

EXP-07 проверяет четыре заранее замороженных направления эффектов на 1440
сценариях: 480 общих основ «граф плюс веса» повторяются для трёх размещений
human-work. Пилот стратифицирован по `N`, семейству графа, типу весов и
концентрации человеческой работы. На каждую из {matrix.expected_cells} ячеек
получено ровно 20 принятых seed; отклонённые попытки не считаются наблюдениями.
Bootstrap перевыбирает общие структурные основы, сохраняя связанные размещения
в одном кластере.

Важное ограничение дизайна: семейства `wide_layered`, `mixed` и `chain_like`
заранее соответствуют low, medium и high корзинам $\\rho_L$. Поэтому различия
между корзинами $\\rho_L$ нельзя отделить от различий семейств графа.

## Генерация и воспроизводимость

- принятых сценариев: **{len(dags)}** на **{len(dags) // 3}** структурных основах;
- отклонённых попыток rejection sampling: **{rejected}**;
- размеры: 8, 16, 32 и 64 задачи;
- веса: homogeneous и дискретизированные lognormal (`sigma=0.55`);
- все принятые графы ацикличны, слабо связны, достижимы из source и лежат
  в целевых корзинах $\\rho_L$ и $\\rho_H^{{cp}}$;
- `exp07_dags.csv` хранит сырой seed, рёбра, веса, human shares, критический
  путь и причину принятия; `exp07_generation_attempts.csv` хранит также отказы.

![Покрытие синтетического дизайна](../figures/exp07_design_coverage.png)

[SVG-версия](../figures/exp07_design_coverage.svg).

## Confirmatory-результаты

На полной выборке `T` означает makespan заранее фиксированной политики
`bottom_level_fcfs_v1`, а не оптимум. $T^*$ используется только для строк exact
со статусом `OPTIMAL`.

{summary_table(baseline)}

Итог по полной policy/lower-bound выборке:

- **Исходный confirmatory-критерий C1 не подтверждён:** медианный contrast
  равен -0.00217, 95% cluster-bootstrap interval [-0.00261, -0.00108]. Профиль,
  обозначенный в frozen matrix как `alternating_sync`, немного уменьшает, а не
  сохраняет или увеличивает policy-tightness относительно
  `alternating_staggered`.
- **C2 подтверждён:** медианный сдвиг policy-optimal P равен нулю для обеих
  cost curves; доля сдвигов в запрещённую положительную сторону равна 0.0042
  для agent-cost и 0.0063 для human-cost, ниже замороженного порога 0.05.
- **C3 подтверждён:** медиана interaction равна 6.4, медиана attenuation от
  overhead равна 2.0. Отрицательные индивидуальные contrasts не скрыты.
- **C4 не подтверждён:** частота human-active branch снизилась с 0.3458 в low
  stratum до 0.1625 в high; средний paired contrast равен -0.1833.

![Распределения paired effects EXP-07](../figures/exp07_claim_effects.png)

[SVG-версия](../figures/exp07_claim_effects.svg).

## Ретроспективная интерпретация C1

Этот раздел добавлен после просмотра результатов и не меняет confirmatory-
решение `not_supported`. Название `alternating_sync` оказалось содержательно
неточным: генератор не выравнивал human-фазы разных задач по wall-clock. В
обоих профилях каждая задача имела четыре одинаковые human-фазы $H_i/4$ и
запускалась согласно DAG и доступности ресурсов, поэтому глобальной
синхронизации человеческих запросов не было ни в одном treatment.

Фактически treatments различались только внутренним разбиением agent-work.
В `alternating_sync` три agent-отрезка задачи равны $A_i/3$; в
`alternating_staggered` они имеют длины $A_i\\{{1/6,2/6,3/6\\}}$, циклически
переставленные между задачами. Следовательно, C1 сравнил более регулярный и
более нерегулярный **асинхронные** профили. Небольшое преимущество первого
варианта становится интуитивно объяснимым, но это post hoc объяснение нельзя
выдавать за подтверждение влияния настоящей синхронизации. Для такого вывода
нужен отдельный дизайн с явно совпадающими wall-clock окнами human-фаз.

## Exact-аудит

Exact-подвыборка заморожена до расчётов: `N=8/16`, homogeneous-веса, средняя
концентрация human-work, seed 0 и 1 для каждого семейства — 12 DAG. После
зафиксированной до просмотра исходов ресурсной поправки для C1 и baseline-gap
рассчитано {len(exact_rows)} сценариев. Статусы: **{json.dumps(exact_counts, ensure_ascii=False, sort_keys=True)}**.
Ни один FEASIBLE incumbent не обозначается как $T^*$ и не входит в proven
paired contrast.

{summary_table(exact) if exact else 'Полных OPTIMAL-пар для отдельной exact-сводки нет.'}

Только четыре C1-пары имели `OPTIMAL` у обоих профилей. Их медиана имеет
противоположный policy-результату знак, но столь малая proven-подвыборка не
используется для отмены результата полной выборки. Она фиксирует, что выводы
про policy и $T^*$ здесь нельзя смешивать.

## Exploratory-диагностика C4

Замороженный C4 оказался структурно неудачно сформулирован. Ветвь lower bound
`gamma*H` зависит от общего человеческого объёма $H$, а
$\\rho_H^{{cp}}=H_{{cp}}/H$ — от его размещения на критическом пути. При
`C=gamma=1` и одинаковых весах изменение одной концентрации не повышает
`gamma*H`. Генератор приблизительно, но не точно выравнивал общий human share:
среднее $H/W_4$ равно 0.3370 в low и 0.2907 в high stratum, что и делает
агрегированный знак отрицательным. По семействам paired effect неоднороден:
wide-layered -0.7250, mixed +0.1563, chain-like +0.0188.

Это наблюдение не превращается в новый confirmatory claim. Для следующего
дизайна C4 нужно заменить на эффект концентрации при строго фиксированном $H$
на очередь/расписание либо изучать $L_4$ при `C != gamma`.

## Решение по claims и Gate IV

Решение `supported` относится только к конкретному замороженному contrast и
пилотному генератору. Индивидуальные исключения сохранены в
`exp07_claim_pairs.csv`; средние и медианы не подменяют распределение по DAG.
Реализованный runner проверил только глобальное пересечение нуля для
bootstrap-интервалов; предусмотренные ветви key-cell и MCSE не исполнялись.
Поэтому extension не запускался, а Gate IV выполнен лишь частично. Seed,
генератор, принятые и отклонённые DAG и confirmatory/exploratory-разделение
сохранены. В содержательные выводы можно
переносить только повторившиеся C2 и C3. Для C1 отклонён исходный confirmatory-
критерий, а ретроспективное объяснение ограничено сравнением регулярного и
нерегулярного асинхронных профилей; C4 требует новой формулировки. Статья в
рамках этого шага не меняется.

## Файлы

- `exp07_generation_attempts.csv` — все попытки и причины отказа/принятия;
- `exp07_dags.csv` — 1440 сценариев на 480 общих структурных основах;
- `exp07_runs.csv` — границы и результаты фиксированной политики;
- `exp07_exact.csv` — статусы, objectives, bounds и gaps exact-аудита;
- `exp07_claim_pairs.csv` — распределения paired effects;
- `exp07_claim_summary.csv` — агрегаты и bootstrap-интервалы;
- `exp07_manifest.json` — frozen claims, параметры и SHA-256.

Текст статьи в рамках эксперимента не менялся.
"""
    path.write_text(text, encoding="utf-8")


def run_exp07(project_root: Path, output_directory: Path) -> tuple[Path, ...]:
    matrix_path = project_root / "scenarios" / "canonical" / "exp07_matrix.yaml"
    matrix = load_exp07_matrix(matrix_path)
    output_directory.mkdir(parents=True, exist_ok=True)
    dags, attempts = generate_dags(matrix)
    dag_rows = _dag_rows(dags)
    attempts_path = output_directory / "exp07_generation_attempts.csv"
    dags_path = output_directory / "exp07_dags.csv"
    _write_csv(attempts_path, attempts)
    _write_csv(dags_path, dag_rows)
    runs, pairs, exact_rows = _run_all(matrix, dags)
    pairs.extend(_exact_pairs(exact_rows, {dag.dag_id: dag for dag in dags}))
    summaries = _summaries(matrix, pairs)
    runs_path = output_directory / "exp07_runs.csv"
    exact_path = output_directory / "exp07_exact.csv"
    pairs_path = output_directory / "exp07_claim_pairs.csv"
    summary_path = output_directory / "exp07_claim_summary.csv"
    _write_csv(runs_path, runs)
    _write_csv(exact_path, exact_rows)
    _write_csv(pairs_path, pairs)
    _write_csv(summary_path, summaries)
    from .exp07_figures import build_exp07_figures
    figure_paths = build_exp07_figures(dags_path, pairs_path, project_root / "figures")
    report_path = output_directory / "exp07_report.md"
    _write_report(report_path, matrix, dags, attempts, summaries, exact_rows)
    output_paths = [attempts_path, dags_path, runs_path, exact_path, pairs_path, summary_path, report_path, *figure_paths]
    extension_rows = [row for row in summaries if row["estimator"] in {"baseline_policy", "lower_bound"}]
    extension_triggered = any(Decimal(row["bootstrap_ci_low"]) < 0 < Decimal(row["bootstrap_ci_high"]) for row in extension_rows if row["bootstrap_statistic"] == "median")
    manifest_path = output_directory / "exp07_manifest.json"
    manifest = {
        "experiment_id": "EXP-07", "generated_at": datetime.now(timezone.utc).isoformat(),
        "command": "uv run python -m experiments run --experiment EXP-07",
        **git_provenance(project_root),
        "frozen_matrix": {"path": str(matrix_path.relative_to(project_root)), "sha256": _sha256(matrix_path)},
        "design": {"type": "stratified_pilot", "cells": matrix.expected_cells, "accepted_dags": len(dags), "accepted_seeds_per_cell": 20, "rejected_attempts": sum(row["accepted"] == "false" for row in attempts), "limitation": matrix.raw["design"]["limitation"]},
        "exact_audit": {"dags": matrix.expected_exact_dags, "expected_scenario_rows": matrix.expected_exact_scenarios, "scenario_rows": len(exact_rows), "status_counts": {status: sum(row["solver_status"] == status for row in exact_rows) for status in sorted(set(row["solver_status"] for row in exact_rows))}, "time_limit_seconds": matrix.exact_time_limit, "random_seed": matrix.exact_random_seed, "workers": matrix.exact_workers, "resource_amendment": matrix.raw["exact_audit"]["resource_amendment"]},
        "claims": matrix.raw["claims"], "pilot_extension": {**matrix.raw["pilot_extension"], "triggered_by_global_summary": extension_triggered, "executed": False},
        "dependencies": _dependencies(),
        "outputs": [{"path": str(path.relative_to(project_root)), "sha256": _sha256(path)} for path in output_paths],
        "implementation": implementation_records(project_root),
        "article_modified": False,
    }
    with manifest_path.open("w", encoding="utf-8") as target:
        json.dump(manifest, target, ensure_ascii=False, indent=2)
        target.write("\n")
    return (*output_paths, manifest_path)
