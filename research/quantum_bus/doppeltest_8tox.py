#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
doppeltest_8tox.py — DOPPELTEST 8→x: Freiheitsgradreduktion GEGEN
Beobachtungsgrenze (Auftrag von Lino/Carmen, 31.10.).

Zwei konkurrierende — zugleich zutreffend sein könnende — Hypothesen:
  H-RED:  Von acht Zustandsrichtungen sind nur 6 bzw. 2 physikalisch
          unabhängig/dynamisch zugänglich (echte Reduktion).
  H-OBS:  Alle acht existieren; ein Messkanal erfasst nur einen Teil der
          Information (Beobachtungsgrenze).

ENTSCHEIDENDE Schärfe (Auftrag): [H,P]=0 zeigt nur dynamische Invarianz,
KEINE physikalische Verbotenheit. Für H-RED wäre ein Constraint nötig
(Dirac: Operator C mit C|ψ⟩=0 auf allen zulässigen Zuständen), für H-OBS
genügt ein Paar ρ1≠ρ2 mit M(ρ1)=M(ρ2) plus ein unterscheidender zweiter Kanal.

Alle Funktionen sind rein modellbasiert (keine erfundenen SSZ-Kopplungen).
Status-Labels im Audit-Dokument: REDUCTION_VS_OBSERVABILITY_AUDIT.md.

© 2025 Carmen Wrede, Lino Casu — ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""
import numpy as np

from .models import kron_all, I2, Z, X
from .reduction import projectors_6_2
from .ssz_symmetry_probe import ssz_H, singlet_projector_full
from .ssz_mixing_analysis import gr_mixing_ratio
from .photon_channel_demo import rho_pair_state, _V_PHI, _V_OTHER

_TOL = 1e-10   # begründete Toleranz: Doppelpräzision, Einträge O(1)

# ---------------------------------------------------------------------------
# Experiment A — Physikalische Reduktion
# ---------------------------------------------------------------------------

def a2_projectors():
    """P6 (Rang 6) und P2 (Rang 2) der Singulett-Triplett-Zerlegung;
    P2 muss dem Q1-geordneten Singulett-Projektor entsprechen
    (Ordnungskonvention explizit geprüft — Pitfall: Bell- vs Q1-Masken)."""
    U, P6, P2 = projectors_6_2()
    P2_q1 = singlet_projector_full()
    assert np.allclose(P2, P2_q1, atol=_TOL), "Ordnungs-Mismatch P2 vs P_s!"
    assert np.allclose(P6 + P2, np.eye(8), atol=_TOL)
    return U, P6, P2


def a3_commutator_norms(D_A=1.0, D_B=1.05, g_A=0.05, g_B=0.05):
    """[H,P] nur als dynamische Invarianz lesbar: Spiegelsymmetrie → ~0,
    Differenzsegmentierung → ≠ 0."""
    U, P6, P2 = a2_projectors()
    H_sym = ssz_H(1.0, 1.0, 1.0, g_A, g_B)
    H_dif = ssz_H(D_A, 1.0, D_B, g_A, g_B)
    n_sym = max(np.linalg.norm(H_sym @ P6 - P6 @ H_sym),
                np.linalg.norm(H_sym @ P2 - P2 @ H_sym))
    n_dif = max(np.linalg.norm(H_dif @ P6 - P6 @ H_dif),
                np.linalg.norm(H_dif @ P2 - P2 @ H_dif))
    return float(n_sym), float(n_dif)


def a4_no_constraint_restriction():
    """Gibt es eine physikalische Beschränkung auf einen Unterraum?
    Superselection-Test: wäre P6 (oder P2) 'physikalisch verboten-frei',
    dürfte KEINE zulässige Operation die Sektoren verbinden. Lokale
    Pauli-Operationen tun es aber (Norm > 0) — also kein Constraint."""
    U, P6, P2 = a2_projectors()
    XA = kron_all([X, I2, I2])
    cross = float(np.linalg.norm(P2 @ XA @ P6))
    # vollrangiger zulässiger Zustand existiert (kein Ausschluss von Richtungen):
    rho_full = np.linalg.matrix_power(
        np.eye(8) / 8 + 0.01 * kron_all([Z, I2, I2]), 2)  # positiv definit
    rho_full = rho_full / np.trace(rho_full)
    ev = np.linalg.eigvalsh(rho_full)
    return cross, bool(ev.min() > 0)


