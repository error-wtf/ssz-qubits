# Appendix C: Confound Playbook — Erweiterte Version

Dieses Appendix bietet detaillierte Anleitungen zur Unterscheidung von SSZ-Effekten und experimentellen Störquellen. Für jede Konfound-Kategorie werden physikalische Mechanismen, Skalierungsverhalten, praktische Implementierung der Mitigationsmaßnahmen und Entscheidungsbäume zur Diagnose vorgestellt.

---

## C.1 Vibrationsisolation

### Physikalischer Mechanismus

Mechanische Vibrationen koppeln auf mehreren Wegen in supraleitende Qubit-Systeme ein:

**Direkte Kopplung:** Beschleunigungen erzeugen Trägheitskräfte auf bewegliche Elemente des Chips, insbesondere auf schwebende Gate-Elektroden in Trapped-Ion-Systemen oder auf mechanisch empfindliche Resonator-Strukturen. Diese Kräfte modulieren Kopplungsstärken und induzieren Phasenrauschen.

**Piezoelektrische Kopplung:** Kristalline Substrate (Saphir, Silizium) zeigen piezoelektrische Effekte unter mechanischem Stress. Vibrationen erzeugen lokale elektrische Felder, die Qubit-Frequenzen verschieben.

**Magnetomechanische Kopplung:** Vibrationen von stromführenden Leitern in der Nähe von Magnetfeldempfindlichen Qubits erzeugen zeitabhängige Flussänderungen, die als Phasenrauschen erscheinen.

### Warum diese Störquelle auftritt

In typischen Laborumgebungen sind folgende Vibrationsquellen präsent:
- Gebäudevibrationen (Aufzüge, HVAC-Systeme): 1–10 Hz
- Vakuumpumpen (Scroll, Turbo): 10–100 Hz
- Akustische Einkopplung (Lüfter, Gespräche): 100–1000 Hz
- Kryostat-interne Quellen (Pulsröhre): 1–2 Hz, harmonische

### Skalierungsverhalten

| Eigenschaft | Vibration | SSZ |
|-------------|-----------|-----|
| Höhenabhängigkeit | Keine (ortsunabhängig) | Linear ∝ Δh |
| Frequenzabhängigkeit | Resonant (peaked) | Linear ∝ ω |
| Zeitabhängigkeit | Impulsartig, nicht-stationär | Linear ∝ t (stationär) |
| Kompensationsumkehr | Nein | Ja |

### Implementierung der Mitigation

**Passive Isolation:**
1. Pneumatische Schwingungsdämpfer unter dem optischen Tisch (Cutoff ~1 Hz)
2. Schwere Masse (Granitblock) zur Trägheitsunterdrückung
3. Weiche Aufhängung des Kryostaten (Federn, Dämpfer)

**Aktive Isolation:**
1. Beschleunigungssensoren (Geophone) an Tisch und Kryostat
2. Feedforward-Controller berechnet Gegenbewegung
3. Piezo-Aktuatoren kompensieren in Echtzeit
4. Typische Unterdrückung: 20–40 dB im Bereich 1–100 Hz

**Kryostat-spezifische Maßnahmen:**
1. Pulsröhren-Entkopplung (flexible Bellows, Schwingungsisolator)
2. Getrennte Fundamente für Pulsröhre und Experimentplattform
3. Zeitliche Synchronisation: Daten nur zwischen Pulsröhren-Schlägen aufnehmen

### Entscheidungsbaum

```
Beobachtete Phasenfluktuationen?
│
├─→ Korreliert mit Beschleunigungssensor-Signal?
│   │
│   ├─→ JA: Vibrations-Konfound bestätigt
│   │   └─→ Maßnahme: Isolation verbessern, Events verwerfen
│   │
│   └─→ NEIN: Weiter zu nächstem Test
│
└─→ Fluktuationen impulsartig (nicht kontinuierlich)?
    │
    ├─→ JA: Wahrscheinlich Vibration
    │
    └─→ NEIN: Unwahrscheinlich Vibration, SSZ-Kandidat prüfen
```

---

## C.2 Thermische Kontrolle

### Physikalischer Mechanismus

Temperaturvariationen beeinflussen Qubits über mehrere Kanäle:

**Frequenzverschiebung:** Transmon-Frequenzen hängen von der Temperatur ab, typischerweise ~1 MHz/K bei Millikelvin-Temperaturen. Dies resultiert aus:
- Änderung der Josephson-Energie E_J (Supraleiter-Gap-Abhängigkeit)
- Thermische Expansion des Substrats (Kapazitätsänderung)
- Änderung der kinetischen Induktivität

