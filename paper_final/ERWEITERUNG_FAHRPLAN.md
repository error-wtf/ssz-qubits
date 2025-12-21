# SSZ Unified Paper - Erweiterung Fahrplan

**Datum:** 2025-12-21
**Ziel:** Stichpunktartige Abschnitte zu vollständigen Fließtexten ausarbeiten

---

## Übersicht: Zu erweiternde Abschnitte

| # | Abschnitt | Datei | Status | Priorität |
|---|-----------|-------|--------|-----------|
| 1 | 1.1 Claim Boundaries | `sections/01_introduction.md` | 🔄 | HOCH |
| 2 | 3.2-3.3 Control Protocol | `sections/03_control.md` | 🔄 | HOCH |
| 3 | 4.2 Upper-bound Experiments | `sections/04_experiments.md` | 🔄 | HOCH |
| 4 | 5. Entanglement & Lindblad | `sections/05_entanglement.md` | 🔄 | MITTEL |
| 5 | 8.1 Conclusion (5 Punkte) | `sections/08_conclusion.md` | 🔄 | HOCH |
| 6 | Appendix B: Confound Playbook | `appendices/C_confounds.md` | 🔄 | MITTEL |

**Legende:** ✅ Fertig | 🔄 In Arbeit | ⏳ Ausstehend

---

## 1. Section 1.1: Claim Boundaries

### Aktueller Zustand
Drei kurze Bullet-Punkte:
- Bounded regime (mm, 10⁻¹³ rad)
- Detection regime (m, 0.6 rad)
- Future regime (Satellite QKD)

### Erforderliche Erweiterung