def a5_leakage_from_P6(t_grid, D_A=1.0, D_B=1.05, g_A=0.05, g_B=0.05):
    """Dynamisches Leakage: Start im P6-Sektor (|T0 m=0⟩), P2-Population
    über die Zeit. Spiegelsymmetrie → 0; Differenzsegmentierung → > 0
    (getrieben GENAU durch den SSZ-Differenzuhr-Mischterm)."""
    from .models import propagate
    v0 = np.zeros(8, dtype=complex)
    v0[1] = 1 / np.sqrt(2)
    v0[4] = 1 / np.sqrt(2)          # |T0 m=0⟩ — reiner P6-Zustand
    U, P6, P2 = a2_projectors()
    assert abs(np.vdot(v0, P2 @ v0)) < _TOL, "Startzustand nicht in P6?!"
    out = {}
    for label, H in (("mirror", ssz_H(1.0, 1.0, 1.0, g_A, g_B)),
                     ("differential", ssz_H(D_A, 1.0, D_B, g_A, g_B))):
        p2_max = 0.0
        for t in t_grid:
            psi = propagate(H, t) @ v0
            p2_max = max(p2_max, float(np.real(np.vdot(psi, P2 @ psi))))
        out[label] = p2_max
    return out


def a6_four_way_classification():
    """Strikte Trennung: Eichredundanz / energetische Unterdrückung /
    dynamische Invarianz / physikalisch unzulässige Zustände — mit Beleg."""
    cross, _ = a4_no_constraint_restriction()
    n_sym, n_dif = a3_commutator_norms()
    return {
        "gauge_redundancy": ("none", "kein Constraint-Operator ableitbar; "
                             "lokal-Pauli verbindet Sektoren (Norm %.3e)" % cross),
        "energetic_suppression": ("partial_only",
                                  "Detuning verschiebt Energien, aber Population "
                                  "kehrt oszillierend zurück — kein Entfernen"),
        "dynamical_invariance": ("mirror_symmetric_only",
                                 "[H,P]=0 bei ω_A=ω_B ∧ g_A=g_B ∧ D_A=D_B "
                                 "(‖[H,P]‖_sym=%.2e, _dif=%.2e)" % (n_sym, n_dif)),
        "physically_forbidden_states": ("none",
                                        "vollrangige ρ zulässig; lokale Unitare "
                                        "erreichen alle 8 Richtungen"),
    }


# ---------------------------------------------------------------------------
# Experiment B — Eingeschränkte Beobachtbarkeit
# ---------------------------------------------------------------------------

def _herm_basis(n=8):
    """Orthonormalbasis des reellen Raums Herm(n) (dim n²)."""
    basis = []
    for j in range(n):
        E = np.zeros((n, n), dtype=complex)
        E[j, j] = 1.0
        basis.append(E.copy())
    for j in range(n):
        for k in range(j + 1, n):
            E = np.zeros((n, n), dtype=complex)
            E[j, k] = 1 / np.sqrt(2)
            E[k, j] = 1 / np.sqrt(2)
            basis.append(E.copy())
            E2 = np.zeros((n, n), dtype=complex)
            E2[j, k] = 1j / np.sqrt(2)
            E2[k, j] = -1j / np.sqrt(2)
            basis.append(E2.copy())
    return basis


def b4_observation_map_rank(effects):
    """Rang/Kern der linearen Beobachtungsabbildung L: Herm(8)→R^k,
    X ↦ (Tr E_i X)_i. Rückgabe: (rank, kernel_dim, kernel_basis)."""
    B = _herm_basis()
    L = np.array([[np.real(np.trace(E @ X)) for X in B] for E in effects])
    s = np.linalg.svd(L, compute_uv=False)
    tol = max(s[0], 1.0) * 1e-12        # begründet: Maschineneps × Skala
    rank = int(np.sum(s > tol))
    # Kernbasis:
    _, _, Vt = np.linalg.svd(L)
    kernel = [sum(Vt[-(i + 1), j] * B[j] for j in range(64))
              for i in range(64 - rank)]
    for K in kernel:
        for E in effects:
            assert abs(np.real(np.trace(E @ K))) < 1e-8
    return rank, 64 - rank, kernel


