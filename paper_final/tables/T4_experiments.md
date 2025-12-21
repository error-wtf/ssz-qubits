# Table 4: Experimental Configurations

| Experiment | Δh Range | Platform | Duration | Expected Bound | Key Controls |
|------------|----------|----------|----------|----------------|--------------|
| **Chip Tilt** | 0-10 mm | Transmon | 100 μs | α < 9×10⁻³ rad/m | Vibration isolation, thermal sensors |
| **Remote Entanglement** | 10-100 cm | Photon-mediated | 1-10 μs | α < 10⁻² rad/m | LO synchronization, path length |
| **3D Chiplet Stack** | 1-5 mm | Stacked transmons | 100 μs | α < 5×10⁻³ rad/m | Cross-layer calibration |
| **Optical Clock Link** | 1-10 m | Sr/Yb clocks | 1-10 s | Detection possible | Fiber noise cancellation |
| **Satellite QKD** | 100+ km | Photon pairs | μs-ms | Strong signal | Atmospheric compensation |

## Protocol Steps

### Chip Tilt Experiment
1. Mount chip on precision tilt stage (±0.01°)
2. Vary angle θ: Δh = L × sin(θ), L = chip length
3. At each angle: 1000× Ramsey sequences
4. Fit slope α = ∂ΔΦ/∂Δh
5. Compare to α_SSZ = ω × r_s / R²

### Remote Entanglement
1. Generate Bell state |Φ⁺⟩ between cryostats
2. WITHOUT compensation: measure phase drift
3. WITH compensation: apply Φ_corr = -ω(r_s·Δh/R²)t
4. Compare fidelities F_with vs F_without
5. Randomize run order to avoid slow drifts

### 3D Chiplet Stack
1. Fabricate 2-3 qubit dies with vertical separation
2. Characterize cross-layer CZ gates
3. Sweep gate duration, measure phase accumulation
4. Add thermal sensors at each layer
5. Fit height-dependent slope

## Usage in DOCX
```python
# 6 columns, first column bold
# Add sub-tables for each protocol
```
