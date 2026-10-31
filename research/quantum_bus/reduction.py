#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
research/quantum_bus/reduction.py — 6⊕2-Basiswechsel, Projektionen, Metriken.

Explizite 6⊕2-Darstellung (Auftrag §5.1): Spinpaar (A,B) in Bell-Basis
(|T+>=|00>, |T0>=(|01>+|10>)/√2, |T−>=|11>, |S>=(|01>−|10>)/√2), tensoriert mit
Qubit M ⇒ 8D; Umordnung auf Blockstruktur [Triplett⊗M (6) | Singulett⊗M (2)].

Vorzeichen-/Ordnungskonvention wird in bell_unitary() exakt dokumentiert und
durch Tests gegen die erzeugenden Zustände geprüft.

Metriken (Auftrag §5.3/§5.4): Rang, Unitarität, Leakage Tr(P_excl ρ), Spur,
von-Neumann-Entropie des reduzierten Zustands, Bell-Fidelity
|<ψ_target|ψ(t)>|² GETRENNT von Verschränkung (Concurrence), CHSH
(feste Achsen vs. maximiert).

© 2025 Carmen Wrede, Lino Casu — ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""
import itertools
import numpy as np

I2 = np.eye(2, dtype=complex)


def kron_all(ops):
    out = np.array([[1.0 + 0j]])
    for op in ops:
        out = np.kron(out, op)
    return out


# Qubit-Ordnung: (A, B, M)  → Basisindex |abm> = a·4 + b·2 + m  (a,b,m ∈ {0,1})

def bell_unitary():
    """U mit (U⊗Order) |abm>-Basis → geordnete Basis [T+M, T0M, T−M, SM] (6)
    gefolgt von [S m=0, S m=1] (2).

    Konkret: erst Bell-Transformation auf (A,B): 
      |00> → |T+>, |11> → |T−>, (|01>+|10>)/√2 → |T0>, (|01>−|10>)/√2 → |S>.
    Dann Permutation der 8 Basisvektoren auf die Reihenfolge
    [T+0,T+1,T00,T01,T−0,T−1, S0,S1] (m = M-Zustand).
    """
    # Bell-Transformationsmatrix B mit B|ab> = Bell-Zustand:
    # Spalten = Bilder von |00>,|01>,|10>,|11> in der Basis (T+,T0,T−,S):
    # |00> → T+ ; |01> → (T0+S)/√2 ; |10> → (T0−S)/√2 ; |11> → T−
    B = np.array([
        [1, 0,          0,         0],
        [0, 1/np.sqrt(2), 1/np.sqrt(2), 0],
        [0, 0,          0,         1],
        [0, 1/np.sqrt(2), -1/np.sqrt(2), 0],
    ], dtype=complex)
    U_full = np.kron(B, I2)   # auf (A,B) ⊗ M, Basis |abm>
    # Permutation: aktuelle Ordnung (Bell-Index b ∈ 0..3 [T+,T0,T−,S]) × m:
    # Zielreihenfolge: [b=0,1,2 (Triplett) mit m=0,1] + [b=3 (S) mit m=0,1]
    perm_src = [0 * 2 + 0, 0 * 2 + 1, 1 * 2 + 0, 1 * 2 + 1,
                2 * 2 + 0, 2 * 2 + 1, 3 * 2 + 0, 3 * 2 + 1]
    U = U_full[perm_src, :]     # Zeilen umordnen = Zielbasis
    return U


def projectors_6_2():
    U = bell_unitary()
    P6 = U.conj().T @ np.diag([1] * 6 + [0] * 2) @ U
    P2 = U.conj().T @ np.diag([0] * 6 + [1] * 2) @ U
    return U, P6, P2


def block_decompose(H):
    """Gibt (U, A6, B62, C2) mit U H U† = [[A6, B62],[B62†, C2]] in der
    geordneten 6⊕2-Basis (Zeilen/Spalten 0..5 = Triplett⊗M, 6..7 = S⊗M)."""
    U = bell_unitary()
    Hp = U @ H @ U.conj().T
    A6 = Hp[:6, :6]
    B62 = Hp[:6, 6:]
    C2 = Hp[6:, 6:]
    return U, A6, B62, C2


