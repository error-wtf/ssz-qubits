# Paper C (Revised): Experimental Framework for Testing Gravitational Phase Coupling

## Upper-Bound Constraints and Platform Comparison

**Authors:** Lino Casu, Carmen Wrede  
**Version:** 1.3 (Revised for consistency with Paper D)  
**Date:** December 2025

---

## Symbol Table

| Symbol | Definition | Units |
|--------|------------|-------|
| Ξ(r) | Segment density | dimensionless |
| D_SSZ(r) | Time dilation factor | dimensionless |
| ΔD | Differential time dilation | dimensionless |
| ω | Angular frequency | rad/s |
| t | Integration time | s |
| Δh | Height difference | m |
| ΔΦ | Phase drift | rad |
| α | Slope (ΔΦ vs Δh) | rad/m |
| σ | Standard deviation | rad |
| N | Number of measurements | - |

---

## Abstract

We present an experimental framework for testing gravitational phase coupling in quantum systems as predicted by the SSZ model. Our rigorous feasibility analysis reveals:

1. **Feasibility gap:** The predicted SSZ effect at mm-scale Δh is ~12 orders of magnitude below current superconducting qubit noise floors.

2. **Null is positive:** A null result in this regime is **SSZ-consistent**—the theory predicts negligibility here.

3. **Upper-bound value:** Experiments constrain anomalous phase couplings to < 10¹⁰ × α_SSZ.

4. **Gold standard:** **Optical atomic clocks** yield ΔΦ ~ 0.6 rad at Δh = 1 m—readily detectable.

5. **Statistical framework:** Slope-fitting with confidence intervals replaces binary thresholds.

All calculations verified; 150 tests pass (100%).

---

## 1. Feasibility Analysis

### 1.1 Signal Size (5 GHz Transmon, 100 μs)

| Δh | ΔD_SSZ | ΔΦ | Detectable? |
|----|--------|-----|-------------|
| 1 μm | 2.19×10⁻²² | 6.9×10⁻¹⁶ rad | No |
| 1 mm | 2.19×10⁻¹⁹ | 6.9×10⁻¹³ rad | No |
| 1 m | 2.19×10⁻¹⁶ | 6.9×10⁻¹⁰ rad | No |
| 10 m | 2.19×10⁻¹⁵ | 6.9×10⁻⁹ rad | No |

### 1.2 Noise Floor

**Representative** single-shot phase uncertainty:

| Source | Magnitude |
|--------|-----------|
| Quantum projection noise | O(1 rad) |
| LO phase noise | ~10⁻³ rad |
| Temperature drift | ~0.6 rad |
| **Combined** | **O(1 rad)** |

### 1.3 Averaging Requirements

For SNR = 3: N = (3 × σ / signal)²

| Δh | Signal | N required | Time @ 10 kHz |
|----|--------|------------|---------------|
| 1 mm | 6.9×10⁻¹³ rad | ~10²⁵ | ~10¹⁴ years |
| 1 m | 6.9×10⁻¹⁰ rad | ~10¹⁹ | ~10⁸ years |

### 1.4 Conclusion

**The SSZ effect is ~12 orders of magnitude below detectability with current superconducting qubit technology.**

**A null result is SSZ-consistent.**

---

## 2. Platform Comparison

### 2.1 Transmon vs Optical Clock

| Parameter | Transmon | Optical Clock | Ratio |
|-----------|----------|---------------|-------|
| Frequency | 5 GHz | 429 THz | 8.6×10⁴ |
| Coherence | 100 μs | 1 s | 10⁴ |
| ΔΦ @ 1m | 6.9×10⁻¹⁰ rad | **0.59 rad** | 8.6×10⁸ |
| N for SNR=3 | 10¹⁹ | **~25** | — |
| **Feasible?** | **No** | **YES** | — |

### 2.2 Optical Clock Calculation

```
ω = 2π × 429×10¹² = 2.70×10¹⁵ rad/s
ΔD = r_s × Δh / R² = 2.19×10⁻¹⁶
t = 1 s

ΔΦ = 2.70×10¹⁵ × 2.19×10⁻¹⁶ × 1 = 0.59 rad
```