def b4_channel_quantities():
    """Kennzahlen des M-Kanals: 2-Outcomes → linearer Rang 2, Kern 62;
    Beobachtungs-Algebra {I_AB⊗A_M}: reelle Dimension 4."""
    E0 = kron_all([I2, np.diag([1.0, 0.0]), I2])
    E1 = kron_all([I2, np.diag([0.0, 1.0]), I2])
    rank, kdim, _ = b4_observation_map_rank([E0, E1])
    alg = [kron_all([I2, M, I2]) for M in
           (np.eye(2), np.array([[0, 1], [1, 0]], dtype=complex),
            np.array([[0, -1j], [1j, 0]], dtype=complex), np.diag([1, -1]))]
    return rank, kdim, 4, alg


def b2_indistinguishable_family(n=5):
    """Kontinuierliche Familie ρ_λ = (1−λ)ρ₁ + λρ₂, ρ₁≠ρ₂, alle mit
    IDENTISCHER Kanalstatistik (beide haben σ_M = |0⟩⟨0|)."""
    r1, _ = rho_pair_state(_V_PHI)
    r2, _ = rho_pair_state(_V_OTHER)
    fam = []
    for lam in np.linspace(0, 1, n):
        rho = (1 - lam) * r1 + lam * r2
        assert np.linalg.eigvalsh(rho).min() > -1e-12   # zulässig
        fam.append(rho)
    return fam


def b3_supplementary_channel(fam):
    """Zweiter, zulässiger Kanal (Bell-Projektor auf AB ⊗ I_M), der die
    Familie unterscheidet. Positivität + Vollständigkeit geprüft."""
    Bell = np.array([1, 0, 0, 1], dtype=complex) / np.sqrt(2)
    Phi = np.kron(Bell, np.array([1, 0], dtype=complex))
    # Ordnung (A,B,M) → in Q1 (A,M,B) platzieren:
    Phi8 = np.zeros(8, dtype=complex)
    for a in range(2):
        for b in range(2):
            Phi8[4 * a + b] = Phi[2 * a + b]        # m = 0
    P = np.outer(Phi8, Phi8.conj())
    E0, E1 = P, np.eye(8) - P
    assert np.linalg.eigvalsh(E0).min() > -1e-12
    assert np.linalg.eigvalsh(E1).min() > -1e-12
    assert np.allclose(E0 + E1, np.eye(8))
    return [float(np.real(np.trace(E0 @ rho))) for rho in fam]


def b5_time_conversion(t_grid, g=0.05):
    """Werden initially-indistinguishable Zustände später unterscheidbar?
    ρ_a = ½(|S m0⟩⟨| + |T− m0⟩⟨|), ρ_b = ½(|S m0⟩⟨| + |T+ m0⟩⟨|):
    gleiche M-Reduktion (beide |0⟩⟨0|), verschiedene T-Komponenten.
    g≠0: Trennung wächst; g=0 (kein Bus): Trennung exakt 0 ∀t."""
    def mk(tcomp):
        psi = np.zeros(8, dtype=complex)
        psi[1] = 1 / np.sqrt(2)                      # S-Anteil (|0,0,1⟩)
        if tcomp == "Tm":
            psi[5] = np.sqrt(0.5)                    # |1,0,1⟩
        else:
            psi[0] = np.sqrt(0.5)                    # |0,0,0⟩
        return np.outer(psi, psi.conj())
    from .models import propagate
    E1 = kron_all([I2, np.diag([0.0, 1.0]), I2])
    out = {}
    for label, gg in (("with_bus", g), ("no_bus", 0.0)):
        Ha = ssz_H(1.0, 1.0, 1.0, gg, gg)
        ra, rb = mk("Tm"), mk("Tp")
        # gleiche M-Reduktion ⇒ identische Statistik bei t=0 (beide Richtungen
        # der Faktorisierung sind separat testfixiert; hier der Spezialfall):
        p_a0 = float(np.real(np.trace(E1 @ ra)))
        p_b0 = float(np.real(np.trace(E1 @ rb)))
        assert abs(p_a0 - p_b0) < 1e-14
        sep = 0.0
        for t in t_grid:
            U = propagate(Ha, t)
            pa = np.real(np.trace(E1 @ (U @ ra @ U.conj().T)))
            pb = np.real(np.trace(E1 @ (U @ rb @ U.conj().T)))
            sep = max(sep, abs(pa - pb))
        out[label] = float(sep)
    return out


