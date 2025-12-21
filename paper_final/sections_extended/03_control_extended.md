# 3. Control and Compensation Protocol — Extended Version

## 3.2 The With/Without Compensation Protocol

The central experimental strategy for validating SSZ theory relies on the deterministic nature of the predicted phase drift. Unlike stochastic noise sources, which by definition cannot be predicted, the SSZ drift can be exactly calculated from known system parameters and consequently fully compensated. This property enables an elegant experimental protocol that unambiguously distinguishes SSZ from all known confounding sources.

### 3.2.1 Experimental Implementation: The Ramsey Protocol

The standard tool for phase measurement in quantum systems is Ramsey interferometry. For two qubits at different heights h₁ and h₂ = h₁ + Δh, the experiment proceeds as follows:

**Superposition Preparation:** First, each qubit is transformed from its ground state |0⟩ into an equal-weight superposition by a π/2 pulse around the X-axis:

```
|0⟩ → (|0⟩ + |1⟩)/√2
```

Alternatively, an entangled Bell state between both qubits can be prepared:

```
|Ψ₀⟩ = (|00⟩ + |11⟩)/√2
```

**Free Evolution:** During the waiting time τ, each qubit accumulates a phase proportional to its local time dilation. For the qubit at height h₁:

```
Φ₁(τ) = ω × D(h₁) × τ
```

and for the qubit at h₂:

```
Φ₂(τ) = ω × D(h₂) × τ
```

The relative phase difference is:

```
ΔΦ(τ) = Φ₂ - Φ₁ = ω × (D(h₂) - D(h₁)) × τ = ω × ΔD × τ
```

**Final Pulse and Measurement:** A second π/2 pulse converts the accumulated phase into a measurable population difference. The probability of finding the qubit in state |1⟩ oscillates with the phase:

```
P(|1⟩) = (1 + cos(ΔΦ))/2
```

### 3.2.2 Without Compensation: Reference Measurement

In the first part of the protocol, the phase drift is measured without correction. This establishes the baseline:

1. Prepare Bell state
2. Allow waiting time τ to elapse
3. State evolves to: |Ψ(τ)⟩ = (|00⟩ + e^(iΔΦ)|11⟩)/√2
4. Perform tomography or complete Ramsey sequence
5. Extract accumulated phase ΔΦ_without
6. Repeat procedure N times for statistical significance

With sufficient statistics (typically N = 10³–10⁴ repetitions), one obtains a mean ⟨ΔΦ_without⟩ and a standard deviation σ.

### 3.2.3 With Compensation: The Decisive Test

In the second part, the predicted SSZ correction is actively applied:

1. Prepare Bell state
2. **Apply compensation phase to higher qubit:**
   ```
   Φ_corr = -ω × (r_s × Δh / R²) × τ
   ```
3. Allow waiting time τ to elapse
4. Perform identical measurement as in the without case
5. Extract accumulated phase ΔΦ_with
6. Repeat procedure N times

### 3.2.4 Implementation of the Compensation Phase

The practical implementation of compensation can be done in various ways:

**Virtual Z-Rotation (preferred):** In modern quantum compiler frameworks like Qiskit, Z-rotations are often implemented as "virtual gates". Instead of applying a physical pulse, the reference frame for all subsequent pulses of the affected qubit is rotated. This has the advantage that no additional error source is introduced by a physical pulse:

```python
from qiskit import QuantumCircuit

def apply_ssz_compensation(qc, qubit_index, delta_h, omega, tau):
    """
    Apply SSZ compensation as virtual Z-rotation.
    
    Args:
        qc: QuantumCircuit
        qubit_index: Index of the qubit to compensate
        delta_h: Height difference in meters
        omega: Qubit frequency in rad/s
        tau: Evolution time in seconds
    """
    r_s = 8.87e-3  # Earth's Schwarzschild radius [m]
    R = 6.371e6    # Earth radius [m]
    
    phi_corr = -omega * r_s * delta_h / R**2 * tau
    qc.rz(phi_corr, qubit_index)
```

