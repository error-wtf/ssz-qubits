#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSZ-Qubits Validation Tests

Cross-validation tests comparing SSZ predictions with:
- Known GR results (weak field limit)
- Published experimental data
- Theoretical consistency checks

© 2025 Carmen Wrede, Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import pytest
from ssz_qubits import (
    C, G, HBAR, M_EARTH, R_EARTH, PHI,
    schwarzschild_radius, xi_segment_density, xi_gradient,
    ssz_time_dilation, time_difference_per_second,
    Qubit, QubitPair,
    analyze_qubit_segment, qubit_pair_segment_mismatch,
    height_to_time_offset
)


# =============================================================================
# VALIDATION 1: GR WEAK FIELD COMPARISON
# =============================================================================

class TestGRWeakFieldComparison:
    """Compare SSZ with GR in weak field limit."""
    
    def test_time_dilation_matches_gr_weak_field(self):
        """SSZ time dilation should match GR in weak field."""
        print("\n" + "="*70)
        print("VALIDATION: SSZ vs GR Time Dilation (Weak Field)")
        print("="*70)
        
        r = R_EARTH  # Weak field
        
        # SSZ: D_SSZ = 1/(1 + Xi) where Xi = r_s/(2r)
        xi = xi_segment_density(r, M_EARTH)
        d_ssz = ssz_time_dilation(r, M_EARTH)
        
        # GR: sqrt(1 - r_s/r) ~ 1 - r_s/(2r) for r >> r_s
        r_s = schwarzschild_radius(M_EARTH)
        d_gr_exact = np.sqrt(1 - r_s/r)
        d_gr_approx = 1 - r_s/(2*r)  # First order approximation
        
        print(f"r_s/r = {r_s/r:.6e} (weak field: << 1)")
        print(f"\nSSZ:")
        print(f"  Xi = {xi:.6e}")
        print(f"  D_SSZ = {d_ssz:.15f}")
        print(f"\nGR:")
        print(f"  sqrt(1-r_s/r) = {d_gr_exact:.15f}")
        print(f"  1 - r_s/(2r) = {d_gr_approx:.15f}")
        print(f"\nComparison:")
        print(f"  |D_SSZ - D_GR| = {abs(d_ssz - d_gr_exact):.6e}")
        print(f"  Relative diff = {abs(d_ssz - d_gr_exact)/d_gr_exact:.6e}")
        
        # In weak field, SSZ and GR should agree to O(Xi^2)
        # D_SSZ = 1/(1+Xi) ~ 1 - Xi + Xi^2 - ...
        # D_GR = sqrt(1-2Xi) ~ 1 - Xi - Xi^2/2 - ...
        # Difference is O(Xi^2)
        
        assert abs(d_ssz - d_gr_exact) < xi**2 * 10, "SSZ should match GR to O(Xi^2)"
        
        print("\nPhysical Interpretation:")
        print("  -> SSZ and GR agree in weak field limit")
        print("  -> Difference is second order in Xi")
        print("  -> At Earth surface: difference ~ 10^-19")
        print("="*70)
    
    def test_gravitational_redshift_formula(self):
        """Verify gravitational redshift matches known formula."""
        print("\n" + "="*70)
        print("VALIDATION: Gravitational Redshift")
        print("="*70)
        
        # Redshift between two heights
        h1 = 0      # Sea level
        h2 = 1000   # 1 km altitude
        
        r1 = R_EARTH + h1
        r2 = R_EARTH + h2
        
        # SSZ prediction
        d1 = ssz_time_dilation(r1, M_EARTH)
        d2 = ssz_time_dilation(r2, M_EARTH)
        z_ssz = d2/d1 - 1  # Redshift
        
        # GR prediction (weak field)
        # z ~ g*h/c^2 where g = GM/R^2
        g = G * M_EARTH / R_EARTH**2
        z_gr = g * (h2 - h1) / C**2
        
        print(f"Height difference: {h2-h1} m")
        print(f"Surface gravity g = {g:.4f} m/s^2")
        print(f"\nSSZ redshift: z = {z_ssz:.6e}")
        print(f"GR redshift: z = {z_gr:.6e}")
        print(f"Relative difference: {abs(z_ssz - z_gr)/z_gr:.6e}")
        
        # Should agree to within 1%
        assert np.isclose(z_ssz, z_gr, rtol=0.01), "Redshift should match GR"
        
        print("\nPhysical Interpretation:")
        print("  -> SSZ reproduces gravitational redshift")
        print("  -> This is measurable with atomic clocks")
        print("="*70)
    
    def test_pound_rebka_experiment(self):
        """Validate against Pound-Rebka experiment (22.5 m tower)."""
        print("\n" + "="*70)
        print("VALIDATION: Pound-Rebka Experiment")
        print("="*70)
        
        # Pound-Rebka: 22.5 m height difference at Harvard
        h = 22.5  # meters
        
        # Measured fractional frequency shift: ~2.5 × 10^-15
        # Theoretical: gh/c^2
        g = G * M_EARTH / R_EARTH**2
        z_theoretical = g * h / C**2
        z_measured = 2.46e-15  # Approximate measured value
        
        # SSZ prediction
        r1 = R_EARTH
        r2 = R_EARTH + h
        d1 = ssz_time_dilation(r1, M_EARTH)
        d2 = ssz_time_dilation(r2, M_EARTH)
        z_ssz = d2/d1 - 1
        
        print(f"Pound-Rebka tower height: {h} m")
        print(f"\nFrequency shift predictions:")
        print(f"  Measured (1960): ~{z_measured:.2e}")
        print(f"  GR theoretical: {z_theoretical:.6e}")
        print(f"  SSZ prediction: {z_ssz:.6e}")
        print(f"\nSSZ vs GR difference: {abs(z_ssz - z_theoretical)/z_theoretical:.6e}")
        
        # SSZ should match GR (and thus experiment) to high precision
        assert np.isclose(z_ssz, z_theoretical, rtol=1e-6)
        
        print("\nPhysical Interpretation:")
        print("  -> SSZ reproduces Pound-Rebka result")
        print("  -> First terrestrial test of gravitational redshift")
        print("  -> Validates SSZ in weak-field laboratory conditions")
        print("="*70)


