# ISSUE MATRIX — ssz-qubits Reparatur/Validierung/Forschung

Statuswerte: OPEN | IN_PROGRESS | REPAIRED (mit Regressiontest) | OPEN_MODEL_CHOICE |
RESEARCH_OPEN | DOCUMENTED_ONLY | BLOCKED.
Schwere: S1 (falsches Ergebnis in Kernformel) | S2 (inkonsistentes Verhalten/API) |
S3 (Doku/Claim-Fehler) | S4 (Testarchitektur/Reproduzierbarkeit) | S5 (Forschungslücke).

Quelle der Befunde: `AUDIT_DE-qubit.md` (Revision e068fe6d…, = Baseline-HEAD) + eigene Verifikation
in dieser Baseline. Jede Zeile wird bei Reparatur mit Regressionstest-Referenz ergänzt.

## A. Technische Reparatur (Phase 1, R1–R5)

| ID | Befund | Klasse | Schwere | Status | Evidenz / Regression |
|---|---|---|---|---|---|
| R1 | Strong-Field-Ableitung `xi_gradient` falsch: implementiert `+(phi/r_s)*exp(-phi*r_s/r)`, korrekt für Modell A: `-(phi*r_s/r**2)*exp(-phi*r_s/r)`. Erdmasse @2r_s: alt +81.2310 m⁻¹, korrekt −20.3078 m⁻¹ | proven_bug | S1 | **REPAIRED** (R1+R3-Commit) | AUDIT §1; mpmath-Nachrechnung exakt; Regression: `tests/test_regressions_audit.py::TestR1StrongFieldGradient` (10 Fälle, RED 13 failed → GREEN 20 passed, Suite 204/204) |
| R2 | Regime-Auto-Umschaltung x≤100/x>100 unstetig (Xi 0.01605 → 0.005; Sprung in D). Keine Hermite im Kerncode; Doku beschreibt anderes Modell | documented_inconsistency | S2 | OPEN | AUDIT §2; Regression: Stetigkeits-/Modelltrenntest |
| R3 | `ssz_time_dilation_difference` nutzt überall D_weak; inkonsistent zur `ssz_time_dilation`-Auswahl (r_s/2r_s: −0.13333 vs −0.08818). 1 mm → 0.0 durch Auslöschung statt 1.0926e−19 | proven_bug | S1 | **REPAIRED** (R1+R3-Commit; regime-Parameter + expm1-stabile ΔD + Mismatch nutzt stabile Funktion) | AUDIT §3,§5; Regression: `TestR3TimeDifferenceModelConsistency` + `TestR3HighPrecisionOracle` (mpmath) |
| R4 | Grenzwerte/Tabellen: Xi-Grenzwerte vertauscht behauptet; D_A-Taylor fehlt Term; Monotonie falsch behauptet; A/B-Formeln vermischt (`exp(-phi*x)` vs `exp(-phi/x)`) | documented_inconsistency | S3 | OPEN | AUDIT §4, φ-Abschnitt; Regression: Tabellen aus Code generiert |
| R5 | Singularitäts-/Regularitätsbehauptungen aus D>0 abgeleitet; GR-Horizont als „physikalische Singularität" bezeichnet | unverified_physical_claim (+ external_literature_fact für Martel&Poisson) | S3 | OPEN | AUDIT §4; Korrektur in Doku + Invarianten-Check wo beansprucht |

## B. Testarchitektur / Reproduzierbarkeit (Phase 0/6)

| ID | Befund | Klasse | Schwere | Status | Maßnahme |
|---|---|---|---|---|---|
| T1 | `pytest.main()` in 8 Testdateien ohne `sys.exit` → Subprocess-Exit 0 unabhängig vom pytest-Urteil | proven_bug (Testarchitektur) | S4 | OPEN | `run_tests.py`/Datei-`__main__`-Blöcke: Exitcode propagieren |
| T2 | `test_corrections.py` = 0 Assertions (Print-only) | proven_bug (Testarchitektur) | S4 | OPEN | Echte Assertions oder als Demo umlabeln |
| T3 | `test_paper_consistency.py`/`comprehensive_test.py`: Assertions nur beim Import, nicht pytest-sammelbar | documented_inconsistency | S4 | OPEN | In pytest-Funktionen overführen (Erhalt der Prüfungen) |
| T4 | scipy fehlt in `requirements.txt` (Import in verify_phi_discretization.py:6) | proven_bug | S4 | OPEN | requirements ergänzen (D0.3) |
| T5 | „REPOSITORY IS 100% CORRECT" als Programmausgabe | unverified_physical_claim | S3 | OPEN | Text ändern; claims in CLAIM_REGISTER |

## C. φ-Leiter / diskrete Struktur (Phase 2)

| ID | Befund | Klasse | Schwere | Status |
|---|---|---|---|---|
| P1 | Gekapptes B-Modell: Knick bei x=1; Hin-/Rückrekursion nicht invers (0.8017118471 → außen 0.8017118471 → innen 0.6321205588; Verlust 0.1695912883) | documented_inconsistency | S2 | OPEN |
| P2 | Intersection-Doku: `exp(-phi*x)` mit `exp(-phi*r_s/r)` gleichgesetzt (falsch für x=r/r_s); A- und B-Rekursionen als eine Dynamik verwendet | documented_inconsistency | S3 | OPEN |
| P3 | D_A-Entwicklung: korrekt `1-phi/x+(3/2)phi²/x²+…`; führender Koeffizient φ ≠ 1/2 (GR): Faktor 2φ | documented_inconsistency | S3 | OPEN |
| P4 | `(Xi,s,D,N',ν)` = 5 abhängige reelle Größen, keine 5 Hilbertraumdimensionen; N'=4(1+Xi) i.A. nicht ganzzahlig, keine Qubit-Zählung | documented_inconsistency | S3 | OPEN |
| P5 | Nullstellen A: x*=1.594811457889, B: x*=1.386561619649 (jeweils unter eigenen Definitionen); Eindeutigkeit unbewiesen | model_hypothesis | S5 | RESEARCH_OPEN |

## D. Schumann/Schur, Dimensionsverwirrung, Quantum Bus (Phase 3–5)

| ID | Befund | Klasse | Schwere | Status |
|---|---|---|---|---|
| S1 | Kein Schur-Komplement, kein Bus-Hamiltonoperator, keine 8→6/8→2-Herleitung im Code; „Schumann" nur Repo-Link | documented_inconsistency | S5 | RESEARCH_OPEN |
| S2 | `simulate_bell_state`: Fidelity = cos²(Phase/2) gesetzt, keine Busdynamik; CHSH für feste Messachsen | unverified_physical_claim | S3 | OPEN |
| S3 | 8=6⊕2 (Singulett/Triplett-Basiswechsel), 8D-Phasenraum, 10→8 Lichtkegel: drei verschiedene Begriffe, nicht austauschbar | model_hypothesis (Klarstellung) | S5 | RESEARCH_OPEN → DIMENSION_LEDGER |

## E. Wissenschaftliche Claims (Phase 7 → CLAIM_REGISTER.csv)

README/FINAL_REPORT/COMPLETE_PROJECT_REPORT/PAPER_* werden vollständig durchsucht; Register
enthält: Claim-ID, wörtlicher Text, Ort, Art, Code-Test, unabhängiger Beleg, Korrektur,
Restunsicherheit. Status bis dahin: OPEN.