**Quasiteilchen-Poisoning:** Erhöhte Temperatur erzeugt nicht-äquilibrierte Quasiteilchen im Supraleiter, die:
- T₁-Relaxation erhöhen (zusätzlicher Verlustkanal)
- Frequenzfluktuationen verursachen (Charge-Parity-Jumps)
- Phasenrauschen beitragen

**Differentielle Effekte:** Ungleichmäßige Temperaturverteilung führt zu unterschiedlichen Frequenzverschiebungen verschiedener Qubits, was als scheinbarer Phasendrift erscheint.

### Warum diese Störquelle auftritt

- Schwankende Wärmelast durch Mikrowellenpulse
- Periodische Erwärmung durch Pulsröhren-Zyklus
- Langsame Drifts durch Helium-Pegel-Änderungen
- Externe Wärme-Einkopplung über Kabel und Infrarot-Strahlung

### Skalierungsverhalten

| Eigenschaft | Thermisch | SSZ |
|-------------|-----------|-----|
| Höhenabhängigkeit | Umgebungsabhängig, nicht ∝ Δh | Linear ∝ Δh |
| Frequenzabhängigkeit | Schwach (materialabhängig) | Linear ∝ ω |
| Zeitabhängigkeit | ∝ t (Drift), aber ratenänderlich | Konstante Rate ∝ t |
| Kompensationsumkehr | Nein | Ja |

### Implementierung der Mitigation

**Thermometrie:**
1. Ruthenium-Oxid-Thermometer (RTD) an 3+ Chip-Positionen
2. Zeitkonstante < 1 s für schnelle Antwort
3. Auslese-Rate > Experiment-Rate

**Thermische Stabilisierung:**
1. Aktive PID-Regelung der Mixing Chamber-Temperatur
2. Thermische Schilde (50 K, 4 K, 100 mK) gut verankert
3. Filterung von Infrarot-Strahlung durch Kabelführungen

**Datenanalyse:**
1. Thermometer-Readings zeitgleich mit Qubit-Daten speichern
2. Korrelationsanalyse: Phase vs. Temperatur
3. Wenn Korrelation > Schwelle: Daten verwerfen oder korrigieren

### Entscheidungsbaum

```
Beobachteter Phasendrift?
│
├─→ Korreliert Drift mit RTD-Readings?
│   │
│   ├─→ JA (Korrelation > 0.5): Thermischer Konfound
│   │   └─→ Maßnahme: Besser stabilisieren, Daten korrigieren
│   │
│   └─→ NEIN: Weiter prüfen
│
└─→ Ändert sich Drift-Rate mit Zeit (nicht konstant)?
    │
    ├─→ JA: Thermisch (langsame Equilibrierung)
    │
    └─→ NEIN: SSZ-Kandidat (konstante Rate)
```

---

## C.3 Frequenz-Interleaving

### Physikalischer Mechanismus

Die Unterscheidung von frequenzabhängigen Effekten erfordert Messungen bei verschiedenen Qubit-Frequenzen. Das Interleaving-Verfahren mischt Messungen bei unterschiedlichen ω-Werten, um systematische Drifts zu dekorrelieren.

### Warum dieses Verfahren notwendig ist

Viele Störquellen haben komplexe Frequenzabhängigkeiten:
- LO-Phasenrauschen: Spektrale Dichte S_φ(f) ∝ f⁻ᵅ
- Thermische Effekte: dω/dT variiert mit ω
- Charge-Noise: 1/f-Spektrum

SSZ hingegen sagt strikte Linearität voraus: ΔΦ ∝ ω.

### Skalierungsverhalten

| Eigenschaft | LO-Noise | Thermisch | SSZ |
|-------------|----------|-----------|-----|
| ω-Skalierung | √ω oder 1/f | Schwach | Linear ω |

### Implementierung des Interleaving

**Multi-Frequenz-Chip-Design:**
1. Mehrere Transmons mit unterschiedlichen Frequenzen auf demselben Chip
2. Typische Frequenzen: 4.0, 4.5, 5.0, 5.5, 6.0 GHz
3. Gleiche Höhenposition für alle (planar)

**Messprotokoll:**
1. Randomisierte Reihenfolge der ω-Werte
2. Für jedes ω: N Ramsey-Sequenzen
3. Block-Design: [ω₁, ω₃, ω₂, ω₅, ω₄, ...] (nicht sequentiell)
4. Langsame Drifts betreffen alle ω gleichermaßen → herausmittelbar

