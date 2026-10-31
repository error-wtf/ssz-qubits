#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests zu Arbeitsauftrag D (Observabilität, nur-photonischer Kanal)."""
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from research.quantum_bus import photon_channel_demo as demo     # noqa: E402


class TestPhotonChannelBlindness:
    def test_pair_states_share_all_m_statistics(self):
        """Zwei verschiedene Paarzustände → identische M-Statistiken."""
        r1, _ = demo.rho_pair_state(demo._V_PHI)
        r2, _ = demo.rho_pair_state(demo._V_OTHER)
        m1 = demo.m_only_statistics(r1)
        m2 = demo.m_only_statistics(r2)
        assert np.max(np.abs(m1 - m2)) < 1e-14
        assert abs(m1[0, 0].real - 1.0) < 1e-12   # beide: M = |0>

    def test_states_are_genuinely_different(self):
        """Negativkontrolle der Gleichheit: Fidelity < 1 — die Zustände sind
        physikalisch verschieden, nur für den M-Kanal ununterscheidbar."""
        _, p1 = demo.rho_pair_state(demo._V_PHI)
        _, p2 = demo.rho_pair_state(demo._V_OTHER)
        assert abs(abs(np.vdot(p1, p2)) ** 2 - 0.5) < 1e-12

    def test_AB_probe_distinguishes(self):
        """Negativkontrolle des Kanals: Mit Zugriff auf A sind die Zustände
        unterscheidbar — Blindheit ist eine Kanaleigenschaft, keine Zustands-
        eigenschaft, und umgekehrt keine Existenzgarantie."""
        r1, _ = demo.rho_pair_state(demo._V_PHI)
        r2, _ = demo.rho_pair_state(demo._V_OTHER)
        assert demo.ab_probe_statistics(r1) != demo.ab_probe_statistics(r2)

    def test_outcome_map_factors_through_M_reduction_iff(self):
        """OPERATIONALE PRÄZISIERUNG (Carnens Feinheit): Die Outcome-Abbildung
        ρ ↦ (Tr E₀ρ, Tr E₁ρ) faktorisiert über die M-Reduktion — Zustände sind
        kanal-unterscheidbar GENAU DANN, wenn ihre M-Reduktionen verschieden
        sind. Beide Richtungen testfixiert (⟺, nicht nur ⟹)."""
        r1, _ = demo.rho_pair_state(demo._V_PHI)
        r2, _ = demo.rho_pair_state(demo._V_OTHER)
        m1 = demo.m_only_statistics(r1)
        m2 = demo.m_only_statistics(r2)
        # (⇐) gleiche M-Reduktion ⇒ identische Outcome-Statistik:
        assert np.max(np.abs(m1 - m2)) < 1e-14
        s1 = [demo._outcome(r1, m) for m in (0, 1)]
        s2 = [demo._outcome(r2, m) for m in (0, 1)]
        assert np.max(np.abs(np.array(s1) - np.array(s2))) < 1e-13
        # (⇒) verschiedene M-Reduktion ⇒ unterscheidbar (Kontrolle mit
        # angereichertem m=1-Zustand):
        r3, _ = demo.rho_pair_state(demo._V_PHI)
        r3[2, 2] += 0.5           # Population in |0, m=1, 0>
        r3[0, 0] -= 0.5           # entnommen aus |0, m=0, 0>
        assert not np.allclose(demo.m_only_statistics(r3),
                               demo.m_only_statistics(r1), atol=1e-10)
        s3 = [demo._outcome(r3, m) for m in (0, 1)]
        assert abs(s3[1] - s1[1]) > 1e-6

    def test_photon_loss_dark_and_invisible(self):
        """Offenes System: Paar-Sektoren emittieren nie (dunkel), M bleibt |0>;
        scheinbare Dimensionsreduktion = Messkanal-Aussage."""
        r1, _ = demo.rho_pair_state(demo._V_PHI)
        r_out = demo.photon_loss_channel(r1)
        assert demo.emission_probability(r_out) < 1e-12
        m_out = demo.m_only_statistics(r_out)
        assert abs(m_out[0, 0].real - 1.0) < 1e-8
