# 3. Qubit Physics and SSZ

## 3.1 Transmon Qubit Fundamentals

The transmon qubit is the workhorse of superconducting quantum computing. Understanding its physics is essential for analyzing SSZ effects.

### Circuit Model

A transmon consists of:
- Josephson junction with energy E_J
- Shunt capacitor with energy E_C = e²/(2C)
- Ratio E_J/E_C ~ 50-100 (charge-insensitive regime)

The Hamiltonian:
```
H = 4E_C(n - n_g)² - E_J cos(φ)
```

where n is the number of Cooper pairs and φ is the superconducting phase.

### Energy Levels

The transition frequency between ground |0⟩ and excited |1⟩ states:
```
ω₀₁ = √(8E_J E_C) - E_C
```

Typical values:
- ω₀₁/(2π) = 4-8 GHz
- Anharmonicity α = ω₁₂ - ω₀₁ ≈ -200 MHz

### Coherence Properties

| Property | Symbol | Typical Value | Best Achieved |
|----------|--------|---------------|---------------|
| Relaxation time | T₁ | 50-100 μs | 500 μs |
| Dephasing time | T₂ | 50-100 μs | 200 μs |
| Gate time | t_gate | 20-50 ns | 10 ns |
| Gate fidelity | F | 99.5% | 99.9% |

### Noise Sources

| Source | Mechanism | Scaling |
|--------|-----------|---------|
| Charge noise | TLS in substrate | 1/f |
| Flux noise | Magnetic impurities | 1/f |
| Photon noise | Thermal photons | exp(-ℏω/k_B T) |
| Quasiparticles | Broken Cooper pairs | T-dependent |

Total dephasing: σ_φ ~ 1 rad over T₂.

---

## 3.2 Phase Accumulation in Qubits

A qubit in state |ψ⟩ = α|0⟩ + β|1⟩ accumulates phase over time:

### Free Evolution

```
|ψ(t)⟩ = α|0⟩ + β·e^(-iωt)|1⟩
```

The relative phase φ(t) = ωt determines the state on the Bloch sphere equator.

### In a Rotating Frame

Applying the rotating wave approximation at drive frequency ω_d:
```
|ψ_rot(t)⟩ = α|0⟩ + β·e^(-iΔt)|1⟩
```

where Δ = ω - ω_d is the detuning.

### SSZ Modification

With SSZ, the qubit frequency depends on height:
```
ω(h) = ω_0 × D(h) = ω_0 / (1 + Ξ(h))
```

For two qubits at heights h₁ and h₂:
```
Δω = ω_0 × (D(h₂) - D(h₁)) = ω_0 × ΔD
```

This differential frequency causes relative phase drift:
```
ΔΦ(t) = Δω × t = ω_0 × ΔD × t
```

---

## 3.3 SSZ Effect on Gate Operations

### Single-Qubit Gates

A Pauli-X gate (bit flip) requires a π-pulse:
```
t_π = π / Ω_Rabi
```

If qubit frequency drifts during the gate:
```
φ_error = ω × ΔD × t_π
```

For transmon (ω = 2π×5 GHz, Δh = 1 mm, t_π = 20 ns):
```
φ_error = 3.14e10 × 2.19e-19 × 20e-9 = 1.4e-16 rad
```

**Completely negligible** compared to other gate errors (~10⁻³ rad).

### Two-Qubit Gates

For a CZ (controlled-Z) gate between qubits at different heights:
- Gate time: ~200 ns
- Phase accumulation: ΔΦ = ω × ΔD × t_gate

For Δh = 1 mm:
```
ΔΦ = 3.14e10 × 2.19e-19 × 200e-9 = 1.4e-15 rad
```

Still negligible, but 10× larger than single-qubit case.

### Idle Periods

During algorithm execution, qubits often wait idle:
- Typical idle: 1-10 μs
- Phase accumulation: ΔΦ ~ 10⁻¹⁴ to 10⁻¹³ rad

