#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
metric_invariants.py — Krümmungsinvarianten für D²-Metriken (audit R5).

Zweck: Die Behauptung „D>0 ⇒ Regularität/keine Singularität" ist UNBEWIESEN.
Dieses Skript berechnet aus einem VOLLSTÄNDIGEN metrischen Ansatz

    ds² = −D(r)² c² dt² + D(r)^(-2) dr² + r² dΩ²      (statisch, kugelsymmetrisch)

die Ricci-Skalar R und den Kretschmann-Skalar K = R_abcd R^abcd SYMBOLISCH
(sympy) und wertet sie aus. Kontrollen:

  1. D ≡ 1                          → R = 0, K = 0 (flach)
  2. D² = 1 − r_s/r (Schwarzschild) → K = 12 r_s²/r⁶ EXAKT (Literatur-Orakel;
     divergence bei r=0; am Horizont r=r_s ENDLICH — dort ist die Singularität
     der Schwarzschild-Koordinaten ein Koordinatenartefakt, Martel & Poisson,
     arXiv:gr-qc/0001069)

Status: Referenzrechnung. KEINE Behauptung, dass SSZ-Metriken singularity-frei
sind; für die im Repo verwendeten D-Profile (Ansatz A/B) werden die Invarianten
am Ende ausgewertet — das ZENTRUM (r→0) ist für beide a priori offen, denn
D>0 allein sagt nichts über Krümmung.

Aufruf: python scripts/metric_invariants.py
© 2025 Carmen Wrede, Lino Casu — ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""
import sys
from pathlib import Path

import sympy as sp

R_COORD, RS_SYM, C_SYM = sp.symbols('r r_s c', positive=True)
THETA = sp.symbols('theta', positive=True)


def _metric_functions(D_expr):
    """g_mun for ds² = −D² c² dt² + D^(-2) dr² + r²dΩ² (signature −+++, coords t,r,θ,φ)."""
    Dinv = 1 / D_expr
    g = sp.diag(-D_expr**2 * C_SYM**2, Dinv**2, R_COORD**2,
                R_COORD**2 * sp.sin(THETA)**2)
    return g


def curvature(D_expr):
    """Return (Ricci scalar R symbolic-simplified, Kretschmann K as lambdable expr).

    K = R_{abcd} R^{abcd}: first index of Riemann raised ONCE (cheap), then a
    single contraction sum — no 4^8 double-sum. The result is checked
    NUMERICALLY against closed-form oracles by the caller (lambdify), which is
    both fast and rigorous to double precision at the sampled radii.
    """
    g = _metric_functions(D_expr)
    n = 4
    t = sp.Symbol('t', real=True)
    phi = sp.Symbol('phi', real=True)
    coords = [t, R_COORD, THETA, phi]
    ginv = g.inv()

    def gamma(a, b, c):
        # Gamma^a_{bc} = 1/2 g^{ad} ( d_c g_db + d_b g_dc − d_d g_bc )
        return sp.Rational(1, 2) * sum(
            ginv[a, d] * (sp.diff(g[d, b], coords[c])
                          + sp.diff(g[d, c], coords[b])
                          - sp.diff(g[b, c], coords[d]))
            for d in range(n))

    # Riemann R^a_{bcd} with FIRST index raised directly (cheaper than lower-first)
    R_up = {}
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    expr = (sp.diff(gamma(a, b, d), coords[c])
                            - sp.diff(gamma(a, b, c), coords[d]))
                    for e in range(n):
                        expr += (gamma(a, c, e) * gamma(e, b, d)
                                 - gamma(a, d, e) * gamma(e, b, c))
                    ex = sp.together(expr)
                    if ex != 0:
                        R_up[(a, b, c, d)] = ex
    # K = R_{abcd} R^{abcd}:
    #   R_{abcd}  = g_{am} R^m_{bcd}            (R_up haelt R^a_{bcd})
    #   R^{abcd}  = g^{bq} g^{cs} g^{dt} R^a_{qst}
    # (g^{ap} g_{pm} = delta^a_m kuerzt sich beim ersten Index.)
    K = sp.Integer(0)
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    r_lower = sp.Add(*[g[a, m] * R_up.get((m, b, c, d), sp.Integer(0))
                                       for m in range(n)])
                    if r_lower == 0:
                        continue
                    r_upper = sp.Add(*[ginv[b, q] * ginv[c, s] * ginv[d, t]
                                       * R_up.get((a, q, s, t), sp.Integer(0))
                                       for q in range(n) for s in range(n)
                                       for t in range(n)])
                    if r_upper == 0:
                        continue
                    K += r_lower * r_upper
    K_raw = sp.together(K)
    # Ricci: R_{ab} = R^c_{a c b};  Rscal = g^{mn} R_{mn}
    Ric = {(a, b): sum(R_up.get((c, a, c, b), 0) for c in range(n))
           for a in range(n) for b in range(n)}
    Rscal = sp.simplify(sum(ginv[m, n_] * Ric[(m, n_)]
                            for m in range(n) for n_ in range(n)))
    return Rscal, K_raw


