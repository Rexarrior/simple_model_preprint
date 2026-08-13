from __future__ import annotations

from decimal import Decimal
from pathlib import Path

from experiments.bounds import compute_aggregates
from experiments.exp08 import (
    build_scenario,
    generate_graphs,
    load_exp08_matrix,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = PROJECT_ROOT / "scenarios" / "canonical" / "exp08_matrix.yaml"


def test_exp08_streams_are_new_balanced_and_disjoint() -> None:
    matrix = load_exp08_matrix(MATRIX_PATH)
    development, _ = generate_graphs(matrix, "development")
    confirmatory, _ = generate_graphs(matrix, "confirmatory")

    assert len(development) == 240
    assert len(confirmatory) == 480
    assert {item.raw_seed for item in development}.isdisjoint(
        item.raw_seed for item in confirmatory
    )
    assert len({item.cell_id for item in development}) == 24
    assert len({item.cell_id for item in confirmatory}) == 24
    assert {
        sum(item.cell_id == cell for item in development)
        for cell in {item.cell_id for item in development}
    } == {10}
    assert {
        sum(item.cell_id == cell for item in confirmatory)
        for cell in {item.cell_id for item in confirmatory}
    } == {20}


def test_exp08_allocator_preserves_total_and_hits_targets() -> None:
    matrix = load_exp08_matrix(MATRIX_PATH)
    graphs, _ = generate_graphs(matrix, "development")
    for graph in graphs:
        total_work = sum(graph.weights, Decimal("0"))
        for label, humans, actual in (
            ("low", graph.human_low, graph.rho_h_low),
            ("high", graph.human_high, graph.rho_h_high),
        ):
            assert sum(humans, Decimal("0")) == total_work * Decimal("0.12")
            assert actual == matrix.concentrations[label]
            shares = [human / weight for human, weight in zip(humans, graph.weights, strict=True)]
            assert min(shares) >= Decimal("0.025")
            assert max(shares) <= Decimal("0.85")


def test_exp08_aggregate_identity_and_negative_control() -> None:
    matrix = load_exp08_matrix(MATRIX_PATH)
    graphs, _ = generate_graphs(matrix, "development")
    graph = next(item for item in graphs if item.task_count == 16 and item.topology_family == "mixed" and item.weight_type == "lognormal")

    for profile in matrix.phase_profiles:
        for p in matrix.agent_counts:
            low = compute_aggregates(build_scenario(matrix, graph, allocation="low", profile=profile, p=p))
            high = compute_aggregates(build_scenario(matrix, graph, allocation="high", profile=profile, p=p))
            assert (low.h, low.w4, low.l4, low.b4, low.active_branches, low.critical_path_l4) == (
                high.h,
                high.w4,
                high.l4,
                high.b4,
                high.active_branches,
                high.critical_path_l4,
            )


def test_exp08_differentiated_slowdown_reference_path_identity() -> None:
    matrix = load_exp08_matrix(MATRIX_PATH)
    graphs, _ = generate_graphs(matrix, "development")
    graph = graphs[0]
    low = build_scenario(matrix, graph, allocation="low", profile="io", p=4, c=Decimal("1"), gamma=Decimal("1.3"))
    high = build_scenario(matrix, graph, allocation="high", profile="io", p=4, c=Decimal("1"), gamma=Decimal("1.3"))
    selected = set(graph.reference_path)
    low_length = sum((low.c * task.a + low.gamma * task.h for task in low.tasks if task.task_id in selected), Decimal("0"))
    high_length = sum((high.c * task.a + high.gamma * task.h for task in high.tasks if task.task_id in selected), Decimal("0"))
    expected = Decimal("0.3") * Decimal("0.4") * compute_aggregates(low).h
    assert high_length - low_length == expected
