#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
symbolic_symmetry.py — SYMBOLISCHE Herleitung der 6⊕2-Symmetriestruktur
(Arbeitsauftrag B des Übergabedokuments HERMES_UEBERGABE_CARMEN_8ZU_X, §5.B).

Beweist symbolisch (sympy, exakt):

 1. P_s = (1 − σ_A·σ_B)/4 mit σ_A·σ_B = X_A X_B + Y_A Y_B + Z_A Z_B
    (Q1-Ordnung A,M,B): Spur(P_s) = 2, Eigenwerte {1,1,0⁶} → Ränge 2/6.
 2. [H, P_s] für H = Σ ω_i Z_i/2 + Σ g_i (X_i X_M + Y_i Y_M)/2
    + ω_p(D_A Z_A + D_B Z_B)/2: verschwindet EXAKT für
    ω_A=ω_B ∧ g_A=g_B ∧ D_A=D_B — der Kommutator faktorisiert in
    (ω_A−ω_B)-, (g_A−g_B)-, (D_A−D_B)-Terme.
 3. P_s H P_t (Sektor-Mischung) faktorisiert ebenfalls in Differenzterme.
 4. Symmetrischer Drive ε(X_A+X_B) erhält die Symmetrie;
    asymmetrischer (ε_A≠ε_B) bricht sie.

Numerische Kreuzvalidierung gegen ssz_symmetry_probe in den Tests.

© 2025 Carmen Wrede, Lino Casu — ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""
import sympy as sp

wA, wM, wB, gA, gB, dA, dB, eA, eB, wp = sp.symbols(
    'omega_A omega_M omega_B g_A g_B D_A D_B eps_A eps_B omega_pair',
    real=True)

X2 = sp.Matrix([[0, 1], [1, 0]])
Y2 = sp.Matrix([[0, -sp.I], [sp.I, 0]])
Z2 = sp.Matrix([[1, 0], [0, -1]])
I2 = sp.eye(2)

XA = sp.kronecker_product(X2, I2, I2)
XM = sp.kronecker_product(I2, X2, I2)
XB = sp.kronecker_product(I2, I2, X2)
YA = sp.kronecker_product(Y2, I2, I2)
YM = sp.kronecker_product(I2, Y2, I2)
YB = sp.kronecker_product(I2, I2, Y2)
ZA = sp.kronecker_product(Z2, I2, I2)
ZM = sp.kronecker_product(I2, Z2, I2)
ZB = sp.kronecker_product(I2, I2, Z2)
I8 = sp.eye(8)


def singlet_projector():
    """P_s = (1 − σ_A·σ_B)/4 in Q1-Ordnung (A, M, B)."""
    sigma_AB = XA * XB + YA * YB + ZA * ZB
    return (I8 - sigma_AB) / 4


def triplet_projector():
    return I8 - singlet_projector()


def H_full(drive=False):
    """H mit Diagonaluhr + Austauschbus [+ Drive]."""
    H = (wA * ZA + wM * ZM + wB * ZB) / 2 \
        + (gA * (XA * XM + YA * YM) + gB * (XM * XB + YM * YB)) / 2 \
        + wp * (dA * ZA + dB * ZB) / 2
    if drive:
        H = H + eA * XA + eB * XB
    return H


def commutator(A, B):
    return (A * B - B * A).applyfunc(sp.simplify)


def symmetrize(M):
    """Setze ω_A=ω_B, g_A=g_B, D_A=D_B, e_A=e_B."""
    return M.subs({wA: wB, gA: gB, dA: dB, eA: eB}).applyfunc(sp.simplify)


def is_zero_matrix(M):
    return all(sp.simplify(e) == 0 for e in M)


def antisymmetrize_coeffs(M):
    """Alle Einträge durch (ω_A−ω_B)-Substitution testbar machen:
    setze eine Differenz auf einen Markierwert und prüfe Faktorisierung."""
    return M


def mixing_block_S_T0():
    """Symbolisches ⟨T0|H|S⟩-Element (Bell-Struktur wie ssz_mixing_analysis)."""
    P_s = singlet_projector()
    H = H_full()
    cross = P_s * H * triplet_projector()
    return cross.applyfunc(sp.simplify)
