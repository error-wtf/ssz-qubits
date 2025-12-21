# 7. Feasibility Landscape and Future Regimes

## 7.1 The Detection Gap

Our analysis reveals a stark dichotomy in SSZ detectability:

### The 12 Orders of Magnitude Gap

For superconducting transmons:
```
Signal:     ΔΦ_SSZ ≈ 10⁻¹³ rad (1 mm, 100 μs)
Noise:      σ_phase ≈ 1 rad
Gap:        10¹² (12 orders of magnitude)
```

This gap cannot be bridged by:
- Longer coherence times (limited to ~1 ms)
- Larger height differences (limited by cryostat size)
- Averaging (would require 10²⁴ shots)

### Crossing the Gap with Optical Frequencies

For optical atomic clocks:
```
Signal:     ΔΦ_SSZ ≈ 0.6 rad (1 m, 1 s)
Noise:      σ_phase ≈ 10⁻³ rad
SNR:        600 (easily detectable)
```

The ~10⁵ frequency enhancement (429 THz / 5 GHz) plus longer coherence times (1 s / 100 μs) gives ~10⁹ sensitivity improvement.

→ **See Figure F1** for visual comparison.

---

## 7.2 Platform Feasibility Matrix

| Platform | ω | T₂ | Max Δh | Max ΔΦ | Noise | SNR | Verdict |
|----------|---|-----|--------|--------|-------|-----|---------|
| Transmon | 5 GHz | 100 μs | 10 mm | 7×10⁻¹² | 1 | 10⁻¹¹ | **Bounded** |
| Fluxonium | 1 GHz | 1 ms | 10 mm | 1×10⁻¹¹ | 0.1 | 10⁻¹⁰ | **Bounded** |
| Trapped ion | 10 MHz | 10 s | 100 mm | 2×10⁻⁸ | 0.01 | 10⁻⁶ | **Bounded** |
| NV center | 3 GHz | 10 ms | 10 mm | 4×10⁻¹⁰ | 0.01 | 10⁻⁸ | **Bounded** |
| Optical clock | 429 THz | 10 s | 10 m | 60 | 10⁻³ | 10⁵ | **Detectable** |
| Optical qubit* | 100 THz | 1 s | 1 mm | 10⁻⁴ | 10⁻⁵ | 10 | **Future** |

*Projected future technology

→ **See Figure F2** for platform comparison.
→ **See Table T3** for detailed values.

---

## 7.3 Regime Classification

### Bounded Regime

**Definition**: SNR << 1, no detection possible

**Platforms**: All current solid-state qubits (transmon, fluxonium, NV, spin qubits)

**Outcome**: 
- Experiments yield null results
- Upper bounds on anomalous couplings
- Null result is SSZ-consistent

**Scientific value**:
- Constrains unknown physics
- Validates experimental methodology
- Prepares for future detection

### Detection Regime

**Definition**: SNR >> 1, direct measurement possible

**Platforms**: Optical atomic clocks, clock networks

**Outcome**:
- Measure SSZ/GR redshift directly
- Test compensation protocol
- Verify scaling predictions

**Scientific value**:
- Fundamental physics test
- SSZ = GR equivalence in weak field
- Compensation proof-of-concept

### Future Regime

**Definition**: SSZ drift comparable to error budget

**Platforms**: Future high-coherence systems (optical qubits, long-baseline networks)

**Outcome**:
- SSZ becomes engineering constraint
- Compensation required for operation
- SSZ-aware design mandatory

**Scientific value**:
- Practical application of theory
- Network synchronization protocols
- Quantum-enhanced geodesy

→ **See Table T5** for regime taxonomy.

---

## 7.4 Existing Experimental Validation

SSZ predictions in the weak field match GR, which has been validated:

### Hafele-Keating (1972)
- Atomic clocks on aircraft
- Measured gravitational redshift + kinematic effects
- Confirmed to 10% accuracy

### Pound-Rebka (1959)
- Gamma rays in vertical tower (22.5 m)
- Measured Δν/ν = 2.5×10⁻¹⁵
- Confirmed to 1% accuracy

### Chou et al. (2010)
- Optical clocks at 33 cm height difference
- Measured Δν/ν = 4×10⁻¹⁷
- Confirmed to 10⁻¹⁸ level

### Bothwell et al. (2022)
- Optical clock across millimetre sample
- Resolved gravitational redshift within single atomic cloud
- Confirmed to 10⁻¹⁹ level

**All these experiments confirm SSZ predictions** (which equal GR in weak field).

---

## 7.5 Path to Detection

### Near-term (1-3 years)

**Optical clock compensation test:**
1. Two Sr clocks at 1 m vertical separation
2. Measure frequency ratio without compensation
3. Apply SSZ-predicted correction
4. Verify compensation effectiveness
5. Publish as SSZ/GR confirmation

**Requirements**: Existing technology, ~$1M budget

### Medium-term (3-7 years)

**Optical clock network SSZ verification:**
1. Multiple nodes at various heights (1-100 m)
2. Simultaneous frequency comparisons
3. Map height-dependent phase evolution
4. Demonstrate network-wide compensation

**Requirements**: Clock network infrastructure, multi-site coordination

### Long-term (7-15 years)

**Satellite optical clock:**
1. Optical clock on ISS or dedicated satellite
2. Ground-to-space comparison (Δh ~ 400 km)
3. Extreme SSZ drift (orders of magnitude larger)
4. Test compensation at large separations

**Requirements**: Space-qualified optical clock, ~$100M budget

---

## 7.6 Why Null Results Matter

A common misconception: "If transmon experiments show nothing, SSZ is useless."

### Counter-argument

1. **Null confirms prediction**: SSZ explicitly predicts null for transmons. A null result supports, not refutes, SSZ.

2. **Upper bounds constrain physics**: Even non-detection places limits on unknown height-dependent couplings.

3. **Methodology validation**: Compensation protocol can be tested even without detection (check that applying random corrections does NOT restore coherence).

4. **Preparation for future**: Experimental infrastructure transfers to future high-coherence systems.

### What would falsify SSZ?

| Observation | Implication |
|-------------|-------------|
| Detection in transmons | Anomalous coupling (not SSZ) |
| Optical clock drift ≠ prediction | SSZ ≠ GR in weak field |
| Compensation fails in optical | SSZ formula incorrect |
| Non-linear height scaling | SSZ model incomplete |

---

## 7.7 Comparison with Related Proposals

### Pikovski et al. (2015): Gravitational Decoherence

- Predicts gravity-induced decoherence via proper time superposition
- Effect scales as (Δx)² m / ℏ
- Requires macroscopic superposition
- **Distinct from SSZ**: Pikovski is decoherence, SSZ is deterministic drift

### Zych et al. (2011): Proper Time Interferometry

- Proposes detecting proper time differences in matter-wave interferometry
- Requires atom interferometer at ~1 m scale
- **Related to SSZ**: Both probe gravitational time dilation on quantum systems

### Quantum Geodesy

- Uses clocks for precise height measurement
- Already demonstrated at cm level
- **SSZ application**: Quantum networks could serve as distributed gravitational sensors
