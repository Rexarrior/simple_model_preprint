from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR
import hashlib
import importlib.metadata
import json
from pathlib import Path
import random
from statistics import mean, median
import time
from typing import Any, Iterable

import yaml

from .bounds import AggregateMetrics, compute_aggregates
from .exact_solver import solve_exact
from .exp07 import TopologySpec, _graph_checks, _layered_predecessors, _task_ids
from .provenance import git_provenance, implementation_records
from .schema import PhaseSpec, Scenario, ScenarioError, TaskSpec, decimal, validate_scenario
from .simulator import simulate_baseline
from .validator import validate_schedule


@dataclass(frozen=True)
class RangeSpec:
    lower: Decimal
    upper: Decimal
    upper_inclusive: bool

    def contains(self, value: Decimal) -> bool:
        return self.lower <= value and (
            value <= self.upper if self.upper_inclusive else value < self.upper
        )


@dataclass(frozen=True)
class StreamSpec:
    name: str
    namespace: str
    start: int
    stop: int
    expected_graphs: int


@dataclass(frozen=True)
class Exp08Matrix:
    source_path: Path
    raw: dict[str, Any]
    task_counts: tuple[int, ...]
    topology_specs: tuple[TopologySpec, ...]
    weight_types: tuple[str, ...]
    streams: dict[str, StreamSpec]
    expected_cells: int
    max_attempts: int
    time_unit: Decimal
    allocation_tick: Decimal
    tolerance: Decimal
    base_effort: Decimal
    rho_l_bins: dict[str, RangeSpec]
    total_human_share: Decimal
    concentrations: dict[str, Decimal]
    share_lower: Decimal
    share_upper: Decimal
    concentration_tolerance: Decimal
    phase_profiles: tuple[str, ...]
    agent_counts: tuple[int, ...]
    equivalence_margin: Decimal
    sensitivity_margins: tuple[Decimal, ...]
    c_gamma_equal: tuple[Decimal, Decimal]
    slowdown_c: Decimal
    slowdown_gamma: Decimal
    slowdown_p: int
    bootstrap_resamples: int
    bootstrap_seed: int


@dataclass(frozen=True)
class GraphBase:
    dag_id: str
    stream: str
    cell_id: str
    task_count: int
    topology_family: str
    weight_type: str
    target_rho_l_bin: str
    observation_index: int
    accepted_attempt: int
    raw_seed: int
    predecessors: tuple[tuple[str, ...], ...]
    weights: tuple[Decimal, ...]
    reference_path: tuple[str, ...]
    reference_path_weight: Decimal
    longest_path_count: int
    rho_l: Decimal
    human_low: tuple[Decimal, ...]
    human_high: tuple[Decimal, ...]
    rho_h_low: Decimal
    rho_h_high: Decimal

    @property
    def path_multiplicity(self) -> str:
        return "unique" if self.longest_path_count == 1 else "tied"


def _mapping(raw: object, *, field: str) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise ScenarioError(f"{field}: expected mapping")
    return raw


def _list(raw: object, *, field: str) -> list[object]:
    if not isinstance(raw, list) or not raw:
        raise ScenarioError(f"{field}: expected non-empty list")
    return raw


def load_exp08_matrix(path: str | Path) -> Exp08Matrix:
    source_path = Path(path).resolve()
    with source_path.open(encoding="utf-8") as source:
        raw = yaml.safe_load(source)
    data = _mapping(raw, field="EXP-08 matrix")
    design = _mapping(data.get("design"), field="design")
    generator = _mapping(data.get("generator"), field="generator")
    streams_raw = _mapping(design.get("streams"), field="design.streams")
    streams: dict[str, StreamSpec] = {}
    for name, value in streams_raw.items():
        item = _mapping(value, field=f"design.streams.{name}")
        indices = _mapping(item.get("observation_indices"), field="observation_indices")
        streams[str(name)] = StreamSpec(
            name=str(name),
            namespace=str(item.get("namespace")),
            start=int(indices.get("start")),
            stop=int(indices.get("stop")),
            expected_graphs=int(item.get("expected_graphs")),
        )
    topology_raw = _mapping(generator.get("topology"), field="generator.topology")
    rho_bins: dict[str, RangeSpec] = {}
    for name, value in _mapping(generator.get("rho_l_bins"), field="rho_l_bins").items():
        item = _mapping(value, field=f"rho_l_bins.{name}")
        rho_bins[str(name)] = RangeSpec(
            decimal(item.get("lower"), field="lower"),
            decimal(item.get("upper"), field="upper"),
            bool(item.get("upper_inclusive", False)),
        )
    allocation = _mapping(data.get("allocation"), field="allocation")
    bounds = _mapping(allocation.get("task_human_share_bounds"), field="share_bounds")
    schedule = _mapping(data.get("schedule_effect"), field="schedule_effect")
    slowdown = _mapping(data.get("differentiated_slowdown"), field="differentiated_slowdown")
    reporting = _mapping(data.get("reporting"), field="reporting")
    matrix = Exp08Matrix(
        source_path=source_path,
        raw=data,
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
        streams=streams,
        expected_cells=int(design.get("expected_cells")),
        max_attempts=int(generator.get("max_attempts_per_observation")),
        time_unit=decimal(generator.get("time_unit"), field="time_unit"),
        allocation_tick=decimal(generator.get("allocation_tick"), field="allocation_tick"),
        tolerance=decimal(generator.get("tolerance"), field="tolerance"),
        base_effort=decimal(generator.get("base_effort"), field="base_effort"),
        rho_l_bins=rho_bins,
        total_human_share=decimal(allocation.get("total_human_share"), field="total_human_share"),
        concentrations={str(name): decimal(value, field=f"concentration.{name}") for name, value in _mapping(allocation.get("reference_path_concentrations"), field="concentrations").items()},
        share_lower=decimal(bounds.get("lower"), field="share_lower"),
        share_upper=decimal(bounds.get("upper"), field="share_upper"),
        concentration_tolerance=decimal(allocation.get("concentration_tolerance"), field="concentration_tolerance"),
        phase_profiles=tuple(str(item) for item in _list(schedule.get("phase_profiles"), field="phase_profiles")),
        agent_counts=tuple(int(item) for item in _list(schedule.get("agent_counts"), field="agent_counts")),
        equivalence_margin=decimal(schedule.get("equivalence_margin"), field="equivalence_margin"),
        sensitivity_margins=tuple(decimal(item, field="sensitivity_margin") for item in _list(schedule.get("sensitivity_margins"), field="sensitivity_margins")),
        c_gamma_equal=(decimal(schedule.get("c"), field="schedule.c"), decimal(schedule.get("gamma"), field="schedule.gamma")),
        slowdown_c=decimal(slowdown.get("c"), field="slowdown.c"),
        slowdown_gamma=decimal(slowdown.get("gamma"), field="slowdown.gamma"),
        slowdown_p=int(slowdown.get("agent_count")),
        bootstrap_resamples=int(reporting.get("bootstrap_resamples")),
        bootstrap_seed=int(reporting.get("bootstrap_seed")),
    )
    _validate_matrix(matrix)
    return matrix


