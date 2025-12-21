# 4. Experimental Designs and Feasibility

## 4.1 Signal Sizes and Noise Floor

The predicted SSZ drift at mm-scale heights is extremely small. The key question is: **when does signal exceed noise?**

### Signal-to-Noise Ratio

```
SNR = ΔΦ_SSZ / σ_noise
```

Detection requires SNR >> 1 (typically > 10 for confident detection).

### Platform Comparison

| Platform | ω/(2π) | Δh | t | ΔΦ_SSZ | Noise | SNR | Regime |
|----------|--------|-----|---|--------|-------|-----|--------|
| Transmon | 5 GHz | 1 mm | 100 μs | 6.9×10⁻¹³ | 1 rad | 10⁻¹² | Bounded |
| Transmon | 5 GHz | 10 mm | 100 μs | 6.9×10⁻¹² | 1 rad | 10⁻¹¹ | Bounded |
| Trapped ion | 10 MHz | 1 mm | 1 ms | 8.8×10⁻¹² | 0.1 rad | 10⁻¹⁰ | Bounded |
| NV center | 2.87 GHz | 1 mm | 1 ms | 4×10⁻¹² | 0.01 rad | 10⁻⁹ | Bounded |
| Optical clock | 429 THz | 1 m | 1 s | 0.59 rad | 10⁻³ rad | 590 | **Detectable** |
| Optical clock | 429 THz | 10 cm | 1 s | 0.059 rad | 10⁻³ rad | 59 | **Detectable** |

**Key insight**: The ~10⁵ frequency ratio between optical (10¹⁴ Hz) and microwave (10⁹ Hz) platforms creates a ~10⁵ sensitivity enhancement.

→ **See Figure F2** for platform comparison visualization.
→ **See Table T3** for detailed drift values.

---

## 4.2 Upper-Bound Experiments

For platforms in the bounded regime, experiments provide **upper bounds** on anomalous height-dependent couplings.

### Experiment 1: Chip Tilt

**Setup:**
- Mount planar chip on precision tilt stage (±0.01° resolution)
- Qubit pairs separated by distance L along tilt axis
- Tilt angle θ creates height difference: Δh = L × sin(θ)

**Protocol:**
1. Calibrate at θ = 0 (level)
2. For θ in [0°, 0.1°, 0.2°, ..., 1°]:
   - Set tilt angle
   - Wait for thermal equilibration (5 min)
   - Run 1000× Ramsey sequences
   - Record mean phase and variance
3. Fit slope: α = ∂ΔΦ/∂Δh
4. Compute 95% confidence interval

**Expected outcome:**
```
α_measured = 0 ± σ_α
Upper bound: α < α_SSZ + 2σ_α
```

For transmons with L = 5 mm, θ_max = 1°:
- Δh_max = 5 mm × sin(1°) = 87 μm
- ΔΦ_max ≈ 6×10⁻¹⁵ rad (undetectable)
- Upper bound: α < 9×10⁻³ rad/m (95% CI)

### Experiment 2: Remote Entanglement

**Setup:**
- Two cryostats separated by Δh = 10-100 cm
- Photon-mediated entanglement generation
- Precise height survey using differential GPS or leveling

**Protocol:**
1. Generate Bell state |Φ⁺⟩ between cryostats
2. WITHOUT compensation: measure phase after time t
3. WITH compensation: apply Φ_corr, measure phase
4. Randomize run order to avoid slow drifts
5. Repeat N = 10⁴ times
6. Compare F_with vs F_without

**Expected outcome:**
- For Δh = 50 cm, t = 10 μs, ω = 5 GHz:
  - ΔΦ ≈ 3.4×10⁻¹³ rad (undetectable)
- Upper bound places limit on anomalous couplings

### Experiment 3: 3D Chiplet Stack

**Setup:**
- 2-3 qubit dies stacked vertically
- Separation: 1-5 mm per layer
- Cross-layer entangling gates via TSV or flip-chip bonding

**Protocol:**
1. Characterize single-layer gates (reference)
2. Characterize cross-layer CZ gates
3. Sweep gate duration, measure phase accumulation
4. Add thermal sensors at each layer
5. Fit height-dependent slope
6. Correlate with thermal readings

**Expected outcome:**
- Cross-layer gate fidelity limited by fabrication, not SSZ
- Upper bound on height-dependent phase coupling

→ **See Table T4** for experiment configurations.

---

## 4.3 Statistical Framework

### Model Comparison

We compare three models using least-squares fitting:

**M₀ (Null model):**
```
ΔΦ = 0 + noise
```
No height dependence.

**M_SSZ (Fixed slope):**
```
ΔΦ = α_SSZ × Δh + noise
α_SSZ = ω × r_s / R²
```
SSZ prediction with no free parameters.

**M_anom (Free slope):**
```
ΔΦ = α × Δh + noise
α = free parameter
```
Linear fit to detect any height dependence.

### Likelihood Ratio Test

Given N measurements at heights Δh_i with results ΔΦ_i and uncertainties σ_i:

```
χ²(model) = Σᵢ [(ΔΦ_i - model(Δh_i))² / σ_i²]
```

Compare models via:
```
Δχ² = χ²(M₀) - χ²(M_anom)
```

### Confidence Intervals

For slope α from linear fit:

```
α = (Σᵢ wᵢ Δhᵢ ΔΦᵢ) / (Σᵢ wᵢ Δhᵢ²)
σ_α = √(1 / Σᵢ wᵢ Δhᵢ²)
```

where wᵢ = 1/σᵢ².

95% confidence interval:
```
α ∈ [α - 1.96σ_α, α + 1.96σ_α]
```

### Falsification Criteria

SSZ is **disfavored** if:
- Measured slope α differs from α_SSZ by > 3σ
- Compensation does NOT restore phase coherence
- Drift does not scale linearly with ω or t

SSZ is **supported** if:
- Null result in bounded regime (as predicted)
- Compensation reverses drift in detection regime
- Scaling matches predictions across platforms

→ **See Table T5** for regime classifications.

---

## 4.4 Required Controls

All experiments must include:

| Control | Purpose | Implementation |
|---------|---------|----------------|
| Thermal monitoring | Reject thermal confounds | RTDs at chip/cryostat |
| Vibration isolation | Reject mechanical noise | Pneumatic/active damping |
| Frequency interleaving | Separate ω-dependent effects | Alternate ω values |
| Reference qubits | Subtract common-mode noise | Same-height controls |
| Randomization | Decorrelate slow drifts | Random Δh order |
| LO characterization | Bound phase noise contribution | Beat-note measurement |

→ **See Appendix C** for complete confound playbook.

---

## 4.5 Detection Regime: Optical Clock Protocol

For optical clocks where detection is feasible:

**Setup:**
- Two Sr or Yb optical lattice clocks
- Separation: Δh = 1 m (vertical)
- Fiber link with noise cancellation
- GPS-disciplined timing reference

**Protocol:**
1. Synchronize clocks at same height (reference)
2. Move one clock vertically by Δh
3. Measure frequency ratio ν₂/ν₁ over time T
4. WITHOUT compensation: expect drift of ~0.6 rad/s
5. WITH compensation: expect null
6. Verify compensation reversal

**Metrics:**
- Fractional frequency shift: Δν/ν = ΔD ≈ 2×10⁻¹⁶ per metre
- Equivalent to Chou et al. (2010) but with compensation test

This experiment directly tests SSZ = GR equivalence in the weak field.