**Physical Pulse Adjustment:** Alternatively, the gate duration itself can be modified to compensate for differential time dilation. The higher qubit "ticks" faster, so its gate must be shortened accordingly:

```python
def adjusted_gate_duration(t_nominal, delta_h):
    """
    Adjust gate duration for SSZ compensation.
    """
    r_s = 8.87e-3
    R = 6.371e6
    delta_D = r_s * delta_h / R**2
    t_adjusted = t_nominal * (1 - delta_D)
    return t_adjusted
```

### 3.2.5 Interpretation of Results

The combination of with and without measurements provides a decision matrix:

| ΔΦ_without | ΔΦ_with | Interpretation |
|------------|---------|----------------|
| ≈ 0 | ≈ 0 | Bounded Regime: Both signals in noise |
| ≠ 0, ∝ Δh | ≈ 0 | **SSZ confirmed**: Drift present and successfully compensated |
| ≠ 0 | ≠ 0, similar | Confound: Drift independent of SSZ correction |
| ≠ 0 | ≠ 0, partially reduced | Mixed signal: SSZ + confound superimposed |

**The critical discriminator:** Only a deterministic, height-dependent drift with the exact amplitude predicted by SSZ is canceled by the compensation. Thermal drifts, LO phase noise, or magnetic disturbances do not depend on Δh in the predicted manner and therefore cannot be compensated by the SSZ correction formula.

### 3.2.6 Why Temperature Drifts Are Not Removed

A common objection is that thermal effects could be falsely interpreted as SSZ. However, these differ fundamentally:

- **Thermal gradients** arise from uneven heat dissipation, radiation coupling, or variations in cryostat geometry. They are environment-dependent and not determined by height.
  
- **SSZ drift** is a direct function of Δh, ω, and τ with a universal amplitude fixed by fundamental constants.

Specifically: if the chip is tilted by 1° creating Δh = 87 μm, the thermal effect depends on whether the heat source (e.g., microwave line) is on the "high" or "low" side. SSZ drift, in contrast, depends only on the height difference itself, independent of orientation relative to the heat source.

---

## 3.3 Scaling Signatures: Detailed Analysis

The distinction between SSZ and confounds relies on four characteristic scaling laws. Each of these laws represents an independent testing opportunity, and their combined fulfillment provides strong evidence for the SSZ hypothesis.

### 3.3.1 Height Scaling

**Mathematical Prediction:** The SSZ phase drift is strictly linear in height difference:

```
ΔΦ = α_SSZ × Δh  with  α_SSZ = ω × r_s / R² = const
```

The slope α_SSZ is uniquely fixed by fundamental constants and the qubit frequency. For a 5-GHz transmon:

```
α_SSZ = 3.14×10¹⁰ × 8.87×10⁻³ / (6.371×10⁶)²
      = 6.87×10⁻⁹ rad/m
```

**Experimental Protocol:**

1. Mount chip on precision tilt stage (piezo actuator, resolution ±0.01°)
2. For a series of angles θ ∈ {0°, 0.1°, 0.2°, ..., 1.0°}:
   - Set angle
   - Wait 5 minutes for thermal equilibration
   - Perform N = 1000 Ramsey sequences
   - Record mean phase and variance
3. Linear regression: ΔΦ = α × Δh + β
4. Calculate 95% confidence interval for α

**Distinguishing from Confounds:** Thermal gradients scale with environment geometry, not height. In a tilt-stage experiment, the relative position of qubits to the heat sink (mixing chamber) changes in complex, non-linear ways. Magnetic field gradients depend on position relative to field sources, not absolute height in the gravitational field.

An experiment showing strictly linear Δh dependence with the predicted slope α_SSZ provides strong evidence for SSZ.

### 3.3.2 Frequency Scaling

**Mathematical Prediction:** The SSZ drift is linear in qubit frequency:

```
ΔΦ ∝ ω
```

