# Table 3: Platform Comparison - Expected Phase Drifts

| Platform | Frequency ω/(2π) | Height Δh | Time t | Predicted ΔΦ | Noise Floor | Detectability |
|----------|------------------|-----------|--------|--------------|-------------|---------------|
| Transmon qubit | 5 GHz | 1 mm | 100 μs | 6.9 × 10⁻¹³ rad | ~1 rad | **Bounded** |
| Transmon qubit | 5 GHz | 10 mm | 100 μs | 6.9 × 10⁻¹² rad | ~1 rad | Bounded |
| Trapped ion | 10 MHz | 1 mm | 1 ms | 8.8 × 10⁻¹² rad | ~0.1 rad | Bounded |
| NV center | 2.87 GHz | 1 mm | 1 ms | 4.0 × 10⁻¹² rad | ~0.01 rad | Bounded |
| Optical clock | 429 THz | 1 m | 1 s | 0.59 rad | ~10⁻³ rad | **Detectable** |
| Optical clock | 429 THz | 10 cm | 1 s | 0.059 rad | ~10⁻³ rad | Detectable |
| Future optical qubit | 100 THz | 1 mm | 10 s | 1.4 × 10⁻⁴ rad | ~10⁻⁵ rad | Future |

## Calculation Formula
```
ΔΦ = ω × (r_s × Δh / R²) × t
   = ω × (8.87e-3 × Δh / (6.371e6)²) × t
   = ω × 2.186e-16 × Δh × t
```

## Key Insight
- **12 orders of magnitude gap** between transmon signal and noise
- Optical clocks: signal-to-noise > 100 at 1 m separation
- Detection threshold: ΔΦ > 10× noise floor

## Usage in DOCX
```python
# 7 columns, alternating row colors
# "Bounded" = orange, "Detectable" = green, "Future" = blue
```
