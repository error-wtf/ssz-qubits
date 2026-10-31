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

## D2.1 — R2: Explizite Modell-Taxonomie statt stiller auto-Umschaltung
- **Befund** (`documented_inconsistency`): legacy-'auto' springt bei x=100 unstetig
  (Ξ: 0.01605014135 → 0.00499999995; D entsprechend). Im Kerncode existiert KEINE
  Hermite-Interpolation; `docs/DISCRETE_SSZ_STATE_FORMULATION.md` beschreibt ein
  ANDERES Modell (Cap min(1−e^{−φx}, Ξ_max), Grenzen 1.8/2.2) als der implementierte Kern.
- **Alternativen:** (a) Toleranzen erhöhen bis Tests grün — VERWORFEN (Auftragsverbot:
  keine Scheinreparatur); (b) auto stillschweigend glatt machen — VERWORFEN (ändern
  Alt-Verhalten heimlich); (c) Blend-Grenzen [50,150] — Konstruktionswahl, als
  OPEN_MODEL_CHOICE gelabelt.
- **Entscheidung:** 
  1. Explizite Modelle: `'weak'`, `'strong_A'` (Alias `'strong'`, etabliert),
  `'strong_B'` (dokumentierte Variante, Xi_B(∞)=1, D_B(∞)=1/2 — NICHT asymptotisch
  flach), `'smooth_bridge_hypothesis'`.
  2. `'auto'`/`'legacy_auto'`: historische unstetige Semantik BIT-KOMPATIBEL erhalten,
  mit DeprecationWarning (1096 Warnungen in der Suite = bewusst sichtbarer Schuldzinns).
  3. Glatte Brücke: C²-Quintic-Blend Xi=(1−s)·A+s·weak auf [50,150] — als
  FORSCHUNGSHYPOTHESE gelabelt; nie Default; nie mit anderen Modellen in einer
  Auswertung vermischt (Modellwahl-Flag durchgängig; Unbekannte → ValueError).
  Numerische Studie vor Implementierung (`logs/bridge_monotonicity_study.py`,
  200k-Punkte-Gitter): Blend über ALLE getesteten Intervalle streng monoton fallend;
  [50,150] gewählt (kleinstes Intervall um den Legacy-Sprung, exakte Anfügung beidseits).
  **WICHTIG (Grenze):** Die Brücke ist KONSTRUKTION. Sie ist damit keine
  Feldgleichungslösung und keine physikalische Konsequenz der Dokumente —
  Energiebedingungen/Scheinkrümmung der Brückenmetrik sind NICHT geprüft (offen).
- **Tests:** tests/test_regressions_r2_models.py — 23 Fälle (Deprecation, Legacy-Sprung
  als PINNTER Negativbefund, Ein-Formel-über-alle-Radien je Modell, B-Grenzwerte,
  A≠B außerhalb x=1, Brücke: exakte Anfügung, C¹-FD-Konsistenz, Fugen-Stetigkeit,
  Monotonie, Differenzfunktion, Modell-Gradient-Konsistenz via FD-Orakel).
  RED: 12 failed (`r2_RED.log`) → GREEN 43/43 (mit R1/R3-Datei), Suite 227/227.
- **Orakel-Präzisionsgrenze (dokumentiert):** FD des strong_B-Gradienten verliert bei
  u=φ·x ≳ 10 die Präzision (expm1-Ergebnisse runden nahe −1.0 auf identische Doubles);
  Implementierung wurde direkt gegen die geschlossene Form geprüft (exakt). FD-Gitter
  für strong_B deshalb auf x ≤ 5 begrenzt — Grenze des ORAKELS, nicht des Codes.
- **Offen:** Interne Caller (analyze_qubit_segment etc.) nutzen noch Default-'auto'
  (warnen jetzt). Migration auf explizite Modelle ohne Verhaltensänderung erfordert
  eine Modellentscheidung pro Funktion (M ist generisch) — OPEN_MODEL_CHOICE, Phase 7.

## D2.2 — T4: scipy in requirements.txt ergänzt
- **Befund** (`proven_bug`): `verify_phi_discretization.py` importiert scipy;
  requirements deklarierte es nicht → Baseline Exit 1 (belegt in BASELINE.md).
- **Entscheidung:** `scipy>=1.0.0` aufgenommen (brentq ist stabil; bewusst keine
  obere Pins, konsistent mit vorhandenem Stil). Audit-venv hatte scipy isoliert
  nachinstalliert (Log `scipy-install.log`) — Verhalten identisch.

## D1.1 — R1: Strong-Field-Ableitung repariert (Commit: R1+R3-Einheit)
- **Befund** (`proven_bug`): `xi_gradient` gab im Strong-Zweig
  `+(phi/r_s)*exp(-phi*r_s/r)` zurück — falsches Vorzeichen UND falscher radialer
  Faktor gegenüber dem exakt gewählten Modell A `Xi_A = 1−exp(−φ·r_s/r)`, dessen
  Ableitung `−(φ·r_s/r²)·exp(−φ·r_s/r)` lautet.
