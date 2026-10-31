# MODEL TABLES — code-generiert (R4)

Erzeugt von `scripts/generate_model_tables.py` (commit-fester Lauf, kein
Handwert). Neuberechnung: `python scripts/generate_model_tables.py`.
Definitionen x = r/r_s; Werte aus `ssz_qubits` mit expliziten Modellen;
Grenzen/Reihen unabhängig mit mpmath (50 dps).

## 1. Grenzwerte (extreme endliche Stützstellen)

| Modell | Xi(x→0⁺) [x=1e-12] | Xi(x→∞) [x=1e12] | D(x→0⁺) | D(x→∞) |
|---|---|---|---|---|
| weak | 500000000000 | 5e-13 | 1.999999999996e-12 | 0.9999999999995 |
| strong_A | 1 | 1.61803398874859e-12 | 0.5 | 0.999999999998382 |
| strong_B | 1.61803398874859e-12 | 1 | 0.999999999998382 | 0.5 |

Korrigierte Fassung (R4): Für Ansatz A gilt Xi_A(0⁺)=1, D_A(0⁺)=1/2, Xi_A(∞)=0, D_A(∞)=1. Für Ansatz B gilt Xi_B(0⁺)=0, Xi_B(∞)=1, D_B(∞)=1/2 — B ist als Uhrenfaktor NICHT global asymptotisch flach. Die frühere Dokumentation mit umgekehrten A-Limits („Xi(0)=0, singularity-free“) war FALSCH (siehe docs/audit/ISSUE_MATRIX.md R4).

## 2. Asymptotische Reihen

Reihen (Ordnung x^-3) gegen Code-/mpmath-Werte bei x = 10^4:

| Reihe | Wert (mpmath) | Reihe abgeschnitten | rel. Abweichung |
|---|---|---|---|
| Xi_A = phi/x - phi^2/(2x^2) + phi^3/(6x^3) - ... | 0.000161790309411 | 0.000161790309411 | 1.77e-13 |
| D_A  = 1 - phi/x + (3/2)phi^2/x^2 - (5/3)phi^3/x^3 + ... | 0.999838235862 | 0.999838235865 | 2.12e-12 |
| Xi_w = 1/(2x) (exakt) | 5.0e-5 | 5.0e-5 | 0.0 |
| D_GR = 1 - 1/(2x) - 1/(8x^2) - ...  [Schwarzschild] | 0.99994999875 | 0.99994999875 | 6.25e-14 |

**GR-Vergleich (R4, erste nichtverschwindende Ordnung):** D_A ≈ 1 − φ/x vs. D_GR ≈ 1 − 1/(2x). Der führende Korrekturkoeffizient unterscheidet sich um den Faktor **2φ ≈ 3.236** — Ansatz A ist im Fernfeld *nicht* GR-identisch, obwohl beide D → 1 gehen. Ein kleiner absoluter Unterschied bei x ≫ 1 belegt keine Gleichheit der messbaren führenden Rotverschiebung.

## 3. Monotonie

| Modell | min dXi/dr über Grid (1e-3 … 1e6) | monoton fallend? |
|---|---|---|
| weak | -5.637102e+07 | JA |
| strong_A | -3.771978e+01 | JA |
| strong_B | 0.000000e+00 | NEIN |

Alle drei etablierten Modelle fallen streng monoton; die frühere Behauptung, Ansatz A steige im 'Saturation'-Bereich, war falsch (folgte aus dem R1-Vorzeichenfehler in xi_gradient).

## 4. Was diese Tabellen NICHT zeigen

- Keine Aussage über Krümmungsinvarianten, Geodätenvollständigkeit oder
  Energiebedingungen — D>0 allein belegt keine Regularität (R5; siehe
  `scripts/metric_invariants.py` für die tatsächlichen Invarianten).
- Keine Feldgleichungsherkunft der Profile (alle drei bleiben POSTULATE).
- Keinexperimenteller Nachweis; dies ist Modellbuchhaltung.
