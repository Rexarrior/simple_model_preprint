# arXiv submission metadata

Prepared for the initial English preprint release. Metadata fields on arXiv
accept ASCII text; retain the ASCII double hyphens below.

## Required fields

**Title**

Phase-Based Planning Model for Software Work in a Human--Agent Cell

**Authors**

Aleksandr Rodionov (Yandex)

**Abstract**

This article considers a fixed software-development workload that one developer
completes with the assistance of multiple AI agents. We propose a deterministic
phase-based model that links task-level AI-assisted durations, the dependency
graph, the number of configured agent streams, cross-stream integration
overhead, and a single sequential human-attention resource. The M0--M4
hierarchy distinguishes ideally divisible work from formulations with
indivisible tasks, critical-path constraints, coordination overhead, and exact
schedules of alternating agent and human-attention phases with local blocking
of a waiting agent.

At M4, we derive a structural lower bound on makespan, $B_4$, that combines
agent-stream load, the critical path, and the human resource, and introduce an
exact resource-augmented phase representation of the optimal makespan. A
CP-SAT-based computational package reproduces the calculations for the
illustrative scenarios and shows that $B_4$ is not always attainable: on the
frozen exact grid, a strict certified gap $T^*>B_4$ occurred in 30 of 90
scenarios. On the finite synthetic grid examined, increasing configuration
overhead produced an interior optimum over configured parallelism, positive
decomposition overhead produced U-shaped exact-makespan profiles, and the
interaction contrast between parallelism and granularity was predominantly
positive, although decomposition did not always yield an absolute gain. These
results constitute computational verification and sensitivity analysis of the
model, not an empirical estimate of the performance of any specific tool or
team.

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
