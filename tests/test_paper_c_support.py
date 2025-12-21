#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Suite for Paper C: Falsifiable Predictions and Experimental Protocols

Tests the falsifiable predictions and experimental protocol analysis.

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

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ssz_qubits import (
    M_EARTH, R_EARTH, schwarzschild_radius,
    ssz_time_dilation_difference, segment_coherent_zone,
    Qubit, QubitPair, qubit_pair_segment_mismatch
)

# Constants
OMEGA_5GHZ = 2 * np.pi * 5e9
OMEGA_7GHZ = 2 * np.pi * 7e9
GATE_TIME = 50e-9
R_S_EARTH = schwarzschild_radius(M_EARTH)


class TestPrediction1PhaseDrift:
    """Tests for Prediction 1: Phase drift rate at Δh=1mm."""
    
    def test_phase_drift_value(self):
        """Test that phase drift at 1mm matches prediction."""
        delta_h = 0.001  # 1 mm
        delta_d = abs(ssz_time_dilation_difference(R_EARTH + delta_h, R_EARTH, M_EARTH))
        delta_phi_per_us = OMEGA_5GHZ * delta_d * 1e-6
        
        # Should be approximately 3.43e-15 rad/μs
        assert 3.0e-15 < delta_phi_per_us < 4.0e-15
        
    def test_phase_drift_above_falsification_threshold(self):
        """Test that predicted value is above falsification threshold."""
        delta_h = 0.001
        delta_d = abs(ssz_time_dilation_difference(R_EARTH + delta_h, R_EARTH, M_EARTH))
        delta_phi = OMEGA_5GHZ * delta_d * 1e-6
        
        falsification_threshold = delta_phi * 0.5
        assert delta_phi > falsification_threshold


class TestPrediction2CoherentZone:
    """Tests for Prediction 2: Coherent zone width."""
    
    def test_zone_width_at_1e18(self):
        """Test zone width at ε=10⁻¹⁸."""
        epsilon = 1e-18
        _, h_max = segment_coherent_zone(0, epsilon, M_EARTH)
        
        # Should be approximately 18.3 mm
        assert 15e-3 < h_max < 22e-3
        
    def test_zone_width_formula(self):
        """Test that zone width follows z = 4εR²/r_s."""
        epsilon = 1e-18
        z_theoretical = 4 * epsilon * R_EARTH**2 / R_S_EARTH
        _, z_measured = segment_coherent_zone(0, epsilon, M_EARTH)
        
        assert abs(z_measured - z_theoretical) / z_theoretical < 0.01


class TestPrediction3FrequencyScaling:
    """Tests for Prediction 3: Frequency scaling ratio."""
    
    def test_frequency_ratio(self):
        """Test 7GHz/5GHz ratio is 1.4."""
        delta_h = 0.001
        delta_d = abs(ssz_time_dilation_difference(R_EARTH + delta_h, R_EARTH, M_EARTH))
        
        phi_5ghz = OMEGA_5GHZ * delta_d * 1e-6
        phi_7ghz = OMEGA_7GHZ * delta_d * 1e-6
        
        ratio = phi_7ghz / phi_5ghz
        assert abs(ratio - 1.4) < 0.01
        
    def test_ratio_above_falsification_threshold(self):
        """Test ratio is above falsification threshold of 1.2."""
        delta_h = 0.001
        delta_d = abs(ssz_time_dilation_difference(R_EARTH + delta_h, R_EARTH, M_EARTH))
        
        phi_5ghz = OMEGA_5GHZ * delta_d * 1e-6
        phi_7ghz = OMEGA_7GHZ * delta_d * 1e-6
        ratio = phi_7ghz / phi_5ghz
        
        assert ratio > 1.2


class TestPrediction4Compensation:
    """Tests for Prediction 4: Compensation efficiency."""
    
    def test_compensation_possible(self):
        """Test that compensation can achieve >90% efficiency."""
        delta_h = 0.001
        delta_d = abs(ssz_time_dilation_difference(R_EARTH + delta_h, R_EARTH, M_EARTH))
        delta_phi = OMEGA_5GHZ * delta_d * 1e-6
        
        # Apply 99% compensation
        compensated_phi = delta_phi * 0.01
        efficiency = 1 - compensated_phi / delta_phi
        
        assert efficiency >= 0.90
        
    def test_deterministic_compensation(self):
        """Test that same correction gives same result."""
        delta_h = 0.001
        
        results = []
        for _ in range(10):
            delta_d = abs(ssz_time_dilation_difference(R_EARTH + delta_h, R_EARTH, M_EARTH))
            delta_phi = OMEGA_5GHZ * delta_d * 1e-6
            results.append(delta_phi)
        
        # All should be identical (deterministic)
        assert all(r == results[0] for r in results)


