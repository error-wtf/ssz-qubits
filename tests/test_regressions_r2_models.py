#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audit-Regressions tests R2 — Regimeauswahl / Modelltrennung / glatte Brücke.

ISSUE_MATRIX R2: Die legacy-'auto'-Umschaltung (x<=100: Xi_A, x>100: Xi_weak)
ist unstetig (Sprung in Xi und D bei x=100). Reparatur = explizite
Modellwahl; legacy_auto bleibt für Altcode mit DeprecationWarning erhalten;
eine glatte Brücke existiert NUR als klar gelabelte Forschungshypothese
('smooth_bridge_hypothesis') und wird nie stillschweigend verwendet.

Konventionen:
  'weak'                    Xi = 1/(2x)                    [etabliert]
  'strong_A' / 'strong'     Xi = 1 - exp(-phi/x)           [etabliert, Ansatz A]
  'strong_B'                Xi = 1 - exp(-phi*x)           [dokumentiert, Ansatz B]
  'smooth_bridge_hypothesis' C2-Blend A→weak auf [50,150]  [HYPOTHESE, Konstruktion]
  'auto' / 'legacy_auto'    historische unstetige Umschaltung [DEPRECATED]

© 2025 Carmen Wrede, Lino Casu — ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""

import warnings

import numpy as np
import pytest

from ssz_qubits import (
    M_EARTH,
    PHI,
    schwarzschild_radius,
    xi_segment_density,
    xi_gradient,
    ssz_time_dilation,
    ssz_time_dilation_difference,
)

RS = schwarzschild_radius(M_EARTH)


