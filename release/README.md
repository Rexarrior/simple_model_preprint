# Release artifacts

Release candidate: `v0.1.0`, assembled and verified on 2026-08-28.

The English PDF and arXiv source archive were rebuilt on 2026-09-05 after
mathematical and logical corrections to the finite-optimum interpretation,
optimality certificate, EXP-02 plateau, EXP-07 decision-rule description,
overhead parameter, and illustrative sensitivity calculations. The frozen
experiment results and Russian reference PDF are unchanged.

- `phase_based_human_agent_planning_en.pdf` -- canonical English preprint;
- `phase_based_human_agent_planning_ru.pdf` -- Russian-language reference
  version; it is intentionally not synchronized with the current English-first
  editorial revision;
- `ARXIV_SUBMISSION.md` -- copy-ready arXiv metadata and submission checklist;
- `SHA256SUMS` -- checksums for the two PDFs and the generated arXiv archive.

The arXiv source archive is generated under `dist/arxiv/` by
`make arxiv-source`; generated archives are intentionally not committed. A
versioned public release should attach both PDFs, the arXiv source archive, and
their SHA-256 checksums. For arXiv itself, upload the generated source archive;
use the English PDF to review the platform-generated preview before submission.
