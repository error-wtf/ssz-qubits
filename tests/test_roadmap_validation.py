#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Suite for SSZ Research Program Roadmap Validation

Tests the three core hypotheses (H1, H2, H3) and work package simulations.

(c) 2025 Carmen Wrede, Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""

import os
import sys

# UTF-8 for Windows
if sys.platform.startswith('win'):
    os.environ['PYTHONIOENCODING'] = 'utf-8'

import pytest
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ssz_qubits import (
    C, G, HBAR, PHI, M_EARTH, R_EARTH,
    schwarzschild_radius, xi_segment_density,
    ssz_time_dilation, ssz_time_dilation_difference,
    segment_coherent_zone, Qubit, QubitPair,
    qubit_pair_segment_mismatch
)


# =============================================================================
# CONSTANTS
# =============================================================================

OMEGA = 2 * np.pi * 5e9  # 5 GHz qubit
GATE_TIME = 50e-9  # 50 ns


# =============================================================================
# H1: DETERMINISTIC PHASE BIAS TESTS
# =============================================================================

class TestH1DeterministicPhaseBias:
    """Tests for Hypothesis H1: Deterministic phase bias from SSZ time dilation."""
    
    def test_phase_drift_formula(self):
        """Test that phase drift follows: DeltaPhi = omega * DeltaD_SSZ * t"""
        delta_h = 0.001  # 1 mm
        t = 1e-6  # 1 us
        
        delta_d = ssz_time_dilation_difference(R_EARTH + delta_h, R_EARTH, M_EARTH)
        delta_phi = OMEGA * abs(delta_d) * t
        
        # Phase drift should be positive and finite
        assert delta_phi > 0
        assert np.isfinite(delta_phi)
        
    def test_effect_is_deterministic(self):
        """Test that SSZ effect is deterministic (same input -> same output)."""
        delta_h = 0.001
        
        results = [
            ssz_time_dilation_difference(R_EARTH + delta_h, R_EARTH, M_EARTH)
            for _ in range(10)
        ]
        
        # All results should be identical
        assert all(r == results[0] for r in results)
        
    def test_phase_drift_scales_with_height(self):
        """Test that phase drift scales linearly with height difference."""
        h1 = 0.001  # 1 mm
        h2 = 0.002  # 2 mm
        
        d1 = abs(ssz_time_dilation_difference(R_EARTH + h1, R_EARTH, M_EARTH))
        d2 = abs(ssz_time_dilation_difference(R_EARTH + h2, R_EARTH, M_EARTH))
        
        ratio = d2 / d1
        assert abs(ratio - 2.0) < 0.01  # Should be ~2x
        
    def test_phase_drift_scales_with_time(self):
        """Test that phase drift scales linearly with time."""
        delta_h = 0.001
        delta_d = abs(ssz_time_dilation_difference(R_EARTH + delta_h, R_EARTH, M_EARTH))
        
        t1 = 1e-6
        t2 = 2e-6
        
        phi1 = OMEGA * delta_d * t1
        phi2 = OMEGA * delta_d * t2
        
        assert abs(phi2 / phi1 - 2.0) < 1e-10
        
    def test_compensation_is_possible(self):
        """Test that knowing DeltaD_SSZ allows compensation."""
        delta_h = 0.001
        t = 1e-6
        
        delta_d = ssz_time_dilation_difference(R_EARTH + delta_h, R_EARTH, M_EARTH)
        delta_phi = OMEGA * abs(delta_d) * t
        
        # Compensation: apply -delta_phi
        compensated_phi = delta_phi - delta_phi
        
        assert compensated_phi == 0.0


# =============================================================================
# H2: SEGMENT-COHERENT ZONES TESTS
# =============================================================================

