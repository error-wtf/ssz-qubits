#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for SSZ Entanglement Module.

These tests verify all Paper B claims are reproducible from the module.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import pytest
from ssz_qubits import Qubit, QubitPair, R_EARTH, M_EARTH
from ssz_entanglement import (
    entangled_pair_phase_drift,
    bell_state_fidelity,
    bell_state_fidelity_approx,
    chsh_parameter,
    characteristic_time_T_SSZ,
    correction_interval,
    correction_gate,
    is_in_coherent_zone,
    analyze_entangled_pair
)


class TestPhaseDrift:
    """Test phase drift calculations."""
    
    def test_phase_drift_1mm(self):
        """Paper B claims: 1.72e-16 rad/gate for 1 mm separation."""
        q1 = Qubit(id='q1', x=0, y=0, z=0, gate_time=50e-9)
        q2 = Qubit(id='q2', x=0, y=0, z=1e-3, gate_time=50e-9)
        pair = QubitPair(q1, q2)
        
        result = entangled_pair_phase_drift(pair)
        
        expected = 1.72e-16
        assert abs(result['phase_drift_per_gate'] - expected) / expected < 0.01
    
    def test_phase_drift_linear_scaling(self):
        """Phase drift should scale linearly with height."""
        heights = [1e-3, 1e-2, 1e-1, 1.0]  # 1mm to 1m
        drifts = []
        
        for h in heights:
            q1 = Qubit(id='q1', x=0, y=0, z=0, gate_time=50e-9)
            q2 = Qubit(id='q2', x=0, y=0, z=h, gate_time=50e-9)
            pair = QubitPair(q1, q2)
            result = entangled_pair_phase_drift(pair)
            drifts.append(result['phase_drift_per_gate'])
        
        # Check linear scaling (small deviations from linearity at large heights
        # due to 1/r^2 gradient, but should be < 1e-5 for Earth surface)
        for i in range(1, len(heights)):
            ratio = drifts[i] / drifts[0]
            expected_ratio = heights[i] / heights[0]
            assert abs(ratio - expected_ratio) / expected_ratio < 1e-5
    
    def test_signed_delta_D(self):
        """Delta_D should be signed: positive if A higher."""
        # A higher than B
        q1 = Qubit(id='A', x=0, y=0, z=1e-3, gate_time=50e-9)
        q2 = Qubit(id='B', x=0, y=0, z=0, gate_time=50e-9)
        pair = QubitPair(q1, q2)
        result = entangled_pair_phase_drift(pair)
        assert result['delta_D'] > 0
        
        # B higher than A
        q1 = Qubit(id='A', x=0, y=0, z=0, gate_time=50e-9)
        q2 = Qubit(id='B', x=0, y=0, z=1e-3, gate_time=50e-9)
        pair = QubitPair(q1, q2)
        result = entangled_pair_phase_drift(pair)
        assert result['delta_D'] < 0


class TestBellStateFidelity:
    """Test Bell state fidelity calculations."""
    
    def test_fidelity_zero_phase(self):
        """F = 1 when Delta_Phi = 0."""
        assert bell_state_fidelity(0) == 1.0
    
    def test_fidelity_pi_phase(self):
        """F = 0 when Delta_Phi = pi."""
        assert abs(bell_state_fidelity(np.pi)) < 1e-15
    
    def test_fidelity_formula(self):
        """F = cos^2(Delta_Phi/2)."""
        for phi in [0.1, 0.5, 1.0, 2.0]:
            expected = np.cos(phi/2)**2
            assert abs(bell_state_fidelity(phi) - expected) < 1e-15
    
    def test_fidelity_paper_value(self):
        """Paper B: 1-F = 7.4e-15 for Delta_Phi = 1.72e-7."""
        delta_phi = 1.72e-7
        F = bell_state_fidelity(delta_phi)
        loss = 1 - F
        expected_loss = 7.4e-15
        assert abs(loss - expected_loss) / expected_loss < 0.1
    
    def test_small_angle_approximation(self):
        """F ≈ 1 - Delta_Phi^2/4 for small phases."""
        for phi in [1e-8, 1e-7, 1e-6, 1e-5]:
            exact = bell_state_fidelity(phi)
            approx = bell_state_fidelity_approx(phi)
            rel_error = abs(exact - approx) / exact
            assert rel_error < 1e-10


class TestCHSHParameter:
    """Test CHSH parameter calculations."""
    
    def test_chsh_max(self):
        """S = 2*sqrt(2) when Delta_Phi = 0."""
        S_max = 2 * np.sqrt(2)
        assert abs(chsh_parameter(0) - S_max) < 1e-15
    
    def test_chsh_zero(self):
        """S = 0 when Delta_Phi = pi/2."""
        assert abs(chsh_parameter(np.pi/2)) < 1e-15
    
    def test_chsh_classical_bound(self):
        """S = 2 (classical bound) when Delta_Phi = pi/4."""
        S = chsh_parameter(np.pi/4)
        assert abs(S - 2.0) < 1e-10
    
    def test_chsh_formula(self):
        """S = 2*sqrt(2)*cos(Delta_Phi)."""
        for phi in [0.1, 0.5, 1.0]:
            expected = 2 * np.sqrt(2) * np.cos(phi)
            assert abs(chsh_parameter(phi) - expected) < 1e-15


