# Diskrete SSZ-Zustandsformulierung: Kanonische technische Referenz

**Version:** 1.0
**Datum:** 2026-03-16
**Autoren:** Carmen Wrede & Lino Casu
**Status:** KANONISCH — Technische Referenz für die diskrete φ-Gitter-Formulierung

---

## Inhaltsverzeichnis

1. [Überblick und Konzept](#1-überblick-und-konzept)
2. [φ-Gitter und dimensionslose Koordinate](#2-φ-gitter-und-dimensionslose-koordinate)
3. [Diskreter SSZ-Zustandsvektor Y_k](#3-diskreter-ssz-zustandsvektor-y_k)
4. [Kanonische stückweise Regimeform](#4-kanonische-stückweise-regimeform)
5. [Natürliche Randwerte am Schwarzschild-Radius](#5-natürliche-randwerte-am-schwarzschild-radius)
6. [Schwachfeld-Rekursion](#6-schwachfeld-rekursion)
7. [Starkfeld-Rekursion](#7-starkfeld-rekursion)
8. [Konzeptioneller Kern](#8-konzeptioneller-kern)
9. [Implementierungsreferenz](#9-implementierungsreferenz)
10. [Kreuzreferenzen](#10-kreuzreferenzen)

---

## 1. Überblick und Konzept

Die diskrete SSZ-Formulierung beantwortet die Frage: *Was passiert mit den SSZ-Zustandsgrößen, wenn wir entlang des radialen φ-Gitters r_k = r_s · φ^k von Gitterpunkt zu Gitterpunkt schreiten?*

**Kernprinzip:** SSZ ist keine diskrete Raumzeittheorie. Das Feld Ξ(r) ist glatt und kontinuierlich für alle r > 0. Die Diskretheit liegt in drei Strukturen:

1. **φ-Segmentzählung**: N'(r) = 4·s(r) als Zustandsgröße, wobei N' = 4 in flacher Raumzeit.
2. **φ-Level-Klassifikation**: ν(r) = ln(1 + Ξ(r)) / ln(φ) — lokale logarithmische Klassifikation des Segmentierungszustands.
3. **φ-Gitter-Rekursion**: Exakte algebraische Rekursionsformeln auf dem Gitter x_k = φ^k.

Das kontinuierliche Feld Ξ(r) bleibt die primäre physikalische Größe. Die diskreten Rekursionen sind Konsequenzen der φ-Gitterstruktur, keine eigenständigen Axiome.

**Verhältnis zur kontinuierlichen Theorie:**

```
Kontinuierlich:   Ξ(r), D(r), s(r)  für alle r > 0
Diskret:          Y_k = Y(r_k)  auf dem Gitter r_k = r_s · φ^k
Zusammenhang:     Y_k = Auswertung der kontinuierlichen Felder an Stützpunkten
```

---

## 2. φ-Gitter und dimensionslose Koordinate

**Schwarzschild-Radius:**

```
r_s = 2GM / c²
```

**Dimensionslose Radialkoordinate:**

```
x = r / r_s
```

**φ-Gitter:**

```
x_k = φ^k       (k ∈ ℤ)

φ = (1 + √5) / 2 = 1.6180339887498948482...
```

**Gitterpunkte (Beispiele):**

| k | x_k = φ^k | r_k = r_s · x_k | Regime |
|---|-----------|-----------------|--------|
| −3 | 0.2361 | 0.236 r_s | g₂: Starkfeld |
| −2 | 0.3820 | 0.382 r_s | g₂: Starkfeld |
| −1 | 0.6180 | 0.618 r_s | g₂: Starkfeld |
| 0 | 1.0000 | 1.000 r_s | g₂: Starkfeld |
| 1 | 1.6180 | 1.618 r_s | g₂/Blend |
| 2 | 2.6180 | 2.618 r_s | g₁: Schwachfeld |
| 3 | 4.2361 | 4.236 r_s | g₁: Schwachfeld |

**φ-Gitter-Eigenschaften:**

```
x_{k+1} = φ · x_k          [Schritt nach außen]
x_{k+1} = x_k / φ          [Schritt nach innen]
x_{k+n} = φ^n · x_k        [n Schritte nach außen]
```

Da φ² = φ + 1 (Fibonacci-Identität), ist das φ-Gitter selbstähnlich: x_{k+2} = x_{k+1} + x_k.

---

## 3. Diskreter SSZ-Zustandsvektor Y_k

**Definition:**

Sei Ξ_k := Ξ(x_k) der Wert der SSZ-Segmentdichte am Gitterpunkt k. Der diskrete SSZ-Zustand am Gitterpunkt k ist:

```
Y_k := (Ξ_k,  s_k,  D_k,  N'_k,  ν_k)
```

mit:

```
Ξ_k   =  Ξ(x_k)                          [Segmentdichte]
s_k   =  1 + Ξ_k                          [Skalierungsfaktor]
D_k   =  1 / (1 + Ξ_k)                    [Zeitdilatation]
N'_k  =  4 · (1 + Ξ_k)                    [effektive Segmentzahl]
ν_k   =  ln(1 + Ξ_k) / ln(φ)             [lokales φ-Level]
```

**Zustandsumrechnungen (vollständig):**

Aus Ξ:
```
s    = 1 + Ξ
D    = 1 / (1 + Ξ)
N'   = 4 · (1 + Ξ)
ν    = ln(1 + Ξ) / ln(φ)
```

Aus D:
```
Ξ    = 1/D - 1
s    = 1/D
N'   = 4/D
ν    = ln(1/D) / ln(φ)
```

Aus ν:
```
s    = φ^ν
Ξ    = φ^ν - 1
D    = φ^{-ν}
N'   = 4 · φ^ν
```

Aus s:
```
Ξ    = s - 1
D    = 1/s
N'   = 4s
ν    = ln(s) / ln(φ)
```

**Satz (Zustandsäquivalenz):** Jede der fünf Komponenten von Y_k bestimmt die übrigen vier eindeutig. Insbesondere gilt: D_k = φ^{−ν_k} und N'_k = 4φ^{ν_k}.

**Physikalische Bedeutung:**

| Komponente | Physikalische Rolle | Grenzwert (r → ∞) | Wert bei r = r_s |
|-----------|---------------------|--------------------|------------------|
| Ξ_k | Lokale Raumzeit-Segmentierung (Primärfeld) | 0 | 0.8017 |
| s_k | Lokale Zeitstreckung; s=1/D | 1 | 1.8017 |
| D_k | Lokale Zeit / Koordinatenzeit | 1 | 0.5550 |
| N'_k | Effektive Segmente pro Wellenperiode | 4 | 7.207 |
| ν_k | Logarithmischer φ-Segmentierungszustand | 0 | ≈ 1.22 |

---

## 4. Kanonische stückweise Regimeform

```
            1 / (2 x_k)                            x_k > 2.2     [g₁: Schwachfeld]
Ξ_k  :=    Ξ_blend(x_k)                            1.8 ≤ x_k ≤ 2.2   [C²-Übergang]
            min(1 - exp(-φ · x_k),  Ξ_max)         x_k < 1.8     [g₂: Starkfeld]
```

mit:

```
Ξ_max = 1 - exp(-φ) ≈ 0.801711847
```

**Blendzone:** Quintische Hermite-C²-Interpolation zwischen g₁ und g₂. Matchet Wert, erste und zweite Ableitung an beiden Rändern (x = 1.8 und x = 2.2). Normierter Parameter t = (x - 1.8) / 0.4 ∈ [0,1].

**Kanonische Starkfeldform — Sättigungsform:**

```
Ξ_g2(x) = 1 - exp(-φ · x)    mit x = r/r_s
```

Eigenschaften:
- Ξ(0) = 0 — singularitätsfrei
- Ξ(r_s) = 1 - exp(-φ) = Ξ_max ≈ 0.8017
- Monoton steigend für x > 0

**Hinweis:** Die Abklingform `1 - exp(-φ r_s/r)` ist komplementär/historisch. Die operative kanonische Form für alle Rekursionen in diesem Dokument ist die Sättigungsform.

---

## 5. Natürliche Randwerte am Schwarzschild-Radius

Am Schwarzschild-Radius (x = 1, k = 0):

```
Ξ_*  =  1 - exp(-φ)              =  0.801711847...
s_*  =  2 - exp(-φ)              =  1.801711847...
D_*  =  1 / (2 - exp(-φ))        =  0.555027710...
N'_* =  4 · (2 - exp(-φ))        =  7.206847389...
ν_*  =  ln(2 - exp(-φ)) / ln(φ)  ≈  1.2248...  ≈ 1.22
```

**Vollständige Tabelle:**

| Größe | Symbol | Exakter Ausdruck | Numerischer Wert |
|-------|--------|-----------------|------------------|
| Segmentdichte | Ξ_* | 1 − exp(−φ) | 0.801711847 |
| Skalierungsfaktor | s_* | 2 − exp(−φ) | 1.801711847 |
| Zeitdilatation | D_* | [2 − exp(−φ)]⁻¹ | 0.555027710 |
| Segmentzahl | N'_* | 4 · [2 − exp(−φ)] | 7.206847389 |
| φ-Level | ν_* | ln[2 − exp(−φ)] / ln(φ) | ≈ 1.22 |

**Äquivalenzfamilie:** Die Werte sind nicht unabhängig. Es gilt:

```
0.555 ↔ 0.802 ↔ 1.802 ↔ 7.207 ↔ 1.22
```

Jeder Wert bestimmt die anderen eindeutig. Insbesondere ist D(r_s) = 0.555 kein freier Parameter, sondern eine direkte Konsequenz von φ.

**Herleitung von Ξ_* = 1 - exp(-φ):**

```
Ξ_* = Ξ_g2(x=1) = 1 - exp(-φ · 1) = 1 - exp(-φ) = 1 - e^{-1.6180...}
    = 1 - 0.19829...
    = 0.80171...
```

**Herleitung von D_*:**

```
D_* = 1 / (1 + Ξ_*) = 1 / (1 + (1 - exp(-φ))) = 1 / (2 - exp(-φ))
    = 1 / (2 - 0.19829...)
    = 1 / 1.80171...
    = 0.55503...
```

**Herleitung von ν_*:**

```
ν_* = ln(s_*) / ln(φ)
    = ln(1.80171...) / ln(1.61803...)
    = 0.58943... / 0.48121...
    = 1.2248...
```

---

## 6. Schwachfeld-Rekursion

**Ausgangspunkt:** Schwachfeld-Formel Ξ_g1(x) = 1/(2x), φ-Gitter x_{k+1} = φ x_k.

**Rekursionsformeln:**

```
Ξ_{k+1} = Ξ_k / φ          [Schritt nach außen, x_{k+1} = φ x_k]
Ξ_{k+1} = φ · Ξ_k          [Schritt nach innen, x_{k+1} = x_k/φ]
```

**Vollständige Herleitung (nach außen):**

```
Ξ_{k+1} = 1 / (2 · x_{k+1})
         = 1 / (2 · φ · x_k)         [da x_{k+1} = φ · x_k]
         = (1 / (2 x_k)) · (1/φ)
         = Ξ_k · (1/φ)
         = Ξ_k / φ
```

**Vollständige Herleitung (nach innen):**

```
Ξ_{k+1} = 1 / (2 · x_{k+1})
         = 1 / (2 · x_k/φ)           [da x_{k+1} = x_k/φ]
         = (1 / (2 x_k)) · φ
         = Ξ_k · φ
```

**Mehrfachschritte:**

```
Ξ_{k+n} = Ξ_k / φ^n      [n Schritte nach außen]
Ξ_{k+n} = Ξ_k · φ^n      [n Schritte nach innen]
```

**Vollständige Zustandsrekursion (nach außen):**

```
Ξ_{k+1} = Ξ_k / φ
s_{k+1} = 1 + Ξ_k/φ
D_{k+1} = 1 / (1 + Ξ_k/φ)
N'_{k+1} = 4 · (1 + Ξ_k/φ)
ν_{k+1} = ln(1 + Ξ_k/φ) / ln(φ)
```

**Interpretation:** Da 1/φ ≈ 0.618, reduziert jeder Schritt nach außen die Segmentdichte um den Faktor des Goldenen Schnitts. Die Schwachfeld-Rekursion ist eine geometrische Folge: Ξ_k = Ξ_0 / φ^k — die Fibonacci-Selbstähnlichkeit in der radialen Segmentdichteverteilung.

**Beispieltabelle (Ausgang bei x=1, Schwachfeld-Näherung):**

| k | x_k | Ξ_k (Schwachfeld) | D_k | N'_k |
|---|-----|-------------------|-----|------|
| 0 | 1.000 | 0.500 | 0.667 | 6.000 |
| 1 | 1.618 | 0.309 | 0.764 | 5.236 |
| 2 | 2.618 | 0.191 | 0.840 | 4.764 |
| 3 | 4.236 | 0.118 | 0.895 | 4.472 |
| 4 | 6.854 | 0.073 | 0.932 | 4.292 |

*(Hinweis: Für x < 2.2 gilt die kanonische Starkfeld- oder Blendformel; Schwachfeldwerte hier zur Illustration der Rekursion.)*

---

## 7. Starkfeld-Rekursion

**Ausgangspunkt:** Kanonische Sättigungsform Ξ_g2(x) = 1 - exp(-φx), φ-Gitter x_{k+1} = φ x_k.

**Rekursionsformeln:**

```
Ξ_{k+1} = 1 - (1 - Ξ_k)^φ          [Schritt nach außen, x_{k+1} = φ x_k]
Ξ_{k+1} = 1 - (1 - Ξ_k)^{1/φ}      [Schritt nach innen, x_{k+1} = x_k/φ]
```

**Vollständige Herleitung (nach außen):**

Da Ξ_k = 1 - exp(-φ x_k), gilt zuerst:

```
1 - Ξ_k = exp(-φ · x_k)
```

Mit x_{k+1} = φ · x_k:

```
Ξ_{k+1} = 1 - exp(-φ · x_{k+1})
         = 1 - exp(-φ · φ · x_k)
         = 1 - exp(-φ² · x_k)
```

Jetzt nutzen wir die Potenzregel exp(-φ² x) = (exp(-φx))^φ:

```
         = 1 - [exp(-φ · x_k)]^φ
         = 1 - (1 - Ξ_k)^φ
```

**Vollständige Herleitung (nach innen):**

Mit x_{k+1} = x_k/φ:

```
Ξ_{k+1} = 1 - exp(-φ · x_{k+1})
         = 1 - exp(-φ · x_k/φ)
         = 1 - exp(-x_k)
```

Jetzt schreiben wir exp(-x_k) = exp(-φ · x_k / φ) und nutzen:

```
exp(-x_k) = [exp(-φ · x_k)]^{1/φ}     [denn: -x_k = (-φ x_k) · (1/φ)]
```

Also:

```
Ξ_{k+1} = 1 - [exp(-φ · x_k)]^{1/φ}
         = 1 - (1 - Ξ_k)^{1/φ}
```

Da 1/φ = φ - 1, gilt alternativ: Ξ_{k+1} = 1 - (1 - Ξ_k)^{φ-1}.

**Operative Form mit Sättigungsbegrenzung:**

```
Ξ_{k+1}^{phys} = min(1 - (1 - Ξ_k)^φ,    Ξ_max)   [nach außen]
Ξ_{k+1}^{phys} = min(1 - (1 - Ξ_k)^{1/φ}, Ξ_max)  [nach innen]
```

**Algebraische Linearisierung:**

Die Substitution q_k = 1 - Ξ_k = exp(-φ x_k) ergibt die linearisierte Form:

```
q_{k+1} = q_k^φ          [nach außen]
q_{k+1} = q_k^{1/φ}      [nach innen]
```

Das ist eine geometrische Folge in logarithmischem Maßstab: ln(q_k) = -φ x_k · ln(e) = -φ^k · x_0.

**Beispieltabelle (Starkfeld, Ausgang bei x=1):**

| k | x_k | Ξ_k | s_k | D_k | N'_k | ν_k |
|---|-----|-----|-----|-----|------|-----|
| −2 | 0.382 | 0.4559 | 1.4559 | 0.6868 | 5.824 | 0.793 |
| −1 | 0.618 | 0.6329 | 1.6329 | 0.6124 | 6.532 | 1.011 |
| 0 | 1.000 | 0.8017 | 1.8017 | 0.5550 | 7.207 | 1.225 |
| 1 | 1.618 | 0.9286 | 1.9286 | 0.5185 | 7.714 | 1.404 |

*(k=2: x=2.618 > 2.2, liegt im Blendübergang/Schwachfeld)*

---

## 8. Konzeptioneller Kern

### SSZ ist kontinuierlich — die Diskretheit ist strukturell

Das φ-Level ν_k = ln(1 + Ξ_k)/ln(φ) ist eine **lokale Klassifikationsgröße**, keine dynamische Feldgröße. Konkret:

- ν_k klassifiziert den *momentanen* Segmentierungszustand eines Beobachters.
- Der *kumulative* Segmentzähler entlang einer langen radialen Bahn kann unbeschränkt wachsen.
- Die *lokale* Segmentdichte Ξ ist durch Ξ_max ≤ 1 beschränkt (Sättigung).

Diese Trennung — lokal beschränktes φ-Level, unbeschränkter kumulativer Zähler — ist die physikalische Grundlage dafür, dass SSZ keine Singularitäten erzeugt: Das Feld sättigt bei Ξ_max, anstatt zu divergieren.

### Beide Rekursionen sind selbstähnlich

```
Schwachfeld:  Ξ_{k+1} = Ξ_k / φ          → geometrische Folge in Ξ
Starkfeld:    q_{k+1} = q_k^φ              → geometrische Folge in ln(q)
```

Beide haben dieselbe algebraische Struktur in ihren natürlichen Variablen. Das ist keine Zufälligkeit, sondern eine direkte Konsequenz der logarithmischen Spirale, die das φ-Gitter erzeugt: Die Spirale reproduziert sich bei jeder Umdrehung selbst — die Rekursion reproduziert sich bei jedem Gitterschritt.

### Das φ-Level als gemeinsame Skala

Das φ-Level ν vereint beide Regime auf einer einheitlichen Skala:

```
ν → 0          (flache Raumzeit, r → ∞)
ν_* ≈ 1.22     (am Schwarzschild-Radius, r = r_s)
```

Mit D_k = φ^{-ν_k} gilt: Jeder Schritt nach außen verringert ν_k, jeder Schritt nach innen erhöht ν_k. Der Schwarzschild-Radius entspricht dem φ-Level ν = ln(2-e^{-φ})/ln(φ) ≈ 1.22 — einem natürlichen, parameterlosen Wert.

---

## 9. Implementierungsreferenz

```python
import numpy as np

PHI = (1 + np.sqrt(5)) / 2       # 1.6180339887498948482...
XI_MAX = 1 - np.exp(-PHI)        # 0.801711847...

def xi_weak(x):
    """Schwachfeld: Ξ = 1/(2x), gültig für x > 2.2"""
    return 1.0 / (2.0 * x)

def xi_strong(x):
    """Starkfeld (Sättigungsform): Ξ = min(1-exp(-φx), Ξ_max), gültig für x < 1.8"""
    return min(1.0 - np.exp(-PHI * x), XI_MAX)

def ssz_state(xi):
    """Vollständiger SSZ-Zustand aus Ξ"""
    s   = 1.0 + xi
    D   = 1.0 / s
    Np  = 4.0 * s
    nu  = np.log(s) / np.log(PHI)
    return {'Xi': xi, 's': s, 'D': D, "N'": Np, 'nu': nu}

def recursion_weak_outward(xi_k):
    """Schwachfeld-Rekursion: Schritt nach außen (x → φx)"""
    return xi_k / PHI

def recursion_weak_inward(xi_k):
    """Schwachfeld-Rekursion: Schritt nach innen (x → x/φ)"""
    return xi_k * PHI

def recursion_strong_outward(xi_k):
    """Starkfeld-Rekursion: Schritt nach außen (x → φx)"""
    xi_next = 1.0 - (1.0 - xi_k) ** PHI
    return min(xi_next, XI_MAX)

def recursion_strong_inward(xi_k):
    """Starkfeld-Rekursion: Schritt nach innen (x → x/φ)"""
    xi_next = 1.0 - (1.0 - xi_k) ** (1.0 / PHI)
    return min(xi_next, XI_MAX)

# Randwerte bei x = 1 (Schwarzschild-Radius):
boundary_state = ssz_state(XI_MAX)
# boundary_state = {'Xi': 0.8017, 's': 1.8017, 'D': 0.5550, "N'": 7.2068, 'nu': 1.22}
```

**Vollständige Implementierung:** `E:\clone\SSZ_PHI_DISCRETIZATION.py`

---

## 10. Kreuzreferenzen

### Buch-Referenzen (E:\clone\SSZ_BOOK_PROJECT)

| Abschnitt | Inhalt |
|-----------|--------|
| Kapitel 4.6 | Vollständige Herleitungen (Sätze 4.4–4.7, Korollare 4.2–4.6) |
| Appendix B.10 | Kanonische Kurzform mit Kreuzreferenz-Tabelle |
| Kapitel 1 | SSZ-Überblick, D_min = 0.555-Ableitung |
| Kapitel 3 | φ als Wachstumsfunktion, r_φ |
| Kapitel 4.1–4.5 | Logarithmische Spirale, Euler-Einbettung, N₀=4 |
| Kapitel 16 | Frequenzrahmen, N₀=4, Segment-Quantisierung |

### Technische Referenzen

| Dokument | Inhalt |
|----------|--------|
| `SSZ_MATHEMATICAL_PHYSICS_DE.md` (dieses Repo) | Mathematische Grundlagen, Ξ-Definitionen |
| `SSZ_FORMULA_DOCUMENTATION_DE.md` (dieses Repo) | Regime-Formeln, Implementierung |
| `SSZ_MATHEMATICAL_PHYSICS.md` (EN) | Englische Entsprechung |
| `DISCRETE_SSZ_STATE_FORMULATION.md` (EN) | Englische Entsprechung dieses Dokuments |

### Formel-Kreuzreferenz

| Formel | Appendix B | Kapitel |
|--------|-----------|---------|
| Ξ_weak = 1/(2x) | B.1.1 | 1, 4.6.3 |
| Ξ_strong = 1-exp(-φx) | B.1.1, B.10.2 | 4.6.3 |
| D = 1/(1+Ξ) | B.1.2 | 1, 4.6.2 |
| s = 1+Ξ | B.1.5 | 4.6.2 |
| Hermite-C² Blend | B.2.2 | 4.6.3 |
| Ξ(r_s) = 0.802 | B.7.1 | 4.6.4 |
| D(r_s) = 0.555 | B.7.1 | 4.6.4 |
| φ-Rekursion (Schwachfeld) | B.10.4 | 4.6.5 |
| φ-Rekursion (Starkfeld) | B.10.5 | 4.6.6 |
| Y_k = (Ξ,s,D,N',ν) | B.10.1 | 4.6.2 |

---

© 2025–2026 Carmen Wrede & Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
