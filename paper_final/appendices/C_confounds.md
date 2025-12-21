# Appendix C: Confound Playbook

## C.1 Overview

This appendix provides practical guidelines for discriminating SSZ effects from experimental confounds. Each confound is analyzed for its scaling behavior and mitigation strategy.

---

## C.2 Thermal Gradients

### Mechanism
Temperature differences across the chip cause:
- Frequency shifts in qubits (~1 MHz/K for transmons)
- Differential thermal expansion
- Varying dielectric losses

### Scaling Behavior
| Property | Thermal | SSZ |
|----------|---------|-----|
| Height dependence | Environment-dependent | Constant slope |
| Frequency scaling | Weak (material-dependent) | ∝ ω |
| Time scaling | ∝ t (drift) | ∝ t (linear) |
| Compensation | Does NOT reverse | Reverses |

### Mitigation
1. **Thermal sensors**: Place RTDs at multiple chip locations
2. **Controlled gradient**: Intentionally vary temperature, measure correlation
3. **Interleaving**: Alternate Δh settings rapidly to decorrelate thermal drift
4. **Shielding**: Improve thermal anchoring and radiation shielding

### Discrimination Test
```
If phase drift correlates with thermal sensor readings:
   → Thermal confound, NOT SSZ
If compensation reverses drift AND thermal sensors stable:
   → SSZ candidate
```

---

## C.3 Local Oscillator (LO) Phase Noise

### Mechanism
Phase noise on the LO used for qubit control causes:
- Random phase fluctuations on all qubits
- Correlated errors if using shared LO
- 1/f spectrum at low frequencies

### Scaling Behavior
| Property | LO Noise | SSZ |
|----------|----------|-----|
| Height dependence | None | Constant slope |
| Frequency scaling | ∝ √f (white) or 1/f | ∝ ω |
| Time scaling | ∝ √t (random walk) | ∝ t (linear) |
| Compensation | Does NOT reverse | Reverses |

### Mitigation
1. **Low phase noise sources**: Use ultra-stable oscillators
2. **Reference qubits**: Include qubits at same height as control
3. **Differential measurement**: Subtract reference phase
4. **Frequency interleaving**: Test multiple ω values

### Discrimination Test
```
If drift is random (not linear in t):
   → LO noise, NOT SSZ
If reference qubits show same drift:
   → Common-mode noise, NOT SSZ
```

---

## C.4 Vibration and Mechanical Noise

### Mechanism
Mechanical vibrations cause:
- Sudden tilt changes (impulse-like)
- Modulation of qubit-cavity coupling
- Flux noise from moving magnetic fields

### Scaling Behavior
| Property | Vibration | SSZ |
|----------|-----------|-----|
| Height dependence | Step-like, discontinuous | Smooth slope |
| Frequency scaling | Usually independent | ∝ ω |
| Time scaling | Impulse-like, non-stationary | ∝ t (stationary) |
| Compensation | Does NOT reverse | Reverses |

### Mitigation
1. **Vibration isolation**: Use pneumatic or active isolation
2. **Accelerometers**: Monitor vibrations, correlate with data
3. **Rigid mounting**: Minimize relative motion
4. **Post-selection**: Reject data during vibration events

### Discrimination Test
```
If accelerometer shows events correlated with phase jumps:
   → Vibration, NOT SSZ
If drift is continuous and proportional to Δh:
   → SSZ candidate
```

---

## C.5 Magnetic Field Drift

### Mechanism
Stray magnetic fields cause:
- Flux noise in SQUID-based qubits
- Zeeman shifts in spin qubits
- Position-dependent field gradients

### Scaling Behavior
| Property | Magnetic | SSZ |
|----------|----------|-----|
| Height dependence | Position-dependent (not ∝ Δh) | ∝ Δh |
| Frequency scaling | Weak or zero | ∝ ω |
| Time scaling | ∝ t (drift) | ∝ t |
| Compensation | Does NOT reverse | Reverses |

### Mitigation
1. **Magnetic shielding**: Mu-metal or superconducting shields
2. **Magnetometers**: Monitor field at multiple positions
3. **Flux-insensitive qubits**: Use sweet-spot operation
4. **Randomization**: Randomize height settings to decorrelate

### Discrimination Test
```
If drift correlates with magnetometer:
   → Magnetic confound, NOT SSZ
If drift scales linearly with Δh but not field:
   → SSZ candidate
```

---

## C.6 Charge Noise

### Mechanism
Fluctuating charges on surfaces cause:
- 1/f noise in transmons (reduced by design)
- Random telegraph noise from two-level systems
- Local, uncorrelated between qubits

### Scaling Behavior
| Property | Charge | SSZ |
|----------|--------|-----|
| Height dependence | Random, local | ∝ Δh |
| Frequency scaling | 1/f spectrum | ∝ ω |
| Time scaling | ∝ √t | ∝ t |
| Compensation | Does NOT reverse | Reverses |

### Mitigation
1. **Transmon design**: Large E_J/E_C ratio
2. **Surface treatment**: Clean fabrication
3. **Averaging**: Multiple measurements reduce random noise
4. **Reference qubits**: Subtract local noise

---

## C.7 Master Discrimination Protocol

```
┌────────────────────────────────────────────────────┐
│  CONFOUND DISCRIMINATION FLOWCHART                 │
├────────────────────────────────────────────────────┤
│                                                    │
│  1. Measure drift at multiple Δh values            │
│     ↓                                              │
│  2. Fit slope α = ∂ΔΦ/∂Δh                         │
│     ↓                                              │
│  Is slope consistent with α_SSZ = ωr_s/R²?         │
│     NO → Anomalous coupling or confound            │
│     YES ↓                                          │
│  3. Apply compensation Φ_corr = -ωΔD×t             │
│     ↓                                              │
│  Does drift reverse to ≈ 0?                        │
│     NO → Confound (NOT SSZ)                        │
│     YES ↓                                          │
│  4. Vary frequency ω                               │
│     ↓                                              │
│  Does drift scale linearly with ω?                 │
│     NO → Confound (NOT SSZ)                        │
│     YES ↓                                          │
│  5. Check time scaling                             │
│     ↓                                              │
│  Is drift linear in t (not √t)?                    │
│     NO → Random noise (NOT SSZ)                    │
│     YES ↓                                          │
│  6. Correlate with environmental sensors           │
│     ↓                                              │
│  Any correlation with T, B, vibration?             │
│     YES → Environmental confound                   │
│     NO → SSZ CANDIDATE                             │
│                                                    │
└────────────────────────────────────────────────────┘
```

---

## C.8 Summary Table

| Confound | Key Discriminator | Mitigation |
|----------|-------------------|------------|
| Thermal | Sensor correlation | RTD monitoring |
| LO noise | √t scaling | Reference qubits |
| Vibration | Impulse-like | Accelerometers |
| Magnetic | Position-dependent | Shielding |
| Charge | Local, random | Averaging |
| **SSZ** | **Compensation reversal** | **None needed** |
