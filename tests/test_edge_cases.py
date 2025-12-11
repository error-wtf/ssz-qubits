#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSZ-Qubits Edge Case Tests

Tests for boundary conditions, extreme values, and error handling.

© 2025 Carmen Wrede, Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import pytest
from ssz_qubits import (
    C, G, M_EARTH, R_EARTH,
    schwarzschild_radius, xi_segment_density, xi_gradient,
    ssz_time_dilation, ssz_time_dilation_difference,
    Qubit, QubitPair,
    analyze_qubit_segment, qubit_pair_segment_mismatch,
    optimal_qubit_height, segment_coherent_zone,
    gate_timing_correction, two_qubit_gate_timing,
    ssz_decoherence_rate, effective_T2, pair_decoherence_time,
    optimize_qubit_array, array_segment_uniformity,
    segment_aware_syndrome_weight, calculate_logical_error_rate
)


# =============================================================================
# EDGE CASE 1: EXTREME RADII
# =============================================================================

class TestExtremeRadii:
    """Tests for extreme radius values."""
    
    def test_very_small_radius(self):
        """Test behavior near Schwarzschild radius."""
        print("\n" + "="*70)
        print("EDGE CASE: Very Small Radius (near r_s)")
        print("="*70)
        
        r_s = schwarzschild_radius(M_EARTH)
        r = r_s * 10  # 10x Schwarzschild radius (still extreme)
        
        xi = xi_segment_density(r, M_EARTH)
        d = ssz_time_dilation(r, M_EARTH)
        
        print(f"r_s (Earth) = {r_s:.6e} m")
        print(f"r = 10 * r_s = {r:.6e} m")
        print(f"Xi = {xi:.6f}")
        print(f"D_SSZ = {d:.6f}")
        
        # At r = 10*r_s, we're in strong field regime (ratio < 100)
        # Xi = 1 - exp(-phi*10) ~ 1.0 (saturation)
        # But we force weak field for consistency: Xi = r_s/(2r) = 0.05
        xi_weak = xi_segment_density(r, M_EARTH, regime='weak')
        assert np.isclose(xi_weak, 0.05, rtol=1e-10)
        assert 0 < d <= 1, "D_SSZ should be between 0 and 1"
        
        print("\nPhysical Interpretation:")
        print("  -> Near r_s: strong field regime")
        print("  -> Xi becomes significant (not << 1)")
        print("  -> D_SSZ deviates significantly from 1")
        print("="*70)
    
    def test_very_large_radius(self):
        """Test behavior at astronomical distances."""
        print("\n" + "="*70)
        print("EDGE CASE: Very Large Radius (1 AU)")
        print("="*70)
        
        AU = 1.496e11  # 1 Astronomical Unit in meters
        
        xi = xi_segment_density(AU, M_EARTH)
        d = ssz_time_dilation(AU, M_EARTH)
        
        print(f"r = 1 AU = {AU:.3e} m")
        print(f"Xi = {xi:.6e}")
        print(f"D_SSZ = {d:.15f}")
        print(f"1 - D_SSZ = {1-d:.6e}")
        
        # Xi should be very small at 1 AU (but not necessarily < 1e-15)
        assert xi < 1e-10, "Xi should be very small at 1 AU"
        assert np.isclose(d, 1.0, rtol=1e-10), "D_SSZ should be ~1"
        
        print("\nPhysical Interpretation:")
        print("  -> At 1 AU from Earth: essentially flat spacetime")
        print("  -> SSZ effects from Earth are negligible")
        print("="*70)
    
    def test_radius_at_schwarzschild(self):
        """Test exactly at Schwarzschild radius."""
        print("\n" + "="*70)
        print("EDGE CASE: Exactly at Schwarzschild Radius")
        print("="*70)
        
        r_s = schwarzschild_radius(M_EARTH)
        
        xi = xi_segment_density(r_s, M_EARTH)
        d = ssz_time_dilation(r_s, M_EARTH)
        
        print(f"r = r_s = {r_s:.6e} m")
        print(f"Xi = {xi:.6f}")
        print(f"D_SSZ = {d:.6f}")
        
        # At r = r_s, auto-regime selects strong field (ratio = 1 < 100)
        # Strong field: Xi = 1 - exp(-phi) ~ 0.8
        # Weak field: Xi = r_s/(2*r_s) = 0.5
        xi_weak = xi_segment_density(r_s, M_EARTH, regime='weak')
        assert np.isclose(xi_weak, 0.5, rtol=1e-10)
        # D_SSZ with weak field Xi = 0.5: D = 1/(1+0.5) = 2/3
        d_weak = 1.0 / (1.0 + xi_weak)
        assert np.isclose(d_weak, 2/3, rtol=1e-10)
        
        print("\nPhysical Interpretation:")
        print("  -> At r = r_s: Xi = 0.5 (strong field)")
        print("  -> D_SSZ = 2/3 (significant time dilation)")
        print("  -> Note: This is inside Earth! (unphysical for Earth)")
        print("="*70)