**Analyse:**
```
Für jeden ω-Wert:
    ΔΦ(ω) = gemessene Phase
    
Lineare Regression:
    ΔΦ = β_ω × ω + Offset
    
SSZ-Test:
    Wenn β_ω konsistent mit r_s × Δh / R² × t:
        → SSZ-Kandidat
    Wenn β_ω = 0 oder nicht-linear:
        → Konfound oder Null-Ergebnis
```

### Entscheidungsbaum

```
Phasendrift bei mehreren ω gemessen?
│
├─→ Drift skaliert linear mit ω (R² > 0.9)?
│   │
│   ├─→ JA: SSZ-konsistent
│   │   └─→ Nächster Test: Kompensationsumkehr prüfen
│   │
│   └─→ NEIN: Konfound (nicht SSZ)
│
└─→ Drift unabhängig von ω (flach)?
    │
    ├─→ JA: Frequenz-unabhängiger Konfound
    │   └─→ Kandidaten: Thermisch, Magnetisch
    │
    └─→ NEIN (komplexe Abhängigkeit): Gemischte Störquellen
```

---

## C.4 Referenz-Qubits

### Physikalischer Mechanismus

Referenz-Qubits sind Kontroll-Qubits auf gleicher Höhe wie das Mess-Qubit. Sie erfahren dieselben umgebungsbedingten Störungen, aber keinen SSZ-Drift (da Δh = 0).

### Warum diese Methode notwendig ist

Gemeinsame Störquellen (Common-Mode):
- Temperaturänderungen des gesamten Chips
- LO-Phasendrift (betrifft alle Qubits gleich)
- Magnetfeldänderungen (großräumig)

Diese Effekte können durch Differenzbildung eliminiert werden:
```
ΔΦ_korrigiert = ΔΦ_messung - ΔΦ_referenz
```

### Implementierung

**Chip-Layout:**
1. Mess-Qubit bei Höhe h + Δh
2. Referenz-Qubit bei Höhe h (gleich wie unteres Mess-Qubit)
3. Beide Qubits identische Frequenz ω

**Messprotokoll:**
1. Simultane Ramsey-Sequenz auf beiden Qubits
2. Phase Φ_mess und Φ_ref extrahieren
3. Differenz: ΔΦ = Φ_mess - Φ_ref
4. Common-Mode-Störungen heben sich auf

**Anforderungen:**
- Referenz-Qubit muss thermisch/magnetisch äquivalent positioniert sein
- Frequenzgleichheit < 1 MHz für gute Subtraktion
- Simultane Messung (< 1 μs Zeitunterschied)

### Entscheidungsbaum

```
Differenz ΔΦ = Φ_mess - Φ_ref berechnet?
│
├─→ ΔΦ ≠ 0, Φ_ref ≈ 0?
│   │
│   ├─→ JA: Höhen-spezifischer Effekt (SSZ-Kandidat)
│   │
│   └─→ NEIN (ΔΦ ≈ 0, Φ_ref ≠ 0): Common-Mode-Störung
│
└─→ Beide Φ ≈ 0?
    │
    └─→ Kein Effekt detektiert (Bounded Regime)
```

---

## C.5 Randomisierung

### Physikalischer Mechanismus

Langsame systematische Drifts (thermisch, magnetisch, LO) können fälschlicherweise als höhenabhängige Signale interpretiert werden, wenn die Messreihenfolge mit der Höhenvariation korreliert ist.

**Beispiel des Problems:**
- Experimente in Reihenfolge: Δh = 0, 1, 2, 3, 4 mm
- Gleichzeitig: Langsame Erwärmung des Systems
- Resultat: Scheinbare Korrelation zwischen Δh und Phase

### Warum Randomisierung notwendig ist

Durch zufällige Reihenfolge der Δh-Werte werden langsame Drifts zu hochfrequentem Rauschen in der Δh-Dimension. Die lineare Regression wird robust gegen diese Störquelle.

### Implementierung

**Vollständige Randomisierung:**
```python
import numpy as np

delta_h_values = [0, 0.5, 1.0, 1.5, 2.0]  # mm
n_repeats = 100

# Vollständig randomisierte Reihenfolge
measurement_order = []
for _ in range(n_repeats):
    shuffled = delta_h_values.copy()
    np.random.shuffle(shuffled)
    measurement_order.extend(shuffled)
```

