#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Paper A formulas against repository."""
import sys
sys.stdout.reconfigure(encoding='utf-8')
from ssz_qubits import *
import numpy as np

print('REPOSITORY ANALYSIS: PAPER A FORMULAS')
print('=' * 70)

# Test coherent zone calculation
print()
print('1. VERIFY GRADIENT FORMULA')
print('-' * 50)

r = R_EARTH
r_s = schwarzschild_radius(M_EARTH)

# Gradient from formula: dXi/dr = -r_s / (2r^2)
gradient_formula = -r_s / (2 * r**2)
print(f'  dXi/dr (formula) = {gradient_formula:.6e}')

# Gradient from numerical differentiation
dr = 1.0  # 1 meter
xi1 = xi_segment_density(r, M_EARTH)
xi2 = xi_segment_density(r + dr, M_EARTH)
gradient_numerical = (xi2 - xi1) / dr
print(f'  dXi/dr (numerical) = {gradient_numerical:.6e}')

print()
print('2. COHERENT ZONE WIDTH - MATHEMATICS')
print('-' * 50)

# For |Delta_Xi| < epsilon, zone width z satisfies:
# |Delta_Xi| = |dXi/dr| * z < epsilon
# => z = epsilon / |dXi/dr| = epsilon * 2R^2 / r_s

epsilon = 1e-18
z_formula_2R2 = epsilon * 2 * R_EARTH**2 / r_s
z_formula_4R2 = epsilon * 4 * R_EARTH**2 / r_s

print(f'  epsilon = {epsilon:.0e}')
print(f'  |dXi/dr| = r_s/(2R^2) = {r_s/(2*R_EARTH**2):.6e}')
print()
print(f'  z = eps / |dXi/dr| = 2*R^2*eps/r_s = {z_formula_2R2*1000:.2f} mm')
print(f'  z = 4*R^2*eps/r_s (Paper Eq.8) = {z_formula_4R2*1000:.2f} mm')

# Check what segment_coherent_zone returns
print()
print('3. REPOSITORY FUNCTION segment_coherent_zone()')
print('-' * 50)

try:
    # Check function signature
    import inspect
    sig = inspect.signature(segment_coherent_zone)
    print(f'  Signature: segment_coherent_zone{sig}')
    
    # Call the function
    result = segment_coherent_zone(R_EARTH, epsilon, M_EARTH)
    print(f'  Result for eps=1e-18:')
    if isinstance(result, dict):
        for k, v in result.items():
            if isinstance(v, float):
                print(f'    {k}: {v:.6e} ({v*1000:.2f} mm)')
            else:
                print(f'    {k}: {v}')
    else:
        print(f'    {result}')
except Exception as e:
    print(f'  Error: {e}')

print()
print('4. NUMERICAL VERIFICATION OF ZONE')
print('-' * 50)

# Calculate zone width where Delta_Xi = epsilon
xi_center = xi_segment_density(R_EARTH, M_EARTH)
print(f'  Xi(R_Earth) = {xi_center:.6e}')
print()
print('  z [mm]  | Delta_Xi        | Delta_Xi/eps')
print('  ' + '-' * 45)
for z_test in [9.15, 18.3, 36.6]:  # in mm
    z_m = z_test / 1000
    xi_edge = xi_segment_density(R_EARTH + z_m, M_EARTH)
    delta_xi = abs(xi_edge - xi_center)
    ratio = delta_xi / epsilon
    print(f'  {z_test:6.2f} | {delta_xi:.6e} | {ratio:.2f}')

print()
print('5. DECOHERENCE ENHANCEMENT FACTOR')
print('-' * 50)

# Check if this is computed in qubit_pair_segment_mismatch
q1 = Qubit(id='q1', x=0, y=0, z=0, gate_time=50e-9)
q2 = Qubit(id='q2', x=0, y=0, z=1e-3, gate_time=50e-9)
pair = QubitPair(q1, q2)
result = qubit_pair_segment_mismatch(pair, M_EARTH)

print('  qubit_pair_segment_mismatch() returns:')
for k, v in result.items():
    print(f'    {k}: {v:.6e}')

# Check if decoherence_enhancement is in the result
if 'decoherence_enhancement' in result:
    print()
    print(f'  decoherence_enhancement IS in repository output')
    print(f'  Value: {result["decoherence_enhancement"]:.6f}')
else:
    print()
    print('  decoherence_enhancement NOT in repository output')

print()
print('=' * 70)
print('SUMMARY')
print('=' * 70)
print()
print('1. Coherent Zone Formula:')
print(f'   Half-width: z = 2*R^2*eps/r_s = {z_formula_2R2*1000:.2f} mm')
print(f'   Total width (Paper Eq.8): z = 4*R^2*eps/r_s = {z_formula_4R2*1000:.2f} mm')
print('   -> Paper uses TOTAL width (correct)')
print()
print('2. Decoherence Enhancement:')
if 'decoherence_enhancement' in result:
    print('   -> IS defined in repository')
else:
    print('   -> NOT defined in repository')
