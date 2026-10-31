# CARMEN_8_TO_X_CONTEXT.md — Forschungskontext für das Gespräch mit Carmen
(Erzeugt gemäß Übergabedokument HERMES_UEBERGABE_CARMEN_8ZU_X_2026-10-31.md §7.
Charakter: vorbereitend. KEINE Autorisierung von Push/Merge; keine rückwirkende
Interpretation von Carmens „8→x" als 6⊕2-Qubit-Problem.)

## 1. Provenienzmatrix (Auftrag A) — Stand bei Erzeugung

| Artefakt | Wert | Nachweis |
|---|---|---|
| Branch | `audit/ssz-qubits-repair-8to6-20261031` | git branch --show-current |
| HEAD | `c1aef9e91927d61ac62f4be716ddf7fddc46d033` | git rev-parse HEAD |
| main (unverändert) | `e068fe6d14d58ca223fabe4ab61fbd1b4000c13f` | Audit-Referenzrevision |
| Arbeitsbaum | sauber bis auf Validierungslogs (Post-Commit-Artefakte) | git status |
| Baseline Original | 184/184 PASS @ e068fe6d, scipy-frei Exit 1 | logs/baseline*, AUDIT_DE-qubit.md §2 |
| Nach R1+R3 | 204/204 | Commit 3e2c39d, logs/r1r3_GREEN2.log |
| Nach R2+T4 | 227/227 | Commit 9df7d04 |
| Nach Phase 2–6 | 271/271 | Commit cbd4d42 |
| Nach Q_SSZ | 284/284 | Commit 922281d |
| Nach Mischterm | 290/290 | Commit c1aef9e |
| Nach Aufträgen B–E (dieses Paket) | **307/307, Exit 0** | reports/repair_validation/final-8tox-* |

**Grüne Tests sind keine physikalische Bestätigung** (BINDING, §2 Übergabe).

Hinweis: Das Übergabedokument nennt HEAD `922281d…` — inzwischen liegt
`c1aef9e` (Mischterm-Analyse) und dieser 8to_x-Commit darüber; Kette lückenlos
in `git log`, jeder Schritt mit Suite-Zähler oben.

## 2. Ursprung der 8→x-Idee (Auftrag A2)

**Status: RESEARCH_OPEN — wartet auf Carmens eigene Antworten** (§7 der Übergabe:
keine private Gesprächsquelle eigenmächtig abrufen; keine Rückinterpretation).
Lokal dokumentiert ist nur: Carmens Stichworte (Quantenphysik, Strong Field,
Schwarze Löcher, acht Dimensionen/Freiheitsgrade, zwei vermeintlich wegfallende
Grade, „Quantum Bus") und der spätere Photon-Impuls („Wir sind Photonenleute",
30.10.). Die taxonomische Einordnung liegt in DIMENSION_ONTOLOGY_MATRIX.csv.

## 3. Was im Korpus tatsächlich belegt ist (kurz, mit Status)

| Befund | Status | Beleg |
|---|---|---|
| 6⊕2 als Singulett/Triplett-Block | PROVEN_IN_MODEL | SYM_COMP_COMMUTANT_PROOF.md Claim 1–3 |
| Invarianz nur bei Spiegelsymmetrie (ω_A=ω_B ∧ g_A=g_B ∧ D_A=D_B) | PROVEN_IN_MODEL | Claim 2; probe-Tests |
| SSZ-Differenzsegmentierung BRICHT 6⊕2 | REFUTED_IN_MODEL (bedingt) | SSZ_SYMMETRY_PROBE_Q.md F3/F4 |
| Kein nichttriviales Q_SSZ (skalare Klasse) | REFUTED_IN_MODEL (bedingt) | ebenda, Kommutant dim 8 |
| Mischterm S↔T0 = ω(D_A−D_B)/2 = Bell-projizierte Zeitdilatation | PROVEN_IN_MODEL | SSZ_SINGLET_MIXING_OBSERVABLE.md |
| SSZ-Gehalt des Mischterms = 2φ-Koeffizient | EXCLUDED_IN_MODEL | Cassini/LLR γ=1 |
| Skalare SSZ-Diagonale ist rein lokal (U_A⊗U_M⊗U_B) | PROVEN_IN_MODEL | TestLocalFactorization |
| Schur exakt im Sektor; SW O(g²); Resonanz → Ausfall | PROVEN_IN_MODEL | bus_effective + Tests |
| Photonen-Kanal: Messblindheit ≠ Ontologie | PROVEN_IN_MODEL | photon_channel_demo |
| Nicht-scalare SSZ-Kopplung (K_AB) | RESEARCH_OPEN | SSZ_QUBUS_CONSTRAINTS.md G1 |

## 4. FD-Brücke (Auftrag F) — nur gekennzeichnete Analogie

- FD-5-Restwert **0.7247315849739798** gegen Artefakte bestätigt:
  `SSZ_FRAME_DRAGGING_20261030/fd_run4/5/6/7_20261030.log:81-82`
  („numerischer Rest des Treibers … ⇒ Störungsantwort echt ≠ 0: True").
  Es ist ein Restwert eines Treiberterms — KEINE unabhängige Validierung.
- Lokales radiales Gleichgewicht ≠ stationäre Gesamtgeometrie: g_tφ-Struktur,
  Drehimpulsfluss, Sagnac/Holonomie, Beobachterprojektionen bleiben getrennt
  (FD_VALIDIERUNGSPROTOKOLL_20261030.md; Labels C=VERIFIED, teils offen).
- **Keine Identifikation** von Quantenspin-6⊕2 mit 4D-Frame-Dragging ohne
  abgeleitete Kopplung; bestmöglicher Status einer Verbindung: explizit
  testbare Analogie (derzeit nicht einmal das — keine hergeleitete Brücke).

## 5. Offene Punkte (ehrlich)

1. Carmens ursprüngliche 8 — offen bis zu ihren Antworten (§2).
2. K_AB-Herleitung (G1) — die zentrale Lücke, identisch mit COMMON_ACTION_GAP.
3. 8→2 verlustfrei für beliebige Eingänge: im Korpus ausgeschlossen; mit
   expliziter Informations-/Postselektionskostenbilanz offen.
4. Entartungs-Jagd im Kommutanten für spezielle Parameter (dritter Zweig
   außer generisch/Spiegelsymmetrie): nicht erschöpfend catalogisiert.
