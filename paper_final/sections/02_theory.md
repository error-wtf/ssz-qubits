# 2. Theory: Deriving the SSZ Phase Drift

The theoretical foundation of gravitational phase coupling rests on the well-established physics of general relativity, recast in a form that is particularly suited to analyzing quantum coherence. This section develops the mathematical framework from first principles, deriving the key formulas that govern the accumulation of phase differences between quantum systems at different gravitational potentials.

The central insight of the SSZ approach is that gravitational time dilation can be understood through the concept of segment density, which quantifies how spacetime is structured at different radial distances from a massive body. This perspective provides not only computational convenience but also conceptual clarity, particularly when extending the theory to strong gravitational fields where the standard perturbative expansions of general relativity become unwieldy.

## 2.1 Segment Density and Time Dilation

In a weak gravitational field, the metric can be expanded in powers of the gravitational potential. The SSZ framework introduces the **segment density** as the fundamental quantity that governs time dilation. This quantity, denoted Ξ (Xi), represents the fractional difference in the rate of time flow compared to an observer at spatial infinity. The physical interpretation is straightforward: a higher segment density corresponds to slower local time, which is the familiar gravitational time dilation predicted by general relativity.

### Definition (Weak Field, r >> r_s)

```
Ξ(r) = r_s / (2r)
```

where:
- r_s = 2GM/c² is the Schwarzschild radius
- r is the radial distance from Earth's center
- For Earth: r_s ≈ 8.87 mm

It is important to clarify the ontological status of the segment density Ξ. In the weak-field regime that characterizes all terrestrial experiments, Ξ is functionally equivalent to the standard general-relativistic gravitational potential rescaled by a factor of 1/(2c²). It does not represent a new force, an additional field, or a modification of gravity. Rather, Ξ provides a convenient reparametrization of the metric that makes phase-drift calculations particularly transparent. The SSZ formulation becomes physically distinct from standard general relativity only in the strong-field regime (r < 100·r_s), where the segment density saturates rather than diverging. For all practical quantum computing applications on Earth, where r/r_s ~ 10⁹, the SSZ framework is merely a useful reframing of established physics, not a claim of new weak-field phenomena.

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

Having established the segment density at a single point, we now consider the crucial quantity for quantum coherence: the difference in time dilation between two nearby locations. When two qubits are placed at slightly different heights in a gravitational field, they experience different rates of time flow. This difference, though extraordinarily small for laboratory-scale separations, accumulates over time and manifests as a relative phase shift between the quantum states.

The differential time dilation between two heights h and h+Δh is found by Taylor expansion. This approach is valid because the height differences of interest (millimetres to metres) are vastly smaller than Earth's radius (approximately 6,371 kilometres), allowing us to treat the gravitational field as approximately uniform over the relevant length scales:

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

The connection between time dilation and quantum phase is direct and fundamental. A quantum oscillator with angular frequency ω accumulates phase at a rate proportional to the local flow of time. If two oscillators experience different time dilation factors, their phases will diverge in a deterministic and predictable manner. This is not a source of random noise or decoherence in the conventional sense; rather, it is a systematic drift that can, in principle, be calculated and compensated.

The connection between proper time and quantum phase follows directly from the Schrödinger equation. For a quantum system with energy E, the phase accumulated over proper time τ is Φ = Eτ/ℏ = ωτ, where ω = E/ℏ is the angular frequency. The key insight is that quantum phase accumulation depends on proper time, not coordinate time. When a qubit oscillates at frequency ω in its local rest frame, the phase it accumulates is ω multiplied by the proper time experienced at that location. Since proper time is related to coordinate time by dτ = D(h)dt, where D(h) is the time dilation factor, two qubits at different gravitational potentials will accumulate different phases even if they evolve for the same coordinate duration. This effect is not a modification of quantum mechanics but rather the standard application of quantum evolution in curved spacetime.

