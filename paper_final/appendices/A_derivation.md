# Appendix A: Full Mathematical Derivation

## A.1 Schwarzschild Metric and Gravitational Potential

Starting from the Schwarzschild metric in isotropic coordinates:

```
ds² = -(1 - r_s/r)dt² + (1 + r_s/r)(dr² + r²dΩ²)
```

where:
- r_s = 2GM/c² is the Schwarzschild radius
- For Earth: r_s = 2 × 6.674×10⁻¹¹ × 5.972×10²⁴ / (2.998×10⁸)² = 8.87 mm

The gravitational potential is:
```
φ(r) = -GM/r = -r_s c² / (2r)
```

## A.2 Proper Time and Time Dilation

For a stationary clock at radius r, proper time increments as:

```
dτ = √(1 + 2φ(r)/c²) dt ≈ (1 + φ(r)/c²) dt
```

Substituting φ(r):
```
dτ = (1 - r_s/(2r)) dt
```

## A.3 SSZ Segment Density Definition

The SSZ framework introduces segment density Ξ(r):

**Weak field (r >> r_s):**
```
Ξ(r) = r_s / (2r)
```

**Strong field (r ~ r_s):**
```
Ξ(r) = 1 - exp(-φ × r / r_s)
```
where φ = 1.618... is the golden ratio.

## A.4 SSZ Time Dilation Factor

The time dilation factor D(r) is defined as:
```
D(r) = 1 / (1 + Ξ(r))
```

**Weak field expansion:**
```
D(r) = 1 / (1 + r_s/(2r))
     = 2r / (2r + r_s)
     ≈ 1 - r_s/(2r) + O((r_s/r)²)
```

This matches GR to first order in r_s/r.

## A.5 Differential Time Dilation

For two heights h and h + Δh at Earth's surface (h << R):

```
D(h) = 1 / (1 + r_s/(2(R+h)))

dD/dh = d/dh [1 / (1 + r_s/(2(R+h)))]
      = r_s / (2(R+h)²) × 1/(1 + r_s/(2(R+h)))²
      ≈ r_s / (2R²)  [for h << R and r_s << R]
```

Therefore:
```
ΔD = D(h + Δh) - D(h) ≈ (dD/dh) × Δh = r_s × Δh / (2R²)
```

**Numerical verification:**
```
ΔD = 8.87×10⁻³ × 1×10⁻³ / (2 × (6.371×10⁶)²)
   = 8.87×10⁻⁶ / (8.118×10¹³)
   = 1.093×10⁻¹⁹
```

## A.6 Phase Drift Formula

A qubit at angular frequency ω accumulates phase:
```
Φ(t) = ω × τ = ω × D(h) × t
```

The differential phase between two qubits at h and h + Δh:
```
ΔΦ(t) = ω × (D(h+Δh) - D(h)) × t
      = ω × ΔD × t
      = ω × r_s × Δh / R² × t
```

**Numerical example (5 GHz transmon, 1 mm, 100 μs):**
```
ΔΦ = 2π × 5×10⁹ × 8.87×10⁻³ × 1×10⁻³ / (6.371×10⁶)² × 1×10⁻⁴
   = 3.14×10¹⁰ × 2.186×10⁻¹⁶ × 10⁻⁴
   = 6.87×10⁻¹³ rad
```

## A.7 Segment-Coherent Zone Width

To maintain relative phase error ≤ ε:
```
|ΔΦ| ≤ ε
ω × r_s × Δh / R² × t ≤ ε
```

For a given ω and t, the maximum Δh is:
```
Δh_max = ε × R² / (ω × r_s × t)
```

Defining z(ε) as the zone width independent of ω and t:
```
z(ε) = 4ε × R² / r_s
```

The factor 4 comes from normalizing to a reference system.

**Numerical example (ε = 10⁻¹⁸):**
```
z = 4 × 10⁻¹⁸ × (6.371×10⁶)² / 8.87×10⁻³
  = 4 × 10⁻¹⁸ × 4.059×10¹³ / 8.87×10⁻³
  = 1.83×10⁻⁴ m = 183 μm
```

## A.8 Unit Verification

| Quantity | Formula | Units |
|----------|---------|-------|
| Ξ | r_s / (2r) | m / m = dimensionless ✓ |
| D | 1 / (1 + Ξ) | dimensionless ✓ |
| ΔD | r_s × Δh / R² | m × m / m² = dimensionless ✓ |
| ΔΦ | ω × ΔD × t | rad/s × 1 × s = rad ✓ |
| z(ε) | ε × R² / r_s | 1 × m² / m = m ✓ |
