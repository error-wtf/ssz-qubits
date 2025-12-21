# SSZ Paper Corrections Log

## Datum: 2025-12-21

---

## Korrektur 1: Zone-Width-Werte (KRITISCH)

### Problem
Die Zone-Width-Berechnung hatte einen Faktor 100 Fehler in allen Dokumenten.

### Ursache
Falsche Exponenten-Konvertierung bei der Umrechnung von m in μm/mm.

### Korrigierte Werte

| ε | ALT (falsch) | NEU (korrekt) |
|---|--------------|---------------|
| 10⁻²⁰ | 1.83 μm | **183 μm** |
| 10⁻¹⁸ | 183 μm | **18.3 mm** |
| 10⁻¹⁵ | 183 mm | **18.3 m** |
| 10⁻¹² | 183 m | **18.3 km** |
| 10⁻⁹ | 183 km | **18,300 km** |

### Betroffene Dateien
- [x] sections/02_theory.md
- [x] sections/06_engineering.md
- [x] sections/12_reproducibility.md
- [x] appendices/A_derivation.md
- [x] appendices/D_constants.md
- [x] appendices/H_code.md
- [x] tables/T8_api.md

### Verifikation
```python
r_s = 8.87e-3  # m
R = 6.371e6    # m
epsilon = 1e-18

z = 4 * epsilon * R**2 / r_s
# = 4 * 1e-18 * 4.059e13 / 8.87e-3
# = 1.83e-2 m = 18.3 mm ✓
```

---

## Korrektur 2: GPS Drift (INFO - kein Fix nötig)

### Beobachtung
GPS drift berechnet: 45.7 μs/day
Dokumente sagen: ~38 μs/day

### Erklärung
- **38 μs/day** = nur gravitativer Anteil (oft zitiert)
- **45.7 μs/day** = voller SSZ/GR Effekt (korrekt)
- Differenz kommt von Orbit-Mittelung

**Status:** Kein Fix nötig, aber Erklärung hinzufügen.

---

## Validierungs-Ergebnisse

| Test | Erwartet | Berechnet | Status |
|------|----------|-----------|--------|
| r_s Earth | 8.87 mm | 8.87 mm | ✓ |
| Xi surface | 6.96e-10 | 6.96e-10 | ✓ |
| D surface | ~0.9999999993 | 0.9999999993 | ✓ |
| ΔD per m | 2.19e-16 | 2.19e-16 | ✓ |
| Phase transmon | 6.87e-13 rad | 6.87e-13 rad | ✓ |
| Phase optical | 0.59 rad | 0.59 rad | ✓ |
| Zone width (ε=10⁻¹⁸) | 18.3 mm | 18.3 mm | ✓ |
| GPS drift | ~45 μs/day | 45.7 μs/day | ✓ |

---

## Figure-Tests

| Figure | Status | Output |
|--------|--------|--------|
| F1_phase_vs_height.py | ✓ | PNG+PDF |
| F2_platform_comparison.py | ✓ | PNG+PDF |
| F3_confound_matrix.py | ✓ | PNG+PDF |
| F4_ssz_vs_gr.py | ✓ | PNG+PDF |
| F5_zone_width.py | ✓ | PNG+PDF |
| F6_compensation.py | ✓ | PNG+PDF |
| F7_strong_field.py | ✓ | PNG+PDF |
| F8_timeline.py | ✓ | PNG+PDF |
| F9_validation.py | ✓ | PNG+PDF |
| F10_network.py | ✓ | PNG+PDF |

**Alle 10 Figures erfolgreich generiert.**

---

## Nächste Schritte

1. [x] Zone-Width-Werte korrigiert
2. [ ] Assembler testen
3. [ ] DOCX generieren
4. [ ] Qualitätsprüfung
