# 5. Entanglement and Phase Preservation

## 5.1 SSZ Effect on Entangled States

Entanglement distribution across separated nodes is sensitive to any relative phase drift. SSZ predicts an additional, **deterministic** contribution to the accumulated phase.

### Bell State Evolution

Consider a Bell state |Φ⁺⟩ prepared between qubits at heights h₁ and h₂:

```
|Ψ(0)⟩ = (|00⟩ + |11⟩) / √2
```

Under SSZ-induced phase drift, the state evolves as:

```
|Ψ(t)⟩ = (|00⟩ + e^(iΔΦ(t))|11⟩) / √2
```

where:
```
ΔΦ(t) = ω × r_s × (h₂ - h₁) / R² × t
```

### Key Distinction from Decoherence

| Property | Random Dephasing | SSZ Drift |
|----------|-----------------|-----------|
| Nature | Stochastic | Deterministic |
| Predictability | None | Exact |
| Time scaling | √t (diffusive) | t (linear) |
| Compensation | Impossible | Possible |
| Entanglement | Destroyed | Rotated |

**Critical insight**: SSZ does NOT destroy entanglement—it rotates the relative phase. The state remains maximally entangled but in a different Bell basis state.

---

## 5.2 Entanglement Fidelity

The fidelity of the evolved state with respect to the target |Φ⁺⟩:

```
F(t) = |⟨Φ⁺|Ψ(t)⟩|² = (1 + cos(ΔΦ(t))) / 2
```

### Without Compensation

For ΔΦ = π (half-oscillation):
```
F = (1 + cos(π)) / 2 = 0
```

The state has rotated to |Φ⁻⟩ = (|00⟩ - |11⟩)/√2.

For ΔΦ = 2π (full oscillation):
```
F = (1 + cos(2π)) / 2 = 1
```

The state returns to |Φ⁺⟩.

### With Compensation

Apply correction phase Φ_corr = -ΔΦ:

```
|Ψ_corr(t)⟩ = (|00⟩ + e^(i(ΔΦ - ΔΦ))|11⟩) / √2 = |Φ⁺⟩
F = 1  (perfect fidelity)
```

**Compensation fully restores the original Bell state.**

---

## 5.3 Platform-Specific Analysis

### Transmon Qubits (Bounded Regime)

Parameters:
- ω = 2π × 5 GHz
- Δh = 1 mm
- t = 100 μs

Phase drift:
```
ΔΦ = 6.87 × 10⁻¹³ rad
```

Fidelity loss:
```
1 - F ≈ ΔΦ²/4 = 1.2 × 10⁻²⁵
```

**Conclusion**: SSZ-induced fidelity loss is utterly negligible (25 orders of magnitude below any measurable effect).

### Optical Clock Qubits (Detection Regime)

Parameters:
- ω = 2π × 429 THz
- Δh = 1 m
- t = 1 s

Phase drift:
```
ΔΦ = 0.59 rad
```

Fidelity:
```
F = (1 + cos(0.59)) / 2 = 0.915
```

**Conclusion**: Without compensation, 8.5% fidelity loss per second. With compensation, fidelity restored to unity.

### Quantum Networks (Future Regime)

For long-baseline quantum networks:
- Δh = 100 m
- t = 1 s

Phase drift:
```
ΔΦ = 59 rad ≈ 9.4 × 2π
```

**Conclusion**: Multiple full rotations per second. Compensation is mandatory for any network operation.

---

## 5.4 Entanglement Lifetime Analysis

Define τ_SSZ as the time for ΔΦ to reach π (complete phase flip):

```
τ_SSZ = π × R² / (ω × r_s × Δh)
```

| Platform | Δh | τ_SSZ | Comparison to T₂ |
|----------|-----|-------|-----------------|
| Transmon | 1 mm | 4.6 × 10⁸ s | >> T₂ (~100 μs) |
| Transmon | 10 mm | 4.6 × 10⁷ s | >> T₂ |
| Optical | 1 m | 5.3 s | ~ T₂ (~10 s) |
| Optical | 10 m | 0.53 s | < T₂ |

**Interpretation**: 
- For transmons, SSZ lifetime vastly exceeds coherence time → no impact
- For optical clocks at m-scale, SSZ lifetime comparable to coherence → requires compensation

---

## 5.5 Multi-Qubit Entanglement

For GHZ states across N nodes at different heights:

```
|GHZ⟩ = (|00...0⟩ + |11...1⟩) / √2
```

Each qubit accumulates phase relative to reference:

```
|Ψ(t)⟩ = (|00...0⟩ + exp(i Σⱼ ΔΦⱼ)|11...1⟩) / √2
```

Total phase:
```
Φ_total = ω × r_s / R² × t × Σⱼ (hⱼ - h_ref)
```

### Compensation Strategy

1. Designate lowest qubit as reference (h_ref)
2. For each qubit j, compute Δhⱼ = hⱼ - h_ref
3. Apply local Z rotations: Φ_corr,j = -ω × r_s × Δhⱼ / R² × t
4. Net effect: all phases aligned

This scales linearly with N and requires only local operations.

---

## 5.6 Didactic Simulations

Paper B includes simulations demonstrating compensation effectiveness. **These use didactic scaling (10⁸× amplification) for visualization.**

### What the simulations show:
- Fidelity oscillates without compensation (qualitatively correct)
- Fidelity remains stable with compensation (qualitatively correct)
- Frequency of oscillation matches ω × ΔD (qualitatively correct)

### What the simulations do NOT show:
- Actual magnitude of physical effect (10⁻¹³ rad, not visible)
- Detectability in current systems (not detectable)
- Quantitative experimental predictions (use real values instead)

→ **See Appendix B** for didactic scaling definition.

---

## 5.7 Implications for Quantum Networks

### Near-term (Bounded Regime)
- Intra-chip entanglement: no SSZ concern
- Short-range links (< 1 m): negligible SSZ
- No action required

### Medium-term (Detection Regime)
- Optical clock networks: SSZ measurable
- Compensation protocol needed for high-fidelity links
- Opportunity for fundamental physics tests

### Long-term (Future Regime)
- Satellite QKD: large Δh (~400 km)
- Intercontinental links: varying gravitational potential
- SSZ becomes engineering constraint
- SSZ-aware network protocols required
