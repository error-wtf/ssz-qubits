# TEST_BEWEISWERT_REGISTER.md — Klassifikation aller 307 Tests nach Aussagekraft
(Carmen, 31.10.: „Anzahl allein misst nicht die physikalische Tragweite."
Dieses Register klassifiziert jede Testdatei nach dem Beweiswert ihrer
bestandenen Fälle. Inventar: pytest --collect-only, 307/307, Stand HEAD
siehe git log. Erzeugt am 31.10.)

## Beweiswert-Tiers (absteigend nach physikalischer Tragweite)

**Tier A — Diskriminations-/Falsifikationskraft (23 Tests)**
Tests, die einen Unterschied zwischen Hypothesen MACHEN und eine hypothetische
Abweichung DETEKTIEREN würden. Bestehen = der untersuchte Mechanismus liefert
keinen unterscheidbaren/neuen Effekt (Negativbefund mit Ausschlusskraft im
Modell). NICHT: Beweis, dass jede mögliche Kopplung ausgeschlossen ist.

**Tier B — Symbolisch exakte Identität (13 Tests)**
Algebraische Herleitungen mit sympy (charpoly, Kommutator-Nullmatrix,
Projektor-Spuren). Bestehen = mathematischer Satz über das Modell (exakt,
keine Toleranzen). NICHT: Physik jenseits des Modells.

**Tier C — Dynamische Vorhersagen im Modell (79 Tests)**
Zeitentwicklungs-, Verschränkungs-, Eliminations- und Sektorprüfungen gegen
numerisch/exakte Referenzen. Bestehen = das Modell verhält sich wie
hergeleitet (inkl. Skalierungen O(g²), Resonanz-Ausfall). NICHT: Validierung
von SSZ als Gravitationstheorie.

**Tier D — Reparatur-Regressionen mit RED/GREEN-Nachweis (56 Tests)**
Jeder Fix aus dem Audit (R1–R5) hat einen dokumentierten roten Lauf (alter
Fehler reproduziert) und grünen Lauf (nach Fix); Toleranzen wurden nie erhöht.
Bestehen = die im Audit dokumentierten Fehler sind behoben und nicht
zurückgefallen. Beweiswert hoch FÜR DIE IMPLEMENTIERUNG; die physikalische
Modellwahl (φ-Koeffizienten) ist damit nicht gerechtfertigt.

**Tier E — Dokumentarische Kohärenz & Software-Architektur (136 Tests)**
Konsistenz von Dokumentzahlen mit Code, Exit-Code-Verhalten, Grenzfälle der
Implementierung, Paper-Support-Zahlen. Bestehen = Repo ist in sich sauber.
KEIN direkter Physikgehalt — aber Voraussetzung für Vertrauen in A–D.

## Register (pro Datei; Sub-Klassifikationen in Klammern)

| Datei | n | Tier | Inhalt / Anmerkung |
|---|---|---|---|
| research/…/test_ssz_symmetry_probe.py | 13 | **A** (teils B) | Q_SSZ-Negativsuite; D-Gitterscan (Invarianz nur bei D_A=D_B); Kommutant dim 8 (B); Positivkontrolle Permutationsalgebra |
| research/…/test_ssz_mixing_analysis.py | 6 | **A** (B, C) | Mischmatrixelement exakt (B); Rabi C; **2φ-Fernfeldausschluss = Tier-A-Falsifikation** (bereits durch Cassini/LLR gedeckt); kein-Bus-Negativkontrolle |
| research/…/test_photon_channel_demo.py | 4 | **A** (C) | Identifizierbarkeit: gleiche M-Statistik bei verschiedenen Zuständen; Negativkontrollen in beide Ontologie-Richtungen; Verlustdynamik C |
| research/…/test_symbolic_and_schur.py | 13 | **B** (C, A-Kontrollen) | charpoly/Kommutator/Drive-Symmetrie symbolisch (B); Schur-Residual + O(g²) (C); generisch-≠0- und asymm.-Drive-Kontrollen (A) |
| research/…/test_quantum_bus.py | 24 | **C** (A) | Q0-Nullmodell, 6⊕2 numerisch, SW ∝ g²/Δ, Resonanz-Kollaps (A-Negativtest), CHSH/Tsirelson |
| tests/test_entanglement.py | 23 | C | Verschränkungsmaße im Modell |
| tests/test_ssz_physics.py | 17 | C | Physikfunktionen gegen Erwartungswerte |
| tests/test_ssz_qubit_applications.py | 15 | C | Anwendungs-Szenarien im Modell |
| tests/test_regressions_audit.py | 20 | **D** | R1/R3: RED 13 failed dokumentiert → GREEN |
| tests/test_regressions_r2_models.py | 23 | **D** | R2 Modelltaxonomie; legacy_auto bit-kompatibel |
| tests/test_regressions_r4r5_limits.py | 13 | **D** | R4/R5 Limes-/Claim-Korrekturen; 2φ-Konsistenz |
| tests/test_paper_d_validation.py | 32 | E | Doku↔Code-Zahlen |
| tests/test_edge_cases.py | 27 | E | Implementierungs-Grenzfälle |
| tests/test_paper_c_support.py | 19 | E | dito |
| tests/test_roadmap_validation.py | 18 | E | dito |
| tests/test_validation.py | 17 | E | Runner/Exit-Codes |
| tests/test_paper_a_support.py | 16 | E | dito |
| tests/test_standalone_scripts.py | 4 | E | T1–T3: sys.exit-Fix, echte Assertions |
| test_corrections.py | 3 | E | T2: Print-only → echte Assertions |

Summe: 23 + 13 + 79 + 56 + 136 = **307** ✓

## Was die 307 insgesamt BEWEISEN — und was nicht

**Belegt:** (i) die dokumentierten Audit-Fehler sind repariert (Tier D mit
RED/GREEN-Evidenz); (ii) im Q1-Modell existiert kein skalares Q_SSZ, und die
6⊕2-Invarianz ist Permutationsalgebra mit D_A=D_B (Tier A/B); (iii) der
S↔T0-Mischterm ist analytisch hergeleitet und dynamisch verifiziert, sein
SSZ-Gehalt (2φ) ist im Modell ausgeschlossen (Tier A/B/C); (iv) die
Software ist in sich konsistent (Tier E).

**Nicht belegt:** SSZ als Gravitationsphysik; Übertragbarkeit der
Qubit-Struktur auf Raumzeit (FD-Brücke bleibt Analogie); Existenz ODER
Nichtexistenz verborgener Freiheitsgrade (Photonenkanal ist
Kanal-Eigenschaft); jede nicht-scalare Kopplung (G1 offen).

**Unabhängige Prüfung:** Repo ist online (github.com/error-wtf/ssz-qubits,
Branch `audit/ssz-qubits-repair-8to6-20261031` @ `5720cae…`+); ein Befehl:
`python -m pytest -q` im venv (requirements.txt, scipy>=1.0.0).