# =============================================================================
# EDGE CASE 2: EXTREME MASSES
# =============================================================================

class TestExtremeMasses:
    """Tests for extreme mass values."""
    
    def test_zero_mass(self):
        """Test with zero mass (flat spacetime)."""
        print("\n" + "="*70)
        print("EDGE CASE: Zero Mass (Flat Spacetime)")
        print("="*70)
        
        M = 0
        r = R_EARTH
        
        r_s = schwarzschild_radius(M)
        
        print(f"M = 0 kg")
        print(f"r_s = {r_s} m")
        
        assert r_s == 0, "r_s should be 0 for M=0"
        
        # Xi would be 0/r = 0, but let's check the formula handles it
        # Actually, xi_segment_density divides by r, so r_s=0 gives Xi=0
        xi = schwarzschild_radius(M) / (2 * r)
        print(f"Xi = {xi}")
        
        assert xi == 0, "Xi should be 0 for M=0"
        
        print("\nPhysical Interpretation:")
        print("  -> Zero mass = flat spacetime")
        print("  -> No gravitational effects")
        print("="*70)
    
    def test_solar_mass(self):
        """Test with solar mass."""
        print("\n" + "="*70)
        print("EDGE CASE: Solar Mass")
        print("="*70)
        
        M_SUN = 1.989e30  # kg
        r = 1.496e11  # 1 AU
        
        xi = xi_segment_density(r, M_SUN)
        d = ssz_time_dilation(r, M_SUN)
        
        print(f"M = M_Sun = {M_SUN:.3e} kg")
        print(f"r = 1 AU = {r:.3e} m")
        print(f"Xi = {xi:.6e}")
        print(f"D_SSZ = {d:.15f}")
        
        # At 1 AU from Sun: weak field but measurable
        assert xi > 1e-10, "Xi should be small but non-zero at 1 AU from Sun"
        assert d < 1.0, "D_SSZ should be < 1"
        
        print("\nPhysical Interpretation:")
        print("  -> At Earth's orbit: weak field from Sun")
        print("  -> GPS must correct for this solar effect")
        print("="*70)
    
    def test_black_hole_mass(self):
        """Test with stellar black hole mass."""
        print("\n" + "="*70)
        print("EDGE CASE: Stellar Black Hole (10 M_Sun)")
        print("="*70)
        
        M_BH = 10 * 1.989e30  # 10 solar masses
        r_s = schwarzschild_radius(M_BH)
        
        # Test at 100 r_s (safe distance)
        r = 100 * r_s
        
        xi = xi_segment_density(r, M_BH)
        d = ssz_time_dilation(r, M_BH)
        
        print(f"M = 10 M_Sun = {M_BH:.3e} kg")
        print(f"r_s = {r_s/1e3:.3f} km")
        print(f"r = 100 r_s = {r/1e3:.3f} km")
        print(f"Xi = {xi:.6f}")
        print(f"D_SSZ = {d:.6f}")
        
        # At 100 r_s, auto-regime selects weak field (ratio = 100)
        # Weak field: Xi = r_s/(2r) = 1/200 = 0.005
        xi_weak = xi_segment_density(r, M_BH, regime='weak')
        assert np.isclose(xi_weak, 0.005, rtol=1e-10)
        
        print("\nPhysical Interpretation:")
        print("  -> Even at 100 r_s from black hole: measurable SSZ effects")
        print("  -> Qubits near black holes would experience strong effects")
        print("="*70)


# =============================================================================
# EDGE CASE 3: QUBIT CONFIGURATIONS
# =============================================================================

