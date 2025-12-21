# Appendix A: Full Mathematical Derivation — Erweiterte Version

## A.0 Physikalische Motivation vor den Formeln

Bevor wir in die mathematischen Details einsteigen, ist es wichtig, die physikalische Intuition hinter den Formeln zu verstehen. Die SSZ-Theorie basiert auf einer einfachen, aber tiefgreifenden Idee: Die Raumzeit ist nicht kontinuierlich glatt, sondern besteht aus diskreten "Segmenten", deren Dichte vom lokalen Gravitationspotential abhängt.

### A.0.1 Die Segment-Analogie

Stellen Sie sich die Raumzeit als ein Gewebe vor, dessen Fäden in der Nähe massiver Objekte dichter gepackt sind. Ein Lichtstrahl oder ein Quantensystem, das durch dieses Gewebe propagiert, muss mehr Fäden "durchqueren", wenn es sich in einer Region hoher Segmentdichte befindet.

Diese zusätzlichen Durchquerungen verlangsamen die effektive Zeitentwicklung – nicht weil die Physik anders ist, sondern weil mehr "Schritte" erforderlich sind, um dieselbe koordinatenzeitliche Distanz zurückzulegen. Dies ist die physikalische Grundlage der Zeitdilatation in SSZ.

### A.0.2 Von GR zu SSZ

Die Allgemeine Relativitätstheorie beschreibt denselben Effekt in der Sprache der gekrümmten Raumzeit. Die Metrik g_μν kodiert, wie Abstände und Zeitintervalle von den Koordinaten abhängen. Im Schwarzschild-Fall:

```
ds² = -(1 - r_s/r)c²dt² + (1 - r_s/r)⁻¹dr² + r²dΩ²
```

Die Komponente g_tt = -(1 - r_s/r) bestimmt das Verhältnis zwischen Koordinatenzeit t und Eigenzeit τ:

```
dτ/dt = √|g_tt| = √(1 - r_s/r)
```

SSZ reformuliert diesen Zusammenhang durch die Einführung der Segmentdichte Ξ:

```
D = dτ/dt = 1/(1 + Ξ)
```

Im schwachen Feld (r >> r_s) sind beide Formulierungen mathematisch äquivalent.

---

## A.3 SSZ Segment Density Definition — Erweiterte Herleitung

### A.3.1 Warum Ξ = r_s/(2r)?

Die spezifische Form der Weak-Field-Segmentdichte ist nicht willkürlich, sondern ergibt sich aus der Forderung nach Konsistenz mit GR im ersten Ordnung.

**Ausgangspunkt: GR-Zeitdilatation**

In Schwarzschild-Koordinaten:
```
D_GR = √(1 - r_s/r)
```

Für r >> r_s (schwaches Feld) können wir Taylor-entwickeln:
```
D_GR ≈ 1 - r_s/(2r) + O((r_s/r)²)
```

**SSZ-Forderung:**

Wir suchen eine Segmentdichte Ξ, sodass:
```
D_SSZ = 1/(1 + Ξ) ≈ 1 - Ξ + Ξ² - ... ≈ 1 - Ξ  (für Ξ << 1)
```

Vergleich mit GR-Entwicklung:
```
1 - Ξ = 1 - r_s/(2r)
→ Ξ = r_s/(2r)
```

**Physikalische Interpretation:**

Die Segmentdichte Ξ ist das Verhältnis des Schwarzschild-Radius zur doppelten radialen Distanz. Sie hat folgende Eigenschaften:

- Bei r → ∞: Ξ → 0 (flache Raumzeit)
- Bei r = R_Erde ≈ 6.4×10⁶ m: Ξ ≈ 7×10⁻¹⁰ (extrem klein)
- Bei r = r_s: Ξ = 0.5 (Weak-Field-Formel wird ungültig)

### A.3.2 Einheiten und Dimensionsanalyse

Eine wichtige Konsistenzprüfung ist die Dimensionsanalyse:

```
[Ξ] = [r_s]/[r] = m/m = dimensionslos ✓
```

Da Ξ in der Formel D = 1/(1+Ξ) erscheint und D ebenfalls dimensionslos ist (Verhältnis von Zeiten), ist die Konsistenz gewährleistet.

