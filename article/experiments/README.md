# Computational experiments for simple_model_full

This directory contains schema v1, the M4 aggregate calculator, schedule
validator, a deterministic baseline scheduler, an exact CP-SAT model and the
frozen EXP-00--EXP-08 experiment pipelines.

The implementation follows the article semantics:

- a started task keeps one agent slot through final acceptance;
- human phases share one non-preemptive resource;
- a task waiting for a human phase keeps its agent slot;
- C(P) scales only agent phases and gamma(P) only human phases;
- queueing time is derived from assignment and phase timestamps.

The baseline ranks ready tasks by decreasing bottom level and task weight.
Human requests use FCFS, with the same priority and identifiers as deterministic
tie-breakers.

## Environment

From this directory:

    uv sync --python 3.13

The lockfile pins OR-Tools, PyYAML and Matplotlib. The project uses a local
virtual environment created by uv.

## Validate scenarios

    uv run python -m experiments validate scenarios/article

The command treats the original schedule of variant 2 as an expected invalid
case and prints the M4 resource conflict.

## Run EXP-00

    uv run python -m experiments run --experiment EXP-00

Outputs:

- results/exp00_summary.csv;
- results/exp00_manifest.json;
- figures/exp00_dag_variants_3_4.*;
- figures/exp00_gantt_variant_2.*.

The summary compares the article schedule and baseline with the proven CP-SAT
optimum. The manifest records dependency versions and SHA-256 hashes.

The interpreted Russian-language report, including both figures, is maintained
separately in `results/exp00_report.md`. It is not inserted into the article.

## Run EXP-01

    uv run python -m experiments run --experiment EXP-01

EXP-01 executes the frozen 90-point exact matrix at `N=4` and writes:

- `results/exp01_runs.csv`;
- `results/exp01_profile_pairs.csv`;
- `results/exp01_counterexample.json`;
- `results/exp01_manifest.json`;
- `results/exp01_report.md`;
- `figures/exp01_gaps.*`;
- `figures/exp01_counterexample_gantt.*` when a counterexample exists.

The matrix is frozen in `scenarios/canonical/exp01_matrix.yaml`. EXP-01 keeps
the lower-bound tightness gap separate from the baseline heuristic gap.
The original 270-point pilot matrix and the common-limit failure that triggered
the predeclared global size reduction are preserved alongside it.

## Run EXP-02

    uv run python -m experiments run --experiment EXP-02

EXP-02 executes a frozen 70-point sweep over
`P in {1, 2, 3, 4, 6, 8, 12}` for two fixed objects and five unique regimes.
It writes:

- `results/exp02_runs.csv`;
- `results/exp02_optimal_p.csv`;
- `results/exp02_manifest.json`;
- `results/exp02_report.md`;
- `figures/exp02_scaling_curve.*`;
- `figures/exp02_active_constraints.*`.

The matrix is frozen in `scenarios/canonical/exp02_matrix.yaml`. Exact status,
best bound and gap are recorded separately from the deterministic baseline;
non-optimal incumbents are never labelled as `T_star`. The practical object
preserves the variant-4 DAG and task totals while applying the synthetic human
shares declared by the EXP-02 design.

## Run EXP-03

    uv run python -m experiments run --experiment EXP-03

EXP-03 executes 32 exact and baseline points for two DAGs, two values of `P`,
two human shares and four phase profiles. It writes:

- `results/exp03_runs.csv`;
- `results/exp03_profile_pairs.csv`;
- `results/exp03_sync_staggered_pairs.csv`;
- `results/exp03_phases.csv` and `results/exp03_events.csv`;
- `results/exp03_counterexample.json`;
- `results/exp03_manifest.json` and `results/exp03_report.md`;
- `figures/exp03_profile_effects.*`;
- `figures/exp03_queue_blocking.*`.

All pairwise comparisons use IO as the reference while preserving the DAG,
`A`, `H`, `W4`, `L4` and `B4`. Full-agent-stop time is measured only when all
`P` slots are occupied and zero agent phases are executing.

## Run EXP-04

    uv run python -m experiments run --experiment EXP-04

EXP-04A reuses the proven practical comparison from EXP-00. EXP-04B applies a
frozen decomposition operator to one critical canonical task. The raw
`6 x 5 x 3 = 90` grid is deduplicated to 66 semantic scenarios and writes:

- `results/exp04a_summary.csv`;
- `results/exp04b_runs.csv` and `results/exp04b_optimal_m.csv`;
- `results/exp04b_phases.csv` and `results/exp04b_events.csv`;
- `results/exp04_manifest.json` and `results/exp04_report.md`;
- `figures/exp04_decomposition_curves.*`;
- `figures/exp04_optimal_granularity.*`.

