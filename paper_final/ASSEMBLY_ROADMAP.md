# SSZ Mega-Paper Assembly Roadmap

## Ziel
Aus allen vorbereiteten Komponenten ein finales **80+ Seiten DOCX** generieren.

---

## Inventar (Stand: 2025-12-21)

### Sections (14 Dateien, ~85 KB)
| Nr | Datei | Größe | Seitenschätzung |
|----|-------|-------|-----------------|
| 1 | 00_abstract.md | 2.5 KB | 1 S. |
| 2 | 01_introduction.md | 4.4 KB | 2 S. |
| 3 | 01b_history.md | 5.9 KB | 3 S. |
| 4 | 02_theory.md | 4.8 KB | 3 S. |
| 5 | 02b_strong_field.md | 5.4 KB | 3 S. |
| 6 | 03_qubit_physics.md | 6.3 KB | 4 S. |
| 7 | 03_control.md | 5.0 KB | 3 S. |
| 8 | 04_experiments.md | 6.4 KB | 4 S. |
| 9 | 05_entanglement.md | 5.4 KB | 3 S. |
| 10 | 06_engineering.md | 7.8 KB | 5 S. |
| 11 | 07_feasibility.md | 6.6 KB | 4 S. |
| 12 | 08_conclusion.md | 6.7 KB | 4 S. |
| 13 | 10_roadmap.md | 9.6 KB | 6 S. |
| 14 | 12_reproducibility.md | 8.1 KB | 5 S. |
| **Summe** | | **~85 KB** | **~50 S.** |

### Tables (8 Dateien, ~15 KB)
| Nr | Datei | Inhalt | Seitenschätzung |
|----|-------|--------|-----------------|
| T1 | T1_symbols.md | Symboldefinitionen | 1 S. |
| T2 | T2_signatures.md | Confound Discrimination | 1 S. |
| T3 | T3_platforms.md | Platform Comparison | 1 S. |
| T4 | T4_experiments.md | Experiment Configs | 1 S. |
| T5 | T5_regimes.md | Claim Taxonomy | 1 S. |
| T6 | T6_validation.md | Experimental Validation | 1 S. |
| T7 | T7_roadmap.md | Timeline | 2 S. |
| T8 | T8_api.md | API Reference | 2 S. |
| **Summe** | | | **~10 S.** |

### Figures (10 Python-Skripte)
| Nr | Datei | Beschreibung | Platzierung |
|----|-------|--------------|-------------|
| F1 | F1_phase_vs_height.py | Phase vs Höhe | Sec 2 |
| F2 | F2_platform_comparison.py | Platform SNR | Sec 4 |
| F3 | F3_confound_matrix.py | Confound Heatmap | Sec 3 |
| F4 | F4_ssz_vs_gr.py | SSZ vs GR | Sec 2 |
| F5 | F5_zone_width.py | Zone Width | Sec 6 |
| F6 | F6_compensation.py | Compensation Protocol | Sec 3 |
| F7 | F7_strong_field.py | Strong Field | Sec 2b |
| F8 | F8_timeline.py | Roadmap Gantt | Sec 10 |
| F9 | F9_validation.py | Validation History | Sec 1b |
| F10 | F10_network.py | Network Diagram | Sec 6 |
| **Summe** | | | **~10 S.** |

### Appendices (8 Dateien, ~50 KB)
| Nr | Datei | Inhalt | Seitenschätzung |
|----|-------|--------|-----------------|
| A | A_derivation.md | Mathematische Ableitung | 2 S. |
| B | B_didactic.md | Didactic Scaling | 2 S. |
| C | C_confounds.md | Confound Playbook | 4 S. |
| D | D_constants.md | Physikalische Konstanten | 3 S. |
| E | E_transition.md | Weak/Strong Transition | 3 S. |
| F | F_platforms.md | Platform Specs | 3 S. |
| G | G_statistics.md | Statistical Methods | 4 S. |
| H | H_code.md | Code Listings | 5 S. |
| **Summe** | | | **~26 S.** |

### References
| Datei | Quellen | Seitenschätzung |
|-------|---------|-----------------|
| references.md | 33 | 3 S. |

---

## Seitenberechnung

| Komponente | Seiten |
|------------|--------|
| Titelseite + TOC | 3 |
| Sections (14) | 50 |
| Tables (inline) | 10 |
| Figures (inline) | 10 |
| Appendices (8) | 26 |
| References | 3 |
| **GESAMT** | **~102 S.** |

---

## Assembly-Fahrplan (7 Phasen)

### Phase 1: Figure-Generierung ⏱️ 10 min
```bash
cd E:\clone\ssz-qubits\paper_final\figures
mkdir -p ../output/figures

# Alle Figures generieren
python F1_phase_vs_height.py
python F2_platform_comparison.py
python F3_confound_matrix.py
python F4_ssz_vs_gr.py
python F5_zone_width.py
python F6_compensation.py
python F7_strong_field.py
python F8_timeline.py
python F9_validation.py
python F10_network.py

# Prüfen: 10 PNG + 10 PDF
ls ../output/figures/
```

**Ergebnis:** 10 PNG-Dateien in `output/figures/`

---

### Phase 2: Assembler-Erweiterung ⏱️ 20 min

Der `assemble_paper.py` muss erweitert werden für:

1. **Erweiterte Kapitelreihenfolge:**
```python
SECTION_ORDER = [
    "00_abstract",
    "01_introduction",
    "01b_history",
    "02_theory",
    "02b_strong_field",
    "03_qubit_physics",
    "03_control",
    "04_experiments",
    "05_entanglement",
    "06_engineering",
    "07_feasibility",
    "08_conclusion",
    "10_roadmap",
    "12_reproducibility",
]
```