class TestR2LegacyAutoDeprecation:
    """Die historische 'auto'-Umschaltung ist dokumentiert DEPRECATED."""

    def test_auto_warns_deprecation(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            xi_segment_density(10.0 * RS, M_EARTH, regime='auto')
        assert any(issubclass(x.category, DeprecationWarning) for x in w), \
            "regime='auto' muss eine DeprecationWarning auslösen"

    def test_legacy_auto_warns_deprecation(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            xi_segment_density(10.0 * RS, M_EARTH, regime='legacy_auto')
        assert any(issubclass(x.category, DeprecationWarning) for x in w)

    def test_legacy_auto_semantics_unchanged(self):
        """Der DEPRECATED Pfad behält exakt die historische (unstetige)
        Semantik — er wird dokumentiert, nicht still repariert."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            assert xi_segment_density(50.0 * RS, M_EARTH, regime='legacy_auto') \
                == pytest.approx(1.0 - np.exp(-PHI / 50.0), rel=1e-15)
            assert xi_segment_density(200.0 * RS, M_EARTH, regime='legacy_auto') \
                == pytest.approx(1.0 / 400.0, rel=1e-15)

    def test_legacy_auto_jump_is_real_and_quantified(self):
        """NEGATIVKONTROLLE/Doku: der Sprung von legacy_auto bei x=100 existiert
        und hat die auditierte Größe. Dieser Test PINNT den bekannten Fehler des
        DEPRECATED-Pfads — er ist ein Warnschild, kein Positivtest."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            xi_left = xi_segment_density(100.0 * RS, M_EARTH, regime='legacy_auto')
            xi_right = xi_segment_density((100.0 + 1e-6) * RS, M_EARTH, regime='legacy_auto')
        assert xi_left == pytest.approx(0.01605014135, rel=1e-8)
        assert xi_right == pytest.approx(0.00499999995, rel=1e-8)
        assert abs(xi_left - xi_right) > 0.01  # endlicher Sprung


class TestR2ExplicitModelsNoHiddenSwitching:
    """Explizite Modelle sind EINE Formel über alle Radien — kein Umschalten."""

    @pytest.mark.parametrize("model", ['weak', 'strong_A', 'strong', 'strong_B'])
    def test_single_formula_across_full_range(self, model):
        """Werte folgen EINER geschlossenen Form auf 0.2 … 1e6 r_s (wo definiert)."""
        grid = np.logspace(np.log10(0.2), 6, 40) * RS
        for r in grid:
            x = r / RS
            xi = xi_segment_density(r, M_EARTH, regime=model)
            if model in ('weak',):
                expected = 1.0 / (2.0 * x)
            elif model in ('strong_A', 'strong'):
                expected = 1.0 - np.exp(-PHI / x)
            else:  # strong_B
                expected = 1.0 - np.exp(-PHI * x)
            assert xi == pytest.approx(expected, rel=1e-12), f"{model} r={x:.3g}r_s"

    def test_strong_alias_equals_strong_A(self):
        for x in (0.5, 1.0, 5.0, 42.0):
            r = x * RS
            assert xi_segment_density(r, M_EARTH, regime='strong') \
                == xi_segment_density(r, M_EARTH, regime='strong_A')

    def test_unknown_model_raises(self):
        with pytest.raises(ValueError):
            xi_segment_density(10 * RS, M_EARTH, regime='magic_regime')


class TestR2StrongBDocumentedLimits:
    """Ansatz B ist ein ANDERES Modell: Xi_B(∞)=1, D_B(∞)=1/2 (nicht flach)."""

    def test_B_limits(self):
        x = np.array([1.0, 1e3, 1e6])
        r = x * RS
        xi = np.array([xi_segment_density(rr, M_EARTH, regime='strong_B') for rr in r])
        assert xi[0] == pytest.approx(1.0 - np.exp(-PHI), rel=1e-12)   # Ξ_max @x=1
        assert xi[1] == pytest.approx(1.0, rel=1e-10)
        assert xi[2] == pytest.approx(1.0, rel=1e-8)
        D = [ssz_time_dilation(rr, M_EARTH, regime='strong_B') for rr in r]
        assert D[2] == pytest.approx(0.5, rel=1e-7)  # D_B(∞) = 1/2 — NICHT flach

    def test_A_and_B_differ_away_from_x1(self):
        """A und B stimmen NUR bei x=1 überein (audit: nicht austauschbar)."""
        for x in (0.5, 2.0, 10.0):
            r = x * RS
            a = xi_segment_density(r, M_EARTH, regime='strong_A')
            b = xi_segment_density(r, M_EARTH, regime='strong_B')
            assert abs(a - b) > 1e-6, f"x={x}: A und B fälschlich gleich?"


class TestR2SmoothBridgeHypothesis:
    """'smooth_bridge_hypothesis' — klar gelabelte KONSTRUKTION, keine Physik."""

    X0, X1 = 50.0, 150.0

    def test_matches_A_below_and_weak_above(self):
        below = xi_segment_density(40.0 * RS, M_EARTH, regime='smooth_bridge_hypothesis')
        ref_a = xi_segment_density(40.0 * RS, M_EARTH, regime='strong_A')
        above = xi_segment_density(200.0 * RS, M_EARTH, regime='smooth_bridge_hypothesis')
        ref_w = xi_segment_density(200.0 * RS, M_EARTH, regime='weak')
        assert below == pytest.approx(ref_a, rel=1e-12)
        assert above == pytest.approx(ref_w, rel=1e-12)

    def test_weak_leading_coefficient_preserved(self):
        """Für x > X1 ist die Brücke EXAKT Xi_weak=1/(2x) — führender Koeffizient 1/2."""
        for x in (200.0, 1e4, 1e6):
            xi = xi_segment_density(x * RS, M_EARTH, regime='smooth_bridge_hypothesis')
            assert xi == pytest.approx(1.0 / (2.0 * x), rel=1e-12)

    def test_c1_smoothness_across_blend(self):
        """C1: analytische Ableitung ≙ zentrale finite Differenz im ganzen Blend-Band."""
        worst = 0.0
        for x in np.linspace(30.0, 220.0, 25):
            r = x * RS
            g_impl = xi_gradient(r, M_EARTH, regime='smooth_bridge_hypothesis')
            h = 1e-7 * r
            gp = xi_segment_density(r + h, M_EARTH, regime='smooth_bridge_hypothesis')
            gm = xi_segment_density(r - h, M_EARTH, regime='smooth_bridge_hypothesis')
            g_fd = (gp - gm) / (2 * h)
            worst = max(worst, abs(g_impl - g_fd) / abs(g_fd))
        assert worst < 1e-5, f"worst rel dev = {worst:.3e}"

    def test_c2_smoothstep_join_values(self):
        """An den Fugen x0/x1: Wert UND Ableitung gehen stetig in A bzw. weak über."""
        for x_edge, model_ref in ((self.X0, 'strong_A'), (self.X1, 'weak')):
            for x in (x_edge - 1e-9, x_edge, x_edge + 1e-9):
                r = x * RS
                v_bridge = xi_segment_density(r, M_EARTH, regime='smooth_bridge_hypothesis')
                v_ref = xi_segment_density(r, M_EARTH, regime=model_ref)
                assert v_bridge == pytest.approx(v_ref, rel=1e-9), f"x={x}"

    def test_monotonically_decreasing(self):
        grid = np.linspace(0.5, 1e5, 3000) * RS
        vals = np.array([xi_segment_density(r, M_EARTH, regime='smooth_bridge_hypothesis')
                         for r in grid])
        assert np.all(np.diff(vals) < 0.0), "Brücke muss streng monoton fallen"

    def test_difference_function_supports_bridge(self):
        """Auch die Differenzfunktion muss das Brückenmodell konsistent behandeln."""
        r1, r2 = 60.0 * RS, 80.0 * RS
        d_fn = ssz_time_dilation_difference(r1, r2, M_EARTH,
                                            regime='smooth_bridge_hypothesis')
        d_direct = (ssz_time_dilation(r1, M_EARTH, regime='smooth_bridge_hypothesis')
                    - ssz_time_dilation(r2, M_EARTH, regime='smooth_bridge_hypothesis'))
        assert d_fn == pytest.approx(d_direct, rel=1e-10)


class TestR2GradientModelConsistency:
    """Gemeinsame Modell-API: xi_gradient(model) ist die exakte Ableitung von
    xi_segment_density(model) — für JEDES Modell (keine Vermischung)."""

    @pytest.mark.parametrize("model", ['weak', 'strong_A', 'strong_B',
                                       'smooth_bridge_hypothesis'])
    def test_gradient_matches_finite_difference(self, model):
        # FD-Orakel-Grenze: fuer strong_B mit u=phi*x >> 1 runden die beiden
        # expm1-Ergebnisse nahe -1.0 auf identische Doubles -> FD verliert
        # alle Stellen (gemessen: x>=~9). Die closed form fuer B ist separat
        # in test_strong_B_gradient_formula und test_B_limits geprueft.
        # Daher FD-Gitter fuer strong_B nur bis x<=5 (u<=8.1, e^-u>3e-4).
        if model == 'weak':
            grid = np.logspace(2.5, 5.0, 12)          # nur wo weak gewählt sein darf
        elif model == 'strong_B':
            grid = np.logspace(np.log10(0.3), 0.7, 8)  # x <= 5 (FD-Präzision)
        else:
            grid = np.logspace(np.log10(0.3), np.log10(40.0), 12)
        for x in grid:
            r = x * RS
            h = 1e-7 * r
            gp = xi_segment_density(r + h, M_EARTH, regime=model)
            gm = xi_segment_density(r - h, M_EARTH, regime=model)
            g_fd = (gp - gm) / (2 * h)
            g_impl = xi_gradient(r, M_EARTH, regime=model)
            assert g_impl == pytest.approx(g_fd, rel=1e-5), \
                f"{model} x={x:.3g}: impl={g_impl:.6e} fd={g_fd:.6e}"

    def test_strong_B_gradient_formula(self):
        """dXi_B/dr = (phi/r_s) * exp(-phi*x) — dokumentierte B-Formel."""
        for x in (0.5, 1.0, 3.0):
            r = x * RS
            expected = (PHI / RS) * np.exp(-PHI * x)
            assert xi_gradient(r, M_EARTH, regime='strong_B') \
                == pytest.approx(expected, rel=1e-12)
