# Paper C v1.1: Experimental Framework for Testing Gravitational Phase Coupling in Quantum Systems

## A Protocol for Upper-Bound Constraints and Platform Comparison

**Authors:** Lino Casu, Carmen Wrede  
**Affiliation:** Independent Researchers  
**Contact:** mail@error.wtf  
**Date:** December 2025  
**Version:** 1.1 (Revised with Feasibility Analysis)

---

## Abstract

We present an experimental framework for testing gravitational phase coupling in quantum systems, as predicted by the Segmented Spacetime (SSZ) model. Building on Papers A and B, we perform a rigorous **order-of-magnitude feasibility analysis** revealing that the predicted SSZ effect at laboratory-scale height differences (Δh ~ mm) is **~12 orders of magnitude below** the noise floor of current superconducting qubit technology. We therefore reframe this work as: (1) an **upper-bound experiment** that can constrain anomalous phase couplings in solid-state qubits, (2) a **platform comparison** identifying optical clocks as the appropriate gold-standard test system, and (3) a **statistical falsification framework** using slope-fitting rather than binary thresholds. We provide concrete hardware implementations for height-difference generation (chip tilt, remote entanglement, 3D chiplet stacks) and a confound discrimination strategy based on scaling signatures rather than absolute exclusions.

**Keywords:** Gravitational Phase Coupling, Quantum Systems, Upper Bound, Feasibility Analysis, Optical Clocks, Falsifiability

---

## 1. Introduction

### 1.1 Context from Papers A and B

In Papers A and B, we derived the SSZ prediction for gravitational phase drift:

```
ΔΦ(t) = ω × ΔD_SSZ(Δh) × t
```

where ΔD_SSZ(Δh) ≈ r_s × Δh / R² for small height differences. We showed this effect is **deterministic, geometry-linked, and in principle compensable**.

### 1.2 The Critical Question

**Can this effect be detected with current technology?**

This paper provides the honest answer: **No, not at laboratory scales with superconducting qubits.** However, this negative result is scientifically valuable when framed correctly.

### 1.3 Revised Goals

1. **Quantify the feasibility gap** between predicted signal and noise floor
2. **Identify appropriate experimental platforms** where detection is possible
3. **Design an upper-bound experiment** that provides value regardless of outcome
4. **Establish a statistical framework** for falsification claims

---

## 2. Feasibility Analysis

### 2.1 Signal Size

For a 5 GHz qubit with Ramsey time T = 100 μs:

| Δh | ΔD_SSZ | ΔΦ (100 μs) |
|----|--------|-------------|
| 1 μm | 1.09×10⁻²² | 3.43×10⁻¹⁶ rad |
| 1 mm | 1.09×10⁻¹⁹ | 3.43×10⁻¹³ rad |
| 1 m | 1.09×10⁻¹⁶ | 3.43×10⁻¹⁰ rad |
| 10 m | 1.09×10⁻¹⁵ | 3.43×10⁻⁹ rad |

### 2.2 Noise Floor

State-of-the-art superconducting qubit phase measurement:

| Source | Magnitude (single shot) |
|--------|------------------------|
| Quantum projection noise | ~1 rad |
| LO phase noise (100 μs) | ~10⁻³ rad |
| Temperature drift (1 mK) | ~0.6 rad |
| **Combined** | **~1 rad** |

### 2.3 Averaging Requirements

For SNR = 3, the required number of shots scales as:

```
N = (SNR × σ_noise / signal)²
```

| Δh | Signal | N required | Time @ 10 kHz | Feasible? |
|----|--------|------------|---------------|-----------|
| 1 mm | 3.4×10⁻¹³ rad | 7.6×10²⁵ | 2.4×10¹⁴ years | **No** |
| 1 m | 3.4×10⁻¹⁰ rad | 7.6×10¹⁹ | 2.4×10⁸ years | **No** |
| 10 m | 3.4×10⁻⁹ rad | 7.6×10¹⁷ | 2.4×10⁶ years | **No** |

### 2.4 Conclusion

**The SSZ effect at GR-predicted levels is ~12 orders of magnitude below detectability with current superconducting qubit technology.**

This is not a failure of the theory—it is the expected regime where gravitational effects are negligible for solid-state systems on Earth.

---

## 3. Alternative Platforms

### 3.1 Optical Atomic Clocks

Optical clocks operate at ~10¹⁵ Hz with coherence times of seconds:

| Parameter | Transmon Qubit | Optical Clock |
|-----------|---------------|---------------|
| Frequency | 5 GHz | 429 THz |
| Coherence | 100 μs | 1 s |
| ΔΦ @ Δh=1m | 3.4×10⁻¹⁰ rad | **1.3×10⁻⁶ rad** |
| N for SNR=3 | 7.6×10¹⁹ | **~10⁹** |
| Feasible? | No | **Yes** |

**Optical clock experiments have already demonstrated gravitational redshift at the ~1 cm level** (Bothwell et al., Nature 2022). This is the appropriate platform for testing gravitational phase coupling.

