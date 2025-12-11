#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSZ-Qubits Physics Tests

Tests for the SSZ framework with TWO REGIMES:

1. WEAK FIELD (r >> r_s, e.g. Earth):
   Xi(r) = r_s / (2r)
   D_SSZ(r) = 1 / (1 + Xi(r)) ~ 1 - Xi(r)

2. STRONG FIELD (r ~ r_s, e.g. black holes):
   Xi(r) = 1 - exp(-phi * r / r_s)
   D_SSZ(r) = 1 / (1 + Xi(r))

For qubit applications on Earth, we use the WEAK FIELD regime.

(c) 2025 Carmen Wrede, Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import pytest
from ssz_qubits import (
    # Constants
    C, G, HBAR, M_EARTH, R_EARTH, PHI,
    # Core functions
    schwarzschild_radius, xi_segment_density, xi_gradient,
    ssz_time_dilation, ssz_time_dilation_difference, time_difference_per_second,
    # Qubit functions
    Qubit, QubitPair, SegmentAnalysis,
    analyze_qubit_segment, qubit_pair_segment_mismatch,
    optimize_qubit_array, array_segment_uniformity,
    height_to_time_offset
)


# =============================================================================
# TEST 1: SCHWARZSCHILD RADIUS
# =============================================================================

class TestSchwarzschildRadius:
    """Tests for Schwarzschild radius calculation."""
    
    def test_earth_schwarzschild_radius(self):
        """Earth's Schwarzschild radius should be ~8.87 mm."""
        print("\n" + "="*70)
        print("TEST: Earth Schwarzschild Radius")
        print("="*70)
        
        r_s = schwarzschild_radius(M_EARTH)
        expected = 2 * G * M_EARTH / C**2
        
        print(f"Calculated r_s = {r_s*1e3:.6f} mm")
        print(f"Expected r_s = {expected*1e3:.6f} mm")
        
        assert 8.8e-3 < r_s < 8.9e-3
        assert np.isclose(r_s, expected, rtol=1e-10)
        
        print("\nPhysical Interpretation:")
        print("  -> Earth's r_s is tiny: ~8.87 mm")
        print(f"  -> r_s/R_Earth = {r_s/R_EARTH:.2e}")
        print("="*70)
    
    def test_sun_schwarzschild_radius(self):
        """Sun's Schwarzschild radius should be ~2.95 km."""
        print("\n" + "="*70)
        print("TEST: Sun Schwarzschild Radius")
        print("="*70)
        
        M_SUN = 1.989e30
        r_s = schwarzschild_radius(M_SUN)
        
        print(f"Calculated r_s = {r_s/1e3:.3f} km")
        
        assert 2.9e3 < r_s < 3.0e3
        print("="*70)


# =============================================================================
# TEST 2: SEGMENT DENSITY Xi (WEAK FIELD - Earth)
# =============================================================================