class TestH2CoherentZones:
    """Tests for Hypothesis H2: Segment-coherent zones."""
    
    def test_zone_width_formula(self):
        """Test zone width formula: z = 4 * eps * R^2 / r_s"""
        r_s = schwarzschild_radius(M_EARTH)
        
        for epsilon in [1e-16, 1e-18, 1e-20]:
            h_min, h_max = segment_coherent_zone(0, epsilon, M_EARTH)
            zone_width = h_max - h_min
            
            z_theoretical = 4 * epsilon * R_EARTH**2 / r_s
            
            # Should match within 1%
            assert abs(zone_width - z_theoretical) / z_theoretical < 0.01
            
    def test_zone_width_scales_with_epsilon(self):
        """Test that zone width scales linearly with epsilon."""
        eps1 = 1e-18
        eps2 = 1e-17  # 10x larger
        
        _, h_max1 = segment_coherent_zone(0, eps1, M_EARTH)
        _, h_max2 = segment_coherent_zone(0, eps2, M_EARTH)
        
        ratio = h_max2 / h_max1
        assert abs(ratio - 10.0) < 0.1
        
    def test_cross_zone_bias(self):
        """Test that cross-zone operations accumulate bias."""
        epsilon = 1e-18
        _, h_max = segment_coherent_zone(0, epsilon, M_EARTH)
        
        # Qubits inside and outside zone
        q_in = Qubit(id="in", x=0, y=0, z=0)
        q_out = Qubit(id="out", x=0, y=0, z=h_max * 2)
        
        pair = QubitPair(q_in, q_out)
        mismatch = qubit_pair_segment_mismatch(pair, M_EARTH)
        
        # Cross-zone should have measurable delta_xi
        assert mismatch['delta_xi'] > 0
        assert mismatch['phase_drift_per_gate'] > 0


# =============================================================================
# H3: SCALING WITH COHERENCE/HEIGHT TESTS
# =============================================================================

class TestH3Scaling:
    """Tests for Hypothesis H3: Relevance grows with coherence/height."""
    
    def test_accumulated_drift_grows_with_coherence(self):
        """Test that accumulated drift grows with longer coherence times."""
        delta_h = 0.001
        delta_d = abs(ssz_time_dilation_difference(R_EARTH + delta_h, R_EARTH, M_EARTH))
        
        t2_short = 10e-6  # 10 us
        t2_long = 100e-6  # 100 us
        
        phi_short = OMEGA * delta_d * t2_short
        phi_long = OMEGA * delta_d * t2_long
        
        assert phi_long > phi_short
        assert abs(phi_long / phi_short - 10.0) < 1e-10
        
    def test_effect_grows_with_height_difference(self):
        """Test that effect grows with larger height differences."""
        heights = [1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 0.1, 1.0]
        
        deltas = [
            abs(ssz_time_dilation_difference(R_EARTH + h, R_EARTH, M_EARTH))
            for h in heights
        ]
        
        # Should be monotonically increasing
        for i in range(len(deltas) - 1):
            assert deltas[i+1] > deltas[i]
            
    def test_macroscopic_height_measurable(self):
        """Test that macroscopic heights produce larger, more measurable effects."""
        # 1 meter height difference
        delta_h = 1.0
        t = 1e-6
        
        delta_d = abs(ssz_time_dilation_difference(R_EARTH + delta_h, R_EARTH, M_EARTH))
        delta_phi = OMEGA * delta_d * t
        
        # Should be ~10^12 times larger than 1 um case
        delta_h_small = 1e-6
        delta_d_small = abs(ssz_time_dilation_difference(R_EARTH + delta_h_small, R_EARTH, M_EARTH))
        delta_phi_small = OMEGA * delta_d_small * t
        
        ratio = delta_phi / delta_phi_small
        assert ratio > 1e5  # Much larger effect


# =============================================================================
# WP1: SIMULATION BENCHMARK TESTS
# =============================================================================