def _validate_matrix(matrix: Exp08Matrix) -> None:
    if matrix.raw.get("schema_version") != 1 or matrix.raw.get("experiment_id") != "EXP-08" or matrix.raw.get("frozen") is not True:
        raise ScenarioError("EXP-08 requires a frozen schema v1 matrix")
    if matrix.task_counts != (8, 16, 32, 64):
        raise ScenarioError("EXP-08 task counts differ from the frozen matrix")
    if tuple(item.name for item in matrix.topology_specs) != ("wide_layered", "mixed", "chain_like"):
        raise ScenarioError("EXP-08 topology order differs from the frozen matrix")
    if matrix.weight_types != ("homogeneous", "lognormal") or matrix.expected_cells != 24:
        raise ScenarioError("EXP-08 graph cells differ from the frozen matrix")
    if set(matrix.streams) != {"development", "confirmatory"}:
        raise ScenarioError("EXP-08 requires separate development and confirmatory streams")
    development = matrix.streams["development"]
    confirmatory = matrix.streams["confirmatory"]
    if development.namespace == confirmatory.namespace:
        raise ScenarioError("EXP-08 stream namespaces must differ")
    for stream, count in ((development, 10), (confirmatory, 20)):
        if stream.stop - stream.start + 1 != count or stream.expected_graphs != matrix.expected_cells * count:
            raise ScenarioError(f"EXP-08 {stream.name} stream count mismatch")
    if matrix.concentrations != {"low": Decimal("0.30"), "high": Decimal("0.70")}:
        raise ScenarioError("EXP-08 allocation targets differ from the frozen matrix")
    if matrix.total_human_share != Decimal("0.12") or matrix.phase_profiles != ("io", "equal_alternating"):
        raise ScenarioError("EXP-08 allocation or phase profiles differ from the frozen matrix")
    if matrix.agent_counts != (1, 4, 8) or matrix.c_gamma_equal != (Decimal("1"), Decimal("1")):
        raise ScenarioError("EXP-08 schedule design differs from the frozen matrix")
    if (matrix.slowdown_c, matrix.slowdown_gamma, matrix.slowdown_p) != (Decimal("1"), Decimal("1.3"), 4):
        raise ScenarioError("EXP-08 differentiated slowdown differs from the frozen matrix")
    if matrix.time_unit != Decimal("0.0001") or matrix.allocation_tick != Decimal("0.001"):
        raise ScenarioError("EXP-08 time grids differ from the frozen matrix")


def _raw_seed(namespace: str, cell_id: str, observation_index: int, attempt: int) -> int:
    canonical = f"{namespace}|{cell_id}|{observation_index}|{attempt}".encode()
    return int.from_bytes(hashlib.sha256(canonical).digest()[:8], "big")


def _derived_seed(raw_seed: int, purpose: str) -> int:
    return int.from_bytes(hashlib.sha256(f"{raw_seed}|{purpose}".encode()).digest()[:8], "big")


def _weights(task_count: int, weight_type: str, matrix: Exp08Matrix, rng: random.Random) -> tuple[Decimal, ...]:
    if weight_type == "homogeneous":
        multipliers = [1] * task_count
    elif weight_type == "lognormal":
        weights_raw = _mapping(_mapping(matrix.raw["generator"], field="generator")["weights"], field="weights")
        data = _mapping(weights_raw["lognormal"], field="weights.lognormal")
        mu = float(decimal(data["mu"], field="mu"))
        sigma = float(decimal(data["sigma"], field="sigma"))
        scale = float(decimal(data["integer_multiplier_scale"], field="scale"))
        minimum = int(data["minimum_multiplier"])
        maximum = int(data["maximum_multiplier"])
        multipliers = [max(minimum, min(maximum, int(round(scale * rng.lognormvariate(mu, sigma))))) for _ in range(task_count)]
    else:
        raise ScenarioError(f"unknown EXP-08 weight type {weight_type}")
    return tuple(matrix.base_effort * item for item in multipliers)


def _reference_path(
    predecessors: tuple[tuple[str, ...], ...],
    weights: tuple[Decimal, ...],
    *,
    tie_seed: int,
) -> tuple[Decimal, tuple[str, ...], int]:
    task_ids = _task_ids(len(weights))
    index = {task_id: position for position, task_id in enumerate(task_ids)}
    rng = random.Random(tie_seed)
    rank = {task_id: rng.random() for task_id in task_ids}
    best: list[Decimal] = []
    parent: list[str | None] = []
    counts: list[int] = []
    for position, task_id in enumerate(task_ids):
        if not predecessors[position]:
            best.append(weights[position])
            parent.append(None)
            counts.append(1)
            continue
        predecessor_score = max(best[index[item]] for item in predecessors[position])
        tied = [item for item in predecessors[position] if best[index[item]] == predecessor_score]
        selected = min(tied, key=lambda item: rank[item])
        best.append(predecessor_score + weights[position])
        parent.append(selected)
        counts.append(sum(counts[index[item]] for item in tied))
    maximum = max(best)
    endpoints = [task_id for task_id in task_ids if best[index[task_id]] == maximum]
    selected_end = min(endpoints, key=lambda item: rank[item])
    path_count = sum(counts[index[item]] for item in endpoints)
    path: list[str] = []
    cursor: str | None = selected_end
    while cursor is not None:
        path.append(cursor)
        cursor = parent[index[cursor]]
    return maximum, tuple(reversed(path)), path_count


def _exact_ticks(value: Decimal, tick: Decimal, *, field: str) -> int:
    ticks = value / tick
    if ticks != ticks.to_integral_value():
        raise ScenarioError(f"{field}: {value} is not divisible by allocation tick {tick}")
    return int(ticks)


def _apportion(
    weights: list[Decimal],
    total_ticks: int,
    matrix: Exp08Matrix,
    *,
    seed: int,
) -> list[int]:
    total_weight = sum(weights, Decimal("0"))
    ideals = [Decimal(total_ticks) * weight / total_weight for weight in weights]
    lower = [int((matrix.share_lower * weight / matrix.allocation_tick).to_integral_value(rounding=ROUND_CEILING)) for weight in weights]
    upper = [int((matrix.share_upper * weight / matrix.allocation_tick).to_integral_value(rounding=ROUND_FLOOR)) for weight in weights]
    values = [max(lo, min(hi, int(ideal.to_integral_value(rounding=ROUND_FLOOR)))) for ideal, lo, hi in zip(ideals, lower, upper, strict=True)]
    ranks = list(range(len(weights)))
    random.Random(seed).shuffle(ranks)
    tie_rank = {item: position for position, item in enumerate(ranks)}
    difference = total_ticks - sum(values)
    while difference > 0:
        candidates = [item for item in range(len(values)) if values[item] < upper[item]]
        if not candidates:
            raise ScenarioError("allocator cannot reach requested group total")
        candidates.sort(key=lambda item: (-(ideals[item] - ideals[item].to_integral_value(rounding=ROUND_FLOOR)), tie_rank[item]))
        for item in candidates:
            if difference == 0:
                break
            values[item] += 1
            difference -= 1
    while difference < 0:
        candidates = [item for item in range(len(values)) if values[item] > lower[item]]
        if not candidates:
            raise ScenarioError("allocator cannot reduce to requested group total")
        candidates.sort(key=lambda item: ((ideals[item] - ideals[item].to_integral_value(rounding=ROUND_FLOOR)), tie_rank[item]))
        for item in candidates:
            if difference == 0:
                break
            values[item] -= 1
            difference += 1
    return values


def allocate_human(
    weights: tuple[Decimal, ...],
    reference_path: tuple[str, ...],
    target: Decimal,
    matrix: Exp08Matrix,
    *,
    seed: int,
) -> tuple[tuple[Decimal, ...], Decimal]:
    task_ids = _task_ids(len(weights))
    on_path = set(reference_path)
    on_indices = [index for index, task_id in enumerate(task_ids) if task_id in on_path]
    off_indices = [index for index, task_id in enumerate(task_ids) if task_id not in on_path]
    if not on_indices or not off_indices:
        raise ScenarioError("reference path must have both on-path and off-path tasks")
    total_work = sum(weights, Decimal("0"))
    total_h = total_work * matrix.total_human_share
    total_ticks = _exact_ticks(total_h, matrix.allocation_tick, field="total H")
    on_ticks = _exact_ticks(total_h * target, matrix.allocation_tick, field="on-path H")
    off_ticks = total_ticks - on_ticks
    allocated = [0] * len(weights)
    for label, indices, ticks in (("on", on_indices, on_ticks), ("off", off_indices, off_ticks)):
        group = _apportion([weights[item] for item in indices], ticks, matrix, seed=_derived_seed(seed, f"allocation-{target}-{label}"))
        for index, value in zip(indices, group, strict=True):
            allocated[index] = value
    human = tuple(Decimal(value) * matrix.allocation_tick for value in allocated)
    if sum(human, Decimal("0")) != total_h:
        raise ScenarioError("paired allocator did not preserve total H")
    actual = sum((human[item] for item in on_indices), Decimal("0")) / total_h
    if abs(actual - target) > matrix.concentration_tolerance:
        raise ScenarioError("paired allocator missed concentration target")
    if any(not (matrix.share_lower <= h / weight <= matrix.share_upper) for h, weight in zip(human, weights, strict=True)):
        raise ScenarioError("paired allocator violated task-level share bounds")
    return human, actual


