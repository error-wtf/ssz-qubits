#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ssz_symmetry_probe.py — Kann SSZ-Segmentierung eine nichttriviale Erhaltungs-
größe Q_SSZ mit [H, Q_SSZ] = 0 und Eigenräumen {6, 2} erzeugen?

Fragestellung (Carmen, 31.10.2026): Nicht weitere frei gewählte SSZ-Kopplungsterme,
sondern: lässt sich aus der SSZ-Mathematik ein Operator HERLEITEN, der mit dem
Bus-Hamiltonoperator kommutiert und dessen Eigenräume den 6⊕2-Zustandsraum
in invariante Sektoren zerlegen? Gelingt das, wäre 6⊕2 strukturell SSZ;
gelingt es nicht, bleibt die Zerlegung gewöhnliche Drehimpulsalgebra.

Methodik (alles ausführbar, nichts behauptet):
 1. INHALTSDEFINITION: Im vorliegenden Korpus besteht SSZ aus LOKALEN SKALAREN
    Zeitfaktoren D(r_i) (Repo: ssz_qubits; keine Mehr-Segment-Operatoren
    hergeleitet — Marolf-Constraint, AX-M3). Die dadurch erzeugbare
    Operatorfamilie ist DIAGONAL in der Z-Basis:
        Q(c) = c_A Z_A + c_M Z_M + c_B Z_B   (und Polynome davon).
 2. KOMMUTANTEN-ANALYSE: Der Raum aller X mit [H, X] = 0 wird exakt als
    Kernraum von vec([H, X]) = (I⊗H − Hᵀ⊗I)vec(X) berechnet. Für H mit 8
    verschiedenen Eigenwerten ist dim = 8 = {f(H)} — dann hat JEDES
    kommutierende Q die 8 eindimensionalen H-Eigenräume: KEINE {6,2}-Zerlegung
    möglich, gleichgültig wie Q gewählt wird.
 3. SSZ-SCAN: Existiert irgendeine D-Wahl (D_A, D_M, D_B), die den Austauschbus
    singulett-invariant macht (B₆₂ = 0)? Der Austauschterm X_A X_M + Y_A Y_M
    enthält kein D — der Scan muss negativ ausfallen; er wird über ein Gitter
    AUSGEFÜHRT, nicht nur behauptet.
 4. POSITIVKONTROLLEN: (a) Σ Z_i/2 kommutiert (Anregungszahl, Eigenräume 4+4,
    nicht 6+2); (b) für den PAAR-SYMMETRISchen Ising-Fall kommutiert der
    Singulett-Projektor P_S — das ist Drehimpulsalgebra, D-unabhängig.

ERGEBNIS (verifiziert in tests/…::TestSSZSymmetryProbe): NEGATIV.
Die Skalar-Segmentierung erzeugt keine nichttriviale Erhaltungsgröße; die
6⊕2-Zerlegung ist gewöhnliche Drehimpulsalgebra. Ein nichttriviales Q_SSZ
würde einen NICHT-skalaren Mehr-Segment-Operator erfordern, den kein
aktueller Korpus-Zweig herleitet (offen, gekoppelt an COMMON_ACTION_GAP).

© 2025 Carmen Wrede, Lino Casu — ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""
import itertools

import numpy as np

from .models import q1_hamiltonian, kron_all, Z, I2
from .reduction import bell_unitary

# Singulett-Projektor auf dem Paar (A,B):
# |S> = (|01> - |10>)/sqrt(2) in der Paarbasis |ab>, Index a*2+b
_V_S = np.array([0, 1, -1, 0], dtype=complex) / np.sqrt(2)
_P_S_PAIR = np.outer(_V_S, _V_S.conj())


def ssz_H(D_A, D_M, D_B, g_A, g_B, omega0=5.0, Delta=0.8):
    """Q1-Austauschbus mit SSZ-Zeitfaktoren: omega_i -> omega_i * D_i.
    D = 1 entspricht 'keine Segmentierung' (GR-/leerer Vergleich)."""
    return q1_hamiltonian(omega0 * D_A, (omega0 + Delta) * D_M,
                          omega0 * D_B, g_A, g_B)


def singlet_projector_full():
    """P_S = |S><S|_{AB} ⊗ I_M in der Q1-Ordnung (A, M, B), Index = a·4+m·2+b.

    |S> = (|a=0,b=1⟩ − |a=1,b=0⟩)/√2 ist in dieser Ordnung NICHT diagonal:
    pro M-Wert m verbindet P_S die Indizes (0,m,1) ↔ (1,m,0) mit ±1/2."""
    P = np.zeros((8, 8), dtype=complex)
    for m in range(2):
        i1 = 2 * m + 1      # |0, m, 1>
        i2 = 4 + 2 * m      # |1, m, 0>
        v = np.zeros(8, dtype=complex)
        v[i1] = 1 / np.sqrt(2)
        v[i2] = -1 / np.sqrt(2)
        P += np.outer(v, v.conj())
    return P


def commutant_dimension(H, tol=1e-9):
    """Dimension des Kommutanten {X: HX = XH} via Kernraum von (I⊗H − Hᵀ⊗I).

    Für H mit 8 verschiedenen Eigenwerten ist dim = 8 (= Polynome in H);
    Entartungen erhöhen die Dimension."""
    n = H.shape[0]
    M = np.kron(np.eye(n), H) - np.kron(H.T, np.eye(n))
    s = np.linalg.svd(M, compute_uv=False)
    return int(np.sum(s < tol * max(s[0], 1.0)))


def commutant_basis(H, tol=1e-9):
    """Orthonormierte Basis des Kommutanten (als 8×8-Matrizen)."""
    n = H.shape[0]
    M = np.kron(np.eye(n), H) - np.kron(H.T, np.eye(n))
    _, s, Vt = np.linalg.svd(M)
    r = int(np.sum(s < tol * max(s[0], 1.0)))
    basis = []
    for k in range(r):
        v = Vt[-1 - k, :].reshape(n, n)
        basis.append(v / np.linalg.norm(v))
    return basis


def singlet_sector_leakage(H):
    """‖P_S H (I−P_S)‖ — Kopplung des Singulett-Sektors heraus (0 = invariant)."""
    P = singlet_projector_full()
    Q = np.eye(8) - P
    return float(np.linalg.norm(P @ H @ Q))


def D_grid_scan(g_A=0.05, g_B=0.05, Delta=0.8, n=11):
    """Scan: Gibt es (D_A, D_M, D_B) mit singulett-invariantem Austauschbus?
    Rückgabe: (Minimales ‖P_S H (I−P_S)‖, Anzahl exakt-invarianter Punkte)."""
    grid = np.linspace(0.8, 1.2, n)
    best = np.inf
    n_inv = 0
    for dA, dM, dB in itertools.product(grid, grid, grid):
        H = ssz_H(dA, dM, dB, g_A, g_B, Delta=Delta)
        leak = singlet_sector_leakage(H)
        best = min(best, leak)
        if leak < 1e-12:
            n_inv += 1
    return best, n_inv


def commutator_norm(H, Q):
    return float(np.linalg.norm(H @ Q - Q @ H))


def total_sz():
    out = np.zeros((8, 8), dtype=complex)
    for i in range(3):
        ops = [I2, I2, I2]
        ops[i] = Z
        out += kron_all(ops)
    return out / 2.0