**Block-Randomisierung:**
```python
# Jeder Block enthält alle Δh-Werte einmal
blocks = []
for _ in range(n_repeats):
    block = delta_h_values.copy()
    np.random.shuffle(block)
    blocks.append(block)
measurement_order = [dh for block in blocks for dh in block]
```

**Latin-Square-Design:**
Für systematische Abdeckung bei kleiner Stichprobe:
```
Block 1: [0, 1, 2, 3, 4]
Block 2: [2, 4, 1, 3, 0]
Block 3: [4, 0, 3, 2, 1]
...
```

### Analyse

Nach Randomisierung:
1. Daten nach Δh gruppieren (nicht nach Messzeit)
2. Für jeden Δh-Wert: Mittelwert und Standardfehler berechnen
3. Lineare Regression: ΔΦ vs. Δh
4. Zeitliche Drifts erscheinen als erhöhte Varianz, nicht als Bias

### Entscheidungsbaum

```
Wurde Messreihenfolge randomisiert?
│
├─→ JA: Analyse kann fortfahren
│
└─→ NEIN: Ergebnisse potenziell durch Drift kontaminiert
    │
    └─→ Maßnahme: Experiment wiederholen mit Randomisierung
        oder: Zeitliche Korrelation explizit modellieren
```

---

## C.6 Master-Entscheidungsfluss

Der folgende Algorithmus integriert alle Konfound-Checks in einen systematischen Diagnoseprozess:

```
┌────────────────────────────────────────────────────────────────┐
│  SSZ vs. KONFOUND: VOLLSTÄNDIGER ENTSCHEIDUNGSBAUM            │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  1. DATENQUALITÄT                                              │
│     ├─→ Randomisierung durchgeführt? (NEIN → Wiederholen)     │
│     └─→ Thermometer-Daten vollständig? (NEIN → Ergänzen)      │
│                                                                │
│  2. COMMON-MODE-SUBTRAKTION                                    │
│     └─→ ΔΦ = Φ_mess - Φ_ref berechnen                         │
│                                                                │
│  3. KONFOUND-AUSSCHLUSS                                        │
│     ├─→ Korrelation mit Beschleunigungssensor? → Vibration    │
│     ├─→ Korrelation mit RTD-Readings? → Thermisch             │
│     └─→ Korrelation mit Magnetometer? → Magnetisch            │
│                                                                │
│  4. SKALIERUNGSTESTS                                           │
│     ├─→ ΔΦ ∝ Δh (linear)? (NEIN → nicht SSZ)                  │
│     ├─→ ΔΦ ∝ ω (linear)? (NEIN → nicht SSZ)                   │
│     └─→ ΔΦ ∝ t (linear)? (NEIN → nicht SSZ)                   │
│                                                                │
│  5. KOMPENSATIONSTEST (entscheidend!)                          │
│     └─→ Φ_corr = -ω×r_s×Δh/R²×t anwenden                      │
│         └─→ ΔΦ_kompensiert ≈ 0? → SSZ BESTÄTIGT               │
│             └─→ NEIN → Konfound oder gemischtes Signal         │
│                                                                │
│  6. ERGEBNIS                                                   │
│     ├─→ Alle Tests bestanden: SSZ-KANDIDAT                    │
│     ├─→ Bounded Regime (ΔΦ ≈ 0): SSZ-KONSISTENT               │
│     └─→ Tests nicht bestanden: KONFOUND IDENTIFIZIERT          │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## C.7 Zusammenfassungstabelle

| Konfound | Physik | Diskriminator | Mitigation |
|----------|--------|---------------|------------|
| **Vibration** | Mechanische Kopplung | Impulsartig, nicht ∝ Δh | Isolation, Sensoren |
| **Thermisch** | Frequenzshift durch T | Korreliert mit RTD | Stabilisierung, Überwachung |
| **LO-Noise** | Phasenfluktuation | √t, nicht ∝ ω linear | Referenz-Qubits, stabiler LO |
| **Magnetisch** | Fluss-Noise | Positionsabhängig ≠ Δh | Abschirmung, Magnetometer |
| **Charge** | 1/f Noise | Lokal, unkorrelliert | Averaging, Transmon-Design |
| **SSZ** | Zeitdilatation | ∝ Δh × ω × t, Komp. reversiert | Keine nötig (deterministisch) |

Die Kombination aller Mitigationsmaßnahmen und Diskriminatoren ermöglicht eine robuste Identifikation von SSZ-Effekten und schließt Fehlinterpretationen systematisch aus.

---

© 2025 Carmen Wrede & Lino Casu