def generate_graphs(matrix: Exp08Matrix, stream_name: str) -> tuple[list[GraphBase], list[dict[str, str]]]:
    if stream_name not in matrix.streams:
        raise ScenarioError(f"unknown EXP-08 stream {stream_name}")
    stream = matrix.streams[stream_name]
    graphs: list[GraphBase] = []
    attempts: list[dict[str, str]] = []
    for task_count in matrix.task_counts:
        for topology in matrix.topology_specs:
            for weight_type in matrix.weight_types:
                cell_id = f"n{task_count}_{topology.name}_{weight_type}"
                for observation_index in range(stream.start, stream.stop + 1):
                    accepted: GraphBase | None = None
                    for attempt in range(matrix.max_attempts):
                        raw_seed = _raw_seed(stream.namespace, cell_id, observation_index, attempt)
                        rng = random.Random(raw_seed)
                        predecessors = _layered_predecessors(task_count, topology, rng)
                        weights = _weights(task_count, weight_type, matrix, rng)
                        graph_ok, reason = _graph_checks(predecessors)
                        path_weight, path, path_count = _reference_path(predecessors, weights, tie_seed=_derived_seed(raw_seed, "reference-path"))
                        rho_l = path_weight / sum(weights, Decimal("0"))
                        if graph_ok and not matrix.rho_l_bins[topology.target_rho_l_bin].contains(rho_l):
                            graph_ok, reason = False, "rho_l_outside_target_bin"
                        human_low: tuple[Decimal, ...] = ()
                        human_high: tuple[Decimal, ...] = ()
                        rho_low = Decimal("0")
                        rho_high = Decimal("0")
                        if graph_ok:
                            try:
                                human_low, rho_low = allocate_human(weights, path, matrix.concentrations["low"], matrix, seed=raw_seed)
                                human_high, rho_high = allocate_human(weights, path, matrix.concentrations["high"], matrix, seed=raw_seed)
                            except ScenarioError as error:
                                graph_ok, reason = False, f"allocator_infeasible:{error}"
                        dag_id = f"exp08_{stream_name}_{cell_id}_{observation_index:02d}"
                        attempts.append({
                            "experiment_id": "EXP-08", "stream": stream_name,
                            "namespace": stream.namespace, "dag_id": dag_id,
                            "cell_id": cell_id, "task_count": str(task_count),
                            "topology_family": topology.name, "weight_type": weight_type,
                            "target_rho_l_bin": topology.target_rho_l_bin,
                            "observation_index": str(observation_index), "attempt": str(attempt),
                            "raw_seed": str(raw_seed), "accepted": str(graph_ok).lower(),
                            "reason": "accepted_all_structural_and_allocator_checks" if graph_ok else reason,
                            "rho_l": _fmt(rho_l), "longest_path_count": str(path_count),
                            "rho_h_low": _fmt(rho_low) if graph_ok else "",
                            "rho_h_high": _fmt(rho_high) if graph_ok else "",
                        })
                        if graph_ok:
                            accepted = GraphBase(
                                dag_id, stream_name, cell_id, task_count, topology.name,
                                weight_type, topology.target_rho_l_bin, observation_index,
                                attempt, raw_seed, predecessors, weights, path, path_weight,
                                path_count, rho_l, human_low, human_high, rho_low, rho_high,
                            )
                            break
                    if accepted is None:
                        raise RuntimeError(f"{stream_name} {cell_id} observation {observation_index}: rejection limit exhausted")
                    graphs.append(accepted)
    if len(graphs) != stream.expected_graphs:
        raise RuntimeError(f"generated {len(graphs)} {stream_name} graphs, expected {stream.expected_graphs}")
    if len({graph.raw_seed for graph in graphs}) != len(graphs):
        raise RuntimeError(f"raw seed collision inside {stream_name} stream")
    return graphs, attempts


def _split_duration(total: Decimal, parts: int, matrix: Exp08Matrix, *, seed: int) -> list[Decimal]:
    ticks = _exact_ticks(total, matrix.allocation_tick, field="phase total")
    quotient, remainder = divmod(ticks, parts)
    order = list(range(parts))
    random.Random(seed).shuffle(order)
    values = [quotient] * parts
    for item in order[:remainder]:
        values[item] += 1
    if any(value <= 0 for value in values):
        raise ScenarioError("phase rounding produced a nonpositive phase")
    return [Decimal(value) * matrix.allocation_tick for value in values]


def build_scenario(
    matrix: Exp08Matrix,
    graph: GraphBase,
    *,
    allocation: str,
    profile: str,
    p: int,
    c: Decimal = Decimal("1"),
    gamma: Decimal = Decimal("1"),
) -> Scenario:
    if allocation not in {"low", "high"} or profile not in matrix.phase_profiles:
        raise ScenarioError("unknown EXP-08 allocation or phase profile")
    humans = graph.human_low if allocation == "low" else graph.human_high
    task_ids = _task_ids(graph.task_count)
    tasks: list[TaskSpec] = []
    for index, (task_id, weight, human, predecessors) in enumerate(zip(task_ids, graph.weights, humans, graph.predecessors, strict=True)):
        agent = weight - human
        phase_seed = _derived_seed(graph.raw_seed, f"phases-{allocation}-{profile}-{index}")
        if profile == "io":
            human_parts = _split_duration(human, 2, matrix, seed=phase_seed)
            phases = (
                PhaseSpec("human_1", "human", human_parts[0]),
                PhaseSpec("agent_1", "agent", agent),
                PhaseSpec("human_2", "human", human_parts[1]),
            )
        else:
            human_parts = _split_duration(human, 4, matrix, seed=phase_seed)
            agent_parts = _split_duration(agent, 3, matrix, seed=_derived_seed(phase_seed, "agent"))
            phase_list: list[PhaseSpec] = []
            for item, human_part in enumerate(human_parts):
                phase_list.append(PhaseSpec(f"human_{item + 1}", "human", human_part))
                if item < 3:
                    phase_list.append(PhaseSpec(f"agent_{item + 1}", "agent", agent_parts[item]))
            phases = tuple(phase_list)
        tasks.append(TaskSpec(task_id, f"Synthetic task {index + 1}", Decimal("1"), weight, human, predecessors, phases, f"qg_{task_id}"))
    scenario = Scenario(
        1, f"{graph.dag_id}_{allocation}_{profile}_p{p}_c{_fmt(c)}_g{_fmt(gamma)}",
        "EXP-08", matrix.time_unit, matrix.tolerance, Decimal("1"), p, c,
        gamma, tuple(tasks), (), matrix.source_path,
    )
    validate_scenario(scenario)
    return scenario


def _reference_path_length(scenario: Scenario, reference_path: Iterable[str]) -> Decimal:
    selected = set(reference_path)
    return sum((scenario.c * task.a + scenario.gamma * task.h for task in scenario.tasks if task.task_id in selected), Decimal("0"))


def _policy_row(graph: GraphBase, allocation: str, profile: str, scenario: Scenario, *, block: str) -> dict[str, str]:
    aggregate = compute_aggregates(scenario)
    validation = validate_schedule(scenario, simulate_baseline(scenario))
    if not validation.valid or validation.metrics is None:
        detail = "; ".join(item.message for item in validation.issues)
        raise RuntimeError(f"{scenario.scenario_id}: invalid baseline: {detail}")
    metrics = validation.metrics
    return {
        "experiment_id": "EXP-08", "block": block, "dag_id": graph.dag_id,
        "cell_id": graph.cell_id, "task_count": str(graph.task_count),
        "topology_family": graph.topology_family, "weight_type": graph.weight_type,
        "path_multiplicity": graph.path_multiplicity,
        "longest_path_count": str(graph.longest_path_count),
        "observation_index": str(graph.observation_index), "raw_seed": str(graph.raw_seed),
        "allocation": allocation, "actual_rho_h_p0": _fmt(graph.rho_h_low if allocation == "low" else graph.rho_h_high),
        "phase_profile": profile, "P": str(scenario.p), "C": _fmt(scenario.c),
        "gamma": _fmt(scenario.gamma), "H": _fmt(aggregate.h), "W4": _fmt(aggregate.w4),
        "L4": _fmt(aggregate.l4), "B4": _fmt(aggregate.b4),
        "active_branches": ",".join(aggregate.active_branches),
        "critical_path": "->".join(aggregate.critical_path_l4),
        "reference_path": "->".join(graph.reference_path),
        "reference_path_length": _fmt(_reference_path_length(scenario, graph.reference_path)),
        "policy_makespan": _fmt(metrics.makespan), "policy_queue": _fmt(metrics.queue_time),
        "policy_blocked_any": _fmt(metrics.blocked_any_time),
    }