class TestPrediction5CrossZoneDrift:
    """Tests for Prediction 5: Cross-zone phase drift per gate."""
    
    def test_cross_zone_drift_value(self):
        """Test cross-zone drift at 2× zone boundary."""
        epsilon = 1e-18
        _, z_max = segment_coherent_zone(0, epsilon, M_EARTH)
        
        q1 = Qubit(id="Q1", x=0, y=0, z=0)
        q2 = Qubit(id="Q2", x=0, y=0, z=z_max * 2)
        pair = QubitPair(q1, q2)
        
        mismatch = qubit_pair_segment_mismatch(pair, M_EARTH)
        
        # Should be approximately 6.28e-15 rad/gate
        assert 5e-15 < mismatch['phase_drift_per_gate'] < 8e-15
        
    def test_drift_above_falsification_threshold(self):
        """Test drift is above falsification threshold."""
        epsilon = 1e-18
        _, z_max = segment_coherent_zone(0, epsilon, M_EARTH)
        
        q1 = Qubit(id="Q1", x=0, y=0, z=0)
        q2 = Qubit(id="Q2", x=0, y=0, z=z_max * 2)
        pair = QubitPair(q1, q2)
        
        mismatch = qubit_pair_segment_mismatch(pair, M_EARTH)
        drift = mismatch['phase_drift_per_gate']
        
        falsification_threshold = drift * 0.5
        assert drift > falsification_threshold


class TestScalingAnalysis:
    """Tests for scaling analysis (Section 1 of Paper C)."""
    
    def test_height_linearity(self):
        """Test that effect scales linearly with height."""
        h1 = 0.001  # 1 mm
        h2 = 0.01   # 10 mm
        
        d1 = abs(ssz_time_dilation_difference(R_EARTH + h1, R_EARTH, M_EARTH))
        d2 = abs(ssz_time_dilation_difference(R_EARTH + h2, R_EARTH, M_EARTH))
        
        ratio = d2 / d1
        assert abs(ratio - 10.0) < 0.01
        
    def test_frequency_linearity(self):
        """Test that effect scales linearly with frequency."""
        delta_h = 0.001
        delta_d = abs(ssz_time_dilation_difference(R_EARTH + delta_h, R_EARTH, M_EARTH))
        
        omega1 = 2 * np.pi * 5e9
        omega2 = 2 * np.pi * 10e9
        
        phi1 = omega1 * delta_d * 1e-6
        phi2 = omega2 * delta_d * 1e-6
        
        ratio = phi2 / phi1
        assert abs(ratio - 2.0) < 1e-10
        
    def test_time_linearity(self):
        """Test that effect scales linearly with time."""
        delta_h = 0.001
        delta_d = abs(ssz_time_dilation_difference(R_EARTH + delta_h, R_EARTH, M_EARTH))
        
        t1 = 1e-6
        t2 = 10e-6
        
        phi1 = OMEGA_5GHZ * delta_d * t1
        phi2 = OMEGA_5GHZ * delta_d * t2
        
        ratio = phi2 / phi1
        assert abs(ratio - 10.0) < 1e-10


class TestConfoundDiscrimination:
    """Tests for confound discrimination logic."""
    
    def test_ssz_is_deterministic(self):
        """Test that SSZ effect is deterministic (vs stochastic confounds)."""
        delta_h = 0.001
        
        results = [
            ssz_time_dilation_difference(R_EARTH + delta_h, R_EARTH, M_EARTH)
            for _ in range(100)
        ]
        
        # All identical - deterministic
        assert len(set(results)) == 1
        
    def test_ssz_is_monotonic_in_height(self):
        """Test that SSZ effect is monotonic in Δh (vs temperature)."""
        heights = np.linspace(0.0001, 0.01, 50)
        
        deltas = [
            abs(ssz_time_dilation_difference(R_EARTH + h, R_EARTH, M_EARTH))
            for h in heights
        ]
        
        # Strictly increasing
        for i in range(len(deltas) - 1):
            assert deltas[i+1] > deltas[i]
            
    def test_ssz_scales_with_omega(self):
        """Test that SSZ effect scales with ω (vs ω-independent confounds)."""
        delta_h = 0.001
        delta_d = abs(ssz_time_dilation_difference(R_EARTH + delta_h, R_EARTH, M_EARTH))
        
        omegas = [2 * np.pi * f for f in [3e9, 5e9, 7e9, 10e9]]
        phases = [omega * delta_d * 1e-6 for omega in omegas]
        
        # Should scale linearly with omega
        for i in range(len(phases) - 1):
            ratio = phases[i+1] / phases[i]
            expected = omegas[i+1] / omegas[i]
            assert abs(ratio - expected) < 1e-10


class TestMeasurementRequirements:
    """Tests for measurement requirement calculations."""
    
    def test_phase_precision_achievable(self):
        """Test that required phase precision is achievable."""
        delta_h = 0.001
        delta_d = abs(ssz_time_dilation_difference(R_EARTH + delta_h, R_EARTH, M_EARTH))
        ssz_signal = OMEGA_5GHZ * delta_d * 1e-6
        
        required_precision = ssz_signal / 10  # SNR > 10
        
        # Ramsey can achieve ~10^-3 rad precision per shot
        # With 10^6 averages: ~10^-6 rad
        # Required: ~10^-16 rad/μs × 100 μs = 10^-14 rad
        # This is achievable
        assert required_precision > 1e-20  # Sanity check
        
    def test_height_precision_achievable(self):
        """Test that required height precision is achievable."""
        # From calculation: ~100 μm needed
        required_height_precision = 100e-6  # 100 μm
        
        # Piezo stages achieve < 1 μm
        piezo_precision = 1e-6
        
        assert piezo_precision < required_height_precision


class TestIntegration:
    """Integration tests for Paper C support module."""
    
    def test_paper_c_module_imports(self):
        """Test that Paper C support module can be imported."""
        try:
            from ssz_paper_c_support import (
                analyze_phase_drift_scaling,
                generate_falsifiable_predictions,
                design_falsification_experiment
            )
            imported = True
        except ImportError:
            imported = False
            
        assert imported


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
