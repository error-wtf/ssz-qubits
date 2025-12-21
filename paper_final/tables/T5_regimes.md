# Table 5: Claim Taxonomy - Three Regimes

| Regime | Platform | Δh | t | ΔΦ_SSZ | Noise | Outcome | Claim |
|--------|----------|-----|---|--------|-------|---------|-------|
| **Bounded** | Transmon | 1 mm | 100 μs | 10⁻¹³ rad | 1 rad | Null result | Upper bound on anomalous coupling |
| **Bounded** | Trapped ion | 1 mm | 1 ms | 10⁻¹¹ rad | 0.1 rad | Null result | Upper bound |
| **Detection** | Optical clock | 1 m | 1 s | 0.6 rad | 10⁻³ rad | Detectable | SSZ/GR confirmation |
| **Detection** | Optical clock | 10 cm | 10 s | 0.6 rad | 10⁻³ rad | Detectable | Compensation test |
| **Future** | Optical qubit | 1 mm | 10 s | 10⁻⁴ rad | 10⁻⁵ rad | Possible | Engineering consideration |
| **Future** | Quantum network | 100 m | 1 s | 60 rad | 0.1 rad | Dominant | Compensation required |

## Regime Definitions

### Bounded Regime (Today)
- **Condition**: ΔΦ_SSZ << Noise floor (≥ 10⁶ gap)
- **Platforms**: Superconducting qubits, trapped ions, NV centers
- **Interpretation**: Null result is SSZ-consistent
- **Value**: Places upper bound on unknown physics

### Detection Regime (Near-term)
- **Condition**: ΔΦ_SSZ > 10× Noise floor
- **Platforms**: Optical atomic clocks, clock networks
- **Interpretation**: Direct measurement possible
- **Value**: Tests SSZ = GR equivalence, compensation protocol

### Future Regime (5-10 years)
- **Condition**: ΔΦ_SSZ comparable to error budget
- **Platforms**: High-coherence optical qubits, satellite QKD
- **Interpretation**: SSZ becomes engineering constraint
- **Value**: Requires SSZ-aware design and calibration

## Forbidden Claims
- ❌ "SSZ detectable in current transmon experiments"
- ❌ "Didactic scaling represents physical prediction"
- ❌ "Null result falsifies SSZ"

## Usage in DOCX
```python
# Color code: Bounded=orange, Detection=green, Future=blue
# Add regime definition boxes after table
```
