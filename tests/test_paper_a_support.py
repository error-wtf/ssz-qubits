#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for SSZ Paper A Support Module.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import pytest
from ssz_qubits import R_EARTH, M_EARTH
from ssz_paper_a_support import (
    gr_time_dilation_weak_field,
    compare_ssz_gr,
    fidelity_reduction_small_angle,
    fidelity_after_gates,
    verify_linear_scaling,
    verify_numerical_stability,
    coherent_zone_analysis,
    decoherence_enhancement_factor
)


class TestGRComparison:
    """Test SSZ vs GR comparison."""
    
    def test_ssz_equals_gr_weak_field(self):
        """SSZ and GR should be identical in weak field."""
        result = compare_ssz_gr(R_EARTH)
        assert result['relative_difference'] < 1e-10
    
    def test_weak_field_detection(self):
        """Should correctly identify weak field regime."""
        result = compare_ssz_gr(R_EARTH)
        assert result['is_weak_field'] == True
    
    def test_gr_formula(self):
        """GR time dilation should follow sqrt(1 - r_s/r)."""
        from ssz_qubits import schwarzschild_radius
        r_s = schwarzschild_radius(M_EARTH)
        D_GR = gr_time_dilation_weak_field(R_EARTH)
        expected = np.sqrt(1 - r_s / R_EARTH)
        assert abs(D_GR - expected) < 1e-15


class TestFidelityReduction:
    """Test fidelity reduction calculations."""
    
    def test_small_angle_formula(self):
        """1 - F = Delta_Phi^2 / 4."""
        phi = 1e-7
        loss = fidelity_reduction_small_angle(phi)
        expected = phi**2 / 4
        assert abs(loss - expected) < 1e-20
    
    def test_paper_value(self):
        """Paper A: 1-F = 7.4e-15 for 10^9 gates, 1 mm."""
        result = fidelity_after_gates(1.0, 10**9)
        expected_loss = 7.4e-15
        assert abs(result['fidelity_reduction'] - expected_loss) / expected_loss < 0.1
    
    def test_approximation_validity(self):
        """Small angle approximation should be valid for small phases."""
        result = fidelity_after_gates(1.0, 10**9)
        assert result['approximation_valid'] == True


class TestLinearScaling:
    """Test linear scaling verification."""
    
    def test_is_linear(self):
        """Phase drift should scale linearly with height."""
        result = verify_linear_scaling()
        assert result['is_linear'] == True
    
    def test_scaling_constant(self):
        """Scaling constant should be ~1.72e-16 rad/mm/gate."""
        result = verify_linear_scaling()
        expected = 1.72e-16
        actual = result['scaling_constant_per_mm']
        assert abs(actual - expected) / expected < 0.01


class TestNumericalStability:
    """Test numerical stability demonstration."""
    
    def test_closed_form_works(self):
        """Closed-form should give non-zero values."""
        result = verify_numerical_stability()
        assert result['closed_form_works'] == True
    
    def test_direct_fails(self):
        """Direct subtraction should fail for small heights."""
        result = verify_numerical_stability()
        assert result['direct_fails_for_small_heights'] == True
    
    def test_stability_demonstrated(self):
        """Overall stability should be demonstrated."""
        result = verify_numerical_stability()
        assert result['numerical_stability_demonstrated'] == True


class TestCoherentZone:
    """Test coherent zone analysis."""
    
    def test_zone_width_formula(self):
        """Zone width should match z = 4*eps*R^2/r_s."""
        result = coherent_zone_analysis(1e-18)
        assert result['formula_matches'] == True
    
    def test_zone_width_value(self):
        """Zone width should be ~18 mm for eps = 1e-18."""
        result = coherent_zone_analysis(1e-18)
        assert abs(result['zone_width_mm'] - 18.3) < 0.5
    
    def test_half_width(self):
        """Half-width should be zone_width / 2."""
        result = coherent_zone_analysis(1e-18)
        assert abs(result['half_width'] - result['zone_width'] / 2) < 1e-10


class TestDecoherenceEnhancement:
    """Test decoherence enhancement factor."""
    
    def test_unity_for_small_delta_xi(self):
        """Enhancement should be ~1 for small delta_xi."""
        factor = decoherence_enhancement_factor(1e-19)
        assert abs(factor - 1.0) < 1e-15
    
    def test_formula(self):
        """Factor should follow 1 + (delta_xi/xi_ref)^2."""
        delta_xi = 1e-12
        xi_ref = 1e-10
        factor = decoherence_enhancement_factor(delta_xi, xi_ref)
        expected = 1 + (delta_xi / xi_ref)**2
        assert abs(factor - expected) < 1e-15


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
