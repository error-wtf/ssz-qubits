#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests: Der D_A−D_B-Mischterm S↔T0 (Carmens Folgefrage).

Kernaussagen (alle exakt getestet):
 1. Mischmatrixelement = (ω_A D_A − ω_B D_B)/2 — Bell-Basis-projizierte
    Differenzuhr. |T±> werden NICHT gemischt.
 2. S↔T0-Rabi-Dynamik mit Frequenz |m| (Zweiniveau innerhalb des N-Manifolds,
    numerisch gegen die volle 8×8-Entwicklung geprüft).
 3. SSZ/GR-Verhältnis der Mischterme (kleine Höhendifferenz) = 2φ ≈ 3.236 —
    der einzige SSZ-spezifische Inhalt, bereits durch Cassini/LLR ausgeschlossen.
"""
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from research.quantum_bus import models as mb                      # noqa: E402
from research.quantum_bus import ssz_symmetry_probe as probe       # noqa: E402
from research.quantum_bus import ssz_mixing_analysis as mix        # noqa: E402


class TestMixingElementFormula:
    def test_matrix_element_is_differential_clock(self):
        """<T0|H_pair|S> = (ω_A D_A − ω_B D_B)/2 — exakt, M-diagonal."""
        vals = mix.mixing_element_S_T0(1.0, 1.05, 5.0)
        expected = (5.0 * 1.0 - 5.0 * 1.05) / 2.0
        for v in vals:
            assert v == pytest.approx(expected, rel=1e-12)

    def test_equal_D_gives_zero_mixing(self):
        vals = mix.mixing_element_S_T0(1.0, 1.0, 5.0)
        assert all(abs(v) < 1e-14 for v in vals)

    def test_Tpm_not_mixed(self):
        """Differenzuhr verschiebt |T±> nur diagonal — kein S↔T±-Element.
        Q1-Ordnung: |T+ m>=|0,m,0> (idx 2m), |T− m>=|1,m,1> (idx 5+2m)."""
        H = mix.pairing_diagonal(1.0, 1.05, 5.0)
        for m in range(2):
            v_S = np.zeros(8, dtype=complex)
            v_S[2 * m + 1] = 1 / np.sqrt(2)
            v_S[4 + 2 * m] = -1 / np.sqrt(2)
            v_Tp = np.zeros(8, dtype=complex)
            v_Tp[2 * m] = 1.0                                # |0, m, 0>
            v_Tm = np.zeros(8, dtype=complex)
            v_Tm[5 + 2 * m] = 1.0                            # |1, m, 1>
            assert abs(np.vdot(v_Tp, H @ v_S)) < 1e-14
            assert abs(np.vdot(v_Tm, H @ v_S)) < 1e-14


class TestRabiDynamics:
    def test_s_to_t0_oscillation_frequency(self):
        """|S m=0>(0) → Population oszilliert mit |m| = |ω(D_A−D_B)|/2.
        g=0.001 ≪ m=0.125: Zweiniveau-Näherung sauber (Störanteil ~ (g/√2/m)²)."""
        w, dA, dB = 5.0, 1.0, 1.05
        m = abs(w * (dA - dB)) / 2.0
        H_diag = mix.pairing_diagonal(dA, dB, w)
        H_ex = mb.q1_hamiltonian(0.0, 0.0, 0.0, 0.001, 0.001)  # symmetrisch, schwach
        H = H_diag + H_ex
        v_S = np.zeros(8, dtype=complex)
        v_S[1] = 1 / np.sqrt(2)
        v_S[4] = -1 / np.sqrt(2)
        U = mb.propagate(H, np.pi / (2 * m))
        psi = U @ v_S
        v_T0 = np.zeros(8, dtype=complex)
        v_T0[1] = 1 / np.sqrt(2)
        v_T0[4] = 1 / np.sqrt(2)
        pT0 = abs(np.vdot(v_T0, psi)) ** 2
        assert pT0 == pytest.approx(1.0, rel=1e-4)


class TestSSZvsGRContent:
    def test_ratio_leading_order_is_2phi(self):
        """SSZ/GR-Mischterme (Leading Order) → 2φ ≈ 3.236.
        Der EINZIGE SSZ-spezifische Inhalt; führender Koeffizient bereits
        durch Cassini/LLR (γ=1) ausgeschlossen → kein neues Fenster."""
        ratio = mix.gr_mixing_ratio()
        phi = (1 + 5 ** 0.5) / 2
        assert ratio == pytest.approx(2 * phi, rel=1e-6)

    def test_no_bus_required_for_mixing(self):
        """Der Mischterm existiert im diagonalen Teil allein — er ist keine
        Bus-Wechselwirkung (H_ex trägt nichts zu S↔T0 bei bei Symmetrie)."""
        H_ex = mb.q1_hamiltonian(0.0, 0.0, 0.0, 0.05, 0.05)
        P_S = probe.singlet_projector_full()
        P_T0 = np.diag([1 if i in (1, 4) else 0 for i in range(8)])
        cross = P_S @ H_ex @ P_T0
        assert np.max(np.abs(cross)) < 1e-12