### 3.2 Trapped Ion Systems

Trapped ions offer intermediate parameters:
- Frequencies: ~10 GHz (hyperfine) to ~10¹⁵ Hz (optical)
- Coherence: seconds to minutes
- Feasibility: Marginal for meter-scale Δh

### 3.3 Recommendation

**For testing SSZ predictions quantitatively, optical atomic clocks are the gold-standard platform.** Superconducting qubits can provide **upper bounds** on anomalous couplings but cannot detect GR-level effects.

---

## 4. Upper-Bound Experiment Design

### 4.1 Scientific Value

An upper-bound experiment provides value by:

1. **Constraining anomalous couplings**: If any beyond-GR phase coupling exists, it must be smaller than our upper bound
2. **Validating null predictions**: SSZ predicts negligible effect at mm-scale—confirming this is a positive result
3. **Establishing methodology**: First systematic study of gravitational phase coupling in solid-state qubits

### 4.2 Hardware Configurations for Δh Generation

**Configuration A: Chip Tilt**

| Tilt Angle | Δh across 20 mm chip |
|------------|---------------------|
| 1° | 0.35 mm |
| 5° | 1.74 mm |
| 10° | 3.47 mm |

*Implementation:* Precision goniometer stage under dilution refrigerator sample mount. Requires careful thermal management.

**Configuration B: Remote Entanglement**

Two qubits in separate dilution refrigerators at different heights, connected via microwave link or fiber-optical transduction.

| Floor separation | Δh | Technical challenge |
|-----------------|-----|---------------------|
| Same floor | 0 | Baseline reference |
| Adjacent floors | 3 m | Moderate |
| Tower experiment | 10-100 m | Significant |

*Implementation:* Requires high-fidelity remote entanglement (demonstrated by multiple groups).

**Configuration C: 3D Chiplet Stack**

Vertically stacked quantum processors with through-silicon vias.

| Stack height | Δh |
|--------------|-----|
| 2-chip stack | 0.5-1 mm |
| Multi-chip stack | 2-5 mm |

*Implementation:* Emerging technology; IBM and Google pursuing 3D integration.

### 4.3 Protocol

```
1. BASELINE PHASE (Δh = 0)
   - Both qubits at same height
   - Characterize intrinsic phase drift: Φ_0(t) ± σ_0
   - Record all environmental parameters

2. Δh SWEEP
   For each configuration (A, B, or C):
     For each Δh in randomized order:
       a. Set height difference
       b. Wait for thermal equilibration (>30 min)
       c. Interleaved measurement:
          - Reference qubits (same height): Φ_ref
          - Test qubits (different heights): Φ_test
       d. Record: ΔΦ = Φ_test - Φ_ref
       e. Repeat N times (N ~ 10⁹)

3. ANALYSIS
   - Fit: ΔΦ vs Δh (expect slope = ω × r_s / R² × t)
   - Extract: slope ± uncertainty
   - Compare to: null hypothesis (slope = 0)
                 SSZ hypothesis (slope = predicted)
```

---

## 5. Statistical Falsification Framework

### 5.1 Replacing Binary Thresholds

The v1.0 falsification thresholds ("<50% → falsified") are replaced with a proper statistical framework.

### 5.2 Model Comparison

Define three models:

**M₀ (Null):** ΔΦ = 0 + noise

**M_SSZ (SSZ prediction):** ΔΦ = α_SSZ × Δh + noise, where α_SSZ = ω × r_s × t / R²

**M_anom (Anomalous):** ΔΦ = α_fit × Δh + noise, where α_fit is a free parameter

### 5.3 Falsification Criteria

1. **SSZ falsified if:**
   - Measured slope α_fit is inconsistent with α_SSZ at >3σ
   - AND |α_fit| significantly different from zero

2. **SSZ supported if:**
   - Measured slope consistent with α_SSZ within uncertainty
   - OR null result consistent with α_SSZ ≈ 0 (at mm-scale, this is the prediction!)

3. **Anomaly detected if:**
   - |α_fit| >> |α_SSZ| (stronger than GR prediction)
   - This would indicate new physics beyond SSZ

### 5.4 Upper Bound Statement

If no signal is detected:

```
|α_anomalous| < σ_slope / Δh_max (95% CL)
```

This constrains any gravitational phase coupling to be smaller than the measurement uncertainty.

---

## 6. Confound Discrimination (Revised)

### 6.1 Principle: Signatures, Not Exclusions

Instead of claiming confounds "cannot" produce certain effects, we identify **distinct scaling signatures**:

| Source | Δh scaling | ω scaling | t scaling | Randomization |
|--------|-----------|-----------|-----------|---------------|
| **SSZ** | Linear | Linear | Linear | Invariant |
| Temperature | Monotonic but non-linear | Weak | Non-linear | Varies |
| LO noise | None (common mode) | None | √t | Varies |
| Vibration | Correlated with mechanics | None | AC spectrum | Varies |
| EM crosstalk | Position-dependent | Weak | None | Varies |

