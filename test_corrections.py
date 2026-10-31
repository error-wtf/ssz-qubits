#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test the corrected physics functions"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
from ssz_qubits import (
    Qubit, QubitPair, qubit_pair_segment_mismatch, 
    ssz_decoherence_rate, effective_T2, pair_decoherence_time,
    M_EARTH, R_EARTH
)
import numpy as np
import pytest

print('KORRIGIERTE WERTE - PHYSIKALISCH KORREKT')
print('=' * 70)

# Test 1: Phase drift per gate
print()
print('1. Phase Drift per Gate (1 mm Hoehendifferenz):')
q1 = Qubit(id='Q1', x=0, y=0, z=0, gate_time=50e-9)
q2 = Qubit(id='Q2', x=0, y=0, z=0.001, gate_time=50e-9)  # 1 mm
pair = QubitPair(q1, q2)
mismatch = qubit_pair_segment_mismatch(pair, M_EARTH)
print(f'   Delta_Xi = {mismatch["delta_xi"]:.3e}')
print(f'   Phase/Gate = {mismatch["phase_drift_per_gate"]:.3e} rad')
print(f'   Decoherence Enhancement = {mismatch["decoherence_enhancement"]:.6f}')
print()

# Verify manually
omega = 2 * np.pi * 5e9
delta_xi = 1.09e-19
t_gate = 50e-9
phase_manual = omega * delta_xi * t_gate
print(f'   Manual check: omega*delta_xi*t_gate = {phase_manual:.3e} rad')
print()

# Test 2: SSZ Decoherence Rate
print('2. SSZ Decoherence Rate:')
q = Qubit(id='Q1', x=0, y=0, z=0, coherence_time_T2=100e-6)
gamma = ssz_decoherence_rate(q, M_EARTH)
T2_eff = effective_T2(q, M_EARTH)
gamma_base = 1.0 / 100e-6
ssz_fraction = (gamma - gamma_base) / gamma_base * 100
print(f'   Base rate (1/T2) = {gamma_base:.3e} /s')
print(f'   Total rate = {gamma:.3e} /s')
print(f'   SSZ contribution = {ssz_fraction:.6f} %')
print(f'   Effective T2 = {T2_eff*1e6:.3f} us (vs 100 us intrinsic)')
print()

# Test 3: Pair Decoherence
print('3. Pair Decoherence (1 mm height diff):')
T2_pair = pair_decoherence_time(pair, M_EARTH)
print(f'   Pair T2 = {T2_pair*1e6:.3f} us')
print(f'   (Expected: ~50 us since 2 qubits add rates)')
print()

print('=' * 70)
print('FAZIT: SSZ-Effekte sind bei Earth-scale WINZIG (< 10^-6 %)')
print('       Das ist physikalisch korrekt!')
print('=' * 70)


# =============================================================================
# Echte pytest-Regressionen (Reparatur 2026-10-31, T2: das Skript war vorher
# Print-only mit 0 Assertions; die Prints bleiben als Demo erhalten).
# =============================================================================

def test_phase_drift_per_gate_matches_manual_and_audit_value():
    """Phase/Gate (1 mm, 5 GHz, 50 ns) ≈ 1.71628e−16 rad — Rechenvorhersage
    unter Modellannahmen, KEINE Messung (Audit §5)."""
    q1 = Qubit(id='Q1', x=0, y=0, z=0, gate_time=50e-9)
    q2 = Qubit(id='Q2', x=0, y=0, z=0.001, gate_time=50e-9)
    mismatch = qubit_pair_segment_mismatch(QubitPair(q1, q2), M_EARTH)
    assert mismatch['delta_time_dilation'] == pytest.approx(1.0926195757e-19, rel=1e-4)
    assert mismatch['phase_drift_per_gate'] == pytest.approx(1.71628e-16, rel=1e-3)


def test_ssz_decoherence_contribution_tiny_at_earth_scale():
    """SSZ-Anteil an der Dekohärenzrate auf der Erde < 1e-4 % (Print-Aussage
    wird jetzt geprüft statt nur behauptet)."""
    q = Qubit(id='Q1', x=0, y=0, z=0, coherence_time_T2=100e-6)
    gamma = ssz_decoherence_rate(q, M_EARTH)
    gamma_base = 1.0 / 100e-6
    ssz_fraction = (gamma - gamma_base) / gamma_base * 100
    assert 0.0 <= ssz_fraction < 1e-4


def test_pair_decoherence_time_halves_T2():
    pair = QubitPair(Qubit(id='Q1', x=0, y=0, z=0),
                     Qubit(id='Q2', x=0, y=0, z=0.001))
    T2_pair = pair_decoherence_time(pair, M_EARTH)
    assert 45e-6 < T2_pair < 55e-6
