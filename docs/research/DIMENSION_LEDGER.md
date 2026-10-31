# DIMENSION LEDGER — die verschiedenen „Acht" (Phase 3)

**Zweck (Auftrag §4):** präzise Definition, Raum, mathematische Reduktion,
erhaltene Observable, nötige Annahmen — strikt getrennt. Keine dieser Zeilen
darf mit einer anderen gleichgesetzt werden.

## A. Drei zweistufige Quantensysteme („8 = C⁸")

| Attribut | Inhalt |
|---|---|
| Objekt | H = (C²)⊗³ ≅ C⁸ — drei Spin-1/2-Qubits |
| „8" | Anzahl **komplexer Basisrichtungen** |
| Allgemeiner reiner Zustand | 2·8−2 = **14 reelle Parameter** (Normierung + globale Phase) |
| „8 = 6 + 2" | unitäre **Basiswechsel** via Singulett/Triplett des ersten Paares: (3⊗2) ⊕ (1⊗2) = C⁶ ⊕ C² — eine Aufteilung, KEINE Eliminierung |
| Erhaltene Observable | Alle (unitäre Transformation: Skalarprodukte, Orthogonalität, Verschränkung invariant) |
| Annahmen | Keine über Physik hinaus — reine lineare Algebra |
| Code-Referenz | `research/quantum_bus/explicit_6plus2.py` (Phase 4) |

## B. Klassisches relativistisches Teilchen („8D Phasenraum")

| Attribut | Inhalt |
|---|---|
| Objekt | (x^μ, p_μ), μ=0..3 — **8D reeller Phasenraum** |
| Reduktion | Massenschale p²=m² (1 Bedingung) + Weltlinien-Reparametrisierung (1 Redundanz) ⇒ **6D reeller physikalischer Phasenraum** im regulären Bereich |
| Erhaltene Observable | Poincaré-Invarianten (Masse, Spin); kein Zustandsvektor |
| Annahmen | Klassisch, keine Quantisierung; „8" ist REELLE Dimension — **keine Gleichsetzung mit C⁸ aus A** |
| Status | Standardmechanik (Lehrbuch); kein SSZ-Inhalt |

## C. Superstring-Lichtkegel („10 → 8")

| Attribut | Inhalt |
|---|---|
| Objekt | 10D Zielraumzeit; Lichtkegelgauge x⁺ = x⁰+x⁹ fixiert |
| „8" | **8 transversale Bosonen-Koordinaten** X^i, i=1..8 nach Eich-/Virasoro-Reduktion |
| Richtung | **10 → 8** — NICHT 8→6, NICHT 8→2, KEIN Quantum Bus |
| Erhaltene Observable | Transversale Oszillatoren; a=1 (offener String) folgt aus der Algebra |
| Annahmen | Volle String-Algebra (Virasoro) — nur als klar beschrifteter VERGLEICH, kein SSZ-Nachweis |
| Status | external_literature_fact (Green/Schwarz/Witten; Polchinski Bd. 1) |

## D. „8 → 2" — four distinct meanings (ohne Definition untestbar)

1. **C⁸ → C²**: lineare Abbildung mit Kernrang ≥ 6 — kann beliebige Inputs NICHT
   verlustfrei unitär erhalten (Rangsatz). Projektion braucht Erfolgswahrscheinlichkeit
   + Restausgänge (Messung) oder Dissipation (Kanal → Umgebung trägt Info).
2. **8 Qubits → 2 Qubits**: C²⁵⁶ → C⁴ — noch stärkere Beschränkung; dieselbe Logik.
3. **8 reelle Koordinaten → 2 reelle**: siehe 1 (reeller Rangsatz).
4. **8 Komponenten → 2 Polarisationen**: physikalisches Beispiel: Masselosse
   Spin-1-Felder nach Eichbedingungen (Photon: 4 Komponenten → 2 Polarisationen);
   kein „Dimensionsverlust", sondern Eichfreiheitsgrade.
   **Status:** RESEARCH_OPEN nur in dem Sinn, dass die SSZ-Doku diese Begriffe
   vermischt hat; mathematisch ist alles above Standard.

## E. Was daraus für SSZ folgt — und was nicht

- Es gibt im `ssz-qubits`-Korpus **keinen hergeleiteten Mechanismus** 8→6 oder
  8→2 (kein Term, kein Constraint; audit §„Schumann, Schur und 8→6/8→2").
  Eine ehrliche NEGATIVE Antwort ist das Forschungsergebnis (Auftrag §10).
- Was KONSTRUIERT werden kann (Phase 4): (i) Basiswechsel 8=6⊕2 mit
  Blockstruktur je nach Hamilton-Symmetrie; (ii) effektive Elimination
  8→6 im Niederenergie-Sektor via Schur-Komplement/Schrieffer-Wolff mit
  kontrollierter Fehlerordnung g/Δ; (iii) Projektion/Postselektion mit
  Erfolgswahrscheinlichkeiten; (iv) Trunkierung (Resonator: 4(n_max+1)).
  Invariant bleibt jeweils NUR der geschützte Unterraum — das Gesamtsystem
  wird durch Spur/Projektion nicht kleiner.
- **SSZ-spezifischer Zusatz:** keine hergeleitete zusätzliche Größe bekannt
  (siehe `docs/research/SSZ_VS_GR_BUS_PREDICTIONS.md`: falls das Busmodell nur
  bekannte Zeitdilatation einsetzt → Label `NO_DISTINGUISHING_PREDICTION`).
