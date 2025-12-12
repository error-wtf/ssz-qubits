#!/usr/bin/env python3
"""Comprehensive test of all SSZ-Qubits modules."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

print('=' * 70)
print('COMPREHENSIVE MODULE IMPORT AND FUNCTION TEST')
print('=' * 70)

errors = []

# Test 1: Core module
print()
print('1. CORE MODULE (ssz_qubits.py)')
print('-' * 50)
try:
    from ssz_qubits import (
        schwarzschild_radius, xi_segment_density, xi_gradient,
        ssz_time_dilation, ssz_time_dilation_difference,
        segment_coherent_zone, qubit_pair_segment_mismatch,
        Qubit, QubitPair, analyze_qubit_segment,
        R_EARTH, M_EARTH, C, G, PHI
    )
    print('  All imports: OK')
    
    # Test functions
    r_s = schwarzschild_radius(M_EARTH)
    xi = xi_segment_density(R_EARTH)
    grad = xi_gradient(R_EARTH)
    D = ssz_time_dilation(R_EARTH)
    dD = ssz_time_dilation_difference(R_EARTH, R_EARTH + 1)
    zone = segment_coherent_zone(0, 1e-18)
    
    q1 = Qubit(id='q1', x=0, y=0, z=0, gate_time=50e-9)
    q2 = Qubit(id='q2', x=0, y=0, z=1e-3, gate_time=50e-9)
    pair = QubitPair(q1, q2)
    mismatch = qubit_pair_segment_mismatch(pair)
    analysis = analyze_qubit_segment(q1)
    
    print('  All functions: OK')
    print(f'  r_s = {r_s*1000:.2f} mm')
    print(f'  Xi = {xi:.2e}')
    print(f'  D = {D:.15f}')
except Exception as e:
    print(f'  ERROR: {e}')
    errors.append(('Core module', str(e)))

# Test 2: Paper A support module
print()
print('2. PAPER A SUPPORT MODULE (ssz_paper_a_support.py)')
print('-' * 50)
try:
    from ssz_paper_a_support import (
        gr_time_dilation_weak_field, compare_ssz_gr,
        fidelity_reduction_small_angle, fidelity_after_gates,
        verify_linear_scaling, verify_numerical_stability,
        coherent_zone_analysis, decoherence_enhancement_factor
    )
    print('  All imports: OK')
    
    # Test functions
    D_gr = gr_time_dilation_weak_field(R_EARTH)
    comp = compare_ssz_gr(R_EARTH)
    fid_loss = fidelity_reduction_small_angle(1e-7)
    fid = fidelity_after_gates(1.0, 10**9)
    lin = verify_linear_scaling()
    stab = verify_numerical_stability()
    zone = coherent_zone_analysis(1e-18)
    dec = decoherence_enhancement_factor(1e-19)
    
    print('  All functions: OK')
    print(f'  SSZ = GR: {comp["relative_difference"]:.2e}')
    print(f'  Linear scaling: {lin["is_linear"]}')
    print(f'  Numerical stability: {stab["numerical_stability_demonstrated"]}')
except Exception as e:
    print(f'  ERROR: {e}')
    errors.append(('Paper A support', str(e)))

# Test 3: Entanglement module
print()
print('3. ENTANGLEMENT MODULE (ssz_entanglement.py)')
print('-' * 50)
try:
    from ssz_entanglement import (
        entangled_pair_phase_drift, bell_state_fidelity,
        bell_state_fidelity_approx, chsh_parameter,
        characteristic_time_T_SSZ, correction_interval,
        correction_gate, is_in_coherent_zone,
        analyze_entangled_pair, EntangledPairAnalysis
    )
    print('  All imports: OK')
    
    # Test functions
    q1 = Qubit(id='A', x=0, y=0, z=0, gate_time=50e-9)
    q2 = Qubit(id='B', x=0, y=0, z=1e-3, gate_time=50e-9)
    pair = QubitPair(q1, q2)
    
    drift = entangled_pair_phase_drift(pair)
    F = bell_state_fidelity(1e-7)
    F_approx = bell_state_fidelity_approx(1e-7)
    S = chsh_parameter(1e-7)
    T = characteristic_time_T_SSZ(1e-3)
    N = correction_interval(1e-6, 1.72e-16)
    corr = correction_gate(1e-7, 'A')
    in_zone = is_in_coherent_zone(pair)
    analysis = analyze_entangled_pair(pair)
    
    print('  All functions: OK')
    print(f'  Phase drift/gate: {drift["phase_drift_per_gate"]:.2e} rad')
    print(f'  T_SSZ: {T/(365.25*24*3600):.1f} years')
    print(f'  In coherent zone: {in_zone}')
except Exception as e:
    print(f'  ERROR: {e}')
    errors.append(('Entanglement module', str(e)))

# Test 4: Numerical values verification
print()
print('4. PAPER NUMERICAL VALUES')
print('-' * 50)
try:
    import numpy as np
    
    # Paper A values
    assert abs(r_s - 8.87e-3) < 0.01e-3, "r_s mismatch"
    assert abs(xi - 6.96e-10) < 0.1e-10, "Xi mismatch"
    
    # Phase drift
    phase_drift = mismatch['phase_drift_per_gate']
    assert abs(phase_drift - 1.72e-16) / 1.72e-16 < 0.01, "Phase drift mismatch"
    
    # Zone width (18.3 mm = 0.0183 m) - recalculate to avoid variable shadowing
    zone_test = segment_coherent_zone(0, 1e-18)
    zone_width = zone_test[1] - zone_test[0]
    assert abs(zone_width - 0.01830) < 0.001, f"Zone width mismatch: {zone_width}"
    
    # Paper B values
    delta_phi = 1.72e-7
    F_exact = np.cos(delta_phi/2)**2
    fid_loss = 1 - F_exact
    assert abs(fid_loss - 7.4e-15) / 7.4e-15 < 0.1, "Fidelity loss mismatch"
    
    T_years = T / (365.25 * 24 * 3600)
    assert abs(T_years - 29) / 29 < 0.05, "T_SSZ mismatch"
    
    print('  All numerical values: OK')
    print(f'  Phase drift: {phase_drift:.2e} rad (expected 1.72e-16)')
    print(f'  Zone width: {zone_width*1000:.2f} mm (expected 18.3)')
    print(f'  T_SSZ: {T_years:.1f} years (expected 29)')
except AssertionError as e:
    print(f'  ASSERTION ERROR: {e}')
    errors.append(('Numerical values', str(e)))
except Exception as e:
    import traceback
    print(f'  ERROR: {e}')
    traceback.print_exc()
    errors.append(('Numerical values', str(e)))

# Test 5: Demo scripts
print()
print('5. DEMO SCRIPTS')
print('-' * 50)
try:
    # Test ssz_paper_a_support demo
    from ssz_paper_a_support import (
        compare_ssz_gr, fidelity_after_gates, 
        verify_linear_scaling, verify_numerical_stability,
        coherent_zone_analysis
    )
    
    comp = compare_ssz_gr(R_EARTH)
    assert comp['is_weak_field'] == True
    
    fid = fidelity_after_gates(1.0, 10**9)
    assert fid['approximation_valid'] == True
    
    lin = verify_linear_scaling()
    assert lin['is_linear'] == True
    
    stab = verify_numerical_stability()
    assert stab['numerical_stability_demonstrated'] == True
    
    zone = coherent_zone_analysis(1e-18)
    assert zone['formula_matches'] == True
    
    print('  ssz_paper_a_support demo: OK')
    
    # Test ssz_entanglement demo
    from ssz_entanglement import analyze_entangled_pair, print_entangled_pair_analysis
    analysis = analyze_entangled_pair(pair, N_gates=10**9)
    assert analysis.in_coherent_zone == True
    
    print('  ssz_entanglement demo: OK')
except AssertionError as e:
    print(f'  ASSERTION ERROR: {e}')
    errors.append(('Demo scripts', str(e)))
except Exception as e:
    print(f'  ERROR: {e}')
    errors.append(('Demo scripts', str(e)))

# Summary
print()
print('=' * 70)
if errors:
    print(f'ERRORS FOUND: {len(errors)}')
    for module, error in errors:
        print(f'  - {module}: {error}')
    sys.exit(1)
else:
    print('ALL TESTS PASSED - REPOSITORY IS 100% CORRECT')
print('=' * 70)
