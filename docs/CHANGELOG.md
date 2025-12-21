# SSZ Paper Suite: Changelog

**Version:** 1.0  
**Date:** 2025-12-21  
**Authors:** Carmen Wrede & Lino Casu

---

## Overview

This changelog documents all modifications made to Papers A, B, C, and D to achieve publication-ready consistency.

---

## Paper D (Master Document) - v2.0

### Major Changes
- [x] **NEW:** Complete rewrite as unified master document
- [x] **NEW:** 5-part structure (Foundations, Predictions, Control, Feasibility, Falsifiability)
- [x] **NEW:** Explicit claim taxonomy (Bounded/Detectable/Future)
- [x] **NEW:** Symbol table at document start
- [x] **NEW:** 7 publication-quality figures

### Content Additions
- [x] Section on "Local vs Global" comparison (addresses equivalence principle)
- [x] Platform comparison table (Transmon vs Optical Clock)
- [x] Statistical falsification framework (slope-fitting, CI)
- [x] Upper-bound experiment design with concrete example
- [x] Confound discrimination matrix
- [x] Reproducibility package reference (150 tests)

### Numerical Corrections
- [x] Verified all ΔΦ calculations with unit checks
- [x] Optical clock: ΔΦ @ 1m = 0.59 rad (corrected from ~0.29)
- [x] Transmon @ 1mm: ΔΦ = 6.87×10⁻¹³ rad (verified)
- [x] Coherent zone widths recalculated and verified

### Language Refinements
- [x] "State-of-the-art" → "Representative" for noise estimates
- [x] Removed any implied detectability at mm-scale
- [x] Added "null result is SSZ-consistent" message
- [x] SSZ vs GR framing: "operational layer in weak-field"

---

## Paper C (Experimental Framework) - v1.2 → v1.3

### Major Changes
- [x] Reframed as upper-bound experiment
- [x] Added platform comparison (optical clocks as gold standard)
- [x] Replaced binary falsification thresholds with statistical framework

### Content Additions
- [x] Feasibility analysis section with ~12 OoM gap acknowledgment
- [x] Chip tilt formula: Δh = L × sin(θ)
- [x] Concrete upper-bound calculation example
- [x] Averaging requirements table

### Numerical Corrections
- [x] Optical clock ΔΦ @ 1m: 0.59 rad (recalculated)
- [x] N_required for SNR=3 verified
- [x] All phase drift values cross-checked

### Removed/Modified Claims
- [x] ~~"10⁶ averages sufficient"~~ → Explicit averaging requirements
- [x] ~~Binary falsification thresholds~~ → Slope-fitting with CI
- [x] ~~Implied detectability~~ → Upper bound framing

---

## Paper B (Phase Coherence) - v1.0 → v1.1

### Major Changes
- [x] Added feasibility caveat paragraph
- [x] Referenced optical clocks as future direction
- [x] Added repo/test suite reference

### Content Additions
- [x] Note on ~12 OoM gap at mm-scale with current technology
- [x] Reference to Paper C for experimental details
- [x] Link to reproducibility package

### Language Refinements
- [x] "SSZ effects are relevant" → "SSZ effects become relevant when..."
- [x] Added regime qualifiers (current vs future systems)
- [x] Explicit T₂ and Δh requirements for relevance

### Numerical Corrections
- [x] All formulas verified against canonical values
- [x] Coherent zone table values verified

---

## Paper A (Qubit Optimization) - v1.0 → v1.1

### Major Changes
- [x] Added feasibility caveat paragraph
- [x] Clarified didactic scaling in simulations
- [x] Added repo/test suite reference

### Content Additions
- [x] Note on current vs future relevance
- [x] Reference to Paper C/D for feasibility details
- [x] Link to reproducibility package

### Language Refinements
- [x] "Geometry optimization improves fidelity" → "Geometry optimization can improve fidelity when effects are detectable"
- [x] Added regime qualifiers throughout
- [x] Explicit acknowledgment of current detection limits

### Simulation Clarifications
- [x] **NEW:** Didactic scaling definition box
- [x] Physical (unscaled) prediction clearly stated
- [x] Scaled demonstration clearly labeled as methodology validation

---

## Cross-Paper Changes

### Symbol Table (Added to All Papers)

| Symbol | Definition | Units |
|--------|------------|-------|
| Ξ(r) | Segment density | dimensionless |
| D_SSZ(r) | Time dilation factor | dimensionless |
| ΔD | Differential time dilation | dimensionless |
| ω | Angular frequency (2πf) | rad/s |
| t | Integration time | s |
| Δh | Height difference | m |
| ΔΦ | Phase drift | rad |
| r_s | Schwarzschild radius | m |
| R | Earth radius | m |
| φ | Golden ratio | dimensionless |

### Canonical Constants (Unified Across All Papers)

| Constant | Value | Unit |
|----------|-------|------|
| c | 299,792,458 | m/s |
| G | 6.67430×10⁻¹¹ | m³/(kg·s²) |
| φ | 1.6180339887 | - |
| M_Earth | 5.972×10²⁴ | kg |
| R_Earth | 6.371×10⁶ | m |
| r_s (Earth) | 8.870×10⁻³ | m |

### Formulas (Verified in All Papers)

| Formula | Expression | Verification |
|---------|------------|--------------|
| Segment density | Ξ = r_s/(2r) | Unit check ✓ |
| Time dilation | D = 1/(1+Ξ) | Unit check ✓ |
| Differential | ΔD = r_s×Δh/R² | Unit check ✓ |
| Phase drift | ΔΦ = ω×ΔD×t | Unit check ✓ |
| Coherent zone | z = 4εR²/r_s | Unit check ✓ |

### References (Added to All Papers)

```
Repository: https://github.com/error-wtf/ssz-qubits
Tests: 150/150 passing (100%)
Command: python -m pytest tests/ -v
```

---

## Removed Claims (All Papers)

| Removed Claim | Reason | Replacement |
|---------------|--------|-------------|
| "Detectable at mm-scale" | ~12 OoM below noise | "Upper bound at mm-scale" |
| "0.1% fidelity improvement" | Unscaled value undetectable | "Didactically scaled demonstration" |
| "50% threshold falsifies SSZ" | Binary threshold inappropriate | "Slope-fitting with CI" |
| "Explains unexplained drifts" | No citation | Removed |
| "SSZ superior to GR" | Misleading | "SSZ operational layer" |

---

## Quality Assurance

### Pre-Publication Checklist (All Papers)

- [x] Symbol table present
- [x] All formulas have unit checks
- [x] Numerical values verified against Python calculations
- [x] Feasibility caveats present where needed
- [x] Repo reference included
- [x] No overclaims about detectability
- [x] SSZ vs GR framing neutral
- [x] Statistical framework uses CI (not binary)

### Numerical Verification

```
python paper_suite_integrator.py
# All verifications PASS
```

---

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2025-12-21 | 1.0 | Initial consistency pass |
| 2025-12-21 | 1.1 | Numerical verification complete |
| 2025-12-21 | 2.0 | All papers revised, master D complete |

---

© 2025 Carmen Wrede & Lino Casu  
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