def b6_tomography_dimensions(seed=7):
    """Vollständige Tomographie (64 IC-Effekte → Rang 64 = injektiv auf
    Herm(8)) gegen eingeschränkte Kanal-Tomographie (IC auf M → Rang 4,
    Kern 60: der AB-Anteil ist irreversibel verloren)."""
    rng = np.random.default_rng(seed)
    effects_full = []
    for _ in range(64):
        v = rng.normal(size=8) + 1j * rng.normal(size=8)
        v /= np.linalg.norm(v)
        effects_full.append(np.outer(v, v.conj()))
    rank_full, _, _ = b4_observation_map_rank(effects_full)
    # IC-M-Kanal: Effekte I_AB ⊗ P_k, P_k = |0>,|1>,|+>,|+i⟩-Projektoren
    P = {"0": np.diag([1.0, 0]), "1": np.diag([0, 1.0]),
         "+": np.array([[0.5, 0.5], [0.5, 0.5]]),
         "+i": np.array([[0.5, -0.5j], [0.5j, 0.5]])}
    effects_m = [kron_all([I2, p, I2]) for p in P.values()]
    rank_m, kdim_m, _ = b4_observation_map_rank(effects_m)
    return rank_full, rank_m, kdim_m


# ---------------------------------------------------------------------------
# Experiment C — Direkter Vergleich
# ---------------------------------------------------------------------------

def c_faking_demo(t=1.0, wa=5.0, wm=5.8, wb=5.0):
    """Kann ein eingeschränkter Kanal echte Dynamik verbergen? Bei g=0 ist
    die M-Statistik KONSTANT (beobachtete Dynamik: null), während der
    volle Zustand driftet (Fidelity < 1) — die Reduktion ist scheinbar."""
    from .models import q0_hamiltonian, propagate
    psi0 = np.zeros(8, dtype=complex)
    psi0[0] = 1 / np.sqrt(2)
    psi0[1] = 1 / np.sqrt(2)          # Überlagerung N=0 / N=1
    H = q0_hamiltonian([wa, wm, wb])
    E1 = kron_all([I2, np.diag([0.0, 1.0]), I2])
    U = propagate(H, t)
    psi_t = U @ psi0
    p0 = float(np.real(np.trace(E1 @ np.outer(psi0, psi0.conj()))))
    p1 = float(np.real(np.trace(E1 @ np.outer(psi_t, psi_t.conj()))))
    fid = float(abs(np.vdot(psi0, psi_t)) ** 2)
    return p0, p1, fid                # p0≈p1 (Kanal blind), fid<1 (echte Dynamik)


def c_distinguishing_resources():
    """Pro Fall: welche zusätzliche Ressource unterscheidet die Beschreibungen?"""
    return {
        "blind_pair": "Zusatzkanal mit AB-Zugriff (b3) ODER kontrollierte "
                      "Kopplung g≠0 (b5): beide konvertieren Blindheit in Signal",
        "invariant_sector": "Differenzsegmentierung D_A≠D_B bricht die "
                            "Invarianz (a5) — die SSZ-Differenzuhr ist selbst "
                            "die Ressource (aber 2φ-falsifiziert, s. u.)",
        "full_space": "tomographisch vollständiger Effektsatz (b6): 64 von 64",
    }


def c_ssz_vs_gr_ratio():
    """SSZ/GR-Fernfeldkoeffizient der Mischterme — 2φ, bereits
    ausgeschlossen (EXCLUDED_IN_MODEL). Hier nur als Audit-Referenz."""
    return gr_mixing_ratio()