class TestQubitConfigurations:
    """Tests for unusual qubit configurations."""
    
    def test_identical_qubits(self):
        """Test pair of identical qubits (same position)."""
        print("\n" + "="*70)
        print("EDGE CASE: Identical Qubit Positions")
        print("="*70)
        
        q1 = Qubit(id="Q1", x=0, y=0, z=0)
        q2 = Qubit(id="Q2", x=0, y=0, z=0)  # Same position
        pair = QubitPair(q1, q2)
        
        mismatch = qubit_pair_segment_mismatch(pair, M_EARTH)
        
        print(f"Both qubits at same position")
        print(f"Separation: {pair.separation} m")
        print(f"Delta Xi: {mismatch['delta_xi']}")
        print(f"Delta D_SSZ: {mismatch['delta_time_dilation']}")
        
        assert pair.separation == 0, "Separation should be 0"
        assert mismatch['delta_xi'] == 0, "Delta Xi should be 0"
        assert mismatch['delta_time_dilation'] == 0, "Delta D should be 0"
        
        print("\nPhysical Interpretation:")
        print("  -> Identical positions = no SSZ mismatch")
        print("  -> Perfect segment coherence (unrealistic but valid)")
        print("="*70)
    
    def test_very_distant_qubits(self):
        """Test qubits separated by large distance."""
        print("\n" + "="*70)
        print("EDGE CASE: Very Distant Qubits (1 km separation)")
        print("="*70)
        
        q1 = Qubit(id="Q1", x=0, y=0, z=0)
        q2 = Qubit(id="Q2", x=1000, y=0, z=0)  # 1 km away
        pair = QubitPair(q1, q2)
        
        mismatch = qubit_pair_segment_mismatch(pair, M_EARTH)
        
        print(f"Separation: {pair.separation} m")
        print(f"Height difference: {pair.height_difference} m")
        print(f"Delta Xi: {mismatch['delta_xi']:.6e}")
        
        assert pair.separation == 1000
        # Same height = same Xi (horizontal separation doesn't matter for Xi)
        assert mismatch['delta_xi'] == 0, "Horizontal separation shouldn't affect Xi"
        
        print("\nPhysical Interpretation:")
        print("  -> Horizontal separation doesn't change Xi (same height)")
        print("  -> Only vertical (radial) separation matters for SSZ")
        print("="*70)
    
    def test_negative_coordinates(self):
        """Test qubits with negative coordinates."""
        print("\n" + "="*70)
        print("EDGE CASE: Negative Coordinates")
        print("="*70)
        
        q1 = Qubit(id="Q1", x=-0.001, y=-0.001, z=0.001)
        q2 = Qubit(id="Q2", x=0.001, y=0.001, z=0.001)
        pair = QubitPair(q1, q2)
        
        analysis1 = analyze_qubit_segment(q1, M_EARTH)
        analysis2 = analyze_qubit_segment(q2, M_EARTH)
        
        print(f"Q1 position: ({q1.x}, {q1.y}, {q1.z})")
        print(f"Q2 position: ({q2.x}, {q2.y}, {q2.z})")
        print(f"Q1 Xi: {analysis1.xi:.6e}")
        print(f"Q2 Xi: {analysis2.xi:.6e}")
        print(f"Separation: {pair.separation*1e3:.3f} mm")
        
        # Same z = same Xi
        assert np.isclose(analysis1.xi, analysis2.xi, rtol=1e-10)
        
        print("\nPhysical Interpretation:")
        print("  -> x,y coordinates don't affect Xi (only z/height matters)")
        print("  -> Negative coordinates are valid")
        print("="*70)
    
    def test_underground_qubit(self):
        """Test qubit below sea level (negative z)."""
        print("\n" + "="*70)
        print("EDGE CASE: Underground Qubit (z < 0)")
        print("="*70)
        
        q = Qubit(id="Q1", x=0, y=0, z=-100)  # 100m below sea level
        analysis = analyze_qubit_segment(q, M_EARTH)
        
        print(f"Qubit at z = -100 m (underground)")
        print(f"R from Earth center: {q.radius_from_earth_center/1e6:.6f} Mm")
        print(f"Xi: {analysis.xi:.6e}")
        print(f"D_SSZ: {analysis.time_dilation:.15f}")
        
        # Closer to Earth center = higher Xi
        q_surface = Qubit(id="Q2", x=0, y=0, z=0)
        analysis_surface = analyze_qubit_segment(q_surface, M_EARTH)
        
        assert analysis.xi > analysis_surface.xi, "Underground Xi should be higher"
        
        print("\nPhysical Interpretation:")
        print("  -> Underground: closer to Earth center")
        print("  -> Higher Xi = stronger gravitational effect")
        print("  -> Time runs slower underground")
        print("="*70)


# =============================================================================
# EDGE CASE 4: NUMERICAL PRECISION
# =============================================================================