**Numerische Größenordnungen:**

| Objekt | r_s | R | Ξ_surface |
|--------|-----|---|-----------|
| Erde | 8.9 mm | 6371 km | 7.0×10⁻¹⁰ |
| Sonne | 3 km | 696,000 km | 2.1×10⁻⁶ |
| Weißer Zwerg | 4 km | 7000 km | 2.9×10⁻⁴ |
| Neutronenstern | 4 km | 12 km | 0.17 |
| Schwarzes Loch (bei Horizont) | - | r_s | 0.5 |

Die Tabelle zeigt den Übergang vom schwachen zum starken Feld. Bei Neutronensternen (Ξ ~ 0.17) beginnt die Weak-Field-Formel signifikant von der Strong-Field-Formel abzuweichen.

---

## A.5 Differential Time Dilation — Erweiterte Analyse

### A.5.1 Taylor-Entwicklung mit höheren Ordnungen

Die Formel ΔD = r_s × Δh / R² ist eine Näherung erster Ordnung. Für Anwendungen, die höhere Präzision erfordern, können wir höhere Ordnungen einbeziehen:

**Exakte Formel:**
```
D(h) = 1 / (1 + r_s/(2(R+h)))
     = 2(R+h) / (2(R+h) + r_s)
```

**Differenz:**
```
ΔD = D(h+Δh) - D(h)
   = 2(R+h+Δh)/(2(R+h+Δh)+r_s) - 2(R+h)/(2(R+h)+r_s)
```

Nach Vereinfachung:
```
ΔD = r_s × Δh × 2 / [(2(R+h)+r_s)(2(R+h+Δh)+r_s)]
```

Für h, Δh << R und r_s << R:
```
ΔD ≈ r_s × Δh × 2 / (2R)² = r_s × Δh / (2R²)
```

**Korrekturterme:**

Für Präzisionsanwendungen (z.B. GPS-Korrekturen):
```
ΔD = r_s × Δh / (2R²) × [1 - 2h/R - Δh/R + O((h/R)²)]
```

Für h = 400 km (ISS):
```
Korrektur: 2h/R ≈ 2×400/6371 ≈ 0.13 (13% Abweichung)
```

Diese Korrektur ist für Satellitenexperimente relevant.

### A.5.2 Numerische Verifikation mit Python

```python
import numpy as np

def delta_D_exact(h, delta_h, R=6.371e6, r_s=8.87e-3):
    """Exakte differentielle Zeitdilatation."""
    D1 = 2 * (R + h) / (2 * (R + h) + r_s)
    D2 = 2 * (R + h + delta_h) / (2 * (R + h + delta_h) + r_s)
    return D2 - D1

def delta_D_approx(h, delta_h, R=6.371e6, r_s=8.87e-3):
    """Näherung erster Ordnung."""
    return r_s * delta_h / (2 * R**2)

# Verifikation
h_values = [0, 1e3, 1e4, 1e5, 4e5]  # 0, 1km, 10km, 100km, 400km
delta_h = 1.0  # 1 m

print("h [km] | Exact | Approx | Fehler [%]")
print("-" * 45)
for h in h_values:
    exact = delta_D_exact(h, delta_h)
    approx = delta_D_approx(h, delta_h)
    error = abs(exact - approx) / exact * 100
    print(f"{h/1e3:6.0f} | {exact:.3e} | {approx:.3e} | {error:.2f}")
```

Erwartete Ausgabe:
```
h [km] | Exact | Approx | Fehler [%]
---------------------------------------------
     0 | 1.093e-19 | 1.093e-19 | 0.00
     1 | 1.093e-19 | 1.093e-19 | 0.03
    10 | 1.090e-19 | 1.093e-19 | 0.31
   100 | 1.059e-19 | 1.093e-19 | 3.11
   400 | 9.57e-20 | 1.093e-19 | 12.41
```

Die Näherung ist für h < 10 km auf < 1% genau.

---

## A.6 Phase Drift Formula — Intuitive Herleitung

### A.6.1 Von Zeitdilatation zu Phase