### 6.2 Control Measurements

**Temperature control:**
- Interleave Δh values randomly
- Monitor temperature continuously
- Compare: same Δh, different thermal history
- **Signature:** SSZ effect is reproducible; temperature effect varies

**LO noise control:**
- Reference qubit at same height
- Common-mode subtraction
- **Signature:** SSZ effect is differential; LO noise is common-mode

**Vibration control:**
- Accelerometer monitoring
- Correlate with phase variance
- **Signature:** SSZ is DC; vibration is AC

### 6.3 The Differential Test

The strongest discriminator remains **compensation**:

1. Measure ΔΦ without SSZ correction
2. Apply predicted SSZ correction: Φ_corr = -ω × ΔD_SSZ(Δh) × t
3. Measure ΔΦ with correction

**Interpretation:**
- If correction reduces variance: supports geometry-linked coupling
- If correction has no effect: no detectable coupling
- If correction increases variance: model is wrong

---

## 7. Consistency with Papers A and B

### 7.1 Apparent Contradiction

Papers A/B suggest SSZ effects are relevant for quantum computing. Paper C shows they are undetectable. How to reconcile?

### 7.2 Resolution

**Papers A/B:** Describe the *regime where SSZ becomes relevant*—as QEC improves and coherence times extend, the cumulative effect grows. The papers identify **when** SSZ corrections would be needed (future systems).

**Paper C:** Tests *current systems* where SSZ effects are negligible. This is not a contradiction—it is the expected result in the present regime.

### 7.3 The Scaling Argument

The key insight from Papers A/B is that relevance scales with:
- Coherence time (T₂)
- Qubit frequency (ω)
- Accumulated gate count (N_gates)
- Height difference (Δh)

For current systems: T₂ ~ 100 μs, Δh ~ mm → negligible
For future systems: T₂ ~ 1 s, Δh ~ m → potentially relevant

Paper C tests the present regime and provides the methodology for future tests.

---

## 8. Discussion

### 8.1 What This Paper Achieves

1. **Honest feasibility assessment**: First rigorous order-of-magnitude analysis
2. **Platform guidance**: Identifies optical clocks as appropriate test system
3. **Methodological foundation**: Statistical framework for future experiments
4. **Upper-bound value**: Even null results constrain anomalous couplings

### 8.2 What This Paper Does Not Claim

1. ~~SSZ is detectable with current superconducting qubits at mm-scale~~
2. ~~10⁶ averages are sufficient~~
3. ~~Piezo stage between two qubits on same chip~~

### 8.3 Path Forward

**Near-term (2025-2027):**
- Upper-bound experiments with tilted chips
- Remote entanglement at ~1 m separation
- Optical clock collaborations

**Medium-term (2027-2030):**
- Tower experiments at 10-100 m separation
- 3D chiplet stacks with significant Δh
- Dedicated optical clock tests

---

## 9. Conclusion

We have presented a revised experimental framework for testing gravitational phase coupling in quantum systems:

1. **Feasibility:** The predicted SSZ effect is ~12 orders of magnitude below current superconducting qubit sensitivity at mm-scale Δh

2. **Reframing:** This paper provides an **upper-bound protocol** rather than a detection experiment

3. **Platform:** **Optical atomic clocks** are identified as the appropriate gold-standard platform for quantitative tests

4. **Statistics:** Falsification is based on **slope-fitting and model comparison**, not binary thresholds

5. **Value:** Even null results constrain anomalous phase couplings and validate the expected negligibility in the current regime

The SSZ framework makes testable predictions. This paper honestly assesses *where* those tests are feasible and *how* they should be conducted.

---

## Acknowledgments

We thank the reviewers for critical feedback that substantially improved this manuscript.

---

## References

1. Casu, L. & Wrede, C. (2025). Paper A: Geometric Qubit Optimization via Segmented Spacetime.
2. Casu, L. & Wrede, C. (2025). Paper B: Phase Coherence and Entanglement Preservation.
3. Bothwell, T. et al. (2022). Resolving the gravitational redshift across a millimetre-scale atomic sample. Nature 602, 420–424.
4. SSZ-Qubits Repository: https://github.com/error-wtf/ssz-qubits

---

## Appendix: Feasibility Calculations

All calculations are reproducible via:

```bash
python paper_c_feasibility_analysis.py
```

Key results:

| Parameter | Value |
|-----------|-------|
| r_s (Earth) | 8.87×10⁻³ m |
| R_Earth | 6.371×10⁶ m |
| ω (5 GHz) | 3.14×10¹⁰ rad/s |
| ΔD_SSZ / Δh | 1.09×10⁻¹⁶ m⁻¹ |
| Single-shot noise | ~1 rad |
| N for SNR=3 @ 1mm | 7.6×10²⁵ |

---

**© 2025 Carmen Wrede & Lino Casu**  
**Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4**
