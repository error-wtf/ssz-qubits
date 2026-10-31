# REDUCTION_VS_OBSERVABILITY_AUDIT.md — Doppeltest 8→x
(Auftrag von Lino/Carmen, 31.10. | Code: research/quantum_bus/doppeltest_8tox.py
| Tests: tests/test_doppeltest_8tox.py (14 Fälle) | Suite: 322 passed, Exit 0
| Alle Zahlen dieses Dokuments sind aus den Testläufen maschinell erzeugt.)

## Vorbemerkung: Nebenfunde des Doppeltests

Der Doppeltest hat **zwei zusätzliche Befunde** produziert, bevor er die
eigentlichen Fragen beantwortete — beide `proven_bug`-Klasse, beide behoben:

1. **`reduction.bell_unitary` bellte (A,M) statt (A,B)** (`kron(B, I2)` in
   Q1-Ordnung). `P2` war daher der (A,M)-Singulett-Projektor (Q1-Indizes
   {2,3,4,5} statt {1,3,4,6}) und kommutierte nicht einmal mit dem
   spiegelsymmetrischen H (Norm 0.80). Die alten Tests waren konsistent
   fehlgelabelt (der „Ising-auf-dem-Paar"-Test baute Z⊗Z⊗**I** = (A,M)-Ising)
   und blieben deshalb grün — ein Lehrstück zur Aussagekraft von Testanzahlen.
   **Fix:** explizite Q1-Index-Platzierung; `P2 ≡ singlet_projector_full`
   jetzt testfixiert; zwei Test-Inputs auf die dokumentierte Semantik
   gestellt (nicht auf grün getrimmt — die Semantik selbst war falsch).
2. **SSZ-Differenzuhr-Beträge:** A3-Commutator-Normen: mirror = 4.5e-16,
   differential = 0.250 — der einzige Unterschied ist der bereits
   dokumentierte Differenzuhr-Mischterm.

## Experiment A — Physikalische Reduktion

| Prüfung | Ergebnis | Wert |
|---|---|---|
| P6/P2 Ränge, Idempotenz, Komplement | OK | Spuren 6/2, P6+P2=I, P2≡P_s (Ordnungstest) |
| [H,P] Spiegelsymmetrie | dynamische Invarianz | ‖[H,P]‖ = 4.5e-16 |
| [H,P] Differenzsegmentierung | Invarianz gebrochen | 0.250 |
| **Constraint auf Unterraum?** | **NEIN** | P2·X_A·P6 = 1.4142 — lokale zulässige Operatoren verbinden die Sektoren; vollrangige ρ zulässig |
| Leakage P6→P2 (mirror) | 1.9e-30 | keine |
| Leakage P6→P2 (D_A≠D_B) | 0.133 | getrieben vom Differenzuhr-Mischterm |
| Leakage P6→P2 (g_A≠g_B) | 0.130 | Positivkontrolle: jede Spiegelbrechung leakt — keine SSZ-Spezialität |

**Vierfache Trennung (A6):**
- Eichredundanz: **none** — kein Constraint-Operator ableitbar.
- Energetische Unterdrückung: **partial_only** — Detuning verschiebt,
  Population kehrt zurück (nichts wird entfernt).
- Dynamische Invarianz: **nur bei Spiegelsymmetrie**.
- Physikalisch unzulässige Zustände: **none** — alle 8 Richtungen erreichbar.

**Urteil Experiment A: H-RED = `REFUTED_IN_MODEL`.** Die Zerlegung ist
algebraisch/dynamisch, keine Freiheitsgradreduktion. Genau das
Abbruchkriterium des Auftrags greift: [H,P]=0 allein ist Invarianz, nicht
Verbot — und ein physikalisches Verbot existiert nicht.

## Experiment B — Eingeschränkte Beobachtbarkeit

| Prüfung | Ergebnis | Wert |
|---|---|---|
| Nicht-injektive Kanal-Abbildung | OK | kontinuierliche Familie ρ_λ, ρ₁≠ρ₂, M(ρ_λ) identisch |
| Zusätzlicher zulässiger Kanal | trennt | Bell-Projektor-POVM: Outcomes 0.25–0.50 über die Familie (Positivität+Vollständigkeit geprüft) |
| **Linearer Rang der Outcome-Abbildung** | **2 von 64** | auf Herm(8) (dim_R 64), Kern-Dimension 62 (Kernvektoren verifiziert) |
| Beobachtungs-Algebra | dim 4 | ≅ B(C²) — operationale Fassung von „2 von 8" (kein Projektionsrang) |
| Zeitkonversion der Blindheit | JA | mit Bus max. Trennung 0.0133; ohne Bus exakt 0 ∀t |
| Tomographie voll / Kanal | 64 / 4 | Kern 60: AB-Anteil ist ohne Zusatzkanal irreversibel verloren |

**Urteil Experiment B: H-OBS = `PROVEN_IN_MODEL`.** Es existieren
verschiedene Gesamtzustände mit identischer Kanalstatistik, die durch einen
zweitens Kanal unterschieden werden. Das Abbruchkriterium wird eingehalten:
die Nicht-Injektivität wird NICHT als Beweis verborgener Raumzeitdimensionen
interpretiert — sie ist eine Eigenschaft der Messabbildung.

## Experiment C — Direkter Vergleich

1. **Vortäuschung demonstriert:** Ein M-only-Beobachter sieht bei g=0
   NULL Dynamik (M-Statistik 0.000→0.000), während der Zustand real driftet
   (Fidelity 0.642) — die eingeschränkte Beobachtbarkeit täuscht eine
   Dimensionsreduktion vor.
2. **Unterscheidungs-Ressourcen pro Fall:** Zusatzkanal mit AB-Zugriff (b3),
   kontrollierte Kopplung g≠0 (b5: konvertiert Blindheit in Signal),
   tomographisch vollständiger Effektsatz (b6).
3. **SSZ-skalar gegen GR:** Verhältnis 3.236068 = 2φ — unverändert
   `EXCLUDED_IN_MODEL` (Cassini/LLR); keine unabhängige Vorhersage.

## Abschlussfrage

**Können die beiden Hypothesen operational unterschieden werden?**

**JA — aber nur mit zusätzlicher physikalischer Ressource.** Konkret:
entweder (i) ein Messzugriff außerhalb des blinden Sektors (B3), oder
(ii) eine kontrollierte Dynamik, die den blinden Sektor an den Kanal koppelt
(B5 — der Austauschbus selbst leistet das). **Ohne jede Kopplung zwischen
blinde[m] Sektor und Kanal sind die Hypothesen für diesen Beobachter
unbeobachtbar-äquivalent** — die Einschränkung ist dann observer-relativ und
dem System nicht attribuierbar.

Im vorliegenden Modell gilt damit die saubere Zuordnung:
- **H-RED: gefallen** (kein Constraint, kein Verbot, Leakage unter jeder
  Spiegelbrechung) — die 6⊕2-Struktur ist Permutationsalgebra plus
  dynamische Invarianz, keine Dimensionsreduktion.
- **H-OBS: bestätigt** (Rang 2/64, Kern 62, nicht-injektiv, dynamisch
  konvertierbar) — als Kanal-Eigenschaft.
- **Gleichzeitigkeit** (Carnes Einschränkung): im Modell realisiert — ein
  System kann beides haben; hier trifft nur H-OBS zu, und zwar genau weil
  H-RED fehlt.

## Reproduktion

```
python -m pytest research/quantum_bus/tests/test_doppeltest_8tox.py -v  # 14 passed
python -m pytest -q                                                     # 322 passed
```
Logs: reports/doppeltest/ ( pytest-Ausgabe ). Branch:
audit/ssz-qubits-repair-8to6-20261031 (GitHub synchron).