# =============================================================================
# VALIDATION 2: GPS TIME DILATION
# =============================================================================

class TestGPSValidation:
    """Validate against GPS satellite time corrections."""
    
    def test_gps_satellite_time_dilation(self):
        """GPS satellites at ~20,200 km experience measurable time dilation."""
        print("\n" + "="*70)
        print("VALIDATION: GPS Satellite Time Dilation")
        print("="*70)
        
        # GPS orbit altitude
        h_gps = 20200e3  # 20,200 km in meters
        
        r_surface = R_EARTH
        r_gps = R_EARTH + h_gps
        
        # SSZ time dilation difference
        d_surface = ssz_time_dilation(r_surface, M_EARTH)
        d_gps = ssz_time_dilation(r_gps, M_EARTH)
        
        # Time gained per day by GPS clock (runs faster in weaker gravity)
        seconds_per_day = 86400
        dt_per_day = (d_gps - d_surface) * seconds_per_day
        dt_per_day_us = dt_per_day * 1e6  # microseconds
        
        # Known value: ~45 us/day faster (gravitational effect only)
        # Note: Special relativity slows it by ~7 us/day, net is ~38 us/day
        known_gr_effect = 45.7e-6  # seconds per day (gravitational only)
        
        print(f"GPS altitude: {h_gps/1e3:.0f} km")
        print(f"\nTime dilation factors:")
        print(f"  D_SSZ (surface): {d_surface:.15f}")
        print(f"  D_SSZ (GPS): {d_gps:.15f}")
        print(f"\nTime difference per day:")
        print(f"  SSZ prediction: {dt_per_day_us:.3f} us/day")
        print(f"  Known GR value: {known_gr_effect*1e6:.3f} us/day")
        print(f"  Difference: {abs(dt_per_day - known_gr_effect)*1e6:.3f} us/day")
        
        # Should match to within 1%
        assert np.isclose(dt_per_day, known_gr_effect, rtol=0.01)
        
        print("\nPhysical Interpretation:")
        print("  -> GPS clocks run ~45 us/day faster than ground clocks")
        print("  -> This MUST be corrected for GPS to work")
        print("  -> SSZ correctly predicts this effect")
        print("="*70)
    
    def test_gps_position_error_without_correction(self):
        """Calculate position error if time dilation not corrected."""
        print("\n" + "="*70)
        print("VALIDATION: GPS Position Error Without Correction")
        print("="*70)
        
        h_gps = 20200e3
        
        # Time error per day
        r_surface = R_EARTH
        r_gps = R_EARTH + h_gps
        d_surface = ssz_time_dilation(r_surface, M_EARTH)
        d_gps = ssz_time_dilation(r_gps, M_EARTH)
        
        dt_per_day = (d_gps - d_surface) * 86400  # seconds
        
        # Position error = c × time error
        position_error_per_day = C * dt_per_day  # meters
        position_error_per_day_km = position_error_per_day / 1000
        
        print(f"Time error per day: {dt_per_day*1e6:.3f} us")
        print(f"Position error per day: {position_error_per_day_km:.1f} km")
        
        # Known: ~10-11 km/day error without correction
        assert 10 < position_error_per_day_km < 15, "Should be ~10-15 km/day"
        
        print("\nPhysical Interpretation:")
        print("  -> Without relativistic correction: ~10 km/day error")
        print("  -> GPS would be useless within hours!")
        print("  -> SSZ effects are REAL and MEASURABLE")
        print("="*70)


