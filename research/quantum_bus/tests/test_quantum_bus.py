#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-4-Tests: Quantum-Bus-Referenzmodelle Q0–Q3 + 6⊕2 + Schur.
Alle Größen mit toleranzbegründeten Grenzen; negativer Test (Q0: KEINE
Verschränkung aus lokalen Z-Phasen) eingeschlossen.
"""
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from research.quantum_bus import models as mb
from research.quantum_bus import reduction as rd
from research.quantum_bus import bus_effective as be


class TestQ0NoBus:
    def test_local_z_phases_create_no_entanglement(self):
        H = mb.q0_hamiltonian([5.0, 6.3, 7.1])
        psi0 = np.zeros(8, dtype=complex)
        psi0[0b000] = 1.0            # |000> Produktzustand
        for t in (0.1, 1.0, 7.7):
            U = mb.propagate(H, t)
            psi = U @ psi0
            assert np.isclose(np.linalg.norm(psi), 1.0)
            rho = np.outer(psi, psi.conj())
            S = rd.von_neumann_entropy(rho, keep=[0], dims=[2, 2, 2])
            assert S < 1e-12, f"t={t}: lokales Modell erzeugt Entropie {S}"


class TestQ1ThreeQubitBus:
    H = mb.q1_hamiltonian(5.0, 5.4, 5.0, 0.02, 0.03)

    def test_hermitian(self):
        assert np.max(np.abs(self.H - self.H.conj().T)) < 1e-13

    def test_unitary_and_norm_and_energy(self):
        t = 1.7
        U = mb.propagate(self.H, t)
        assert np.max(np.abs(U.conj().T @ U - np.eye(8))) < 1e-10
        psi0 = np.zeros(8, dtype=complex)
        psi0[0b100] = 1.0 / np.sqrt(2)
        psi0[0b010] = 1.0 / np.sqrt(2)
        psi = U @ psi0
        assert np.isclose(np.linalg.norm(psi), 1.0, atol=1e-10)
        E0 = np.vdot(psi0, self.H @ psi0).real
        E1 = np.vdot(psi, self.H @ psi).real
        assert abs(E1 - E0) < 1e-9

    def test_total_sz_conserved(self):
        N = mb.total_sz(3)
        assert np.max(np.abs(self.H @ N - N @ self.H)) < 1e-11

    def test_spectrum_real(self):
        lam = np.linalg.eigvalsh(self.H)
        assert np.all(np.isfinite(lam))


class TestExplicit6Plus2:
    def test_unitary_is_unitary(self):
        U = rd.bell_unitary()
        assert np.max(np.abs(U.conj().T @ U - np.eye(8))) < 1e-12

    def test_bell_definition(self):
        """U|00m> muss |T+>|m> sein (Konvention T+ = |00>)."""
        U = rd.bell_unitary()
        psi = U @ np.eye(8)[0b000]  # |00 m=0>
        assert abs(psi[0] - 1.0) < 1e-12            # Zeile 0 = |T+ m=0>
        psi = U @ np.eye(8)[0b001]  # |00 m=1>
        assert abs(psi[1] - 1.0) < 1e-12            # Zeile 1 = |T+ m=1>

    def test_singlet_row(self):
        """U|01 m=0> = (|T0>|0> − |S>|0>)/√2 — S-Anteil liegt im 2er-Block."""
        U = rd.bell_unitary()
        psi = U @ np.eye(8)[0b010]  # |01 m=0>
        assert abs(psi[2] - 1 / np.sqrt(2)) < 1e-12   # |T0 m=0>
        assert abs(psi[6] - 1 / np.sqrt(2)) < 1e-12   # |S m=0>

    def test_generic_h_not_block_diagonal(self):
        """NEGATIVKONTROLLE: generischer Austauschbus koppelt S⊗M an T⊗M —
        der 6×2-Block ist NICHT null (Sektor nicht invariant)."""
        H = mb.q1_hamiltonian(5.0, 5.4, 5.0, 0.02, 0.03)
        _, _, B62, _ = rd.block_decompose(H)
        assert np.linalg.norm(B62) > 1e-3

    def test_symmetric_ising_IS_block_diagonal(self):
        """Nur wenn die Symmetrie es verlangt: Ising auf dem Paar lässt den
        Singulett-Sektor invariant → B62 = 0 exakt."""
        J = 0.7
        ZAB = np.kron(mb.Z, mb.Z)
        H = J * np.kron(ZAB, mb.I2) / 4.0
        _, _, B62, _ = rd.block_decompose(H)
        assert np.max(np.abs(B62)) < 1e-12


class TestSchurComplement:
    H = mb.q1_hamiltonian(5.0, 5.0 + 0.8, 5.0, 0.01, 0.01)  # g/Δ = 0.0125

    def test_exact_eigenvalues_satisfy_schur_condition(self):
        lam_low = be.low_sector_eigenpairs(self.H, be.LOW_INDICES_Q1,
                                           be.HIGH_INDICES_Q1)
        assert len(lam_low) == 4  # 4+4-Split nach M-Anregung
        worst = max(be.schur_residual(self.H, E, be.LOW_INDICES_Q1,
                                      be.HIGH_INDICES_Q1) for E in lam_low)
        assert worst < 1e-8, f"σ_min-Residuum {worst}"

    def test_schur_residual_nonzero_away_from_spectrum(self):
        assert be.schur_residual(self.H, 4.0, be.LOW_INDICES_Q1,
                                 be.HIGH_INDICES_Q1) > 1e-3

    def test_static_sw_error_scales_quadratically(self):
        res = be.error_vs_detuning([0.02, 0.04], Delta=0.8)
        err_small, err_big = res[0][1], res[1][1]
        assert err_small > 0 and err_big > 0
        ratio = err_big / err_small
        assert 2.5 < ratio < 6.5, f"SW-Fehlskalung {ratio} (erwartet ≈4)"

    def test_static_sw_fails_near_resonance(self):
        """Δ → 0: statische Elimination MUSS versagen (Doku-Punkt §5.2)."""
        res = be.error_vs_detuning([0.2, 0.4], Delta=1e-9)
        assert res[-1][1] > 1e-3  # riesiger Fehler nahe Resonanz


class TestQ2Resonator:
    def test_dimension_and_hermiticity(self):
        H = mb.q2_hamiltonian(5.0, 5.0, 5.0, 0.05, 0.05, n_max=6)
        assert H.shape == (4 * 7, 4 * 7)
        assert np.max(np.abs(H - H.conj().T)) < 1e-12

    def test_excitation_conservation(self):
        H = mb.q2_hamiltonian(5.0, 5.0, 5.0, 0.1, 0.1, n_max=6)
        N = mb.total_excitation_q2(6)
        assert np.max(np.abs(H @ N - N @ H)) < 1e-10

    def test_truncation_convergence(self):
        g, wr = 0.5, 10.0   # g/ω_r = 0.05
        H8 = mb.q2_hamiltonian(5.0, 5.0, wr, g, g, n_max=8)
        H14 = mb.q2_hamiltonian(5.0, 5.0, wr, g, g, n_max=14)
        lam8 = np.sort(np.linalg.eigvalsh(H8).real)[:6]
        lam14 = np.sort(np.linalg.eigvalsh(H14).real)[:6]
        assert np.max(np.abs(lam8 - lam14)) < 1e-8

    def test_dispersive_shift_present(self):
        """Dispersion: Eigenwerte hängen nichtlinear von g ab (virtuelle
        Anregungen); bei g=0 exakt produktartig."""
        H0 = mb.q2_hamiltonian(5.0, 5.0, 10.0, 0.0, 0.0, n_max=6)
        Hg = mb.q2_hamiltonian(5.0, 5.0, 10.0, 0.5, 0.5, n_max=6)
        lam0 = np.sort(np.linalg.eigvalsh(H0).real)
        lamg = np.sort(np.linalg.eigvalsh(Hg).real)
        assert np.max(np.abs(lam0 - lamg)) > 1e-3


class TestQ3DephasingChannel:
    def test_trace_and_positivity_preserved(self):
        rho = np.zeros((4, 4), dtype=complex)
        rho[0, 0] = rho[1, 1] = 0.5
        rho[0, 1] = 0.3
        out = mb.dephasing_channel(rho, 0.25, qubit=0, n_qubits=2)
        assert abs(np.trace(out).real - 1.0) < 1e-14
        assert np.min(np.linalg.eigvalsh(out)) > -1e-14

    def test_coherence_decay_factor(self):
        """Off-Diagonale des dephasierten Qubits skaliert mit (1−2p).
        |00><10| unterscheidet sich im ERSTEN Qubit → Dephasing auf qubit=0."""
        rho = np.zeros((4, 4), dtype=complex)
        rho[0, 0] = rho[1, 1] = 0.5
        rho[0, 1] = 0.4   # |00><01|: unterscheidet sich im zweiten Qubit
        rho[0, 2] = 0.4   # |00><10|: unterscheidet sich im ersten Qubit
        out = mb.dephasing_channel(rho, 0.25, qubit=0, n_qubits=2)
        assert abs(out[0, 1] - 0.4) < 1e-14              # unberührt
        assert abs(out[0, 2] - (1 - 2 * 0.25) * 0.4) < 1e-14


class TestMetricsAndCHSH:
    def test_concurrence_bell_vs_product(self):
        bell = np.zeros((4, 4), dtype=complex)
        bell[0, 0] = bell[3, 3] = 0.5
        bell[0, 3] = bell[3, 0] = 0.5     # |Φ+><Φ+|  (|00>=0, |11>=3)
        assert abs(rd.concurrence(bell) - 1.0) < 1e-12
        prod = np.zeros((4, 4), dtype=complex)
        prod[0, 0] = 1.0                   # |00><00|
        assert rd.concurrence(prod) == 0.0

    def test_bell_fidelity_separate_from_entanglement(self):
        """Lokaler Z-Bias ändert die Fidelity ZUM Bell-Zustand, aber NICHT die
        Verschränkung — die beiden Größen sind scharf getrennt."""
        theta = 0.3
        psi = (np.array([1, 0, 0, np.exp(-1j * theta)]) / np.sqrt(2))
        target = np.array([1, 0, 0, 1]) / np.sqrt(2)
        F = rd.bell_fidelity(psi, target)
        assert F == pytest.approx(np.cos(theta / 2) ** 2, rel=1e-12)
        rho = np.outer(psi, psi.conj())
        assert rd.concurrence(rho) == pytest.approx(1.0, abs=1e-6)  # bleibt max. verschränkt

    def test_chsh_bounds_and_rotation_invariance(self):
        bell = np.array([1, 0, 0, 1]) / np.sqrt(2)   # |Φ+>
        rho = np.outer(bell, bell.conj())
        # feste Standard-Achsen: a=z, a'=x, b=(z+x)/√2, b'=(z−x)/√2 → 2√2
        a  = np.array([0.0, 0.0, 1.0])
        a2 = np.array([1.0, 0.0, 0.0])
        b  = np.array([1.0, 0.0, 1.0]) / np.sqrt(2)
        b2 = np.array([-1.0, 0.0, 1.0]) / np.sqrt(2)
        S_fix = rd.chsh_fixed(rho, axes=(a, a2, b, b2))
        assert S_fix == pytest.approx(2 * np.sqrt(2), abs=1e-9)
        # Maximum über ALLE lokalen Achsen (Horodecki exakt):
        S_max = rd.chsh_max(rho)
        assert S_max == pytest.approx(2 * np.sqrt(2), abs=1e-9)
        assert S_max <= 2 * np.sqrt(2) + 1e-9          # Tsirelson
        # Z-Rotation des Zustands: Max CHSH unverändert (Horodecki exakt)
        th = 0.7
        U = np.kron(np.diag([np.exp(-1j * th / 2), np.exp(1j * th / 2)]),
                    np.eye(2))
        psi_r = U @ bell
        S_r = rd.chsh_max(np.outer(psi_r, psi_r.conj()))
        assert S_r == pytest.approx(2 * np.sqrt(2), abs=1e-9)
        # separabler Zustand: kein Verstoß
        prod = np.zeros((4, 4), dtype=complex)
        prod[0, 0] = 1.0
        assert rd.chsh_max(prod) <= 2.0 + 1e-9

    def test_projection_leakage(self):
        U, P6, P2 = rd.projectors_6_2()
        psi = np.eye(8)[0b010] / np.sqrt(2) + np.eye(8)[0b100] / np.sqrt(2)
        proj = P6 @ psi
        p_succ = float(np.linalg.norm(proj) ** 2)
        assert 0.0 < p_succ < 1.0
        psi_norm = proj / np.linalg.norm(proj)
        rho = np.outer(psi_norm, psi_norm.conj())
        assert rd.leakage(rho, P2) < 1e-12
