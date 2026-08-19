# Release artifacts

- `phase_based_human_agent_planning_en.pdf` -- canonical English preprint;
- `phase_based_human_agent_planning_ru.pdf` -- Russian-language source version;
- `ARXIV_SUBMISSION.md` -- copy-ready arXiv metadata and submission checklist;
- `SHA256SUMS` -- checksums for the two PDFs and the generated arXiv archive.

The arXiv source archive is generated under `dist/arxiv/` by
`make arxiv-source`; generated archives are intentionally not committed. A
versioned public release should attach both PDFs, the arXiv source archive, and
their SHA-256 checksums.
