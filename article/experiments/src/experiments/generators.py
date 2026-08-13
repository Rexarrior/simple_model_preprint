from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Iterator

import yaml

from .schema import (
    PhaseSpec,
    Scenario,
    ScenarioError,
    TaskSpec,
    decimal,
    validate_scenario,
)


@dataclass(frozen=True)
class Exp01Matrix:
    source_path: Path
    schema_version: int
    experiment_id: str
    frozen_at: str
    seed: int
    expected_point_count: int
    topologies: tuple[str, ...]
    task_counts: tuple[int, ...]
    agent_counts: tuple[int, ...]
    human_shares: tuple[Decimal, ...]
    phase_profiles: tuple[str, ...]
    time_unit: Decimal
    tolerance: Decimal
    task_weight_cycle: tuple[Decimal, ...]
    c: Decimal
    gamma: Decimal
    solver_time_limit_seconds: float
    solver_random_seed: int
    solver_workers: int

    @property
    def point_count(self) -> int:
        return (
            len(self.topologies)
            * len(self.task_counts)
            * len(self.agent_counts)
            * len(self.human_shares)
            * len(self.phase_profiles)
        )


@dataclass(frozen=True)
class Exp01Case:
    topology: str
    task_count: int
    agent_count: int
    human_share: Decimal
    phase_profile: str
    scenario: Scenario


def _required_list(raw: object, *, field: str) -> list[object]:
    if not isinstance(raw, list) or not raw:
        raise ScenarioError(f"{field}: expected non-empty list")
    return raw


def load_exp01_matrix(path: str | Path) -> Exp01Matrix:
    source_path = Path(path).resolve()
    with source_path.open("r", encoding="utf-8") as source:
        raw = yaml.safe_load(source)
    if not isinstance(raw, dict):
        raise ScenarioError("EXP-01 matrix must be a mapping")
    if raw.get("frozen") is not True:
        raise ScenarioError("EXP-01 matrix must be frozen before execution")
    exact = raw.get("exact_solver")
    if not isinstance(exact, dict):
        raise ScenarioError("exact_solver must be a mapping")

    matrix = Exp01Matrix(
        source_path=source_path,
        schema_version=int(raw.get("schema_version", 0)),
        experiment_id=str(raw.get("experiment_id", "")),
        frozen_at=str(raw.get("frozen_at", "")),
        seed=int(raw.get("seed", 0)),
        expected_point_count=int(raw.get("expected_point_count", 0)),
        topologies=tuple(
            str(item) for item in _required_list(raw.get("topologies"), field="topologies")
        ),
        task_counts=tuple(
            int(item) for item in _required_list(raw.get("task_counts"), field="task_counts")
        ),
        agent_counts=tuple(
            int(item) for item in _required_list(raw.get("agent_counts"), field="agent_counts")
        ),
        human_shares=tuple(
            decimal(item, field="human_shares")
            for item in _required_list(raw.get("human_shares"), field="human_shares")
        ),
        phase_profiles=tuple(
            str(item)
            for item in _required_list(raw.get("phase_profiles"), field="phase_profiles")
        ),
        time_unit=decimal(raw.get("time_unit"), field="time_unit"),
        tolerance=decimal(raw.get("tolerance"), field="tolerance"),
        task_weight_cycle=tuple(
            decimal(item, field="task_weight_cycle")
            for item in _required_list(
                raw.get("task_weight_cycle"), field="task_weight_cycle"
            )
        ),
        c=decimal(raw.get("c"), field="c"),
        gamma=decimal(raw.get("gamma"), field="gamma"),
        solver_time_limit_seconds=float(exact.get("time_limit_seconds", 60)),
        solver_random_seed=int(exact.get("random_seed", 0)),
        solver_workers=int(exact.get("workers", 1)),
    )
    _validate_exp01_matrix(matrix)
    return matrix


def _validate_exp01_matrix(matrix: Exp01Matrix) -> None:
    expected_topologies = {
        "chain",
        "independent",
        "fork_join",
        "diamond",
        "two_layer",
    }
    expected_profiles = {"io", "alternating_sync", "alternating_staggered"}
    if matrix.schema_version != 1 or matrix.experiment_id != "EXP-01":
        raise ScenarioError("EXP-01 matrix requires schema_version=1 and experiment_id=EXP-01")
    if set(matrix.topologies) != expected_topologies:
        raise ScenarioError("EXP-01 matrix must contain the five canonical topologies")
    if set(matrix.phase_profiles) != expected_profiles:
        raise ScenarioError("EXP-01 matrix must contain the three frozen profiles")
    if any(value < 4 for value in matrix.task_counts):
        raise ScenarioError("canonical DAGs require at least four tasks")
    if any(value <= 0 for value in matrix.agent_counts):
        raise ScenarioError("agent counts must be positive")
    if any(value <= 0 or value >= 1 for value in matrix.human_shares):
        raise ScenarioError("human shares must lie strictly between zero and one")
    if matrix.time_unit <= 0 or matrix.tolerance < 0:
        raise ScenarioError("time_unit and tolerance are invalid")
    if any(value <= 0 for value in matrix.task_weight_cycle):
        raise ScenarioError("task weights must be positive")
    if matrix.solver_workers != 1:
        raise ScenarioError("EXP-01 exact runs are frozen to one worker")
    if matrix.point_count != matrix.expected_point_count:
        raise ScenarioError(
            "frozen EXP-01 matrix point count mismatch: "
            f"expected {matrix.expected_point_count}, got {matrix.point_count}"
        )


def _task_ids(task_count: int) -> tuple[str, ...]:
    width = max(2, len(str(task_count)))
    return tuple(f"t{index + 1:0{width}d}" for index in range(task_count))