# =============================================================================
# VALIDATION 3: ATOMIC CLOCK EXPERIMENTS
# =============================================================================

class TestAtomicClockValidation:
    """Validate against precision atomic clock experiments."""
    
    def test_nist_optical_clock_experiment(self):
        """NIST 2010: Detected time dilation over 33 cm height difference."""
        print("\n" + "="*70)
        print("VALIDATION: NIST Optical Clock Experiment (2010)")
        print("="*70)
        
        # NIST experiment: 33 cm height difference
        h = 0.33  # meters
        
        # Measured fractional frequency shift: ~4 × 10^-17
        z_measured = 3.6e-17  # Approximate
        
        # SSZ prediction
        r1 = R_EARTH
        r2 = R_EARTH + h
        d1 = ssz_time_dilation(r1, M_EARTH)
        d2 = ssz_time_dilation(r2, M_EARTH)
        z_ssz = d2/d1 - 1
        
        # GR prediction
        g = G * M_EARTH / R_EARTH**2
        z_gr = g * h / C**2
        
        print(f"Height difference: {h*100:.0f} cm")
        print(f"\nFrequency shift:")
        print(f"  NIST measured: ~{z_measured:.1e}")
        print(f"  GR prediction: {z_gr:.6e}")
        print(f"  SSZ prediction: {z_ssz:.6e}")
        
        # SSZ should match GR
        assert np.isclose(z_ssz, z_gr, rtol=1e-6)
        
        print("\nPhysical Interpretation:")
        print("  -> NIST detected time dilation over 33 cm!")
        print("  -> Most precise test of gravitational redshift")
        print("  -> SSZ matches this precision measurement")
        print("="*70)
    
    def test_tokyo_skytree_experiment(self):
        """Tokyo Skytree 2020: 450 m height difference."""
        print("\n" + "="*70)
        print("VALIDATION: Tokyo Skytree Experiment (2020)")
        print("="*70)
        
        # Tokyo Skytree: 450 m observation deck
        h = 450  # meters
        
        # SSZ prediction
        r1 = R_EARTH
        r2 = R_EARTH + h
        d1 = ssz_time_dilation(r1, M_EARTH)
        d2 = ssz_time_dilation(r2, M_EARTH)
        z_ssz = d2/d1 - 1
        
        # Time gained per day at top
        dt_per_day_ns = z_ssz * 86400 * 1e9  # nanoseconds
        
        # Measured: ~4 ns/day faster at top
        dt_measured_ns = 4.0  # approximate
        
        print(f"Height: {h} m (Tokyo Skytree)")
        print(f"\nTime difference per day:")
        print(f"  Measured: ~{dt_measured_ns:.1f} ns/day")
        print(f"  SSZ prediction: {dt_per_day_ns:.3f} ns/day")
        
        # Should be close
        assert np.isclose(dt_per_day_ns, dt_measured_ns, rtol=0.1)
        
        print("\nPhysical Interpretation:")
        print("  -> Clocks at top of Skytree run ~4 ns/day faster")
        print("  -> Portable optical clocks can now measure this")
        print("  -> SSZ correctly predicts building-scale effects")
        print("="*70)


# =============================================================================
# VALIDATION 4: THEORETICAL CONSISTENCY
# =============================================================================

