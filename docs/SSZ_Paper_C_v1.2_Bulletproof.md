# Paper C v1.2: Experimental Framework for Testing Gravitational Phase Coupling in Quantum Systems

## A Protocol for Upper-Bound Constraints and Platform Comparison

**Authors:** Lino Casu, Carmen Wrede  
**Affiliation:** Independent Researchers  
**Contact:** mail@error.wtf  
**Date:** December 2025  
**Version:** 1.2 (Bulletproof Edition)

---

## Abstract

We present an experimental framework for testing gravitational phase coupling in quantum systems, as predicted by the Segmented Spacetime (SSZ) model. Building on Papers A and B, we perform a rigorous **order-of-magnitude feasibility analysis** revealing that the predicted SSZ effect at laboratory-scale height differences (Δh ~ mm) is **~12 orders of magnitude below** the noise floor of current superconducting qubit technology. **Crucially, a null result in this regime is itself SSZ-consistent**: the theory predicts negligible effects at mm-scale with current coherence times. We therefore reframe this work as: (1) an **upper-bound experiment** that can constrain anomalous phase couplings in solid-state qubits, (2) a **platform comparison** identifying optical atomic clocks as the appropriate gold-standard test system (where ΔΦ ~ 0.3 rad at Δh = 1 m is readily detectable), and (3) a **statistical falsification framework** using slope-fitting rather than binary thresholds. We provide concrete hardware implementations for height-difference generation (chip tilt, remote entanglement, 3D chiplet stacks) and a confound discrimination strategy based on scaling signatures.

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

This paper provides the honest answer: **No, not at laboratory scales with superconducting qubits.** However, this negative result is scientifically valuable when framed correctly—and is in fact **consistent with SSZ predictions** in the current regime.

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

**Representative** single-shot phase uncertainty in superconducting qubit measurements:

| Source | Magnitude (single shot) | Notes |
|--------|------------------------|-------|
| Quantum projection noise | O(1 rad) | Fundamental limit |
| LO phase noise (100 μs) | ~10⁻³ rad | Depends on oscillator quality |
| Temperature drift (1 mK) | ~0.6 rad | Qubit frequency shift |
| **Combined** | **O(1 rad)** | Dominated by projection noise |

*Note: These are representative order-of-magnitude estimates. Actual values depend on specific hardware and measurement protocols.*

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

This is not a failure of the theory—it is the expected regime where gravitational effects are negligible for solid-state systems on Earth. **A null result is SSZ-consistent.**

---

## 3. Alternative Platforms

### 3.1 Optical Atomic Clocks

Optical clocks operate at ~10¹⁵ Hz with coherence times of seconds. The key advantage is the **10⁵× higher frequency** combined with **10⁴× longer coherence**:

| Parameter | Transmon Qubit | Optical Clock | Ratio |
|-----------|---------------|---------------|-------|
| Frequency f | 5 GHz | 429 THz | 8.6×10⁴ |
| ω = 2πf | 3.1×10¹⁰ rad/s | 2.7×10¹⁵ rad/s | 8.6×10⁴ |
| Coherence t | 100 μs | 1 s | 10⁴ |
| ΔD_SSZ @ 1m | 1.09×10⁻¹⁶ | 1.09×10⁻¹⁶ | 1 |
| **ΔΦ @ Δh=1m** | **3.4×10⁻¹⁰ rad** | **~0.29 rad** | **8.6×10⁸** |
| N for SNR=3 | 7.6×10¹⁹ | **~100** | — |
| **Feasible?** | **No** | **YES** | — |

**Calculation for optical clocks:**
```
ΔΦ = ω × ΔD_SSZ × t
   = 2.7×10¹⁵ rad/s × 1.09×10⁻¹⁶ × 1 s
   = 0.29 rad
```

This is a **directly measurable** phase shift. **Optical clock experiments have already demonstrated gravitational redshift at the ~1 cm level** (Bothwell et al., Nature 2022).

### 3.2 Trapped Ion Systems

Trapped ions offer intermediate parameters:
- Frequencies: ~10 GHz (hyperfine) to ~10¹⁵ Hz (optical transitions)
- Coherence: seconds to minutes
- Feasibility: Possible for meter-scale Δh with optical transitions

### 3.3 Recommendation

**For testing SSZ predictions quantitatively, optical atomic clocks are the gold-standard platform.** Superconducting qubits can provide **upper bounds** on anomalous couplings but cannot detect GR-level effects in the current regime.

---

## 4. Upper-Bound Experiment Design

### 4.1 Scientific Value

An upper-bound experiment provides value by:

1. **Constraining anomalous couplings**: If any beyond-GR phase coupling exists, it must be smaller than our upper bound
2. **Validating null predictions**: SSZ predicts negligible effect at mm-scale—confirming this is a **positive result**
3. **Establishing methodology**: First systematic study of gravitational phase coupling in solid-state qubits

### 4.2 Hardware Configurations for Δh Generation

