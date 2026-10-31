#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests: DOPPELTEST 8→x (Experimente A, B, C).
Positive UND negative Kontrollen je Hypothese; echte Assertions; die
Abbruchkriterien des Auftrags sind als Tests kodiert.
"""
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from research.quantum_bus import doppeltest_8tox as dt             # noqa: E402
from research.quantum_bus import reduction as rd                   # noqa: E402
from research.quantum_bus import ssz_symmetry_probe as probe       # noqa: E402

T_GRID = np.linspace(0.05, 3.0, 24)


# ============================ Experiment A ==================================

class TestA_Reduction:
    def test_projectors_rank_and_consistency(self):
        """Ränge 6/2, Idempotenz, Komplementarität, Q1-Ordnungskonsistenz."""
        U, P6, P2 = dt.a2_projectors()
        for P, r in ((P6, 6), (P2, 2)):
            assert abs(np.trace(P).real - r) < 1e-10
            assert np.allclose(P @ P, P, atol=1e-10)
            assert np.linalg.eigvalsh(P).min() > -1e-12
        assert np.allclose(P2, probe.singlet_projector_full(), atol=1e-12)

    def test_commutator_mirror_vs_differential(self):
        """Negativbefund für H-RED: [H,P]=0 NUR bei Spiegelsymmetrie —
        das ist dynamische Invarianz, KEINE physikalische Verbotenheit."""
        n_sym, n_dif = dt.a3_commutator_norms()
        assert n_sym < 1e-12
        assert n_dif > 1e-3

    def test_no_constraint_restriction(self):
        """KERNTEST GEGEN H-RED: Lokale zulässige Operationen verbinden die
        Sektoren (Kreuznorm > 0) und vollrangige Zustände sind zulässig —
        es existiert KEIN Constraint, der auf 6 oder 2 beschränkt."""
        cross, full_rank_ok = dt.a4_no_constraint_restriction()
        assert cross > 0.1
        assert full_rank_ok

    def test_leakage_mirror_zero_differential_positive(self):
        """Dynamik: Spiegelsymmetrie → kein P6→P2-Leakage; Differenz-
        segmentierung → messbares Leakage (getrieben vom Differenzuhr-Mix).
        Positivkontrolle: g_A≠g_B leakt ebenfalls (keine SSZ-Spezialität)."""
        out = dt.a5_leakage_from_P6(T_GRID)
        out2 = dt.a5_leakage_from_P6(T_GRID, g_A=0.05, g_B=0.07)
        assert out["mirror"] < 1e-10
        assert out["differential"] > 0.1
        assert out2["differential"] > 0.1

    def test_four_way_classification(self):
        """Vierfache Trennung dokumentiert und maschinenlesbar."""
        cls = dt.a6_four_way_classification()
        assert cls["gauge_redundancy"][0] == "none"
        assert cls["physically_forbidden_states"][0] == "none"
        assert cls["dynamical_invariance"][0] == "mirror_symmetric_only"


# ============================ Experiment B ==================================

class TestB_Observability:
    def test_indistinguishable_family(self):
        """ρ₁≠ρ₂ mit M(ρ₁)=M(ρ₂): kontinuierliche Familie, alle kanal-gleich.
        Positivkontrolle: die Zustände sind wirklich verschieden
        (AB-Observablen trennen die Endpunkte)."""
        fam = dt.b2_indistinguishable_family()
        # M-Outcomemap: E_m = I_AB ⊗ |m><m| — in Q1-Ordnung ist m Bit 1:
        E0 = np.diag([1.0 if (i // 2) % 2 == 0 else 0.0 for i in range(8)])
        assert abs(np.real(np.trace(E0 @ fam[0]))
                   - np.real(np.trace(E0 @ fam[-1]))) < 1e-12
        # Verschiedenheit der Endpunkte über AB-Observablen:
        ZA = np.diag([1 if (i // 4) == 0 else -1 for i in range(8)])
        v0 = float(np.real(np.trace(ZA @ fam[0])))
        v1 = float(np.real(np.trace(ZA @ fam[-1])))
        assert abs(v0 - v1) > 0.1

    def test_supplementary_channel_distinguishes(self):
        """Gegenprobe zu H-OBS-Nichtexistenz: ein zweiter zulässiger Kanal
        (Positivität+Vollständigkeit geprüft) trennt die Familie."""
        fam = dt.b2_indistinguishable_family()
        outcomes = dt.b3_supplementary_channel(fam)
        assert max(outcomes) - min(outcomes) > 0.1
        assert all(0.0 <= p <= 1.0 + 1e-12 for p in outcomes)

    def test_observation_map_rank_kernel_algebra(self):
        """2-Outcomes: linearer Rang 2 auf Herm(8) (dim 64), Kern-Dim 62;
        Beobachtungs-Algebra ≅ B(C²), reelle Dimension 4."""
        rank, kdim, alg_dim, alg = dt.b4_channel_quantities()
        assert (rank, kdim, alg_dim) == (2, 62, 4)
        # Algebra-Erzeuger sind nicht alle proportional — dim wirklich 4:
        stacked = np.array([a.flatten() for a in alg])
        assert np.linalg.matrix_rank(stacked, tol=1e-10) == 4

    def test_time_conversion_of_blindness(self):
        """C-Kern: Mit Bus (g≠0) werden initial blind-paare später
        unterscheidbar; ohne Bus (g=0) exakt nie. → Beobachtungsgrenze ist
        dynamisch konvertierbar, keine feste Zustandseigenschaft."""
        out = dt.b5_time_conversion(T_GRID)
        assert out["with_bus"] > 1e-3
        assert out["no_bus"] < 1e-12

    def test_tomography_dimensions(self):
        """Voll (64→64, injektiv) gegen eingeschränkt (64→4, Kern 60)."""
        rank_full, rank_m, kdim_m = dt.b6_tomography_dimensions()
        assert rank_full == 64
        assert (rank_m, kdim_m) == (4, 60)


# ============================ Experiment C ==================================

class TestC_DirectComparison:
    def test_restricted_channel_fakes_reduction(self):
        """Ein M-only-Beobachter sieht NULL Dynamik (p konstant), während
        der Zustand real driftet (Fidelity < 1) — scheinbare Reduktion."""
        p0, p1, fid = dt.c_faking_demo()
        assert abs(p1 - p0) < 1e-12
        assert fid < 0.999

    def test_resources_registered(self):
        res = dt.c_distinguishing_resources()
        assert len(res) == 3

    def test_ssz_gr_ratio_still_2phi(self):
        """SSZ-skalar liefert keine unabhängige Vorhersage: 2φ, bereits
        ausgeschlossen (EXCLUDED_IN_MODEL) — im Audit unverändert."""
        ratio = dt.c_ssz_vs_gr_ratio()
        phi = (1 + 5 ** 0.5) / 2
        assert ratio == pytest.approx(2 * phi, rel=1e-6)


# ============================ Abschlussfrage ================================

class TestVerdict:
    def test_operational_separability_verdict(self):
        """Abschlussfrage: JA, operational unterscheidbar — aber nur MIT
        zusätzlicher Ressource (AB-Zugriff ODER kontrollierte Kopplung).
        Ohne jede Kopplung zwischen blindem Sektor und Kanal sind die
        Hypothesen für diesen Beobachter unbeobachtbar-äquivalent."""
        out = dt.b5_time_conversion(T_GRID)
        separable_with_resource = out["with_bus"] > 1e-3
        equivalent_without = out["no_bus"] < 1e-12
        assert separable_with_resource and equivalent_without
        # und H-RED ist im Modell gefallen (kein Constraint):
        cross, _ = dt.a4_no_constraint_restriction()
        assert cross > 0.1
