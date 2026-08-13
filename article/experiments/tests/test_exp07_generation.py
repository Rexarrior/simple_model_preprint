from __future__ import annotations

from collections import Counter
from decimal import Decimal
from pathlib import Path

from experiments.bounds import compute_aggregates
from experiments.exp07 import (
    _decompose,
    _is_exact_dag,
    build_scenario,
    generate_dags,
    load_exp07_matrix,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = PROJECT_ROOT / "scenarios" / "canonical" / "exp07_matrix.yaml"


def test_frozen_exp07_generator_counts_and_bins() -> None:
    matrix = load_exp07_matrix(MATRIX_PATH)
    dags, attempts = generate_dags(matrix)

    assert len(dags) == 1440
    assert sum(row["accepted"] == "true" for row in attempts) == 1440
    assert len({dag.dag_id for dag in dags}) == 1440
    counts = Counter(
        (
            dag.task_count,
            dag.topology_family,
            dag.weight_type,
            dag.human_concentration_bin,
        )
        for dag in dags
    )
    assert set(counts.values()) == {20}
    for dag in dags:
        assert matrix.rho_l_bins[dag.target_rho_l_bin].contains(dag.rho_l)
        assert matrix.rho_h_bins[dag.human_concentration_bin].contains(dag.rho_h_cp)
        assert not dag.predecessors[0]
        assert all(dag.predecessors[index] for index in range(1, dag.task_count))


def test_human_strata_reuse_the_same_graph_and_weights() -> None:
    matrix = load_exp07_matrix(MATRIX_PATH)
    dags, _ = generate_dags(matrix)
    signatures: dict[tuple[int, str, str, int], set[tuple[object, ...]]] = {}
    for dag in dags:
        key = (
            dag.task_count,
            dag.topology_family,
            dag.weight_type,
            dag.observation_seed,
        )
        signatures.setdefault(key, set()).add(
            (dag.raw_seed, dag.predecessors, dag.weights, dag.critical_path, dag.rho_l)
        )
    assert len(signatures) == 480
    assert all(len(items) == 1 for items in signatures.values())


def test_phase_profiles_preserve_frozen_aggregates() -> None:
    matrix = load_exp07_matrix(MATRIX_PATH)
    dags, _ = generate_dags(matrix)
    dag = next(
        item
        for item in dags
        if item.task_count == 16
        and item.topology_family == "mixed"
        and item.weight_type == "lognormal"
        and item.human_concentration_bin == "medium"
    )
    aggregates = [
        compute_aggregates(build_scenario(matrix, dag, profile=profile))
        for profile in ("io", "alternating_sync", "alternating_staggered")
    ]
    assert {(item.w4, item.l4, item.b4, item.critical_path_l4) for item in aggregates} == {
        (
            aggregates[0].w4,
            aggregates[0].l4,
            aggregates[0].b4,
            aggregates[0].critical_path_l4,
        )
    }


def test_decomposition_conserves_work_at_zero_overhead() -> None:
    matrix = load_exp07_matrix(MATRIX_PATH)
    dags, _ = generate_dags(matrix)
    dag = next(
        item
        for item in dags
        if item.task_count == 8
        and item.topology_family == "chain_like"
        and item.weight_type == "homogeneous"
        and item.human_concentration_bin == "medium"
    )
    base = build_scenario(matrix, dag, profile="io", p=4)
    decomposed, selected = _decompose(matrix, base, overhead_rate=Decimal("0"))
    base_metrics = compute_aggregates(base)
    decomposed_metrics = compute_aggregates(decomposed)
    assert decomposed_metrics.w4 == base_metrics.w4
    assert decomposed.task_by_id[f"{selected}_join"].quality_gate_id == base.task_by_id[selected].quality_gate_id


def test_exact_audit_selection_is_frozen_to_twelve_dags() -> None:
    matrix = load_exp07_matrix(MATRIX_PATH)
    dags, _ = generate_dags(matrix)
    selected = [dag for dag in dags if _is_exact_dag(matrix, dag)]
    assert len(selected) == matrix.expected_exact_dags == 12
    assert {dag.task_count for dag in selected} == {8, 16}
    assert {dag.weight_type for dag in selected} == {"homogeneous"}
    assert {dag.human_concentration_bin for dag in selected} == {"medium"}
    assert {dag.observation_seed for dag in selected} == {0, 1}
    assert matrix.expected_exact_scenarios == 36
    assert matrix.exact_time_limit == 10