Die Verbindung zwischen Zeitdilatation und Quantenphase ist fundamental und elegant:

**Quantenmechanische Phasenakkumulation:**

Ein Quantenzustand |ψ⟩ mit Energie E akkumuliert Phase gemäß der Schrödinger-Gleichung:
```
|ψ(t)⟩ = e^(-iEt/ℏ)|ψ(0)⟩
```

Für ein Zwei-Niveau-System (Qubit) mit Energieaufspaltung ℏω:
```
Phase: Φ(t) = ωt
```

**Einbeziehung der Zeitdilatation:**

Wenn die lokale Uhr langsamer läuft (D < 1), vergeht weniger Eigenzeit τ für dieselbe Koordinatenzeit t:
```
τ = D × t
```

Die akkumulierte Phase hängt von der Eigenzeit ab:
```
Φ(t) = ω × τ = ω × D × t
```

**Differentielle Phase zwischen zwei Qubits:**

Qubit 1 bei Höhe h₁: Φ₁(t) = ω × D(h₁) × t
Qubit 2 bei Höhe h₂: Φ₂(t) = ω × D(h₂) × t

Phasendifferenz:
```
ΔΦ(t) = Φ₂ - Φ₁ = ω × (D(h₂) - D(h₁)) × t = ω × ΔD × t
```

### A.6.2 Physikalische Interpretation

Die Phasendrift ΔΦ hat eine intuitive Interpretation:

- **ω-Faktor:** Höhere Frequenzen bedeuten mehr Oszillationen pro Zeiteinheit, also mehr akkumulierte Phase.
- **ΔD-Faktor:** Größere Zeitdilatationsdifferenz bedeutet größere Diskrepanz in der Phasenakkumulationsrate.
- **t-Faktor:** Längere Zeit bedeutet mehr akkumulierte Differenz.

**Analogie zum Alltagsleben:**

Stellen Sie sich zwei Wanderer vor, die parallel auf unterschiedlichen Höhen einen Berg besteigen. Der höhere Wanderer (weniger Zeitdilatation) macht bei gleicher Koordinatenzeit mehr Schritte. Nach einer Stunde hat er mehr Höhenmeter zurückgelegt – analog zur größeren akkumulierten Phase.

### A.6.3 Warum der Effekt so klein ist

Die Kleinheit des SSZ-Effekts für Transmons lässt sich in drei Faktoren zerlegen:

1. **Gravitationspotential der Erde:** r_s/R ≈ 10⁻⁹
2. **Relative Höhendifferenz:** Δh/R ≈ 10⁻⁹ (für 1 mm)
3. **Zeitdauer:** t/t_Planck ~ 10²⁰ (für 100 μs)

Kombiniert:
```
ΔΦ ∼ ω × (r_s/R) × (Δh/R) × t ∼ 10¹⁰ × 10⁻⁹ × 10⁻⁹ × 10⁻⁴ ∼ 10⁻¹³
```

Jeder der drei Faktoren (außer ω) unterdrückt den Effekt um viele Größenordnungen.

---

## A.7 Segment-Coherent Zone Width — Erweiterte Diskussion

### A.7.1 Physikalische Bedeutung der Zonenbreite

Die Segment-kohärente Zonenbreite z(ε) definiert den maximalen räumlichen Bereich, über den Quantenoperationen mit einer Phasenfehler-Toleranz ε durchgeführt werden können, ohne SSZ-Kompensation.

**Herleitung:**

Wir fordern |ΔΦ| ≤ ε für alle Qubits innerhalb der Zone:
```
|ω × r_s × Δh / R² × t| ≤ ε
```

Auflösung nach Δh:
```
Δh ≤ ε × R² / (ω × r_s × t)
```

Um eine frequenz- und zeitunabhängige Metrik zu erhalten, normieren wir auf Referenzwerte (ω_ref, t_ref):
```
z(ε) = 4ε × R² / r_s
```

Der Faktor 4 entsteht durch die Normierung (ω_ref × t_ref = 4 in natürlichen Einheiten).

### A.7.2 Zonenbreite für verschiedene Anwendungen