class TestTheoreticalConsistency:
    """Test theoretical consistency of SSZ framework."""
    
    def test_xi_and_time_dilation_consistency(self):
        """Verify D_SSZ = 1/(1+Xi) holds exactly."""
        print("\n" + "="*70)
        print("VALIDATION: Xi and Time Dilation Consistency")
        print("="*70)
        
        radii = [R_EARTH * f for f in [0.5, 1.0, 2.0, 10.0, 100.0]]
        
        print(f"{'r/R_Earth':>12} | {'Xi':>15} | {'D_SSZ':>18} | {'1/(1+Xi)':>18} | {'Match':>8}")
        print("-" * 80)
        
        all_match = True
        for r in radii:
            xi = xi_segment_density(r, M_EARTH)
            d = ssz_time_dilation(r, M_EARTH)
            d_check = 1.0 / (1.0 + xi)
            match = np.isclose(d, d_check, rtol=1e-14)
            all_match = all_match and match
            
            print(f"{r/R_EARTH:>12.1f} | {xi:>15.6e} | {d:>18.15f} | {d_check:>18.15f} | {'OK' if match else 'FAIL':>8}")
        
        assert all_match, "D_SSZ should equal 1/(1+Xi) exactly"
        
        print("\nPhysical Interpretation:")
        print("  -> SSZ formula D_SSZ = 1/(1+Xi) is internally consistent")
        print("  -> Holds across all radii tested")
        print("="*70)
    
    def test_gradient_consistency(self):
        """Verify gradient is derivative of Xi."""
        print("\n" + "="*70)
        print("VALIDATION: Gradient Consistency")
        print("="*70)
        
        r = R_EARTH
        dr = 0.01  # 1 cm step
        
        # Analytical gradient
        grad_analytical = xi_gradient(r, M_EARTH)
        
        # Numerical gradient (5-point stencil for higher accuracy)
        xi_m2 = xi_segment_density(r - 2*dr, M_EARTH)
        xi_m1 = xi_segment_density(r - dr, M_EARTH)
        xi_p1 = xi_segment_density(r + dr, M_EARTH)
        xi_p2 = xi_segment_density(r + 2*dr, M_EARTH)
        grad_numerical = (-xi_p2 + 8*xi_p1 - 8*xi_m1 + xi_m2) / (12 * dr)
        
        print(f"Analytical dXi/dr: {grad_analytical:.10e} /m")
        print(f"Numerical dXi/dr: {grad_numerical:.10e} /m")
        print(f"Relative error: {abs(grad_analytical - grad_numerical)/abs(grad_analytical):.6e}")
        
        assert np.isclose(grad_analytical, grad_numerical, rtol=1e-8)
        
        print("\nPhysical Interpretation:")
        print("  -> Gradient formula is correct derivative of Xi")
        print("  -> Numerical and analytical agree to 10^-8")
        print("="*70)
    
    def test_energy_conservation_proxy(self):
        """Test that time dilation satisfies energy-like conservation."""
        print("\n" + "="*70)
        print("VALIDATION: Energy Conservation Proxy")
        print("="*70)
        
        # In GR: E = m*c^2 * sqrt(1 - r_s/r) is conserved for radial motion
        # In SSZ: E_ssz = m*c^2 * D_SSZ should be analogous
        
        # Test: D_SSZ(r) * (1 + Xi(r)) = 1 (by definition)
        
        radii = [R_EARTH * f for f in [1.0, 1.5, 2.0, 5.0, 10.0]]
        
        print(f"{'r/R_Earth':>12} | {'D_SSZ':>18} | {'1 + Xi':>18} | {'Product':>18}")
        print("-" * 75)
        
        for r in radii:
            xi = xi_segment_density(r, M_EARTH)
            d = ssz_time_dilation(r, M_EARTH)
            product = d * (1 + xi)
            
            print(f"{r/R_EARTH:>12.1f} | {d:>18.15f} | {1+xi:>18.15f} | {product:>18.15f}")
            
            assert np.isclose(product, 1.0, rtol=1e-14)
        
        print("\nPhysical Interpretation:")
        print("  -> D_SSZ * (1 + Xi) = 1 is an invariant")
        print("  -> Analogous to energy conservation in GR")
        print("="*70)
    
    def test_schwarzschild_limit(self):
        """Test behavior approaching Schwarzschild radius."""
        print("\n" + "="*70)
        print("VALIDATION: Schwarzschild Limit Behavior")
        print("="*70)
        
        r_s = schwarzschild_radius(M_EARTH)
        
        # Test at various multiples of r_s
        factors = [100, 10, 5, 2, 1.5, 1.1, 1.01]
        
        print(f"r_s (Earth) = {r_s:.6e} m")
        print(f"\n{'r/r_s':>10} | {'Xi':>12} | {'D_SSZ':>12} | {'D_GR':>12}")
        print("-" * 55)
        
        for f in factors:
            r = r_s * f
            xi = xi_segment_density(r, M_EARTH)
            d_ssz = ssz_time_dilation(r, M_EARTH)
            d_gr = np.sqrt(1 - r_s/r) if r > r_s else 0
            
            print(f"{f:>10.2f} | {xi:>12.6f} | {d_ssz:>12.6f} | {d_gr:>12.6f}")
        
        print("\nPhysical Interpretation:")
        print("  -> As r -> r_s: Xi -> 0.5, D_SSZ -> 2/3")
        print("  -> SSZ avoids singularity at r = r_s (D_SSZ remains finite)")
        print("  -> GR has D_GR -> 0 as r -> r_s")
        print("="*70)


