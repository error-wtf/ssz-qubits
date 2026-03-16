# GR-SSZ Intersection: Ableitung auf dem φ-Gitter

**Version:** 1.0  
**Datum:** 2026-03-16  
**Autoren:** Carmen Wrede & Lino Casu  
**Basis:** `gr-ssz-match.md` (error-wtf/segmented-calculation-suite)  
**Status:** KANONISCH

---

## Zusammenfassung

`gr-ssz-match.md` dokumentiert zwei Formeln für die SSZ-Segmentdichte Xi(r) und zwei
verschiedene Schnittpunkte r*/r_s ≈ 1.595 und r*/r_s ≈ 1.387, an denen D_SSZ = D_GR gilt.
Dieses Dokument diskretisiert das Schnittpunktproblem **ableitungsartig** auf dem natürlichen
φ-Gitter x_k = φ^k und beantwortet algebraisch:

1. Warum liegen **beide** Schnittpunkte im **selben** φ-Bracket [φ⁰, φ¹] = [1.000, 1.618]?
2. Welche exakten Rekursionsformeln verbinden D_GR und D_SSZ auf dem Gitter?
3. Was ist die Aussage für echte astrophysikalische Objekte?

**Hauptergebnis:** Beide Schnittpunkte — obwohl numerisch verschieden — sind algebraisch durch
dieselbe Ungleichungskette gebunden: φ + e⁻¹ < 2 und φ + e^{−φ²} < 2. Beide liegen zwingend
im Bracket [1, φ].

---

## Inhaltsverzeichnis

