# Candidate visualizations: inclusion assessment

Date: 2026-08-09.

## Decision applied

1. **Variant-2 schedule comparison — included in the main text, replacing the
   one-panel Gantt.** It directly demonstrates the M4 feasibility claim: the
   left schedule violates the shared human resource, while the right schedule
   restores feasibility and makes local blocking visible.
2. **Resource-augmented critical path — included in the computational-results
   explanation of $T^*>B_4$.** Its reconstructed longest path is
   36.45 hours, equal to the proven optimum of the selected
   EXP-05 scenario. It adds a
   concept not visible in aggregate branches alone; its compact 3x3 layout is
   designed for the final A4 text width.
3. **Task-level intervention map — included in the appendix.** It cleanly shows
   zero/positive local value and reports a global `P:4→5` gain of
   0.00 hours. However, the intervention magnitudes are controlled
   synthetic choices and the planned decomposition column remains
   methodologically undefined for arbitrary tasks.
4. **Probabilistic fan — not included in the current article.** It uses
   100 synthetic draws from the frozen EXP-06 error model, not an
   empirical distribution. It is useful as a design preview for a future
   calibrated study, not as evidence about real deadline risk.

## Not generated

- The empirical calibration map requires observed `prediction–actual` pairs.
- The multiple-cell portfolio visualization belongs to a model extension that
  is explicitly outside the current single-cell scope.
- An interactive simulator is a separate artifact rather than a static article
  figure.
