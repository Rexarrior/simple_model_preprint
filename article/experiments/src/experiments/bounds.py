from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from .schema import Scenario, topological_task_ids


@dataclass(frozen=True)
class AggregateMetrics:
    t_h: Decimal
    a: Decimal
    h: Decimal
    w3: Decimal
    l3: Decimal
    w4: Decimal
    l4: Decimal
    work_branch: Decimal
    human_branch: Decimal
    b4: Decimal
    active_branches: tuple[str, ...]
    critical_path_l3: tuple[str, ...]
    critical_path_l4: tuple[str, ...]


def _longest_path(
    scenario: Scenario,
    weights: dict[str, Decimal],
) -> tuple[Decimal, tuple[str, ...]]:
    order = topological_task_ids(scenario)
    best: dict[str, Decimal] = {}
    parent: dict[str, str | None] = {}
    tasks = scenario.task_by_id
    for task_id in order:
        predecessors = tasks[task_id].predecessors
        if not predecessors:
            best[task_id] = weights[task_id]
            parent[task_id] = None
            continue
        predecessor = max(
            predecessors,
            key=lambda item: (best[item], item),
        )
        best[task_id] = best[predecessor] + weights[task_id]
        parent[task_id] = predecessor
    last = max(order, key=lambda item: (best[item], item))
    path: list[str] = []
    cursor: str | None = last
    while cursor is not None:
        path.append(cursor)
        cursor = parent[cursor]
    path.reverse()
    return best[last], tuple(path)


def compute_aggregates(scenario: Scenario) -> AggregateMetrics:
    zero = Decimal("0")
    t_h = scenario.x * sum((task.z for task in scenario.tasks), zero)
    a = scenario.x * sum((task.z * task.a for task in scenario.tasks), zero)
    h = scenario.x * sum((task.z * task.h for task in scenario.tasks), zero)

    weights3 = {
        task.task_id: scenario.x
        * task.z
        * (scenario.c * task.a + task.h)
        for task in scenario.tasks
    }
    weights4 = {
        task.task_id: scenario.x
        * task.z
        * (scenario.c * task.a + scenario.gamma * task.h)
        for task in scenario.tasks
    }
    w3 = sum(weights3.values(), zero)
    w4 = sum(weights4.values(), zero)
    l3, path3 = _longest_path(scenario, weights3)
    l4, path4 = _longest_path(scenario, weights4)
    work_branch = w4 / Decimal(scenario.p)
    human_branch = scenario.gamma * h
    branches = {
        "work": work_branch,
        "critical_path": l4,
        "human": human_branch,
    }
    b4 = max(branches.values())
    active = tuple(
        name
        for name, value in branches.items()
        if abs(value - b4) <= scenario.tolerance
    )
    return AggregateMetrics(
        t_h=t_h,
        a=a,
        h=h,
        w3=w3,
        l3=l3,
        w4=w4,
        l4=l4,
        work_branch=work_branch,
        human_branch=human_branch,
        b4=b4,
        active_branches=active,
        critical_path_l3=path3,
        critical_path_l4=path4,
    )