1. [Ausgangsproblem](#1-ausgangsproblem)
2. [Das φ-Gitter als natürliche Diskretisierung](#2-das-φ-gitter-als-natürliche-diskretisierung)
3. [Ableitung: D_GR am φ-Gitter](#3-ableitung-d_gr-am-φ-gitter)
4. [Ableitung: D_SSZ am φ-Gitter — Abklingform](#4-ableitung-d_ssz-am-φ-gitter--abklingform)
5. [Ableitung: D_SSZ am φ-Gitter — Sättigungsform](#5-ableitung-d_ssz-am-φ-gitter--sättigungsform)
6. [Vorzeichenanalyse und Bracket-Theorem](#6-vorzeichenanalyse-und-bracket-theorem)
7. [Schwachfeld-Asymptotik: Konvergenz beider Formeln zur GR](#7-schwachfeld-asymptotik-konvergenz-beider-formeln-zur-gr)
8. [Test an echten astrophysikalischen Werten](#8-test-an-echten-astrophysikalischen-werten)
9. [Python-Verifikation](#9-python-verifikation)
10. [Zusammenfassung](#10-zusammenfassung)

---

## 1. Ausgangsproblem

### 1.1 Zwei Formeln für Xi(r)

`gr-ssz-match.md` definiert mit x = r/r_s:

```
Abklingform (Calculation-Suite):    Xi_A(x) = 1 - exp(-φ/x) = 1 - exp(-φ r_s/r)
Sättigungsform (Unified-Results):   Xi_B(x) = 1 - exp(-φ x) = 1 - exp(-φ r/r_s)
```

Beide stimmen exakt bei x = 1 (r = r_s) überein:

```
Xi_A(1) = Xi_B(1) = 1 - exp(-φ) = Xi_max ≈ 0.801711847
```

Die Zeitdilatation lautet in beiden Fällen:

```
D_SSZ(x) = 1 / (1 + Xi(x))
```

Für x = 1: D_SSZ(1) = 1/(2 - exp(-φ)) ≈ 0.555027710 — endlich, singularitätsfrei.

### 1.2 GR-Zeitdilatation

Die allgemein-relativistische Zeitdilatation (Schwarzschild-Metrik, radiale Ruhe):

```
D_GR(x) = sqrt(1 - 1/x)     für x > 1
D_GR(1) = 0                  (Koordinatensingularität)
```

### 1.3 Die beiden Schnittpunkte

Aus `gr-ssz-match.md` (numerisch verifiziert):

| Formel | Schnittpunkt r*/r_s | D* |
|--------|--------------------|----|
| Abklingform Xi_A | 1.594811 | 0.610710 |
| Sättigungsform Xi_B | 1.387 | 0.528 |

**Frage:** Warum liegen beide im Bereich [1.0, 1.618]? Ist das Zufall oder strukturell?

---

## 2. Das φ-Gitter als natürliche Diskretisierung

### 2.1 Definition

Der Goldene Schnitt φ = (1+√5)/2 = 1.6180339887... erzeugt das φ-Gitter:

```
x_k = φ^k     (k ∈ ℤ)
```

Eigenschaften (aus Kapitel 3 des Buches):
- Jeder Schritt nach außen: x_{k+1} = φ · x_k
- φ² = φ + 1 (Fibonacci-Identität)
- (1/φ)² = 2 - φ  ← wird in Satz 1 zentral

### 2.2 Gitterpunkte und ihr physikalischer Kontext

| k | x_k = φ^k | r_k = r_s · x_k | Physikalischer Kontext |
|---|-----------|-----------------|------------------------|
| 0 | 1.0000 | r_s | Schwarzschild-Radius (Horizont) |
| 1 | 1.6180 | 1.618 r_s | φ-Schritt über Horizont |
| 2 | 2.6180 | 2.618 r_s | Photonensphäre-Bereich |
| 3 | 4.2361 | 4.236 r_s | Innerste stabile Kreisbahn (ISCO ≈ 3r_s) |
| 4 | 6.8541 | 6.854 r_s | Starkes Starkfeld |

**Beobachtung:** Der Intersection-Bereich [1.387, 1.595] aus `gr-ssz-match.md` liegt exakt zwischen
den Gitterpunkten k=0 und k=1 — also im Bracket [φ⁰, φ¹] = [1.000, 1.618].

---

## 3. Ableitung: D_GR am φ-Gitter

### 3.1 Allgemeine Formel

An jedem Gitterpunkt x_k = φ^k gilt:

```
D_GR(x_k) = sqrt(1 - φ^{-k})
```

**Tabelle:**

| k | x_k | φ^{-k} | D_GR(x_k) | Exakter Ausdruck |
|---|-----|--------|-----------|-----------------|
| 0 | 1.0000 | 1.0000 | 0 | 0 (Singularität) |
| 1 | 1.6180 | 0.6180 | 0.61803 | 1/φ |
| 2 | 2.6180 | 0.3820 | 0.78615 | 1/√φ |
| 3 | 4.2361 | 0.2361 | 0.87404 | √(1−φ⁻³) |
| 4 | 6.8541 | 0.1459 | 0.92418 | √(1−φ⁻⁴) |

### 3.2 Satz 1: Algebraische Identität D_GR(φ) = 1/φ

**Satz 1:** *Es gilt D_GR(φ) = 1/φ.*

**Beweis:**

Aus der Fibonacci-Identität φ² = φ + 1 folgt durch Umformung:

```
(1/φ)² = 1/φ² = 1/(φ+1) ... nein, einfacher:
```

Wir nutzen: 1/φ = φ - 1. Dann:

```
(1/φ)² = (φ-1)²
       = φ² - 2φ + 1
       = (φ+1) - 2φ + 1      [da φ² = φ+1]
       = 2 - φ
```

Also: 2 - φ = (1/φ)² = φ^{-2}. Damit:

```
D_GR(φ) = sqrt(1 - 1/φ)
         = sqrt(1 - (φ-1))    [da 1/φ = φ-1]
         = sqrt(2 - φ)
         = sqrt((1/φ)²)
         = 1/φ  ✓
```

**Numerisch:** D_GR(1.6180...) = 1/1.6180... = 0.6180... ☐

### 3.3 Satz 2: Rekursionsformel für D_GR

**Satz 2:** *Sei a_k = D_GR(x_k)². Dann gilt:*

```
a_{k+1} = (a_k + 1/φ) / φ
```

**Beweis:**

```
a_k = D_GR(φ^k)² = 1 - φ^{-k}

a_{k+1} = 1 - φ^{-(k+1)}
         = 1 - φ^{-k}/φ
         = 1 - (1 - a_k)/φ
         = 1 - 1/φ + a_k/φ
         = a_k/φ + (1 - 1/φ)
```

Wir zeigen: 1 - 1/φ = 1/φ²

```
1 - 1/φ = 1 - (φ-1) = 2 - φ = (1/φ)² = 1/φ²  ✓  [aus Satz 1]
```

Also: a_{k+1} = a_k/φ + 1/φ² = (a_k · φ + 1) / φ² ... Vereinfachung:

```
a_{k+1} = a_k/φ + 1/φ² = (a_k + 1/φ) / φ  ✓
```

**Fixpunkt:** Aus a* = (a* + 1/φ)/φ → a*·φ = a* + 1/φ → a*(φ-1) = 1/φ → a*·(1/φ) = 1/φ → a* = 1.
D_GR → 1 für k → ∞ (flache Raumzeit).  ☐

---

## 4. Ableitung: D_SSZ am φ-Gitter — Abklingform

### 4.1 Substitution

Abklingform: Xi_A(x) = 1 - exp(-φ/x). An Gitterpunkten x_k = φ^k:

```
Xi_A(x_k) = 1 - exp(-φ · φ^{-k}) = 1 - exp(-φ^{1-k})
```

**Substitution:** q_k := exp(-φ^{1-k}) = 1 - Xi_A(x_k)

Dann gilt:
```
D_SSZ_A(x_k) = 1 / (1 + Xi_A(x_k)) = 1 / (2 - q_k)
```

### 4.2 Tabelle der Gitterwerte

| k | x_k | φ^{1-k} | q_k | D_SSZ_A(x_k) |
|---|-----|---------|-----|--------------|
| 0 | 1.0000 | φ = 1.6180 | exp(−φ) = 0.19829 | 1/(2−0.19829) = **0.55503** |
| 1 | 1.6180 | 1.0000 | exp(−1) = 0.36788 | 1/(2−0.36788) = **0.61270** |
| 2 | 2.6180 | 1/φ = 0.6180 | exp(−0.6180) = 0.53902 | 1/(2−0.53902) = **0.68449** |
| 3 | 4.2361 | 1/φ² = 0.3820 | exp(−0.3820) = 0.68233 | 1/(2−0.68233) = **0.75899** |
| 4 | 6.8541 | 1/φ³ = 0.2361 | exp(−0.2361) = 0.78979 | 1/(2−0.78979) = **0.82687** |

### 4.3 Satz 3: Rekursionsformel für q_k (Abklingform)

**Satz 3:** *Es gilt q_{k+1} = q_k^{1/φ}  (Schritt nach außen: x → φx).*

**Beweis:**

```
q_k     = exp(-φ^{1-k})
q_{k+1} = exp(-φ^{1-(k+1)}) = exp(-φ^{-k})
```

Wir zeigen: φ^{-k} = φ^{1-k}/φ = (log-Basis: −φ^{1-k} / φ):

```
q_{k+1} = exp(-φ^{1-k}/φ)
         = exp(-φ^{1-k})^{1/φ}    [Potenzregel: exp(a/φ) = exp(a)^{1/φ}]
         = q_k^{1/φ}  ✓
```  ☐

**In log-Skala** ist die Rekursion linear: ln(q_{k+1}) = ln(q_k)/φ.

**Konsequenz:**
```
q_{k+n} = q_k^{φ^{-n}}     [n Schritte nach außen]
```

Als k → ∞: q_k → 1, Xi_A → 0, D_SSZ_A → 1 (flache Raumzeit).

---

## 5. Ableitung: D_SSZ am φ-Gitter — Sättigungsform

### 5.1 Substitution

Sättigungsform: Xi_B(x) = 1 - exp(-φx). An Gitterpunkten x_k = φ^k:

```
Xi_B(x_k) = 1 - exp(-φ · φ^k) = 1 - exp(-φ^{k+1})
```

**Substitution:** p_k := exp(-φ^{k+1}) = 1 - Xi_B(x_k)

Dann gilt:
```
D_SSZ_B(x_k) = 1 / (2 - p_k)
```

### 5.2 Tabelle der Gitterwerte

| k | x_k | φ^{k+1} | p_k | D_SSZ_B(x_k) |
|---|-----|---------|-----|--------------|
| 0 | 1.0000 | φ = 1.6180 | exp(−φ) = 0.19829 | 1/(2−0.19829) = **0.55503** |
| 1 | 1.6180 | φ² = 2.6180 | exp(−2.6180) = 0.07322 | 1/(2−0.07322) = **0.51900** |
| 2 | 2.6180 | φ³ = 4.2361 | exp(−4.2361) = 0.01449 | 1/(2−0.01449) = **0.50363** |
| 3 | 4.2361 | φ⁴ = 6.8541 | exp(−6.8541) = 0.00106 | 1/(2−0.00106) = **0.50027** |

**Beobachtung:** D_SSZ_B sinkt schnell → 0.5 für k ≥ 2. Die Sättigungsform ist auf den
Bereich x < 2 (nahe Horizont) ausgelegt.

### 5.3 Satz 4: Rekursionsformel für p_k (Sättigungsform)

**Satz 4:** *Es gilt p_{k+1} = p_k^φ  (Schritt nach außen: x → φx).*

**Beweis:**

```
p_k     = exp(-φ^{k+1})
p_{k+1} = exp(-φ^{k+2}) = exp(-φ · φ^{k+1}) = exp(-φ^{k+1})^φ = p_k^φ  ✓
```  ☐

**In log-Skala:** ln(p_{k+1}) = φ · ln(p_k) — die Sättigungsform ist algebraisch
dual zur Abklingform: die Potenzen 1/φ und φ sind vertauscht.

| Formel | Substitution | Rekursion (außen) | Verhalten für k → ∞ |
|--------|-------------|-------------------|---------------------|
| Abkling (A) | q_k = exp(−φ^{1−k}) | q_{k+1} = q_k^{1/φ} | q_k → 1, D_SSZ_A → 1 |
| Sättigung (B) | p_k = exp(−φ^{k+1}) | p_{k+1} = p_k^φ | p_k → 0, D_SSZ_B → 1/2 |

---

## 6. Vorzeichenanalyse und Bracket-Theorem

### 6.1 Definition der Differenz

Sei:
```
Δ_k^A = D_SSZ_A(x_k) - D_GR(x_k)     [Abklingform minus GR]
Δ_k^B = D_SSZ_B(x_k) - D_GR(x_k)     [Sättigungsform minus GR]
```

### 6.2 Gitterwerte k = 0 und k = 1

**Bei k = 0 (x = 1, Horizont):**

```
D_GR(1) = sqrt(1 - 1) = 0

D_SSZ_A(1) = D_SSZ_B(1) = 1/(2 - exp(-φ)) ≈ 0.55503    [beide gleich!]

Δ_0^A = Δ_0^B = 0.55503 > 0     ✓  (SSZ regulär, GR singulär)
```

**Bei k = 1 (x = φ):**

```
D_GR(φ) = 1/φ ≈ 0.61803             [aus Satz 1, exakt algebraisch]

D_SSZ_A(φ) = 1/(2 - exp(-1)) = 1/(2 - e⁻¹) ≈ 0.61270
D_SSZ_B(φ) = 1/(2 - exp(-φ²))      ≈ 0.51900

Δ_1^A = 0.61270 - 0.61803 = -0.00533 < 0
Δ_1^B = 0.51900 - 0.61803 = -0.09903 < 0
```

**Vorzeichen-Tabelle:**

| k | x_k | D_GR | D_SSZ_A | D_SSZ_B | Δ^A | Δ^B |
|---|-----|------|---------|---------|-----|-----|
| 0 | 1.000 | 0.00000 | 0.55503 | 0.55503 | **+0.555** | **+0.555** |
| 1 | 1.618 | 0.61803 | 0.61270 | 0.51900 | **−0.005** | **−0.099** |
| 2 | 2.618 | 0.78615 | 0.68449 | 0.50363 | −0.102 | −0.283 |
| 3 | 4.236 | 0.87404 | 0.75899 | 0.50027 | −0.115 | −0.374 |

### 6.3 Satz 5 (Hauptsatz): Beide Schnittpunkte liegen im φ-Bracket [1, φ]

**Satz 5:** *Für beide SSZ-Formeln gilt Δ_0 > 0 und Δ_1 < 0. Da alle Funktionen stetig
sind, liegen beide Schnittpunkte r* im Intervall (φ⁰, φ¹) = (1.000, 1.618).*

**Beweis der Vorzeichenbedingungen:**

**Teil 1: Δ_0 > 0** (gilt für beide Formeln)

D_GR(1) = 0. D_SSZ(1) = 1/(2-exp(-φ)) > 0. Also Δ_0 = D_SSZ(1) - 0 > 0. ☐

**Teil 2: Δ_1^A < 0** (Abklingform)

Zu zeigen: D_SSZ_A(φ) < D_GR(φ), d.h. 1/(2-e⁻¹) < 1/φ.

```
1/(2-e⁻¹) < 1/φ
⟺  φ < 2 - e⁻¹         [beide Seiten positiv, Kehrwert kehrt Ordnung um]
⟺  φ + e⁻¹ < 2
```

**Numerischer Beweis:**

```
φ + e⁻¹ = 1.6180339887... + 0.3678794412... = 1.9859134299... < 2  ✓
```

**Algebraische Begründung:** φ < 2 (da φ = (1+√5)/2 < 2) und e⁻¹ < 1, aber die entscheidende
Aussage ist, dass ihre Summe unter 2 liegt. Dies folgt aus φ < 2 - e⁻¹ ≈ 1.632, was direkt
aus φ = 1.618 < 1.632 verifizierbar ist. ☐

**Teil 3: Δ_1^B < 0** (Sättigungsform)

Zu zeigen: 1/(2-e^{-φ²}) < 1/φ.

```
⟺  φ + e^{-φ²} < 2
```

**Numerischer Beweis:**

```
φ² = 2.6180339887...
e^{-φ²} = e^{-2.618...} ≈ 0.0732...
φ + e^{-φ²} = 1.6180... + 0.0732... = 1.6912... < 2  ✓
```

Da e^{-φ²} < e^{-2} < 0.14 und φ < 2 - 0.14 = 1.86: beide Term tragen so wenig bei,
dass die Summe deutlich unter 2 liegt. ☐

**Fazit:** Beide Δ-Funktionen sind stetig und wechseln das Vorzeichen zwischen k=0 und k=1.
Nach dem Zwischenwertsatz existiert jeweils genau ein Nulldurchgang in (1, φ). ☐

### 6.4 Warum beide Schnittpunkte DASSELBE Bracket teilen

Obwohl die Schnittpunkte numerisch verschieden sind (1.387 vs 1.595), teilen sie das
GLEICHE φ-Bracket [1, φ] = [φ⁰, φ¹]. Dies ist kein Zufall:

- Beide Formeln stimmen **exakt** bei x=1 überein: Xi_A(1) = Xi_B(1) = 1-exp(-φ).
- Bei x=φ gilt für BEIDE: D_SSZ < D_GR = 1/φ, bewiesen durch φ + (kleiner Term) < 2.
- Die unterschiedlichen Abstände vom Schnittpunkt zu φ¹ erklären die verschiedenen r*-Werte.

---

## 7. Schwachfeld-Asymptotik: Konvergenz beider Formeln zur GR

### 7.1 Taylorentwicklung für große x

**Abklingform** für x >> 1 (φ/x << 1):

```
Xi_A(x) = 1 - exp(-φ/x) ≈ φ/x - (φ/x)²/2 + ...
D_SSZ_A(x) = 1/(1 + φ/x - ...) ≈ 1 - φ/x + (φ/x)² + ...
```

**GR** für x >> 1:

```
D_GR(x) = sqrt(1 - 1/x) ≈ 1 - 1/(2x) - 1/(8x²) - ...
```

**Differenz:**

```
D_SSZ_A(x) - D_GR(x) ≈ (1 - φ/x) - (1 - 1/(2x))
                       = -(φ - 1/2)/x
                       = -1.1180.../x     für x >> 1
```

**Sättigungsform** für x << 1 (φx << 1, d.h. nahe Horizont):

```
Xi_B(x) ≈ φx - (φx)²/2 + ...
D_SSZ_B(x) ≈ 1 - φx + ...
```

Die Sättigungsform ist für große x NICHT für das Schwachfeld ausgelegt (Xi_B → Xi_max
statt → 0). Die Abklingform ist die korrekte für globale Analyse.

### 7.2 Tabelle der relativen Differenz

| x = r/r_s | |Δ^A|/D_GR | Physikalisches Objekt |
|-----------|-----------|----------------------|
| 1.595 | 0% (Schnittpunkt) | — |
| 2.0 | ~9% | Kompakter NS |
| 2.5 | ~12% | Typischer NS |
| 10 | ~7% | Stabiles Objekt |
| 100 | ~1.1% | Massereicher Stern |
| 1000 | ~0.11% | Weißer Zwerg |
| 10⁶ | ~1.1×10⁻⁴% | Leichter Stern |
| 10⁹ | ~1.1×10⁻⁷% | GPS-Satellit |

*Relative Differenz ≈ (φ-1/2)/x = 1.118/x für x >> 1.*

---

## 8. Test an echten astrophysikalischen Werten

### 8.1 Testdaten

Alle Werte mit kanonischen SSZ-Formeln (Abklingform Xi_A für x > 1.8, Hermite-C² Blend
für 1.8 ≤ x ≤ 2.2, Sättigungsform Xi_B für x < 1.8):

| Objekt | M [M☉] | R [km] | r_s [km] | x = R/r_s | k_φ | D_GR | D_SSZ_A | Δ = D_SSZ_A − D_GR | Δ/D_GR |
|--------|--------|--------|----------|-----------|-----|------|---------|---------------------|--------|
| BH Horizont | — | r_s | — | **1.000** | [0,1] | 0 (!) | 0.5550 | +0.5550 | — |
| Decay-Schnitt | — | — | — | **1.595** | [0,1] | 0.6107 | 0.6107 | 0.0000 | 0% |
| Satur.-Schnitt | — | — | — | **1.387** | [0,1] | 0.5279 | — | — | — |
| PSR J0740+6620 | 2.08 | 12.4 | 6.14 | **2.020** | [1,2] | 0.7107 | 0.6447 | −0.0660 | −9.3% |
| NS kanonisch | 1.40 | 10.0 | 4.14 | **2.416** | [1,2] | 0.7657 | 0.6721 | −0.0936 | −12.2% |
| PSR J0030+0451 | 1.34 | 12.7 | 3.96 | **3.207** | [2,3] | 0.8297 | 0.7165 | −0.1132 | −13.6% |
| Sirius B | 1.02 | 5800 | 3.01 | **1927** | [15,16] | 0.99974 | 0.99916 | −0.00058 | −0.058% |
| Sonne Oberfläche | 1.00 | 696000 | 2.95 | **235932** | [25,26] | 0.99999788 | 0.99999526 | −2.6×10⁻⁶ | −2.6×10⁻⁴% |
| GPS (Erde) | 5.97×10⁻⁶ | 26571 | 8.87×10⁻³ | **3.0×10⁹** | [45,46] | ≈1 | ≈1 | −3.7×10⁻¹⁰ | ~0 |

**Legende k_φ:** Das φ-Bracket [k, k+1] ist dasjenige, in dem x_obj = R/r_s liegt:
φ^k ≤ x_obj < φ^{k+1}.

### 8.2 Schlussfolgerungen aus den Testdaten

1. **BH-Horizont (x=1):** GR-Singularität D_GR=0, SSZ finit D_SSZ=0.555. Dies ist
   die physikalisch bedeutsamste Diskrepanz und entspricht exakt D_min aus Kapitel 1.

2. **Neutronensterne (x≈2–3, Bracket [1,2] oder [2,3]):** SSZ sagt 9–14% mehr
   Zeitdilatation voraus als GR. Testbar mit NICER (Röntgenspektroskopie).

3. **Weißer Zwerg Sirius B (x≈1927, Bracket [15,16]):** Differenz ~0.06% — unter
   aktueller Messgenauigkeit, aber prinzipiell messbar mit zukünftiger Instrumentierung.

4. **Sonne, GPS (x >> 10⁶):** Differenz < 10⁻⁶ — SSZ und GR praktisch identisch.
   Alle Schwachfeld-Experimente (Pound-Rebka, GPS, Cassini) sind konsistent.

5. **Universelle Schranke:** Die relative Differenz ist stets ≤ (φ-1/2)/x = 1.118/x.
   Kein Experiment bei x > 10 kann SSZ von GR unterscheiden bis zu Präzision 10%.

---

## 9. Python-Verifikation

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GR-SSZ Intersection: φ-Ladder Discretization
Verifikation der Sätze 1-5 und der Testdaten aus Abschnitt 8.

Basis: gr-ssz-match.md (error-wtf/segmented-calculation-suite)

© 2026 Carmen Wrede & Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""

import numpy as np
from scipy.optimize import brentq


# =============================================================================
# KONSTANTEN
# =============================================================================

PHI = (1 + np.sqrt(5)) / 2       # 1.6180339887498948482...
XI_MAX = 1 - np.exp(-PHI)        # 0.801711847... = Xi(r_s)
D_MIN  = 1 / (2 - np.exp(-PHI))  # 0.555027710... = D_SSZ(r_s)


# =============================================================================
# KERNFUNKTIONEN
# =============================================================================

def xi_decay(x):
    """Abklingform (Calculation-Suite): Xi_A(x) = 1 - exp(-phi/x)"""
    return 1.0 - np.exp(-PHI / x)

def xi_satur(x):
    """Sättigungsform (Unified-Results): Xi_B(x) = 1 - exp(-phi*x)"""
    return 1.0 - np.exp(-PHI * x)

def d_ssz(xi):
    """SSZ Zeitdilatation aus Segmentdichte"""
    return 1.0 / (1.0 + xi)

def d_gr(x):
    """GR Zeitdilatation (Schwarzschild)"""
    return np.sqrt(1.0 - 1.0/x) if x > 1.0 else 0.0


# =============================================================================
# SATZ 1: D_GR(φ) = 1/φ
# =============================================================================

class TestSatz1_DGR_Phi:
    """Satz 1: D_GR(φ) = 1/φ (algebraische Identität)."""

    def test_dgr_at_phi(self):
        print("\n" + "="*70)
        print("SATZ 1: D_GR(φ) = 1/φ")
        print("="*70)

        d_gr_phi = d_gr(PHI)
        expected = 1.0 / PHI

        print(f"  D_GR(φ)    = sqrt(1 - 1/φ) = {d_gr_phi:.15f}")
        print(f"  1/φ        =                  {expected:.15f}")
        print(f"  Differenz  =                  {abs(d_gr_phi - expected):.2e}")

        assert abs(d_gr_phi - expected) < 1e-14, f"Satz 1 FAIL: {d_gr_phi} ≠ {expected}"
        print("  STATUS: PASS ✓")

    def test_recursion_satz2(self):
        """Satz 2: a_{k+1} = (a_k + 1/phi) / phi"""
        print("\n" + "="*70)
        print("SATZ 2: Rekursion D_GR²_{k+1} = (D_GR²_k + 1/φ) / φ")
        print("="*70)
        a = [d_gr(PHI**k)**2 for k in range(6)]
        for k in range(5):
            a_next_direct  = d_gr(PHI**(k+1))**2
            a_next_recurse = (a[k] + 1.0/PHI) / PHI
            err = abs(a_next_direct - a_next_recurse)
            print(f"  k={k}: a_k={a[k]:.6f}, a_{{k+1}} direkt={a_next_direct:.6f}, "
                  f"rekursiv={a_next_recurse:.6f}, Δ={err:.2e}")
            assert err < 1e-13, f"Satz 2 FAIL bei k={k}"
        print("  STATUS: PASS ✓")


# =============================================================================
# SATZ 3: Rekursion q_{k+1} = q_k^{1/phi} (Abklingform)
# =============================================================================

class TestSatz3_Decay_Recursion:
    """Satz 3: q_{k+1} = q_k^{1/phi} für q_k = exp(-phi^{1-k})"""

    def test_recursion_decay(self):
        print("\n" + "="*70)
        print("SATZ 3: q_{k+1} = q_k^{1/φ}  [Abklingform]")
        print("="*70)
        for k in range(0, 5):
            q_k       = np.exp(-PHI**(1-k))
            q_k1_direct  = np.exp(-PHI**(1-(k+1)))
            q_k1_recurse = q_k**(1.0/PHI)
            err = abs(q_k1_direct - q_k1_recurse)
            print(f"  k={k}: q_k={q_k:.6f}, q_{{k+1}} direkt={q_k1_direct:.6f}, "
                  f"rekursiv={q_k1_recurse:.6f}, Δ={err:.2e}")
            assert err < 1e-13, f"Satz 3 FAIL bei k={k}"
        print("  STATUS: PASS ✓")


# =============================================================================
# SATZ 4: Rekursion p_{k+1} = p_k^phi (Sättigungsform)
# =============================================================================

class TestSatz4_Satur_Recursion:
    """Satz 4: p_{k+1} = p_k^phi für p_k = exp(-phi^{k+1})"""

    def test_recursion_satur(self):
        print("\n" + "="*70)
        print("SATZ 4: p_{k+1} = p_k^φ  [Sättigungsform]")
        print("="*70)
        for k in range(0, 5):
            p_k         = np.exp(-PHI**(k+1))
            p_k1_direct  = np.exp(-PHI**(k+2))
            p_k1_recurse = p_k**PHI
            err = abs(p_k1_direct - p_k1_recurse)
            print(f"  k={k}: p_k={p_k:.6f}, p_{{k+1}} direkt={p_k1_direct:.6f}, "
                  f"rekursiv={p_k1_recurse:.6f}, Δ={err:.2e}")
            assert err < 1e-13, f"Satz 4 FAIL bei k={k}"
        print("  STATUS: PASS ✓")


# =============================================================================
# SATZ 5: Bracket-Theorem — beide Schnittpunkte in [φ^0, φ^1]
# =============================================================================

class TestSatz5_BracketTheorem:
    """Satz 5: Beide Schnittpunkte liegen im φ-Bracket [1, φ]."""

    def test_delta_sign_decay(self):
        """Vorzeichenwechsel von Δ^A zwischen k=0 und k=1."""
        print("\n" + "="*70)
        print("SATZ 5: Bracket-Theorem (Abklingform)")
        print("="*70)
        delta_0 = d_ssz(xi_decay(1.0))   - d_gr(1.0)
        delta_1 = d_ssz(xi_decay(PHI))   - d_gr(PHI)
        print(f"  Δ^A at k=0 (x=1.000): {delta_0:+.6f}  → {'POSITIV' if delta_0>0 else 'NEGATIV'}")
        print(f"  Δ^A at k=1 (x=φ):     {delta_1:+.6f}  → {'POSITIV' if delta_1>0 else 'NEGATIV'}")
        print(f"  Vorzeichenwechsel:  {delta_0 > 0 and delta_1 < 0}")
        assert delta_0 > 0, "Satz 5 FAIL: Δ_0^A soll positiv sein"
        assert delta_1 < 0, "Satz 5 FAIL: Δ_1^A soll negativ sein"
        print("  STATUS: PASS ✓")

    def test_delta_sign_satur(self):
        """Vorzeichenwechsel von Δ^B zwischen k=0 und k=1."""
        print("\n" + "="*70)
        print("SATZ 5: Bracket-Theorem (Sättigungsform)")
        print("="*70)
        delta_0 = d_ssz(xi_satur(1.0))   - d_gr(1.0)
        delta_1 = d_ssz(xi_satur(PHI))   - d_gr(PHI)
        print(f"  Δ^B at k=0 (x=1.000): {delta_0:+.6f}  → {'POSITIV' if delta_0>0 else 'NEGATIV'}")
        print(f"  Δ^B at k=1 (x=φ):     {delta_1:+.6f}  → {'POSITIV' if delta_1>0 else 'NEGATIV'}")
        print(f"  Vorzeichenwechsel:  {delta_0 > 0 and delta_1 < 0}")
        assert delta_0 > 0, "Satz 5 FAIL: Δ_0^B soll positiv sein"
        assert delta_1 < 0, "Satz 5 FAIL: Δ_1^B soll negativ sein"
        print("  STATUS: PASS ✓")

    def test_intersection_points(self):
        """Numerische Schnittpunkte aus gr-ssz-match.md verifizieren."""
        print("\n" + "="*70)
        print("SATZ 5: Numerische Schnittpunkte (Brentq-Verifikation)")
        print("="*70)

        # Abklingform
        f_decay = lambda x: d_ssz(xi_decay(x)) - d_gr(x)
        x_star_A = brentq(f_decay, 1.001, PHI - 1e-6)
        D_star_A = d_gr(x_star_A)
        print(f"  Abklingform:    r*/r_s = {x_star_A:.6f}  D* = {D_star_A:.6f}")
        print(f"  Erwartung:      r*/r_s = 1.594811       D* = 0.610710")
        assert abs(x_star_A - 1.594811) < 0.0001, "Intersection decay FAIL"
        assert x_star_A > 1.0 and x_star_A < PHI,  "Bracket-Bedingung FAIL"

        # Sättigungsform
        f_satur = lambda x: d_ssz(xi_satur(x)) - d_gr(x)
        x_star_B = brentq(f_satur, 1.001, PHI - 1e-6)
        D_star_B = d_gr(x_star_B)
        print(f"  Sättigungsform: r*/r_s = {x_star_B:.6f}  D* = {D_star_B:.6f}")
        print(f"  Erwartung:      r*/r_s ≈ 1.387          D* ≈ 0.528")
        assert abs(x_star_B - 1.387) < 0.001,  "Intersection satur FAIL"
        assert x_star_B > 1.0 and x_star_B < PHI, "Bracket-Bedingung FAIL"

        print(f"\n  BEIDE Schnittpunkte in φ-Bracket [1.000, {PHI:.3f}]: BESTÄTIGT ✓")
        print("  STATUS: PASS ✓")


# =============================================================================
# ECHTE ASTROPHYSIKALISCHE OBJEKTE
# =============================================================================

class TestRealObjects:
    """Test an echten astrophysikalischen Objekten."""

    G  = 6.6743e-11   # m³/(kg·s²)
    C  = 2.99792458e8 # m/s
    M_SUN = 1.9885e30 # kg

    def r_s(self, M_solar):
        M = M_solar * self.M_SUN
        return 2 * self.G * M / self.C**2  # in Metern

    def test_real_objects(self):
        print("\n" + "="*70)
        print("REALE OBJEKTE: GR vs SSZ (Abklingform)")
        print("="*70)
        print(f"{'Objekt':<25} {'x':>8} {'k_bracket':>10} {'D_GR':>8} {'D_SSZ_A':>9} {'Δ%':>8}")
        print("-"*70)

        objects = [
            ("BH Horizont",         None,  None,    1.000),
            ("PSR J0740+6620",      2.08,  12400,   None),
            ("NS kanonisch",        1.40,  10000,   None),
            ("PSR J0030+0451",      1.34,  12700,   None),
            ("Sirius B",            1.02,  5800000, None),
            ("Sonne Oberfläche",    1.00,  696000000, None),
        ]

        for name, M_solar, R_m, x_override in objects:
            if x_override is not None:
                x = x_override
            else:
                rs = self.r_s(M_solar)
                x = R_m / rs

            # φ-Bracket bestimmen
            if x > 1.0:
                k_low = int(np.floor(np.log(x) / np.log(PHI)))
                k_bracket = f"[{k_low},{k_low+1}]"
            else:
                k_bracket = "[−1,0]"

            # Zeitdilatationen
            dg = d_gr(x) if x > 1.0 else 0.0
            da = d_ssz(xi_decay(x)) if x > 0 else 0.0

            if dg > 0:
                delta_pct = (da - dg) / dg * 100
                print(f"  {name:<23} {x:>10.3f} {k_bracket:>10} {dg:>8.5f} {da:>9.5f} {delta_pct:>+7.2f}%")
            else:
                print(f"  {name:<23} {x:>10.3f} {k_bracket:>10} {'0 (sing.)':>8} {da:>9.5f} {'N/A':>8}")

        print("="*70)
        print("\n  Erwartete starke Abweichungen bei NS (~10-14%): physikalische SSZ-Vorhersage")
        print("  Schwache Objekte (Sonne, Sirius B): SSZ ≈ GR — Schwachfeld-Konsistenz")


# =============================================================================
# MAIN: ALLE TESTS AUSFÜHREN
# =============================================================================

if __name__ == "__main__":
    print("\n" + "#"*70)
    print("# GR-SSZ INTERSECTION: φ-GITTER DISKRETISIERUNG")
    print("# Verifikation der Sätze 1-5")
    print("#"*70)

    print(f"\nKonstanten:")
    print(f"  φ        = {PHI:.15f}")
    print(f"  exp(-φ)  = {np.exp(-PHI):.15f}")
    print(f"  Xi_max   = {XI_MAX:.15f}")
    print(f"  D_min    = {1/(2-np.exp(-PHI)):.15f}")
    print(f"  φ + e⁻¹  = {PHI + np.exp(-1):.15f} < 2  [Satz-5-Bedingung A]")
    print(f"  φ + e⁻ᵠ² = {PHI + np.exp(-PHI**2):.15f} < 2  [Satz-5-Bedingung B]")

    t1 = TestSatz1_DGR_Phi()
    t1.test_dgr_at_phi()
    t1.test_recursion_satz2()

    TestSatz3_Decay_Recursion().test_recursion_decay()
    TestSatz4_Satur_Recursion().test_recursion_satur()

    t5 = TestSatz5_BracketTheorem()
    t5.test_delta_sign_decay()
    t5.test_delta_sign_satur()
    t5.test_intersection_points()

    TestRealObjects().test_real_objects()

    print("\n" + "="*70)
    print("ALLE TESTS BESTANDEN ✓")
    print("="*70)
```

---

## 10. Zusammenfassung

### 10.1 Was diskretisiert wurde

`gr-ssz-match.md` beschreibt ein kontinuierliches Problem: Wo schneiden sich D_GR(x)
und D_SSZ(x)? Die φ-Gitter-Diskretisierung übersetzt dieses Problem in eine Folge
algebraischer Aussagen auf den Gitterpunkten x_k = φ^k:

| Schritt | Kontinuierlich | Diskret (φ-Gitter) |
|---------|---------------|---------------------|
| D_GR | sqrt(1-1/x) | sqrt(1-φ^{-k}) = 1/φ bei k=1 (exakt) |
| D_SSZ_A | 1/(2-exp(-φ/x)) | 1/(2-q_k), q_k = exp(-φ^{1-k}) |
| D_SSZ_B | 1/(2-exp(-φx)) | 1/(2-p_k), p_k = exp(-φ^{k+1}) |
| Schnittpunkt | löse f(x)=0 | Vorzeichenwechsel von Δ_k zwischen k=0 und k=1 |

### 10.2 Die fünf Sätze

| Satz | Aussage |
|------|---------|
| **Satz 1** | D_GR(φ) = 1/φ — exakter algebraischer Wert aus φ²=φ+1 |
| **Satz 2** | D²_GR Rekursion: a_{k+1} = (a_k + 1/φ)/φ, Fixpunkt a*=1 |
| **Satz 3** | Abkling-Rekursion: q_{k+1} = q_k^{1/φ} — geometrische Folge in log-Skala |
| **Satz 4** | Sättigungs-Rekursion: p_{k+1} = p_k^φ — algebraisch dual zu Satz 3 |
| **Satz 5** | Bracket-Theorem: Beide r* liegen in (φ⁰, φ¹). Bedingung: φ + e⁻¹ < 2 und φ + e^{-φ²} < 2 |

### 10.3 Physikalische Bedeutung der Testdaten

- **Neutronensterne** (x = 2–3): SSZ sagt 9–14% mehr Zeitdilatation als GR. Messbar mit NICER.
- **Schwachfeld** (x > 100): Differenz < 1%. Alle bisherigen Experimente konsistent.
- **GR-Singularität** (x = 1): SSZ-Regularisierung D=0.555 vs. GR-Singularität D=0.

### 10.4 Kreuzreferenzen

| Thema | Referenz |
|-------|---------|
| φ als Wachstumsfunktion | Kapitel 3 (Buch) |
| D_min = 0.555 Ableitungskette | Kapitel 1 (Buch) |
| Zwei-Regime-Struktur | Appendix B.2 (Buch) |
| gr-ssz-match Ausgangsdokument | `docs/gr-ssz-match.md` (segmented-calculation-suite) |
| Kanonische Randwerte | `DISCRETE_SSZ_STATE_FORMULATION_DE.md` (dieses Repo) |
| Implementierung | `SSZ_PHI_DISCRETIZATION.py` (E:\clone) |

---

© 2025–2026 Carmen Wrede & Lino Casu  
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
