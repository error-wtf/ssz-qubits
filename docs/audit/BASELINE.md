# BASELINE — ssz-qubits vor Reparatur

**Aufgenommen:** 31.10.2026 (Europe/Berlin) · **Branch:** `audit/ssz-qubits-repair-8to6-20261031`
**Revision:** `e068fe6d14d58ca223fabe4ab61fbd1b4000c13f` (= Referenzrevision des Audits `AUDIT_DE-qubit.md`; Abweichung: KEINE — Arbeitsbaum war sauber)
**Snapshot (nichtdestruktiv, außerhalb des Arbeitsbaums):**
`/home/error/physics/ssz-qubits-audit-20261031/original-source-snapshot-e068fe6-20261031.tar.gz` (30,6 MB)
**Manifeste:** `original-manifest-before.sha256` / `original-manifest-after.sha256` (136 Dateien, in `/home/error/physics/ssz-qubits-audit-20261031/baseline/`)

## Umgebung (isoliert)

| Bestandteil | Wert |
|---|---|
| venv | `/home/error/physics/ssz-qubits-audit-20261031/venv314` (außerhalb des Repo) |
| Python | 3.14.8 (x86_64, Kali Rolling) |
| numpy | 2.5.4 (= auditiert) |
| matplotlib | 3.11.2 (= auditiert) |
| pytest | 9.2.0 (= auditiert) |
| scipy | zunächst NICHT installiert (bewusst); danach isoliert nachinstalliert, Log: `logs/baseline/scipy-install.log` |
| pip freeze | `baseline/pip-freeze-baseline.txt`, `baseline/pip-freeze-with-scipy.txt` |
| Bytecode/Backend | `PYTHONDONTWRITEBYTECODE=1`, `MPLBACKEND=Agg` |

## Unveränderte Baseline-Läufe (wahre Exitcodes)

Logs: `/home/error/physics/ssz-qubits-audit-20261031/logs/baseline/` und Kopien in `reports/repair_validation/baseline-manual/`.

| Lauf | Befehl | Exit | Befund |
|---|---|---|---|
| pytest-full | `python -m pytest -v --tb=long -p no:cacheprovider --junitxml=…` | **0** | **184 passed in 0.30s** (`pytest-full.log`, `pytest-results.xml`) |
| run_tests | `python run_tests.py` | 0 | Runner: Demo + 9 Testdateien „erfolgreich" (Subprocess-Exitcodes werden vom Runner-Design nicht hart geprüft — s. Discovery) |
| phi_no_scipy | `python verify_phi_discretization.py` | **1** | `ModuleNotFoundError: No module named 'scipy'` (Zeile 6) — belegt: SciPy fehlt in `requirements.txt` |
| phi_with_scipy | dgl. nach isolierter SciPy-Installation | 0 | „GESAMT-ERGEBNIS: ALLE TESTS BESTANDEN" |
| paper_a_form | `python verify_paper_a_formulas.py` | 0 | — |
| comprehensive | `python comprehensive_test.py` | 0 | letzte Zeile: „REPOSITORY IS 100% CORRECT" — **Programmausgabe, kein Audit-Urteil** (Gegenbeispiele R1–R4) |
| corrections | `python test_corrections.py` | 0 | Print-only, 0 Assertions, 0 Testfunktionen (59 Zeilen) — kein pytest-Sammelfall |
| paper_consist | `python test_paper_consistency.py` | 0 | 12 Assertions auf Modulebene (Lauf beim Import), 0 Testfunktionen |
| demo | `python demo.py` | 0 | — |

## Test-Discovery (eindeutige Zahlen)

- **Mit pytest gesammelte Fälle: 184** (`--collect-only -q`, Log: `collect-only.txt`), alle in `tests/`.
- **8 Testdateien** rufen am Dateiende `pytest.main([...])` **ohne** `sys.exit(...)`: test_edge_cases.py:731, test_entanglement.py:239, test_paper_a_support.py:141, test_paper_c_support.py:300, test_roadmap_validation.py:333, test_ssz_physics.py:466, test_ssz_qubit_applications.py:714, test_validation.py:646. Konsequenz: Beim Subprocess-Aufruf durch `run_tests.py` ist der Prozess-Exit 0 **kein** pytest-Urteil (Audit-Befund bestätigt).
- `test_corrections.py`: **0** `assert`, **0** `def test` → reine Druckausgabe, wird von pytest nicht gesammelt (Datei im Repo-Root, keine `test_`-Funktionen).
- `test_paper_consistency.py` (12 asserts) und `comprehensive_test.py` (12 asserts): Assertions laufen beim **Import**/direkten Ausführen, nicht als gesammelte pytest-Fälle.
- `tests/test_ssz_physics_OLD_WRONG_FORMULA.py.bak`: deaktivierte Alt-Testdatei (`.bak`, von pytest ignoriert) — historischer Beleg, bleibt erhalten.
- Assertions je tests/-Datei: edge_cases 40, entanglement 29, paper_a_support 16, paper_c_support 19, paper_d_validation 35, roadmap_validation 21, ssz_physics 22, ssz_qubit_applications 13, validation 19 (Summe 214 Assertions in 184 Funktionen).

## Integrität nach den Baseline-Läufen

`diff original-manifest-before.sha256 original-manifest-after.sha256`:
**Alle Originaldateien byte-identisch.** Einzig NEU (generiert, gitignored, danach entfernt):
`.pytest_cache/*` (4 Dateien) und `reports/full-output.md`, `reports/RUN_SUMMARY.md` (durch `run_tests.py`).

## Rechenintensive Läufe (Matrix, bewusst getrennt — nicht übersprungen)

In der Baseline-Kernmatrix NICHT enthalten (Plan, Ausführung in Phase 7/finaler Validierung):
`analyze_for_paper.py`, `analyze_for_paper_b.py`, `analyze_repo_for_paper_b_v2.py`, `final_summary.py`,
`ssz_roadmap_validation.py` (Hauptteil ohnehin über tests/test_roadmap_validation.py gedeckt),
`visualize_ssz_qubits.py`, `generate_improved_plots.py`, `generate_paper_*` (DOCX/Plot-Generatoren),
`paper_suite_integrator.py`, `paper_c_feasibility_analysis.py`, `update_docx_figures.py`, `_fix_paths.py`.
Diese werden mit `MPLBACKEND=Agg` und Zeitlimit in `reports/repair_validation/` protokolliert;
Ergebnisse fließen in den CLAIM-Register- und Abschlussbericht ein.

## Gate 0 — Status: ERFÜLLT

Ausgangszustand, Befehle und wahre Exitcodes liegen als Artefakte vor; Originaldateien sind in der
Baseline unverändert (Manifest-Beweis). Kein Blocker.