class TestSegmentDensityWeakField:
    """Tests for SSZ segment density in WEAK FIELD regime.
    
    WEAK FIELD FORMULA: Xi(r) = r_s / (2r)
    
    Properties:
        - Xi decreases as 1/r
        - Xi << 1 for r >> r_s
        - Valid for Earth, Solar System, GPS
    """
    
    def test_xi_at_earth_surface(self):
        """Xi at Earth's surface should be ~7e-10."""
        print("\n" + "="*70)
        print("TEST: Xi at Earth Surface (Weak Field)")
        print("="*70)
        
        xi = xi_segment_density(R_EARTH, M_EARTH)
        
        print(f"Xi(R_Earth) = {xi:.6e}")
        print(f"Expected ~ 7e-10 (weak field)")
        
        # Earth surface: Xi ~ r_s/(2*R_Earth) ~ 8.87mm / (2 * 6371km) ~ 7e-10
        assert 6e-10 < xi < 8e-10
        
        print("\nPhysical Interpretation:")
        print("  -> Xi << 1 confirms Earth's surface is in weak-field regime")
        print("  -> SSZ effects are small but measurable with precision instruments")
        print("="*70)
    
    def test_xi_decreases_with_radius(self):
        """Xi should decrease as 1/r in weak field."""
        print("\n" + "="*70)
        print("TEST: Xi Decreases with Radius (1/r scaling)")
        print("="*70)
        
        r1 = R_EARTH
        r2 = 2 * R_EARTH
        
        xi1 = xi_segment_density(r1, M_EARTH)
        xi2 = xi_segment_density(r2, M_EARTH)
        
        ratio = xi1 / xi2
        print(f"Xi(R) = {xi1:.6e}")
        print(f"Xi(2R) = {xi2:.6e}")
        print(f"Xi(R)/Xi(2R) = {ratio:.6f}")
        
        assert np.isclose(ratio, 2.0, rtol=1e-10), "Xi should scale as 1/r"
        
        print("\nPhysical Interpretation:")
        print("  -> Xi = r_s/(2r) falls off as 1/r")
        print("  -> Doubling distance halves segment density")
        print("="*70)
    
    def test_xi_positive_definite(self):
        """Xi should always be positive for r > 0."""
        print("\n" + "="*70)
        print("TEST: Xi Positive Definite")
        print("="*70)
        
        radii = [1e3, 1e6, R_EARTH, 1e9, 1e12]
        
        print(f"{'Radius [m]':>15} | {'Xi':>15}")
        print("-" * 35)
        
        for r in radii:
            xi = xi_segment_density(r, M_EARTH)
            print(f"{r:>15.2e} | {xi:>15.6e}")
            assert xi > 0
        
        print("="*70)
    
    def test_xi_formula_weak_field(self):
        """Verify Xi = r_s/(2r) in weak field."""
        print("\n" + "="*70)
        print("TEST: Xi Formula Verification (Weak Field)")
        print("="*70)
        
        r = R_EARTH + 1000  # 1 km altitude
        r_s = schwarzschild_radius(M_EARTH)
        
        xi_calculated = xi_segment_density(r, M_EARTH)
        xi_expected = r_s / (2 * r)
        
        print(f"Xi (function) = {xi_calculated:.10e}")
        print(f"r_s/(2r) = {xi_expected:.10e}")
        
        assert np.isclose(xi_calculated, xi_expected, rtol=1e-14)
        print("="*70)


# =============================================================================
# TEST 3: SEGMENT GRADIENT (WEAK FIELD)
# =============================================================================

class TestSegmentGradientWeakField:
    """Tests for segment density gradient in WEAK FIELD.
    
    WEAK FIELD: dXi/dr = -r_s / (2r^2)
    Gradient is NEGATIVE (Xi decreases with r)
    """
    
    def test_gradient_negative(self):
        """Gradient should be NEGATIVE in weak field."""
        print("\n" + "="*70)
        print("TEST: Gradient is Negative (Weak Field)")
        print("="*70)
        
        grad = xi_gradient(R_EARTH, M_EARTH)
        
        print(f"dXi/dr at Earth surface = {grad:.6e} /m")
        
        assert grad < 0, "Gradient must be negative in weak field"
        
        print("\nPhysical Interpretation:")
        print("  -> Xi DECREASES with r (weak field)")
        print("  -> Moving away from mass reduces segment density")
        print("="*70)
    
    def test_gradient_scales_as_1_over_r_squared(self):
        """Gradient magnitude should scale as 1/r^2."""
        print("\n" + "="*70)
        print("TEST: Gradient 1/r^2 Scaling")
        print("="*70)
        
        r1 = R_EARTH
        r2 = 2 * R_EARTH
        
        grad1 = abs(xi_gradient(r1, M_EARTH))
        grad2 = abs(xi_gradient(r2, M_EARTH))
        
        ratio = grad1 / grad2
        print(f"|dXi/dr|(R) = {grad1:.6e} /m")
        print(f"|dXi/dr|(2R) = {grad2:.6e} /m")
        print(f"Ratio = {ratio:.6f}")
        print(f"Expected (2R/R)^2 = 4.0")
        
        assert np.isclose(ratio, 4.0, rtol=1e-10)
        print("="*70)


# =============================================================================
# TEST 4: SSZ TIME DILATION (WEAK FIELD)
# =============================================================================

