# Appendix D: Physical Constants and Derived Values

## D.1 Fundamental Constants

| Constant | Symbol | Value | Unit | Source |
|----------|--------|-------|------|--------|
| Speed of light | c | 2.99792458 × 10⁸ | m/s | CODATA 2018 |
| Gravitational constant | G | 6.67430 × 10⁻¹¹ | m³/(kg·s²) | CODATA 2018 |
| Planck constant | ℏ | 1.054571817 × 10⁻³⁴ | J·s | CODATA 2018 |
| Golden ratio | φ | 1.6180339887498948 | - | Mathematical |
| Boltzmann constant | k_B | 1.380649 × 10⁻²³ | J/K | CODATA 2018 |

## D.2 Earth Parameters

| Parameter | Symbol | Value | Unit | Notes |
|-----------|--------|-------|------|-------|
| Earth mass | M_⊕ | 5.9722 × 10²⁴ | kg | IAU 2015 |
| Earth radius (mean) | R_⊕ | 6.371 × 10⁶ | m | WGS84 |
| Schwarzschild radius | r_s | 8.870 × 10⁻³ | m | r_s = 2GM/c² |
| Surface gravity | g | 9.80665 | m/s² | Standard |
| Surface potential | φ_0 | -6.26 × 10⁷ | J/kg | φ = -GM/R |

## D.3 SSZ Derived Values (Earth Surface)

| Quantity | Formula | Value | Unit |
|----------|---------|-------|------|
| Segment density | Ξ₀ = r_s/(2R) | 6.961 × 10⁻¹⁰ | - |
| Time dilation | D₀ = 1/(1+Ξ₀) | 0.999999999304 | - |
| Differential ΔD/Δh | r_s/R² | 2.186 × 10⁻¹⁶ | m⁻¹ |
| Phase slope (5 GHz) | ω × r_s/R² | 6.87 × 10⁻⁶ | rad/(m·s) |
| Phase slope (429 THz) | ω × r_s/R² | 0.589 | rad/(m·s) |

## D.4 Platform Parameters

### Transmon Qubit
| Parameter | Symbol | Typical Value | Range |
|-----------|--------|---------------|-------|
| Frequency | ω/(2π) | 5 GHz | 4-8 GHz |
| Coherence time T₁ | T₁ | 50-100 μs | 10-500 μs |
| Dephasing time T₂ | T₂ | 50-100 μs | 10-200 μs |
| Anharmonicity | α/(2π) | -200 MHz | -100 to -300 MHz |
| Operating temperature | T | 15 mK | 10-50 mK |

### Optical Atomic Clock (Sr/Yb)
| Parameter | Symbol | Typical Value | Range |
|-----------|--------|---------------|-------|
| Clock frequency | ω/(2π) | 429 THz (Sr) | 400-500 THz |
| Coherence time | T | 1-10 s | 0.1-100 s |
| Fractional instability | σ_y | 10⁻¹⁸ | 10⁻¹⁹-10⁻¹⁷ |
| Systematic uncertainty | Δν/ν | 10⁻¹⁸ | 10⁻¹⁹-10⁻¹⁷ |

### Trapped Ion
| Parameter | Symbol | Typical Value | Range |
|-----------|--------|---------------|-------|
| Qubit frequency | ω/(2π) | 10-100 MHz | 1 MHz-1 GHz |
| Coherence time | T₂ | 1-10 s | 0.1-100 s |
| Gate fidelity | F | 99.9% | 99%-99.99% |

## D.5 SSZ Phase Drift Values

### Reference Calculations

```python
# Constants
r_s = 8.87e-3      # m
R = 6.371e6        # m
c = 2.998e8        # m/s

# Transmon (5 GHz, 1 mm, 100 μs)
omega_t = 2 * np.pi * 5e9       # rad/s
dh_t = 1e-3                      # m
t_t = 100e-6                     # s
phi_t = omega_t * r_s * dh_t / R**2 * t_t
# Result: 6.87e-13 rad

# Optical clock (429 THz, 1 m, 1 s)
omega_o = 2 * np.pi * 429e12    # rad/s
dh_o = 1.0                       # m
t_o = 1.0                        # s
phi_o = omega_o * r_s * dh_o / R**2 * t_o
# Result: 0.589 rad
```

### Quick Reference Table

| Platform | Δh | t | ΔΦ | SNR |
|----------|-----|---|------|-----|
| Transmon | 1 mm | 100 μs | 6.9×10⁻¹³ rad | 10⁻¹² |
| Transmon | 10 mm | 100 μs | 6.9×10⁻¹² rad | 10⁻¹¹ |
| Transmon | 1 mm | 1 ms | 6.9×10⁻¹² rad | 10⁻¹¹ |
| Optical | 10 cm | 1 s | 0.059 rad | 59 |
| Optical | 1 m | 1 s | 0.589 rad | 589 |
| Optical | 1 m | 10 s | 5.89 rad | 5890 |

## D.6 Segment-Coherent Zone Widths

| Tolerance ε | z(ε) | Application |
|-------------|------|-------------|
| 10⁻²⁰ | 1.83 μm | Extreme precision |
| 10⁻¹⁸ | 183 μm | QEC threshold |
| 10⁻¹⁵ | 183 mm | High-fidelity gates |
| 10⁻¹² | 183 m | Standard gates |
| 10⁻⁹ | 183 km | Coarse sync |

## D.7 Python Reference Module

```python
"""SSZ Constants Module"""

# Fundamental
C = 2.99792458e8        # m/s
G = 6.67430e-11         # m³/(kg·s²)
HBAR = 1.054571817e-34  # J·s
PHI = 1.6180339887498948

# Earth
M_EARTH = 5.9722e24     # kg
R_EARTH = 6.371e6       # m
r_s_EARTH = 2 * G * M_EARTH / C**2  # = 8.87e-3 m

# Derived
XI_SURFACE = r_s_EARTH / (2 * R_EARTH)  # = 6.96e-10
D_SURFACE = 1 / (1 + XI_SURFACE)        # ≈ 1 - 7e-10

def phase_drift(omega, dh, t, r_s=r_s_EARTH, R=R_EARTH):
    """Calculate SSZ phase drift in radians."""
    return omega * r_s * dh / R**2 * t

def zone_width(epsilon, r_s=r_s_EARTH, R=R_EARTH):
    """Calculate segment-coherent zone width in meters."""
    return 4 * epsilon * R**2 / r_s
```