# ----------------------------- Metriken -------------------------------------

def von_neumann_entropy(rho, keep, dims):
    """Von-Neumann-Entropie (nats) des reduzierten Zustands über `keep`."""
    r = partial_trace(rho, keep, dims)
    evals = np.linalg.eigvalsh(r)
    evals = evals[evals > 1e-15]
    return float(-np.sum(evals * np.log(evals)))


def partial_trace(rho, keep, dims):
    """Partialtrace; rho hat Shape (prod(dims), prod(dims)); `keep` = Indizes."""
    keep = sorted(keep)
    n = len(dims)
    traced = [i for i in range(n) if i not in keep]
    keep_dims = [dims[i] for i in keep]
    traced_dims = [dims[i] for i in traced]
    dk = int(np.prod(keep_dims)) if keep_dims else 1
    dt = int(np.prod(traced_dims)) if traced_dims else 1
    # Anordnung: (keep-Systeme, getracete Systeme) je Ket- und Bra-Seite
    ax = keep + traced + [n + i for i in keep] + [n + i for i in traced]
    t = np.transpose(rho.reshape(dims + dims), ax)
    t = t.reshape(dk, dt, dk, dt)
    return np.einsum('ajbj->ab', t)


def concurrence(rho2):
    """Wootters-Concurrence für 2-Qubit-Dichteoperator (Basis |00>,|01>,|10>,|11>)."""
    Y = np.array([[0, 0, 0, -1], [0, 0, 1, 0], [0, 1, 0, 0], [-1, 0, 0, 0]], dtype=complex)
    # Standard: rho_tilde = (sigma_y ⊗ sigma_y) · rho* · (sigma_y ⊗ sigma_y)
    rho_tilde = Y @ rho2.conj() @ Y.conj().T
    evals = np.linalg.eigvals(rho2 @ rho_tilde)
    evals = np.sort(np.sqrt(np.clip(np.abs(evals), 0, None)))[::-1]
    return float(max(0.0, evals[0] - evals[1] - evals[2] - evals[3]))


def bell_fidelity(psi, target):
    """|<target|psi>|² — SCHARF getrennt von Verschränkungsmaßen."""
    return float(abs(np.vdot(target, psi)) ** 2)


def leakage(rho, P_excluded):
    """Tr(P_excluded ρ) — Wahrscheinlichkeit außerhalb des geschützten Raums."""
    return float(np.trace(P_excluded @ rho).real)


def chsh_fixed(rho2, axes):
    """CHSH mit FESTGEHALTENEN Messachsen: S = |E(a,b)+E(a,b')+E(a',b)−E(a',b')|,
    E(a,b) = aᵀ T b, T_ij = Tr(ρ σ_i⊗σ_j)."""
    T = correlation_matrix(rho2)
    a, a2, b, b2 = axes

    def E(av, bv):
        return float(av @ T @ bv)

    return abs(E(a, b) + E(a, b2) + E(a2, b) - E(a2, b2))


def chsh_max(rho2):
    """Maximales CHSH über ALLE lokalen Messachsen — exakt via Horodecki:
    S_max = 2·sqrt(u1 + u2), u1 ≥ u2 = zwei größte Eigenwerte von TᵀT.
    (Horodetski/Quantum-Information-Standardergebnis; ersetzt einen Gitter-Scan,
    der gedrehte Optimalachsen in nicht-x-z-Ebenen verpassen würde.)"""
    T = correlation_matrix(rho2)
    u = np.linalg.eigvalsh(T.T @ T)[::-1]
    return 2.0 * np.sqrt(max(0.0, u[0] + u[1]))


def correlation_matrix(rho2):
    return np.array([[np.trace(rho2 @ np.kron(PAULI[i], PAULI[j])).real
                      for j in range(3)] for i in range(3)])


PAULI = [np.array([[0, 1], [1, 0]], dtype=complex),
         np.array([[0, -1j], [1j, 0]], dtype=complex),
         np.array([[1, 0], [0, -1]], dtype=complex)]
