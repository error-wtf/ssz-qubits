#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
photon_channel_demo.py — Arbeitsauftrag D: Können nur-photonische Messkanäle
scheinbar reduzierte Dimensionalität vortäuschen? (Carmens Impuls
„Wir sind Photonenleute", 30.10.)

Demonstriert an C²⊗C²⊗C² (A, M, B), Detektor koppelt NUR an M:

 1. DETEKTORALGEBRA: Effekte Π_m ⊗ I_AB erzeugen eine Algebra mit Rang 2 —
    der Kanal „sieht" 2 von 8 Dimensionen.
 2. BLINDHEIT: Zwei Zustände, die sich NUR im Paar (A,B) unterscheiden,
    liefern für ALLE M-Effekte identische Statistiken, haben aber
    Fidelity < 1 — sie sind physikalisch verschieden und für diesen Kanal
    ununterscheidbar.
 3. OFFENES SYSTEM (Photonverlust L = |0><1|_M): M bleibt im dunklen |0>,
    Emission ≤ 1e-16 — Zustände im (A,B)-Sektor emittieren nie und bleiben
    unsichtbar; scheinbare „2 weggefallene Freiheitsgrade" sind eine Aussage
    über den MESSKANAL, nicht über den Zustandsraum.

STATUS-LABELS (§6): PROVEN_IN_MODEL (als Demonstration von Messblindheit).
AUSDRÜCKLICH KEINE Ontologie: aus Unsichtbarkeit folgt weder Nichtexistenz
(Kern der Demo) noch Existenz verborgener Dimensionen (Rückrichtung bleibt
Hypothese und braucht unabhängige Kopplungsnachweise).

© 2025 Carmen Wrede, Lino Casu — ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""
import numpy as np

from .models import kron_all, I2, Z
from .reduction import partial_trace

# |Φ+>_{AB} und ein davon verschiedener Paarzustand (|00>: Produkt, <Z_A>=1):
_V_PHI = np.array([1, 0, 0, 1], dtype=complex) / np.sqrt(2)
_V_OTHER = np.array([1, 0, 0, 0], dtype=complex)


def rho_pair_state(vec_pair):
    """ρ = |pair><pair|_{AB} ⊗ |0><0|_M in Q1-Ordnung (A, M, B):
    Amplituden wohnen auf idx = a·4 + m·2 + b mit m = 0."""
    psi = np.zeros(8, dtype=complex)
    for a in range(2):
        for b in range(2):
            psi[4 * a + b] = vec_pair[2 * a + b]   # m = 0
    return np.outer(psi, psi.conj()), psi


def m_only_statistics(rho):
    """Alle Messstatistiken, die ein nur-photonischer M-Kanal erhalten kann:
    der reduzierte M-Dichteoperator."""
    return partial_trace(rho, keep=[1], dims=[2, 2, 2])


def ab_probe_statistics(rho):
    """Negativkontroll-Kanal: Detektor mit Zugriff auf A (z.B. σ_z^A)."""
    ZA = kron_all([Z, I2, I2])
    return float(np.real(np.trace(ZA @ rho)))


def photon_loss_channel(rho, rate=1.0, n_steps=200, dt=0.01):
    """Amplitudendämpfung auf M (L = |0><1|_M), forderside: ρ ← ρ + dt·LρL†
    − dt/2·{L†L, ρ} (Euler, klein genug für Demo-Genauigkeit)."""
    L = np.zeros((8, 8), dtype=complex)
    L[0, 2] = 1.0   # |0>_M <1|_M in Q1-Ordnung: idx2 = |0,m=1,0> → idx0 = |0,m=0,0>
    L[1, 3] = 1.0   # +b-Anteil
    L[4, 6] = 1.0
    L[5, 7] = 1.0
    Ldag = L.conj().T
    out = rho.copy()
    for _ in range(n_steps):
        out = out + dt * rate * (L @ out @ Ldag) \
            - dt * rate / 2 * (Ldag @ L @ out + out @ Ldag @ L)
    return out


def emission_probability(rho):
    """P(Photon emittiert) = Tr(L†L ρ) = Tr(ρ · P_{m=1})."""
    P_m1 = kron_all([I2, np.diag([0, 1]), I2])
    return float(np.real(np.trace(P_m1 @ rho)))