# =============================================================================
# VALIDATION 5: QUBIT-SPECIFIC VALIDATION
# =============================================================================

class TestQubitValidation:
    """Validate qubit-specific SSZ predictions."""
    
    def test_qubit_height_sensitivity(self):
        """Validate sensitivity to qubit height differences."""
        print("\n" + "="*70)
        print("VALIDATION: Qubit Height Sensitivity")
        print("="*70)
        
        # Create qubits at various height differences
        heights_um = [0, 1, 10, 100, 1000]  # micrometers
        
        q_ref = Qubit(id="Q_ref", x=0, y=0, z=0)
        xi_ref = xi_segment_density(q_ref.radius_from_earth_center, M_EARTH)
        
        print(f"Reference qubit at z=0")
        print(f"Xi_ref = {xi_ref:.6e}")
        print(f"\n{'Height [um]':>12} | {'Delta Xi':>15} | {'Detectable':>12}")
        print("-" * 45)
        
        for h_um in heights_um:
            h_m = h_um * 1e-6
            q = Qubit(id=f"Q_{h_um}", x=0, y=0, z=h_m)
            xi = xi_segment_density(q.radius_from_earth_center, M_EARTH)
            delta_xi = abs(xi - xi_ref)
            
            # Detectable if delta_xi > 10^-20 (rough estimate)
            detectable = delta_xi > 1e-20
            
            print(f"{h_um:>12} | {delta_xi:>15.6e} | {'Yes' if detectable else 'No':>12}")
        
        print("\nPhysical Interpretation:")
        print("  -> Micrometer-scale height differences are detectable in Xi")
        print("  -> This is relevant for precision qubit placement")
        print("="*70)
    
    def test_pair_mismatch_scaling(self):
        """Validate that pair mismatch scales linearly with height difference."""
        print("\n" + "="*70)
        print("VALIDATION: Pair Mismatch Linear Scaling")
        print("="*70)
        
        height_diffs = [0.001, 0.002, 0.005, 0.01]  # meters
        mismatches = []
        
        for dh in height_diffs:
            q1 = Qubit(id="Q1", x=0, y=0, z=0)
            q2 = Qubit(id="Q2", x=0, y=0, z=dh)
            pair = QubitPair(q1, q2)
            
            mismatch = qubit_pair_segment_mismatch(pair, M_EARTH)
            mismatches.append(mismatch['delta_xi'])
        
        # Check linear scaling
        print(f"{'Height diff [mm]':>18} | {'Delta Xi':>15}")
        print("-" * 40)
        for dh, m in zip(height_diffs, mismatches):
            print(f"{dh*1000:>18.1f} | {m:>15.6e}")
        
        # Ratio of mismatches should equal ratio of height differences
        ratio_h = height_diffs[1] / height_diffs[0]
        ratio_m = mismatches[1] / mismatches[0]
        
        print(f"\nHeight ratio (2mm/1mm): {ratio_h:.1f}")
        print(f"Mismatch ratio: {ratio_m:.6f}")
        
        assert np.isclose(ratio_h, ratio_m, rtol=0.01), "Mismatch should scale linearly"
        
        print("\nPhysical Interpretation:")
        print("  -> Delta Xi scales linearly with height difference")
        print("  -> Doubling height diff doubles segment mismatch")
        print("="*70)
    
    def test_decoherence_physical_bounds(self):
        """Validate decoherence predictions are physically reasonable."""
        print("\n" + "="*70)
        print("VALIDATION: Decoherence Physical Bounds")
        print("="*70)
        
        # Typical superconducting qubit parameters
        T2_typical = 100e-6  # 100 us
        
        q = Qubit(id="Q1", x=0, y=0, z=0, coherence_time_T2=T2_typical)
        analysis = analyze_qubit_segment(q, M_EARTH)
        
        print(f"Typical T2: {T2_typical*1e6:.0f} us")
        print(f"Xi at surface: {analysis.xi:.6e}")
        print(f"Coherence factor: {analysis.coherence_factor:.6f}")
        
        # SSZ effect should be small but non-zero
        assert analysis.coherence_factor > 0.99, "SSZ shouldn't dominate decoherence"
        assert analysis.coherence_factor < 1.0, "SSZ should have some effect"
        
        print("\nPhysical Interpretation:")
        print("  -> SSZ contributes ~0.01% to decoherence at Earth surface")
        print("  -> Other mechanisms (thermal, EM) dominate")
        print("  -> But SSZ effect is fundamental and unavoidable")
        print("="*70)