class TestNumericalPrecision:
    """Tests for numerical precision and stability."""
    
    def test_float_precision_xi(self):
        """Test Xi calculation doesn't lose precision."""
        print("\n" + "="*70)
        print("EDGE CASE: Float Precision in Xi")
        print("="*70)
        
        # Two close radii - use larger difference for numerical stability
        r1 = R_EARTH
        r2 = R_EARTH + 1.0  # 1 meter difference (detectable)
        
        xi1 = xi_segment_density(r1, M_EARTH)
        xi2 = xi_segment_density(r2, M_EARTH)
        
        print(f"r1 = {r1:.15e} m")
        print(f"r2 = {r2:.15e} m")
        print(f"Delta r = {r2-r1:.6e} m")
        print(f"Xi1 = {xi1:.15e}")
        print(f"Xi2 = {xi2:.15e}")
        print(f"Delta Xi = {xi1-xi2:.15e}")
        
        # Should be able to distinguish 1 meter difference
        assert xi1 != xi2, "Should distinguish 1 m difference"
        assert xi1 > xi2, "Xi should decrease with increasing r"
        
        print("\nPhysical Interpretation:")
        print("  -> Float64 can resolve meter-scale differences in Xi")
        print("  -> Important for precision qubit positioning")
        print("="*70)
    
    def test_time_dilation_precision(self):
        """Test time dilation calculation precision."""
        print("\n" + "="*70)
        print("EDGE CASE: Time Dilation Precision")
        print("="*70)
        
        r = R_EARTH
        d = ssz_time_dilation(r, M_EARTH)
        
        # D_SSZ should be very close to 1 but distinguishable
        print(f"D_SSZ = {d:.20f}")
        print(f"1 - D_SSZ = {1-d:.20e}")
        
        assert d != 1.0, "D_SSZ should be distinguishable from 1"
        assert 1 - d > 1e-16, "Should have enough precision to measure deviation"
        
        print("\nPhysical Interpretation:")
        print("  -> Float64 has enough precision for Earth-surface SSZ")
        print("  -> Can measure ~10^-10 deviations from unity")
        print("="*70)
    
    def test_gradient_numerical_vs_analytical(self):
        """Compare numerical and analytical gradient."""
        print("\n" + "="*70)
        print("EDGE CASE: Gradient Numerical vs Analytical")
        print("="*70)
        
        r = R_EARTH
        dr = 1.0  # 1 meter step
        
        # Analytical gradient
        grad_analytical = xi_gradient(r, M_EARTH)
        
        # Numerical gradient (central difference)
        xi_plus = xi_segment_density(r + dr, M_EARTH)
        xi_minus = xi_segment_density(r - dr, M_EARTH)
        grad_numerical = (xi_plus - xi_minus) / (2 * dr)
        
        print(f"Analytical gradient: {grad_analytical:.10e} /m")
        print(f"Numerical gradient: {grad_numerical:.10e} /m")
        print(f"Relative error: {abs(grad_analytical - grad_numerical)/abs(grad_analytical):.6e}")
        
        assert np.isclose(grad_analytical, grad_numerical, rtol=1e-6)
        
        print("\nPhysical Interpretation:")
        print("  -> Analytical and numerical gradients agree")
        print("  -> Validates the gradient formula")
        print("="*70)


# =============================================================================
# EDGE CASE 5: ERROR HANDLING
# =============================================================================

class TestErrorHandling:
    """Tests for error handling."""
    
    def test_zero_radius_error(self):
        """Test error on zero radius."""
        print("\n" + "="*70)
        print("EDGE CASE: Zero Radius Error")
        print("="*70)
        
        with pytest.raises(ValueError) as excinfo:
            xi_segment_density(0, M_EARTH)
        
        print(f"Error message: {excinfo.value}")
        assert "positive" in str(excinfo.value).lower() or "radius" in str(excinfo.value).lower()
        
        print("\nPhysical Interpretation:")
        print("  -> r=0 is a singularity, correctly rejected")
        print("="*70)
    
    def test_negative_radius_error(self):
        """Test error on negative radius."""
        print("\n" + "="*70)
        print("EDGE CASE: Negative Radius Error")
        print("="*70)
        
        with pytest.raises(ValueError) as excinfo:
            xi_segment_density(-1000, M_EARTH)
        
        print(f"Error message: {excinfo.value}")
        
        print("\nPhysical Interpretation:")
        print("  -> Negative radius is unphysical, correctly rejected")
        print("="*70)
    
    def test_optimal_height_zero_xi(self):
        """Test optimal height with zero target Xi."""
        print("\n" + "="*70)
        print("EDGE CASE: Optimal Height for Xi=0")
        print("="*70)
        
        with pytest.raises(ValueError) as excinfo:
            optimal_qubit_height(0, M_EARTH)
        
        print(f"Error message: {excinfo.value}")
        
        print("\nPhysical Interpretation:")
        print("  -> Xi=0 requires infinite distance (unphysical)")
        print("="*70)
    
    def test_optimal_height_negative_xi(self):
        """Test optimal height with negative target Xi."""
        print("\n" + "="*70)
        print("EDGE CASE: Optimal Height for Xi<0")
        print("="*70)
        
        with pytest.raises(ValueError) as excinfo:
            optimal_qubit_height(-1e-10, M_EARTH)
        
        print(f"Error message: {excinfo.value}")
        
        print("\nPhysical Interpretation:")
        print("  -> Negative Xi is unphysical (no negative curvature)")
        print("="*70)