def _aggregate_row(graph: GraphBase, allocation: str, scenario: Scenario) -> dict[str, str]:
    aggregate = compute_aggregates(scenario)
    return {
        "experiment_id": "EXP-08", "block": "C", "dag_id": graph.dag_id,
        "cell_id": graph.cell_id, "task_count": str(graph.task_count),
        "topology_family": graph.topology_family, "weight_type": graph.weight_type,
        "path_multiplicity": graph.path_multiplicity,
        "longest_path_count": str(graph.longest_path_count),
        "observation_index": str(graph.observation_index), "raw_seed": str(graph.raw_seed),
        "allocation": allocation, "actual_rho_h_p0": _fmt(graph.rho_h_low if allocation == "low" else graph.rho_h_high),
        "phase_profile": "io", "P": str(scenario.p), "C": _fmt(scenario.c),
        "gamma": _fmt(scenario.gamma), "H": _fmt(aggregate.h), "W4": _fmt(aggregate.w4),
        "L4": _fmt(aggregate.l4), "B4": _fmt(aggregate.b4),
        "active_branches": ",".join(aggregate.active_branches),
        "critical_path": "->".join(aggregate.critical_path_l4),
        "reference_path": "->".join(graph.reference_path),
        "reference_path_length": _fmt(_reference_path_length(scenario, graph.reference_path)),
        "policy_makespan": "", "policy_queue": "", "policy_blocked_any": "",
    }


def _invariant_row(graph: GraphBase, low: dict[str, str], high: dict[str, str]) -> dict[str, str]:
    fields = ("H", "W4", "L4", "B4", "active_branches", "critical_path")
    checks = {f"same_{field}": str(low[field] == high[field]).lower() for field in fields}
    return {
        "dag_id": graph.dag_id, "task_count": str(graph.task_count),
        "topology_family": graph.topology_family, "weight_type": graph.weight_type,
        "path_multiplicity": graph.path_multiplicity,
        "phase_profile": low["phase_profile"], "P": low["P"], **checks,
        "all_invariants_hold": str(all(low[field] == high[field] for field in fields)).lower(),
    }


def _schedule_pair(graph: GraphBase, low: dict[str, str], high: dict[str, str]) -> dict[str, str]:
    b4 = Decimal(low["B4"])
    row = {
        "pair_type": "schedule_policy", "dag_id": graph.dag_id,
        "task_count": str(graph.task_count), "topology_family": graph.topology_family,
        "weight_type": graph.weight_type, "path_multiplicity": graph.path_multiplicity,
        "observation_index": str(graph.observation_index), "phase_profile": low["phase_profile"],
        "P": low["P"], "path_stable": "", "path_transition": "",
        "delta_reference_path_length": "", "delta_reference_path_length_normalized": "",
        "delta_L4": "", "delta_B4": "", "theoretical_delta": "", "identity_holds": "",
    }
    for field, suffix in (("policy_makespan", "makespan"), ("policy_queue", "queue"), ("policy_blocked_any", "blocked_any")):
        delta = Decimal(high[field]) - Decimal(low[field])
        row[f"delta_{suffix}"] = _fmt(delta)
        row[f"delta_{suffix}_normalized"] = _fmt(delta / b4)
    return row


def _slowdown_pair(matrix: Exp08Matrix, graph: GraphBase, low: dict[str, str], high: dict[str, str]) -> dict[str, str]:
    delta_path = Decimal(high["reference_path_length"]) - Decimal(low["reference_path_length"])
    delta_l4 = Decimal(high["L4"]) - Decimal(low["L4"])
    delta_b4 = Decimal(high["B4"]) - Decimal(low["B4"])
    total_h = Decimal(low["H"])
    theoretical = (matrix.slowdown_gamma - matrix.slowdown_c) * (matrix.concentrations["high"] - matrix.concentrations["low"]) * total_h
    low_path = low["critical_path"]
    high_path = high["critical_path"]
    reference = low["reference_path"]
    stable = low_path == reference and high_path == reference
    return {
        "pair_type": "differentiated_slowdown", "dag_id": graph.dag_id,
        "task_count": str(graph.task_count), "topology_family": graph.topology_family,
        "weight_type": graph.weight_type, "path_multiplicity": graph.path_multiplicity,
        "observation_index": str(graph.observation_index), "phase_profile": "io",
        "P": str(matrix.slowdown_p), "path_stable": str(stable).lower(),
        "path_transition": f"{low_path} => {high_path}",
        "delta_reference_path_length": _fmt(delta_path),
        "delta_reference_path_length_normalized": _fmt(delta_path / Decimal(low["B4"])),
        "delta_L4": _fmt(delta_l4), "delta_B4": _fmt(delta_b4),
        "theoretical_delta": _fmt(theoretical),
        "identity_holds": str(abs(delta_path - theoretical) <= matrix.tolerance).lower(),
        "delta_makespan": "", "delta_makespan_normalized": "",
        "delta_queue": "", "delta_queue_normalized": "",
        "delta_blocked_any": "", "delta_blocked_any_normalized": "",
    }


def _quantile(values: list[Decimal], q: Decimal) -> Decimal:
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    position = q * Decimal(len(ordered) - 1)
    lower = int(position)
    fraction = position - lower
    return ordered[lower] * (Decimal("1") - fraction) + ordered[min(lower + 1, len(ordered) - 1)] * fraction


def _bootstrap_median(values: list[Decimal], *, resamples: int, seed: int) -> tuple[Decimal, Decimal, Decimal]:
    rng = random.Random(seed)
    center = Decimal(str(median(values)))
    samples = [Decimal(str(median([values[rng.randrange(len(values))] for _ in values]))) for _ in range(resamples)]
    return center, _quantile(samples, Decimal("0.025")), _quantile(samples, Decimal("0.975"))


def _decision(ci_low: Decimal, ci_high: Decimal, margin: Decimal) -> str:
    if ci_low > margin:
        return "positive"
    if ci_high < -margin:
        return "negative"
    if ci_low >= -margin and ci_high <= margin:
        return "practically_equivalent"
    return "inconclusive"


def _summaries(matrix: Exp08Matrix, pairs: list[dict[str, str]]) -> list[dict[str, str]]:
    schedule_pairs = [row for row in pairs if row["pair_type"] == "schedule_policy"]
    rows: list[dict[str, str]] = []
    index = 0
    for profile in matrix.phase_profiles:
        for p in matrix.agent_counts:
            selected = [row for row in schedule_pairs if row["phase_profile"] == profile and row["P"] == str(p)]
            for metric in ("makespan", "queue", "blocked_any"):
                values = [Decimal(row[f"delta_{metric}_normalized"]) for row in selected]
                center, ci_low, ci_high = _bootstrap_median(values, resamples=matrix.bootstrap_resamples, seed=matrix.bootstrap_seed + index)
                index += 1
                margin = matrix.equivalence_margin
                rows.append({
                    "summary_type": "schedule", "scope": "overall", "phase_profile": profile,
                    "P": str(p), "metric": f"delta_{metric}_normalized", "n": str(len(values)),
                    "mean": _fmt(Decimal(str(mean(values)))), "median": _fmt(center),
                    "q25": _fmt(_quantile(values, Decimal("0.25"))), "q75": _fmt(_quantile(values, Decimal("0.75"))),
                    "bootstrap_ci_low": _fmt(ci_low), "bootstrap_ci_high": _fmt(ci_high),
                    "margin": _fmt(margin), "decision": _decision(ci_low, ci_high, margin),
                    "decision_margin_0.005": _decision(ci_low, ci_high, matrix.sensitivity_margins[0]),
                    "decision_margin_0.02": _decision(ci_low, ci_high, matrix.sensitivity_margins[1]),
                    "negative_beyond_margin_rate": _fmt(Decimal(sum(value < -margin for value in values)) / len(values)),
                    "within_margin_rate": _fmt(Decimal(sum(-margin <= value <= margin for value in values)) / len(values)),
                    "positive_beyond_margin_rate": _fmt(Decimal(sum(value > margin for value in values)) / len(values)),
                })
    slowdown = [row for row in pairs if row["pair_type"] == "differentiated_slowdown"]
    for scope, selected in (("all", slowdown), ("path_stable", [row for row in slowdown if row["path_stable"] == "true"])):
        for metric in ("delta_reference_path_length_normalized", "delta_L4", "delta_B4"):
            values = [Decimal(row[metric]) for row in selected]
            if not values:
                continue
            center, ci_low, ci_high = _bootstrap_median(values, resamples=matrix.bootstrap_resamples, seed=matrix.bootstrap_seed + index)
            index += 1
            decision = "positive" if ci_low > 0 else "inconclusive"
            if scope == "all" and metric in {"delta_L4", "delta_B4"}:
                decision = "exploratory_only"
            rows.append({
                "summary_type": "slowdown", "scope": scope, "phase_profile": "io",
                "P": str(matrix.slowdown_p), "metric": metric, "n": str(len(values)),
                "mean": _fmt(Decimal(str(mean(values)))), "median": _fmt(center),
                "q25": _fmt(_quantile(values, Decimal("0.25"))), "q75": _fmt(_quantile(values, Decimal("0.75"))),
                "bootstrap_ci_low": _fmt(ci_low), "bootstrap_ci_high": _fmt(ci_high),
                "margin": "", "decision": decision,
                "decision_margin_0.005": "", "decision_margin_0.02": "",
                "negative_beyond_margin_rate": _fmt(Decimal(sum(value < 0 for value in values)) / len(values)),
                "within_margin_rate": _fmt(Decimal(sum(value == 0 for value in values)) / len(values)),
                "positive_beyond_margin_rate": _fmt(Decimal(sum(value > 0 for value in values)) / len(values)),
            })
    return rows


