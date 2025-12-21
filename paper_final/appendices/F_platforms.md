# Appendix F: Platform Technical Specifications

## F.1 Superconducting Qubits

### Transmon

| Parameter | Symbol | Value | Range |
|-----------|--------|-------|-------|
| Qubit frequency | ω₀₁/(2π) | 5 GHz | 4-8 GHz |
| Anharmonicity | α/(2π) | -200 MHz | -100 to -300 MHz |
| E_J/E_C ratio | - | 50-100 | 20-200 |
| Relaxation time | T₁ | 50-100 μs | 10-500 μs |
| Dephasing time | T₂ | 50-100 μs | 10-200 μs |
| Gate time (1Q) | t_1Q | 20 ns | 10-50 ns |
| Gate time (2Q) | t_2Q | 200 ns | 50-500 ns |
| Gate fidelity (1Q) | F_1Q | 99.9% | 99%-99.99% |
| Gate fidelity (2Q) | F_2Q | 99.5% | 98%-99.9% |
| Operating temperature | T | 15 mK | 10-50 mK |
| Chip size | L | 5-10 mm | 2-20 mm |
| Qubit count | N | 10-100 | 1-1000+ |

### Fluxonium

| Parameter | Symbol | Value | Range |
|-----------|--------|-------|-------|
| Qubit frequency | ω₀₁/(2π) | 0.5-1 GHz | 0.1-2 GHz |
| Anharmonicity | α/(2π) | Large | GHz scale |
| E_L/E_J ratio | - | 0.5-2 | 0.1-10 |
| Relaxation time | T₁ | 100-500 μs | 50-1000 μs |
| Dephasing time | T₂ | 100-500 μs | 50-500 μs |
| Gate time | t_gate | 50-100 ns | 20-200 ns |
| Operating temperature | T | 15 mK | 10-30 mK |

### SSZ Implications

For transmon at Δh = 1 mm, t = 100 μs:
```
ΔΦ_SSZ = 2π × 5e9 × 8.87e-3 × 1e-3 / (6.371e6)² × 1e-4
       = 6.87e-13 rad
```

**Ratio to noise**: 6.87e-13 / 1 = 6.87e-13 (negligible)

---

## F.2 Trapped Ions

### ⁴⁰Ca⁺

| Parameter | Symbol | Value |
|-----------|--------|-------|
| Qubit transition | - | S₁/₂ ↔ D₅/₂ |
| Optical frequency | ω/(2π) | 729 THz |
| Hyperfine frequency | - | N/A |
| Coherence time | T₂ | 1-10 s |
| Gate time (1Q) | t_1Q | 1-10 μs |
| Gate time (2Q) | t_2Q | 50-200 μs |
| Gate fidelity | F | 99.9%+ |
| Ion spacing | d | 5-10 μm |
| Trap depth | U | ~1 eV |

### ¹⁷¹Yb⁺

| Parameter | Symbol | Value |
|-----------|--------|-------|
| Qubit transition | - | ²S₁/₂ hyperfine |
| Hyperfine frequency | ω/(2π) | 12.6 GHz |
| Optical frequency | - | 369 nm (cooling) |
| Coherence time | T₂ | 10 min+ |
| Gate fidelity | F | 99.99% |

### SSZ Implications

For optical transition (729 THz) at Δh = 1 mm, t = 1 s:
```
ΔΦ_SSZ = 2π × 729e12 × 2.19e-16 × 1
       = 1.0e-3 rad
```

**Detectable** with high-precision ion clocks.

---

## F.3 Neutral Atoms

### ⁸⁷Rb

| Parameter | Symbol | Value |
|-----------|--------|-------|
| Clock transition | - | 5S₁/₂ ↔ 5P₃/₂ |
| Frequency | ω/(2π) | 384 THz |
| Hyperfine splitting | - | 6.8 GHz |
| Trap depth | U/k_B | ~1 mK |
| Coherence time | T₂ | 1-10 s |
| Array size | N | 100-1000 |
| Atom spacing | d | 3-10 μm |

### ¹³³Cs

| Parameter | Symbol | Value |
|-----------|--------|-------|
| Clock transition | - | Hyperfine |
| Frequency | ω/(2π) | 9.2 GHz |
| Coherence time | T₂ | 1-100 s |

### SSZ Implications

For optical Rb at Δh = 1 m, t = 1 s:
```
ΔΦ_SSZ = 2π × 384e12 × 2.19e-13 × 1
       = 0.53 rad
```