def main():
    print("=" * 78)
    print("R5 — Krümmungsinvarianten für ds² = −D²c²dt² + D^(-2)dr² + r²dΩ²")
    print("=" * 78)

    print("\n[1] Kontrolle D ≡ 1 (flach):")
    R, K = curvature(sp.Integer(1))
    print(f"    R = {R}   K = {K}")
    assert sp.simplify(R) == 0 and sp.simplify(K) == 0, "Flachraum-Kontrolle FEHLGESCHLAGEN"
    print("    → OK (R=0, K=0)")

    def K_check(K_expr, oracle, radii, r_s_val):
        """Numerische Orakel-Prüfung des symbolischen K an mehreren Radien.
        K ist für statisch-kugelsymmetrische Metriken θ-unabhängig; das wird
        unten symbolisch geprüft (dK/dθ = 0 an θ=π/2), danach θ=π/2 gesetzt."""
        import sympy as _sp
        dK_dtheta = _sp.diff(K_expr, THETA).subs(THETA, _sp.pi / 2)
        assert _sp.simplify(dK_dtheta) == 0, "K ist nicht theta-unabhaengig?!"
        K_eval = K_expr.subs(THETA, _sp.pi / 2)
        f = _sp.lambdify((R_COORD, RS_SYM, C_SYM), K_eval, 'numpy')
        worst = 0.0
        for r_val in radii:
            got = float(f(r_val, r_s_val, 299792458.0))
            want = float(oracle(r_val, r_s_val))
            rel = abs(got - want) / abs(want)
            worst = max(worst, rel)
        return worst

    print("\n[2] Kontrolle Schwarzschild D² = 1 − r_s/r (Orakel K = 12 r_s²/r⁶):")
    D_schw = sp.sqrt(1 - RS_SYM / R_COORD)
    R, K = curvature(D_schw)
    print(f"    R (symbolisch vereinfacht) = {sp.simplify(R)}")
    worst = K_check(K, lambda r, rs: 12 * rs**2 / r**6,
                    radii=(3.0, 5.0, 11.0, 100.0), r_s_val=2.0)
    print(f"    K vs 12 r_s²/r⁶ an 4 Radien: worst rel Abweichung = {worst:.3e}")
    assert worst < 1e-9, "Schwarzschild-Kretschmann-Orakel verfehlt"
    print("    → OK (Orakel numerisch exakt getroffen an allen Stützstellen)")
    K_h = sp.Rational(12, 1) / sp.Integer(2)**4  # 12 rs²/rs⁴ = 12/rs⁴ = 0.75 für rs=2
    print(f"    K(r = r_s) = 12 r_s²/r_s⁴ = {float(K_h)} (ENDLICH — aus der")
    print("    geschlossenen Form; die UNVEREINFACHTE symbolische K-Form darf vor")
    print("    Substitution nicht direkt an r=r_s gesetzt werden (0/0-Artefakt).")
    print("    Die 'Singularität' des Schwarzschild-Horizonts ist ein KOORDINATEN-")
    print("    ARTEFAKT; die zentrale Krümmungssingularität liegt bei r→0:")
    print("    K = 12 r_s²/r⁶ → ∞ (vgl. Martel & Poisson, arXiv:gr-qc/0001069).")

    print("\n[3] Repo-Ansatz A: D_A = 1/(2 − exp(−φ r_s/r))  [Xi_A = 1 − exp(−φ/x)]:")
    PHI = (1 + sp.sqrt(5)) / 2
    D_A = 1 / (2 - sp.exp(-PHI * RS_SYM / R_COORD))
    R, K = curvature(D_A)
    print(f"    R = {sp.simplify(R)}")
    for r_val in (0.5, 1.0, 2.0, 10.0):
        Kv = sp.N(K.subs([(R_COORD, r_val), (RS_SYM, 1.0), (C_SYM, 1)]))
        print(f"    K(r = {r_val} r_s) = {Kv}")
    print("    → BEFUND: D_A > 0 überall, aber D>0 BEWEIST KEINE REGULARITÄT.")
    print("      Die K-Werte am Zentrum (r→0) sind hier die relevanten Größen;")
    print("      eine 'singularity-free'-Behauptung würde Geodätenvollständigkeit,")
    print("      Energiebedingungen und Feldgleichungen erfordern — NICHTS davon")
    print("      ist im Repo geleistet (audit R5).")

    print("\n[4] Repo-Ansatz B: D_B = 1/(2 − exp(−φ r/r_s))  [Xi_B = 1 − exp(−φ x)]:")
    D_B = 1 / (2 - sp.exp(-PHI * R_COORD / RS_SYM))
    R, K = curvature(D_B)
    print(f"    R = {sp.simplify(R)}")
    for r_val in (0.5, 1.0, 10.0):
        Kv = sp.N(K.subs([(R_COORD, r_val), (RS_SYM, 1.0), (C_SYM, 1)]))
        print(f"    K(r = {r_val} r_s) = {Kv}")
    print("    → B: D→1/2 im Fernfeld — NICHT asymptotisch flach (R4);")
    print("      dieselbe R5-Einschränkung wie bei A.")

    print("\nStatus dieser Ausgaben: NUMERISCHE Tests über symbolische Herleitung;")
    print("keine physikalische Regularitäts- oder Informationsparadoxon-Aussage.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