def canonical_predecessors(topology: str, task_count: int) -> tuple[tuple[str, ...], ...]:
    task_ids = _task_ids(task_count)
    predecessors: list[tuple[str, ...]] = [() for _ in task_ids]
    if topology == "independent":
        return tuple(predecessors)
    if topology == "chain":
        for index in range(1, task_count):
            predecessors[index] = (task_ids[index - 1],)
        return tuple(predecessors)
    if topology == "fork_join":
        for index in range(1, task_count - 1):
            predecessors[index] = (task_ids[0],)
        predecessors[-1] = tuple(task_ids[1:-1])
        return tuple(predecessors)
    if topology == "diamond":
        branch_a = list(range(1, task_count - 1, 2))
        branch_b = list(range(2, task_count - 1, 2))
        for branch in (branch_a, branch_b):
            for offset, index in enumerate(branch):
                predecessors[index] = (
                    task_ids[0] if offset == 0 else task_ids[branch[offset - 1]],
                )
        sink_predecessors = [task_ids[branch[-1]] for branch in (branch_a, branch_b) if branch]
        predecessors[-1] = tuple(sink_predecessors)
        return tuple(predecessors)
    if topology == "two_layer":
        width = task_count // 2
        for index in range(width, task_count):
            left = (index - width) % width
            right = (left + 1) % width
            predecessors[index] = tuple(sorted({task_ids[left], task_ids[right]}))
        return tuple(predecessors)
    raise ScenarioError(f"unknown canonical topology {topology}")


def _profile_phases(
    profile: str,
    *,
    task_index: int,
    agent_duration: Decimal,
    human_duration: Decimal,
) -> tuple[PhaseSpec, ...]:
    if profile == "io":
        return (
            PhaseSpec("human_1", "human", human_duration / Decimal(2)),
            PhaseSpec("agent_1", "agent", agent_duration),
            PhaseSpec("human_2", "human", human_duration / Decimal(2)),
        )
    if profile == "front_loaded":
        return (
            PhaseSpec(
                "human_1",
                "human",
                human_duration * Decimal("0.90"),
            ),
            PhaseSpec("agent_1", "agent", agent_duration),
            PhaseSpec(
                "human_2",
                "human",
                human_duration * Decimal("0.10"),
            ),
        )

    human_parts = [human_duration / Decimal(4)] * 4
    if profile == "alternating_sync":
        agent_parts = [agent_duration / Decimal(3)] * 3
    elif profile == "alternating_staggered":
        numerator_cycles = ((1, 2, 3), (2, 3, 1), (3, 1, 2))
        numerators = numerator_cycles[task_index % len(numerator_cycles)]
        agent_parts = [
            agent_duration * Decimal(numerator) / Decimal(6)
            for numerator in numerators
        ]
    else:
        raise ScenarioError(f"unknown phase profile {profile}")

    phases: list[PhaseSpec] = []
    for index, human_part in enumerate(human_parts):
        phases.append(PhaseSpec(f"human_{index + 1}", "human", human_part))
        if index < len(agent_parts):
            phases.append(
                PhaseSpec(f"agent_{index + 1}", "agent", agent_parts[index])
            )
    return tuple(phases)


def build_exp01_scenario(
    matrix: Exp01Matrix,
    *,
    topology: str,
    task_count: int,
    agent_count: int,
    human_share: Decimal,
    phase_profile: str,
) -> Scenario:
    task_ids = _task_ids(task_count)
    predecessors = canonical_predecessors(topology, task_count)
    tasks: list[TaskSpec] = []
    for index, task_id in enumerate(task_ids):
        weight = matrix.task_weight_cycle[index % len(matrix.task_weight_cycle)]
        human_duration = weight * human_share
        agent_duration = weight - human_duration
        tasks.append(
            TaskSpec(
                task_id=task_id,
                name=f"Canonical task {index + 1}",
                z=weight,
                k=Decimal("1"),
                h=human_share,
                predecessors=predecessors[index],
                phases=_profile_phases(
                    phase_profile,
                    task_index=index,
                    agent_duration=agent_duration,
                    human_duration=human_duration,
                ),
                quality_gate_id=f"qg_{task_id}",
            )
        )
    human_label = int(human_share * Decimal(100))
    scenario = Scenario(
        schema_version=1,
        scenario_id=(
            f"exp01_{topology}_n{task_count}_p{agent_count}_"
            f"rh{human_label:02d}_{phase_profile}"
        ),
        variant_id="EXP-01",
        time_unit=matrix.time_unit,
        tolerance=matrix.tolerance,
        x=Decimal("1"),
        p=agent_count,
        c=matrix.c,
        gamma=matrix.gamma,
        tasks=tuple(tasks),
        schedules=(),
        source_path=matrix.source_path,
    )
    validate_scenario(scenario)
    return scenario


def iter_exp01_cases(matrix: Exp01Matrix) -> Iterator[Exp01Case]:
    for topology in matrix.topologies:
        for task_count in matrix.task_counts:
            for agent_count in matrix.agent_counts:
                for human_share in matrix.human_shares:
                    for phase_profile in matrix.phase_profiles:
                        yield Exp01Case(
                            topology=topology,
                            task_count=task_count,
                            agent_count=agent_count,
                            human_share=human_share,
                            phase_profile=phase_profile,
                            scenario=build_exp01_scenario(
                                matrix,
                                topology=topology,
                                task_count=task_count,
                                agent_count=agent_count,
                                human_share=human_share,
                                phase_profile=phase_profile,
                            ),
                        )
