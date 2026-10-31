#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests: Arbeitsaufträge B (symbolische 6⊕2), C (Schur vs SW im S-Sektor),
E2 (Lokalitätsfaktorisierung) des Übergabedokuments. Negativkontrollen inklusive.
"""
import sys
from pathlib import Path

import numpy as np
import pytest
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from research.quantum_bus import symbolic_symmetry as ss       # noqa: E402
from research.quantum_bus import models as mb                  # noqa: E402
from research.quantum_bus import reduction as rd               # noqa: E402
from research.quantum_bus import ssz_symmetry_probe as probe   # noqa: E402
from research.quantum_bus import bus_effective as be           # noqa: E402

# S-Sektor in Q1-Ordnung (A, M, B): S⊗M = {(0,m,1),(1,m,0)} → Indizes 1,4 (m=0), 3,6 (m=1)
S_IDX = [1, 3, 4, 6]
COMP_IDX = [0, 2, 5, 7]   # T± ⊗ M


class TestSymbolicSingletProjector:
    def test_trace_ranks_eigenvalues(self):
        """Spur(P_s)=2, Spur(P_t)=6, charpoly = x⁶(x−1)² → Ränge 2/6."""
        P_s = ss.singlet_projector()
        P_t = ss.triplet_projector()
        assert sp.simplify(P_s.trace()) == 2
        assert sp.simplify(P_t.trace()) == 6
        x = P_s.charpoly().gen
        assert sp.simplify(P_s.charpoly().as_expr()
                           - x ** 6 * (x - 1) ** 2) == 0

    def test_idempotent(self):
        P_s = ss.singlet_projector()
        assert ss.is_zero_matrix(P_s * P_s - P_s)

    def test_matches_numeric_probe_projector(self):
        P_sym = np.array(ss.singlet_projector().tolist(), dtype=complex)
        P_num = probe.singlet_projector_full()
        assert np.max(np.abs(P_sym - P_num)) < 1e-14


class TestSymbolicCommutator:
    def test_commutator_vanishes_at_mirror_symmetry(self):
        """[H, P_s] = 0 exakt für ω_A=ω_B ∧ g_A=g_B ∧ D_A=D_B (symbolisch)."""
        C = ss.commutator(ss.H_full(), ss.singlet_projector())
        assert ss.is_zero_matrix(ss.symmetrize(C))

    def test_commutator_generic_nonzero(self):
        """Negativkontrolle: generische Parameter → [H,P_s] ≠ 0."""
        C = ss.commutator(ss.H_full(), ss.singlet_projector())
        assert not ss.is_zero_matrix(C)

    def test_symmetric_drive_preserves(self):
        """Symmetrischer Drive ε(X_A+X_B) erhält [H,P_s]=0."""
        H = ss.H_full(drive=True)
        C = ss.commutator(H, ss.singlet_projector())
        assert ss.is_zero_matrix(ss.symmetrize(C))   # symmetrize setzt eA=eB

    def test_asymmetric_drive_breaks(self):
        """Negativkontrolle: ε_A≠ε_B bricht [H,P_s] bei sonst voller Symmetrie."""
        H = ss.H_full(drive=True).subs({ss.wA: ss.wB, ss.gA: ss.gB,
                                        ss.dA: ss.dB, ss.eA: 2, ss.eB: 1})
        C = ss.commutator(H, ss.singlet_projector()).applyfunc(sp.simplify)
        assert not ss.is_zero_matrix(C)


class TestSectorMixing:
    def test_Ps_H_Pt_vanishes_at_symmetry(self):
        """P_s H P_t = 0 exakt an der Spiegelsymmetrie (Blockdiagonalität)."""
        assert ss.is_zero_matrix(ss.symmetrize(ss.mixing_block_S_T0()))

    def test_Ps_H_Pt_generic_nonzero(self):
        assert not ss.is_zero_matrix(ss.mixing_block_S_T0())


class TestSchurVsSW_S_Sector:
    def _exact_S_support(self, H):
        lam, vecs = np.linalg.eigh(H)
        out = []
        for k in range(len(lam)):
            if float(np.sum(np.abs(vecs[S_IDX, k]) ** 2)) >= 0.99:
                out.append(float(lam[k]))
        return np.array(sorted(out))

    def test_schur_residual_zero_at_exact_eigenvalues(self):
        """det(H_eff(E)−E)=0: σ_min(H_eff(E)−E) ≈ 0 an exakten S-Eigenwerten."""
        H = mb.q1_hamiltonian(5.0, 5.8, 5.0, 0.01, 0.01)
        exact = self._exact_S_support(H)
        assert len(exact) == 4
        for E in exact:
            assert be.schur_residual(H, E, S_IDX, COMP_IDX) < 1e-10

    def test_sw_error_scales_quadratically_in_g(self):
        """Statische SW-Näherung: Fehler O(g²) (Faktor ≈4 bei Verdopplung von g);
        Negativkontrolle g=0: exakt."""
        errs = []
        for g in (0.005, 0.01):
            H = mb.q1_hamiltonian(5.0, 5.8, 5.0, g, g)
            exact = self._exact_S_support(H)
            E0 = float(exact.mean())
            Hsw = be.schrieffer_wolff_static(H, E0, S_IDX, COMP_IDX)
            approx = np.sort(np.linalg.eigvalsh(Hsw).real)
            # die 4 Näherungswurzeln den 4 exakten S-Werten zuordnen:
            err = float(max(min(abs(a - e) for a in approx) for e in exact))
            errs.append(err)
        H0 = mb.q1_hamiltonian(5.0, 5.8, 5.0, 0.0, 0.0)
        exact0 = self._exact_S_support(H0)
        for E in exact0:
            assert be.schur_residual(H0, E, S_IDX, COMP_IDX) < 1e-12
        # O(g²): Fehler/g² ≈ konstant (hier ≈ 2.5); Absolutwerte klein:
        assert errs[0] < 5e-4
        assert 2.0 < errs[1] / max(errs[0], 1e-15) < 8.0
        c0, c1 = errs[0] / 0.005 ** 2, errs[1] / 0.01 ** 2
        assert abs(c1 / c0 - 1) < 0.6   # g²-Skalierung (kein lineares g-Verhalten)


class TestLocalFactorization:
    def test_diagonal_ssz_evolution_is_product(self):
        """E2: U(t) der reinen SSZ-Diagonale = U_A⊗U_M⊗U_B (bit-exakt) —
        die skalare Segmentierung ist rein lokale Phase."""
        t, wa, wm, wbp = 0.37, 5.0, 5.8, 5.0
        H_diag = mb.q0_hamiltonian([wa, wm, wbp])
        U = mb.propagate(H_diag, t)
        UA = np.diag([np.exp(-1j * wa * t / 2), np.exp(1j * wa * t / 2)])
        UM = np.diag([np.exp(-1j * wm * t / 2), np.exp(1j * wm * t / 2)])
        UB = np.diag([np.exp(-1j * wbp * t / 2), np.exp(1j * wbp * t / 2)])
        assert np.max(np.abs(U - mb.kron_all([UA, UM, UB]))) < 1e-12

    def test_no_entanglement_from_scalar_D_plus_exchange_control(self):
        """Produktzustand unter reiner Diagonale: Paar-Concurrence = 0.
        Negativkontrolle: Austausch g≠0 erzeugt Concurrence > 0."""
        v = np.array([1, 1], dtype=complex) / np.sqrt(2)
        psi0 = np.kron(np.kron(v, v), v)          # (8,) Produktzustand
        assert psi0.shape == (8,)
        H_diag = mb.q0_hamiltonian([5.0 * 1.0, 5.8 * 1.05, 5.0 * 0.95])
        psi = mb.propagate(H_diag, 0.41) @ psi0
        rho = np.outer(psi, psi.conj())
        rho_pair = rd.partial_trace(rho, keep=[0, 2], dims=[2, 2, 2])
        assert abs(rd.concurrence(rho_pair)) < 1e-12
        # Kontrolle: Austausch erzeugt Paar-Verschränkung über M (O((g·t)²)):
        H_ex = mb.q1_hamiltonian(5.0, 5.8, 5.0, 0.5, 0.5)
        psi2 = mb.propagate(H_ex, 2.0) @ psi0
        rho2 = np.outer(psi2, psi2.conj())
        rho2_pair = rd.partial_trace(rho2, keep=[0, 2], dims=[2, 2, 2])
        assert rd.concurrence(rho2_pair) > 1e-3