A central motivation for emphasizing φ in the SSZ strong-field extension originates from this phase representation. Euler's formula provides the natural language for quantum phase factors: the state evolution is expressed as e^(iΦ), where Φ is the accumulated proper-time phase. This makes the question of which structural constants yield stable, cross-regime behavior of Φ particularly relevant when extending GR-consistent weak-field behavior into strong-field closures. Within the SSZ validation suite, φ-based closures consistently preserve weak-field GR agreement while improving strong-field fit stability and cross-observable consistency compared to generic alternatives. Thus, the role of φ is not introduced as an aesthetic add-on, but as a structurally and empirically robust choice that emerged from the requirement of stable phase scaling across gravitational regimes.

**Clarification on Causal Direction:** Euler's formula does not imply φ; rather, it motivates focusing on phase stability as the primary selection criterion. The connection is methodological, not derivational: because quantum evolution is fundamentally expressed through phase factors e^(iΦ), the question "which closure preserves phase stability across regimes?" becomes the natural selection principle. The answer—that φ-based saturation outperforms alternatives—is an empirical finding within the SSZ validation framework, not a logical consequence of Euler's identity.

Consider two qubits at heights h and h+Δh with angular frequency ω. The phase accumulated by each qubit depends on the proper time experienced at its location:

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

A natural question arises from the preceding analysis: over what spatial extent can quantum operations be performed without significant gravitational phase errors? This question leads to the concept of segment-coherent zones, which define the maximum height separation between qubits that can be tolerated for a given phase error budget. The answer depends on the acceptable error tolerance, which varies according to the application. For quantum error correction, tolerances of 10⁻¹⁸ or smaller may be required, while for standard gate operations, tolerances of 10⁻¹² might suffice.

To maintain a fixed relative phase error ε, we define the **segment-coherent zone width** as the maximum height difference that keeps the accumulated phase drift below the threshold:

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

The apparent independence of z(ε) from frequency ω and time t deserves clarification. The full expression for the maximum tolerable height difference is Δh_max = ε × R² / (ω × r_s × t), which does depend on both parameters. The simplified zone width z(ε) = 4ε × R² / r_s is obtained by normalizing to reference values (ω_ref, t_ref) such that ω_ref × t_ref = 4 in natural units. This normalized quantity provides a purely geometric measure of spatial tolerance: given a phase error budget ε, what is the characteristic length scale over which the gravitational potential varies enough to exhaust that budget? The answer depends on Earth's geometry (R and r_s) and the chosen tolerance, but not on the specific quantum system. For any particular experiment, the actual constraint on Δh must be computed using the full formula with the relevant ω and t.

**Clarification on the Role of z(ε):** The normalized zone width z(ε) is introduced solely as a geometric design metric; it does not represent a new observable but provides platform-independent intuition. The practical quantity remains Δh_max, which depends on the specific quantum system (ω) and operation time (t). The zone width z(ε) answers the question "how does the gravitational landscape constrain quantum coherence at a given tolerance?" in a form that facilitates comparison across different experimental platforms without repeatedly specifying ω and t.

### Physical Interpretation

| Tolerance ε | Zone Width z(ε) | Application |
|-------------|-----------------|-------------|
| 10⁻²⁰ | 183 μm | Extreme precision |
| 10⁻¹⁸ | 18.3 mm | QEC threshold |
| 10⁻¹⁵ | 18.3 m | High-fidelity gates |
| 10⁻¹² | 18.3 km | Standard gates |

### Design Implication

- Transmon qubits on a **planar chip** lie within one zone (μm variations)
- **Stacked chiplets** (mm separation) span multiple zones → require compensation
- **Remote nodes** (m separation) definitely require compensation

→ **See Figure F5** for zone width as function of tolerance.

---

## 2.5 Comparison with General Relativity

A critical question for any theoretical framework is its relationship to established physics. The SSZ formulation is not intended as a replacement for general relativity but rather as a reformulation that is particularly convenient for quantum applications. In the weak-field regime that characterizes all terrestrial experiments and most astrophysical observations, the SSZ predictions are mathematically equivalent to those of standard general relativity. The differences between the two frameworks become significant only in the strong-field regime near compact objects such as neutron stars or black holes.

In the weak field, SSZ and GR give identical predictions to first order. This equivalence is not accidental but follows directly from the construction of the segment density function, which was designed to reproduce the Schwarzschild metric in the appropriate limit:

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
