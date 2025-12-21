# Master Paper Appendices

---

## Appendix A: Full Derivations

### A.1 Segment Density Derivation

**Starting Point:** In SSZ, spacetime segments have density proportional to gravitational potential.

**Weak Field (r >> r_s):**
```
Ξ(r) = r_s / (2r)
```

where r_s = 2GM/c² is the Schwarzschild radius.

**Strong Field (r < 100 r_s):**
```
Ξ(r) = 1 - exp(-φ × r / r_s)
```

where φ = 1.618... (golden ratio).

**Transition:** C²-continuous via quintic Hermite interpolation in [90, 110] r_s.

### A.2 Time Dilation Factor

**Definition:**
```
D_SSZ(r) = 1 / (1 + Ξ(r))
```

**Taylor Expansion (weak field):**
```
D_SSZ ≈ 1 - Ξ + Ξ² - ... ≈ 1 - r_s/(2r)
```

**Comparison to GR:**
```
D_GR = √(1 - r_s/r) ≈ 1 - r_s/(2r) - (r_s/r)²/8 - ...
```

First-order terms match exactly.

### A.3 Differential Time Dilation

**Gradient:**
```
dD/dr = d/dr [1/(1 + r_s/(2r))]
      ≈ r_s / (2r²)  for small Ξ
```

**For height difference Δh:**
```
ΔD = (dD/dr) × Δh = (r_s / 2R²) × Δh × 2 = r_s × Δh / R²
```

### A.4 Phase Drift

**Accumulated phase:**
```
Φ = ω × τ
```

where τ is proper time.

**Differential phase:**
```
ΔΦ = ω × (τ_upper - τ_lower)
    = ω × Δτ
    = ω × ΔD × t_coord
```

**Final formula:**
```
ΔΦ = ω × (r_s × Δh / R²) × t
```

### A.5 Coherent Zone Width

**Definition:** Region where Ξ varies by < ε:
```
|Ξ(r + z/2) - Ξ(r - z/2)| < ε
```

**Solution:**
```
z(ε) = 4ε × R² / r_s
```

**Values:**
| ε | z(ε) |
|---|------|
| 10⁻¹⁸ | 18 mm |
| 10⁻¹⁵ | 18 m |
| 10⁻¹² | 18 km |

---

## Appendix B: Didactic Scaling Definition

### B.1 What Didactic Scaling Is

**Purpose:** Validate methodology when physical signals are too small.

**Definition:** Multiply SSZ prediction by scaling factor S >> 1:
```
ΔΦ_scaled = S × ΔΦ_physical
```

**Typical S:** 10¹⁰ to 10¹⁵

### B.2 What Gets Scaled

| Parameter | Scaled? | Reason |
|-----------|---------|--------|
| Signal magnitude | YES | Make visible |
| Noise model | NO | Keep realistic |
| Scaling laws | NO | Same functional form |
| Statistical methods | NO | Real analysis |

### B.3 What Didactic Scaling Proves

✓ Compensation algorithm works  
✓ Statistical framework is sound  
✓ Pipeline handles real data  
✗ Physical detectability (NOT claimed)

### B.4 Labeling Requirements

**All scaled results MUST include:**
```
[DIDACTIC SCALING: S = X, for methodology validation only]
```

---

## Appendix C: Confound Playbook

### C.1 Confound Matrix

| Source | Δh Scaling | ω Scaling | t Scaling | Randomization |
|--------|------------|-----------|-----------|---------------|
| **SSZ** | **Linear** | **Linear** | **Linear** | **Invariant** |
| Temperature | Correlates | Weak | Non-linear | Varies |
| LO phase | None | None | √t | Varies |
| Vibration | Mechanical | None | AC | Varies |
| Magnetic | Layout | Weak | Varies | Varies |
| Crosstalk | Proximity | ω-dependent | None | Fixed |

### C.2 Control Protocols

**Temperature:**
- Thermalize before each Δh setting
- Randomize Δh order → breaks thermal correlation
- Monitor with independent sensors

**LO Phase Noise:**
- Common-mode reference qubit
- Differential measurement cancels LO drift
- Short sequences minimize accumulation

**Vibration:**
- Accelerometer monitoring
- Mechanical isolation
- Statistical rejection of vibration-correlated runs

### C.3 SSZ Unique Signature

SSZ is uniquely identified by:
1. Linear in Δh
2. Linear in ω
3. Linear in t
4. Invariant under randomization
5. Deterministic (same Δh → same ΔΦ)

No known confound matches all five.

---

## Appendix D: Symbol Table & Constants

### D.1 Symbols

| Symbol | Definition | Units |
|--------|------------|-------|
| Ξ(r) | Segment density | - |
| D_SSZ(r) | Time dilation factor | - |
| ΔD | Differential time dilation | - |
| ω | Angular frequency | rad/s |
| f | Frequency | Hz |
| t | Evolution/integration time | s |
| Δh | Height difference | m |
| ΔΦ | Phase drift | rad |
| α | Slope (ΔΦ vs Δh) | rad/m |
| σ | Standard deviation | [varies] |
| N | Number of measurements | - |
| z(ε) | Coherent zone width | m |
| ε | Tolerance | - |
| r_s | Schwarzschild radius | m |
| R | Earth radius | m |
| φ | Golden ratio | - |
| S | Didactic scaling factor | - |

### D.2 Canonical Constants

| Constant | Value | Units |
|----------|-------|-------|
| c | 2.99792458×10⁸ | m/s |
| G | 6.67430×10⁻¹¹ | m³/(kg·s²) |
| ℏ | 1.054571817×10⁻³⁴ | J·s |
| φ | 1.6180339887498948 | - |
| M_Earth | 5.972×10²⁴ | kg |
| R_Earth | 6.371×10⁶ | m |
| r_s_Earth | 8.870×10⁻³ | m |

### D.3 Platform Parameters

| Platform | Frequency | Coherence | ΔΦ @ 1m |
|----------|-----------|-----------|---------|
| Transmon | 5 GHz | 100 μs | 6.9×10⁻¹⁰ rad |
| Optical Clock | 429 THz | 1 s | 0.59 rad |

### D.4 Derived Values

| Quantity | Formula | Value |
|----------|---------|-------|
| Ξ(R_Earth) | r_s/(2R) | 6.96×10⁻¹⁰ |
| D_SSZ(R_Earth) | 1/(1+Ξ) | 0.999999999304 |
| ΔD @ 1m | r_s×Δh/R² | 2.19×10⁻¹⁶ |

---

**© 2025 Carmen Wrede & Lino Casu**