2. **Figure-Zuordnung:**
```python
FIGURE_PLACEMENT = {
    "02_theory": ["F1_phase_vs_height", "F4_ssz_vs_gr"],
    "02b_strong_field": ["F7_strong_field"],
    "01b_history": ["F9_validation"],
    "03_control": ["F3_confound_matrix", "F6_compensation"],
    "04_experiments": ["F2_platform_comparison"],
    "06_engineering": ["F5_zone_width", "F10_network"],
    "10_roadmap": ["F8_timeline"],
}
```

3. **Table-Integration:**
```python
TABLE_PLACEMENT = {
    "02_theory": ["T1_symbols"],
    "03_control": ["T2_signatures"],
    "04_experiments": ["T3_platforms", "T4_experiments"],
    "07_feasibility": ["T5_regimes"],
    "01b_history": ["T6_validation"],
    "10_roadmap": ["T7_roadmap"],
    "12_reproducibility": ["T8_api"],
}
```

4. **Appendix-Reihenfolge:**
```python
APPENDIX_ORDER = ["A", "B", "C", "D", "E", "F", "G", "H"]
```

---

### Phase 3: Markdown-Verbesserungen ⏱️ 15 min

Prüfen und ggf. anpassen:
- [ ] Konsistente Heading-Level (# für Kapitel, ## für Unterkapitel)
- [ ] Keine Unicode-Probleme (Windows cp1252)
- [ ] Code-Blöcke korrekt formatiert
- [ ] Tabellen-Syntax korrekt
- [ ] Cross-References (Fig. X, Tab. Y, Sec. Z)

---

### Phase 4: DOCX-Generierung ⏱️ 5 min
```bash
cd E:\clone\ssz-qubits\paper_final
python assemble_paper.py
```

**Ergebnis:** `output/SSZ_Unified_Paper.docx`

---

### Phase 5: Qualitätsprüfung ⏱️ 20 min

**Checkliste:**
- [ ] Seitenzahl ≥ 80
- [ ] Alle 14 Sections enthalten
- [ ] Alle 10 Figures eingefügt und lesbar
- [ ] Alle 8 Tables formatiert
- [ ] Alle 8 Appendices vorhanden
- [ ] 33 References gelistet
- [ ] TOC korrekt
- [ ] Keine leeren Seiten
- [ ] Formeln lesbar
- [ ] Code-Blöcke monospace

---

### Phase 6: Korrekturen ⏱️ variabel

Falls Probleme gefunden:
1. Markdown-Quellen korrigieren
2. Assembler anpassen
3. Erneut generieren
4. Erneut prüfen

---

### Phase 7: Finalisierung ⏱️ 5 min

1. Finale Version speichern
2. PDF-Export (optional)
3. Git commit + push
4. Backup erstellen

---

## Detaillierte Kapitelstruktur

### Hauptteil (50 Seiten)

```
PART I: FOUNDATIONS (15 S.)
├── 1. Introduction and Scope (2 S.)
├── 1b. Historical Background (3 S.) [F9, T6]
├── 2. Theory: Deriving SSZ Phase Drift (3 S.) [F1, F4, T1]
└── 2b. Strong Field Extension (3 S.) [F7]

PART II: QUANTUM SYSTEMS (14 S.)
├── 3. Qubit Physics and SSZ (4 S.)
├── 3b. Control and Compensation (3 S.) [F3, F6, T2]
├── 4. Experiments and Feasibility (4 S.) [F2, T3, T4]
└── 5. Entanglement and Phase (3 S.)

PART III: APPLICATIONS (15 S.)
├── 6. Engineering Implications (5 S.) [F5, F10]
├── 7. Feasibility Landscape (4 S.) [T5]
└── 8. Conclusion (4 S.)

PART IV: FUTURE (11 S.)
├── 10. Research Roadmap (6 S.) [F8, T7]
└── 12. Reproducibility (5 S.) [T8]
```

### Appendices (26 Seiten)

```
APPENDICES
├── A. Full Mathematical Derivation (2 S.)
├── B. Didactic Scaling Definition (2 S.)
├── C. Confound Playbook (4 S.)
├── D. Physical Constants (3 S.)
├── E. Weak-Strong Transition (3 S.)
├── F. Platform Specifications (3 S.)
├── G. Statistical Methods (4 S.)
└── H. Code Listings (5 S.)
```

---

## Zeitleiste

| Phase | Dauer | Kumulativ |
|-------|-------|-----------|
| 1. Figures | 10 min | 10 min |
| 2. Assembler | 20 min | 30 min |
| 3. Markdown | 15 min | 45 min |
| 4. DOCX | 5 min | 50 min |
| 5. Prüfung | 20 min | 70 min |
| 6. Korrekturen | ~30 min | 100 min |
| 7. Finalisierung | 5 min | **105 min** |

**Geschätzte Gesamtzeit: ~2 Stunden**

---

## Abhängigkeiten

```
Figures → Assembler → DOCX → Prüfung → Korrektur → Final
           ↑
         Markdown
           ↑
         Tables
           ↑
        Appendices
           ↑
        References
```

---

## Risiken und Mitigationen

| Risiko | Wahrscheinlichkeit | Mitigation |
|--------|-------------------|------------|
| Unicode-Fehler | Mittel | UTF-8 encoding erzwingen |
| Figure-Fehler | Niedrig | Einzeln testen |
| Formatierungsfehler | Mittel | Iterative Prüfung |
| Zu kurz (<80 S.) | Niedrig | Mehr Erklärungen |
| Zu lang (>120 S.) | Niedrig | Akzeptabel |

---

## Nächster Schritt

```
→ Phase 1: Figures generieren
  cd E:\clone\ssz-qubits\paper_final\figures
```
