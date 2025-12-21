# 1.3 Claim Boundaries — Extended Version

The predictions of SSZ theory span a wide spectrum of experimental conditions, from current superconducting quantum processors to future satellite-based quantum networks. To avoid misunderstandings and define clear falsification criteria, we classify our claims into three distinct regimes. This classification is based on the ratio between the predicted SSZ signal and the noise level of the respective experimental platform.

---

## 1.3.1 Bounded Regime: Today's Superconducting Qubits

The first regime, most relevant for current quantum computing research, encompasses superconducting transmon qubits as used in IBM, Google, and Rigetti systems. In these systems, typical chip dimensions are in the millimeter range, and coherence times reach values of 50–200 microseconds.

For a representative example, consider two qubits on the same chip with a height difference of Δh = 1 mm. The transmon frequency is typically ω/(2π) = 5 GHz, corresponding to an angular frequency of ω = 3.14 × 10¹⁰ rad/s. For a characteristic gate duration of t = 100 μs, the SSZ-induced phase drift is:

```
ΔΦ = ω × r_s × Δh / R² × t
   = 3.14×10¹⁰ × 8.87×10⁻³ × 10⁻³ / (6.371×10⁶)² × 10⁻⁴
   = 6.87 × 10⁻¹³ rad
```

This value lies **twelve orders of magnitude** below the typical dephasing noise of about 1 rad, which is limited by T₂ processes. The physical interpretation is clear: with current technology, the SSZ effect in superconducting systems is fundamentally undetectable.

**Why the mm scale is chosen:** The choice of Δh ~ 1 mm corresponds to typical height variations on a planar qubit chip. Even with intentional chip tilting (tilt experiments), achievable height differences are limited to a few millimeters, since larger angles would lead to unacceptable thermal gradients.

**Interpretation of null results:** An experiment in this regime that detects no height-dependent phase drift is fully consistent with SSZ predictions. Such a null result does not falsify the theory but rather confirms the quantitative prediction that the effect is undetectable at these scales. Instead, it provides an upper bound on any anomalous couplings that might exceed the SSZ prediction.

**Relevant experimental platforms:**
- IBM Quantum: Transmon qubits with T₂ ≈ 100–200 μs
- Google Sycamore: Transmon architecture with comparable parameters
- Rigetti: Superconducting processors with similar characteristics
- IQM: European transmon development

---

## 1.3.2 Detection Regime: Optical Atomic Clocks

The second regime opens the possibility of direct detection of the SSZ effect. It is based on optical atomic clocks, whose extraordinary frequency stability and long coherence times enable dramatically increased sensitivity.

The key factor is the frequency ratio: optical transitions in strontium or ytterbium clocks operate at ω/(2π) ≈ 429 THz, corresponding to a factor of about 10⁵ compared to microwave transmons. Since SSZ phase drift scales linearly with frequency, this increase leads to a proportionally amplified signal.

For a typical optical clock configuration with Δh = 1 m and a measurement time of t = 1 s:

```
ΔΦ = ω × r_s × Δh / R² × t
   = 2.69×10¹⁵ × 8.87×10⁻³ × 1 / (6.371×10⁶)² × 1
   = 0.59 rad
```

With a noise level of optical clocks of σ ≈ 10⁻³ rad, a signal-to-noise ratio of SNR ≈ 590 results—more than sufficient for unambiguous detection.

**Historical Validation:** The fundamental physics of this regime has already been experimentally confirmed. Chou et al. demonstrated gravitational time dilation at NIST in 2010 at a height difference of only 33 cm. More recent experiments at Tokyo Skytree (Bothwell et al., 2022) with Δh = 450 m achieved even higher precision. These experiments confirm the equivalence of SSZ and general relativity in the weak field—they measure exactly the effect that SSZ predicts.

**The Gold Standard for SSZ Validation:** Optical atomic clocks provide the ideal framework for a definitive test of the SSZ compensation hypothesis. The protocol would proceed as follows:

1. Synchronize two clocks at the same height (reference measurement)
2. Vertically displace one clock by Δh
3. Measure phase drift over time T without compensation (expected drift: ~0.6 rad/s per meter)
4. Apply compensation phase Φ_corr = -ω × r_s × Δh / R² × t
5. Verify that the drift returns to zero

The reversal of drift under compensation is the decisive discriminator that distinguishes SSZ from all known confounding sources.

**Technological Maturity:** Unlike many fundamental physics experiments, this protocol requires no new technology. Optical clocks with the required precision already exist in several laboratories worldwide (NIST, PTB, RIKEN, SYRTE).

---

## 1.3.3 Future Regime: Advanced Quantum Networks

The third regime looks toward a future in which SSZ is no longer merely a curiosity of fundamental physics but becomes a practical engineering constraint. This regime is characterized by large height differences and high coherence requirements.

**Satellite-Based Quantum Communication:** Quantum Key Distribution (QKD) between ground stations and satellites operates at height differences of Δh ~ 400 km (Low Earth Orbit) to ~36,000 km (geosynchronous). At optical frequencies and second-long protocols, SSZ phase drifts would reach hundreds to thousands of complete oscillations per second:

```
For Δh = 400 km, ω = 2π × 429 THz:
ΔΦ = 2.69×10¹⁵ × 8.87×10⁻³ × 4×10⁵ / (6.371×10⁶)² × 1
   ≈ 2.4 × 10⁵ rad/s ≈ 38,000 × 2π/s
```

This means that the relative phase between entangled photons on the ground and in orbit would oscillate at approximately 38 kHz. Without precise compensation, any phase-sensitive quantum operation would be impossible.

**Intercontinental Quantum Networks:** Ground stations in different geographic regions are located at different gravitational potentials due to latitude, elevation above sea level, and local mass anomalies. For a quantum network requiring nanosecond synchronization over continental distances, these differences become significant.

**SSZ as Engineering Constraint:** In this regime, the perspective shifts: SSZ is no longer an effect to be detected but a known boundary condition that must be considered in system design. Analogies can be found in today's GPS technology, where relativistic corrections (both special and general relativity) are routinely programmed into the clocks.

**Protocol Implications:**
- Height metadata must be exchanged between network nodes
- Real-time compensation algorithms are required
- SSZ-aware error correction protocols must be developed
- Calibration procedures must incorporate gravitational potential differences

**Timeline:** The development of this regime depends on the progress of quantum network technology. First satellite-based QKD experiments (Micius/China) have demonstrated feasibility. SSZ-relevant applications are expected to become practically relevant in the 2030–2040 timeframe.

---

## Summary of Regimes

| Regime | Δh | ΔΦ | SNR | Status | Interpretation |
|--------|-----|-----|-----|--------|----------------|
| Bounded | ~mm | ~10⁻¹³ rad | 10⁻¹² | Today | Null result = SSZ-consistent |
| Detection | ~m | ~0.6 rad | ~600 | Possible today | Detection and compensation test |
| Future | ~km | ~10⁵ rad/s | ∞ | 2030+ | Engineering constraint |

**We explicitly emphasize:** Claims that SSZ is detectable in current mm-scale devices are not supported by our analysis. Simulations showing visible drifts use didactic scaling for visualization and do not represent physical predictions.

---

© 2025 Carmen Wrede & Lino Casu
