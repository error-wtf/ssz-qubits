# SSZ SYMMETRY PROBE — [H, Q_SSZ] = 0? (Antwort auf Carmens Forschungsfrage, 31.10.)

**Frage (Carmen, 31.10.2026):** Kann die Segmentierung eine nichttriviale,
physikalisch begründete Symmetrie oder Erhaltungsgröße erzeugen, die den
6⊕2-Zustandsraum in invariante Sektoren zerlegt? Dazu: Operator aus der
SSZ-Mathematik herleiten und [H, Q_SSZ]=0 zeigen; Eigenräume {6,2} wären
eine echte strukturelle Verbindung, sonst bleibt 6⊕2 Drehimpulsalgebra.

## Methode (ausführbar: research/quantum_bus/ssz_symmetry_probe.py,
Tests: tests…::TestSSZSymmetryProbe, 13 Fälle)

1. **Inhaltsdefinition:** Im vorliegenden Korpus besteht SSZ aus lokalen
   skalaren Zeitfaktoren D(r_i) — die erzeugbare Operatorfamilie ist diagonal
   (Q = Σ c_i Z_i und Polynome davon). Kein Korpus-Zweig leitet einen
   nicht-scalaren Mehr-Segment-Operator her (Marolf-Constraint AX-M3).
2. **Kommutanten-Algebra:** Raum aller X mit [H,X]=0 exakt als Kernraum von
   (I⊗H − Hᵀ⊗I).
3. **D-Gitterscan:** 11³-Kombinationen (D_A, D_M, D_B), Singulett-Sektor-
   Leckage ‖P_S H (I−P_S)‖ je Punkt.
4. **Positivkontrollen:** Anregungszahl ΣZ/2 (bekannt) und der
   Spiegelsymmetrie-Fall.

## Befunde (alle testfixiert)

| # | Befund | Beleg |
|---|---|---|
| F1 | Generischer Bus (g_A≠g_B oder Differenzsegmentierung): Kommutant = {f(H)}, **dim = 8**. Jedes kommutierende Q_SSZ wäre f(H) mit den 8 eindimensionalen Eigenräumen — eine {6,2}-Zerlegung ist algebraisch ausgeschlossen. | `test_generic_exchange_bus_commutant_is_polynomials_in_H` |
| F2 | Spiegelsymmetrie (ω_A=ω_B, g_A=g_B, **D_A=D_B**): P_S ∈ Kommutant, Eigenwerte 0×6 + 1×2. Die Invarianz ist **A↔B-Permutation** (Singulett = antisymmetrischer Unterraum) — gewöhnliche Drehimpulsalgebra. | `test_singlet_projector_mirror_symmetric_case` |
| F3 | **D-Scan: Invarianz genau auf der D_A=D_B-Diagonale** (121/121 Punkte; 0 außerhalb; Leckage off-diagonal ≥ 1e-3). D_M ist tangential. | `test_invariance_only_on_the_DA_equals_DB_diagonal` |
| F4 | **Kernbefund:** Differenzsegmentierung D_A≠D_B **bricht** [H, P_S]=0 selbst bei sonst perfekter Spiegelsymmetrie — SSZ zerstört die 6⊕2-Invarianz, sobald die beiden Qubits unterschiedliche Segmentierung sehen (das ist der eigentliche SSZ-Anwendungsfall: qubit_pair_segment_mismatch). | `test_differential_segmentation_breaks_invariance`, `test_singlet_projector_broken_by_ssz_differential` |
| F5 | Diagonale SSZ-Größen: gleiche Koeffizienten ⇒ Anregungszahlerhaltung (kein SSZ-Inhalt); ungleiche Koeffizienten ⇒ Brechung der Austausch-Struktur. Kein Zwischenweg. | `TestDiagonalQFamilyCannotCommute` |

## Urteil (gelabelt)

**NEGATIV mit geschärftem Inhalt (`proven` auf Modell-Ebene, numerisch
abschließend für die skalare Formulierung):**

1. Ein Q_SSZ mit [H, Q_SSZ]=0 und Eigenräumen {6,2} existiert in der
   skalaren SSZ-Formulierung **nicht**.
2. Stärker: **6⊕2 wird erst invariant bei GLEICHER Segmentierung beider
   Qubits (D_A=D_B) und ist dann reine Permutationsalgebra; jedes
   Segmentierungs-DIFFERENZIAL zerstört sie.** SSZ-segmentierung trägt also
   nicht zur Zerlegung bei — sie ist ihr feindlich.
3. Die 6⊕2-Struktur des Korpus bleibt damit, was der Audit vermutete:
   **gewöhnliche Drehimpulsalgebra** (Singulett/Triplett-Basiswechsel).

## Was die Antwort ändern würde (offener Weg, präzise formuliert)

Ein nichttriviales Q_SSZ benötigt einen **nicht-scalaren, paar-korrelierenden
Operator aus Segmentfreiheitsgraden** (z.B. ein Segment-Paar-Korrelator, der
auf A und B gemeinsam wirkt). Kein aktueller Zweig leitet so etwas her —
das ist dieselbe Lücke wie COMMON_ACTION_GATE (f3/f4 als Zustandsfunktionen)
und der Marolf-Constraint (AX-M3: lokal-kinematische Modelle liefern keine
universell gekoppelte Gravitation). Solange dieser Schritt fehlt, bleibt
jede 6⊕2-Aussage über SSZ Drehimpulsalgebra — Status `RESEARCH_OPEN` mit
nun präziser Bedingung: *hergeleiter nicht-diagonaler Paar-Segment-Operator
oder negativ endgültig.*

## Reproduktion

```
python -m pytest research/quantum_bus/tests/test_ssz_symmetry_probe.py -v
# 13 passed; D-Scan: 1331 Punkte, Invarianz nur auf D_A=D_B-Diagonale
```