Even maximum idle times are far below noise.

---

## 3.4 Decoherence vs Deterministic Drift

### Key Distinction

| Property | Decoherence | SSZ Drift |
|----------|-------------|-----------|
| Nature | Random | Deterministic |
| Predictability | Statistical only | Exact |
| Source | Environment | Geometry |
| Time scaling | √t or log(t) | Linear t |
| Compensation | QEC (expensive) | Phase shift (cheap) |
| Fidelity impact | Reduces purity | Rotates state |

### Bloch Sphere Picture

**Decoherence**: State vector shrinks toward center (mixed state)
**SSZ Drift**: State vector rotates around Z-axis (pure state maintained)

### Mathematical Comparison

Decoherence (T₂ process):
```
ρ(t) = |0⟩⟨0| + e^(-t/T₂)·e^(iφ(t))|1⟩⟨0| + h.c.
```

SSZ drift (coherent):
```
|ψ(t)⟩ = (|0⟩ + e^(iΔΦ(t))|1⟩)/√2
```

SSZ preserves coherence; it just shifts the phase.

---

## 3.5 Platform Comparison

### Superconducting Qubits

| Type | ω/(2π) | T₂ | Δh_max | SSZ Effect |
|------|--------|-----|--------|------------|
| Transmon | 5 GHz | 100 μs | 10 mm | 10⁻¹² rad |
| Fluxonium | 1 GHz | 1 ms | 10 mm | 10⁻¹¹ rad |
| Charge qubit | 10 GHz | 1 μs | 10 mm | 10⁻¹⁴ rad |

### Trapped Ions

| Species | ω/(2π) | T₂ | Δh_max | SSZ Effect |
|---------|--------|-----|--------|------------|
| ⁴⁰Ca⁺ | 729 THz (optical) | 1 s | 1 mm | 10⁻⁶ rad |
| ¹⁷¹Yb⁺ | 12.6 GHz | 10 min | 1 mm | 10⁻⁸ rad |
| ⁹Be⁺ | 1.25 GHz | 10 s | 1 mm | 10⁻⁹ rad |

### NV Centers

| Type | ω/(2π) | T₂ | Δh_max | SSZ Effect |
|------|--------|-----|--------|------------|
| Ground state | 2.87 GHz | 1 ms | 1 mm | 10⁻¹¹ rad |
| Optical | 470 THz | 10 ns | 1 mm | 10⁻¹¹ rad |

### Optical Atomic Clocks

| Species | ω/(2π) | T₂ | Δh_max | SSZ Effect |
|---------|--------|-----|--------|------------|
| ⁸⁷Sr | 429 THz | 10 s | 1 m | **6 rad** |
| ¹⁷¹Yb | 518 THz | 10 s | 1 m | **7 rad** |
| ²⁷Al⁺ | 1.12 PHz | 1 s | 1 m | **16 rad** |

**Only optical platforms can detect SSZ** with current technology.

---

## 3.6 Implications for Quantum Computing

### Current Generation

For all current superconducting quantum computers:
- IBM: 127-1121 qubits, planar layout, Δh < 100 μm
- Google: 72 qubits, planar layout, Δh < 50 μm
- Rigetti: 80 qubits, 3D integration, Δh < 1 mm

SSZ effect: < 10⁻¹² rad per gate cycle. **Completely negligible.**

### Future Generations

As coherence times improve toward milliseconds and beyond:
- SSZ effect grows linearly with T₂
- At T₂ = 10 ms: SSZ ~ 10⁻⁹ rad (still negligible)
- At T₂ = 1 s: SSZ ~ 10⁻⁶ rad (approaching QEC thresholds)

### Optical Quantum Computing

Photonic and optical-frequency platforms:
- Frequencies 10⁵× higher than microwave
- Coherence times potentially longer
- SSZ becomes relevant at mm-scale separations

**Design recommendation**: Future optical quantum computers should include SSZ calibration in their control systems.
