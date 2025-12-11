# SSZ-Qubits: Segmented Spacetime Framework for Quantum Computing

[![License: ACSL](https://img.shields.io/badge/License-Anti--Capitalist-red.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Tests: 74/74](https://img.shields.io/badge/Tests-74%2F74%20Passed-brightgreen.svg)](tests/)

---

## Inhaltsverzeichnis

1. [Ueberblick](#ueberblick)
2. [Das Problem](#das-problem)
3. [Die SSZ-Loesung](#die-ssz-loesung)
4. [Theoretische Grundlagen](#theoretische-grundlagen)
5. [Installation](#installation)
6. [Schnellstart](#schnellstart)
7. [API-Referenz](#api-referenz)
8. [Anwendungsbeispiele](#anwendungsbeispiele)
9. [Test-Suite](#test-suite)
10. [Visualisierungen](#visualisierungen)
11. [Physikalische Ergebnisse](#physikalische-ergebnisse)
12. [Experimentelle Validierung](#experimentelle-validierung)
13. [Projektstruktur](#projektstruktur)
14. [FAQ](#faq)
15. [Referenzen](#referenzen)
16. [Autoren & Lizenz](#autoren--lizenz)

---

## Ueberblick

**SSZ-Qubits** wendet das Segmented Spacetime (SSZ) Framework auf Quantencomputing an. Es bietet Werkzeuge zur Analyse und Minimierung gravitativer Effekte auf Qubit-Systeme.

> **"Die Qubits leben nicht nur im Raum, sondern auch in Segmenten der Raumzeit."**

### Was ist SSZ?

SSZ (Segmented Spacetime / Segmentierte Raumzeit) ist ein theoretisches Framework, das Raumzeit als **diskrete Struktur** behandelt, anstatt als kontinuierliches Gebilde wie in der klassischen Allgemeinen Relativitaetstheorie (ART).

### Warum ist das fuer Qubits relevant?

Qubits sind extrem empfindlich gegenueber:
- Zeitdilatation durch Gravitationsfelder
- Phasenverschiebungen durch Hoehendifferenzen
- Decoherence durch Segment-Mismatch

SSZ quantifiziert diese Effekte und ermoeglicht deren Kompensation.

---

## Das Problem

### Klassische Qubit-Probleme

| Problem | Beschreibung | Auswirkung |
|---------|--------------|------------|
| **Decoherence** | Verlust der Quantenkohaerenz | Fehler in Berechnungen |
| **Timing-Fehler** | Asynchrone Gate-Operationen | Falsche Ergebnisse |
| **Raeumlicher Drift** | Positionsabhaengige Phasenfehler | Unvorhersagbare Fehler |
| **Gravitationsgradienten** | Hoehenabhaengige Zeitdilatation | Systematische Fehler |

### Das uebersehene Problem

**Selbst Mikrometer-Hoehendifferenzen zwischen Qubits fuehren zu messbaren Effekten!**

```
1 um Hoehendifferenz -> Delta Xi ~ 10^-22
1 mm Hoehendifferenz -> Delta Xi ~ 10^-19 -> ~0.01 ps/s Desynchronisation
```

Diese Effekte werden in der klassischen Qubit-Physik oft als "Hardware-Drift" oder "unerklärliche Decoherence" abgetan.

---

## Die SSZ-Loesung

SSZ bietet ein geometrisches Framework mit:

### 1. Segment Density Xi(r)
Quantifiziert die lokale Raumzeit-Struktur:
```
Xi(r) = r_s / (2r)
```
wobei r_s der Schwarzschild-Radius ist.

### 2. SSZ Time Dilation D_SSZ
Bestimmt lokale Uhrenraten:
```
D_SSZ = 1 / (1 + Xi)
```

### 3. Segment-Kohaerente Zonen
Definiert optimale Qubit-Platzierungsbereiche, in denen Xi-Variation minimal ist.

### 4. Geometry-Aware QEC
Ermoeglicht gravitationsbewusste Fehlerkorrektur.

### 5. Golden Ratio phi
Steuert die Segment-Saettigung in starken Feldern:
```
phi = (1 + sqrt(5)) / 2 = 1.618033988749895
```

---

## Theoretische Grundlagen

### Zwei SSZ-Regime

SSZ unterscheidet zwei Regime basierend auf der Feldstaerke:

#### Weak Field (r/r_s > 100) - Anwendbar auf der Erde

```
Xi(r) = r_s / (2r)
dXi/dr = -r_s / (2r^2)
D_SSZ = 1 / (1 + Xi) ≈ 1 - Xi + O(Xi^2)
```

**Beispiel Erde:**
- r_s = 8.87 mm
- r = 6.371e6 m (Erdradius)
- Xi = 6.96e-10
- D_SSZ = 0.999999999303892

#### Strong Field (r/r_s < 100) - Nahe Schwarzen Loechern

```
Xi(r) = 1 - exp(-phi * r / r_s)
dXi/dr = (phi / r_s) * exp(-phi * r / r_s)
```

**Wichtig:** Im Strong Field bleibt D_SSZ **finite** am Horizont (D_SSZ ≈ 0.555), waehrend die ART eine Singularitaet vorhersagt.

### Fundamentale Konstanten

| Konstante | Symbol | Wert | Einheit |
|-----------|--------|------|---------|
| Lichtgeschwindigkeit | c | 299792458 | m/s |
| Gravitationskonstante | G | 6.67430e-11 | m³/(kg·s²) |
| Planck-Konstante | ℏ | 1.054571817e-34 | J·s |
| Golden Ratio | φ | 1.6180339887498948 | - |
| Erdmasse | M_E | 5.972e24 | kg |
| Erdradius | R_E | 6.371e6 | m |

### Schwarzschild-Radius

```
r_s = 2GM / c²
```

| Objekt | Schwarzschild-Radius |
|--------|---------------------|
| Erde | 8.87 mm |
| Sonne | 2.95 km |
| Sagittarius A* | 12 Mio km |

---

## Installation

### Voraussetzungen

- Python 3.8 oder hoeher
- pip (Python Package Manager)

### Installation

```bash
# Repository klonen
git clone https://github.com/error-wtf/ssz-qubits.git
cd ssz-qubits

# Abhaengigkeiten installieren
pip install -r requirements.txt

# Installation verifizieren
python -c "from ssz_qubits import *; print('SSZ-Qubits erfolgreich installiert!')"
```

### Abhaengigkeiten

```
numpy>=1.20.0
pytest>=7.0.0
matplotlib>=3.5.0
```

### Tests ausfuehren

```bash
# Alle Tests
python run_tests.py

# Oder mit pytest
pytest tests/ -v
```

Erwartete Ausgabe:
```
============================= 74 passed in 0.54s ==============================
```

---

## Schnellstart

### Minimales Beispiel

```python
from ssz_qubits import Qubit, QubitPair, analyze_qubit_segment, qubit_pair_segment_mismatch

# Qubit auf Meereshoehe erstellen
q1 = Qubit(id="Q1", x=0, y=0, z=0)

# Qubit 1 cm hoeher erstellen
q2 = Qubit(id="Q2", x=0, y=0, z=0.01)

# Einzelnes Qubit analysieren
analysis = analyze_qubit_segment(q1)
print(f"Xi = {analysis.xi:.6e}")
print(f"D_SSZ = {analysis.time_dilation:.15f}")

# Qubit-Paar analysieren
pair = QubitPair(q1, q2)
mismatch = qubit_pair_segment_mismatch(pair)
print(f"Delta Xi = {mismatch['delta_xi']:.6e}")
```

### Interaktive Demo

```bash
python demo.py
```

Die Demo zeigt 9 verschiedene Anwendungsfaelle:
1. Basic SSZ Physics
2. Single Qubit Analysis
3. Qubit Pair Mismatch
4. Coherent Zones
5. Array Optimization
6. Gate Timing Corrections
7. Decoherence Analysis
8. Experimental Validation
9. Practical System Design

---

## API-Referenz

### Konstanten

```python
from ssz_qubits import C, G, HBAR, M_EARTH, R_EARTH, PHI

C        # Lichtgeschwindigkeit [m/s]
G        # Gravitationskonstante [m³/(kg·s²)]
HBAR     # Reduzierte Planck-Konstante [J·s]
M_EARTH  # Erdmasse [kg]
R_EARTH  # Erdradius [m]
PHI      # Golden Ratio
```

### Kernfunktionen

#### `schwarzschild_radius(M)`
Berechnet den Schwarzschild-Radius.
```python
r_s = schwarzschild_radius(M_EARTH)  # 8.87e-3 m
```

#### `xi_segment_density(r, M, regime='auto')`
Berechnet die Segment Density Xi.
```python
xi = xi_segment_density(R_EARTH, M_EARTH)  # 6.96e-10
xi = xi_segment_density(r, M, regime='weak')   # Erzwingt Weak Field
xi = xi_segment_density(r, M, regime='strong') # Erzwingt Strong Field
```

#### `xi_gradient(r, M, regime='auto')`
Berechnet den Gradienten dXi/dr.
```python
grad = xi_gradient(R_EARTH, M_EARTH)  # -1.09e-16 /m
```

#### `ssz_time_dilation(r, M)`
Berechnet die SSZ-Zeitdilatation D_SSZ.
```python
d = ssz_time_dilation(R_EARTH, M_EARTH)  # 0.999999999303892
```

### Qubit-Klassen

#### `Qubit`
```python
from ssz_qubits import Qubit

q = Qubit(
    id="Q1",              # Eindeutige ID
    x=0,                  # X-Position [m]
    y=0,                  # Y-Position [m]
    z=0,                  # Hoehe ueber Referenz [m]
    coherence_time_T2=100e-6,  # T2-Zeit [s] (Standard: 100 us)
    gate_time=50e-9       # Gate-Zeit [s] (Standard: 50 ns)
)

# Eigenschaften
q.radius_from_earth_center  # Abstand vom Erdmittelpunkt
```

#### `QubitPair`
```python
from ssz_qubits import QubitPair

pair = QubitPair(q1, q2)

# Eigenschaften
pair.separation          # Raeumliche Trennung [m]
pair.height_difference   # Hoehendifferenz [m]
```

### Analyse-Funktionen

#### `analyze_qubit_segment(qubit, M)`
```python
analysis = analyze_qubit_segment(q, M_EARTH)
# Rueckgabe: SegmentAnalysis mit:
#   .xi              - Segment Density
#   .gradient        - dXi/dr
#   .time_dilation   - D_SSZ
#   .radius          - Abstand vom Zentrum
```

#### `qubit_pair_segment_mismatch(pair, M)`
```python
mismatch = qubit_pair_segment_mismatch(pair, M_EARTH)
# Rueckgabe: Dict mit:
#   'delta_xi'              - Xi-Differenz
#   'delta_time_dilation'   - D_SSZ-Differenz
#   'phase_drift_per_gate'  - Phasendrift pro Gate
#   'decoherence_enhancement' - Decoherence-Faktor
```

#### `segment_coherent_zone(center_height, max_xi_variation, M)`
```python
h_min, h_max = segment_coherent_zone(0, 1e-18, M_EARTH)
# Rueckgabe: Tuple (min_hoehe, max_hoehe) in Metern
```

#### `optimize_qubit_array(n, base_height, max_separation)`
```python
qubits = optimize_qubit_array(16, base_height=0, max_separation=1e-3)
# Rueckgabe: Liste von n optimiert platzierten Qubits
```

#### `array_segment_uniformity(qubits, M)`
```python
uniformity = array_segment_uniformity(qubits, M_EARTH)
# Rueckgabe: Dict mit:
#   'xi_mean'      - Mittleres Xi
#   'xi_std'       - Standardabweichung
#   'xi_min'       - Minimum
#   'xi_max'       - Maximum
#   'xi_range'     - Spannweite
#   'uniformity'   - Uniformitaets-Score (0-1)
```

### Gate-Timing-Funktionen

#### `gate_timing_correction(qubit, M)`
```python
correction = gate_timing_correction(q, M_EARTH)
# Rueckgabe: Korrekturfaktor fuer Gate-Zeit
```

#### `two_qubit_gate_timing(pair, M)`
```python
timing = two_qubit_gate_timing(pair, M_EARTH)
# Rueckgabe: Dict mit:
#   'optimal_gate_time'  - Optimale Gate-Dauer
#   'timing_asymmetry'   - Benoetigte Timing-Asymmetrie
#   'max_fidelity_loss'  - Maximaler Fidelity-Verlust
#   'd_qubit_a'          - D_SSZ fuer Qubit A
#   'd_qubit_b'          - D_SSZ fuer Qubit B
```

### Decoherence-Funktionen

#### `ssz_decoherence_rate(qubit, M)`
```python
gamma = ssz_decoherence_rate(q, M_EARTH)
# Rueckgabe: SSZ-bedingte Decoherence-Rate [1/s]
```

#### `effective_T2(qubit, M)`
```python
T2_eff = effective_T2(q, M_EARTH)
# Rueckgabe: Effektive T2-Zeit unter SSZ-Einfluss [s]
```

#### `pair_decoherence_time(pair, M)`
```python
T2_pair = pair_decoherence_time(pair, M_EARTH)
# Rueckgabe: Paar-Decoherence-Zeit [s]
```

---

## Anwendungsbeispiele

### 1. Qubit-Platzierungsoptimierung

**Problem:** Minimiere SSZ-Mismatch zwischen Qubits in einem Array.

```python
from ssz_qubits import optimize_qubit_array, array_segment_uniformity, M_EARTH

# 100-Qubit-Array optimieren
qubits = optimize_qubit_array(100, base_height=0, max_separation=5e-3)

# Uniformitaet pruefen
uniformity = array_segment_uniformity(qubits, M_EARTH)
print(f"Xi-Uniformitaet: {uniformity['uniformity']:.6f}")
print(f"Xi-Spannweite: {uniformity['xi_range']:.6e}")
```

### 2. Kohaerente Zone finden

**Problem:** Finde den Hoehenbereich, in dem Xi-Variation unter einer Toleranz bleibt.

```python
from ssz_qubits import segment_coherent_zone, M_EARTH

# Zone mit Toleranz 10^-18 finden
h_min, h_max = segment_coherent_zone(0, 1e-18, M_EARTH)
print(f"Kohaerente Zone: {h_min*1e6:.1f} um bis {h_max*1e6:.1f} um")
print(f"Zonenbreite: {(h_max-h_min)*1e6:.1f} um")
```

### 3. Gate-Timing korrigieren

**Problem:** Kompensiere Zeitdilatation bei Zwei-Qubit-Gates.

```python
from ssz_qubits import Qubit, QubitPair, two_qubit_gate_timing, M_EARTH

q1 = Qubit(id="Q1", x=0, y=0, z=0, gate_time=50e-9)
q2 = Qubit(id="Q2", x=0, y=0, z=10e-3, gate_time=50e-9)  # 10 mm hoeher
pair = QubitPair(q1, q2)

timing = two_qubit_gate_timing(pair, M_EARTH)
print(f"Optimale Gate-Zeit: {timing['optimal_gate_time']*1e9:.6f} ns")
print(f"Timing-Asymmetrie: {timing['timing_asymmetry']:.6e}")
```

### 4. Decoherence analysieren

**Problem:** Bestimme den SSZ-Beitrag zur Decoherence.

```python
from ssz_qubits import Qubit, ssz_decoherence_rate, effective_T2, M_EARTH

q = Qubit(id="Q1", x=0, y=0, z=0, coherence_time_T2=100e-6)

gamma = ssz_decoherence_rate(q, M_EARTH)
T2_eff = effective_T2(q, M_EARTH)

print(f"Intrinsische T2: {q.coherence_time_T2*1e6:.1f} us")
print(f"Effektive T2: {T2_eff*1e6:.3f} us")
print(f"SSZ-Beitrag: {(1 - T2_eff/q.coherence_time_T2)*100:.2f}%")
```

### 5. Quantenkommunikation synchronisieren

**Problem:** Berechne Zeitdrift zwischen entfernten Qubits.

```python
from ssz_qubits import Qubit, ssz_time_dilation, R_EARTH, M_EARTH

# Zwei Stationen mit 100 m Hoehendifferenz
h1 = 0       # Meereshoehe
h2 = 100     # 100 m hoeher

d1 = ssz_time_dilation(R_EARTH + h1, M_EARTH)
d2 = ssz_time_dilation(R_EARTH + h2, M_EARTH)

delta_d = d2 - d1
drift_per_hour = delta_d * 3600 * 1e9  # ns/Stunde

print(f"Zeitdrift: {drift_per_hour:.3f} ns/Stunde")
```

---

## Test-Suite

### Uebersicht

| Kategorie | Tests | Beschreibung |
|-----------|-------|--------------|
| Physics | 17 | Physikalische Formeln |
| Edge Cases | 25 | Extreme Werte, Fehlerbehandlung |
| Validation | 17 | Experimentelle Validierung |
| Applications | 15 | Praktische Anwendungen |
| **Gesamt** | **74** | |

### Tests ausfuehren

```bash
# Alle Tests mit detaillierter Ausgabe
python run_tests.py

# Einzelne Test-Datei
pytest tests/test_ssz_physics.py -v

# Mit pytest (schneller)
pytest tests/ -v --tb=short
```

### Test-Kategorien

#### Physics Tests (`test_ssz_physics.py`)
- Schwarzschild-Radius Validierung
- Segment Density Berechnungen
- Zeitdilatation Verifikation
- Gradient-Konsistenz
- Physikalische Grenzen
- Golden Ratio Eigenschaften
- Strong Field Verhalten

#### Edge Cases (`test_edge_cases.py`)
- Extreme Radien (nahe r_s bis 1 AU)
- Extreme Massen (0 bis Schwarze Loecher)
- Ungewoehnliche Qubit-Konfigurationen
- Numerische Praezision
- Fehlerbehandlung
- Spezielle Qubit-Eigenschaften
- QEC Edge Cases

#### Validation (`test_validation.py`)
- GR Weak-Field Vergleich
- GPS-Satellit Zeitdilatation
- Pound-Rebka Experiment
- NIST Optische Uhr
- Tokyo Skytree Experiment
- Theoretische Konsistenz
- Dimensionsanalyse

#### Qubit Applications (`test_ssz_qubit_applications.py`)
- Segmentierte Zeitlogik als Qubit-Uhr
- Decoherence als Geometrie-Phaenomen
- Gravitationsbedingte Drift-Vorhersage
- Segment-Aware QEC
- Quantenkommunikation Sync

---

## Visualisierungen

### Plots generieren

```bash
python visualize_ssz_qubits.py
```

### Generierte Plots

| Datei | Beschreibung |
|-------|--------------|
| `time_dilation_vs_height.png` | D_SSZ vs Hoehe |
| `qubit_pair_mismatch.png` | Paar-Mismatch-Analyse |
| `coherent_zone.png` | Segment-kohaerente Zonen |
| `qubit_array_analysis.png` | Array-Optimierung |
| `ssz_vs_gr_comparison.png` | SSZ vs ART Vergleich |
| `golden_ratio_structure.png` | phi-Struktur |

### Beispiel-Visualisierung

```python
import matplotlib.pyplot as plt
import numpy as np
from ssz_qubits import ssz_time_dilation, R_EARTH, M_EARTH

heights = np.linspace(0, 1000, 100)  # 0 bis 1000 m
d_ssz = [ssz_time_dilation(R_EARTH + h, M_EARTH) for h in heights]

plt.plot(heights, d_ssz)
plt.xlabel('Hoehe [m]')
plt.ylabel('D_SSZ')
plt.title('SSZ Zeitdilatation vs Hoehe')
plt.savefig('my_plot.png')
```

---

## Physikalische Ergebnisse

### Erdoberflaeche

| Parameter | Wert |
|-----------|------|
| Xi | 6.961078e-10 |
| D_SSZ | 0.999999999303892 |
| dXi/dr | -1.093e-16 /m |
| r_s (Erde) | 8.87 mm |

### Qubit-Effekte

| Hoehendifferenz | Delta Xi | Zeitdrift |
|-----------------|----------|-----------|
| 1 um | ~10^-22 | Messbar |
| 10 um | ~10^-21 | Signifikant |
| 100 um | ~10^-20 | Kritisch |
| 1 mm | ~10^-19 | ~0.01 ps/s |
| 10 mm | ~10^-18 | ~0.1 ps/s |

### Kohaerente Zonen

| Toleranz | Zonenbreite |
|----------|-------------|
| 10^-16 | 458 mm |
| 10^-17 | 46 mm |
| 10^-18 | 4.6 mm |
| 10^-19 | 458 um |
| 10^-20 | 46 um |

### SSZ vs ART Vergleich

| Aspekt | ART | SSZ |
|--------|-----|-----|
| Raumzeit | Kontinuierlich | Diskret |
| Am Horizont | D = 0 (Singularitaet) | D = 0.555 (Finite) |
| Weak Field | D ≈ 1 - r_s/2r | D = 1/(1+Xi) ≈ gleich |
| Quantisierung | Nein | Ja (phi-basiert) |

---

## Experimentelle Validierung

### GPS-System

| Parameter | SSZ-Vorhersage | Gemessen | Status |
|-----------|----------------|----------|--------|
| Zeitdrift | ~45 us/Tag | ~45 us/Tag | MATCH |
| Positionsfehler | ~11 km/Tag | ~10 km/Tag | MATCH |

### Pound-Rebka Experiment (1960)

| Parameter | SSZ-Vorhersage | Gemessen | Status |
|-----------|----------------|----------|--------|
| Rotverschiebung | 2.46e-15 | (2.57±0.26)e-15 | MATCH |

### NIST Optische Uhren (2010)

| Parameter | SSZ-Vorhersage | Status |
|-----------|----------------|--------|
| 33 cm Hoehendifferenz | Messbar | MATCH |

### Tokyo Skytree (2020)

| Parameter | SSZ-Vorhersage | Status |
|-----------|----------------|--------|
| 450 m Hoehendifferenz | Messbar | MATCH |

---

## Projektstruktur

```
ssz-qubits/
├── ssz_qubits.py               # Kernmodul (933 Zeilen)
├── demo.py                     # Interaktive Demo (9 Demos)
├── run_tests.py                # Test-Runner
├── visualize_ssz_qubits.py     # Visualisierung (6 Plots)
├── requirements.txt            # Abhaengigkeiten
├── README.md                   # Diese Datei
├── FINAL_REPORT.md             # Finaler Report
├── COMPLETE_PROJECT_REPORT.md  # Vollstaendiger Bericht
│
├── docs/
│   ├── SSZ_FORMULA_DOCUMENTATION.md    # Formel-Dokumentation
│   ├── SSZ_MATHEMATICAL_PHYSICS.md     # Math/Physik Grundlagen
│   ├── SSZ_QUBIT_APPLICATIONS.md       # Praktische Anwendungen
│   └── SSZ_QUBIT_THEORY_SUMMARY.md     # Theorie-Zusammenfassung
│
├── tests/
│   ├── test_ssz_physics.py             # 17 Physics Tests
│   ├── test_edge_cases.py              # 25 Edge Case Tests
│   ├── test_validation.py              # 17 Validation Tests
│   └── test_ssz_qubit_applications.py  # 15 Application Tests
│
├── outputs/                    # Generierte Plots
│   ├── time_dilation_vs_height.png
│   ├── qubit_pair_mismatch.png
│   ├── coherent_zone.png
│   ├── qubit_array_analysis.png
│   ├── ssz_vs_gr_comparison.png
│   └── golden_ratio_structure.png
│
└── reports/                    # Test-Reports
    ├── RUN_SUMMARY.md
    └── full-output.md
```

---

## FAQ

### Allgemein

**Q: Was ist der Unterschied zwischen SSZ und der Allgemeinen Relativitaetstheorie?**

A: Die ART behandelt Raumzeit als kontinuierliches Gebilde. SSZ behandelt Raumzeit als **diskrete Struktur** mit messbaren Segmenten. Im Weak Field (wie auf der Erde) liefern beide nahezu identische Ergebnisse. Der Unterschied zeigt sich in starken Feldern: SSZ vermeidet die Singularitaet am Schwarzschild-Horizont.

**Q: Warum ist der Golden Ratio phi wichtig?**

A: phi = (1+sqrt(5))/2 steuert die Saettigungsrate der Segment Density im Strong Field. Die Formel Xi = 1 - exp(-phi*r/r_s) sorgt dafuer, dass Xi bei r = r_s einen endlichen Wert erreicht (ca. 0.8), anstatt zu divergieren.

**Q: Ist SSZ experimentell bestaetigt?**

A: SSZ reproduziert alle bekannten experimentellen Ergebnisse (GPS, Pound-Rebka, Atomuhren) im Weak Field. Die Vorhersagen fuer Strong Fields (Schwarze Loecher) sind noch nicht direkt testbar.

### Technisch

**Q: Welche Python-Version wird benoetigt?**

A: Python 3.8 oder hoeher.

**Q: Wie genau sind die Berechnungen?**

A: Die Berechnungen verwenden 64-bit Floating Point (numpy.float64) mit einer Praezision von etwa 15-16 signifikanten Stellen.

**Q: Kann ich SSZ mit meinem Qubit-Simulator integrieren?**

A: Ja! SSZ-Qubits ist als Python-Modul konzipiert und kann in jeden Python-basierten Simulator integriert werden. Importieren Sie einfach die benoetigten Funktionen.

**Q: Warum sind manche Werte 0.000000e+00?**

A: Bei optimierten Arrays mit konstanter Hoehe ist die Xi-Variation exakt null. Das ist kein Fehler, sondern das gewuenschte Ergebnis der Optimierung.

### Qubit-spezifisch

**Q: Wie gross ist der SSZ-Effekt auf typische Qubits?**

A: Bei 1 mm Hoehendifferenz betraegt Delta Xi etwa 10^-19, was zu einer Zeitdrift von ~0.01 ps/s fuehrt. Bei typischen Gate-Zeiten von 50 ns ist der direkte Effekt klein, aber akkumuliert ueber viele Operationen.

**Q: Sollte ich SSZ-Korrekturen in meinem Quantencomputer implementieren?**

A: Fuer aktuelle Quantencomputer mit wenigen Qubits und kurzen Kohärenzzeiten sind andere Fehlerquellen (thermisches Rauschen, EM-Stoerungen) dominanter. SSZ wird relevant bei:
- Grossen Qubit-Arrays (>100 Qubits)
- Langen Kohärenzzeiten (>1 ms)
- Praezisen Timing-Anforderungen (<1 ps)
- Verteilten Quantensystemen

**Q: Was ist eine "kohaerente Zone"?**

A: Eine kohaerente Zone ist ein Hoehenbereich, in dem die Xi-Variation unter einer bestimmten Toleranz bleibt. Alle Qubits innerhalb dieser Zone haben nahezu identische Segment-Eigenschaften, was Mismatch-Fehler minimiert.

---

## Referenzen

### Primaerliteratur

1. Casu, L. & Wrede, C. (2025). "Segmented Spacetime: A Discrete Framework for Quantum Gravity"
2. Casu, L. & Wrede, C. (2025). "SSZ Applications in Quantum Computing"

### Experimentelle Validierung

3. Pound, R.V. & Rebka, G.A. (1960). "Apparent Weight of Photons". Physical Review Letters, 4(7), 337-341.
4. Chou, C.W. et al. (2010). "Optical Clocks and Relativity". Science, 329(5999), 1630-1633.
5. Takamoto, M. et al. (2020). "Test of general relativity by a pair of transportable optical lattice clocks". Nature Photonics, 14, 411-415.

### Hintergrund

6. Ashby, N. (2003). "Relativity in the Global Positioning System". Living Reviews in Relativity, 6(1).
7. Will, C.M. (2014). "The Confrontation between General Relativity and Experiment". Living Reviews in Relativity, 17(1).

---

## Autoren & Lizenz

### Autoren

**Carmen Wrede** - Theoretische Physik, SSZ-Theorie  
**Lino Casu** - Implementierung, Qubit-Anwendungen

### Kontakt

- GitHub: [github.com/error-wtf](https://github.com/error-wtf)
- Repository: [github.com/error-wtf/ssz-qubits](https://github.com/error-wtf/ssz-qubits)

### Lizenz

Dieses Projekt ist lizenziert unter der **Anti-Capitalist Software License v1.4**.

Diese Lizenz erlaubt:
- Nutzung fuer nicht-kommerzielle Zwecke
- Modifikation und Weiterverteilung
- Akademische und Forschungszwecke

Diese Lizenz verbietet:
- Kommerzielle Nutzung durch kapitalistische Unternehmen
- Nutzung fuer militaerische Zwecke
- Nutzung zur Ueberwachung

Vollstaendiger Lizenztext: [LICENSE](LICENSE)

---

© 2025 Carmen Wrede & Lino Casu

**"Die Qubits leben nicht nur im Raum, sondern auch in Segmenten der Raumzeit."**