**Configuration A: Chip Tilt**

When a chip of length L is tilted by angle θ from horizontal, qubits at opposite ends experience a height difference:

```
Δh = L × sin(θ) ≈ L × θ  (for small θ in radians)
```

| Tilt Angle θ | sin(θ) | Δh across 20 mm chip |
|--------------|--------|---------------------|
| 1° (0.017 rad) | 0.0175 | 0.35 mm |
| 5° (0.087 rad) | 0.0872 | 1.74 mm |
| 10° (0.175 rad) | 0.174 | 3.47 mm |

*Implementation:* Precision goniometer stage under dilution refrigerator sample mount. Requires careful thermal management to maintain uniform temperature across tilted chip.

**Configuration B: Remote Entanglement**

Two qubits in separate dilution refrigerators at different heights, connected via microwave link or fiber-optical transduction.

| Floor separation | Δh | Technical challenge |
|-----------------|-----|---------------------|
| Same floor | 0 | Baseline reference |
| Adjacent floors | 3 m | Moderate |
| Tower experiment | 10-100 m | Significant |

*Implementation:* Requires high-fidelity remote entanglement (demonstrated by multiple groups at km scale).

**Configuration C: 3D Chiplet Stack**

Vertically stacked quantum processors with through-silicon vias.

| Stack configuration | Δh |
|---------------------|-----|
| 2-chip stack | 0.5-1 mm |
| Multi-chip stack | 2-5 mm |

*Implementation:* Emerging technology; IBM and Google pursuing 3D integration.

### 4.3 Protocol

```
1. BASELINE PHASE (Δh = 0)
   - Both qubits at same height (level chip)
   - Characterize intrinsic phase drift: Φ_0(t) ± σ_0
   - Record all environmental parameters

2. Δh SWEEP (randomized order)
   For each tilt angle in randomized order:
     a. Set tilt angle → Δh
     b. Wait for thermal equilibration (>30 min)
     c. Interleaved measurement:
        - Reference qubits (chip center): Φ_ref
        - Test qubits (chip edges): Φ_test
     d. Record: ΔΦ = Φ_test - Φ_ref
     e. Repeat N times (N ~ 10⁹)

3. ANALYSIS
   - Fit: ΔΦ vs Δh
   - Extract: slope α ± σ_α
   - Compare to predictions
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
   - OR null result consistent with α_SSZ ≈ 0 (at mm-scale, **this is the prediction!**)

3. **Anomaly detected if:**
   - |α_fit| >> |α_SSZ| (stronger than GR prediction)
   - This would indicate new physics beyond SSZ

### 5.4 Upper Bound Statement

If no signal is detected, we report an upper bound:

```
|α_anomalous| < σ_α / Δh_max  (95% CL)
```

**Concrete Example:**

With Δh_max = 3.5 mm (10° tilt on 20 mm chip), N = 10⁹ shots, and assuming σ_single ≈ 1 rad:

```
σ_after_averaging = σ_single / √N = 1 / √10⁹ ≈ 3.2×10⁻⁵ rad

σ_α ≈ σ_after_averaging / Δh_max = 3.2×10⁻⁵ / 3.5×10⁻³ ≈ 9×10⁻³ rad/m

Upper bound: |α_anomalous| < 9×10⁻³ rad/m (95% CL)
```

For comparison, the SSZ-predicted slope is:
```
α_SSZ = ω × r_s × t / R² ≈ 3.1×10¹⁰ × 8.87×10⁻³ × 10⁻⁴ / (6.4×10⁶)² 
      ≈ 6.7×10⁻¹³ rad/m
