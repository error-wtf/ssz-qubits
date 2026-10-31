# SCHUMANN vs. SCHUR — getrennte Konzepte (Phase 2, Reparaturauftrag 2026-10-31)

**Befundlage (alles mit Dateipfaden belegt, nichts verändert):**

## 1. `ssz-qubits` (dieses Repo, HEAD e068fe6d…)

- Die String-Suche nach `Schumann` über alle `.py`/`.md`/`.txt` ergibt **keine
  Implementierung** — nur Verweise/Links auf das eigenständige Repo
  `ssz-schumann` (README.md). Kein Schur-Bezug im Code (Audit §Schumann,
  `mechanism-search.txt`).

## 2. `ssz-schumann` (separates Repo, LOKAL vorhanden, NICHT verändert)

- **Pfad:** `/home/error/physics/ssz-schumann` · **Git-HEAD:** `6172213c7333`
- **Inhalt:** Wendet das SSZ-Framework auf die **Schumann-Resonanzen** an —
  elektromagnetische stehende Wellen in der Erd-Ionosphät-Höhle
  (README.md: „Schumann resonances as a probe for spacetime segmentation").
- **Kernhypothese (README.md):** uniforme relative Frequenzverschiebung
  `Δf_n / f_n ≈ −δ_seg(t)` über alle Moden n — abgrenzt von klassischen
  dispersiven Effekten; Testbadge „94 passed".
- **Schur-Bezug:** `grep -ril "schur"` über `.py`/`.md` → **kein Treffer**.
  Keine Schur-Zerlegung, kein Schur-Komplement.

## 3. Schur-Zerlegung / Schur-Komplement (separate lineare Algebra)

- Für `H = [[A, B],[B†, C]]` mit invertierbarem `E−C` ist
  `H_eff(E) = A + B (E−C)⁻¹ B†` das Schur-Komplement des Eigenwertproblems —
  eine Elimination von Hilfsvariablen (wird NUR in der Phase-4-Forschung unter
  `research/quantum_bus/` als Referenztechnik implementiert, nie als Physik-Claim).

## 4. Schluss (gelabelt)

| Frage | Antwort |
|---|---|
| Ist `ssz-schumann` eine Resonanztheorie? | **JA** — Schumann-Resonanzen (EM Eigenmoden der Erd-Ionosphät-Höhle) mit einer SSZ-Frequenzverschiebungshypothese. |
| Mathematische Verbindung Schumann ↔ Schur-Komplement? | **NEIN / OFFEN** — kein Beleg in einem der beiden Repos; die Begriffe bezeichnen Verschiedenes (Resonanzphysik vs. Matrixelimination). Namensähnlichkeit ist Fallstrick, nicht Herleitung. |
| Zusammenhang Schumann ↔ Quantum Bus? | **KEINER dokumentiert.** Ein Bus wäre ein quantisierter Vermittler-Freiheitsgrad mit Kopplungstermen; die Schumann-Analyse ist klassische Spektralanalyse realer Daten. |