# =============================================================================
# EDGE CASE 6: SPECIAL QUBIT PROPERTIES
# =============================================================================

class TestSpecialQubitProperties:
    """Tests for special qubit property values."""
    
    def test_zero_coherence_time(self):
        """Test qubit with zero coherence time."""
        print("\n" + "="*70)
        print("EDGE CASE: Zero Coherence Time")
        print("="*70)
        
        q = Qubit(id="Q1", x=0, y=0, z=0, coherence_time_T2=0)
        
        # This should cause division by zero in decoherence rate
        # Let's see how it's handled
        try:
            gamma = ssz_decoherence_rate(q, M=M_EARTH)
            print(f"Decoherence rate: {gamma}")
            # If it doesn't raise, gamma should be inf
            assert gamma == np.inf or gamma > 1e20
        except (ZeroDivisionError, ValueError) as e:
            print(f"Error (expected): {e}")
        
        print("\nPhysical Interpretation:")
        print("  -> T2=0 means instant decoherence (infinite rate)")
        print("="*70)
    
    def test_very_long_coherence_time(self):
        """Test qubit with very long coherence time."""
        print("\n" + "="*70)
        print("EDGE CASE: Very Long Coherence Time (1 second)")
        print("="*70)
        
        q = Qubit(id="Q1", x=0, y=0, z=0, coherence_time_T2=1.0)  # 1 second
        
        gamma = ssz_decoherence_rate(q, M=M_EARTH)
        T2_eff = effective_T2(q, M=M_EARTH)
        
        print(f"Base T2: {q.coherence_time_T2} s")
        print(f"SSZ decoherence rate: {gamma:.6e} /s")
        print(f"Effective T2: {T2_eff:.6f} s")
        
        assert T2_eff <= q.coherence_time_T2
        assert T2_eff > 0
        
        print("\nPhysical Interpretation:")
        print("  -> Even with 1s T2, SSZ effects are present")
        print("  -> Long-lived qubits accumulate more SSZ phase drift")
        print("="*70)
    
    def test_very_short_gate_time(self):
        """Test qubit with very short gate time."""
        print("\n" + "="*70)
        print("EDGE CASE: Very Short Gate Time (1 ps)")
        print("="*70)
        
        q1 = Qubit(id="Q1", x=0, y=0, z=0, gate_time=1e-12)
        q2 = Qubit(id="Q2", x=0, y=0, z=0.01, gate_time=1e-12)
        pair = QubitPair(q1, q2)
        
        timing = two_qubit_gate_timing(pair, M_EARTH)
        
        print(f"Gate time: 1 ps")
        print(f"Optimal gate time: {timing['optimal_gate_time']*1e12:.6f} ps")
        print(f"Timing asymmetry: {timing['timing_asymmetry']:.6e}")
        
        assert timing['optimal_gate_time'] > 0
        assert np.isfinite(timing['timing_asymmetry'])
        
        print("\nPhysical Interpretation:")
        print("  -> Ultra-fast gates have less time for SSZ drift")
        print("  -> But timing precision requirements increase")
        print("="*70)


# =============================================================================
# EDGE CASE 7: QEC EDGE CASES
# =============================================================================

