# 3. Control and Compensation Protocol

## 3.1 Core Insight: Deterministic Drift

The central insight of SSZ is that the phase drift is **deterministic**, not random. Once Δh and system parameters are known, the drift can be predicted exactly:

```
ΔΦ_predicted = ω × r_s × Δh / R² × t
```

This is fundamentally different from:
- Thermal noise (random, unpredictable)
- Charge noise (random telegraph, unpredictable)
- LO phase noise (stochastic, partially predictable)

**Because SSZ drift is deterministic, it can be fully compensated.**

---

## 3.2 With/Without Compensation Protocol

We propose a simple experimental protocol that discriminates SSZ from confounds:

### Step 1: Prepare Entangled State

Prepare a Bell state between two qubits at heights h and h+Δh:

```
|Ψ₀⟩ = (|00⟩ + |11⟩) / √2
```

### Step 2: WITHOUT Compensation

1. Let the system evolve for time t
2. The state becomes: |Ψ(t)⟩ = (|00⟩ + e^(iΔΦ)|11⟩) / √2
3. Perform tomography or Ramsey sequence
4. Measure accumulated phase ΔΦ_without
5. Record result

### Step 3: WITH Compensation

1. Apply correction phase to higher qubit:
   ```
   Φ_corr = -ω × (r_s × Δh / R²) × t
   ```
2. Let system evolve for time t
3. Perform same measurement
4. Measure ΔΦ_with
5. Record result

### Step 4: Compare Results

| Outcome | Interpretation |
|---------|----------------|
| ΔΦ_with ≈ 0, ΔΦ_without ≠ 0 | SSZ confirmed |
| Both ≈ 0 | SSZ below noise (bounded regime) |
| Both ≠ 0, similar | Confound (not SSZ) |
| ΔΦ_with ≠ 0, different | Partial confound |

### Key Discriminator

**Only SSZ reverses under compensation.** Confounds such as temperature drift, LO noise, or vibration do not depend on Δh in the predicted way and therefore do not cancel.

→ **See Figure F6** for protocol visualization.

---

## 3.3 Scaling Signatures

Four scaling signatures differentiate SSZ from confounds:

### Height Scaling

```
SSZ: ∂ΔΦ/∂Δh = ω × r_s / R² = constant
```

- Measure at multiple Δh values
- Fit slope α = ∂ΔΦ/∂Δh
- Compare to predicted α_SSZ

**Confounds**: Thermal gradients scale with environment, not height.

### Frequency Scaling

```
SSZ: ΔΦ ∝ ω (linear)
```

- Test at multiple qubit frequencies
- Plot ΔΦ vs ω
- Expect linear relationship

**Confounds**: Temperature effects typically scale as 1/f or f⁰.

### Time Scaling

```
SSZ: ΔΦ ∝ t (linear accumulation)
```

- Vary evolution time t
- Plot ΔΦ vs t
- Expect linear relationship

**Confounds**: 
- White noise: ∝ √t
- 1/f noise: sublinear

### Compensation Reversal

```
SSZ: ΔΦ_compensated → 0
```

- Apply calculated Φ_corr
- Measure residual phase
- Expect near-zero if SSZ correct

**Confounds**: Do not reverse (not functions of Δh).

→ **See Table T2** for complete signature comparison.

---

## 3.4 Compensation Implementation

### Software Phase Correction

For virtual Z gates (most efficient):

```python
def compensate_ssz(qubit_high, delta_h, omega, t):
    """Apply SSZ compensation via virtual Z gate."""
    r_s = 8.87e-3  # m
    R = 6.371e6    # m
    phi_corr = -omega * r_s * delta_h / R**2 * t
    qubit_high.rz(phi_corr)
```

### Pulse Timing Adjustment

For physical gate timing:

```python
def adjust_gate_time(t_nominal, delta_h):
    """Adjust gate duration for SSZ compensation."""
    r_s = 8.87e-3
    R = 6.371e6
    delta_D = r_s * delta_h / R**2
    t_adjusted = t_nominal * (1 + delta_D)
    return t_adjusted
```

### Calibration Procedure

1. Measure device height profile via profilometry
2. Compute ΔD for each qubit pair
3. Store compensation parameters in calibration database
4. Apply corrections during gate synthesis

**Key advantage**: SSZ drift is static and deterministic, so calibration is one-time (unless device is moved).

---

## 3.5 Sensitivity Analysis

### Compensation Accuracy Requirements

For residual error < ε after compensation:

```
|Φ_corr - ΔΦ_true| < ε
```

Required height accuracy:

```
δh / Δh < ε / ΔΦ
```

| Platform | ΔΦ | Target ε | Required δh/Δh |
|----------|-----|----------|----------------|
| Optical clock (1m) | 0.6 rad | 10⁻³ rad | 0.17% |
| Future optical (1mm) | 10⁻⁴ rad | 10⁻⁵ rad | 10% |

**Conclusion**: Height measurement accuracy of ~1% is sufficient for effective compensation.

---

## 3.6 Multi-Qubit Extension

For N qubits at heights h₁, h₂, ..., hₙ:

1. Choose reference qubit (e.g., lowest height h_ref)
2. For each qubit i, compute:
   ```
   Δh_i = h_i - h_ref
   ΔD_i = r_s × Δh_i / R²
   ```
3. Apply compensation phase to each qubit:
   ```
   Φ_corr,i = -ω × ΔD_i × t
   ```

This generalizes naturally to multi-qubit gates and error correction circuits.