The join retains the selected task's quality gate. Useful work is conserved at
zero overhead, while every positive overhead contribution is traced separately
to agent and human work.

## Run EXP-05

    uv run python -m experiments run --experiment EXP-05

EXP-05 reuses the frozen EXP-04B operator and varies both agent slots `P` and
parallel subtasks `m`. The raw `6 x 6 x 3 x 2 = 216` grid is deduplicated to
156 semantic scenarios, then reconstructed for analysis. It writes:

- `results/exp05_runs.csv` and `results/exp05_grid.csv`;
- `results/exp05_interactions.csv` and `results/exp05_optimal_m.csv`;
- `results/exp05_phases.csv` and `results/exp05_events.csv`;
- `results/exp05_manifest.json` and `results/exp05_report.md`;
- `figures/exp05_makespan_heatmaps.*`;
- `figures/exp05_interaction_contrast.*`;
- `figures/exp05_active_constraints.*`.

The interaction contrast is computed only when all four required objectives
are proven `OPTIMAL`. Feasible incumbents remain separate from `T_star`.

## Run EXP-06

    uv run python -m experiments run --experiment EXP-06

EXP-06 separates three claims: exact invariance to a common time scale,
ranking stability of practical variants 3 and 4 under paired random relative
errors, and two frozen adverse boundary directions. It writes:

- `results/exp06a_scale.csv`, phases and events;
- `results/exp06b_pairs.csv`, sampled multipliers and aggregate summary;
- `results/exp06c_pairs.csv` and threshold summary;
- `results/exp06_manifest.json` and `results/exp06_report.md`;
- `figures/exp06_scale_invariance.*`;
- `figures/exp06_ranking_stability.*` and `exp06_margin_distributions.*`;
- `figures/exp06_adversarial_thresholds.*`.

Random and adverse errors use different frozen models. Neither is described as
an empirical confidence interval.

## Run EXP-07

    uv run python -m experiments run --experiment EXP-07

EXP-07 runs a frozen stratified pilot of 1440 accepted synthetic DAGs: four
task counts, three topology families, homogeneous or lognormal weights, three
human-work concentration strata and 20 observation seeds per cell. It writes:

- `results/exp07_generation_attempts.csv` and `results/exp07_dags.csv`;
- `results/exp07_runs.csv` and `results/exp07_exact.csv`;
- `results/exp07_claim_pairs.csv` and `results/exp07_claim_summary.csv`;
- `results/exp07_manifest.json` and `results/exp07_report.md`;
- `figures/exp07_design_coverage.*` and `figures/exp07_claim_effects.*`.

The full sample reports only the frozen deterministic policy and lower bounds.
The exact audit is restricted to 12 predeclared DAGs with `N <= 16` and to 36
baseline-gap/C1 scenarios after a pre-outcome global resource amendment; only
`OPTIMAL` objectives are labelled `T_star`. C2--C4 remain policy/lower-bound
contrasts. Topology family is stratified with the `rho_L` bin, so those two
effects are explicitly not separately identified.

## Run EXP-08

EXP-08 deliberately separates development and confirmatory data. Run the
stages in order:

    uv run python -m experiments run --experiment EXP-08 --stage development
    uv run python -m experiments run --experiment EXP-08 --stage confirmatory

The development stage generates 240 new graph bases in the
`EXP-08-development-v1` namespace, validates paired allocation and records
timing only. It writes `results/exp08_freeze.json`; development rows are never
used to estimate effects. The confirmatory command refuses to run without a
matching freeze file and then generates 480 different graph bases in the
`EXP-08-confirmatory-v1` namespace. No EXP-07 DAG or raw seed is reused.

Confirmatory outputs include invariant checks, policy schedule effects,
differentiated-slowdown path effects, a small exact audit selected by the
predeclared development timing rule, a report and three PNG/SVG figures. The
shortcut `--stage all` performs the two stages sequentially, but the explicit
commands above make the freeze boundary easier to audit.

## Build the first two article figures

    uv run python -m experiments figures --set main

Outputs are written as SVG and PNG:

- figures/exp00_dag_variants_3_4.*;
- figures/exp00_gantt_variant_2.*.

## Build candidate additional figures

    uv run python -m experiments figures --set candidates

This command creates four additional visualizations: the original versus
resource-feasible schedule for variant 2, a resource-augmented EXP-05 path, a
task-level intervention map for variant 4, and an illustrative probability fan
that reuses the frozen EXP-06 error model.
It also writes the underlying candidate CSV files and
`results/candidate_visualizations_report.md`. The first three figures are used
in the article or its appendix; the probability fan remains a design preview
and is not included.

## Tests

    uv run pytest
