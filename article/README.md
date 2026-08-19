# Manuscript sources

`main_en.tex` is the canonical English manuscript for the preprint.
`main.tex` is the Russian source baseline. Both versions use the same
bibliography and computational figures.

The English translation is assembled from semantic blocks under `en/blocks/`.
The translation termbase, source hashes, and resolved editorial queries are
documented in `en/README.md`, `en/termbase.md`, `en/block_manifest.md`, and
`en/translation_queries.md`.

## Build

Run from this directory:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error \
  -outdir=output/pdf main_en.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error \
  -outdir=output/pdf main.tex
```

The authoritative build outputs are `output/pdf/main_en.pdf` and
`output/pdf/main.pdf`. Generated LaTeX files and local build directories are
ignored by Git.

## Computational package

```bash
cd experiments
uv sync --python 3.13
uv run pytest -q
```

EXP-00--EXP-08, their frozen scenario matrices, exact and heuristic results,
and figure-generation commands are described in `experiments/README.md`.

## Interactive artifact

The M4 Human--Agent Workbench source is in `calculator/`; the live deployment
is available at <https://m4.articles.rexarrior.fun/>. It is a companion
interface to the model, not a substitute for the reproducibility package.

## Publication packaging

Do not upload this entire directory to arXiv. The repository-level command
`make arxiv-source` builds an isolated archive containing only the English
LaTeX inputs, bibliography, generated `.bbl`, and figures required to compile
the paper. The experiments, calculator, audit records, and complete results
belong in the versioned repository/archival release instead.
