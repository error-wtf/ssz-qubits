# CHANGELOG_AGENT.md
## Substantial Changes Made During Paper Integration

**Agent Version:** SSZ Paper Integrator v3.0  
**Date:** December 2025

---

## Section Expansions

### 1. Introduction (Section 1)

| Change | Rationale |
|--------|-----------|
| Added "Local vs Global" subsection | Addresses equivalence principle objection preemptively |
| Added "Reader map" paragraph | Guides reader through document structure |
| Expanded motivation beyond "qubits need precision" | Now explains why SSZ specifically matters |

### 2. Claims/Non-Claims (Section 2)

| Change | Rationale |
|--------|-----------|
| Created explicit claim taxonomy table | Prevents misinterpretation of scope |
| Added "What SSZ Does NOT Claim" list | Preemptive defense against overclaim accusations |
| Referenced Figure D.7 (claim taxonomy visual) | Single source of truth |

### 3. Theory (Section 3)

| Change | Rationale |
|--------|-----------|
| Added unit checks after every formula | Reviewer-friendly verification |
| Added GR consistency proof | Shows weak-field equivalence explicitly |
| Expanded numerical examples table | Covers all three platforms |

### 4. Compensation (Section 4)

| Change | Rationale |
|--------|-----------|
| Elevated WITH/WITHOUT to "gold standard" | Was mentioned but not emphasized |
| Added property comparison table | Shows why confounds don't match |
| Added interpretation matrix | Clear decision tree for results |

### 5. Experiments (Section 5)

| Change | Rationale |
|--------|-----------|
| Merged hardware configs from C | Single authoritative list |
| Added protocol pseudocode | Reproducible steps |
| Added upper bound calculation | Shows scientific value |

### 6. Statistics (Section 6)

| Change | Rationale |
|--------|-----------|
| Full M₀/M_SSZ/M_anom framework | Was mentioned, now defined |
| Explicit "Why Not Binary" section | Addresses common misunderstanding |
| Added power analysis | Shows optical clock feasibility |

### 7. Feasibility (Section 7)

| Change | Rationale |
|--------|-----------|
| "12 OoM gap" made headline | Key message for reviewers |
| Platform comparison table expanded | Side-by-side numbers |
| Added roadmap timeline | Concrete next steps |

---

## Clarifications Added

| Topic | Original State | Clarification |
|-------|----------------|---------------|
| Equivalence principle | Not addressed | Section 1.2 explains global comparison |
| Didactic scaling | Defined but scattered | Appendix B with explicit rules |
| Null interpretation | Implicit | "Null is SSZ-consistent" explicit everywhere |
| Statistical framework | Named | Full definition with models |

---

## Content Relocated

| Content | From | To | Reason |
|---------|------|-----|--------|
| Full derivations | Paper A | Appendix A | Main text cleaner |
| Confound matrix | Paper C | Appendix C | Consolidated |
| Symbol table | Scattered | Appendix D | Single source |
| Hardware configs | Paper C | Section 5.1 | With experiments |

---

## Unresolved Ambiguities

| Issue | Resolution Strategy |
|-------|---------------------|
| Optical clock collaboration details | Mark as "future work"; no invented specifics |
| Strong-field predictions | Reference ssz-metric-pure repo for tensor details |
| Exact noise model for optical clocks | Cite Bothwell et al. 2022 |

---

## Removed/Modified Claims

| Original | Modified To | Reason |
|----------|-------------|--------|
| "SSZ enables qubit optimization" | "SSZ identifies deterministic drift (future relevance)" | Detectability caveat |
| Implicit detection at mm-scale | Explicit upper-bound framing | Consistency |
| Binary threshold language | CI/model comparison | Statistical rigor |

---

## Figure/Table Callouts Added

All callouts match FIGURE_TABLE_PLAN.md:

- Figure D.1: Local vs global comparison
- Figure D.2: Phase vs height scaling
- Figure D.3: Coherent zone visualization
- Figure D.4: Platform feasibility
- Figure D.5: Experimental setup
- Figure D.6: Confound discrimination
- Figure D.7: Claim taxonomy
- Table D.1: Symbol table
- Table D.2: Canonical constants
- Table D.3: Platform comparison
- Table D.4: Feasibility map

---

**All changes maintain consistency with CONSISTENCY_REPORT.md constraints.**
