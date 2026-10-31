#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_phi_ladder.py — Phase-2-Verifikation der φ-Leiter (Audit-Abschnitt φ).

Geprüft werden die DOKUMENTIerten Identitäten (AUDIT_DE-qubit.md, φ-Abschnitt),
getrennt nach Ansatz A und B, mit mpmath-Hochpräzision:

  1. D_GR(φ) = 1/φ                                  (x_k = φ^k, k ≥ 0)
  2. a_{k+1} = (a_k + 1/φ)/φ  mit a_k = 1 − φ^(−k)   (Exakt-Rekursion)
  3. A: q_k = e^(−φ^(1−k)) ⇒ q_{k+1} = q_k^(1/φ)     (außen, unkappt)
     A: Ξ_{k+1} = 1 − (1−Ξ_k)^(1/φ)
  4. B: p_k = e^(−φ^(k+1)) ⇒ p_{k+1} = p_k^φ         (außen, unkappt)
     B: Ξ_{k+1} = 1 − (1−Ξ_k)^φ
  5. Hin-/Rückrechnung über viele Stufen (Invertierbarkeit der unkappten
     Rekursionen) und der VERSCHIEDENEN gekappten Vorschrift (Knick bei x=1,
     NICHT invers: 0.8017118471 → außen 0.8017118471 → innen 0.6321205588).
  6. Nullstellen der GR-Schnittbedingung (ungekappt, getrennt):
     A: x* = 1.594811457889 ; B: x* = 1.386561619649.

Status: NUMERISCHE_TESTS. Die Nullstellensuche bestätigt Existenz am
Vorzeichenwechsel, KEINE Eindeutigkeit (Intervallbeweis offen).
© 2025 Carmen Wrede, Lino Casu — ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""
import sys
from pathlib import Path

import mpmath as mp

mp.mp.dps = 40
PHI = (1 + mp.sqrt(5)) / 2

OK = True


def check(name, cond, detail=""):
    global OK
    status = "PASS" if cond else "FAIL"
    if not cond:
        OK = False
    print(f"[{status}] {name}" + (f" — {detail}" if detail else ""))


