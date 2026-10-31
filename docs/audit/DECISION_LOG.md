# DECISION LOG — ssz-qubits Reparatur/Validierung/Forschung

Regel (Auftrag §0): Jede nichttriviale Änderung und Entscheidung wird hier dokumentiert —
Befund, Evidenz, Alternativen, Entscheidung, Tests, offene Unsicherheit.
Evidenzklassen: `proven_bug` | `documented_inconsistency` | `model_hypothesis` |
`numerical_artifact` | `unverified_physical_claim` | `external_literature_fact`.

---

## D0.1 — Arbeitsumgebung isoliert außerhalb des Repo
- **Befund:** Repo gehört root; Audit-Läufe dürfen den Quellbaum nicht verschmutzen.
- **Entscheidung:** Arbeits-/Snapshot-/venv-Verzeichnis `/home/error/physics/ssz-qubits-audit-20261031/`
  (außerhalb des Arbeitsbaums); Snapshot `original-source-snapshot-e068fe6-20261031.tar.gz`.
  Kein globales `pip install`, keine Systempaketänderung, keine `safe.directory=*`-Globalconfig
  (nicht einmal benötigt — direkte Git-Aufrufe im Repo funktionierten ohne dubious-ownership-Fehler).
- **Tests:** Manifest-Diff vor/nach allen Baseline-Läufen: Originaldateien byte-identisch.

## D0.2 — Auditierte Versionsmatrix exakt reproduziert
- **Befund:** Audit lief mit Python 3.14.8 / numpy 2.5.4 / matplotlib 3.11.2 / pytest 9.2.0.
- **Entscheidung:** venv314 mit exakt diesen Pin-Versionen (nicht System-numpy 2.4.6), um
  Vergleichbarkeit mit `AUDIT_DE-qubit.md` zu garantieren. Danach Prüfung gegen die
  Projekt-Metadaten (`requirements.txt`: numpy>=1.20, matplotlib>=3.5, pytest>=7 — erfüllt).
- **Tests:** `pip check` → „No broken requirements found".

## D0.3 — SciPy: fehlende Abhängigkeit als eigener Befund, nicht still gefixt
- **Befund** (`proven_bug`, Abhängigkeitsfehler): `verify_phi_discretization.py:6` importiert
  `scipy.optimize.brentq`; `requirements.txt` deklariert scipy NICHT. Baseline-Lauf ohne scipy:
  **Exit 1** (`ModuleNotFoundError`), mit scipy (isoliert installiert, Log `scipy-install.log`):
  Exit 0.
- **Entscheidung:** Reparatur = Ergänzung `scipy>=1.0` in `requirements.txt` erfolgt als eigene
  dokumentierte Änderung im Reparatur-Commit (Phase 1-Gate), NICHT während der Baseline.
- **Offen:** Mindestversion bewusst niedrig (brentq ist stabil seit 0.x); exakte Pinning-Entscheidung
  in D1.x nachgesehen.

## D0.4 — Baseline vor jeder Korrektur; Infrastruktur-Commit getrennt
- **Entscheidung:** Der unveränderte Basellauf (184 passed; φ Exit 1 ohne scipy) wurde VOR der
  ersten Repo-Änderung erfasst. Der erste Branch-Commit enthält ausschließlich Infrastruktur
  (`scripts/run_full_validation.sh`, `docs/audit/*`, Baseline-Rohlogs) — **keine** Reparatur.
  Damit bleibt „vorher rot / nachher grün" für jede Reparatureinheit sauber messbar.
- **Tests:** siehe BASELINE.md Matrix.

## D0.5 — Validierungsskript-Design
- **Entscheidung:** `scripts/run_full_validation.sh`: `set -Eeuo pipefail`; einzelne FAILs brechen
  die Matrix nicht ab (sonst verschwinden spätere Läufe), ABER: jede Zeile mit wahrem Exitcode in
  `status.tsv`, Gesamtklassifikation in `summary.json` mit `overall=FAIL`, Skript-Exit ≠ 0 bei FAIL.
  `|| true`-Maskierung existiert nirgends; einziges erwartetes Negativverhalten (φ ohne scipy)
  wird als `EXPECTED_FAIL` klassifiziert, nicht weggefiltert.
- **Tests:** Smoke-Lauf (mit scipy): 8/8 PASS, Exit 0, JUnit-XML + summary.json erzeugt.

## D0.6 — Untracked Alt-Dateien und .bak
- **Befund:** `tests/test_ssz_physics_OLD_WRONG_FORMULA.py.bak` (von pytest ignoriert) ist
  historischer Beleg der Formelkorrekturgeschichte.
- **Entscheidung:** Erhalten, keine Löschung (Auftragsregel: keine Datenlöschung; historische
  Texte bleiben nachvollziehbar).

---
(Einträge für R1–R5, φ, Schumann, Quantum-Bus folgen pro Reparatureinheit.)
