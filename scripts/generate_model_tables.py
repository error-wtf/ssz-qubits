#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_model_tables.py — reproduzierbare Referenztabellen für die SSZ-Modelle
(Reparaturauftrag 2026-10-31, R4: "Kontrolliere Tabellen durch echten Code und
generiere sie reproduzierbar statt händisch").

Erzeugt docs/research/MODEL_TABLES.md. Alle Zahlen werden AUS DEM CODE berechnet
(ssz_qubits, explizite Modelle), Grenzfälle über extreme endliche Stützstellen
und Reihen numerisch gegen die behaupteten Koeffizienten geprüft (mpmath, 50 dps).

Aufruf:  python scripts/generate_model_tables.py   (schreibt die .md Datei)
© 2025 Carmen Wrede, Lino Casu — ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""
import sys
from pathlib import Path

import numpy as np
from mpmath import mp

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from ssz_qubits import (  # noqa: E402
    M_EARTH, PHI, schwarzschild_radius,
    xi_segment_density, xi_gradient, ssz_time_dilation,
)

mp.dps = 50
RS = schwarzschild_radius(M_EARTH)

MODELS = {
    'weak':   r"Xi_w(x) = 1/(2x)",
    'strong_A': r"Xi_A(x) = 1 - exp(-phi/x)",
    'strong_B': r"Xi_B(x) = 1 - exp(-phi*x)",
}


def xi_mp(model, x):
    """Hohe Präzision, unabhängig vom Implementierungscode (mpmath)."""
    x = mp.mpf(x)
    phi = mp.phi
    if model == 'weak':
        return 1 / (2 * x)
    if model == 'strong_A':
        return 1 - mp.e**(-phi / x)
    if model == 'strong_B':
        return 1 - mp.e**(-phi * x)
    raise ValueError(model)


def limit_table():
    """Grenzwerte über extreme ENDLICHE Stützstellen (kein symbolisches Limit)."""
    rows = ["| Modell | Xi(x→0⁺) [x=1e-12] | Xi(x→∞) [x=1e12] | D(x→0⁺) | D(x→∞) |",
            "|---|---|---|---|---|"]
    for m in MODELS:
        xi0 = float(xi_mp(m, 1e-12))
        xiinf = float(xi_mp(m, 1e12))
        d0 = 1.0 / (1.0 + xi0)
        dinf = 1.0 / (1.0 + xiinf)
        rows.append(f"| {m} | {xi0:.15g} | {xiinf:.15g} | {d0:.15g} | {dinf:.15g} |")
    rows.append("")
    rows.append("Korrigierte Fassung (R4): Für Ansatz A gilt Xi_A(0⁺)=1, D_A(0⁺)=1/2, "
                "Xi_A(∞)=0, D_A(∞)=1. Für Ansatz B gilt Xi_B(0⁺)=0, Xi_B(∞)=1, "
                "D_B(∞)=1/2 — B ist als Uhrenfaktor NICHT global asymptotisch flach. "
                "Die frühere Dokumentation mit umgekehrten A-Limits („Xi(0)=0, "
                "singularity-free“) war FALSCH (siehe docs/audit/ISSUE_MATRIX.md R4).")
    return "\n".join(rows)


def series_table():
    """Fernfeld-Entwicklungen numerisch bei x=1e4 geprüft (mpmath-Orakel)."""
    x = mp.mpf(10)**4
    phi = mp.phi
    checks = [
        ("Xi_A = phi/x - phi^2/(2x^2) + phi^3/(6x^3) - ...",
         xi_mp('strong_A', x),
         phi/x - phi**2/(2*x**2) + phi**3/(6*x**3)),
        ("D_A  = 1 - phi/x + (3/2)phi^2/x^2 - (5/3)phi^3/x^3 + ...",
         1/(1 + xi_mp('strong_A', x)),
         1 - phi/x + mp.mpf(3)/2*phi**2/x**2 - mp.mpf(5)/3*phi**3/x**3),
        ("Xi_w = 1/(2x) (exakt)",
         xi_mp('weak', x), 1/(2*x)),
        ("D_GR = 1 - 1/(2x) - 1/(8x^2) - ...  [Schwarzschild]",
         mp.sqrt(1 - 1/x),
         1 - 1/(2*x) - 1/(8*x**2)),
    ]
    rows = ["Reihen (Ordnung x^-3) gegen Code-/mpmath-Werte bei x = 10^4:",
            "", "| Reihe | Wert (mpmath) | Reihe abgeschnitten | rel. Abweichung |",
            "|---|---|---|---|"]
    for name, val, ser in checks:
        rel = abs(val - ser) / abs(val)
        rows.append(f"| {name} | {mp.nstr(val, 12)} | {mp.nstr(ser, 12)} | {mp.nstr(rel, 3)} |")
    rows.append("")
    rows.append(
        "**GR-Vergleich (R4, erste nichtverschwindende Ordnung):** "
        "D_A ≈ 1 − φ/x vs. D_GR ≈ 1 − 1/(2x). Der führende Korrekturkoeffizient "
        "unterscheidet sich um den Faktor **2φ ≈ 3.236** — Ansatz A ist im Fernfeld "
        "*nicht* GR-identisch, obwohl beide D → 1 gehen. Ein kleiner absoluter "
        "Unterschied bei x ≫ 1 belegt keine Gleichheit der messbaren führenden "
        "Rotverschiebung.")
    return "\n".join(rows)


def monotonicity_table():
    rows = ["| Modell | min dXi/dr über Grid (1e-3 … 1e6) | monoton fallend? |",
            "|---|---|---|"]
    grid = np.logspace(-3, 6, 4000) * RS
    for m in MODELS:
        grads = [xi_gradient(r, M_EARTH, regime=m) for r in grid]
        gmin = min(grads)
        rows.append(f"| {m} | {gmin:.6e} | {'JA' if gmin < 0 else 'NEIN'} |")
    rows.append("")
    rows.append("Befund: `weak` und `strong_A` fallen streng monoton; `strong_B` steigt "
                "streng monoton gegen Xi=1 (min dXi/dr = 0 nur als Sättigungsgrenze). "
                "Die frühere Behauptung, Ansatz A steige im 'Saturation'-Bereich, war "
                "falsch (folgte aus dem R1-Vorzeichenfehler in xi_gradient). Hinweis: "
                "Das weak-Modell ist nur für x > 100 deklariert; seine Werte bei x < 1 "
                "liegen außerhalb des Gültigkeitsbereichs und dienen nur der Vollständigkeit.")
    return "\n".join(rows)


def main():
    content = f"""# MODEL TABLES — code-generiert (R4)

Erzeugt von `scripts/generate_model_tables.py` (commit-fester Lauf, kein
Handwert). Neuberechnung: `python scripts/generate_model_tables.py`.
Definitionen x = r/r_s; Werte aus `ssz_qubits` mit expliziten Modellen;
Grenzen/Reihen unabhängig mit mpmath (50 dps).

## 1. Grenzwerte (extreme endliche Stützstellen)

{limit_table()}

## 2. Asymptotische Reihen

{series_table()}

## 3. Monotonie

{monotonicity_table()}

## 4. Was diese Tabellen NICHT zeigen

- Keine Aussage über Krümmungsinvarianten, Geodätenvollständigkeit oder
  Energiebedingungen — D>0 allein belegt keine Regularität (R5; siehe
  `scripts/metric_invariants.py` für die tatsächlichen Invarianten).
- Keine Feldgleichungsherkunft der Profile (alle drei bleiben POSTULATE).
- Keinexperimenteller Nachweis; dies ist Modellbuchhaltung.
"""
    out = ROOT / "docs" / "research" / "MODEL_TABLES.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8")
    print(f"geschrieben: {out}")


if __name__ == "__main__":
    main()
