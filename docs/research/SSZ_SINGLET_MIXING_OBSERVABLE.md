# SSZ SINGLET MIXING OBSERVABLE — Der D_A−D_B-Mischterm S↔T0
### (Carmens Folgefrage vom 31.10.: Ist der Mischterm unabhängig messbar und
### geht er über gewöhnliche Zeitdilatation hinaus? — Antwort: Nein, mit Präzisierung.)

**Ausführbar:** `research/quantum_bus/ssz_mixing_analysis.py` +
`tests/test_ssz_mixing_analysis.py` (6 Fälle, Suite 290 passed).

## 1. Exakte Struktur des Mischterms

Die Differenzsegmentierung D_A≠D_B wirkt im Q1-Bus nur über die Diagonale
`ω(D_A Z_A + D_B Z_B)/2`. In der Bell-Basis des Paares (A,B) gilt:

| Matrixelement | Wert (exakt) | Bedeutung |
|---|---|---|
| ⟨T0\|H\|S⟩ | **(ω_A D_A − ω_B D_B)/2** | der Mischterm |
| ⟨T±\|H\|S⟩ | **0** | T± werden nur diagonal verschoben |
| ⟨S\|H\|S⟩, ⟨T0\|H\|T0⟩ | ±(ω_A D_A + ω_B D_B)/2·(…) | Summenuhr |

Der Mischterm ist also **genau die paarweise Differenzuhr**
ω·(D_A−D_B)/2 — dieselbe Größe wie `ssz_time_dilation_difference`,
projiziert auf den Singulett/Triplett-Basiswechsel.

## 2. Dynamik (numerisch vs. Zweiniveau)

Start im Singulett ⇒ S↔T0-Rabi-Oszillation mit Frequenz |m|:
numerische 8×8-Entwicklung reproduziert vollständige Populationübertragung
bei t = π/(2|m|) (g ≪ m, Fehler der Zweiniveau-Näherung ~ (g/√2m)²).

## 3. Der SSZ-spezifische Gehalt — und warum er kein neues Fenster ist

Das Verhältnis der Mischterme SSZ/GR (Leading Order, auslöschungsfrei aus
den geschlossenen Formeln):

    dD_SSZ/dx ÷ dD_GR/dx → 2φ ≈ 3.236

Der Mischterm ist also **Bell-Basis-projizierte Zeitdilatation**:

- Er existiert **ohne jeden Bus** (reiner Diagonalanteil; der Austauschterm
  trägt bei Spiegelsymmetrie nichts zu S↔T0 bei — testfixiert).
- Sein **einziger** SSZ-spezifischer Gehalt ist der Faktor 2φ gegen GR —
  und genau dieser führende Koeffizient ist durch Cassini/LLR
  (PPN γ=1 ⇒ Koeffizient 1/2) bereits ausgeschlossen.
- Damit präzisiert sich `NO_DISTINGUISHING_PREDICTION`: Die messbare Größe
  existiert (S↔T0-Oszillation), aber ihr SSZ-Gehalt reduziert sich auf die
  bereits falsifizierte Leitertaste. **Keine unabhängig neue Observable.**

## 4. Konsequenz für die Aufgabenwahl A/B

Task A (Verifikation des Negativresultats) ist damit **abgeschlossen und
geschärft**: Das Negativresultat hält in der exakten Blockstruktur — der
Mischterm ist kein neuer Freiheitsgrad, sondern Zeitdilatation im
Singulett/Triplett-Gewand. **Task B (nicht-scalare SSZ-Kopplung) ist damit
der einzig offene Weg** — mit der nun präzisen Bedingung: Es müsste ein
Kopplungsterm hergeleitet werden, der (i) off-diagonal in der Segmentierung
wirkt (nicht D_i·Z_i) und (ii) aus Segmentprinzipien kommt (Marolf-Gate
AX-M3, COMMON_ACTION_GAP f3/f4). Beides existiert im Korpus nicht.

## 5. Reproduktion

```
python -m pytest research/quantum_bus/tests/test_ssz_mixing_analysis.py -v   # 6 passed
python -m pytest -q                                                          # 290 passed
```
