# Appendix B: Didactic Scaling Definition

## B.1 Purpose

Didactic scaling is a **visualization technique** used to make extremely small SSZ effects visible in simulations and plots. It is **NOT a physical prediction** and must always be explicitly labeled.

## B.2 The Problem

The SSZ phase drift for realistic transmon experiments is:
```
ΔΦ_physical ≈ 10⁻¹³ rad (for Δh = 1 mm, t = 100 μs)
```

This is:
- 12 orders of magnitude below the noise floor (~1 rad)
- Invisible on any linear or log plot with practical axis ranges
- Impossible to distinguish from numerical noise in simulations

## B.3 Didactic Scaling Factor

To visualize the **qualitative behavior** of SSZ effects, we apply a scaling factor S:
```
ΔΦ_didactic = S × ΔΦ_physical
```

Typical values:
- S = 10⁸ (shows ~10⁻⁵ rad effects as visible)
- S = 10¹² (amplifies to order 0.1 rad)
- S = 10¹⁵ (makes ~1 rad visible)

## B.4 What Didactic Scaling Shows

| Aspect | Valid for Didactic | NOT Valid |
|--------|-------------------|-----------|
| Qualitative scaling with Δh | ✓ | |
| Linear time accumulation | ✓ | |
| Frequency proportionality | ✓ | |
| Compensation reversal | ✓ | |
| Actual magnitude | | ✗ |
| Detectability claims | | ✗ |
| Noise comparison | | ✗ |

## B.5 Mandatory Labeling

All didactically scaled results MUST include:

1. **Plot title annotation:**
   ```
   "Didactic visualization (scaled by 10^8 for visibility)"
   ```

2. **Caption text:**
   ```
   "Note: Amplified by factor S = 10^8 to visualize qualitative behavior.
    Actual physical signal is 10^-13 rad, far below measurement threshold."
   ```

3. **Code comment:**
   ```python
   # DIDACTIC SCALING: Multiply by 1e8 for visualization ONLY
   # Physical prediction: ΔΦ ≈ 6.87e-13 rad (undetectable)
   ```

## B.6 Example: Paper B Simulations

Paper B includes simulations showing entanglement fidelity vs. time with and without compensation. These use S = 10⁸:

**Correct interpretation:**
- The shape of the fidelity curve is correct
- Compensation restores fidelity (qualitatively correct)
- The oscillation frequency is exaggerated

**Incorrect interpretation:**
- ❌ "SSZ causes visible fidelity loss in 100 μs"
- ❌ "The effect is measurable in current systems"
- ❌ "This simulation predicts experimental outcomes"

## B.7 When Didactic Scaling is Appropriate

| Context | Didactic OK? |
|---------|-------------|
| Educational presentation | ✓ with label |
| Methodology demonstration | ✓ with label |
| Algorithm testing | ✓ with label |
| Physical prediction | ✗ NEVER |
| Experimental proposal | ✗ NEVER |
| Journal figure (main) | ✗ Use real values |
| Journal figure (supplementary) | ✓ with explicit note |

## B.8 Alternative: Log-Scale Plotting

Instead of didactic scaling, consider log-scale plots that show the true magnitude:
```python
ax.set_yscale('log')
ax.axhline(1e-13, label='SSZ signal')
ax.axhline(1, label='Noise floor')
# Shows 12 OoM gap honestly
```

## B.9 Summary

**Didactic scaling is a teaching tool, not a physical model.**

- Always label with explicit scaling factor
- Never claim detectability based on scaled results
- Use for qualitative demonstrations only
- Prefer honest log-scale plots for quantitative analysis
