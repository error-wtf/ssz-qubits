# SSZ Paper Suite: Consistency Report

**Version:** 1.0  
**Date:** 2025-12-21  
**Authors:** Carmen Wrede & Lino Casu

---

## Executive Summary

This report documents all identified inconsistencies across Papers A, B, C, and D, along with resolutions applied to create a publication-ready, internally consistent paper suite.

**Key Finding:** Core mathematical formulas are CONSISTENT across all papers. Primary issues relate to:
1. Feasibility claim alignment (A/B vs C/D)
2. Didactic scaling definition clarity
3. Platform recommendation consistency

---

## 1. Verified Constants (Canonical Values)

All papers MUST use these exact values:

| Constant | Symbol | Value | Unit |
|----------|--------|-------|------|
| Speed of light | c | 299,792,458 | m/s |
| Gravitational constant | G | 6.67430×10⁻¹¹ | m³/(kg·s²) |
| Golden ratio | φ | 1.6180339887 | - |
| Earth mass | M_Earth | 5.972×10²⁴ | kg |
| Earth radius | R | 6.371×10⁶ | m |
| **Earth Schwarzschild radius** | **r_s** | **8.870×10⁻³** | **m** |

---

## 2. Verified Formulas (Canonical Forms)

### 2.1 Segment Density (Weak Field)
```
Ξ(r) = r_s / (2r)
```
- **Unit check:** [m]/[m] = dimensionless ✓
- **At Earth surface:** Ξ = 6.96×10⁻¹⁰

### 2.2 Time Dilation Factor
```
D_SSZ(r) = 1 / (1 + Ξ(r))
```
- **Unit check:** dimensionless ✓
- **At Earth surface:** D_SSZ = 0.999999999304

### 2.3 Differential Time Dilation (linearized)
```
ΔD_SSZ = r_s × Δh / R²
```
- **Unit check:** [m]×[m]/[m²] = dimensionless ✓
- **At Δh = 1 mm:** ΔD = 2.19×10⁻¹⁹
- **At Δh = 1 m:** ΔD = 2.19×10⁻¹⁶

### 2.4 Phase Drift
```
ΔΦ = ω × ΔD_SSZ × t
```
- **Unit check:** [rad/s]×[1]×[s] = [rad] ✓

### 2.5 Coherent Zone Width
```
z(ε) = 4ε × R² / r_s
```
- **Unit check:** [1]×[m²]/[m] = [m] ✓

---

## 3. Conflict Matrix

| Item | Paper A | Paper B | Paper C | Paper D | Status | Resolution |
|------|---------|---------|---------|---------|--------|------------|
| Ξ formula | r_s/(2r) | r_s/(2r) | r_s/(2r) | r_s/(2r) | ✓ CONSISTENT | - |
| D_SSZ formula | 1/(1+Ξ) | 1/(1+Ξ) | 1/(1+Ξ) | 1/(1+Ξ) | ✓ CONSISTENT | - |
| ΔΦ formula | ω×ΔD×t | ω×ΔD×t | ω×ΔD×t | ω×ΔD×t | ✓ CONSISTENT | - |
| z(ε) formula | 4εR²/r_s | 4εR²/r_s | 4εR²/r_s | 4εR²/r_s | ✓ CONSISTENT | - |
| Feasibility claim | Implies relevance | Implies relevance | ~12 OoM gap | ~12 OoM gap | ⚠️ ALIGNED | Add caveat to A/B |
| Detection claim | Unclear | Unclear | Upper bound | Upper bound | ⚠️ ALIGNED | Clarify in A/B |
| Optical clock | Not mentioned | Not mentioned | Gold standard | Gold standard | ⚠️ ADDED | Add to A/B |
| SSZ vs GR | Operational | Operational | Consistent | Consistent | ✓ CONSISTENT | - |
| Statistical framework | None | None | Slope-fitting | Slope-fitting | ✓ OK | Stats in C/D |
| Repo reference | Missing | Missing | Present | Present | ⚠️ ADDED | Add to A/B |

---

## 4. Top 10 Resolved Inconsistencies

### 4.1 Feasibility Gap Acknowledgment
**Issue:** Papers A/B discuss SSZ applications without explicit feasibility bounds.  
**Resolution:** Added to A/B revised versions:
> "Note: At mm-scale height differences with current superconducting qubits (T₂ ~ 100 μs), the predicted SSZ effect is approximately 12 orders of magnitude below the noise floor. These concepts become practically relevant for future systems with extended coherence times (T₂ >> 1 s) or larger height differences (Δh ~ meters), or with optical atomic clocks."

### 4.2 Detection vs Upper Bound Framing
**Issue:** A/B could imply direct detection is possible today.  
**Resolution:** Clarified that current experiments provide **upper bounds**, not detection. Direct detection requires optical clock regime.

### 4.3 Optical Clock as Gold Standard
**Issue:** A/B did not mention optical clocks.  
**Resolution:** Added section referencing optical clocks as the appropriate platform for quantitative SSZ tests (ΔΦ ~ 0.3-0.6 rad at Δh = 1 m).

