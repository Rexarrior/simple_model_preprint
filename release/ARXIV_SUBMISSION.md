# arXiv submission metadata

Prepared for the initial English preprint release. Metadata fields on arXiv
accept ASCII text; retain the ASCII double hyphens below.

## Required fields

**Title**

Phase-Based Planning Model for Software Work in a Human--Agent Cell

**Authors**

Aleksandr Rodionov (Yandex)

**Abstract**

Reduced active human effort per task does not by itself determine project
duration: autonomous intervals may overlap, while dependencies, integration,
and repeated developer attention constrain elapsed time. We compare one
developer using up to $P$ agent streams with sequential no-AI completion of the
same fixed interdependent workload and acceptance criterion.

We propose a deterministic phase-based model linking task- and mode-specific
durations, a task DAG, agent streams, integration overhead, and capacity-one
human attention. Its M0--M4 hierarchy progresses from divisible work through
indivisibility, precedence, and overhead to exact phase schedules with local
slot retention. M0 gives an exact aggregate criterion; under identical-stream,
zero-overhead assumptions, M1--M2 give sufficient speedup guarantees for
indivisibility and precedence.

At M4, the structural lower bound $B_4$ combines stream load, critical-path
length, and total human attention; minimizing the maximum-weight path length
over feasible resource-augmented phase graphs gives $T^*$ exactly. A
reproducible package combines CP-SAT optimization on frozen exact grids with
larger synthetic fixed-policy grids and targeted exact-solver audits. In the
frozen 90-scenario EXP-01 grid, a strict certified gap $T^*>B_4$ occurred in 30
cases. On examined finite grids, configuration-dependent overhead produced
interior minima over $P$, while positive decomposition overhead produced
U-shaped granularity profiles; more streams or finer decomposition need not
reduce makespan.

Within the model, achievable speedup is a property of the fully specified
human--agent process, not of the AI tool or nominal agent count alone. These
results check internal logic rather than estimate a particular tool or team;
practical use requires local calibration.

**Category**

- Primary: `cs.SE` (Software Engineering)
- Recommended cross-list: `cs.MA` (Multiagent Systems)
- Do not add `cs.AI` merely because AI agents appear in the application; the
  paper does not introduce a general AI planning or learning method.

**License**

Creative Commons Attribution 4.0 (`CC BY 4.0`).

## Optional fields

**Comments**

79 pages, 12 figures. Accompanying source code, frozen scenarios, raw results,
and an interactive calculator are available in the versioned artifact
repository. No dedicated funding.

Leave `Journal-ref` and publisher `DOI` empty for the initial preprint. arXiv
assigns its own DataCite DOI after announcement; that identifier is not entered
into the publisher-DOI field.

## Upload checklist

1. Run `make verify` from the repository root.
2. Upload the archive produced by `make arxiv-source`, not the full repository
   and not only the locally generated PDF.
3. Select PDFLaTeX if processor selection is requested.
4. Confirm that arXiv chooses `main.tex` as the sole top-level file.
5. Compare the arXiv-generated PDF with
   `phase_based_human_agent_planning_en.pdf`, including all figures,
   references, page count, and PDF metadata.
6. Confirm the author name, current affiliation, ORCID, category, cross-list,
   abstract, comments, and CC BY 4.0 license before final submission.
7. After announcement, add the arXiv identifier and DOI to the repository,
   `CITATION.cff`, manuscript availability statement, and public release; then
   submit a new arXiv version only if the PDF itself changes.
