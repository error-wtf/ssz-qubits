#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
research/quantum_bus/bus_effective.py — Schur-Komplement & Schrieffer-Wolff.

Für H = [[H_LL, H_LH],[H_LH†, H_HH]] (Sektorzerlegung über Basisindizes):
  Eigenwertbedingung im Niederenergie-Sektor:  det(H_eff(E) − E·I) = 0 mit
      H_eff(E) = H_LL + H_LH (E·I − H_HH)⁻¹ H_HL        (exakt, E-abhängig)
  Statische Näherung um E₀ (Schrieffer-Wolff 2. Ordnung):
      H_sw ≈ H_LL + H_LH (E₀·I − H_HH)⁻¹ H_HL
  Fehlerordnung O(‖H_LH‖²/Δ) — bricht NAHE RESONANZ zusammen.

KEINE Physik-Aussage: dieses Modul eliminiert Hilfsfreiheitsgrade mathematisch;
„Elimination" ist keine Zustandsvernichtung (siehe DIMENSION_LEDGER.md D).

Für das Q1-Modell (Ordnung (A, M, B), Index = a·4+m·2+b) ist der
energetische Sektor-Split 4+4: niederenergetisch = {|a m=0 b>},
hoch = {|a m=1 b>} (M-Anregung ≈ +Δ).
"""
import numpy as np

LOW_INDICES_Q1 = [0, 1, 4, 5]   # |a, m=0, b>
HIGH_INDICES_Q1 = [2, 3, 6, 7]  # |a, m=1, b>


def sector_blocks(H, low_idx, high_idx):
    lo = np.asarray(low_idx)
    hi = np.asarray(high_idx)
    H_LL = H[np.ix_(lo, lo)]
    H_LH = H[np.ix_(lo, hi)]
    H_HH = H[np.ix_(hi, hi)]
    return H_LL, H_LH, H_HH


def H_eff_energy(H, E, low_idx, high_idx):
    """Energieabhängiges effektives Hamiltonian im Low-Sektor."""
    H_LL, H_LH, H_HH = sector_blocks(H, low_idx, high_idx)
    return H_LL + H_LH @ np.linalg.solve(E * np.eye(H_HH.shape[0]) - H_HH,
                                         H_LH.conj().T)


def schur_residual(H, E, low_idx, high_idx):
    """σ_min(H_eff(E) − E·I) — für einen exakten Eigenwert E im Low-Sektor ≈ 0."""
    Heff = H_eff_energy(H, E, low_idx, high_idx)
    return float(np.min(np.linalg.svdvals(Heff - E * np.eye(Heff.shape[0]))))


def schrieffer_wolff_static(H, E0, low_idx, high_idx):
    """Statische 2.-Ordnung-Näherung."""
    H_LL, H_LH, H_HH = sector_blocks(H, low_idx, high_idx)
    return H_LL + H_LH @ np.linalg.solve(E0 * np.eye(H_HH.shape[0]) - H_HH,
                                         H_LH.conj().T)


def low_sector_eigenpairs(H, low_idx, high_idx):
    """Exakte Eigenwerte mit überwiegendem Low-Sektor-Support (|⟨low|ψ⟩|² ≥ 0.99)."""
    lam, vecs = np.linalg.eigh(H)
    lo = np.asarray(low_idx)
    out = []
    for k in range(len(lam)):
        support = float(np.sum(np.abs(vecs[lo, k]) ** 2))
        if support >= 0.99:
            out.append(lam[k])
    return np.array(sorted(out))


def error_vs_detuning(g_list, Delta, omega_common=5.0):
    """Max-Fehler der statischen SW-Eigenwerte (Low-Sektor) als Funktion von g.

    Modell: Q1-Hamiltonian mit ω_A=ω_B=ω_common, ω_M=ω_common+Δ, Kopplung g
    an beiden Kanten. Nahe Resonanz (Δ→0) divergiert die Näherung —
    dokumentierter Ausfall der adiabatischen Elimination.
    """
    from .models import q1_hamiltonian
    out = []
    for g in g_list:
        H = q1_hamiltonian(omega_common, omega_common + Delta, omega_common, g, g)
        lam_low = low_sector_eigenpairs(H, LOW_INDICES_Q1, HIGH_INDICES_Q1)
        n_low = H[0, 0].shape[0] if False else len(LOW_INDICES_Q1)
        if len(lam_low) != n_low:
            # Sektorbegriff kollabiert: Eigenzustände mischen stark über die
            # 4+4-Grenze — die adiabatische Elimination ist hier SINNLOS.
            out.append((g, np.inf))
            continue
        E0 = float(lam_low.mean())
        try:
            Hsw = schrieffer_wolff_static(H, E0, LOW_INDICES_Q1, HIGH_INDICES_Q1)
            lam_sw = np.sort(np.linalg.eigvalsh(Hsw).real)
            err = float(np.max(np.abs(lam_sw - lam_low)))
        except np.linalg.LinAlgError:
            err = np.inf
        out.append((g, err))
    return out
