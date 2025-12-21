#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Paper C v1.1 Feasibility Analysis

Realistic order-of-magnitude calculations for SSZ detection.

Key Questions:
1. What is the actual signal size?
2. What is the realistic noise floor?
3. How many averages needed for SNR > 3?
4. Is this achievable? If not, what Δh/platform is needed?

(c) 2025 Carmen Wrede, Lino Casu
"""

import os
import sys

# UTF-8 for Windows
if sys.platform.startswith('win'):
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

import numpy as np
from ssz_qubits import (
    M_EARTH, R_EARTH, schwarzschild_radius,
    ssz_time_dilation_difference
)

# Constants
R_S_EARTH = schwarzschild_radius(M_EARTH)
OMEGA_5GHZ = 2 * np.pi * 5e9

print("="*70)
print("PAPER C v1.1: FEASIBILITY ANALYSIS")
print("="*70)

# =============================================================================
# 1. SSZ SIGNAL SIZE
# =============================================================================
print("\n" + "="*70)
print("1. SSZ SIGNAL SIZE")
print("="*70)

delta_h_values = [1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 0.1, 1.0, 10.0]  # m

print(f"\n{'Δh':>12} | {'ΔD_SSZ':>15} | {'Δφ/μs [rad]':>15} | {'Δφ@100μs [rad]':>15}")
print("-"*70)

for dh in delta_h_values:
    delta_d = abs(ssz_time_dilation_difference(R_EARTH + dh, R_EARTH, M_EARTH))
    phi_per_us = OMEGA_5GHZ * delta_d * 1e-6
    phi_100us = OMEGA_5GHZ * delta_d * 100e-6
    
    if dh < 1e-3:
        dh_str = f"{dh*1e6:.0f} μm"
    elif dh < 1:
        dh_str = f"{dh*1e3:.0f} mm"
    else:
        dh_str = f"{dh:.1f} m"
    
    print(f"{dh_str:>12} | {delta_d:>15.2e} | {phi_per_us:>15.2e} | {phi_100us:>15.2e}")

# =============================================================================
# 2. REALISTIC NOISE FLOOR
# =============================================================================
print("\n" + "="*70)
print("2. REALISTIC NOISE FLOOR (State-of-the-Art Transmons)")
print("="*70)

# Best-case parameters from literature
T2_star = 100e-6  # Ramsey T2* [s]
T2_echo = 500e-6  # Echo T2 [s]
readout_fidelity = 0.99  # Single-shot readout fidelity
shots_per_second = 10000  # Typical repetition rate

# Phase noise sources
print("\nPhase noise contributions (per single shot):")

# Ramsey phase precision: limited by T2* decay
# Phase uncertainty ~ 1/√(contrast) ~ 1 rad for single shot
single_shot_phase_noise = 1.0  # rad (order of magnitude)
print(f"  Single-shot phase noise:     ~{single_shot_phase_noise:.1f} rad")

# LO phase noise (typical 10 kHz linewidth → ~10⁻³ rad in 100 μs)
lo_phase_noise = 1e-3  # rad
print(f"  LO phase noise (100 μs):     ~{lo_phase_noise:.0e} rad")

# Temperature drift (1 mK → ~1 kHz → ~0.6 rad in 100 μs)
temp_phase_drift = 2 * np.pi * 1e3 * 100e-6  # ~0.6 rad
print(f"  Temperature drift (1 mK):    ~{temp_phase_drift:.1f} rad")

# Combined noise floor (dominated by single-shot)
combined_noise = np.sqrt(single_shot_phase_noise**2 + lo_phase_noise**2)
print(f"\n  Combined noise floor:        ~{combined_noise:.1f} rad (single shot)")

# =============================================================================
# 3. AVERAGING REQUIREMENTS
# =============================================================================
print("\n" + "="*70)
print("3. AVERAGING REQUIREMENTS FOR SNR > 3")
print("="*70)

target_snr = 3
delta_h = 1e-3  # 1 mm
delta_d = abs(ssz_time_dilation_difference(R_EARTH + delta_h, R_EARTH, M_EARTH))
signal_100us = OMEGA_5GHZ * delta_d * 100e-6

print(f"\nFor Δh = 1 mm, T_Ramsey = 100 μs:")
print(f"  Signal:          {signal_100us:.2e} rad")
print(f"  Noise (1 shot):  {single_shot_phase_noise:.1f} rad")

# N averages reduces noise by sqrt(N)
# Need: signal / (noise / sqrt(N)) > SNR
# → N > (SNR * noise / signal)²
N_required = (target_snr * single_shot_phase_noise / signal_100us)**2
print(f"  N for SNR=3:     {N_required:.2e} shots")

# Time required
time_required_s = N_required / shots_per_second
time_required_hours = time_required_s / 3600
time_required_years = time_required_hours / (24 * 365)

print(f"  Time @ 10 kHz:   {time_required_s:.2e} s = {time_required_hours:.2e} hours")
print(f"                   = {time_required_years:.2e} years")

print(f"\n  ** CONCLUSION: {N_required:.0e} shots needed → NOT FEASIBLE **")

# =============================================================================
# 4. WHAT Δh IS NEEDED FOR REALISTIC DETECTION?
# =============================================================================
print("\n" + "="*70)
print("4. REQUIRED Δh FOR REALISTIC DETECTION")
print("="*70)

# Target: SNR=3 with N=10^9 shots (achievable in ~1 day)
N_realistic = 1e9  # ~1 day at 10 kHz
noise_after_averaging = single_shot_phase_noise / np.sqrt(N_realistic)
required_signal = target_snr * noise_after_averaging

print(f"\nWith N = 10⁹ shots (~1 day at 10 kHz):")
print(f"  Noise after averaging: {noise_after_averaging:.2e} rad")
print(f"  Required signal (SNR=3): {required_signal:.2e} rad")

# What Δh gives this signal?
# signal = ω × ΔD × t
# ΔD ≈ r_s × Δh / R² (linearized)
# Δh_required = signal × R² / (ω × t × r_s)
t_ramsey = 100e-6
required_dh = required_signal * R_EARTH**2 / (OMEGA_5GHZ * t_ramsey * R_S_EARTH)

print(f"  Required Δh: {required_dh:.2f} m = {required_dh*100:.0f} cm")

# What if we use longer coherence (optical clocks)?
print("\n  ** With longer integration (optical clock, T=1s):")
t_optical = 1.0
required_dh_optical = required_signal * R_EARTH**2 / (2 * np.pi * 429e12 * t_optical * R_S_EARTH)
print(f"     Required Δh: {required_dh_optical*1e3:.3f} mm")

# =============================================================================
# 5. HARDWARE OPTIONS FOR Δh
# =============================================================================
print("\n" + "="*70)
print("5. HARDWARE OPTIONS FOR Δh GENERATION")
print("="*70)

chip_size = 20e-3  # 20 mm chip

print("\nOption A: CHIP TILT")
print("-" * 40)
tilt_angles = [0.1, 1, 5, 10]  # degrees
for angle in tilt_angles:
    dh = chip_size * np.sin(np.radians(angle))
    print(f"  Tilt {angle:>4}°: Δh = {dh*1e3:.2f} mm across 20 mm chip")

print("\nOption B: REMOTE ENTANGLEMENT (two dilution fridges)")
print("-" * 40)
floor_heights = [0.5, 1.0, 2.0, 5.0]  # m
for h in floor_heights:
    delta_d = abs(ssz_time_dilation_difference(R_EARTH + h, R_EARTH, M_EARTH))
    signal = OMEGA_5GHZ * delta_d * 100e-6
    n_needed = (target_snr * single_shot_phase_noise / signal)**2
    print(f"  Δh = {h:.1f} m: signal = {signal:.2e} rad, N = {n_needed:.2e}")

print("\nOption C: 3D CHIPLET STACK")
print("-" * 40)
stack_heights = [0.1, 0.5, 1.0, 2.0]  # mm
for h in stack_heights:
    dh = h * 1e-3
    delta_d = abs(ssz_time_dilation_difference(R_EARTH + dh, R_EARTH, M_EARTH))
    signal = OMEGA_5GHZ * delta_d * 100e-6
    print(f"  Stack Δh = {h:.1f} mm: signal = {signal:.2e} rad")

# =============================================================================
# 6. RECOMMENDED EXPERIMENTAL APPROACH
# =============================================================================
print("\n" + "="*70)
print("6. RECOMMENDED APPROACH (Upper-Bound Experiment)")
print("="*70)

print("""
FRAMING: Upper-Bound / Null-Result Experiment