def _strata_rows(pairs: list[dict[str, str]]) -> list[dict[str, str]]:
    schedule = [row for row in pairs if row["pair_type"] == "schedule_policy"]
    rows: list[dict[str, str]] = []
    for field in ("task_count", "topology_family", "weight_type", "path_multiplicity"):
        for value in sorted({row[field] for row in schedule}):
            for profile in sorted({row["phase_profile"] for row in schedule}):
                for p in sorted({row["P"] for row in schedule}, key=int):
                    selected = [row for row in schedule if row[field] == value and row["phase_profile"] == profile and row["P"] == p]
                    values = [Decimal(row["delta_makespan_normalized"]) for row in selected]
                    rows.append({
                        "stratum_field": field, "stratum_value": value,
                        "phase_profile": profile, "P": p, "n": str(len(values)),
                        "mean_delta_makespan_normalized": _fmt(Decimal(str(mean(values)))),
                        "median_delta_makespan_normalized": _fmt(Decimal(str(median(values)))),
                        "negative_rate": _fmt(Decimal(sum(item < 0 for item in values)) / len(values)),
                        "zero_rate": _fmt(Decimal(sum(item == 0 for item in values)) / len(values)),
                        "positive_rate": _fmt(Decimal(sum(item > 0 for item in values)) / len(values)),
                    })
    return rows