**1.1.1 Bounded Regime (Today's Superconducting Qubits)**
- Begründung der mm-Skala (typische Chip-Dimensionen)
- Warum 100 μs Kohärenzzeit relevant
- Berechnung: ΔΦ = ω × r_s × Δh / R² × t = 6.9×10⁻¹³ rad
- Vergleich zum Noise Floor (~1 rad T₂-limitiert)
- Interpretation: Null-Ergebnis ist SSZ-konsistent
- Relevante Plattformen: IBM, Google, Rigetti Transmons

**1.1.2 Detection Regime (Optical Atomic Clocks)**
- Begründung der m-Skala (Labor-Aufbau, NIST Tokyo Skytree)
- Frequenzverhältnis: 10¹⁴ Hz vs 10⁹ Hz = 10⁵× Verstärkung
- Berechnung: ΔΦ = 0.59 rad (SNR > 100)
- Historische Validierung: Chou et al. 2010, Bothwell 2022
- Gold-Standard für SSZ-Validierung

**1.1.3 Future Regime (Advanced Quantum Networks)**
- Satellit-basierte Höhendifferenzen (~400 km)
- SSZ als Engineering-Constraint (nicht nur Curiosity)
- Quantum Key Distribution mit SSZ-aware Protokollen
- Timeline: 2030+

### Neue Datei
`sections_extended/01_claim_boundaries_extended.md`

---

## 2. Section 3: Control and Compensation Protocol

### Aktueller Zustand
- Step 1-4 als nummerierte Listen
- Scaling Signatures als Bullet-Points
- Code-Snippets ohne Kontext

### Erforderliche Erweiterung

**3.2 With/Without Protocol - Fließtext**
- Praktische Ramsey-Experiment-Beschreibung
- Konkrete Pulssequenz: π/2 - Wartezeit - π/2
- Phasenakkumulation während Wartezeit
- Virtual-Z-Frame-Implementierung (IBM Qiskit)
- Warum Temperatur-Drifts NICHT entfernt werden

**3.3 Scaling Signatures - Unterabschnitte**

*3.3.1 Height Scaling*
- Mathematische Ableitung der konstanten Steigung
- Warum thermische Gradienten NICHT ∝ Δh sind
- Experimentelles Setup: Piezo-Stage, Tilt-Winkel

*3.3.2 Frequency Scaling*
- Lineare ω-Abhängigkeit vs. 1/f für thermisch
- Multi-Frequency-Protokoll-Design
- Erwartete Datenpunkte und Fit

*3.3.3 Time Scaling*
- Lineare t-Akkumulation vs. √t für Random Walk
- Unterscheidung von White Noise und 1/f Noise
- Time-Series-Analyse

*3.3.4 Compensation Reversal*
- Der entscheidende Diskriminator
- Warum NUR SSZ reversiert
- Praktische Implementierung

### Neue Datei
`sections_extended/03_control_extended.md`

---

## 3. Section 4.2: Upper-bound Experiments

### Aktueller Zustand
Drei Experimente in Stichpunkten:
- Tilt (5 Zeilen)
- Remote Entanglement (8 Zeilen)
- 3D Chiplet Stack (8 Zeilen)

### Erforderliche Erweiterung

**Experiment 1: Chip Tilt - Vollständige Beschreibung**
- **Aufbau**: Dilution Refrigerator, Piezo-Kipptisch, Auflösung ±0.01°
- **Technik**: Stepper-Motor oder Piezo-Aktuator
- **Parameter**: L = 5 mm Qubit-Abstand, θ = 0°-1°, Δh_max = 87 μm
- **Messdauer**: 1000× Ramsey bei jeder Winkelstellung
- **Statistische Auswertung**: Lineare Regression, 95% CI
- **Erwartete Unsicherheiten**: σ_α ≈ 10⁻³ rad/m
- **Störquellen**: Thermische Drift bei Winkeländerung (5 min Equilibration)

**Experiment 2: Remote Entanglement - Vollständige Beschreibung**
- **Aufbau**: Zwei Kryostaten, vertikale Trennung 10-100 cm
- **Technik**: Photonenlink (optische Faser, heralded entanglement)
- **Parameter**: Bell-State |Φ⁺⟩, t = 10-100 μs
- **GPS/Nivellierung**: Höhenmessung auf mm-Genauigkeit
- **Statistische Auswertung**: Fidelity F_with vs F_without, N = 10⁴
- **Erwartete Unsicherheiten**: σ_F ≈ 10⁻³
- **Störquellen**: Fiber-Längenänderungen, LO-Drift zwischen Kryostaten

**Experiment 3: 3D Chiplet Stack - Vollständige Beschreibung**
- **Aufbau**: 2-3 gestapelte Qubit-Dies, TSV oder Flip-Chip
- **Technik**: Vertikale Interconnects, Cross-Layer-CZ-Gates
- **Parameter**: Layer-Abstand 1-5 mm, Cross-Layer-Fidelity
- **Thermische Überwachung**: Sensoren pro Layer
- **Statistische Auswertung**: Gate-Fidelity vs. Layer-Position
- **Erwartete Unsicherheiten**: Dominiert von Fabrikation, nicht SSZ
- **Störquellen**: Thermische Gradienten zwischen Layern

### Neue Datei
`sections_extended/04_experiments_extended.md`

---

## 4. Section 5: Entanglement and Phase Preservation

### Aktueller Zustand
- Bell-State-Evolution (Gleichung)
- Fidelity-Formel
- Keine Lindblad-Behandlung

### Erforderliche Erweiterung

**5.x Lindblad Master Equation Treatment**
- Dichtematrix ρ(t) statt reiner Zustand
- Lindblad-Form: dρ/dt = -i[H,ρ] + Σ_k (L_k ρ L_k† - ½{L_k†L_k, ρ})
- SSZ als deterministischer Hamilton-Beitrag: H_SSZ = ω·ΔD·σ_z
- Wirkung auf Off-Diagonal-Elemente ρ₀₁ und ρ₁₀
- Unterscheidung: Deterministischer Term vs. Dissipator

**5.x Compensation in Entangled Networks**
- Photon-Link-Phasenkorrektur (vor/nach Transmission)
- Lokale Gate-Korrektur (Z-Rotation an einem Node)
- Feedforward vs. Feedback-Implementierung
- Multi-Node-Skalierung (GHZ über N Knoten)

### Neue Datei
`sections_extended/05_entanglement_extended.md`

---

## 5. Section 8.1: Conclusion (5-Punkte-Liste)

### Aktueller Zustand
Fünf stichpunktartige Aussagen:
1. 12 orders of magnitude gap
2. Null results are positive
3. Optical clocks detectable
4. Upper bounds constrain
5. No current impact

### Erforderliche Erweiterung

**Absatz 1: Die 12 Größenordnungen-Lücke**
- Erklärung warum diese Lücke existiert (ω × Δh × t)
- Bedeutung für Interpretationen
- Warum dies NICHT gegen SSZ spricht

**Absatz 2: Null-Ergebnis als positives Ergebnis**
- Philosophie der Falsifikation
- SSZ-Vorhersage = Undetektierbarkeit in bounded regime
- Wie Null-Ergebnisse die Theorie stützen

**Absatz 3: Optische Uhren als Gold-Standard**
- Technologische Reife
- Bereits demonstrierte Präzision (Chou, Bothwell)
- Konkreter experimenteller Pfad

**Absatz 4: Obere Schranken auf anomale Kopplungen**
- Was eine obere Schranke bedeutet
- Konsequenzen für alternative Theorien
- α < α_SSZ + 2σ Interpretation

**Absatz 5: Zukünftige Selbstkalibrierung**
- Vision: SSZ-aware Quantenprozessoren
- Automatische Höhenprofilierung
- Compiler-integrierte Korrektur

### Neue Datei
`sections_extended/08_conclusion_extended.md`

---

## 6. Appendix B/C: Confound Playbook

### Aktueller Zustand
- Fünf Konfound-Typen mit kurzen Stichpunkten
- Keine detaillierte Physik

### Erforderliche Erweiterung

Für jeden Konfound (Vibration, Thermal, LO, Magnetic, Charge):

**Erweiterte Struktur pro Konfound:**
1. **Physikalischer Mechanismus** (2-3 Sätze)
2. **Warum dieser Konfound auftritt** (Gerätespezifisch)
3. **Skalierungsverhalten** (Tabelle + Erklärung)
4. **Implementierung der Mitigation** (konkrete Schritte)
5. **Entscheidungsbaum** (Wenn X, dann Y)

### Neue Datei
`appendices_extended/C_confounds_extended.md`

---

## Workflow

```
Phase 1: Erweiterte Dateien erstellen (sections_extended/, appendices_extended/)
Phase 2: Review und Konsistenzprüfung
Phase 3: Integration in Hauptdateien (oder als Ersatz)
Phase 4: Assembler anpassen für erweiterte Version
Phase 5: Neues DOCX generieren: SSZ_Unified_Paper_EXTENDED.docx
```

---

## Dateistatus

### Phase 1 (Ursprüngliche Erweiterungen)

| Komponente | Datei | Status |
|------------|-------|--------|
| Fahrplan | ERWEITERUNG_FAHRPLAN.md | ✅ |
| 1.1 Claim Boundaries | sections_extended/01_claim_boundaries_extended.md | ✅ |
| 3.2-3.3 Control | sections_extended/03_control_extended.md | ✅ |
| 4.2 Experiments | sections_extended/04_experiments_extended.md | ✅ |
| 5.x Lindblad | sections_extended/05_entanglement_extended.md | ✅ |
| 8.1 Conclusion | sections_extended/08_conclusion_extended.md | ✅ |
| App C Confounds | appendices_extended/C_confounds_extended.md | ✅ |

### Phase 2 (Zusätzliche Erweiterungen)

| Komponente | Datei | Status |
|------------|-------|--------|
| 2.5 Strong Field (Why φ?) | sections_extended/02b_strong_field_extended.md | ✅ |
| 6. Engineering Design | sections_extended/06_engineering_extended.md | ✅ |
| 7. Feasibility Roadmap | sections_extended/07_feasibility_extended.md | ✅ |
| App A Derivation | appendices_extended/A_derivation_extended.md | ✅ |

---

## Nächste Schritte

```bash
# 1. Verzeichnisse erstellen
mkdir -p paper_final/sections_extended
mkdir -p paper_final/appendices_extended

# 2. Erweiterte Dateien erstellen (dieser Fahrplan)

# 3. Nach Fertigstellung:
python assemble_paper.py --extended
```

---

## Geschätzter Umfang

| Abschnitt | Aktuell | Erweitert | Zuwachs |
|-----------|---------|-----------|---------|
| 1.1 Claim Boundaries | ~25 Zeilen | ~120 Zeilen | +95 |
| 3.2-3.3 Control | ~80 Zeilen | ~250 Zeilen | +170 |
| 4.2 Experiments | ~70 Zeilen | ~300 Zeilen | +230 |
| 5.x Lindblad | ~0 Zeilen | ~150 Zeilen | +150 |
| 8.1 Conclusion | ~30 Zeilen | ~150 Zeilen | +120 |
| App C Confounds | ~210 Zeilen | ~400 Zeilen | +190 |
| **Gesamt** | **~415** | **~1370** | **+955** |

**Erwartete Seitenzahl-Erhöhung: ~10-15 Seiten**

---

© 2025 Carmen Wrede & Lino Casu
Licensed under ANTI-CAPITALIST SOFTWARE LICENSE v1.4