1. PRIMARY GOAL: Place upper bound on any anomalous phase coupling
   - If SSZ effect exists at predicted level: too small to detect
   - If SSZ effect is LARGER than GR prediction: detectable
   - Null result → constrains any beyond-GR phase coupling

2. RECOMMENDED SETUP:
   - Chip tilt: 5° → Δh ≈ 1.7 mm across 20 mm chip
   - OR: Two-module remote entanglement at Δh = 1-2 m
   - Ramsey with echo: extend coherence to T2 ~ 500 μs
   - 10⁹ shots per configuration (~1 day)

3. STATISTICAL FRAMEWORK:
   - Fit slope: ΔΦ vs Δh (expect slope = ω × r_s / R²)
   - Null hypothesis: slope = 0
   - SSZ hypothesis: slope = predicted value
   - Report: measured slope ± uncertainty, compare to predictions

4. FALSIFICATION CRITERIA:
   - SSZ falsified if: measured slope inconsistent with prediction at 3σ
   - AND slope is zero within uncertainty
   - Upper bound: |anomalous coupling| < X rad/m/s

5. OUTCOME VALUE:
   - Either: first constraint on gravitational phase coupling in qubits
   - Or: detection of unexpected signal → major discovery
""")

# =============================================================================
# 7. SUMMARY TABLE
# =============================================================================
print("\n" + "="*70)
print("7. SUMMARY: FEASIBILITY MATRIX")
print("="*70)

print("""
| Setup                    | Δh      | Signal (100μs) | N for SNR=3 | Feasible?  |
|--------------------------|---------|----------------|-------------|------------|
| On-chip, no tilt         | 0       | 0              | ∞           | No         |
| On-chip, 5° tilt         | 1.7 mm  | 5.8×10⁻¹³ rad  | 2.7×10²⁵    | No         |
| 3D chiplet, 2 mm stack   | 2 mm    | 6.9×10⁻¹³ rad  | 1.9×10²⁵    | No         |
| Remote, Δh = 1 m         | 1 m     | 3.4×10⁻¹⁰ rad  | 7.7×10¹⁸    | Marginal   |
| Remote, Δh = 10 m        | 10 m    | 3.4×10⁻⁹ rad   | 7.7×10¹⁶    | Difficult  |
| Optical clock, Δh = 1 m  | 1 m     | ~10⁻⁶ rad      | ~10¹⁰       | YES        |
|--------------------------|---------|----------------|-------------|------------|

CONCLUSION:
- Superconducting qubits at mm-scale Δh: NOT feasible for detection
- Superconducting qubits at m-scale Δh (remote): marginal
- Optical clocks at m-scale Δh: FEASIBLE (already demonstrated!)

RECOMMENDATION:
Frame Paper C as:
1. Upper-bound experiment for superconducting qubits
2. Point to optical clock experiments as gold-standard platform
3. Value: first systematic constraint on gravitational phase coupling in solid-state qubits
""")

print("\n" + "="*70)
print("END OF FEASIBILITY ANALYSIS")
print("="*70)