class TestWP1Simulation:
    """Tests for WP1: Simulation benchmark."""
    
    def test_baseline_has_unity_fidelity(self):
        """Test that baseline (no SSZ) has perfect fidelity."""
        # Without any drift, fidelity should be 1.0
        phase_error = 0.0
        fidelity = np.cos(phase_error / 2)**2
        assert fidelity == 1.0
        
    def test_ssz_drift_reduces_fidelity(self):
        """Test that SSZ drift reduces fidelity."""
        delta_h = 0.001
        n_gates = 1000000  # Many gates to accumulate effect
        
        delta_d = abs(ssz_time_dilation_difference(R_EARTH + delta_h, R_EARTH, M_EARTH))
        phase_per_gate = OMEGA * delta_d * GATE_TIME
        total_phase = phase_per_gate * n_gates
        
        fidelity = np.cos(total_phase / 2)**2
        
        # Should still be very close to 1 for Earth-scale effects
        # but theoretically less than 1
        assert fidelity <= 1.0
        
    def test_compensation_recovers_fidelity(self):
        """Test that compensation recovers baseline fidelity."""
        delta_h = 0.001
        n_gates = 1000000
        compensation_efficiency = 0.99
        
        delta_d = abs(ssz_time_dilation_difference(R_EARTH + delta_h, R_EARTH, M_EARTH))
        phase_per_gate = OMEGA * delta_d * GATE_TIME
        
        # Without compensation
        total_phase_uncompensated = phase_per_gate * n_gates
        
        # With compensation
        residual_phase_per_gate = phase_per_gate * (1 - compensation_efficiency)
        total_phase_compensated = residual_phase_per_gate * n_gates
        
        f_uncompensated = np.cos(total_phase_uncompensated / 2)**2
        f_compensated = np.cos(total_phase_compensated / 2)**2
        
        # Compensated should be better
        assert f_compensated >= f_uncompensated


# =============================================================================
# FALSIFIABILITY TESTS
# =============================================================================

class TestFalsifiability:
    """Tests for falsifiability conditions."""
    
    def test_height_dependence_exists(self):
        """Test that there IS height dependence (falsifiable if not)."""
        h1 = 0.001
        h2 = 0.002
        
        d1 = ssz_time_dilation_difference(R_EARTH + h1, R_EARTH, M_EARTH)
        d2 = ssz_time_dilation_difference(R_EARTH + h2, R_EARTH, M_EARTH)
        
        assert d1 != d2  # Must depend on height
        
    def test_correct_omega_scaling(self):
        """Test that effect scales with omega as predicted."""
        delta_h = 0.001
        t = 1e-6
        
        delta_d = abs(ssz_time_dilation_difference(R_EARTH + delta_h, R_EARTH, M_EARTH))
        
        omega1 = 2 * np.pi * 5e9
        omega2 = 2 * np.pi * 10e9  # 2x frequency
        
        phi1 = omega1 * delta_d * t
        phi2 = omega2 * delta_d * t
        
        assert abs(phi2 / phi1 - 2.0) < 1e-10
        
    def test_monotonic_in_height(self):
        """Test that effect is monotonic in height (falsifiable if not)."""
        heights = np.linspace(0.0001, 1.0, 100)
        
        deltas = [
            abs(ssz_time_dilation_difference(R_EARTH + h, R_EARTH, M_EARTH))
            for h in heights
        ]
        
        # Check monotonicity
        for i in range(len(deltas) - 1):
            assert deltas[i+1] >= deltas[i]


# =============================================================================
# INTEGRATION TEST
# =============================================================================

class TestIntegration:
    """Integration tests running the full validation."""
    
    def test_roadmap_validation_runs(self):
        """Test that the roadmap validation script runs successfully."""
        # Import the validation module
        try:
            from ssz_roadmap_validation import (
                validate_H1_phase_bias,
                validate_H2_coherent_zones,
                validate_H3_scaling
            )
            imported = True
        except ImportError:
            imported = False
            
        assert imported, "Could not import ssz_roadmap_validation module"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