```

**This experiment constrains anomalous couplings to be < 10¹⁰ × α_SSZ**, which is scientifically meaningful as a first systematic bound.

---

## 6. Confound Discrimination (Revised)

### 6.1 Principle: Signatures, Not Exclusions

Instead of claiming confounds "cannot" produce certain effects, we identify **distinct scaling signatures**:

| Source | Δh scaling | ω scaling | t scaling | Randomization response |
|--------|-----------|-----------|-----------|------------------------|
| **SSZ** | Linear | Linear | Linear | Invariant |
| Temperature | May correlate | Weak | Non-linear | Varies with thermal history |
| LO noise | None (common mode) | None | √t | Varies run-to-run |
| Vibration | Correlated with mechanics | None | AC spectrum | Varies with environment |
| EM crosstalk | Position-dependent | Weak | Constant | Varies with EM environment |

### 6.2 Control Measurements

**Temperature control:**
- Interleave Δh values randomly → breaks thermal correlation
- Monitor temperature continuously at multiple points
- Compare: same Δh, different thermal history
- **Key signature:** SSZ effect is reproducible; temperature effect varies with history

**LO noise control:**
- Reference qubit at same height as one test qubit
- Common-mode subtraction removes LO contribution
- **Key signature:** SSZ effect is differential; LO noise is common-mode

**Vibration control:**
- Accelerometer monitoring during all measurements
- Correlate phase variance with vibration power spectrum
- **Key signature:** SSZ is DC (constant at fixed Δh); vibration is AC

### 6.3 The Differential Test

The strongest discriminator remains **compensation**:

1. Measure ΔΦ without SSZ correction
2. Apply predicted SSZ correction: Φ_corr = -ω × ΔD_SSZ(Δh) × t
3. Measure ΔΦ with correction

**Interpretation:**
- If correction reduces variance: supports geometry-linked coupling
- If correction has no effect: no detectable coupling (consistent with SSZ at mm-scale)
- If correction increases variance: model is incorrect

---

## 7. Consistency with Papers A and B

### 7.1 Apparent Contradiction

Papers A/B suggest SSZ effects are relevant for quantum computing. Paper C shows they are undetectable. How to reconcile?

### 7.2 Resolution

**Papers A/B:** Describe the *regime where SSZ becomes relevant*—as QEC improves and coherence times extend, the cumulative effect grows. The papers identify **when** SSZ corrections would be needed (future systems with T₂ >> 1 s, Δh ~ m).

**Paper C:** Tests *current systems* where SSZ effects are negligible. This is not a contradiction—**it is the expected result in the present regime.**

### 7.3 The Scaling Argument

The key insight from Papers A/B is that relevance scales with:
- Coherence time (T₂): current ~100 μs → future ~1 s+
- Accumulated time (N_gates × t_gate): current ~ms → future ~s
- Height difference (Δh): current ~mm → future ~m (distributed systems)

For current systems: T₂ ~ 100 μs, Δh ~ mm → **negligible** (and SSZ predicts this)
For future systems: T₂ ~ 1 s, Δh ~ m → **potentially relevant**

**A null result today validates SSZ in the regime where it predicts negligibility.**

---

## 8. Discussion

### 8.1 What This Paper Achieves

1. **Honest feasibility assessment**: First rigorous order-of-magnitude analysis for qubit systems
2. **Platform guidance**: Identifies optical clocks as the appropriate gold-standard (ΔΦ ~ 0.3 rad at 1 m)
3. **Methodological foundation**: Statistical framework for future experiments
4. **Upper-bound value**: Even null results constrain anomalous couplings to < 10¹⁰ × α_SSZ

### 8.2 What This Paper Does Not Claim

1. ~~SSZ is detectable with current superconducting qubits at mm-scale~~
2. ~~10⁶ averages are sufficient~~
3. ~~Piezo stage creates Δh between two qubits on same chip~~
4. ~~Null result falsifies SSZ~~ (it is consistent with SSZ predictions)

### 8.3 Path Forward

**Near-term (2025-2027):**
- Upper-bound experiments with tilted chips (this paper)
- Collaboration with optical clock groups for gold-standard tests
- Remote entanglement at ~1 m separation

**Medium-term (2027-2030):**
- Tower experiments at 10-100 m separation
- 3D chiplet stacks with significant Δh
- Dedicated optical clock tests at multiple heights

---

## 9. Conclusion

We have presented a revised experimental framework for testing gravitational phase coupling in quantum systems:

1. **Feasibility:** The predicted SSZ effect is ~12 orders of magnitude below current superconducting qubit sensitivity at mm-scale Δh

2. **Null is positive:** A null result in the current regime is **consistent with SSZ predictions**—the theory predicts negligibility here

3. **Platform:** **Optical atomic clocks** are the gold-standard platform, with ΔΦ ~ 0.3 rad at Δh = 1 m (readily detectable)

4. **Statistics:** Falsification uses **slope-fitting and model comparison**, reporting upper bounds with explicit confidence levels

5. **Value:** This paper provides the first systematic constraint on gravitational phase coupling in solid-state qubits

The SSZ framework makes testable predictions. This paper honestly assesses *where* those tests are feasible, *how* they should be conducted, and *what* a null result means.

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

## Appendix: Key Calculations

**SSZ phase drift:**
```
ΔΦ = ω × ΔD_SSZ(Δh) × t
ΔD_SSZ(Δh) ≈ r_s × Δh / R²
```

**For 5 GHz qubit, Δh = 1 mm, t = 100 μs:**
```
ΔΦ = 3.1×10¹⁰ × (8.87×10⁻³ × 10⁻³ / (6.4×10⁶)²) × 10⁻⁴
   = 3.1×10¹⁰ × 2.2×10⁻¹⁹ × 10⁻⁴
   = 6.8×10⁻¹³ rad
```

**For optical clock (429 THz), Δh = 1 m, t = 1 s:**
```
ΔΦ = 2.7×10¹⁵ × (8.87×10⁻³ × 1 / (6.4×10⁶)²) × 1
   = 2.7×10¹⁵ × 2.2×10⁻¹⁶
   = 0.59 rad  (O(0.1-1 rad) — easily detectable)
```

---

**© 2025 Carmen Wrede & Lino Casu**  
**Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4**
