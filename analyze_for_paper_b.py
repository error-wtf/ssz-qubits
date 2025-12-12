#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Analyze repository for Paper B - Entanglement focus."""
import sys
sys.stdout.reconfigure(encoding='utf-8')
from ssz_qubits import *
import numpy as np
import inspect

print('PHASE 1: REPOSITORY-ANALYSE FUER PAPER B')
print('=' * 70)

# List all functions
print('VERFUEGBARE FUNKTIONEN:')
members = inspect.getmembers(sys.modules['ssz_qubits'], inspect.isfunction)
for name, func in members:
    if not name.startswith('_'):
        print(f'  {name}')

print()
print('QUBIT PAIR MISMATCH ANALYSE')
print('-' * 70)

# Create test pair (Qubit uses x, y, z coordinates)
q1 = Qubit(id='q1', x=0.0, y=0.0, z=0.0, gate_time=50e-9)
q2 = Qubit(id='q2', x=0.0, y=0.0, z=1e-3, gate_time=50e-9)  # 1mm higher
pair = QubitPair(q1, q2)

result = qubit_pair_segment_mismatch(pair, M_EARTH)
print('Ergebnis fuer 1mm Hoehendifferenz:')
for key, val in result.items():
    print(f'  {key}: {val:.6e}')

print()
print('SKALIERUNG MIT HOEHENUNTERSCHIED')
print('-' * 70)

heights = [1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 0.1, 1.0]
print('dh [m]       | delta_xi      | phase_drift/gate')
print('-' * 50)
for h in heights:
    q1 = Qubit(id='q1', x=0.0, y=0.0, z=0.0, gate_time=50e-9)
    q2 = Qubit(id='q2', x=0.0, y=0.0, z=h, gate_time=50e-9)
    pair = QubitPair(q1, q2)
    result = qubit_pair_segment_mismatch(pair, M_EARTH)
    dxi = result['delta_xi']
    pdg = result['phase_drift_per_gate']
    print(f'{h:12.2e} | {dxi:13.6e} | {pdg:13.6e}')

# Verify linearity
print()
print('Linearitaetspruefung: phase_drift / dh sollte konstant sein')
ratios = []
for h in heights:
    q1 = Qubit(id='q1', x=0.0, y=0.0, z=0.0, gate_time=50e-9)
    q2 = Qubit(id='q2', x=0.0, y=0.0, z=h, gate_time=50e-9)
    pair = QubitPair(q1, q2)
    result = qubit_pair_segment_mismatch(pair, M_EARTH)
    ratio = result['phase_drift_per_gate'] / h
    ratios.append(ratio)
    print(f'  dh={h:.2e}: ratio = {ratio:.6e}')

print(f'Standardabweichung der Ratios: {np.std(ratios):.2e} (sollte ~0 sein)')

print()
print('=' * 70)
print('ENTANGLEMENT FIDELITY BERECHNUNGEN')
print('=' * 70)

# Bell state fidelity: F = cos^2(DeltaPhi/2)
omega = 2 * np.pi * 5e9
t_gate = 50e-9

print()
print('Bell State Fidelity: F = cos^2(DeltaPhi/2)')
print('Taylor fuer kleine DeltaPhi: F = 1 - (DeltaPhi)^2/4')
print()

print('dh [m]  | N_gates | DeltaPhi [rad] | F (exakt)        | 1-F')
print('-' * 75)

test_cases = [
    (1e-3, 1e3),
    (1e-3, 1e6),
    (1e-3, 1e9),
    (1e-2, 1e6),
    (1e-2, 1e9),
    (0.1, 1e6),
    (0.1, 1e9),
    (1.0, 1e6),
    (1.0, 1e9),
    (10.0, 1e9),
    (100.0, 1e9),
]

for dh, n_gates in test_cases:
    r1 = R_EARTH
    r2 = R_EARTH + dh
    delta_d = abs(ssz_time_dilation_difference(r1, r2, M_EARTH))
    delta_phi = omega * delta_d * t_gate * n_gates
    fidelity = np.cos(delta_phi / 2)**2
    loss = 1 - fidelity
    print(f'{dh:7.1e} | {n_gates:7.0e} | {delta_phi:14.6e} | {fidelity:.12f} | {loss:.3e}')

print()
print('=' * 70)
print('DEPHASIERUNGSZEIT T_SSZ')
print('=' * 70)

# T_SSZ defined as time for DeltaPhi to reach pi (complete dephasing)
# DeltaPhi = omega * delta_D * t
# pi = omega * delta_D * T_SSZ
# T_SSZ = pi / (omega * delta_D)

print()
print('T_SSZ = pi / (omega * |DeltaD|)')
print('Zeit bis DeltaPhi = pi (vollstaendige Dephasierung)')
print()

for dh in [1e-3, 1e-2, 0.1, 1.0, 10.0, 100.0, 1000.0]:
    r1 = R_EARTH
    r2 = R_EARTH + dh
    delta_d = abs(ssz_time_dilation_difference(r1, r2, M_EARTH))
    T_ssz = np.pi / (omega * delta_d)
    
    # Convert to meaningful units
    if T_ssz > 3.15e7:  # > 1 year
        T_str = f'{T_ssz/3.15e7:.2e} Jahre'
    elif T_ssz > 86400:  # > 1 day
        T_str = f'{T_ssz/86400:.2e} Tage'
    elif T_ssz > 3600:  # > 1 hour
        T_str = f'{T_ssz/3600:.2e} Stunden'
    else:
        T_str = f'{T_ssz:.2e} s'
    
    print(f'  dh = {dh:8.1e} m: T_SSZ = {T_ssz:.3e} s = {T_str}')

print()
print('=' * 70)
print('KOMPENSATIONSINTERVALL')
print('=' * 70)

# Correction interval: apply phase correction when DeltaPhi reaches threshold
# N_corr = threshold / phase_per_gate

threshold = 1e-6  # 1 microrad threshold
print(f'Schwellwert: DeltaPhi_max = {threshold:.0e} rad')
print()

for dh in [1e-3, 1e-2, 0.1, 1.0]:
    r1 = R_EARTH
    r2 = R_EARTH + dh
    delta_d = abs(ssz_time_dilation_difference(r1, r2, M_EARTH))
    phase_per_gate = omega * delta_d * t_gate
    N_corr = threshold / phase_per_gate
    print(f'  dh = {dh:.0e} m: N_corr = {N_corr:.2e} Gates')

print()
print('=' * 70)
print('ZUSAMMENFASSUNG DER SKALIERUNGSGESETZE')
print('=' * 70)

print('''
1. Segment Density:
   Xi(r) = r_s / (2r)
   
2. Time Dilation:
   D(r) = 1 / (1 + Xi(r))
   
3. Time Dilation Difference (stabile Form):
   DeltaD = 2*r_s*(r1-r2) / ((2*r1+r_s)*(2*r2+r_s))
   
4. Lineare Naeherung (r >> r_s):
   DeltaD = (r_s / 2R^2) * dh = 1.09e-16 * dh [pro Meter]
   
5. Phase pro Gate:
   DeltaPhi_gate = omega * |DeltaD| * t_gate
   = 1.72e-16 * (dh/mm) * (f/5GHz) * (t/50ns) rad
   
6. Kumulative Phase:
   DeltaPhi_total = N * DeltaPhi_gate
   
7. Bell State Fidelity:
   F = cos^2(DeltaPhi/2)
   F = 1 - (DeltaPhi)^2/4 + O(DeltaPhi^4)  [Taylor]
   
8. Dephasierungszeit:
   T_SSZ = pi / (omega * |DeltaD|)
''')
