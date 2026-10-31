# PHI MODEL COMPARISON — A / B / Gekappt B / Weak / GR (Phase 2)

Alle Zahlen aus `scripts/verify_phi_ladder.py` (mpmath, 40 dps; Log:
`reports/repair_validation/…/verify_phi_ladder.out`) bzw.
`docs/research/MODEL_TABLES.md` (aus `scripts/generate_model_tables.py`).
**Regel (Auftrag §2): x=r/r_s, r_k=r_s·φ^k, Ξ, s=1+Ξ, D=1/(1+Ξ), N′=4(1+Ξ),
ν=ln(1+Ξ)/ln(φ) strikt nach Definition. Fünf verknüpfte reelle Größen sind
keine fünf Hilbertraumdimensionen; N′ ist i.A. NICHT ganzzahlig.**

## Definitionen

| Modell | Formel | Ξ(0⁺) | Ξ(∞) | D(0⁺) | D(∞) | Monotonie |
|---|---|---|---|---|---|---|
| weak | Ξ_w = 1/(2x) | (nicht deklariert für x<100) | →0 | — | →1 | fallend |
| **A** | Ξ_A = 1−e^(−φ/x) | **1** | **0** | **1/2** | 1 | **fallend** |
| **B** | Ξ_B = 1−e^(−φx) | 0 | 1 | 1 | **1/2** | steigend |
| gekappt B | min(Ξ_B, Ξ_max=1−e^(−φ)) | 0 | Ξ_max | 1 | 1/(1+Ξ_max)=0.5550 | steigend, **Knick bei x=1** |
| GR | D_GR = √(1−1/x) | — | — | — | — | (x ≥ 1) |

## Rekursionen (nicht austauschbar!)

- **A:** q_k = e^(−φ^(1−k)) ⇒ **q_{k+1} = q_k^(1/φ)**; äquivalent
  Ξ_{k+1} = 1 − (1−Ξ_k)^(1/φ). [mpmath-geprüft, k=−5..7, PASS]
- **B:** p_k = e^(−φ^(k+1)) ⇒ **p_{k+1} = p_k^φ**; äquivalent
  Ξ_{k+1} = 1 − (1−Ξ_k)^φ. [PASS]
- Exaktrekursion auf der Leiter: a_{k+1} = (a_k + 1/φ)/φ mit a_k = 1−φ^(−k);
  **D_GR(φ) = 1/φ**. [PASS]
- Unkappte A-Rekursion: 40 Stufen hin + 40 zurück → Start exakt wiederhergestellt
  (Verlust < 1e−20). [PASS]

## Cap-Knick (dokumentierter Defekt des gekappten B-Modells)

Leiter x_k = φ^k, Start x=1 → Ξ = 1−e^(−φ) = 0.8017118471:
- Schritt außen (x=φ): Formelwert 1−e^(−φ²) = 0.92705387 > Ξ_max → **Cap hält →
  Wert unverändert**.
- Schritt innen (x=1/φ): 1−e^(−1) = **0.6321205588**.
- ⇒ Hin-/rückweg **nicht invers**; Verlust **0.1695912883**. [Audit-Zahlen exakt
  reproduziert]

## GR-Schnitte (ungekappt, getrennt; Existenz numerisch, Eindeutigkeit OFFEN)

- **A:** D_A(x) = D_GR(x) bei **x\*_A = 1.594811457889** (Bisektion, 200 it,
  dps=40; reproduziert bis 5e−12).
- **B:** D_B(x) = D_GR(x) bei **x\*_B = 1.386561619649** (dgl.).
- Numerische Nullstelle ≠ Eindeutigkeitsbeweis. Ein Intervalleindeutigkeitsbeweis
  steht aus → **RESEARCH_OPEN**.

## Was die φ-Struktur NICHT beweist

1. Keine Quantendynamik: Identitäten sind algebraische Substitutionen reeller
   Zahlen; kein Hamiltonoperator, keine Zustandszählung.
2. `(Ξ, s, D, N′, ν)` = EINE Funktion in fünf Darstellungen — kein 5-dimensionaler
   Hilbertraum; N′ = 4(1+Ξ) ist i.A. nicht ganzzahlig und keine Qubit-Anzahl.
3. Keine experimentelle Bestätigung; keine Feldgleichung; A und B sind
   Verschiedene Profile (nur bei x=1 gemeinsam), die Gleichsetzung
   `exp(−φ·x)` = `exp(−φ·r_s/r)` ist für x = r/r_s FALSCH.
4. Fernfeld: D_A ≈ 1 − φ/x vs. D_GR ≈ 1 − 1/(2x): führender Koeffizient
   unterscheidet sich um **2φ ≈ 3.236** (keine GR-Identität in erster Ordnung).
