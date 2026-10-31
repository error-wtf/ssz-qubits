# QUANTUM BUS DERIVATION — Hamiltonoperatoren, Blöcke, Schur, Näherung (Phase 4)

**Ort:** `research/quantum_bus/` (separates Forschungspaket; NICHTS davon ist im
produktiven `ssz_qubits.py`). Einheiten ħ=1. Status aller Modelle:
**REFERENZ-/HYPOTHESEN-MODELLE** — kein Bus-Effekt ist nachgewiesen, keine
SSZ-Kopplung ist hergeleitet (siehe SSZ_VS_GR_BUS_PREDICTIONS.md).

## Modell Q0 — Kontrolle ohne Bus
`H0 = Σ_i (ω_i/2) Z_i`. Rein lokal ⇒ faktorisierend: Produktzustände bleiben
Produktzustände (Reduced-Entropy-Test = 0, `tests/…::TestQ0NoBus`).
**Negativkontrolle:** Jedes Modell, das aus lokalen Z-Phasen Verschränkung
macht, hat einen Wechselwirkungsterm.

## Modell Q1 — Dreifach-Zweizustandsmodell (8×8)
`H = Σ_i ω_i Z_i/2 + g_A (X_A X_M + Y_A Y_M)/2 + g_B (X_M X_B + Y_M Y_B)/2`
(Basisordnung (A, M, B); Index = a·4+m·2+b). Eigenschaften (getestet):
hermitesch; U unitär; Norm/Energie erhalten; **Σ Zᵢ/2 ist erhalten**
(Austausch-Modell). Basis-Datei: `models.py::q1_hamiltonian`.

## Explizite 6⊕2 (Auftrag §5.1)
Bell-Basis des Paares (A,B): |T+⟩=|00⟩, |T0⟩=(|01⟩+|10⟩)/√2, |T−⟩=|11⟩,
|S⟩=(|01⟩−|10⟩)/√2 ⊗ M ⇒ Ordnung [T⊗M (6) | S⊗M (2)], `reduction.py::bell_unitary`
(unitarisch, gegen erzeugende Zustände getestet).
**Blockstruktur ist NICHT generisch:** für den generischen Austauschbus ist
‖B₆₂‖>0 (Singulett koppelt an Triplett über X_A-Anteile — Negativkontrolle);
NUR wenn der Hamiltonoperator die Paar-Symmetrie respektiert (z.B. Ising
J Z_A Z_B/4) ist B₆₂=0 exakt. „6=6⊕2" ist Basiswechsel, keine Eliminierung.

## Schur-Komplement / effektiver Hamiltonoperator (Auftrag §5.2)
Sektorzerlegung des Q1-Modells nach M-Anregung (energetisch 4+4:
Low = {|a,m=0,b⟩} = Indizes {0,1,4,5}, High = M-Anregung):
`H_eff(E) = H_LL + H_LH (E·I − H_HH)⁻¹ H_HL` — exakt, E-abhängig
(`bus_effective.py`). Geprüft: für jeden exakten Low-Eigenwert E gilt
σ_min(H_eff(E) − E·I) < 1e−8.
**Statische Näherung (SW 2. Ordnung) um E₀:** Fehler ∝ g²/Δ — numerisch als
Quotient err(2g)/err(g) ≈ 4 verifiziert (Δ=0.8). **Nahe Resonanz (Δ→0)
versagt die Methode** (E−H_HH singulär; Sektorbegriff kollabiert) — als
Negativtest fixiert.

## Modell Q2 — physischer Resonatorbus
`H = Σ ω_i Z_i/2 + ω_r a†a + Σ g_i (σ_i⁺ a + σ_i⁻ a†)`, Trunkierung n_max ⇒
dim = 4(n_max+1). Erhaltungsgröße N = Σ s⁺s⁻ + a†a ([H,N]=0 getestet).
Trunkierungs-Konvergenz: n_max 8→14 verschiebt die 6 tiefsten Eigenwerte
< 1e−8 bei g/ω_r = 0.05. Dispersiver Shift nichtlinear in g nachgewiesen.

## Modell Q3 — REDUZIERT (gelabelt)
Reiner Dephasing-Kanal ρ→(1−p)ρ+p ZρZ als CPTP-Kraus-Map (Spur-, Positivitäts-,
Faktor-(1−2p)-Tests). **Keine vollständige Lindblad-Dynamik implementiert —
OFFEN** (Auftrag erlaubt Q3 optional nur nach Q1/Q2-Validierung).

## 8→6 / 8→2: was jeder Prozess leistet (Auftrag §5.3)
| Prozess | 8→? | verlustfrei unitär? | Metrik |
|---|---|---|---|
| Basiswechsel | 8=6⊕2 | JA (nur Umbenennung) | ‖B₆₂‖, Blockdiagonalität |
| SW/Schur-Elimination | 8→4 effektiv | NEIN — Näherung, Fehler g²/Δ | Eigenwert-Fehler, σ_min-Residuum |
| Projektion/Postselektion | 8→6 | NEIN (Erfolgwahrscheinlichkeit < 1) | p_succ, Leakage Tr(P₂ρ) |
| Partialtrace/Reset | 8→reduziert | NEIN (Info in Umgebung) | Von-Neumann-Entropie |
| Code-Unterraum | 6 oder 2 ab initio | JA innerhalb des Unterraums | Invarianz ‖B₆₂‖=0 |
Alle implementiert/getestet in `reduction.py` + `bus_effective.py`.
„8→2" (C⁸→C²) hat Kernrang 6: beliebige Inputs sind NICHT verlustfrei
abbildbar (Rangsatz; DIMENSION_LEDGER.md D).

## Fidelity vs. Verschränkung vs. CHSH (Auftrag §5.4)
Bell-Fidelity |⟨ψ_target|ψ⟩|², Concurrence (Wootters) und CHSH sind in
`reduction.py` **separat** implementiert und getestet: lokaler Phasen-Bias θ
ändert F=cos²(θ/2), aber Concurrence=1 und CHSH_max=2√2 bleiben exakt
(Horodecki-Formel für das Achsen-Maximum; Tsirelson-Bound geprüft;
Z-Rotation-Invarianz fixiert). Vergleiche mit analytischen Grenzfällen:
ungekoppelt (g=0 → Q0), Δ→∞ (kopplungsfrei), resonant (SW-Versagen).
