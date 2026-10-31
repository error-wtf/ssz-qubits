# SSZ vs. GR im Busmodell — trennbare Vorhersagen (Phase 5)

**Kernfrage (Auftrag §6):** Welche SSZ-spezifische zusätzliche Größe tritt im
Busmodell gegenüber GR auf — ohne willkürliche Fit-Parameter?

## Antwort (ehrlich, gelabelt)

**`NO_DISTINGUISHING_PREDICTION`** — in der vorliegenden SSZ-Formulierung
(=`ssz-qubits`: lokale Zeit-/Frequenzfaktoren D(r) aus Ξ-Modellen) tritt im
Bus-Hamiltonoperator gegenüber einer GR-Baseline mit derselben lokalen
Gangunterschied-Funktion **kein zusätzlicher Term auf**. Die Modelle Q0–Q3
nutzen D nur als skalaren Vorfaktor in Frequenzen (`D(r_i)·ω_i`); GR liefert
über die PPP/Schwarzschild-Zeitdilatation denselben strukturellen Term. Was
sich unterscheidet, ist allein der ZAHLENWERT von D(r) — und dort ist der
führende Fernfeldkoeffizient von Ansatz A (φ vs. 1/2, Faktor 2φ) bereits
durch Cassini/LLR ausgeschlossen (R4/MODEL_TABLES.md). Keine modellfreie
φ-Kopplung ist hergeleitet; eine zu erfinden wäre verboten (Auftrag §6).

## Drei getrennte Konfigurationen (Struktur, nicht ausgeführte Physik)

| Konfiguration | Zeitfaktor | Bus-Hamiltonterm | SSZ-Zusatz |
|---|---|---|---|
| GR-baseline | D_GR(r)=√(1−r_s/r) (Koordinaten: Schwarzschild-areal; Gültigkeit r>r_s) | ω_i^GR = ω_i⁰·D_GR(r_i) | — |
| SSZ-legacy | D aus Ξ-Modellen des Repos (A/weak; Fehler dokumentiert, R1–R4) | ω_i^SSZ = ω_i⁰·D_SSZ(r_i) | none — nur Zahlenwert |
| SSZ-candidate | OFFEN: bräuchte eine HERGELEITETE Segment-/JIF-Kopplung an die Bus-Wechselwirkung (z.B. modulierte g_ij) — existiert nicht im Korpus | — | undefiniert ⇒ keine testbare Vorhersage |

**Gemeinsame Zeitparametrisierung (Auftrag §6):** für räumlich verteilte
gekoppelte Qubits definiert EIN Beobachter die Koordinatenzeit t; lokale
Eigenzeiten dτ_i = D_i dt erscheinen als lokale Frequenzskalen ω_i·D_i im
Hamiltonoperator. Addiert man unterschiedliche Eigenzeiten direkt in eine
Matrix, ist das eine Koordinatenverletzung (nicht getan — und als Fehler
dokumentiert, falls in Alt-Code auffindbar: `ssz_roadmap_validation.py`
verwendet nur skalare Phasen, keine Eigenzeit-Matrix — geprüft).

## Falsifikationsmatrix (Struktur mit ehrlichen Einträgen)

| Observable | GR-Wert | SSZ-Wert (Ansatz A) | Differenz | freie Parameter | Status |
|---|---|---|---|---|---|
| Relative Phase 1 mm Höhe, 5 GHz, 50 ns | 1.7143e−16 rad (PPP, β=γ=1) | 1.71628e−16 rad (stabile Differenz) | ~0.1 % (2φ-Effekt im Koeffizienten) | KEINE | RECHENVORHERSAGE; Messung fehlt; unter jedem realen Rauschen (T2 ~ 100 µs ⇒ Phasenrauschen ≫) |
| Dispersiver Shift Q2 | g²/Δ-Standard | identische Struktur (D skaliert nur ω) | none | — | NO_DISTINGUISHING_PREDICTION |
| Entangle-fähiger Bus | braucht Wechselwirkungsterm | keine SSZ-Herleitung eines solchen | — | — | SSZ-LÜCKE (nicht widerlegt, nicht belegt) |
| GPS/Pound-Rebka/NIST | bestätigen Standard-GR | identisch im Weak Field | < 1e−9 | — | KEINE neuartigen SSZ-Quanteneffekte belegt (Claims Register) |

## Grenzen (explizit)

- Labor-Qubits testen ANALOGE Horizont-/Scrambling-Eigenschaften höchstens,
  niemals automatisch echte Hawking-Strahlung astrophysikalischer
  Raumzeiten; keine Vermengung mit 10→8-Lichtkegel-Strings oder AdS/CFT
  ohne Abbildung von Algebra, Symmetrie, Observablen, Dynamik
  (Auftrag §6; DIMENSION_LEDGER.md C).
- Signalgrößen (1e−16 rad/Gate) sind gegen Frequenzauflösung, T1/T2,
  Rauschen und thermische Besetzung abzuwägen — aktuelle realistische
  Schätzungen: NICHT messbar an Supraleitern ohneOrders Magnituden neuer Physik.