### 4.4 Didactic Scaling Definition
**Issue:** Simulation results in A/B could be misinterpreted as physical predictions.  
**Resolution:** Added explicit disclaimer:
> "Simulation results are didactically scaled by factor S to demonstrate methodology. Physical prediction (unscaled) is ΔΦ = [value], which is below current detectability."

### 4.5 Coherent Zone Table Values
**Issue:** Different papers cited different zone widths without showing calculation.  
**Resolution:** Unified table with formula verification:

| Tolerance ε | z(ε) Calculated | z(ε) Displayed |
|-------------|-----------------|----------------|
| 10⁻¹⁸ | 18.3 mm | 18 mm |
| 10⁻¹⁵ | 18.3 m | 18 m |
| 10⁻¹² | 18.3 km | 18 km |

### 4.6 Numerical Precision
**Issue:** Some papers rounded r_s to 8.87 mm, others used more precision.  
**Resolution:** Standardized to r_s = 8.870×10⁻³ m (4 significant figures sufficient for all calculations).

### 4.7 SSZ vs GR Language
**Issue:** Potential for "GR is wrong" interpretation.  
**Resolution:** Explicit statement in all papers:
> "In the weak-field regime (r >> r_s), SSZ reproduces General Relativity predictions. The distinction between SSZ segmentation and GR continuity becomes observable only in strong-field or high-precision regimes."

### 4.8 Compensation Protocol Consistency
**Issue:** Different descriptions of compensation in A/B vs C/D.  
**Resolution:** Unified description of "with/without compensation" as the central experimental discriminator across all papers.

### 4.9 Test Suite Reference
**Issue:** A/B did not reference reproducibility package.  
**Resolution:** Added to all papers:
> "All predictions are reproducible via the ssz-qubits repository (https://github.com/error-wtf/ssz-qubits). 150 unit tests verify numerical consistency."

### 4.10 Claim Taxonomy
**Issue:** No unified framework for what SSZ claims vs. doesn't claim.  
**Resolution:** Added to Paper D (and referenced in A/B/C):

| Regime | Claim | Testable Today? |
|--------|-------|-----------------|
| **Bounded** | mm-scale transmons provide upper bounds | Yes (null expected) |
| **Detectable** | Optical clocks at m-scale show signal | Yes (~0.3-0.6 rad) |
| **Future** | Large-scale QC networks need compensation | Engineering relevance |

---

## 5. Numerical Verification Summary

### 5.1 Phase Drift Calculations (Verified)

| Platform | f | Δh | t | ΔΦ (calculated) | Status |
|----------|---|-----|---|-----------------|--------|
| Transmon | 5 GHz | 1 μm | 100 μs | 6.87×10⁻¹⁶ rad | ✓ |
| Transmon | 5 GHz | 1 mm | 100 μs | 6.87×10⁻¹³ rad | ✓ |
| Transmon | 5 GHz | 1 m | 100 μs | 6.87×10⁻¹⁰ rad | ✓ |
| Optical | 429 THz | 1 m | 1 s | 0.59 rad | ✓ |

### 5.2 Averaging Requirements (Verified)

| Δh | Signal | N for SNR=3 | Time @ 10 kHz |
|----|--------|-------------|---------------|
| 1 mm | 6.87×10⁻¹³ rad | ~10²⁵ | ~10¹⁴ years |
| 1 m | 6.87×10⁻¹⁰ rad | ~10¹⁹ | ~10⁸ years |
| 10 m | 6.87×10⁻⁹ rad | ~10¹⁷ | ~10⁶ years |

**Conclusion:** ~12-13 orders of magnitude gap for transmon qubits. Null result is SSZ-consistent.

---

## 6. Quality Gate Checklist

- [x] No statement contradicts ~12 OoM gap in transmon/mm regime
- [x] Coherent zone definition + table numerically correct in all papers
- [x] Every central equation has defined variables + units
- [x] Didactic scaling explicitly defined and separated from physical detectability
- [x] SSZ vs GR weak-field consistency clearly stated
- [x] Repo reference (150 tests) in all papers
- [x] Optical clock identified as gold standard
- [x] Upper-bound framing for transmon experiments
- [x] Slope-fitting statistical framework (not binary thresholds)

---

## 7. Remaining Open Items

1. **External validation:** Optical clock experiments (Bothwell et al. 2022) confirm GR redshift at cm-scale. SSZ prediction at this scale is identical to GR—need strong-field or network-scale tests for distinction.

2. **Strong-field regime:** Papers focus on weak-field. Strong-field (Ξ = 1 - exp(-φr/r_s)) mentioned but not experimentally testable with current technology.

3. **Simulation reproducibility:** All simulation parameters should be documented (seeds, noise models, circuit depths) if simulations are retained.

---

**Document Status:** COMPLETE  
**All conflicts resolved.**

---

© 2025 Carmen Wrede & Lino Casu  
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
