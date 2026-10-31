#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Audit-Regressions tests R4/R5 — Grenzwerte, Reihen, Singularitäts-Claims.

R4: Dokumentierte Grenzwerte/Tabellen müssen zum CODE passen; die Tabellen
    werden code-generiert (scripts/generate_model_tables.py →
    docs/research/MODEL_TABLES.md). Diese Tests pinpen die Mathematik.
R5: Regularität wird NICHT aus D>0 behauptet; die Korrekturen der
    Singularitäts-Texte werden als Doc-Guards gesichert.

© 2025 Carmen Wrede, Lino Casu — ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import math
from pathlib import Path

import numpy as np
import pytest

from ssz_qubits import (
    M_EARTH, PHI, schwarzschild_radius,
    xi_segment_density, ssz_time_dilation,
)

RS = schwarzschild_radius(M_EARTH)
ROOT = Path(__file__).resolve().parent.parent


class TestR4LimitsModelA:
    """Xi_A(0⁺)=1, Xi_A(∞)=0, D_A(0⁺)=1/2, D_A(∞)=1 — die KORRIGIERTEN Limits."""

    def test_A_limits(self):
        xi0 = xi_segment_density(1e-16 * RS, M_EARTH, regime='strong_A')
        xiinf = xi_segment_density(1e16 * RS, M_EARTH, regime='strong_A')
        assert xi0 == pytest.approx(1.0, abs=1e-13)
        assert xiinf == pytest.approx(0.0, abs=1e-13)
        d0 = ssz_time_dilation(1e-16 * RS, M_EARTH, regime='strong_A')
        dinf = ssz_time_dilation(1e16 * RS, M_EARTH, regime='strong_A')
        assert d0 == pytest.approx(0.5, rel=1e-13)
        assert dinf == pytest.approx(1.0, rel=1e-13)

    def test_B_limits(self):
        xi0 = xi_segment_density(1e-16 * RS, M_EARTH, regime='strong_B')
        xiinf = xi_segment_density(1e16 * RS, M_EARTH, regime='strong_B')
        assert xi0 == pytest.approx(0.0, abs=1e-13)
        assert xiinf == pytest.approx(1.0, abs=1e-13)
        dinf = ssz_time_dilation(1e16 * RS, M_EARTH, regime='strong_B')
        assert dinf == pytest.approx(0.5, rel=1e-13)  # B NICHT asymptotisch flach


class TestR4AsymptoticSeries:
    """Fernfeld-Reihen bei x=1e4 (numerisch, Ordnung x⁻³)."""

    X = 1e4

    def test_Xi_A_series(self):
        x = self.X
        got = xi_segment_density(x * RS, M_EARTH, regime='strong_A')
        expect = PHI/x - PHI**2/(2*x**2) + PHI**3/(6*x**3)
        assert got == pytest.approx(expect, rel=1e-10)

    def test_D_A_series(self):
        x = self.X
        got = ssz_time_dilation(x * RS, M_EARTH, regime='strong_A')
        expect = 1 - PHI/x + 1.5*PHI**2/x**2 - (5.0/3.0)*PHI**3/x**3
        assert got == pytest.approx(expect, rel=1e-9)

    def test_leading_coefficient_factor_2phi_vs_GR(self):
        """D_A ≈ 1−φ/x vs D_GR ≈ 1−1/(2x): Quotient der führenden Terme → 2φ≈3.236.
        Bei endlichem x=1e4 sind die x⁻²-Korrekturen relativ O(1.5φ/x)≈2.4e-4 —
        daher Toleranz 1e-3 (die Reihen SELBST sind in test_D_A_series exakt
        geprüft)."""
        x = 1e4
        dA = ssz_time_dilation(x * RS, M_EARTH, regime='strong_A')
        dGR = math.sqrt(1 - 1/x)
        ratio = (1 - dA) / (1 - dGR)
        assert ratio == pytest.approx(2 * PHI, rel=1e-3)


