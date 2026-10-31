#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ssz_mixing_analysis.py — Der D_A−D_B-Mischterm zwischen Singulett und Triplett
(Carmens Folgefrage, 31.10.2026).

Frage: Liefert der durch D_A−D_B verursachte Mischterm zwischen S- und
Triplett-Sektor eine unabhängig messbare Größe, die über gewöhnliche
relativistische Zeitdilatation hinausgeht?

Analyse (alles exakt verifizierbar):
 1. BLOCKSTRUKTUR: In der Bell-Basis (Paar A,B ⊗ M) koppelt die Diagonale
    Σ ω_i D_i Z_i/2 den Singulett |S> an |T0> mit Matrixelement
        m = (ω_A D_A − ω_B D_B)/2,
    während |T±> (|00>, |11>) NICHT gemischt werden (nur diagonal verschoben).
    ⇒ Der Mischterm ist genau die PAARWEISE DIFFERENZUHR, projiziert auf die
    Bell-Basis.
 2. DYNAMIK: |S>(0) entwickelt S↔T0-Rabi-Oszillation mit Frequenz |m|
    (Zweiniveau-Näherung gültig für |m| ≪ Abstand zu T±-Manifold).
 3. GR-VERGLEICH: Dieselbe Struktur mit D → D_GR = √(1−r_s/r). Das Verhältnis
    der Mischterme (kleine Höhendifferenz h) → dD_SSZ/dD_GR → 2φ ≈ 3.236.
    Das ist der ALLEINIGE SSZ-spezifische Inhalt — und genau dieser
    führende Koeffizient ist durch Cassini/LLR (γ=1 ⇒ Koeffizient 1/2)
    bereits ausgeschlossen.

URTEIL: Der Mischterm ist Bell-Basis-projizierte Zeitdilatation.
`NO_DISTINGUISHING_PREDICTION` wird präzisiert: die messbare Größe existiert,
ist aber (i) keine Bus-Observable (sie existiert ohne jeden Bus) und
(ii) ihr SSZ-Anteil ist der bereits falsifizierte 2φ-Koeffizient.
Route zu neuer Physik: nur nicht-scalare Kopplung (Task B).

© 2025 Carmen Wrede, Lino Casu — ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""
import numpy as np

from .models import kron_all, Z, I2
from .ssz_symmetry_probe import singlet_projector_full


def pairing_diagonal(D_A, D_B, omega_pair):
    """Der S↔T0-Mischterm: (omega_A D_A Z_A + omega_B D_B Z_B)/2 auf dem Paar,
    tensoriert mit I_M — in Q1-Ordnung (A, M, B)."""
    ZA = kron_all([Z, I2, I2])
    ZB = kron_all([I2, I2, Z])
    return omega_pair * (D_A * ZA + D_B * ZB) / 2.0


def mixing_element_S_T0(D_A, D_B, omega_pair):
    """<T0 m| H_pair |S m'> — exakt (omega_A D_A − omega_B D_B)/2, M-diagonal."""
    H = pairing_diagonal(D_A, D_B, omega_pair)
    P_S = singlet_projector_full()
    # |T0 m> in Q1-Ordnung: (|01> + |10>)/√2 ⊗ |m> — Indizes wie P_S-Konstruktion
    vals = []
    for m in range(2):
        iT0 = 2 * m + 0 if False else None
        # T0 = (|0,m,1> + |1,m,0>)/√2
        v_T0 = np.zeros(8, dtype=complex)
        v_T0[2 * m + 1] = 1 / np.sqrt(2)
        v_T0[4 + 2 * m] = 1 / np.sqrt(2)
        v_S = np.zeros(8, dtype=complex)
        v_S[2 * m + 1] = 1 / np.sqrt(2)
        v_S[4 + 2 * m] = -1 / np.sqrt(2)
        vals.append(np.vdot(v_T0, H @ v_S))
    return vals  # [m=0, m=1] — beide = (omega D_A − omega D_B)/2


def theoretical_mixing(D_A, D_B, omega_pair):
    return (omega_pair * D_A - omega_pair * D_B) / 2.0


def gr_mixing_ratio(x=1e8):
    """Verhältnis dD_SSZ/dx ÷ dD_GR/dx (Leading Order, auslöschungsfrei):
    D_SSZ = 1/(2−exp(−φ/x)) ⇒ dD/dx = exp(−φ/x)·φ/x²/(2−exp(−φ/x))²
    D_GR  = √(1−1/x)      ⇒ dD/dx = 1/(2x²·√(1−1/x))
    Grenzwert x→∞: 2φ ≈ 3.236."""
    phi = (1 + 5 ** 0.5) / 2
    f = np.exp(-phi / x)
    d_ssz = f * phi / x ** 2 / (2 - f) ** 2
    d_gr = 1 / (2 * x ** 2 * np.sqrt(1 - 1 / x))
    return float(d_ssz / d_gr)
