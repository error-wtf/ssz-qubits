# 4.2 Upper-Bound Experiments — Extended Version

For platforms in the Bounded Regime where the SSZ effect lies far below the noise floor, experiments serve not for direct detection but for establishing upper bounds on anomalous height-dependent couplings. These bounds are scientifically valuable: they confirm the SSZ prediction of undetectability on one hand and exclude alternative theories predicting stronger effects on the other.

---

## 4.2.1 Experiment 1: Chip Tilting (Tilt Experiment)

### Setup and Components

The tilt experiment uses the geometry of a planar qubit chip to create controlled height differences. The setup consists of the following components:

**Cryostat System:** A commercial dilution refrigerator (e.g., Bluefors LD-400) with a base temperature of 10–20 mK provides the experimental environment. The qubit chip is mounted at the mixing chamber, the coldest point of the system.

**Precision Tilt Stage:** A piezo-based tilt stage is installed between the chip holder and mixing chamber. Critical specifications:
- Angular range: ±2°
- Resolution: ±0.01° (corresponding to ~0.2 mrad)
- Reproducibility: < 0.005°
- Cryogenic compatibility: Operation at < 100 mK

Alternative: A stepper motor-based system with gearing can achieve higher angles but requires careful thermal decoupling.

**Qubit Chip:** A planar superconducting chip with at least two transmon qubits. Critical parameters:
- Qubit separation L along tilt axis: 5–10 mm
- Qubit frequencies: typically 4–6 GHz
- T₂ coherence time: > 50 μs

### Geometric Relations

For a tilt angle θ and qubit separation L along the tilt axis, the height difference is:

```
Δh = L × sin(θ)
```

For small angles (θ < 5°), sin(θ) ≈ θ (in radians), so:

```
Δh ≈ L × θ_rad = L × (θ_deg × π/180)
```

**Example calculation:** L = 5 mm, θ = 1°
```
Δh = 5 mm × sin(1°) = 5 mm × 0.01745 = 87.3 μm
```

### Measurement Protocol

**Phase 1: Calibration (θ = 0°)**

1. Align chip horizontally (spirit level or accelerometer)
2. Perform 100 Ramsey sequences per qubit
3. Determine baseline phase noise σ₀
4. Verify thermal stability (RTD sensors at 3+ positions)

**Phase 2: Angle Sweep**

For each angle θ ∈ {0°, 0.1°, 0.2°, 0.3°, 0.5°, 0.7°, 1.0°}:

1. Drive piezo stage to target angle (< 1 minute)
2. **Thermal equilibration:** Wait 5 minutes
   - Rationale: Angle change modifies thermal contact
   - Record RTD readings during wait period
3. **Data acquisition:**
   - N = 1000 Ramsey sequences (with/without protocol)
   - Wait time τ = 50–100 μs
   - Measure both qubits simultaneously
4. Save temperature readings at time of each measurement
5. Calculate statistics: ⟨ΔΦ⟩, σ_ΔΦ

**Phase 3: Return Path Measurement**

Repeat sweep in reverse order to identify hysteresis effects.

### Statistical Evaluation

**Linear Regression:**
```
ΔΦ_i = α × Δh_i + β + ε_i
```

where ε_i is the measurement error.

**Slope Estimation:**
```
α = (Σᵢ wᵢ Δhᵢ ΔΦᵢ) / (Σᵢ wᵢ Δhᵢ²)
```
with weights wᵢ = 1/σᵢ².

**95% Confidence Interval:**
```
α ∈ [α̂ - 1.96 × σ_α, α̂ + 1.96 × σ_α]
```

**Upper Bound:**
```
α_max = α̂ + 2σ_α
```

### Expected Results

For typical transmon parameters:
- SSZ prediction: α_SSZ = 6.87 × 10⁻⁹ rad/m
- Expected measurement: α ≈ 0 ± σ_α
- Typical σ_α: ~10⁻³ rad/m (dominated by T₂ noise)

**Interpretation:** The experiment will not detect a slope (α consistent with 0) but will establish an upper bound of α < 10⁻² rad/m—six orders of magnitude above the SSZ prediction.

### Noise Sources and Countermeasures

| Noise Source | Signature | Countermeasure |
|------------|----------|---------------|
| Thermal redistribution | Correlated with RTD readings | Thermal sensors, long equilibration |
| Mechanical hysteresis | Difference forward/return path | Measure both directions, averaging |
| Magnetic field change | Position-dependent, not ∝ Δh | Magnetometer, mu-metal shield |
| Vibrations during tilting | Transient effects | Acquire data during rest periods |

---

## 4.2.2 Experiment 2: Remote Entanglement

### Setup and Components

The remote entanglement experiment investigates SSZ effects over macroscopic distances by creating entangled states between spatially separated cryostats.

**Dual-Cryostat System:** Two separate dilution refrigerators, each with a qubit chip, vertically offset from each other. Critical configuration:
- Vertical separation: Δh = 10 cm to 1 m
- Horizontal distance: minimal (< 2 m for fiber length)

**Photon Link:** Entanglement is established via an optical channel:
- Microwave-to-optics converter in each cryostat
- Optical single-mode fiber between systems
- Noise suppression via servo loop on fiber length
- Heralding detector to confirm successful entanglement

**Height Measurement:** Precise determination of Δh through:
- Differential GPS (accuracy ~1 cm)
- Optical leveling (accuracy ~1 mm)
- Barometric pressure measurement (as consistency check)

### Entanglement Generation

The protocol for generating remote entanglement follows the "heralded entanglement" scheme:

