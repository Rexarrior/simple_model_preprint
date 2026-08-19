# English manuscript workspace

This directory contains the English translation of the manuscript. The Russian
sources in the parent directory remain the source baseline and are not edited
during translation.

Translation is performed in numbered semantic blocks under `blocks/`. Each
block preserves the source order, mathematics, labels, references, citations,
numbers, paths, experiment identifiers, and machine-readable names.

The Russian baseline was rebuilt on 2026-08-13 from `../main.tex`: 84 pages.
The English integration was audited again on 2026-08-19 against the baseline
hashes below.

## Integrated English manuscript

The complete English manuscript is assembled by `../main_en.tex`. All 35
translation blocks are connected in source order through the section-level
files in this directory. The language note from the Russian working version is
intentionally omitted, and the English build uses T1 encoding and English
babel settings.

Build from the `article` directory with:

```text
latexmk -pdf -interaction=nonstopmode -halt-on-error \
  -outdir=output/pdf main_en.tex
```

The verified output is `../output/pdf/main_en.pdf` (79 A4 pages). The final
build has no undefined references or citations, duplicate labels, LaTeX errors,
or box warnings. Editorial ambiguities found during translation and their
explicit resolutions are listed in `translation_queries.md`.

## Baseline hashes

- `main.tex`: `64716d18158da90b0c3dc6181e936d2f26dd6c26818210680e9b8d3465b2cc52`
- `Базовая модель.tex`: `48410b1618aa897b4434a51be7e54990019d29844d466f9d9cd382249e676ff9`
- `Краткие термины и обозначения.tex`: `fc0ca9a011b2496084ae59cb2ed2c0d88de963ca71872867c65497b9c0a337ba`
- `Термины и обозначения.tex`: `96fb5bcb40264bc5ec8e7cfe2d3e1c52f5d63765678c5e351bbf430c9ee9871a`
- `computational_method.tex`: `dc0145fb09470a42e834e4ad69b034f5cb3e3c57d12f9a2821cce30d1c039e5e`
- `computational_results.tex`: `26507b1913becc75961a1bfb6adaa84ddf2129a162f0fffc07f903b41e32ba39`
- `Введение.tex`: `952211ebee9376e74a0310a7e28a0fec832511eede7d25e599a471a86c76e044`
- `conclusion.tex`: `f540e1621add035f18f011f54613e0fedcf69da9090db5d5de7ec616ef699663`
