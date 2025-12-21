# Table 2: Scaling Signatures and Confound Discrimination

| Effect | Height Scaling | Frequency Scaling | Time Scaling | Compensation Reversal |
|--------|----------------|-------------------|--------------|----------------------|
| **SSZ drift** | constant slope ∂ΔΦ/∂Δh | ∝ ω | ∝ t | **Yes** |
| Thermal gradient | variable, environment-dep. | often weak | ∝ t | No |
| LO phase noise | none | white noise (∝√f) | ∝ √t | No |
| Vibration/tilt | step-like, impulse | frequency-indep. | impulse-like | No |
| Magnetic field drift | position-dependent | weak coupling | ∝ t | No |
| Charge noise | random, local | 1/f spectrum | ∝ √t | No |

## Key Discriminators

1. **Height scaling**: SSZ predicts constant slope α_SSZ = ω·r_s/R²
2. **Frequency scaling**: SSZ ∝ ω (linear), noise typically ∝ f⁰ or 1/f
3. **Compensation**: Only SSZ reverses under Φ_corr = -ω(r_s·Δh/R²)t

## Usage in DOCX
```python
# 6 columns, header row bold
# "Yes" in last column: green highlight
# "No" entries: red highlight
```