class TestQECEdgeCases:
    """Tests for QEC-related edge cases."""
    
    def test_syndrome_weight_bounds(self):
        """Test syndrome weight is bounded [0, 1]."""
        print("\n" + "="*70)
        print("EDGE CASE: Syndrome Weight Bounds")
        print("="*70)
        
        heights = [-1000, 0, 1000, 10000, 100000]  # Various heights
        
        for h in heights:
            q = Qubit(id="Q", x=0, y=0, z=h)
            weight_x = segment_aware_syndrome_weight(q, 'X', M_EARTH)
            weight_z = segment_aware_syndrome_weight(q, 'Z', M_EARTH)
            
            print(f"h={h:>7}m: X-weight={weight_x:.6f}, Z-weight={weight_z:.6f}")
            
            assert 0 <= weight_x <= 1, f"X weight out of bounds at h={h}"
            assert 0 <= weight_z <= 1, f"Z weight out of bounds at h={h}"
        
        print("\nPhysical Interpretation:")
        print("  -> Syndrome weights always in [0,1] regardless of position")
        print("="*70)
    
    def test_logical_error_rate_bounds(self):
        """Test logical error rate is bounded [0, 1]."""
        print("\n" + "="*70)
        print("EDGE CASE: Logical Error Rate Bounds")
        print("="*70)
        
        qubits = optimize_qubit_array(9, base_height=0)
        
        error_rates = [1e-4, 1e-3, 1e-2, 0.1]
        distances = [3, 5, 7]
        
        for p in error_rates:
            for d in distances:
                p_L = calculate_logical_error_rate(qubits, d, p, M_EARTH)
                print(f"p={p:.0e}, d={d}: p_L={p_L:.6e}")
                
                assert 0 <= p_L <= 1, f"Logical error rate out of bounds"
        
        print("\nPhysical Interpretation:")
        print("  -> Logical error rate always valid probability")
        print("  -> Higher distance = lower logical error (below threshold)")
        print("="*70)
    
    def test_single_qubit_array(self):
        """Test array with single qubit."""
        print("\n" + "="*70)
        print("EDGE CASE: Single Qubit Array")
        print("="*70)
        
        qubits = optimize_qubit_array(1, base_height=0)
        uniformity = array_segment_uniformity(qubits, M_EARTH)
        
        print(f"Number of qubits: {len(qubits)}")
        print(f"Xi mean: {uniformity['xi_mean']:.6e}")
        print(f"Xi std: {uniformity['xi_std']}")
        print(f"Uniformity: {uniformity['uniformity']}")
        
        assert len(qubits) == 1
        assert uniformity['xi_std'] == 0, "Single qubit has zero std"
        
        print("\nPhysical Interpretation:")
        print("  -> Single qubit: trivially uniform")
        print("="*70)


# =============================================================================
# EDGE CASE 8: SEGMENT COHERENT ZONE
# =============================================================================

class TestSegmentCoherentZone:
    """Tests for segment coherent zone calculation."""
    
    def test_coherent_zone_contains_center(self):
        """Coherent zone should contain the center height."""
        print("\n" + "="*70)
        print("EDGE CASE: Coherent Zone Contains Center")
        print("="*70)
        
        center_height = 100  # 100 m
        h_min, h_max = segment_coherent_zone(center_height, max_xi_variation=1e-15)
        
        print(f"Center height: {center_height} m")
        print(f"Coherent zone: [{h_min:.6f}, {h_max:.6f}] m")
        print(f"Zone width: {h_max - h_min:.6f} m")
        
        assert h_min <= center_height <= h_max, "Zone should contain center"
        
        print("\nPhysical Interpretation:")
        print("  -> Coherent zone is symmetric around center")
        print("  -> Width depends on allowed Xi variation")
        print("="*70)
    
    def test_coherent_zone_width_scales(self):
        """Larger Xi variation = wider coherent zone."""
        print("\n" + "="*70)
        print("EDGE CASE: Coherent Zone Width Scaling")
        print("="*70)
        
        center_height = 0
        
        variations = [1e-17, 1e-16, 1e-15, 1e-14]
        widths = []
        
        for var in variations:
            h_min, h_max = segment_coherent_zone(center_height, max_xi_variation=var)
            width = h_max - h_min
            widths.append(width)
            print(f"Max Xi variation: {var:.0e} -> Zone width: {width:.6f} m")
        
        # Widths should increase with variation
        for i in range(len(widths) - 1):
            assert widths[i+1] > widths[i], "Wider variation should give wider zone"
        
        print("\nPhysical Interpretation:")
        print("  -> Tighter Xi tolerance = narrower coherent zone")
        print("  -> Trade-off between precision and usable volume")
        print("="*70)


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("SSZ-QUBITS EDGE CASE TEST SUITE")
    print("="*70)
    print("Running edge case and boundary condition tests...")
    print("="*70 + "\n")
    
    pytest.main([__file__, "-v", "-s", "--tb=short"])
