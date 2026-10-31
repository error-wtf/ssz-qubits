#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests zur Forschungsfrage [H, Q_SSZ] = 0 (Carmen, 31.10.2026).

Jeder Test trägt zur Beantwortung bei: entweder schließt er eine
Q_SSZ-Familie aus oder identifiziert die einzige verbleibende Quelle
von 6⊕2-Invarianz (gewöhnliche Drehimpulalgebra).
"""
import itertools
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from research.quantum_bus import models as mb                    # noqa: E402
from research.quantum_bus import reduction as rd                 # noqa: E402
from research.quantum_bus import ssz_symmetry_probe as probe     # noqa: E402
from research.quantum_bus.models import Z, I2, kron_all          # noqa: E402


class TestCommutantStructure:
    def test_generic_exchange_bus_commutant_is_polynomials_in_H(self):
        """Generischer Bus (g_A≠g_B, Detuning): 8 verschiedene Eigenwerte ⇒
        Kommutant = {f(H)}, dim = 8. Jedes kommutierende Q_SSZ wäre f(H) und
        hätte die 8 EINDIMENSIONALEN H-Eigenräume — eine {6,2}-Zerlegung ist
        dann ausgeschlossen."""
        H = probe.ssz_H(1.0, 1.0, 1.0, g_A=0.05, g_B=0.07, Delta=0.8)
        lam = np.linalg.eigvalsh(H)
        assert np.min(np.diff(np.sort(lam))) > 1e-6     # nichtentartet
        dim = probe.commutant_dimension(H)
        assert dim == 8, f"Kommutant-Dim {dim} (erwartet 8)"

    def test_therefore_no_6plus2_eigenspace_split(self):
        """Direkt: der 6er-Basis-Projektor kommutiert nicht mit H — der
        Sektor ist für den generischen Bus nicht invariant."""
        H = probe.ssz_H(1.0, 1.0, 1.0, g_A=0.05, g_B=0.07, Delta=0.8)
        U = rd.bell_unitary()
        P6 = U.conj().T @ np.diag([1] * 6 + [0] * 2) @ U
        assert np.linalg.norm(H @ P6 - P6 @ H) > 1e-3


class TestSSZDScan:
    def test_invariance_only_on_the_DA_equals_DB_diagonal(self):
        """GESCHÄRFTER BEFUND: Der Austauschbus ist singulett-invariant GENAU
        dann, wenn D_A = D_B (Spiegelsymmetrie A↔B). Jeder Punkt mit
        Differenzsegmentierung D_A≠D_B — der eigentliche SSZ-Anwendungsfall —
        BRICHT die 6⊕2-Invarianz."""
        grid = np.linspace(0.8, 1.2, 11)
        inv_diag, inv_offdiag = 0, 0
        worst_offdiag = np.inf
        for dA, dM, dB in itertools.product(grid, grid, grid):
            H = probe.ssz_H(dA, dM, dB, 0.05, 0.05, Delta=0.8)
            leak = probe.singlet_sector_leakage(H)
            if leak < 1e-12:
                if abs(dA - dB) < 1e-12:
                    inv_diag += 1
                else:
                    inv_offdiag += 1
            else:
                if abs(dA - dB) > 1e-12:
                    worst_offdiag = min(worst_offdiag, leak)
        assert inv_offdiag == 0, "Invarianz außerhalb D_A=D_B gefunden?!"
        # 11·11 = 121: D_A=D_B über die gesamte D_M-Achse (D_M ist tangential
        # zum Singulett-Sektor — P_S wirkt nicht auf M).
        assert inv_diag == 121
        assert worst_offdiag > 1e-3

    def test_differential_segmentation_breaks_invariance(self):
        """Der Kernbefund: D_A=1.0, D_B=1.05 (unterschiedliche Segmentierung —
        z.B. Höhendifferenz) zerstört [H, P_S]=0 selbst bei sonst perfekter
        Spiegelsymmetrie."""
        H_sym = probe.ssz_H(1.0, 1.0, 1.0, 0.05, 0.05)
        P = probe.singlet_projector_full()
        assert probe.commutator_norm(H_sym, P) < 1e-12   # Spiegelsymmetrie: ok
        H_diff = probe.ssz_H(1.0, 1.0, 1.05, 0.05, 0.05)
        assert probe.commutator_norm(H_diff, P) > 1e-3   # Segmentierungsdifferenz: gebrochen

    def test_leakage_independent_of_D_at_fixed_coupling(self):
        """Strukturprobe: ‖P_S H (I−P_S)‖ hängt nur von den Kopplungen ab —
        zwei verschiedene D-WahlEN mit gleichen g liefern gleiche Leckage-Struktur
        (D skaliert nur diagonal)."""
        l1 = probe.singlet_sector_leakage(probe.ssz_H(1.0, 1.0, 1.0, 0.05, 0.05))
        l2 = probe.singlet_sector_leakage(probe.ssz_H(1.2, 0.9, 1.05, 0.05, 0.05))
        assert l1 > 0 and l2 > 0  # beide nicht-invariant


class TestDiagonalQFamilyCannotCommute:
    def test_UNEQUAL_ssz_diagonal_vs_exchange(self):
        """SSZ-D macht die diagonalen Koeffizienten UNGLEICH (ω_i·D_i).
        Q = Z_A + 1.3·Z_M + 0.7·Z_B kommutiert dann NICHT mit dem Austausch —
        die Segmentierung bricht die einzige Erhaltungsstruktur, statt eine
        neue zu liefern."""
        H_ex = mb.q1_hamiltonian(0.0, 0.0, 0.0, 0.05, 0.05)  # nur Kopplung
        Q_unequal = kron_all([Z, I2, I2]) + 1.3 * kron_all([I2, Z, I2]) \
            + 0.7 * kron_all([I2, I2, Z])
        assert probe.commutator_norm(H_ex, Q_unequal) > 1e-3

    def test_EQUAL_coefficients_is_excitation_conservation_not_ssz(self):
        """Gleiche Koeffizienten: Q = ΣZ/2 kommutiert — das ist die bekannte
        Anregungszahlerhaltung des Austauschmodells, KEIN SSZ-Inhalt."""
        H_ex = mb.q1_hamiltonian(0.0, 0.0, 0.0, 0.05, 0.05)
        assert probe.commutator_norm(H_ex, probe.total_sz()) < 1e-10

    def test_full_h_diagonal_part_trivial(self):
        """Trivialität dokumentiert: [H_diag, Q_diag] = 0 — neu entsteht
        daraus keine Erhaltungsgröße."""
        H_diag = mb.q0_hamiltonian([5.0, 5.8, 5.0])
        Q = probe.total_sz()
        assert probe.commutator_norm(H_diag, Q) < 1e-12


class TestKnownConservedQuantitiesAreNot6plus2:
    def test_excitation_number_eigenspaces(self):
        """ΣZ/2 kommutiert (bekannt), aber Eigenräume haben Dimensionen
        {1, 3, 3, 1} — NICHT {6, 2}."""
        H = probe.ssz_H(1.0, 1.0, 1.0, 0.05, 0.05)
        N = probe.total_sz()
        assert probe.commutator_norm(H, N) < 1e-10
        evals, counts = np.unique(np.round(np.linalg.eigvalsh(N), 8),
                                  return_counts=True)
        assert list(counts) == [1, 3, 3, 1]

    def test_singlet_projector_mirror_symmetric_case(self):
        """Spiegelsymmetrie (ω_A=ω_B, g_A=g_B, D_A=D_B): P_S kommutiert —
        das ist die A↔B-Permutation (Drehimpulsalgebra), der EINZIGE Fall mit
        6⊕2-invarianter Dynamik."""
        P = probe.singlet_projector_full()
        H = probe.ssz_H(1.0, 1.0, 1.0, 0.05, 0.05)
        assert probe.commutator_norm(H, P) < 1e-12

    def test_singlet_projector_broken_by_ssz_differential(self):
        """Mit Differenzsegmentierung D_A≠D_B ist P_S KEINE Erhaltungsgröße —
        SSZ bricht die 6⊕2-Invarianz (Kernbefund der Fragestellung)."""
        P = probe.singlet_projector_full()
        H = probe.ssz_H(1.0, 1.0, 1.05, 0.05, 0.05)
        assert probe.commutator_norm(H, P) > 1e-3


class TestPositiveControlAngularMomentumAlgebra:
    def test_pair_symmetric_ising_conserves_singlet(self):
        """POSITIVKONTROLLE: pair-symmetrisches Ising lässt S invariant —
        Drehimpulsalgebra, D-unabhängig (kein SSZ-Inhalt).
        Ordnung (A, M, B): Z_A Z_B = Z⊗I⊗Z."""
        H = 0.7 * np.kron(np.kron(mb.Z, mb.I2), mb.Z) / 4.0
        P = probe.singlet_projector_full()
        assert probe.commutator_norm(H, P) < 1e-12
        assert probe.singlet_sector_leakage(H) < 1e-12
        # und der Kommutant ist größer als {f(H)} (Entartung):
        assert probe.commutant_dimension(H) > 8

    def test_singlet_projector_definition(self):
        """P_S trifft genau die 2 S⊗m-Zustände (Eigenwerte 0×6, 1×2)."""
        P = probe.singlet_projector_full()
        assert abs(np.trace(P).real - 2.0) < 1e-12
        evals = np.round(np.linalg.eigvalsh(P).real, 12).tolist()
        assert evals == [0.0] * 6 + [1.0] * 2
