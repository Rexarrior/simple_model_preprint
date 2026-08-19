# Active preprint release plan

Last updated: 2026-08-19.

This is the only operational plan for the initial preprint release. Historical
plans remain under `tmp_docs/archive/`; the evidence matrix, screening log, and
scientific audits are supporting records rather than task lists.

## Current status

- [x] The M0--M4 formal model and main argument are complete.
- [x] EXP-00--EXP-08, frozen scenarios, raw results, manifests, tests, and
  figure generators are included.
- [x] Mathematical/logical, literature, and claim--citation audits are present.
- [x] Author name, current affiliation, email, ORCID, declarations, and the
  employer-publication disclosure are included.
- [x] MIT and CC BY 4.0 license boundaries are documented.
- [x] The calculator source and independent live deployment are documented.
- [x] The English manuscript is complete, synchronized with the recorded
  Russian baseline hashes, and integrated as `article/main_en.tex`.
- [x] All nine translation queries have explicit editorial resolutions.
- [x] English and Russian build targets and an isolated arXiv-source builder
  are available through the root `Makefile`.
- [x] Copy-ready arXiv metadata and a submission checklist are stored in
  `release/ARXIV_SUBMISSION.md`.
- [x] Full local verification is complete: both PDFs build, experiments and
  calculator checks pass, the isolated arXiv archive builds, and every PDF page
  has passed visual QA.
- [x] Final release PDFs and SHA-256 checksums are stored under `release/`.
- [x] The public Git remote and permanent repository URL are available at
  `https://github.com/Rexarrior/simple_model_preprint`.
- [ ] The immutable `v0.1.0` release and external archival DOI have not been
  created.
- [ ] The arXiv identifier has not been assigned.

## Remaining release sequence

1. [x] Run the complete verification target: manuscript builds, experiment
   tests, calculator tests/lint/audit, isolated arXiv build, and visual PDF QA.
2. [ ] Review the final English PDF and the copy-ready metadata as the author.
3. [x] Publish this repository to a public Git host and record its permanent
   URL in `README.md`, `CITATION.cff`, and both availability statements.
4. [ ] Create the immutable `v0.1.0` tag/release. Attach the English and Russian
   PDFs, arXiv source archive, and SHA-256 checksums.
5. [ ] Archive that exact tagged release in a DOI-issuing repository such as
   Zenodo. Add the artifact DOI to repository metadata and the manuscript's
   availability statement, then rebuild the English PDF and source archive.
6. [ ] Submit the generated source archive to arXiv using
   `release/ARXIV_SUBMISSION.md`; inspect arXiv's compiled PDF before confirming.
7. [ ] After announcement, add the arXiv identifier and arXiv-assigned DOI to
   the repository and citation metadata. Submit an arXiv replacement only if
   the manuscript PDF changes.

## Release gates

- both manuscripts compile from a clean checkout without undefined references,
  citations, labels, box warnings, or missing figures;
- the English PDF has no clipped text, overlap, broken glyphs, unreadable
  figures, or malformed landscape pages;
- experiment and calculator verification passes from locked dependencies;
- the arXiv archive contains one top-level `main.tex` and only required TeX,
  bibliography, `.bbl`, and figure inputs;
- the public release contains no secrets, local databases, virtual
  environments, build caches, or third-party full-text publications;
- repository URL, release tag, checksums, artifact DOI, and manuscript metadata
  agree everywhere they appear.

The remaining external identifiers are the immutable release URL, archival DOI,
and arXiv identifier; they cannot be filled in before those records exist.