**Easily detectable** in optical lattice clocks.

---

## F.4 Optical Atomic Clocks

### ⁸⁷Sr Lattice Clock

| Parameter | Symbol | Value |
|-----------|--------|-------|
| Clock transition | - | ¹S₀ ↔ ³P₀ |
| Frequency | ω/(2π) | 429.228 THz |
| Wavelength | λ | 698 nm |
| Natural linewidth | Γ | 1 mHz |
| Fractional stability | σ_y | 10⁻¹⁸ |
| Systematic uncertainty | Δν/ν | 10⁻¹⁸ |
| Interrogation time | T | 1-10 s |
| Atom number | N | 10³-10⁴ |

### ¹⁷¹Yb Lattice Clock

| Parameter | Symbol | Value |
|-----------|--------|-------|
| Clock transition | - | ¹S₀ ↔ ³P₀ |
| Frequency | ω/(2π) | 518.295 THz |
| Wavelength | λ | 578 nm |
| Natural linewidth | Γ | 10 mHz |
| Fractional stability | σ_y | 10⁻¹⁸ |

### ²⁷Al⁺ Ion Clock

| Parameter | Symbol | Value |
|-----------|--------|-------|
| Clock transition | - | ¹S₀ ↔ ³P₀ |
| Frequency | ω/(2π) | 1.121 PHz |
| Natural linewidth | Γ | 8 mHz |
| Fractional stability | σ_y | 10⁻¹⁹ |

### SSZ Implications

For Sr clock at Δh = 1 m, t = 1 s:
```
ΔΦ_SSZ = 2π × 429e12 × 2.19e-13 × 1
       = 0.59 rad

SNR = 0.59 / 1e-3 = 590
```

**Gold standard for SSZ detection.**

---

## F.5 NV Centers in Diamond

| Parameter | Symbol | Value |
|-----------|--------|-------|
| Ground state splitting | ω/(2π) | 2.87 GHz |
| Zero-field splitting | D | 2.87 GHz |
| Strain coupling | - | ~1 GHz/strain |
| T₁ (room temp) | T₁ | 5-10 ms |
| T₂ (room temp) | T₂ | 1-3 μs |
| T₂ (cryogenic) | T₂ | 1-10 ms |
| Optical lifetime | τ | 12 ns |
| Operating temperature | T | 4 K - 300 K |

### SSZ Implications

For NV at Δh = 1 mm, t = 1 ms:
```
ΔΦ_SSZ = 2π × 2.87e9 × 2.19e-19 × 1e-3
       = 3.9e-12 rad
```

**Negligible** for current NV experiments.

---

## F.6 Photonic Qubits

| Parameter | Symbol | Value |
|-----------|--------|-------|
| Wavelength | λ | 1550 nm (telecom) |
| Frequency | ω/(2π) | 193 THz |
| Coherence time | T₂ | Limited by path |
| Gate time | t_gate | ~ps |
| Loss | α | 0.2 dB/km (fiber) |
| Detection efficiency | η | 90%+ |

### SSZ Implications

Photons travel at c, so SSZ affects:
- Time of flight (Shapiro delay)
- Not direct phase accumulation

For fiber link with Δh = 10 m over 100 km:
```
ΔT_Shapiro ≈ r_s × Δh / (c × R) × L/c
           ≈ 10⁻²¹ s (negligible)
```

---

## F.7 Summary Table

| Platform | ω/(2π) | T₂ | Best Δh | ΔΦ_SSZ | SNR | Regime |
|----------|--------|-----|---------|--------|-----|--------|
| Transmon | 5 GHz | 100 μs | 10 mm | 7e-12 | 10⁻¹¹ | Bounded |
| Fluxonium | 1 GHz | 1 ms | 10 mm | 1e-11 | 10⁻¹⁰ | Bounded |
| Trapped ion | 12 GHz | 10 min | 1 mm | 10⁻⁷ | 10⁻⁵ | Bounded |
| Trapped ion | 729 THz | 1 s | 1 mm | 10⁻³ | 10 | Marginal |
| NV center | 2.87 GHz | 10 ms | 1 mm | 10⁻¹¹ | 10⁻⁸ | Bounded |
| Sr clock | 429 THz | 10 s | 1 m | 6 | 6000 | **Detectable** |
| Yb clock | 518 THz | 10 s | 1 m | 7 | 7000 | **Detectable** |
| Al⁺ clock | 1.1 PHz | 1 s | 1 m | 16 | 16000 | **Detectable** |