class TestSSZTimeDilationWeakField:
    """Tests for SSZ time dilation in WEAK FIELD.
    
    D_SSZ(r) = 1 / (1 + Xi(r)) ~ 1 - Xi(r) for Xi << 1
    """
    
    def test_time_dilation_at_earth_surface(self):
        """D_SSZ at Earth surface should be very close to 1."""
        print("\n" + "="*70)
        print("TEST: D_SSZ at Earth Surface")
        print("="*70)
        
        d = ssz_time_dilation(R_EARTH, M_EARTH)
        
        print(f"D_SSZ(R_Earth) = {d:.15f}")
        print(f"Deviation from 1 = {1-d:.6e}")
        
        assert 0.9999999 < d < 1.0
        
        print("\nPhysical Interpretation:")
        print("  -> D_SSZ ~ 1 - Xi ~ 0.9999999993")
        print("  -> Time runs ~0.7 nanoseconds slower per second")
        print("="*70)
    
    def test_time_dilation_formula(self):
        """Verify D_SSZ = 1/(1+Xi)."""
        print("\n" + "="*70)
        print("TEST: D_SSZ Formula Verification")
        print("="*70)
        
        r = R_EARTH + 1000
        
        xi = xi_segment_density(r, M_EARTH)
        d_calculated = ssz_time_dilation(r, M_EARTH)
        d_expected = 1.0 / (1.0 + xi)
        
        print(f"Xi = {xi:.6e}")
        print(f"D_SSZ (function) = {d_calculated:.15f}")
        print(f"1/(1+Xi) = {d_expected:.15f}")
        
        assert np.isclose(d_calculated, d_expected, rtol=1e-14)
        print("="*70)
    
    def test_time_dilation_increases_with_altitude(self):
        """Time should run faster at higher altitude (larger D_SSZ)."""
        print("\n" + "="*70)
        print("TEST: Time Dilation Altitude Dependence")
        print("="*70)
        
        heights = [0, 100, 1000, 10000]
        
        print(f"{'Height [m]':>12} | {'D_SSZ':>20}")
        print("-" * 40)
        
        d_sea = ssz_time_dilation(R_EARTH, M_EARTH)
        prev_d = d_sea
        
        for h in heights:
            r = R_EARTH + h
            d = ssz_time_dilation(r, M_EARTH)
            print(f"{h:>12} | {d:>20.15f}")
            
            assert d >= prev_d, "D_SSZ should increase with altitude"
            prev_d = d
        
        print("\nPhysical Interpretation:")
        print("  -> Time runs FASTER at higher altitude")
        print("  -> This is the gravitational time dilation effect")
        print("="*70)


# =============================================================================
# TEST 5: QUBIT ANALYSIS (WEAK FIELD)
# =============================================================================

class TestQubitAnalysisWeakField:
    """Tests for qubit SSZ analysis in weak field."""
    
    def test_qubit_at_earth_surface(self):
        """Analyze qubit at Earth's surface."""
        print("\n" + "="*70)
        print("TEST: Qubit at Earth Surface")
        print("="*70)
        
        q = Qubit(id="Q1", x=0, y=0, z=0)
        analysis = analyze_qubit_segment(q, M_EARTH)
        
        print(f"Position: z = {q.z} m (sea level)")
        print(f"Xi = {analysis.xi:.6e}")
        print(f"D_SSZ = {analysis.time_dilation:.15f}")
        print(f"dXi/dr = {analysis.segment_gradient:.6e}")
        
        # Weak field: Xi ~ 7e-10, D_SSZ ~ 1
        assert 6e-10 < analysis.xi < 8e-10
        assert 0.9999999 < analysis.time_dilation < 1.0
        assert analysis.segment_gradient < 0  # Negative in weak field
        
        print("\nPhysical Interpretation:")
        print("  -> Earth surface is in weak-field regime")
        print("  -> Xi ~ 7e-10, D_SSZ ~ 0.9999999993")
        print("="*70)
    
    def test_qubit_pair_mismatch(self):
        """Test segment mismatch for qubit pair."""
        print("\n" + "="*70)
        print("TEST: Qubit Pair Segment Mismatch")
        print("="*70)
        
        q1 = Qubit(id="Q1", x=0, y=0, z=0)
        q2 = Qubit(id="Q2", x=0, y=0, z=1000)  # 1 km higher
        pair = QubitPair(q1, q2)
        
        mismatch = qubit_pair_segment_mismatch(pair, M_EARTH)
        
        print(f"Height difference: {pair.height_difference} m")
        print(f"Delta Xi: {mismatch['delta_xi']:.6e}")
        print(f"Delta D_SSZ: {mismatch['delta_time_dilation']:.6e}")
        
        # Should have measurable mismatch
        assert mismatch['delta_xi'] > 0
        assert mismatch['delta_time_dilation'] > 0
        
        print("\nPhysical Interpretation:")
        print("  -> Height difference causes segment mismatch")
        print("  -> This affects two-qubit gate fidelity")
        print("="*70)


