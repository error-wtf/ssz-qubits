#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analyze ssz_qubits behavior for paper consistency.
Extract actual numerical values from the implementation.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
from ssz_qubits import *
import numpy as np

print('PHASE 1: NUMERISCHE ANALYSE DER SKRIPTE')
print('=' * 70)

# 1. Grundkonstanten
print()
print('1. PHYSIKALISCHE KONSTANTEN')
print('-' * 40)
r_s = schwarzschild_radius(M_EARTH)
print(f'   r_s (Earth) = {r_s:.6e} m = {r_s*1e3:.4f} mm')
print(f'   R_Earth = {R_EARTH:.6e} m')
print(f'   G = {G:.6e}')
print(f'   c = {C:.6e}')

# 2. Segment Density Berechnung
print()
print('2. SEGMENT DENSITY Xi(r) = r_s / (2r)')
print('-' * 40)
xi_surface = xi_segment_density(R_EARTH, M_EARTH)
xi_1m = xi_segment_density(R_EARTH + 1, M_EARTH)
xi_1km = xi_segment_density(R_EARTH + 1000, M_EARTH)
print(f'   Xi(R_Earth) = {xi_surface:.6e}')
print(f'   Xi(R_Earth + 1m) = {xi_1m:.6e}')
print(f'   Xi(R_Earth + 1km) = {xi_1km:.6e}')
gradient = (xi_1m - xi_surface) / 1
print(f'   Gradient: dXi/dh = {gradient:.6e} per meter')

# 3. Time Dilation
print()
print('3. TIME DILATION D_SSZ(r) = 1/(1+Xi)')
print('-' * 40)
d_surface = ssz_time_dilation(R_EARTH, M_EARTH)
d_1m = ssz_time_dilation(R_EARTH + 1, M_EARTH)
print(f'   D_SSZ(R_Earth) = {d_surface:.15f}')
print(f'   D_SSZ(R_Earth + 1m) = {d_1m:.15f}')
print(f'   1 - D_SSZ = {1 - d_surface:.6e}')

# 4. Numerisch stabile Differenz
print()
print('4. NUMERISCH STABILE DIFFERENZ')
print('-' * 40)
for dh in [1e-6, 1e-3, 1, 1000]:
    r1 = R_EARTH
    r2 = R_EARTH + dh
    delta_d = ssz_time_dilation_difference(r1, r2, M_EARTH)
    print(f'   dh = {dh:8.0e} m: Delta_D = {delta_d:.6e}')

# Verify linear scaling
print()
print('   Linear scaling check:')
dh_ref = 1.0
delta_d_ref = ssz_time_dilation_difference(R_EARTH, R_EARTH + dh_ref, M_EARTH)
slope = delta_d_ref / dh_ref
print(f'   Slope = Delta_D / dh = {slope:.6e} per meter')

# 5. Phase Drift Berechnung
print()
print('5. PHASE DRIFT BERECHNUNG')
print('-' * 40)
omega = 2 * np.pi * 5e9  # 5 GHz
t_gate = 50e-9  # 50 ns
print(f'   omega = 2*pi*5 GHz = {omega:.6e} rad/s')
print(f'   t_gate = 50 ns')

for dh_mm in [0.01, 0.1, 1, 10]:
    dh = dh_mm * 1e-3
    q1 = Qubit(id='Q1', x=0, y=0, z=0, gate_time=t_gate)
    q2 = Qubit(id='Q2', x=0, y=0, z=dh, gate_time=t_gate)
    pair = QubitPair(q1, q2)
    mismatch = qubit_pair_segment_mismatch(pair, M_EARTH)
    phase = mismatch['phase_drift_per_gate']
    print(f'   dh = {dh_mm:5.2f} mm: Phase/Gate = {phase:.3e} rad')

# Verify phase formula
print()
print('   Phase formula verification:')
dh = 1e-3  # 1 mm
delta_d = ssz_time_dilation_difference(R_EARTH, R_EARTH + dh, M_EARTH)
phase_manual = omega * abs(delta_d) * t_gate
print(f'   omega * |Delta_D| * t_gate = {phase_manual:.3e} rad')

# 6. Coherent Zone
print()
print('6. COHERENT ZONE BERECHNUNG')
print('-' * 40)
for var in [1e-14, 1e-16, 1e-18, 1e-20]:
    h_min, h_max = segment_coherent_zone(0, max_xi_variation=var, M=M_EARTH)
    width = h_max - h_min
    print(f'   max_dXi = {var:.0e}: zone width = {width:.3e} m')

# Verify zone formula
print()
print('   Zone formula verification:')
print('   z = max_dXi / |dXi/dh| = max_dXi * 2*R^2 / r_s')
for var in [1e-18]:
    z_formula = var * 2 * R_EARTH**2 / r_s
    h_min, h_max = segment_coherent_zone(0, max_xi_variation=var, M=M_EARTH)
    z_actual = h_max - h_min
    print(f'   Formula: {z_formula:.3e} m, Actual: {z_actual:.3e} m')

print()
print('=' * 70)
print('ZUSAMMENFASSUNG DER NUMERISCHEN BEZIEHUNGEN')
print('=' * 70)
print()
print('Die Skripte implementieren folgende Beziehungen:')
print()
print('1. Xi(r) = r_s / (2r)  mit r_s = 2GM/c^2')
print('2. D_SSZ(r) = 1 / (1 + Xi(r))')
print('3. Delta_D = D(r2) - D(r1) [numerisch stabil berechnet]')
print('4. Phase_drift = omega * |Delta_D| * t_gate')
print('5. Zone_width = max_dXi * 2*R^2 / r_s')
print()
print('Skalierungen (aus den Daten):')
print(f'   Delta_D pro Meter: {slope:.2e}')
print(f'   Phase pro Gate (1mm, 5GHz, 50ns): {phase_manual:.2e} rad')