- **Evidenz:** Audit-Kontrollzahlen UNABHÄNGIG mit mpmath (dps=30) reproduziert,
  mit der Modul-Konstanten G=6.67430e-11 exakt: alt +81.231020879 m⁻¹, analytisch
  −20.3077552198 m⁻¹, FD −20.3077… m⁻¹ (Log: `ssz-qubits-audit-20261031/logs/
  r1_independent_check.out`). Regressionstests VOR Fix: 13 failed (RED-Log
  `r1r3_RED.log`), NACH Fix: 20 passed (`r1r3_GREEN2.log`).
- **Alternativen:** (a) Ableitung nur numerisch anbieten — verworfen (die
  analytische Form ist elementar und exakt); (b) Vorzeichen nur flippen —
  verworfen (radialer Faktor war ebenfalls falsch, r_s/r² vs. 1/r_s).
- **Entscheidung:** Analytische Ableitung des gewählten Modells implementiert;
  gemeinsame Validatoren `_validate_radius`/`_validate_mass` (r>0, finite;
  M≥0, finite); **M=0 ist DEFINIERT als flach** (Ξ=0, dΞ/dr=0, D=1) — vorher
  ZeroDivisionError. Dokumentationstext im Docstring korrigiert (die alte
  Behauptung „Positive gradient … increases with r" war falsch, R4-vorab).
- **Tests:** tests/test_regressions_audit.py::TestR1StrongFieldGradient (10 Fälle:
  FD-Orakel über log-Gitter 0.2–100 r_s, Audit-Kontrollwert, Monotonie, Alt-Wert
  weg, Weak unverändert, Massenskalierung, Extremwerte, Unterlauf, Validation,
  M=0). Gesamtsuite danach: **204 passed, Exit 0** (keine Alt-Test-Kollision).
- **Offen:** Modell-Trennung A/B und `legacy_auto`-Deprecation = R2 (nächste Einheit).

## D1.2 — R3: Zeitdifferenzen stabil UND modelltreu (gleicher Commit)
- **Befund** (`proven_bug`): `ssz_time_dilation_difference` nutzte überall die
  Weak-Identität `D=2r/(2r+r_s)`; im Strong-Regime inkonsistent zur
  `ssz_time_dilation`-Auswahl (r_s/2r_s: alt −0.13333333333, korrekt
  −0.08818137022 — mpmath-bestätigt). Zusätzlich `qubit_pair_segment_mismatch`:
  direkte D-Subtraktion → 0.0 bei 1 mm Höhendifferenz (Auslöschung; stabil
  1.0926195757e−19).
- **Evidenz:** RED: test_strongfield_matches_direct_model_difference u.a.
  (13 failed inkl. TypeError-Beleg für fehlenden regime-Parameter); GREEN:
  20/20; Gesamtsuite 204/204.
- **Entscheidung:** 
  (a) `ssz_time_dilation_difference(r1, r2, M, regime='auto')`: Weak/Weak
  behält die exakte rationale Form (Back-Kompatibilität bit-genau); Strong/Strong
  über expm1 mit ANALYTISCHER u-Differenz `u1−u2 = φ·r_s·(r2−r1)/(r1·r2)` (keine
  Float-Differenz fast gleicher u); ΔD = (Ξ₂−Ξ₁)/((1+Ξ₁)(1+Ξ₂)) — identisch zum
  Single-Radius-Modell; Mixed (auto an der 100·r_s-Grenze) pro Radius wie
  `ssz_time_dilation`.
  (b) `ssz_time_dilation` erhält `regime`-Parameter (Default 'auto' — keine
  Verhaltensänderung für Alt-Callers), damit Test/Code dasselbe Modell adressieren.
  (c) `qubit_pair_segment_mismatch` nutzt die stabile Differenzfunktion.
- **Ehrlichkeitsvermerk:** Beim ersten Implementierungsentwurf wurde ΔD mit
  Ξ₁−Ξ₂ statt Ξ₂−Ξ₁ zurückgegeben — der Vorzeichenfehler wurde DURCH DEN
  REGRESSIONSTEST (Audit-Kontrollwert −0.08818137022) gefangen und korrigiert.
  Das ist der beabsichtigte Mechanismus „Test beißt vor Freigabe".
- **Grenze:** Das 1 mm/5 GHz/50 ns-Signal (≈1.71628e−16 rad/Gate) ist eine
  RECHENVORHERSAGE unter Modellannahmen — kein experimenteller Nachweis
  (Audit §5; gelabelt im Test-Docstring).

