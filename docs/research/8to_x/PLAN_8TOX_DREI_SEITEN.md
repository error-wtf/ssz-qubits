# PLAN_8TOX_DREI_SEITEN.md — Untersuchungsplan: „8 Zustandsrichtungen, aber
# nur 6/2 beobachtbar, dynamisch zugänglich oder unabhängig"
(Carmens Direktive 31.10.: keine weiteren skalaren Modellvarianten; die
290→307 Tests sind die ABGESCHLOSSENE Prüfung dieses speziellen Qubit-Modells,
nicht die Antwort auf die allgemeine 8→x-Frage. Dieses Dokument ist ein
Arbeitsplan — keine Physikbehauptung und kein neues Modell.)

## Die Frage präzise

Was bedeutet es physikalisch, wenn eine Theorie acht Zustandsrichtungen hat,
aber nur sechs oder zwei davon (i) beobachtbar, (ii) dynamisch zugänglich
oder (iii) unabhängig sind? Drei Untersuchungsseiten, drei verschiedene
Bedeutungen von „weg" — die Vermischung dieser Bedeutungen ist der
Hauptfehlermodus der bisherigen 8→x-Diskussion.

## Seite 1 — ZWANGSBEDINGUNGEN (Was ist redundant?)

Existierender Anker: DIMENSION_ONTOLOGY_MATRIX.csv (Zeilen: relativistisches
Teilchen, Feldtheorie-Constraints), Dirac-Zählung als Standard.

Zu leisten morgen:
1. Für das Q1-Qubit-Modell explizit entscheiden: gibt es ÜBERHAUPT
   Constraint-Redundanz? (Erwartung basierend auf Kommutanten-Analyse: NEIN —
   alle 8 Basen sind physikalisch; 6⊕2 ist Koordinatenwahl, kein Zwang.
   Das muss als Negativbefund dokumentiert werden, nicht als Lücke.)
2. Kontrastfälle aus der Taxonomie: Wo ist „wegfallen" Eichfreiheit
   (Lichtkegel: 2.longitudinale Moden = Zwang), wo Massenschale, wo nichts?
3. Kriterium formulieren: Ein Sektor ist „zwangsredundant" gdw. er in KEINER
   Observablen auftritt UND die Dynamik ihn nicht erreichbar macht — mit
   maschinenprüfbarem Test im Qubit-Kontrastmodell.

## Seite 2 — INFORMATIONSZUGÄNGLICHKEIT (Was ist messbar?)

**Leitfrage (formuliert von Lino/Carmen, 31.10.):**
> Welche Eigenschaften des Gesamtsystems lassen sich aus einem
> eingeschränkten Beobachtungskanal rekonstruieren?
Mathematisch untersuchbar ohne neue Kosmologie; Rekonstruktionstheorie
(Quantum Tomography, channel identification) liefert den Werkzeugkasten.

**Begriffsfeinheit geklärt (Carnens Einwand, 31.10.):** „2 von 8" ist KEIN
algebraischer Rang (weder Projektionsrang noch Rang eines linearen
Beobachtungsoperators), sondern operationale Aussage: Die Outcome-Abbildung
ρ ↦ (Tr E₀ρ, Tr E₁ρ) mit E_m = I_AB⊗|m⟩⟨m| faktorisiert über die
M-Reduktion; Zustände sind kanal-unterscheidbar ⟺ ihre M-Reduktionen
verschieden sind. Beide Richtungen ⟺ sind testfixiert
(`test_outcome_map_factors_through_M_reduction_iff`).

Existierender Anker: photon_channel_demo.py (Messblindheit als
Kanaleigenschaft, in keine Richtung ontologisch verwertbar), partial_trace-
Analysen, CHSH/Fidelity-Instrumente in reduction.py.

Zu leisten morgen:
1. Zugänglichkeits-Hierarchie formalisieren: Detektor-Algebra A_obs ⊂ B(H);
   „beobachtbar" = Separierbarkeit durch A_obs. Für den M-Kanal: Rang 2 von 8
   (bereits demonstriert) — Verallgemeinerung: minimaler Satz von Kanälen,
   der 8 von 8 trennt (Tomographie-Bedarf vs. Sektor-Zugriff).
2. Identifizierbarkeits-Kriterium: zwei Zustände sind A_obs-äquivalent gdw.
   Tr(ρ E) = Tr(ρ' E) ∀ E ∈ A_obs. Für Q1: welche (A_obs, Dynamik)-Paare
   lassen 6 bzw. 2 Richtungen „verschwinden", ohne dass sie weg sind?
3. Bindung an Carmen: aus Unsichtbarkeit folgt weder Nichtexistenz noch
   Existenz (photon_channel_demo-Doku, beide Richtungen verboten).

## Seite 3 — TATSÄCHLICHE DYNAMIK (Was ist erreichbar/instabil?)

Existierender Anker: Q_SSZ-Probe (Invarianz nur bei Spiegelsymmetrie),
Mischterm-Analyse (S↔T0-Rabi, 2φ ausgeschlossen), bus_effective (SW/Schur,
Resonanz-Ausfall).

Zu leisten morgen:
1. Erreichbarkeits-Semantik: „dynamisch weg" kann heißen (a) invariant
   entkoppelt (Singulett bei Spiegelsymmetrie), (b) nicht anregbar aus dem
   Initialzustand (Auswahl nach Erhaltungsgröße ΣZ), (c) leckend (Mischterm
   ≠ 0). Für jede der drei 8→x-Zerlegungen festnageln, welche Bedeutung vorliegt.
2. Trennung (Carmens Kernpunkt): 6↔2-Mischung erzeugt KEINE Dimensions-
   reduction — die Unitarität auf C⁸ bleibt bijektiv; Mischung verschiebt
   nur Population zwischen Blöcken. Formaler Einzeiler mit Test im bestehenden
   Modell (keine neue Variante: propagate + Sektorpopulationen genügt).
3. Stabilitätsfrage: ist 6⊕2 unter Störungen (D_A−D_B ≠ 0) OPEN oder
   STABLE-broken? (Bekannt: bricht sofort — einordnen als „strukturell
   fragil, nicht topologisch geschützt".)

## Deliverables morgen (Vorschlag)

- OBSERVABILITY_HIERARCHY.md (Seiten 1+2, mit Negativbefund „keine
  Constraint-Redundanz im Qubit-Modell")
- ein ausführbarer Identifizierbarkeits-Test (Seite 2, im bestehenden
  photon_channel_demo-Modell — keine neue Modellklasse)
- Erreichbarkeits-Matrix (Seite 3) als Ergänzung der
  DIMENSION_ONTOLOGY_MATRIX.csv

## Bewahrte negative Ergebnisse (nicht verlieren)

- Q_SSZ negativ (skalare Klasse, bedingt) — SSZ_SYMMETRY_PROBE_Q.md
- Mischterm = Bell-projizierte Zeitdilatation; 2φ EXCLUDED_IN_MODEL —
  SSZ_SINGLET_MIXING_OBSERVABLE.md
- K_AB-Herleitung offen — SSZ_QUBUS_CONSTRAINTS.md G1
- 6⊕2 = Drehimpulsalgebra — SYM_COMP_COMMUTANT_PROOF.md