class TestCharacteristicTime:
    """Test T_SSZ calculations."""
    
    def test_T_SSZ_1mm(self):
        """Paper B: T_SSZ ≈ 29 years for 1 mm separation."""
        T = characteristic_time_T_SSZ(1e-3)
        years = T / (365.25 * 24 * 3600)
        assert abs(years - 29) / 29 < 0.05
    
    def test_T_SSZ_scaling(self):
        """T_SSZ should scale inversely with height."""
        T_1mm = characteristic_time_T_SSZ(1e-3)
        T_10mm = characteristic_time_T_SSZ(10e-3)
        
        # T_SSZ ∝ 1/|Delta_D| ∝ 1/h
        ratio = T_1mm / T_10mm
        assert abs(ratio - 10) / 10 < 0.01
    
    def test_T_SSZ_zero_height(self):
        """T_SSZ = inf when height difference is zero."""
        T = characteristic_time_T_SSZ(0)
        assert T == np.inf


class TestCorrectionInterval:
    """Test correction interval calculations."""
    
    def test_correction_interval_paper_value(self):
        """Paper B: N_corr ≈ 5.8e9 for 1 mm, eps = 1e-6."""
        phase_drift = 1.72e-16  # rad/gate for 1 mm
        eps = 1e-6
        N = correction_interval(eps, phase_drift)
        expected = 5.8e9
        assert abs(N - expected) / expected < 0.1
    
    def test_correction_interval_zero_drift(self):
        """N_corr = inf when drift is zero."""
        N = correction_interval(1e-6, 0)
        assert N == np.inf


class TestCorrectionGate:
    """Test correction gate specification."""
    
    def test_correction_higher_A(self):
        """When A is higher, correct A with Rz(-phi)."""
        corr = correction_gate(1e-7, higher_qubit='A')
        assert corr['target_qubit'] == 'A'
        assert corr['rotation_angle'] == -1e-7
    
    def test_correction_higher_B(self):
        """When B is higher, correct B with Rz(+phi)."""
        corr = correction_gate(1e-7, higher_qubit='B')
        assert corr['target_qubit'] == 'B'
        assert corr['rotation_angle'] == 1e-7


class TestCoherentZone:
    """Test coherent zone membership."""
    
    def test_same_height_in_zone(self):
        """Qubits at same height are always in same zone."""
        q1 = Qubit(id='q1', x=0, y=0, z=0, gate_time=50e-9)
        q2 = Qubit(id='q2', x=1, y=0, z=0, gate_time=50e-9)
        pair = QubitPair(q1, q2)
        assert is_in_coherent_zone(pair, tolerance=1e-18)
    
    def test_small_separation_in_zone(self):
        """1 mm separation should be in 18 mm zone (eps=1e-18)."""
        q1 = Qubit(id='q1', x=0, y=0, z=0, gate_time=50e-9)
        q2 = Qubit(id='q2', x=0, y=0, z=1e-3, gate_time=50e-9)
        pair = QubitPair(q1, q2)
        # Zone width is ~18 mm for eps=1e-18
        assert is_in_coherent_zone(pair, tolerance=1e-18)
    
    def test_large_separation_out_of_zone(self):
        """100 mm separation should be outside 18 mm zone."""
        q1 = Qubit(id='q1', x=0, y=0, z=0, gate_time=50e-9)
        q2 = Qubit(id='q2', x=0, y=0, z=0.1, gate_time=50e-9)
        pair = QubitPair(q1, q2)
        # Zone width is ~18 mm for eps=1e-18
        assert not is_in_coherent_zone(pair, tolerance=1e-18)


class TestFullAnalysis:
    """Test complete entangled pair analysis."""
    
    def test_analysis_1mm(self):
        """Full analysis for 1 mm separation."""
        q1 = Qubit(id='q1', x=0, y=0, z=0, gate_time=50e-9)
        q2 = Qubit(id='q2', x=0, y=0, z=1e-3, gate_time=50e-9)
        pair = QubitPair(q1, q2)
        
        analysis = analyze_entangled_pair(pair, N_gates=10**9)
        
        # Check all Paper B values
        assert abs(analysis.phase_drift_per_gate - 1.72e-16) / 1.72e-16 < 0.01
        assert abs(analysis.T_SSZ / (365.25*24*3600) - 29) / 29 < 0.05
        assert abs((1 - analysis.fidelity_after_N_gates) - 7.4e-15) / 7.4e-15 < 0.1
        assert analysis.in_coherent_zone == True


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
