# Phase-Based Planning Model for Software Work in a Human--Agent Cell

This repository accompanies Aleksandr Rodionov's preprint on planning a fixed
software-development workload performed by one developer with multiple AI
agents.

Public repository: <https://github.com/Rexarrior/simple_model_preprint>

The canonical manuscript for international distribution is the English source
at [`article/main_en.tex`](article/main_en.tex). The Russian source at
[`article/main.tex`](article/main.tex) is retained as the translation baseline
and for the Russian-language release.

## Current release candidate

- [English preprint PDF](release/phase_based_human_agent_planning_en.pdf)
- [Russian reference PDF](release/phase_based_human_agent_planning_ru.pdf)
- [arXiv metadata and upload checklist](release/ARXIV_SUBMISSION.md)
- [release checksums](release/SHA256SUMS)

Release, artifact DOI, and arXiv identifiers are intentionally not shown until
the corresponding public records exist.

## Repository contents

- `article/` -- English and Russian LaTeX sources and the bibliography;
- `article/experiments/` -- the reproducible EXP-00--EXP-08 computational
  package, frozen scenarios, tests, raw results, and figure generators;
- `article/calculator/` -- source code for the M4 Human--Agent Workbench;
- `article/literature_reviews/` -- author-written source reviews;
- `tmp_docs/` -- the active release plan, literature-search protocol, evidence
  matrix, and scientific-audit records;
- `release/` -- distribution PDFs and arXiv submission metadata;
- `scripts/` -- release and arXiv-source builders.

Full-text PDFs of third-party publications are intentionally excluded. The
repository contains bibliographic records, the search protocol, an evidence
matrix, and original source-review notes, but does not redistribute copyrighted
source material.

## Build the manuscripts

Requirements: a recent TeX Live installation with `latexmk`, `pdflatex`, and
BibTeX.

```bash
make pdf-en
make pdf-ru
```

The generated PDFs are written to `article/output/pdf/`. To construct the
minimal source archive intended for arXiv, run:

```bash
make arxiv-source
```

The archive and its SHA-256 checksum are written to `dist/arxiv/`. The builder
uses the LaTeX recorder output to include only source files and figures required
by the English manuscript, then verifies that the isolated archive compiles.

## Verify the research artifacts

```bash
make test-experiments
make test-calculator
```

The experiment environment is locked by `uv.lock`. The calculator environment
is locked by `package-lock.json`.

## Licenses

- source code, tests, and build/deployment configuration: MIT;
- manuscript text, documentation, author-created figures, scenarios, and
  results: CC BY 4.0;
- third-party works and trademarks are excluded.

See [`LICENSE.md`](LICENSE.md) for the precise scope.

## Author and disclosure

Aleksandr Rodionov -- Yandex, Saint Petersburg, Russia<br>
<rexarrior@yandex.ru><br>
[ORCID 0009-0006-6710-923X](https://orcid.org/0009-0006-6710-923X)

The research was conducted independently in the author's personal time and
received no dedicated funding from Yandex. Some computational work used Yandex
equipment and computing infrastructure. The views expressed are solely those
of the author and do not necessarily represent those of Yandex.
