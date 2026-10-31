#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
demo_bus.py — minimales, reproduzierbares Beispiel (Phase 4, Gate 4).

Zeigt an Modell Q1 (Austauschbus, HYPOTHESE):
  1. Dynamik: Anregungsaustausch A↔M↔B (Erhaltungsgröße ΣZ bleibt konstant),
  2. exakte Eigenwerte vs. statische Schrieffer-Wolff-Näherung als Funktion
     von g/Δ (Fehlerordnung g²/Δ; Versagen nahe Resonanz),
  3. Bell-Fidelity GETRENNT von Concurrence/CHSH für ein Bell-Paar unter
     lokalem Phasen-Bias (kein Bus — nur Uhrenvergleich).
Erzeugt research/quantum_bus/plots/bus_demo.png (beschriftet).

Aufruf: python research/quantum_bus/demo_bus.py
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from research.quantum_bus import models as mb          # noqa: E402
from research.quantum_bus import reduction as rd       # noqa: E402
from research.quantum_bus import bus_effective as be   # noqa: E402


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    outdir = Path(__file__).resolve().parent / "plots"
    outdir.mkdir(exist_ok=True)

    print("=" * 70)
    print("Quantum-Bus-Referenzmodelle — Demo (Q1, Hypothese; kein SSZ-Claim)")
    print("=" * 70)

    # --- 1) Dynamik: Austausch A ↔ M bei g_B = 0, resonant ------------------
    w, g = 5.0, 0.5
    H = mb.q1_hamiltonian(w, w, w, g, 0.0)
    psi0 = np.zeros(8, dtype=complex)
    psi0[0b100] = 1.0                      # |A=1, M=0, B=0>
    ts = np.linspace(0, 2 * np.pi / g, 200)
    pA = [abs((mb.propagate(H, t) @ psi0)[0b100]) ** 2 for t in ts]
    pB = [abs((mb.propagate(H, t) @ psi0)[0b001]) ** 2 for t in ts]
    pM = [abs((mb.propagate(H, t) @ psi0)[0b010]) ** 2 for t in ts]

    # Erhaltungsgröße
    N = mb.total_sz(3)
    drift = max(abs(np.vdot(mb.propagate(H, t) @ psi0, N @ (mb.propagate(H, t) @ psi0)).real
                    - np.vdot(psi0, N @ psi0).real) for t in ts)
    print(f"[1] ΣZ-Drift über {len(ts)} Zeiten: {drift:.2e} (Erhaltungsgröße)")

    # --- 2) exakt vs. statische SW-Näherung ---------------------------------
    g_list = [0.01, 0.02, 0.04, 0.08, 0.16]
    res = be.error_vs_detuning(g_list, Delta=0.8)
    print("[2] statische SW-Fehler vs g (Δ=0.8):")
    for gval, err in res:
        print(f"      g={gval:5.2f}  max|λ_SW−λ_exact| = {err:.3e}")
    res_res = be.error_vs_detuning([0.05, 0.2], Delta=1e-9)
    print(f"    nahe Resonanz (Δ=1e-9): {res_res}  → Elimination versagt")

    # --- 3) Fidelity vs. Verschränkung (getrennt!) --------------------------
    theta = 0.3
    psi = np.array([1, 0, 0, np.exp(-1j * theta)]) / np.sqrt(2)
    target = np.array([1, 0, 0, 1]) / np.sqrt(2)
    rho = np.outer(psi, psi.conj())
    print(f"[3] Bell-Fidelity |<Φ+|ψ>|² = {rd.bell_fidelity(psi, target):.6f} "
          f"(= cos²(θ/2))  vs. Concurrence = {rd.concurrence(rho):.6f} (= 1)")
    print(f"    CHSH max = {rd.chsh_max(rho):.6f} (= 2√2, unverändert durch lokale Phase)")

    # --- Plot ----------------------------------------------------------------
    fig, axs = plt.subplots(1, 2, figsize=(10, 4))
    axs[0].plot(ts, pA, label="P(A=1)")
    axs[0].plot(ts, pM, label="P(M=1)")
    axs[0].plot(ts, pB, label="P(B=1)")
    axs[0].set_xlabel("t")
    axs[0].set_ylabel("Besetzung")
    axs[0].set_title(f"Q1-Austausch A↔M (g={g}, resonant) — HYPOTHESE")
    axs[0].legend()
    axs[1].semilogy([g for g, _ in res], [e for _, e in res], "o-")
    axs[1].set_xlabel("g")
    axs[1].set_ylabel("max |λ_SW − λ_exact|")
    axs[1].set_title("statische SW-Näherung, Δ=0.8 (Versagen nahe Resonanz)")
    fig.tight_layout()
    fig.savefig(outdir / "bus_demo.png", dpi=120)
    print(f"\nPlot geschrieben: {outdir / 'bus_demo.png'}")
    print("\nHINWEIS: Dies sind Referenzmodelle. Es ist KEIN SSZ-spezifischer")
    print("Bus-Effekt nachgewiesen; siehe docs/research/SSZ_VS_GR_BUS_PREDICTIONS.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