def main():
    print("=" * 78)
    print("Phase 2 — φ-Leiter: Identitäten, Rekursionen, Cap-Knick, Nullstellen")
    print("=" * 78)

    # 1) D_GR(φ) = 1/φ
    dgr = mp.sqrt(1 - 1 / PHI)
    check("D_GR(phi) = 1/phi", abs(dgr - 1 / PHI) < mp.mpf(10) ** -35,
          f"D_GR(phi)={mp.nstr(dgr, 20)}  1/phi={mp.nstr(1 / PHI, 20)}")

    # 2) a-Rekursion
    ok = True
    a = 1 - PHI ** 0  # a_0 = 0
    for k in range(0, 30):
        expect = 1 - PHI ** (-(k + 1))
        a = (a + 1 / PHI) / PHI
        if abs(a - expect) > mp.mpf(10) ** -30:
            ok = False
            break
    check("a_{k+1} = (a_k + 1/phi)/phi, a_k = 1 - phi^(-k)", ok, f"30 Stufen, dps=40")

    # 3) A-Rekursion: q_{k+1} = q_k^(1/phi) für q_k = e^(-phi^(1-k))
    ok = True
    for k in range(-5, 8):
        qk = mp.e ** (-PHI ** (1 - k))
        qk1 = mp.e ** (-PHI ** (1 - (k + 1)))
        if abs(qk ** (1 / PHI) - qk1) > mp.mpf(10) ** -30 * abs(qk1):
            ok = False
            break
    check("A: q_{k+1} = q_k^(1/phi) für q_k = e^(-phi^(1-k))", ok, "k=-5..7")
    ok = True
    for k in range(-5, 8):
        xik = 1 - mp.e ** (-PHI ** (1 - k))
        xik1 = 1 - mp.e ** (-PHI ** (1 - (k + 1)))
        if abs(1 - (1 - xik) ** (1 / PHI) - xik1) > mp.mpf(10) ** -30:
            ok = False
            break
    check("A: Xi_{k+1} = 1 - (1-Xi_k)^(1/phi)", ok)

    # 4) B-Rekursion
    ok = True
    for k in range(-5, 8):
        pk = mp.e ** (-PHI ** (k + 1))
        pk1 = mp.e ** (-PHI ** (k + 2))
        if abs(pk ** PHI - pk1) > mp.mpf(10) ** -30 * abs(pk1):
            ok = False
            break
    check("B: p_{k+1} = p_k^phi für p_k = e^(-phi^(k+1))", ok, "k=-5..7")
    ok = True
    for k in range(-5, 8):
        xik = 1 - mp.e ** (-PHI ** (k + 1))
        xik1 = 1 - mp.e ** (-PHI ** (k + 2))
        if abs(1 - (1 - xik) ** PHI - xik1) > mp.mpf(10) ** -30:
            ok = False
            break
    check("B: Xi_{k+1} = 1 - (1-Xi_k)^phi", ok)

    # 5) Hin-/rück über viele Stufen (unkappt: exakt invertierbar?)
    #    A außen: Xi_{k+1} = 1−(1−Xi_k)^(1/φ) ⇄ Xi_k = 1−(1−Xi_{k+1})^φ
    x0 = mp.mpf('0.3')
    xk = x0
    for _ in range(40):
        xk = 1 - (1 - xk) ** (1 / PHI)
    xback = x0
    for _ in range(40):
        xback = 1 - (1 - xback) ** PHI
    # Richtung 2 rueckwaerts zum Start:
    xk2 = xk
    for _ in range(40):
        xk2 = 1 - (1 - xk2) ** PHI
    check("A: 40 Stufen hin + 40 Stufen zurueck kehrt zum Start",
          abs(xk2 - x0) < mp.mpf(10) ** -20,
          f"Start={mp.nstr(x0, 10)} zurück={mp.nstr(xk2, 12)}")

    # Gekappte Vorschrift (Doku-Modell): Cap min(1−e^{−φx}, Ξ_max=1−e^{−φ})
    # auf der Leiter x_k = φ^k. Audit-Regression: Start Ξ=0.8017118471 (x=1);
    # Schritt außen (x=φ): Formelwert 1−e^{−φ²}=0.9255 > Cap → CAP hält →
    # gleicher Wert; Schritt innen (x=1/φ): 1−e^{−1}=0.6321205588 — die
    # Cap-Vorschrift ist daher NICHT invers (Verlust 0.1695912883).
    xi_cap = mp.mpf('0.8017118471')
    xi_max = 1 - mp.e ** (-PHI)

    def capped_B(x):
        return min(1 - mp.e ** (-PHI * x), xi_max)

    x_start = mp.mpf(1)               # x_0 = 1 → Ξ = 1−e^{−φ} = Startwert
    check("Cap-Setup: Ξ(x=1) = 1−e^{−φ} = 0.8017118471",
          abs(capped_B(x_start) - xi_cap) < mp.mpf('5e-10'))
    outer = capped_B(x_start * PHI)   # Schritt außen
    inner = capped_B(x_start / PHI)   # Schritt innen
    check("Gekappt: außen (x=φ) → Cap hält → gleicher Wert 0.8017118471",
          abs(outer - xi_cap) < mp.mpf('5e-10'),
          f"Formelwert außen = {mp.nstr(1 - mp.e**(-PHI*PHI), 8)} > Cap")
    check("Gekappt: innen (x=1/φ) → 0.6321205588 (Audit-Regression)",
          abs(inner - mp.mpf('0.6321205588')) < mp.mpf('5e-10'),
          f"berechnet={mp.nstr(inner, 12)}")
    check("Gekappt: hin(2 Stufen)/zurück NICHT invers (Verlust 0.1695912883)",
          abs((xi_cap - inner) - mp.mpf('0.1695912883')) < mp.mpf('5e-10'))

    # 6) Nullstellen der GR-Schnittbedingung (ungekappt, getrennt):
    #    dokumentierte Schnitte sind die D-Kurven-Schnitte mit D_GR(x)=√(1−1/x):
    #    A: D_A(x) = D_GR(x)  → x*_A = 1.594811457889
    #    B: D_B(x) = D_GR(x)  → x*_B = 1.386561619649
    def D_A(x):
        return 1 / (1 + (1 - mp.e ** (-PHI / x)))
    def D_B(x):
        return 1 / (1 + (1 - mp.e ** (-PHI * x)))
    def D_GR(x):
        return mp.sqrt(1 - 1 / x)

    def bisect(f, lo, hi, n=200):
        flo, fhi = f(lo), f(hi)
        assert flo * fhi <= 0, "kein Vorzeichenwechsel im Intervall"
        for _ in range(n):
            mid = (lo + hi) / 2
            if flo * f(mid) <= 0:
                hi = mid
            else:
                lo = mid
                flo = f(lo)
        return (lo + hi) / 2

    xA = bisect(lambda x: D_A(x) - D_GR(x), mp.mpf('1.2'), mp.mpf('2.0'))
    check("A: D_A = D_GR bei x* = 1.594811457889 (Bisektion, Existenz)",
          abs(xA - mp.mpf('1.594811457889')) < mp.mpf('5e-12'),
          f"x*_A = {mp.nstr(xA, 15)}")

    xB = bisect(lambda x: D_B(x) - D_GR(x), mp.mpf('1.05'), mp.mpf('1.6'))
    check("B: D_B = D_GR bei x* = 1.386561619649 (Bisektion, Existenz)",
          abs(xB - mp.mpf('1.386561619649')) < mp.mpf('5e-12'),
          f"x*_B = {mp.nstr(xB, 15)}")
    print("\nEindeutigkeit der Nullstellen: OFFEN (numerische Suche = Existenz,")
    print("kein Intervallbeweis; leget die Doku einen Zwischenwertsatz nur für")
    print("Existenz aus — korrekt so gelabelt.)")

    print("\nGESAMT:", "PASS" if OK else "FAIL")
    return 0 if OK else 1


if __name__ == "__main__":
    sys.exit(main())
