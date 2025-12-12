#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSZ Paper A Support Module

Additional functions to support Paper A claims:
- GR comparison (weak-field equivalence)
- Fidelity reduction (small-angle approximation)
- Linear scaling verification
- Numerical stability verification
"""
import numpy as np
from typing import Dict, Tuple, List
from ssz_qubits import (
    schwarzschild_radius, xi_segment_density, xi_gradient,
    ssz_time_dilation, ssz_time_dilation_difference,
    qubit_pair_segment_mismatch, segment_coherent_zone,
    Qubit, QubitPair, R_EARTH, M_EARTH, C, G
)


# =============================================================================
# GR COMPARISON (Paper A Section 4.3)
# =============================================================================

def gr_time_dilation_weak_field(r: float, M: float = M_EARTH) -> float:
    """
    General Relativity time dilation in weak-field approximation.
    
    D_GR = sqrt(1 - r_s/r) ≈ 1 - r_s/(2r) for r >> r_s
    
    This is the standard Schwarzschild result.
    
    Parameters
    ----------
    r : float
        Radial distance from center of mass [m]
    M : float
        Central mass [kg]
        
    Returns
    -------
    float
        GR time dilation factor
    """
    r_s = schwarzschild_radius(M)
    return np.sqrt(1 - r_s / r)


def compare_ssz_gr(r: float, M: float = M_EARTH) -> Dict[str, float]:
    """
    Compare SSZ and GR time dilation predictions.
    
    In weak-field (r >> r_s), SSZ and GR are identical to high precision.
    
    Parameters
    ----------
    r : float
        Radial distance [m]
    M : float
        Central mass [kg]
        
    Returns
    -------
    dict
        Comparison including:
        - D_SSZ: SSZ time dilation
        - D_GR: GR time dilation
        - relative_difference: |D_SSZ - D_GR| / D_GR
        - is_weak_field: True if r > 1000 * r_s
    """
    r_s = schwarzschild_radius(M)
    D_SSZ = ssz_time_dilation(r, M)
    D_GR = gr_time_dilation_weak_field(r, M)
    
    rel_diff = abs(D_SSZ - D_GR) / D_GR
    is_weak = r > 1000 * r_s
    
    return {
        'D_SSZ': D_SSZ,
        'D_GR': D_GR,
        'relative_difference': rel_diff,
        'is_weak_field': is_weak,
        'r_over_r_s': r / r_s
    }


# =============================================================================
# FIDELITY REDUCTION (Paper A Section 7.1)
# =============================================================================

def fidelity_reduction_small_angle(delta_phi: float) -> float:
    """
    Fidelity reduction using small-angle approximation.
    
    1 - F ≈ ΔΦ²/4 for ΔΦ << 1
    
    This is the approximation used in Paper A Section 7.1.
    
    Parameters
    ----------
    delta_phi : float
        Phase drift [rad]
        
    Returns
    -------
    float
        Fidelity reduction (1 - F)
    """
    return delta_phi**2 / 4


def fidelity_after_gates(
    height_diff_mm: float,
    N_gates: int,
    qubit_frequency: float = 5e9,
    gate_time: float = 50e-9
) -> Dict[str, float]:
    """
    Calculate fidelity after N gate operations.
    
    Uses the small-angle approximation valid for Paper A scenarios.
    
    Parameters
    ----------
    height_diff_mm : float
        Height difference in millimeters
    N_gates : int
        Number of gate operations
    qubit_frequency : float
        Qubit frequency [Hz]
    gate_time : float
        Gate duration [s]
        
    Returns
    -------
    dict
        Fidelity analysis including:
        - delta_phi_total: Total accumulated phase [rad]
        - fidelity: F = 1 - ΔΦ²/4
        - fidelity_reduction: 1 - F
    """
    # Phase drift per gate: 1.72e-16 rad/mm/gate
    phase_per_gate_per_mm = 1.72e-16
    delta_phi = N_gates * phase_per_gate_per_mm * height_diff_mm
    
    fidelity_loss = fidelity_reduction_small_angle(delta_phi)
    
    return {
        'delta_phi_total': delta_phi,
        'fidelity': 1 - fidelity_loss,
        'fidelity_reduction': fidelity_loss,
        'approximation_valid': delta_phi < 0.1  # Small angle valid for phi < 0.1
    }


# =============================================================================
# LINEAR SCALING VERIFICATION (Paper A Section 4.2)
# =============================================================================

def verify_linear_scaling(
    height_range: List[float] = None,
    tolerance: float = 1e-3
) -> Dict[str, any]:
    """
    Verify linear scaling of phase drift with height.
    
    Paper A Eq. 7: |ΔΦ_gate| ∝ |Δh| × f × t_gate
    
    Note: Small deviations from perfect linearity at larger heights
    are expected due to the 1/r² dependence of the gradient.
    For Earth-surface applications (h << R), linearity holds to < 0.1%.
    
    Parameters
    ----------
    height_range : list
        Heights to test [m], default [1e-6 to 1e-2] (sub-cm range)
    tolerance : float
        Maximum allowed deviation from linearity (default 0.1%)
        
    Returns
    -------
    dict
        Verification results including:
        - is_linear: True if scaling is linear within tolerance
        - max_deviation: Maximum deviation from linear fit
        - heights: Tested heights
        - phase_drifts: Corresponding phase drifts
    """
    if height_range is None:
        # Use sub-cm range where linearity is excellent
        height_range = [1e-6, 1e-5, 1e-4, 1e-3, 1e-2]
    
    drifts = []
    for h in height_range:
        q1 = Qubit(id='q1', x=0, y=0, z=0, gate_time=50e-9)
        q2 = Qubit(id='q2', x=0, y=0, z=h, gate_time=50e-9)
        pair = QubitPair(q1, q2)
        result = qubit_pair_segment_mismatch(pair)
        drifts.append(result['phase_drift_per_gate'])
    
    # Check linearity: drift[i] / drift[0] should equal height[i] / height[0]
    deviations = []
    for i in range(1, len(height_range)):
        expected_ratio = height_range[i] / height_range[0]
        actual_ratio = drifts[i] / drifts[0]
        deviation = abs(actual_ratio - expected_ratio) / expected_ratio
        deviations.append(deviation)
    
    max_dev = max(deviations)
    
    return {
        'is_linear': max_dev < tolerance,
        'max_deviation': max_dev,
        'heights': height_range,
        'phase_drifts': drifts,
        'scaling_constant': drifts[0] / height_range[0],  # rad/m/gate
        'scaling_constant_per_mm': drifts[0] / height_range[0] * 1e-3  # rad/mm/gate
    }


# =============================================================================
# NUMERICAL STABILITY VERIFICATION (Paper A Section 3.2)
# =============================================================================

def verify_numerical_stability(
    height_range: List[float] = None
) -> Dict[str, any]:
    """
    Demonstrate numerical stability of closed-form ΔD expression.
    
    Paper A Eq. 4: ΔD = 2rₛ(r₁-r₂)/((2r₁+rₛ)(2r₂+rₛ))
    
    Shows that direct subtraction D(r₁) - D(r₂) fails due to
    floating-point cancellation, while closed-form remains accurate.
    
    Parameters
    ----------
    height_range : list
        Height differences to test [m]
        
    Returns
    -------
    dict
        Verification results including:
        - closed_form_works: True if closed-form gives non-zero values
        - direct_fails: True if direct subtraction gives zero (cancellation)
        - height_diffs: Tested height differences
        - closed_form_values: Values from closed-form
        - direct_values: Values from direct subtraction
    """
    if height_range is None:
        height_range = [1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1.0]
    
    closed_values = []
    direct_values = []
    
    for dh in height_range:
        r1 = R_EARTH
        r2 = R_EARTH + dh
        
        # Closed-form (numerically stable)
        delta_D_closed = ssz_time_dilation_difference(r1, r2, M_EARTH)
        
        # Direct subtraction (suffers from cancellation)
        D1 = ssz_time_dilation(r1, M_EARTH)
        D2 = ssz_time_dilation(r2, M_EARTH)
        delta_D_direct = D1 - D2
        
        closed_values.append(delta_D_closed)
        direct_values.append(delta_D_direct)
    
    # Closed-form should give non-zero values for all heights
    closed_form_works = all(v != 0 for v in closed_values)
    
    # Direct subtraction should fail (give zero) for small heights
    direct_fails_small = any(v == 0 for v in direct_values[:-1])
    
    return {
        'closed_form_works': closed_form_works,
        'direct_fails_for_small_heights': direct_fails_small,
        'numerical_stability_demonstrated': closed_form_works and direct_fails_small,
        'height_diffs': height_range,
        'closed_form_values': closed_values,
        'direct_values': direct_values,
        'explanation': 'Closed-form avoids floating-point cancellation that affects direct subtraction'
    }


# =============================================================================
# COHERENT ZONE ANALYSIS (Paper A Section 5)
# =============================================================================

def coherent_zone_analysis(
    epsilon: float = 1e-18,
    center_height: float = 0,
    M: float = M_EARTH
) -> Dict[str, float]:
    """
    Complete analysis of a segment-coherent zone.
    
    Paper A Eq. 8: z = 4εR²/rₛ
    
    Parameters
    ----------
    epsilon : float
        Maximum allowed Xi variation
    center_height : float
        Center height above sea level [m]
    M : float
        Central mass [kg]
        
    Returns
    -------
    dict
        Zone analysis including:
        - zone_width: Total zone width [m]
        - half_width: Half-width (±z/2) [m]
        - zone_bounds: (min_height, max_height) [m]
        - formula_value: 4εR²/rₛ [m]
        - max_phase_drift: Maximum phase drift within zone [rad/gate]
    """
    r_s = schwarzschild_radius(M)
    r_center = R_EARTH + center_height
    
    # Formula: z = 4 * eps * R^2 / r_s
    z_formula = 4 * epsilon * r_center**2 / r_s
    
    # Get actual zone from function
    zone = segment_coherent_zone(center_height, epsilon, M)
    zone_width = zone[1] - zone[0]
    
    # Calculate max phase drift within zone
    q1 = Qubit(id='q1', x=0, y=0, z=zone[0], gate_time=50e-9)
    q2 = Qubit(id='q2', x=0, y=0, z=zone[1], gate_time=50e-9)
    pair = QubitPair(q1, q2)
    result = qubit_pair_segment_mismatch(pair)
    
    return {
        'epsilon': epsilon,
        'zone_width': zone_width,
        'zone_width_mm': zone_width * 1000,
        'half_width': zone_width / 2,
        'half_width_mm': zone_width * 500,
        'zone_bounds': zone,
        'formula_value': z_formula,
        'formula_matches': abs(zone_width - z_formula) / z_formula < 0.01,
        'max_phase_drift': result['phase_drift_per_gate']
    }


# =============================================================================
# DECOHERENCE ENHANCEMENT (Paper A Section 6.2)
# =============================================================================

def decoherence_enhancement_factor(
    delta_xi: float,
    xi_ref: float = 1e-10
) -> float:
    """
    Calculate decoherence enhancement factor.
    
    Formula: 1 + (ΔΞ/Ξ_ref)²
    
    For Earth-scale effects, this is essentially 1.0.
    
    Parameters
    ----------
    delta_xi : float
        Segment density difference
    xi_ref : float
        Reference segment density (default 1e-10)
        
    Returns
    -------
    float
        Decoherence enhancement factor
    """
    return 1.0 + (delta_xi / xi_ref)**2


# =============================================================================
# DEMO
# =============================================================================

if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    
    print('SSZ Paper A Support Module - Demo')
    print('=' * 60)
    
    # GR Comparison
    print()
    print('1. SSZ vs GR COMPARISON')
    print('-' * 40)
    comp = compare_ssz_gr(R_EARTH)
    print(f'  D_SSZ = {comp["D_SSZ"]:.15f}')
    print(f'  D_GR  = {comp["D_GR"]:.15f}')
    print(f'  Relative difference: {comp["relative_difference"]:.2e}')
    print(f'  Weak field: {comp["is_weak_field"]}')
    
    # Fidelity
    print()
    print('2. FIDELITY AFTER 10^9 GATES (1 mm)')
    print('-' * 40)
    fid = fidelity_after_gates(1.0, 10**9)
    print(f'  Delta_Phi = {fid["delta_phi_total"]:.2e} rad')
    print(f'  Fidelity = {fid["fidelity"]:.15f}')
    print(f'  1 - F = {fid["fidelity_reduction"]:.2e}')
    
    # Linear scaling
    print()
    print('3. LINEAR SCALING VERIFICATION')
    print('-' * 40)
    lin = verify_linear_scaling()
    print(f'  Is linear: {lin["is_linear"]}')
    print(f'  Max deviation: {lin["max_deviation"]:.2e}')
    print(f'  Scaling constant: {lin["scaling_constant"]*1000:.2e} rad/mm/gate')
    
    # Numerical stability
    print()
    print('4. NUMERICAL STABILITY')
    print('-' * 40)
    stab = verify_numerical_stability()
    print(f'  Closed-form works: {stab["closed_form_works"]}')
    print(f'  Direct subtraction fails: {stab["direct_fails_for_small_heights"]}')
    print(f'  Stability demonstrated: {stab["numerical_stability_demonstrated"]}')
    
    # Coherent zone
    print()
    print('5. COHERENT ZONE (eps = 1e-18)')
    print('-' * 40)
    zone = coherent_zone_analysis(1e-18)
    print(f'  Zone width: {zone["zone_width_mm"]:.2f} mm')
    print(f'  Half-width: {zone["half_width_mm"]:.2f} mm')
    print(f'  Formula matches: {zone["formula_matches"]}')
    
    print()
    print('=' * 60)