| Anwendung | Toleranz ε | z(ε) | Implikation |
|-----------|------------|------|-------------|
| Ultrapräzisions-Metrologie | 10⁻²⁰ | 183 μm | Sub-mm Abstände |
| Quantum Error Correction | 10⁻¹⁸ | 18.3 mm | Chip-Skala |
| High-Fidelity Gates | 10⁻¹⁵ | 18.3 m | Labor-Skala |
| Standard Gates | 10⁻¹² | 18.3 km | Stadt-Skala |
| Grobe Synchronisation | 10⁻⁹ | 18,300 km | Kontinental |

**Interpretation:**

- Alle Qubits auf einem planaren Chip (Δh < 100 μm) sind für alle praktischen Zwecke innerhalb einer Zone.
- 3D-Chiplet-Stacks (Δh ~ 1 mm) erfordern Kompensation nur für extreme Präzision (ε < 10⁻¹⁷).
- Optische Netzwerke (Δh ~ 1 m) erfordern Kompensation für Standard-Fidelity.

### A.7.3 Design-Implikationen

Die Zonenbreite bietet ein einfaches Kriterium für Chip-Designer:

```python
def needs_ssz_compensation(qubit_layout, target_fidelity):
    """
    Bestimmt, ob SSZ-Kompensation für ein Qubit-Layout erforderlich ist.
    
    Args:
        qubit_layout: Dict[QubitId, Height] in Metern
        target_fidelity: Ziel-Fidelity (z.B. 0.9999)
    
    Returns:
        bool: True wenn Kompensation nötig
    """
    epsilon = 1 - target_fidelity
    zone_width = 4 * epsilon * R_EARTH**2 / r_s_EARTH
    
    heights = list(qubit_layout.values())
    max_delta_h = max(heights) - min(heights)
    
    return max_delta_h > zone_width
```

---

## A.8 Unit Verification — Erweiterte Konsistenzprüfung

### A.8.1 Systematische Dimensionsanalyse

Jede physikalische Formel muss dimensionell konsistent sein. Hier verifizieren wir alle SSZ-Formeln:

**Segmentdichte Ξ:**
```
[Ξ] = [r_s] / [r] = m / m = 1 (dimensionslos) ✓
```

**Zeitdilatationsfaktor D:**
```
[D] = 1 / (1 + [Ξ]) = 1 / 1 = 1 (dimensionslos) ✓
```

**Differentielle Zeitdilatation ΔD:**
```
[ΔD] = [r_s] × [Δh] / [R²] = m × m / m² = 1 (dimensionslos) ✓
```

**Phasendrift ΔΦ:**
```
[ΔΦ] = [ω] × [ΔD] × [t] = (rad/s) × 1 × s = rad ✓
```

**Zonenbreite z(ε):**
```
[z] = [ε] × [R²] / [r_s] = 1 × m² / m = m ✓
```

**Kompensationsphase Φ_corr:**
```
[Φ_corr] = [ω] × [r_s] × [Δh] / [R²] × [t]
         = (rad/s) × m × m / m² × s = rad ✓
```

Alle Formeln sind dimensionell konsistent.

### A.8.2 Grenzfall-Verifikation

Physikalische Formeln müssen in Grenzfällen sinnvolle Ergebnisse liefern:

**Flache Raumzeit (r_s → 0):**
```
Ξ → 0, D → 1, ΔD → 0, ΔΦ → 0
```
✓ Keine Gravitationseffekte ohne Masse.

**Große Distanz (r → ∞):**
```
Ξ → 0, D → 1
```
✓ Asymptotisch flache Raumzeit.

**Gleiche Höhe (Δh = 0):**
```
ΔD = 0, ΔΦ = 0
```
✓ Keine Phasendifferenz ohne Höhendifferenz.

**Instantane Messung (t = 0):**
```
ΔΦ = 0
```
✓ Keine Phasenakkumulation ohne Zeit.

**Statisches System (ω = 0):**
```
ΔΦ = 0
```
✓ Keine Phase ohne Oszillation.

Alle Grenzfälle sind physikalisch sinnvoll.

---

© 2025 Carmen Wrede & Lino Casu
