# 2. Theory: Deriving the SSZ Phase Drift

## 2.1 Segment Density and Time Dilation

In a weak gravitational field, the metric can be expanded in powers of the gravitational potential. The SSZ framework introduces the **segment density** as the fundamental quantity:

### Definition (Weak Field, r >> r_s)

```
Ξ(r) = r_s / (2r)
```

where:
- r_s = 2GM/c² is the Schwarzschild radius
- r is the radial distance from Earth's center
- For Earth: r_s ≈ 8.87 mm

### Time Dilation Factor

A clock at height h experiences a time-dilation factor relative to infinity:

```
D(h) = 1 / (1 + Ξ(h))
```

Proper time increments as:

```
dτ = D(h) dt
```

### Expansion for h << R

For heights h much smaller than Earth's radius R:

```
Ξ(h) = r_s / (2(R+h)) ≈ r_s / (2R) × (1 - h/R + ...)
```

At Earth's surface (h = 0):

```
Ξ₀ = r_s / (2R) = 8.87×10⁻³ / (2 × 6.371×10⁶) = 6.96×10⁻¹⁰
```

This gives D₀ ≈ 0.999999999304, matching GR to first order.

---

## 2.2 Differential Time Dilation

The differential time dilation between two heights h and h+Δh is found by Taylor expansion:

```
ΔD ≡ D(h+Δh) - D(h) ≈ (dD/dh) × Δh
```

Computing the derivative:

```
dD/dh = d/dh [1/(1 + Ξ(h))]
      = -1/(1+Ξ)² × dΞ/dh
      = -1/(1+Ξ)² × (-r_s/(2(R+h)²))
      = r_s / (2(R+h)² × (1+Ξ)²)
```

For h << R and Ξ << 1:

```
dD/dh ≈ r_s / (2R²)
```

Therefore:

```
ΔD = r_s × Δh / R²
```

### Numerical Verification

For Δh = 1 mm:

```
ΔD = 8.87×10⁻³ × 1×10⁻³ / (6.371×10⁶)²
   = 8.87×10⁻⁶ / 4.059×10¹³
   = 2.19×10⁻¹⁹
```

**Unit check**: [m × m / m²] = dimensionless ✓

---

## 2.3 Phase Drift for a Two-Qubit System

Consider two qubits at heights h and h+Δh with angular frequency ω. The phase accumulated by each qubit is:

```
Φ₁(t) = ω × D(h) × t
Φ₂(t) = ω × D(h+Δh) × t
```

The **SSZ phase drift** is the difference:

```
ΔΦ(t) = Φ₂ - Φ₁ = ω × (D(h+Δh) - D(h)) × t = ω × ΔD × t
```

Substituting ΔD:

```
ΔΦ(t) = ω × r_s × Δh / R² × t
```

### Numerical Example: Transmon Qubit

Parameters:
- ω/(2π) = 5 GHz → ω = 3.14×10¹⁰ rad/s
- Δh = 1 mm = 10⁻³ m
- t = 100 μs = 10⁻⁴ s

Calculation:

```
ΔΦ = 3.14×10¹⁰ × 8.87×10⁻³ × 10⁻³ / (6.371×10⁶)² × 10⁻⁴
   = 3.14×10¹⁰ × 2.19×10⁻¹⁹ × 10⁻⁴
   = 6.87×10⁻¹³ rad
```

**This is ~10⁻¹³ rad, roughly 12 orders of magnitude below the typical dephasing noise of ~1 rad.**

### Numerical Example: Optical Clock

Parameters:
- ω/(2π) = 429 THz → ω = 2.69×10¹⁵ rad/s
- Δh = 1 m
- t = 1 s

Calculation:

```
ΔΦ = 2.69×10¹⁵ × 8.87×10⁻³ × 1 / (6.371×10⁶)² × 1
   = 2.69×10¹⁵ × 2.19×10⁻¹⁶
   = 0.589 rad
```

**This is ~0.6 rad, well above the optical clock noise floor of ~10⁻³ rad.**

→ **See Figure F1** for phase drift vs. height across platforms.

---

## 2.4 Segment-Coherent Zones

To maintain a fixed relative phase error ε, we define the **segment-coherent zone width**:

### Derivation

Require |ΔΦ| ≤ ε:

```
ω × r_s × Δh / R² × t ≤ ε
```

Solving for Δh:

```
Δh ≤ ε × R² / (ω × r_s × t)
```

Defining z(ε) independent of ω and t (normalized to reference values):

```
z(ε) = 4ε × R² / r_s
```

### Physical Interpretation

| Tolerance ε | Zone Width z(ε) | Application |
|-------------|-----------------|-------------|
| 10⁻¹⁸ | 183 μm | QEC threshold |
| 10⁻¹⁵ | 183 mm | High-fidelity gates |
| 10⁻¹² | 183 m | Standard gates |

### Design Implication

- Transmon qubits on a **planar chip** lie within one zone (μm variations)
- **Stacked chiplets** (mm separation) span multiple zones → require compensation
- **Remote nodes** (m separation) definitely require compensation

→ **See Figure F5** for zone width as function of tolerance.

---

## 2.5 Comparison with General Relativity

In the weak field, SSZ and GR give identical predictions to first order:

| Quantity | GR Formula | SSZ Formula | Difference |
|----------|------------|-------------|------------|
| Redshift | Δν/ν = gh/c² | Δν/ν = r_s·h/(2R²) | < 10⁻¹⁵ |
| Time dilation | D = √(1-r_s/r) | D = 1/(1+Ξ) | < 10⁻¹⁵ |
| Phase drift | ΔΦ = ω·gh·t/c² | ΔΦ = ω·r_s·Δh·t/R² | Equivalent |

The SSZ formulation uses segment density as the fundamental variable, which:
- Provides a natural framework for quantum phase calculations
- Extends to strong fields without singularities
- Connects to discrete spacetime concepts

→ **See Figure F4** for SSZ vs GR comparison across field strengths.