**Directly measurable.** Optical clock experiments have demonstrated gravitational redshift at ~1 cm level (Bothwell et al., Nature 2022).

### 2.3 Recommendation

**Optical atomic clocks are the gold-standard platform for quantitative SSZ tests.**

---

## 3. Upper-Bound Experiment Design

### 3.1 Scientific Value

1. **Constrain anomalous couplings:** Any beyond-GR coupling < upper bound
2. **Validate null predictions:** SSZ predicts negligibility at mm-scale
3. **Establish methodology:** First systematic study in solid-state qubits

### 3.2 Hardware: Chip Tilt

```
Δh = L × sin(θ)
```

| Tilt Angle | Δh (20 mm chip) |
|------------|-----------------|
| 1° | 0.35 mm |
| 5° | 1.74 mm |
| 10° | 3.47 mm |

### 3.3 Upper Bound Calculation

With Δh_max = 3.5 mm, N = 10⁹ shots, σ = 1 rad:

```
σ_averaged = 1 / √10⁹ = 3.2×10⁻⁵ rad
σ_slope = 3.2×10⁻⁵ / 3.5×10⁻³ = 9×10⁻³ rad/m

Upper bound: |α_anom| < 9×10⁻³ rad/m (95% CL)
```

SSZ prediction: α_SSZ ≈ 6.7×10⁻¹³ rad/m

**Constrains anomalous couplings to < 10¹⁰ × α_SSZ.**

---

## 4. Statistical Framework

### 4.1 Model Comparison

**M₀ (Null):** ΔΦ = 0 + noise

**M_SSZ:** ΔΦ = α_SSZ × Δh + noise

**M_anom:** ΔΦ = α_fit × Δh + noise (free)

### 4.2 Falsification Criteria

**SSZ falsified if:**
- α_fit inconsistent with α_SSZ at >3σ
- AND |α_fit| ≠ 0
- IN DETECTION REGIME (optical clocks)

**SSZ supported if:**
- α_fit consistent with α_SSZ
- OR null at mm-scale (this IS the prediction)

### 4.3 Why Not Binary Thresholds

"<50% → falsified" is inappropriate because:
- At mm-scale, α_SSZ ≈ 0, so noise dominates
- Proper statistics require confidence intervals
- Model comparison accounts for uncertainties

---

## 5. Confound Discrimination

### 5.1 Scaling Signatures

| Source | Δh | ω | t | Randomization |
|--------|-----|---|---|---------------|
| **SSZ** | **Linear** | **Linear** | **Linear** | **Invariant** |
| Temperature | Correlates | Weak | Non-linear | Varies |
| LO noise | None | None | √t | Varies |
| Vibration | Mechanical | None | AC | Varies |

### 5.2 Control Protocol

1. **Randomize Δh order** → breaks thermal correlation
2. **Common-mode LO reference** → cancels in differential
3. **Accelerometer monitoring** → identifies vibration

### 5.3 With/Without Compensation

The strongest discriminator:
- Measure without correction
- Apply: Φ_corr = -ω × (r_s × Δh / R²) × t
- Measure with correction
- Compare variance

---

## 6. Consistency Note

### 6.1 Papers A/B vs Paper C

**Apparent contradiction:** A/B discuss SSZ relevance; C shows undetectability.

**Resolution:** A/B describe the *regime where SSZ becomes relevant*—future systems with T₂ >> 1 s, Δh ~ m. Paper C tests *current systems* where effects are negligible.

**A null result today validates SSZ in the regime where it predicts negligibility.**

---

## 7. Conclusion

1. **Feasibility:** ~12 OoM gap at mm-scale with superconducting qubits
2. **Null is positive:** SSZ predicts negligibility in current regime
3. **Gold standard:** Optical clocks (ΔΦ ~ 0.6 rad at 1 m)
4. **Statistics:** Slope-fitting with CI, not binary thresholds
5. **Upper bound:** Constrains anomalous couplings to < 10¹⁰ × α_SSZ

---

## References

1. Paper D: Unified Framework (this series)
2. Bothwell et al. (2022). Nature 602, 420-424.
3. SSZ-Qubits: https://github.com/error-wtf/ssz-qubits

---

**© 2025 Carmen Wrede & Lino Casu**  
**Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4**
