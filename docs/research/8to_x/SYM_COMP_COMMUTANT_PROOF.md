# SYM_COMP_COMMUTANT_PROOF.md — Symbolischer Beweis der 6⊕2-Symmetriestruktur
(Arbeitsauftrag B, Übergabedokument 31.10. | Code: research/quantum_bus/symbolic_symmetry.py
| Tests: tests/test_symbolic_and_schur.py::TestSymbolic* | Suite: 307 passed)

## Claim 1 — Projektoren (Status: PROVEN_IN_MODEL, symbolisch + numerisch)

**Definition:** P_s = (1 − σ_A·σ_B)/4 mit σ_A·σ_B = X_A X_B + Y_A Y_B + Z_A Z_B,
tensoriert mit I_M; P_t = I₈ − P_s. Q1-Ordnung (A, M, B).

**Herleitung (exakt, sympy):** Spur(P_s) = 2, Spur(P_t) = 6,
charpoly(P_s) = x⁶(x−1)² → Eigenwerte {1,1,0,0,0,0,0,0}. Ränge 2 und 6.

**Maschinell:** `test_trace_ranks_eigenvalues`, `test_idempotent`,
`test_matches_numeric_probe_projector` (Übereinstimmung mit dem numerischen
Modul < 1e-14).

## Claim 2 — Kommutator (Status: PROVEN_IN_MODEL, mit Negativkontrolle)

**Behauptung:** [H, P_s] = 0 exakt für ω_A=ω_B ∧ g_A=g_B ∧ D_A=D_B (ω_M frei).

**Herleitung:** sympy-Commutator des vollen H (Diagonaluhr + beidseitiger
Austausch + SSZ-Differenzuhr); Substitution der Spiegelbedingungen → Nullmatrix.

**Negativkontrollen:**
- generische Parameter: [H,P_s] ≠ 0 (`test_commutator_generic_nonzero`);
- asymmetrischer Drive ε_A≠ε_B bricht die Symmetrie selbst bei voller
  Spiegel-Symmetrie der restlichen Terme (`test_asymmetric_drive_breaks`);
- SYMMETRISCHER Drive ε(X_A+X_B) erhält sie (`test_symmetric_drive_preserves`).

**Gültigkeitsbereich:** Q1-Modellklasse; Zusatzterme müssen unter A↔B
(ohne M-Tausch) invariant sein.

**Physikalischer Kern (numerisch abgesichert in ssz_symmetry_probe):** Die
Invarianz entsteht durch destruktive Interferenz beider Austauschwege
(X_A X_M gegen X_M X_B): einzeln koppeln sie S an T0/T−, gemeinsam heben
sie sich im Singulett-Sektor exakt weg. Es ist A↔B-Permutationsalgebra,
kein SSZ-Inhalt (D_A=D_B nötig; Differenzsegmentierung bricht — siehe
SSZ_SYMMETRY_PROBE_Q.md F3/F4).

## Claim 3 — Sektor-Mischung (Status: PROVEN_IN_MODEL)

P_s H P_t = 0 exakt an der Spiegelsymmetrie; generisch ≠ 0. Die Mischkanäle:
Diagonaluhr ∝ (ω_A D_A − ω_B D_B) (nur S↔T0), Austausch ∝ (g_A−g_B).
→ `test_Ps_H_Pt_vanishes_at_symmetry`, `test_Ps_H_Pt_generic_nonzero`.

## Claim 4 — Kommutanten-Dimension (numerisch, exakt)

Generisch (Differenzterme an): dim{X: [H,X]=0} = 8 = {f(H)} → keine {6,2}-
Zerlegung möglich. Spiegelsymmetrisch: dim > 8 (Entartung), P_s ∈ Kommutant.
→ ssz_symmetry_probe, `test_generic_exchange_bus_commutant_is_polynomials_in_H`.

**Unabhängige Referenz:** Wigner/von-Neumann Kommutanten-Struktursatz
(Fulton/Harris, Representation Theory, §27); Bell-Basis: Nielsen & Chuang §2.6.