This is a direct consequence of the phase accumulation rate: the higher the frequency, the more phase cycles per unit time, the greater the difference under differential time dilation.

**Experimental Protocol:**

1. Use multi-frequency chip (e.g., qubits with ω₁ = 4 GHz, ω₂ = 5 GHz, ω₃ = 6 GHz)
2. Perform identical Ramsey sequence on all qubits
3. Plot phase drift as function of ω
4. Linear regression: ΔΦ = β_ω × ω

**Distinguishing from Confounds:**

- **Thermal effects:** Frequency shifts due to temperature scale as dω/dT, typically ~1 MHz/K. This is an absolute shift, not a relative phase drift. The resulting phase accumulation shows complex frequency dependence, not strictly ∝ ω.

- **1/f noise:** Low-frequency noise typically shows a 1/f spectrum, i.e., a decrease with increasing frequency—the opposite of the SSZ prediction.

- **White phase noise:** Frequency-independent, i.e., ΔΦ ∝ ω⁰.

A linear increase of phase drift with ω is a strong SSZ signal.

### 3.3.3 Time Scaling

**Mathematical Prediction:** The SSZ phase accumulation is linear in time:

```
ΔΦ(t) = (ω × r_s × Δh / R²) × t
```

This is the hallmark of a deterministic drift: constant rate of phase accumulation.

**Experimental Protocol:**

1. Ramsey sequences with varying wait time τ ∈ {10 μs, 20 μs, 50 μs, 100 μs, 200 μs}
2. For each τ: N = 1000 repetitions
3. Plot ΔΦ as function of τ
4. Linear regression: ΔΦ = γ × τ

**Distinguishing from Confounds:**

- **Random Walk (White Noise):** Accumulates as ΔΦ ∝ √τ. The characteristic signature is a slowdown of phase growth at long times.

- **1/f Noise:** Sublinear accumulation, typically ΔΦ ∝ τ^α with α < 1.

- **Systematic Drift (e.g., thermal):** Can be linear, but with environment-dependent rate, not the one predicted by SSZ.

The distinction between linear (SSZ) and √τ scaling (random walk) is experimentally accessible and provides a robust discriminator.

### 3.3.4 Compensation Reversal

**The Decisive Test:** Only an effect that exactly matches the SSZ formula is canceled by applying Φ_corr = -ω × r_s × Δh / R² × τ:

```
ΔΦ_compensated = ΔΦ_SSZ + Φ_corr = 0
```

**Experimental Protocol:**

1. Without measurement: Record ΔΦ_without
2. With measurement: Apply Φ_corr, record ΔΦ_with
3. Calculate reduction factor: R = |ΔΦ_with / ΔΦ_without|

**Expected Results:**

- **SSZ dominant:** R ≈ 0 (complete compensation)
- **Confound dominant:** R ≈ 1 (no compensation)
- **Mixed:** 0 < R < 1 (partial compensation)

**Why Only SSZ Is Reversed:** The compensation formula is specific to the SSZ mechanism. Thermal drifts, LO noise, or magnetic disturbances have no connection to Earth's mass, the Schwarzschild radius, or height difference. Applying the SSZ correction to these effects has no physical basis and therefore does not lead to compensation.

---

## 3.4 Summary: Confound Discrimination

| Signature | SSZ | Thermal | LO-Noise | Magnetic | Vibration |
|----------|-----|---------|----------|----------|-----------|
| ∝ Δh (linear) | ✓ | ✗ | ✗ | ✗ | ✗ |
| ∝ ω (linear) | ✓ | ✗ | √f or 1/f | ✗ | ✗ |
| ∝ t (linear) | ✓ | ✓ | √t | ✓ | impulsive |
| Compensation reverses | ✓ | ✗ | ✗ | ✗ | ✗ |

The combination of all four signatures—especially compensation reversal—provides a robust criterion for identifying SSZ effects.

---

© 2025 Carmen Wrede & Lino Casu