1. **Local Superposition:** Prepare both qubits in |+⟩ = (|0⟩+|1⟩)/√2
2. **Photon Emission:** Each qubit emits a photon correlated with its state
3. **Bell-State Measurement:** Photons interfere at beam splitter, Hong-Ou-Mandel effect
4. **Heralding:** Upon detection of certain output patterns, qubit state is |Φ⁺⟩ = (|00⟩+|11⟩)/√2
5. **Timestamp:** Precise time of successful entanglement is noted

### Measurement Protocol

**Phase 1: Calibration at Equal Height**

1. Bring both cryostats to exactly the same height
2. Perform entanglement protocol, N = 10³ successful heralds
3. Determine Bell fidelity F₀ and phase Φ₀
4. Characterize baseline variance σ₀

**Phase 2: Vertical Separation**

1. Raise one cryostat by Δh (mechanically or using building structure)
2. Precisely measure height difference
3. Wait for thermal/mechanical stabilization (> 1 hour)

**Phase 3: Without Compensation**

For evolution times τ ∈ {10 μs, 50 μs, 100 μs, 500 μs}:
1. Establish entanglement
2. Allow time τ to elapse
3. Local tomography on both qubits
4. Extract phase ΔΦ_without and fidelity F_without
5. N = 10⁴ repetitions for statistics

**Phase 4: With Compensation**

Identical protocol, but:
1. After entanglement generation: compensation pulse Φ_corr on higher qubit
2. Allow time τ to elapse
3. Measurement as above
4. Extract ΔΦ_with and F_with

**Phase 5: Randomization**

- Randomly vary with/without order
- Measure different τ values interleaved
- Decorrelate slow drifts through randomization

### Expected Results

For Δh = 50 cm, ω = 2π × 5 GHz, τ = 100 μs:

```
ΔΦ_SSZ = 3.14×10¹⁰ × 8.87×10⁻³ × 0.5 / (6.371×10⁶)² × 10⁻⁴
       = 3.4 × 10⁻¹³ rad
```

This lies far below the noise floor (~0.1 rad for remote entanglement), therefore:
- Expectation: ΔΦ_without ≈ ΔΦ_with ≈ 0 (both in noise)
- Upper bound on anomalous coupling can be established

### Noise Sources and Countermeasures

| Noise Source | Signature | Countermeasure |
|------------|----------|---------------|
| Fiber length fluctuation | Fast phase jumps | Active fiber length stabilization |
| Different LO phases | Drift between cryostats | Common reference oscillator |
| Magnetic field differences | Location-dependent | Magnetometers at both sites |
| Environmental vibrations | Uncorrelated | Pneumatic tables, correlation analysis |

---

## 4.2.3 Experiment 3: 3D Chiplet Stack

### Setup and Components

The 3D stack experiment uses advanced packaging technology to place qubits in different vertical planes within the same cryostat.

**Chiplet Architecture:** Multiple qubit dies are stacked vertically:
- 2–3 layers with 1–4 qubits each
- Vertical spacing per layer: 1–5 mm
- Connection via TSV (Through-Silicon Via) or flip-chip bonding

**Interconnects:** Cross-layer gates are realized through:
- Capacitive coupling through substrate
- Inductive coupling via planar coils
- Direct galvanic connection via TSV

**Thermal Instrumentation:**
- RTD sensor on each layer
- Thermal anchors per layer to mixing chamber
- Heater for controlled gradient experiments

### Measurement Protocol

**Phase 1: Single-Layer Characterization**

For each layer individually:
1. Standard qubit benchmarking (T₁, T₂, gate fidelity)
2. Randomized benchmarking for single-qubit gates
3. Document baseline performance

**Phase 2: Cross-Layer Gate Characterization**

For all qubit pairs between different layers:
1. Perform CZ gate
2. Determine gate fidelity via interleaved RB
3. Measure phase accumulation during gate duration
4. Repeat at different gate durations

**Phase 3: Thermal Mapping**

1. Intentional heating power on one layer
2. Record temperature profile across all layers
3. Investigate correlation with phase drift
4. Separate thermal contribution from height contribution

**Phase 4: Height-Dependent Analysis**

1. Cross-layer gate drift as function of layer position
2. Slope fit: Δ(gate phase) vs. Δh (layer spacing)
3. Comparison with SSZ prediction

### Expected Results

For typical 3D stack parameters (Δh = 3 mm, ω = 5 GHz, t_gate = 100 ns):

```
ΔΦ_SSZ = 3.14×10¹⁰ × 8.87×10⁻³ × 3×10⁻³ / (6.371×10⁶)² × 10⁻⁷
       = 2.1 × 10⁻¹⁶ rad
```

This is negligible compared to typical gate errors (~10⁻³).

**Expectation:**
- Cross-layer fidelity primarily limited by fabrication
- No measurable height-dependent trend
- Upper bound on coupling: α < 10⁻² rad/m

### Noise Sources and Countermeasures

| Noise Source | Signature | Countermeasure |
|------------|----------|---------------|
| Thermal gradients between layers | Correlated with RTD differences | Layer-specific temperature measurement |
| Different substrate quality | Layer-dependent T₂ | Normalization to single-layer performance |
| Parasitic couplings | Cross-layer crosstalk | Dynamical decoupling |
| Mechanical stress | Layer-dependent frequency shifts | Frequency calibration per layer |

---

## 4.2.4 Summary of Experiments

| Experiment | Δh Range | Technical Complexity | Expected Result |
|------------|------------|------------------------|---------------------|
| Chip Tilt | 10–100 μm | Medium | α < 10⁻² rad/m |
| Remote Entanglement | 10–100 cm | High | Fidelity limited by link |
| 3D Stack | 1–5 mm | High | Fabrication-limited |

All three experiments are expected to yield null results that are, however, fully consistent with SSZ predictions. The scientific value lies in establishing upper bounds and preparing for future, more sensitive measurements.

---

© 2025 Carmen Wrede & Lino Casu
