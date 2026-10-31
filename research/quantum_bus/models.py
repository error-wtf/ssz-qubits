#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
research/quantum_bus/models.py — Referenzmodelle Q0–Q3 (Phase 4).

STRIKT GETRENNTE Referenzmodelle; nichts davon geht in das produktive
`ssz_qubits.py`. Einheiten: ħ = 1 (Konvention dokumentiert); Frequenzen in
rad/s-Einheiten von ħ abhängig.

Q0: Kontrollsystem OHNE Bus — zwei/drei Qubits, H0 = Σ ω_i Z_i/2.
    Erwartung: rein lokale Z-Phasen erzeugen KEINE Verschränkung aus
    Produktzuständen.
Q1: Dreifach-Zweizustandsmodell (8×8): Qubits A, M, B mit
    H = Σ_i ω_i Z_i/2 + g_A(X_A X_M + Y_A Y_M)/2 + g_B(X_M X_B + Y_M Y_B)/2
    (hypothetisches Modell, klar gelabelt; Austausch-Kopplung).
Q2: Physischer Resonatorbus: Bus = harmonischer Oszillator (a, a†), Trunkierung
    n_max ⇒ Hilbertraumdimension 4(n_max+1). JC-artige Kopplung
    Σ_i g_i (σ_i^+ a + σ_i^− a†); dispersives Regime prüfbar.
Q3 (REDUZIERT, gelabelt): reiner Dephasing-Kanal als CPTP-Kraus-Map — KEINE
    vollständige Lindblad-Mastergleichung (offen; erst nach Q1/Q2-Validierung).

© 2025 Carmen Wrede, Lino Casu — ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""
import numpy as np
from scipy import linalg

# hbar = 1 throughout this package (documented convention).

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
SZ = np.array([[0, 1], [0, 0]], dtype=complex)   # sigma^+
SD = np.array([[0, 0], [1, 0]], dtype=complex)   # sigma^-


def kron_all(ops):
    out = np.array([[1.0 + 0j]])
    for op in ops:
        out = np.kron(out, op)
    return out


# ============================== Q0 ==========================================

def q0_hamiltonian(omegas):
    """H0 = sum_i (omega_i/2) Z_i — purely local."""
    n = len(omegas)
    H = np.zeros((2**n, 2**n), dtype=complex)
    for i, w in enumerate(omegas):
        ops = [I2] * n
        ops[i] = Z
        H += (w / 2.0) * kron_all(ops)
    return H


def propagate(H, t):
    """U(t) = exp(−i H t); prüft Hermitizität von H."""
    if np.max(np.abs(H - H.conj().T)) > 1e-12:
        raise ValueError("H ist nicht hermitesch")
    return linalg.expm(-1j * H * t)


# ============================== Q1 ==========================================

def q1_hamiltonian(omega_A, omega_M, omega_B, g_A, g_B):
    """8×8 Austausch-Busmodell (HYPOTHESE — kein SSZ-Claim)."""
    ZA, ZM, ZB = kron_all([Z, I2, I2]), kron_all([I2, Z, I2]), kron_all([I2, I2, Z])
    XAXM = kron_all([X, X, I2])
    YAYM = kron_all([Y, Y, I2])
    XMXB = kron_all([I2, X, X])
    YMYB = kron_all([I2, Y, Y])
    H = (omega_A / 2) * ZA + (omega_M / 2) * ZM + (omega_B / 2) * ZB
    H += (g_A / 2) * (XAXM + YAYM) + (g_B / 2) * (XMXB + YMYB)
    return H


def total_sz(n=3):
    ops = [I2] * n
    out = np.zeros((2**n, 2**n), dtype=complex)
    for i in range(n):
        ops = [I2] * n
        ops[i] = Z
        out += kron_all(ops)
    return out / 2.0


# ============================== Q2 ==========================================

def raise_op(n_max):
    d = np.zeros((n_max, n_max), dtype=complex)
    for k in range(1, n_max):
        d[k - 1, k] = np.sqrt(k)   # a|k> = sqrt(k)|k-1>  (column k)
    return d


def q2_hamiltonian(omega_A, omega_B, omega_r, g_A, g_B, n_max):
    """Resonatorbus: dim = 4(n_max+1). RWA-Kopplung g_i (s+ a + s− a†)."""
    na = n_max + 1
    a = raise_op(na)                       # a (annihilation)
    ad = a.conj().T
    Iq, Ir = I2, np.eye(na, dtype=complex)
    H = np.zeros((4 * na, 4 * na), dtype=complex)
    # qubit terms: (omega/2) Z, ordering (A, B, r)
    for idx, (w, zq) in enumerate([(omega_A, Z), (omega_B, Z)]):
        ops = [Iq, Iq, Ir]
        ops[idx] = zq
        H += (w / 2) * kron_all(ops)
    ops = [Iq, Iq, ad @ a]
    H += omega_r * kron_all(ops)
    # Kopplungen g_i (s+ a + s- a†), s = (X + iY)/2 = SZ
    for idx, g in ((0, g_A), (1, g_B)):
        sp_ = [Iq, Iq, Ir]
        sp_[idx] = SZ
        sm_ = [Iq, Iq, Ir]
        sm_[idx] = SD
        H += g * (kron_all(sp_) @ kron_all([Iq, Iq, a])
                  + kron_all(sm_) @ kron_all([Iq, Iq, ad]))
    return H


def total_excitation_q2(n_max):
    """N = Σ s+_i s−_i + a†a — conservation law of the RWA model."""
    na = n_max + 1
    N = np.zeros((4 * na, 4 * na), dtype=complex)
    for idx in (0, 1):
        sp_ = [I2, I2, np.eye(na, dtype=complex)]
        sp_[idx] = SZ
        sm_ = [I2, I2, np.eye(na, dtype=complex)]
        sm_[idx] = SD
        N += kron_all(sp_) @ kron_all(sm_)
    N += kron_all([I2, I2, raise_op(na).conj().T @ raise_op(na)])
    return N


# ============================== Q3 (reduziert) ==============================

def dephasing_channel(rho, p, qubit=0, n_qubits=2):
    """Reiner Dephasing-Kanal auf `qubit`: rho -> (1−p) rho + p Z rho Z.
    CPTP (Mischung zweier unitärer Kanäle)."""
    ops = [I2] * n_qubits
    ops[qubit] = Z
    Zfull = kron_all(ops)
    out = (1 - p) * rho + p * (Zfull @ rho @ Zfull)
    return out
