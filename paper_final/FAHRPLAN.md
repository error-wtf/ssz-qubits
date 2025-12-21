# SSZ Unified Paper - Fahrplan

## Ziel
Vollständiges, journal-ready Paper aus allen SSZ-Quellen (A, B, C, D, E)

---

## Komponenten-Übersicht

### Sections (8 Hauptkapitel)
| Datei | Kapitel | Quelle |
|-------|---------|--------|
| `sections/00_abstract.md` | Abstract + Keywords | Master D |
| `sections/01_introduction.md` | Introduction, Scope, Claims | A, D |
| `sections/02_theory.md` | Segment Density, Time Dilation, Phase Drift | A, B |
| `sections/03_control.md` | Compensation Protocol, Scaling Signatures | B, D |
| `sections/04_experiments.md` | Experimental Designs, Upper Bounds | C v1.2 |
| `sections/05_entanglement.md` | Phase Preservation, Fidelity | B |
| `sections/06_engineering.md` | Layout, Compiler Integration | A, D |
| `sections/07_feasibility.md` | Platform Comparison, Future Regimes | C, D |
| `sections/08_conclusion.md` | Summary, Falsification Criteria | D |

### Tables (5 Tabellen)
| Datei | Inhalt | Referenz |
|-------|--------|----------|
| `tables/T1_symbols.md` | Symbol-Definitionen | Sec 1 |
| `tables/T2_signatures.md` | Confound Discrimination | Sec 3 |
| `tables/T3_platforms.md` | Platform Comparison (Drift) | Sec 4 |
| `tables/T4_experiments.md` | Experiment Configurations | Sec 4 |
| `tables/T5_regimes.md` | Claim Taxonomy (3 Regimes) | Sec 1 |

### Figures (6 Abbildungen)
| Datei | Beschreibung | Generator |
|-------|--------------|-----------|
| `figures/F1_phase_vs_height.py` | Phase Drift vs Δh | matplotlib |
| `figures/F2_platform_comparison.py` | Bar Chart Platforms | matplotlib |
| `figures/F3_confound_matrix.py` | Discrimination Heatmap | matplotlib |
| `figures/F4_ssz_vs_gr.py` | Time Dilation Comparison | matplotlib |
| `figures/F5_zone_width.py` | Coherent Zone z(ε) | matplotlib |
| `figures/F6_compensation.py` | With/Without Protocol | matplotlib |

### Appendices (4 Anhänge)
| Datei | Inhalt | Quelle |
|-------|--------|--------|
| `appendices/A_derivation.md` | Full Math Derivation | A, Master |
| `appendices/B_didactic.md` | Didactic Scaling Definition | B |
| `appendices/C_confounds.md` | Confound Playbook | C v1.2 |
| `appendices/D_constants.md` | Physical Constants | All |

### References
| Datei | Inhalt |
|-------|--------|
| `references.md` | Alle Quellen (BibTeX-Style) |

---

## Workflow

```
1. Tabellen erstellen (T1-T5)
2. Figure-Generatoren schreiben (F1-F6)
3. Appendices verfassen (A-D)
4. Sections verfassen (00-08)
5. References kompilieren
6. Alles via Python-Skript zu DOCX zusammenführen
```

---

## Konsistenz-Regeln

- **Notation**: Ξ(r) = r_s/(2r), D = 1/(1+Ξ), ΔD = r_s·Δh/R²
- **Konstanten**: r_s = 8.87 mm, R = 6.371×10⁶ m
- **Claim-Qualifier**: Immer Regime angeben (bounded/detection/future)
- **Didactic**: Explizit kennzeichnen, keine physikalischen Claims
- **Units**: SI, alle Formeln mit Unit-Check

---

## Dateistatus

| Komponente | Status | Dateien |
|------------|--------|---------|
| Fahrplan | ✓ | FAHRPLAN.md |
| Tables | ✓ | T1-T5 (5 Dateien) |
| Figures | ✓ | F1-F6 (6 Python-Skripte) |
| Appendices | ✓ | A-D (4 Dateien) |
| Sections | ✓ | 00-08 (9 Dateien) |
| References | ✓ | references.md |
| Assembler | ✓ | assemble_paper.py |

## Nächster Schritt

```bash
cd E:\clone\ssz-qubits\paper_final
python assemble_paper.py
```

Output: `output/SSZ_Unified_Paper.docx`