class TestR4Monotonicity:
    def test_A_strictly_decreasing(self):
        grid = np.logspace(-1, 4, 500) * RS
        vals = [xi_segment_density(r, M_EARTH, regime='strong_A') for r in grid]
        assert all(np.diff(vals) < 0)

    def test_generated_tables_exist_and_match_code(self):
        """Die R4-Tabelle muss existieren und die korrigierten A-Limits enthalten."""
        f = ROOT / "docs" / "research" / "MODEL_TABLES.md"
        assert f.exists(), "docs/research/MODEL_TABLES.md fehlt (Generator laufen lassen)"
        text = f.read_text(encoding="utf-8")
        assert "Xi_A(0⁺)=1" in text
        assert "2φ ≈ 3.236" in text


class TestR5SingularityClaimsRemoved:
    """Doc-Guards: zurückgezogene Behauptungen dürfen nicht zurückkommen."""

    def test_no_100_percent_correct_print(self):
        src = (ROOT / "comprehensive_test.py").read_text(encoding="utf-8")
        assert "REPOSITORY IS 100% CORRECT" not in src

    def test_README_horizon_claims_corrected(self):
        for name in ("README.md", "README_DE.md"):
            text = (ROOT / name).read_text(encoding="utf-8")
            # Die zurückgezogene Behauptung darf NUR noch im Korrekturvermerk
            # (Zitat + "withdrawn"/"zurückgezogen") vorkommen:
            n_en = text.count("avoids the singularity")
            n_de = text.count("vermeidet die Singularität") + text.count("vermeidet die Singularitaet")
            total = n_en + n_de
            assert total <= 1, f"{name}: Behauptung {total}x unmarkiert"
            if total:
                assert ("withdrawn" in text) or ("zurückgezogen" in text)
            assert "metric_invariants.py" in text  # Verweis auf die Invarianten-Rechnung

    def test_formula_doc_limits_corrected(self):
        for name in ("docs/SSZ_FORMULA_DOCUMENTATION.md",
                     "docs/SSZ_FORMULA_DOCUMENTATION_DE.md"):
            text = (ROOT / name).read_text(encoding="utf-8")
            assert "| Xi(0) | = 0" not in text
            assert "Singularity-free!:" not in text
            assert "Singularitätsfrei**: Xi(0) = 0" not in text

    def test_discrete_doc_no_singularity_free(self):
        for name in ("docs/DISCRETE_SSZ_STATE_FORMULATION.md",
                     "docs/DISCRETE_SSZ_STATE_FORMULATION_DE.md"):
            lines = (ROOT / name).read_text(encoding="utf-8").splitlines()
            marked = ("gestrichen", "Withdrawn", "withdrawn")
            bad = [ln for ln in lines
                   if ("singularity-free" in ln or "singularitätsfrei" in ln)
                   and not any(m in ln for m in marked)]
            assert not bad, f"{name}: unmarkierte 'singularity-free'-Zeilen: {bad}"

    def test_metric_invariants_script_and_evidence_exist(self):
        assert (ROOT / "scripts" / "metric_invariants.py").exists()
        # Beleg-Log mit bestandenem Schwarzschild-Orakel (finaler Lauf wird in
        # reports/repair_validation/ archiviert):
        candidates = list((ROOT / "reports" / "repair_validation").rglob("metric_invariants.out"))
        assert candidates, "Invarianten-Beleglog fehlt in reports/repair_validation/"
        log = candidates[0].read_text(encoding="utf-8", errors="replace")
        assert "worst rel Abweichung = 0.000e+00" in log
        assert "→ OK (Orakel numerisch exakt getroffen an allen Stützstellen)" in log

    def test_flat_space_control_via_curvature_module(self):
        """Schnelle Kontrolle der ausgelieferten Maschine: D≡1 → R=K=0."""
        sympy = pytest.importorskip("sympy")
        import sys
        sys.path.insert(0, str(ROOT / "scripts"))
        from metric_invariants import curvature  # noqa: E402
        R, K = curvature(sympy.Integer(1))
        assert sympy.simplify(R) == 0 and sympy.simplify(K) == 0