def _exact_pair_rows(exact_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    groups: dict[tuple[str, str], dict[str, dict[str, str]]] = {}
    for row in exact_rows:
        groups.setdefault((row["dag_id"], row["P"]), {})[row["allocation"]] = row
    pairs: list[dict[str, str]] = []
    for (dag_id, p), allocations in sorted(groups.items()):
        if set(allocations) != {"low", "high"}:
            continue
        low = allocations["low"]
        high = allocations["high"]
        if low["solver_status"] != "OPTIMAL" or high["solver_status"] != "OPTIMAL":
            continue
        delta = Decimal(high["solver_objective"]) - Decimal(low["solver_objective"])
        pairs.append({
            "dag_id": dag_id, "task_count": low["task_count"],
            "topology_family": low["topology_family"],
            "observation_index": low["observation_index"], "phase_profile": "io",
            "P": p, "low_T_star": low["solver_objective"],
            "high_T_star": high["solver_objective"], "B4": low["B4"],
            "delta_T_star": _fmt(delta),
            "delta_T_star_normalized": _fmt(delta / Decimal(low["B4"])),
        })
    return pairs


def _exact_summaries(matrix: Exp08Matrix, pairs: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for offset, p in enumerate((4, 8), 100):
        values = [Decimal(row["delta_T_star_normalized"]) for row in pairs if row["P"] == str(p)]
        if not values:
            continue
        center, ci_low, ci_high = _bootstrap_median(values, resamples=matrix.bootstrap_resamples, seed=matrix.bootstrap_seed + offset)
        margin = matrix.equivalence_margin
        rows.append({
            "summary_type": "exact", "scope": "frozen_exact_subset",
            "phase_profile": "io", "P": str(p), "metric": "delta_T_star_normalized",
            "n": str(len(values)), "mean": _fmt(Decimal(str(mean(values)))),
            "median": _fmt(center), "q25": _fmt(_quantile(values, Decimal("0.25"))),
            "q75": _fmt(_quantile(values, Decimal("0.75"))),
            "bootstrap_ci_low": _fmt(ci_low), "bootstrap_ci_high": _fmt(ci_high),
            "margin": _fmt(margin), "decision": _decision(ci_low, ci_high, margin),
            "decision_margin_0.005": _decision(ci_low, ci_high, matrix.sensitivity_margins[0]),
            "decision_margin_0.02": _decision(ci_low, ci_high, matrix.sensitivity_margins[1]),
            "negative_beyond_margin_rate": _fmt(Decimal(sum(value < -margin for value in values)) / len(values)),
            "within_margin_rate": _fmt(Decimal(sum(-margin <= value <= margin for value in values)) / len(values)),
            "positive_beyond_margin_rate": _fmt(Decimal(sum(value > margin for value in values)) / len(values)),
        })
    return rows


def _graph_rows(graphs: list[GraphBase]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for graph in graphs:
        task_ids = _task_ids(graph.task_count)
        rows.append({
            "experiment_id": "EXP-08", "stream": graph.stream, "dag_id": graph.dag_id,
            "cell_id": graph.cell_id, "task_count": str(graph.task_count),
            "topology_family": graph.topology_family, "weight_type": graph.weight_type,
            "target_rho_l_bin": graph.target_rho_l_bin,
            "observation_index": str(graph.observation_index), "accepted_attempt": str(graph.accepted_attempt),
            "raw_seed": str(graph.raw_seed), "rho_l": _fmt(graph.rho_l),
            "reference_path": "->".join(graph.reference_path),
            "reference_path_weight": _fmt(graph.reference_path_weight),
            "longest_path_count": str(graph.longest_path_count), "path_multiplicity": graph.path_multiplicity,
            "rho_h_low": _fmt(graph.rho_h_low), "rho_h_high": _fmt(graph.rho_h_high),
            "weights_json": json.dumps([_fmt(item) for item in graph.weights], separators=(",", ":")),
            "human_low_json": json.dumps([_fmt(item) for item in graph.human_low], separators=(",", ":")),
            "human_high_json": json.dumps([_fmt(item) for item in graph.human_high], separators=(",", ":")),
            "predecessors_json": json.dumps({task_id: list(items) for task_id, items in zip(task_ids, graph.predecessors, strict=True)}, separators=(",", ":"), sort_keys=True),
        })
    return rows


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise RuntimeError(f"cannot write empty CSV {path}")
    with path.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def _fmt(value: Decimal | None) -> str:
    return "" if value is None else format(value, "f")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _dependency_versions() -> dict[str, str]:
    versions: dict[str, str] = {}
    for name in ("matplotlib", "ortools", "PyYAML", "pytest"):
        try:
            versions[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            versions[name] = "not-installed"
    return versions


def _exp07_raw_seeds(project_root: Path) -> set[int]:
    path = project_root / "results" / "exp07_dags.csv"
    if not path.exists():
        return set()
    return {int(row["raw_seed"]) for row in _read_csv(path)}


def _development_audit_rows(matrix: Exp08Matrix, graphs: list[GraphBase]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for graph in graphs:
        total_work = sum(graph.weights, Decimal("0"))
        for allocation, humans, actual in (("low", graph.human_low, graph.rho_h_low), ("high", graph.human_high, graph.rho_h_high)):
            target = matrix.concentrations[allocation]
            shares = [human / weight for human, weight in zip(humans, graph.weights, strict=True)]
            rows.append({
                "dag_id": graph.dag_id, "allocation": allocation,
                "total_human_share": _fmt(sum(humans, Decimal("0")) / total_work),
                "target_concentration": _fmt(target), "actual_concentration": _fmt(actual),
                "concentration_error": _fmt(actual - target),
                "minimum_task_human_share": _fmt(min(shares)),
                "maximum_task_human_share": _fmt(max(shares)),
                "total_h_preserved": str(sum(humans, Decimal("0")) == total_work * matrix.total_human_share).lower(),
                "bounds_hold": str(min(shares) >= matrix.share_lower and max(shares) <= matrix.share_upper).lower(),
            })
    return rows


def _exact_benchmark_rows(matrix: Exp08Matrix, graphs: list[GraphBase]) -> list[dict[str, str]]:
    benchmark = _mapping(_mapping(matrix.raw["development"], field="development")["exact_benchmark"], field="exact_benchmark")
    task_counts = {int(item) for item in _list(benchmark["task_counts"], field="benchmark.task_counts")}
    topology_families = {str(item) for item in _list(benchmark["topology_families"], field="benchmark.topology_families")}
    weight_types = {str(item) for item in _list(benchmark["weight_types"], field="benchmark.weight_types")}
    indices = {int(item) for item in _list(benchmark["observation_indices"], field="benchmark.indices")}
    allocations = [str(item) for item in _list(benchmark["allocations"], field="benchmark.allocations")]
    agent_counts = [int(item) for item in _list(benchmark["agent_counts"], field="benchmark.agent_counts")]
    selected = [graph for graph in graphs if graph.task_count in task_counts and graph.topology_family in topology_families and graph.weight_type in weight_types and graph.observation_index in indices]
    rows: list[dict[str, str]] = []
    for graph in selected:
        for allocation in allocations:
            for p in agent_counts:
                scenario = build_scenario(matrix, graph, allocation=allocation, profile=str(benchmark["phase_profile"]), p=p)
                solution = solve_exact(
                    scenario, time_limit_seconds=float(benchmark["time_limit_seconds"]),
                    random_seed=int(benchmark["random_seed"]), workers=int(benchmark["workers"]),
                )
                rows.append({
                    "dag_id": graph.dag_id, "task_count": str(graph.task_count),
                    "topology_family": graph.topology_family, "allocation": allocation,
                    "P": str(p), "solver_status": solution.status,
                    "solver_wall_time_seconds": f"{solution.wall_time:.6f}",
                    "objective_recorded": "false",
                })
    return rows


def _freeze_exact_scope(matrix: Exp08Matrix, timing_rows: list[dict[str, str]]) -> list[int]:
    rule = _mapping(_mapping(matrix.raw["development"], field="development")["exact_freeze_rule"], field="exact_freeze_rule")
    maximum = decimal(rule["maximum_p95_wall_time_seconds"], field="maximum_p95")
    included: list[int] = []
    for task_count in sorted({int(row["task_count"]) for row in timing_rows}):
        selected = [row for row in timing_rows if int(row["task_count"]) == task_count]
        wall = [Decimal(row["solver_wall_time_seconds"]) for row in selected]
        if all(row["solver_status"] == "OPTIMAL" for row in selected) and _quantile(wall, Decimal("0.95")) <= maximum:
            included.append(task_count)
    if not included:
        raise RuntimeError("development exact benchmark did not qualify any task count")
    return included


def run_development(project_root: Path, output_directory: Path, matrix: Exp08Matrix) -> tuple[Path, ...]:
    output_directory.mkdir(parents=True, exist_ok=True)
    graphs, attempts = generate_graphs(matrix, "development")
    attempts_path = output_directory / "exp08_development_attempts.csv"
    graphs_path = output_directory / "exp08_development_dags.csv"
    audit_path = output_directory / "exp08_development_allocator_audit.csv"
    timing_path = output_directory / "exp08_development_policy_timing.csv"
    exact_timing_path = output_directory / "exp08_development_exact_timing.csv"
    _write_csv(attempts_path, attempts)
    _write_csv(graphs_path, _graph_rows(graphs))
    audit_rows = _development_audit_rows(matrix, graphs)
    _write_csv(audit_path, audit_rows)
    timing_rows: list[dict[str, str]] = []
    for graph in graphs:
        for allocation in ("low", "high"):
            scenario = build_scenario(matrix, graph, allocation=allocation, profile="io", p=8)
            started = time.perf_counter()
            validation = validate_schedule(scenario, simulate_baseline(scenario))
            elapsed = time.perf_counter() - started
            if not validation.valid:
                raise RuntimeError(f"{scenario.scenario_id}: development policy validation failed")
            timing_rows.append({
                "dag_id": graph.dag_id, "task_count": str(graph.task_count),
                "topology_family": graph.topology_family, "weight_type": graph.weight_type,
                "allocation": allocation, "phase_profile": "io", "P": "8",
                "wall_time_seconds": f"{elapsed:.9f}", "outcome_recorded": "false",
            })
    _write_csv(timing_path, timing_rows)
    exact_timing = _exact_benchmark_rows(matrix, graphs)
    _write_csv(exact_timing_path, exact_timing)
    exact_task_counts = _freeze_exact_scope(matrix, exact_timing)
    development_seeds = {int(row["raw_seed"]) for row in attempts}
    exp07_overlap = development_seeds & _exp07_raw_seeds(project_root)
    if exp07_overlap:
        raise RuntimeError("EXP-08 development raw seed overlaps EXP-07")
    freeze_path = output_directory / "exp08_freeze.json"
    rule = _mapping(_mapping(matrix.raw["development"], field="development")["exact_freeze_rule"], field="exact_freeze_rule")
    freeze = {
        "experiment_id": "EXP-08", "status": "frozen_for_confirmatory",
        "frozen_at": datetime.now(timezone.utc).isoformat(),
        "matrix": {"path": str(matrix.source_path.relative_to(project_root)), "sha256": _sha256(matrix.source_path)},
        "development": {
            "namespace": matrix.streams["development"].namespace,
            "accepted_graphs": len(graphs), "outcomes_used": False,
            "allocator_rows": len(audit_rows),
            "all_allocator_checks_passed": all(row["total_h_preserved"] == "true" and row["bounds_hold"] == "true" and Decimal(row["concentration_error"]) == 0 for row in audit_rows),
            "policy_timing_rows": len(timing_rows), "exact_timing_rows": len(exact_timing),
            "exp07_raw_seed_overlap": 0,
        },
        "confirmatory": {
            "namespace": matrix.streams["confirmatory"].namespace,
            "expected_graphs": matrix.streams["confirmatory"].expected_graphs,
            "exact_task_counts": exact_task_counts,
            "exact_topology_families": [str(item) for item in _list(_mapping(_mapping(matrix.raw["development"], field="development")["exact_benchmark"], field="exact_benchmark")["topology_families"], field="exact topology families")],
            "exact_observation_indices": [int(item) for item in _list(rule["confirmatory_observation_indices"], field="confirm indices")],
            "exact_time_limit_seconds": float(rule["confirmatory_time_limit_seconds"]),
            "exact_workers": 1, "exact_random_seed": 0,
        },
        "development_outputs": [
            {"path": str(path.relative_to(project_root)), "sha256": _sha256(path)}
            for path in (attempts_path, graphs_path, audit_path, timing_path, exact_timing_path)
        ],
        "article_modified": False,
    }
    with freeze_path.open("w", encoding="utf-8") as target:
        json.dump(freeze, target, ensure_ascii=False, indent=2)
        target.write("\n")
    return attempts_path, graphs_path, audit_path, timing_path, exact_timing_path, freeze_path


def _load_freeze(project_root: Path, output_directory: Path, matrix: Exp08Matrix) -> dict[str, Any]:
    freeze_path = output_directory / "exp08_freeze.json"
    if not freeze_path.exists():
        raise RuntimeError("EXP-08 confirmatory stage requires results/exp08_freeze.json")
    with freeze_path.open(encoding="utf-8") as source:
        freeze = _mapping(json.load(source), field="freeze")
    if freeze.get("status") != "frozen_for_confirmatory":
        raise RuntimeError("EXP-08 freeze status is not confirmatory-ready")
    frozen_matrix = _mapping(freeze.get("matrix"), field="freeze.matrix")
    if frozen_matrix.get("sha256") != _sha256(matrix.source_path):
        raise RuntimeError("EXP-08 matrix changed after development freeze")
    confirmatory = _mapping(freeze.get("confirmatory"), field="freeze.confirmatory")
    if confirmatory.get("namespace") != matrix.streams["confirmatory"].namespace:
        raise RuntimeError("EXP-08 confirmatory namespace differs from freeze")
    for item in _list(freeze.get("development_outputs"), field="development_outputs"):
        record = _mapping(item, field="development_output")
        path = project_root / str(record["path"])
        if not path.exists() or _sha256(path) != record["sha256"]:
            raise RuntimeError(f"EXP-08 development output changed after freeze: {path}")
    return freeze


def _exact_rows(matrix: Exp08Matrix, graphs: list[GraphBase], freeze: dict[str, Any]) -> list[dict[str, str]]:
    config = _mapping(freeze["confirmatory"], field="freeze.confirmatory")
    task_counts = {int(item) for item in _list(config["exact_task_counts"], field="exact_task_counts")}
    topology_families = {str(item) for item in _list(config["exact_topology_families"], field="exact_topology_families")}
    indices = {int(item) for item in _list(config["exact_observation_indices"], field="exact_indices")}
    selected = [graph for graph in graphs if graph.task_count in task_counts and graph.topology_family in topology_families and graph.weight_type == "homogeneous" and graph.observation_index in indices]
    rows: list[dict[str, str]] = []
    for graph in selected:
        for p in (4, 8):
            for allocation in ("low", "high"):
                scenario = build_scenario(matrix, graph, allocation=allocation, profile="io", p=p)
                aggregate = compute_aggregates(scenario)
                solution = solve_exact(
                    scenario, time_limit_seconds=float(config["exact_time_limit_seconds"]),
                    random_seed=int(config["exact_random_seed"]), workers=int(config["exact_workers"]),
                )
                if solution.schedule is not None:
                    validation = validate_schedule(scenario, solution.schedule)
                    if not validation.valid:
                        raise RuntimeError(f"{scenario.scenario_id}: invalid exact schedule")
                rows.append({
                    "dag_id": graph.dag_id, "task_count": str(graph.task_count),
                    "topology_family": graph.topology_family, "observation_index": str(graph.observation_index),
                    "allocation": allocation, "phase_profile": "io", "P": str(p),
                    "B4": _fmt(aggregate.b4), "solver_status": solution.status,
                    "solver_objective": _fmt(solution.objective), "solver_best_bound": _fmt(solution.best_bound),
                    "solver_gap": _fmt(solution.relative_gap), "solver_wall_time_seconds": f"{solution.wall_time:.6f}",
                })
    return rows


def _write_report(
    path: Path,
    matrix: Exp08Matrix,
    graphs: list[GraphBase],
    attempts: list[dict[str, str]],
    invariants: list[dict[str, str]],
    pairs: list[dict[str, str]],
    summaries: list[dict[str, str]],
    exact_rows: list[dict[str, str]],
    exact_pairs: list[dict[str, str]],
) -> None:
    rejected = sum(row["accepted"] == "false" for row in attempts)
    tied = sum(graph.path_multiplicity == "tied" for graph in graphs)
    schedule = [row for row in summaries if row["summary_type"] == "schedule"]
    slowdown = [row for row in summaries if row["summary_type"] == "slowdown"]
    exact_summary = [row for row in summaries if row["summary_type"] == "exact"]
    c_pairs = [row for row in pairs if row["pair_type"] == "differentiated_slowdown"]
    stable = sum(row["path_stable"] == "true" for row in c_pairs)
    exact_counts = {status: sum(row["solver_status"] == status for row in exact_rows) for status in sorted({row["solver_status"] for row in exact_rows})}

    def schedule_table(rows: list[dict[str, str]]) -> str:
        lines = ["| Profile | P | Metric | n | Median [95% bootstrap] | Decision |", "|---|---:|---|---:|---:|---|"]
        for row in rows:
            lines.append(f"| {row['phase_profile']} | {row['P']} | `{row['metric']}` | {row['n']} | {Decimal(row['median']):.4f} [{Decimal(row['bootstrap_ci_low']):.4f}, {Decimal(row['bootstrap_ci_high']):.4f}] | **{row['decision']}** |")
        return "\n".join(lines)

    def slowdown_table(rows: list[dict[str, str]]) -> str:
        lines = ["| Scope | Metric | n | Median [95% bootstrap] | Decision |", "|---|---|---:|---:|---|"]
        for row in rows:
            lines.append(f"| {row['scope']} | `{row['metric']}` | {row['n']} | {Decimal(row['median']):.4f} [{Decimal(row['bootstrap_ci_low']):.4f}, {Decimal(row['bootstrap_ci_high']):.4f}] | **{row['decision']}** |")
        return "\n".join(lines)

    def exact_table(rows: list[dict[str, str]]) -> str:
        lines = ["| P | Proven pairs | Median delta T-star / B4 [95% bootstrap] | Decision |", "|---:|---:|---:|---|"]
        for row in rows:
            lines.append(f"| {row['P']} | {row['n']} | {Decimal(row['median']):.4f} [{Decimal(row['bootstrap_ci_low']):.4f}, {Decimal(row['bootstrap_ci_high']):.4f}] | **{row['decision']}** |")
        return "\n".join(lines)

    text = f"""# EXP-08: общий human-work и концентрация на reference path

## Дизайн и чистота выборки

EXP-08 использует **{len(graphs)}** новых confirmatory graph/weight-основ в
namespace `{matrix.streams['confirmatory'].namespace}`. Ни один DAG или raw
seed EXP-07 и ни одна из 240 development-основ не входят в оценки эффектов.
Отклонено {rejected} attempts; причины сохранены. Все 24 ячейки
`N × topology × weight type` содержат по 20 принятых наблюдений.

Reference path P0 выбран на structural weights при C=gamma=1 до allocations
seeded tie-break, не связанным с `task_id`. У {tied} из {len(graphs)} основ
существует более одного равного longest path; они помечены как `tied`.

![Покрытие allocation design](../figures/exp08_allocation_coverage.png)

[SVG-версия](../figures/exp08_allocation_coverage.svg).

## EXP-08A: aggregate identity

В paired low/high allocations строго сохраняются DAG, weights, общий H и W4;
концентрация H на P0 меняется с 0.30 до 0.70. Проверены H, W4, L4, B4,
активные ветви и structural critical path во всех {len(invariants)} комбинациях
двух phase profiles и P=1/4/8. Полный invariant check прошли
**{sum(row['all_invariants_hold'] == 'true' for row in invariants)}/{len(invariants)}** строк.

## EXP-08B: влияние на расписание фиксированной политики

Эффект определён как high concentration минус low и нормирован на общий B4.
`positive` означает рост времени/очереди, `negative` — снижение,
`practically_equivalent` — весь bootstrap interval внутри ±0.01, иначе
`inconclusive`. Primary rows — профиль `io`, P=4/8; P=1 — negative control,
`equal_alternating` — robustness.

{schedule_table(schedule)}

![Paired schedule effects](../figures/exp08_schedule_effects.png)

[SVG-версия](../figures/exp08_schedule_effects.svg).

Sensitivity decisions для margins 0.005 и 0.02 и доли individual effects за
пределами margin сохранены в `exp08_summary.csv`. Описательная стратификация
по N, topology, weight type и unique/tied path находится в
`exp08_strata.csv`; она не заменяет overall confirmatory decision.

## EXP-08C: differentiated slowdown

При C=1 и gamma=1.3 рост длины замороженного P0 должен точно равняться
`(gamma-C) × (0.70-0.30) × H`. Identity прошла
**{sum(row['identity_holds'] == 'true' for row in c_pairs)}/{len(c_pairs)}**
пар. P0 остался глобальным longest path в обеих allocations для {stable} из
{len(c_pairs)} пар; только эта path-stable подвыборка используется для
confirmatory-вывода о глобальном L4. Path switches сохранены отдельно.

{slowdown_table(slowdown)}

Строки `all / delta_L4` и `all / delta_B4` являются exploratory: глобальный
путь может переключиться. Confirmatory-интерпретация этих метрик разрешена
только для `path_stable`; identity для длины замороженного P0 использует все
480 пар.

![Critical-path effects](../figures/exp08_critical_path_effects.png)

[SVG-версия](../figures/exp08_critical_path_effects.svg).

## Exact-аудит

Scope и единый time limit выбраны автоматически по замороженному timing-rule
на development-потоке до генерации confirmatory-основ. Рассчитано
{len(exact_rows)} сценариев; статусы: **{json.dumps(exact_counts, ensure_ascii=False, sort_keys=True)}**.
Только `OPTIMAL` objectives можно обозначать как T-star; `FEASIBLE` incumbents
сохраняются вместе с bound и gap.

Ресурсная поправка сделана только по statuses/wall time, без записи objectives:
первичный экран `N=8/16, 5 s` и повторный `N=8, 30 s` не доказали все
`wide_layered, P=4` случаи. До confirmatory-генерации scope был единообразно
зафиксирован как `N=8`, homogeneous, `mixed/chain_like`, observation indices
0/1, allocations low/high и P=4/8 с limit 30 s.

{exact_table(exact_summary)}

Полные {len(exact_pairs)} proven paired contrasts сохранены отдельно; малая
exact-подвыборка является аудитом policy-результата, а не заменяет основную
480-графовую оценку.

## Ограничения

- topology family по наследству генератора смешана с rho_L bin;
- результаты расписания относятся к `bottom_level_fcfs_v1`, а не автоматически
  к оптимуму;
- equivalence margin 0.01 является engineering threshold;
- tied structural paths и path switches не смешиваются с path-stable выводом;
- development timing не используется как outcome.

## Файлы

- `exp08_confirmatory_attempts.csv`, `exp08_confirmatory_dags.csv`;
- `exp08_runs.csv`, `exp08_invariants.csv`, `exp08_pairs.csv`;
- `exp08_summary.csv`, `exp08_strata.csv`, `exp08_exact.csv`,
  `exp08_exact_pairs.csv`;
- `exp08_freeze.json`, `exp08_manifest.json` и этот отчёт;
- три пары PNG/SVG в `figures/`.

Текст статьи в рамках EXP-08 не менялся.
"""
    path.write_text(text, encoding="utf-8")


def run_confirmatory(project_root: Path, output_directory: Path, matrix: Exp08Matrix) -> tuple[Path, ...]:
    freeze = _load_freeze(project_root, output_directory, matrix)
    graphs, attempts = generate_graphs(matrix, "confirmatory")
    development_seeds = {int(row["raw_seed"]) for row in _read_csv(output_directory / "exp08_development_attempts.csv")}
    confirmatory_seeds = {int(row["raw_seed"]) for row in attempts}
    if development_seeds & confirmatory_seeds:
        raise RuntimeError("EXP-08 development and confirmatory raw seed streams overlap")
    if confirmatory_seeds & _exp07_raw_seeds(project_root):
        raise RuntimeError("EXP-08 confirmatory raw seed overlaps EXP-07")

    attempts_path = output_directory / "exp08_confirmatory_attempts.csv"
    graphs_path = output_directory / "exp08_confirmatory_dags.csv"
    _write_csv(attempts_path, attempts)
    _write_csv(graphs_path, _graph_rows(graphs))
    runs: list[dict[str, str]] = []
    invariants: list[dict[str, str]] = []
    pairs: list[dict[str, str]] = []
    for offset, graph in enumerate(graphs, 1):
        for profile in matrix.phase_profiles:
            for p in matrix.agent_counts:
                by_allocation: dict[str, dict[str, str]] = {}
                for allocation in ("low", "high"):
                    scenario = build_scenario(matrix, graph, allocation=allocation, profile=profile, p=p)
                    row = _policy_row(graph, allocation, profile, scenario, block="AB")
                    runs.append(row)
                    by_allocation[allocation] = row
                invariants.append(_invariant_row(graph, by_allocation["low"], by_allocation["high"]))
                pairs.append(_schedule_pair(graph, by_allocation["low"], by_allocation["high"]))
        slowdown_rows: dict[str, dict[str, str]] = {}
        for allocation in ("low", "high"):
            scenario = build_scenario(
                matrix, graph, allocation=allocation, profile="io", p=matrix.slowdown_p,
                c=matrix.slowdown_c, gamma=matrix.slowdown_gamma,
            )
            row = _aggregate_row(graph, allocation, scenario)
            runs.append(row)
            slowdown_rows[allocation] = row
        pairs.append(_slowdown_pair(matrix, graph, slowdown_rows["low"], slowdown_rows["high"]))
        if offset % 80 == 0:
            print(f"EXP-08 confirmatory: {offset}/{len(graphs)} graph bases")

    summaries = _summaries(matrix, pairs)
    strata = _strata_rows(pairs)
    exact_rows = _exact_rows(matrix, graphs, freeze)
    exact_pairs = _exact_pair_rows(exact_rows)
    summaries.extend(_exact_summaries(matrix, exact_pairs))
    runs_path = output_directory / "exp08_runs.csv"
    invariant_path = output_directory / "exp08_invariants.csv"
    pairs_path = output_directory / "exp08_pairs.csv"
    summary_path = output_directory / "exp08_summary.csv"
    strata_path = output_directory / "exp08_strata.csv"
    exact_path = output_directory / "exp08_exact.csv"
    exact_pairs_path = output_directory / "exp08_exact_pairs.csv"
    _write_csv(runs_path, runs)
    _write_csv(invariant_path, invariants)
    _write_csv(pairs_path, pairs)
    _write_csv(summary_path, summaries)
    _write_csv(strata_path, strata)
    _write_csv(exact_path, exact_rows)
    _write_csv(exact_pairs_path, exact_pairs)
    from .exp08_figures import build_exp08_figures
    figure_paths = build_exp08_figures(graphs_path, pairs_path, project_root / "figures")
    report_path = output_directory / "exp08_report.md"
    _write_report(report_path, matrix, graphs, attempts, invariants, pairs, summaries, exact_rows, exact_pairs)
    output_paths = [attempts_path, graphs_path, runs_path, invariant_path, pairs_path, summary_path, strata_path, exact_path, exact_pairs_path, report_path, *figure_paths]
    manifest_path = output_directory / "exp08_manifest.json"
    manifest = {
        "experiment_id": "EXP-08", "generated_at": datetime.now(timezone.utc).isoformat(),
        "command": "uv run python -m experiments run --experiment EXP-08 --stage confirmatory",
        **git_provenance(project_root),
        "frozen_matrix": {"path": str(matrix.source_path.relative_to(project_root)), "sha256": _sha256(matrix.source_path)},
        "freeze": {"path": str((output_directory / "exp08_freeze.json").relative_to(project_root)), "sha256": _sha256(output_directory / "exp08_freeze.json")},
        "design": {
            "development_namespace": matrix.streams["development"].namespace,
            "confirmatory_namespace": matrix.streams["confirmatory"].namespace,
            "confirmatory_graphs": len(graphs),
            "development_confirmatory_raw_seed_overlap": 0,
            "exp07_confirmatory_raw_seed_overlap": 0,
            "rejected_confirmatory_attempts": sum(row["accepted"] == "false" for row in attempts),
        },
        "exact_audit": {
            **_mapping(freeze["confirmatory"], field="freeze.confirmatory"),
            "scenario_rows": len(exact_rows),
            "status_counts": {status: sum(row["solver_status"] == status for row in exact_rows) for status in sorted({row["solver_status"] for row in exact_rows})},
        },
        "dependencies": _dependency_versions(),
        "outputs": [{"path": str(path.relative_to(project_root)), "sha256": _sha256(path)} for path in output_paths],
        "implementation": implementation_records(project_root),
        "article_modified": False,
    }
    with manifest_path.open("w", encoding="utf-8") as target:
        json.dump(manifest, target, ensure_ascii=False, indent=2)
        target.write("\n")
    return (*output_paths, manifest_path)


def run_exp08(project_root: Path, output_directory: Path, *, stage: str = "all") -> tuple[Path, ...]:
    matrix = load_exp08_matrix(project_root / "scenarios" / "canonical" / "exp08_matrix.yaml")
    outputs: list[Path] = []
    if stage in {"all", "development"}:
        outputs.extend(run_development(project_root, output_directory, matrix))
    if stage in {"all", "confirmatory"}:
        outputs.extend(run_confirmatory(project_root, output_directory, matrix))
    return tuple(outputs)