# =============================================================================
# TEST 6: GOLDEN RATIO
# =============================================================================

class TestGoldenRatio:
    """Tests for golden ratio in SSZ."""
    
    def test_phi_value(self):
        """Verify phi = (1+sqrt(5))/2."""
        print("\n" + "="*70)
        print("TEST: Golden Ratio Value")
        print("="*70)
        
        phi_expected = (1 + np.sqrt(5)) / 2
        
        print(f"PHI (constant) = {PHI:.15f}")
        print(f"(1+sqrt(5))/2 = {phi_expected:.15f}")
        
        assert np.isclose(PHI, phi_expected, rtol=1e-15)
        print("="*70)
    
    def test_phi_property(self):
        """Verify phi^2 = phi + 1."""
        print("\n" + "="*70)
        print("TEST: Golden Ratio Property")
        print("="*70)
        
        phi_squared = PHI ** 2
        phi_plus_one = PHI + 1
        
        print(f"phi^2 = {phi_squared:.15f}")
        print(f"phi + 1 = {phi_plus_one:.15f}")
        
        assert np.isclose(phi_squared, phi_plus_one, rtol=1e-14)
        print("="*70)


# =============================================================================
# TEST 7: STRONG FIELD REGIME (for completeness)
# =============================================================================

class TestStrongFieldRegime:
    """Tests for SSZ in STRONG FIELD regime (r ~ r_s).
    
    STRONG FIELD FORMULA: Xi(r) = 1 - exp(-phi * r / r_s)
    
    Properties:
        - Xi(0) = 0 (singularity-free!)
        - Xi(inf) -> 1 (saturation)
        - D_SSZ(r_s) ~ 0.555 (finite at horizon!)
    """
    
    def test_strong_field_xi_at_schwarzschild(self):
        """Xi at r_s should be ~0.8 in strong field."""
        print("\n" + "="*70)
        print("TEST: Xi at Schwarzschild Radius (Strong Field)")
        print("="*70)
        
        M_BH = 10 * 1.989e30  # 10 solar mass black hole
        r_s = schwarzschild_radius(M_BH)
        
        xi = xi_segment_density(r_s, M_BH, regime='strong')
        
        print(f"Xi(r_s) = {xi:.6f}")
        print(f"Expected ~ 0.8 (from 1 - exp(-phi))")
        
        # Xi(r_s) = 1 - exp(-phi) ~ 0.8
        assert 0.79 < xi < 0.81
        
        print("\nPhysical Interpretation:")
        print("  -> Strong field uses saturation formula")
        print("  -> Xi ~ 0.8 at Schwarzschild radius")
        print("="*70)
    
    def test_strong_field_d_ssz_finite_at_horizon(self):
        """D_SSZ should be FINITE at r_s (unlike GR!)."""
        print("\n" + "="*70)
        print("TEST: D_SSZ Finite at Horizon (Strong Field)")
        print("="*70)
        
        M_BH = 10 * 1.989e30
        r_s = schwarzschild_radius(M_BH)
        
        # Force strong field regime
        xi = xi_segment_density(r_s, M_BH, regime='strong')
        d = 1.0 / (1.0 + xi)
        
        print(f"D_SSZ(r_s) = {d:.6f}")
        print(f"Expected ~ 0.555")
        
        assert 0.5 < d < 0.6
        assert np.isfinite(d)
        
        print("\nPhysical Interpretation:")
        print("  -> GR: D_GR(r_s) = 0 (singularity!)")
        print("  -> SSZ: D_SSZ(r_s) ~ 0.555 (FINITE!)")
        print("  -> SSZ resolves event horizon singularity")
        print("="*70)


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s", "--tb=short"])