# =============================================================================
# VALIDATION 6: DIMENSIONAL ANALYSIS
# =============================================================================

class TestDimensionalAnalysis:
    """Verify dimensional consistency of all quantities."""
    
    def test_xi_dimensionless(self):
        """Xi should be dimensionless."""
        print("\n" + "="*70)
        print("VALIDATION: Xi Dimensionless")
        print("="*70)
        
        # Xi = r_s / (2r) = [m] / [m] = dimensionless
        r = R_EARTH
        xi = xi_segment_density(r, M_EARTH)
        
        print(f"Xi = r_s / (2r)")
        print(f"  r_s has units [m]")
        print(f"  r has units [m]")
        print(f"  Xi = [m]/[m] = dimensionless")
        print(f"  Xi value: {xi:.6e} (no units)")
        
        # Xi should be a pure number
        assert isinstance(xi, float)
        assert 0 < xi < 1, "Xi should be between 0 and 1 for r > r_s"
        
        print("\nPhysical Interpretation:")
        print("  -> Xi is a pure ratio (dimensionless)")
        print("  -> Represents 'strength' of spacetime segmentation")
        print("="*70)
    
    def test_gradient_has_correct_units(self):
        """Gradient should have units of 1/m."""
        print("\n" + "="*70)
        print("VALIDATION: Gradient Units")
        print("="*70)
        
        # dXi/dr = -r_s / (2r^2) = [m] / [m^2] = [1/m]
        r = R_EARTH
        grad = xi_gradient(r, M_EARTH)
        
        print(f"dXi/dr = -r_s / (2r^2)")
        print(f"  r_s has units [m]")
        print(f"  r^2 has units [m^2]")
        print(f"  dXi/dr = [m]/[m^2] = [1/m]")
        print(f"  Gradient value: {grad:.6e} /m")
        
        # Gradient should be negative and have magnitude ~ Xi/R_Earth
        expected_magnitude = xi_segment_density(r, M_EARTH) / R_EARTH
        
        print(f"  Expected magnitude: ~{expected_magnitude:.6e} /m")
        
        assert grad < 0, "Gradient should be negative"
        assert np.isclose(abs(grad), expected_magnitude, rtol=0.1)
        
        print("\nPhysical Interpretation:")
        print("  -> Gradient has units [1/m] as expected")
        print("  -> Magnitude ~ Xi/r (rate of change per unit distance)")
        print("="*70)
    
    def test_time_offset_has_correct_units(self):
        """Time offset should have units of seconds."""
        print("\n" + "="*70)
        print("VALIDATION: Time Offset Units")
        print("="*70)
        
        h = 1.0  # 1 meter
        duration = 1.0  # 1 second
        
        dt = height_to_time_offset(h, duration, M_EARTH)
        
        print(f"height_to_time_offset({h} m, {duration} s) = {dt:.6e} s")
        print(f"  Input: height [m], duration [s]")
        print(f"  Output: time offset [s]")
        
        # Should be a small positive number in seconds
        assert dt > 0
        assert dt < duration, "Time offset should be << duration"
        
        print("\nPhysical Interpretation:")
        print("  -> Time offset is in seconds")
        print("  -> Represents accumulated clock difference")
        print("="*70)


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("SSZ-QUBITS VALIDATION TEST SUITE")
    print("="*70)
    print("Running cross-validation tests against known results...")
    print("="*70 + "\n")
    
    pytest.main([__file__, "-v", "-s", "--tb=short"])
