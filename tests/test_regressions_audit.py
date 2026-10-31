#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Audit-Regressions tests für ssz-qubits — Reparaturauftrag 2026-10-31.

Jeder Test referenziert einen Eintrag in docs/audit/ISSUE_MATRIX.md und war
VOR der jeweiligen Reparatur ROT (Beleg: reports/repair_validation/).

Klassen: R1 (Strong-Field-Ableitung), R3 (Zeitdifferenzen stabil und modelltreu).
Orakel-Strategie (Auftrag §7.3): numerische Differentiation und mpmath in
HOHER Präzision als INDEPENDENTE Referenz — die Analytformel wird nicht 1:1
aus dem Implementierungscode kopiert.

© 2025 Carmen Wrede, Lino Casu — ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import pytest

from ssz_qubits import (
    M_EARTH,
    R_EARTH,
    PHI,
    schwarzschild_radius,
    xi_segment_density,
    xi_gradient,
    ssz_time_dilation,
    ssz_time_dilation_difference,
    qubit_pair_segment_mismatch,
    Qubit,
    QubitPair,
)


# =============================================================================
# R1 — Strong-Field-Ableitung (xi_gradient, Modell A: Xi = 1 - exp(-phi*r_s/r))
# =============================================================================

# Logarithmisch verteilte Radien im Strong-Field-Band (0.2 .. 100 r_s)
R_GRID_RS = np.logspace(np.log10(0.2), np.log10(100.0), 25)


def _fd_gradient(r, M, h_rel=1e-7):
    """Zentrale finite Differenz — unabhängiges Orakel, kein Formel-Copy."""
    h = h_rel * r
    xp = (1.0 - np.exp(-PHI * schwarzschild_radius(M) / (r + h)))
    xm = (1.0 - np.exp(-PHI * schwarzschild_radius(M) / (r - h)))
    return (xp - xm) / (2.0 * h)


class TestR1StrongFieldGradient:
    """ISSUE_MATRIX R1: Vorzeichen und radialer Faktor von xi_gradient."""

    def test_matches_finite_difference_over_log_grid(self):
        """dXi/dr (strong) muss der zentralen FD über den ganzen Band entsprechen."""
        rs = schwarzschild_radius(M_EARTH)
        worst = 0.0
        for x in R_GRID_RS:
            r = x * rs
            g_impl = xi_gradient(r, M_EARTH, regime='strong')
            g_fd = _fd_gradient(r, M_EARTH)
            rel = abs(g_impl - g_fd) / abs(g_fd)
            worst = max(worst, rel)
            assert rel < 1e-5, f"r={x:.3f}r_s: impl={g_impl!r} fd={g_fd!r} rel={rel:.3e}"

    def test_audit_control_value_earth_2rs(self):
        """Kontrollwert Audit: Erdmasse, r=2r_s → −20.3077552198 m⁻¹ (analytisch)."""
        rs = schwarzschild_radius(M_EARTH)
        g = xi_gradient(2.0 * rs, M_EARTH, regime='strong')
        assert g == pytest.approx(-20.3077552198, rel=1e-9)

    def test_gradient_is_negative_in_strong_field(self):
        """Xi_A fällt monoton mit r → dXi/dr < 0 im gesamten Strong-Band."""
        rs = schwarzschild_radius(M_EARTH)
        for x in R_GRID_RS:
            assert xi_gradient(x * rs, M_EARTH, regime='strong') < 0.0, f"x={x}"

    def test_old_buggy_value_is_gone(self):
        """Der alte Fehlerwert (+81.23 m⁻¹) darf nicht mehr auftreten."""
        rs = schwarzschild_radius(M_EARTH)
        g = xi_gradient(2.0 * rs, M_EARTH, regime='strong')
        assert not np.isclose(g, +81.2310208790, rtol=1e-3)

    def test_weak_gradient_unaffected(self):
        """Weak-Field-Zweig bleibt exakt −r_s/(2r²)."""
        rs = schwarzschild_radius(M_EARTH)
        r = 1000.0 * rs
        assert xi_gradient(r, M_EARTH, regime='weak') == pytest.approx(
            -rs / (2.0 * r**2), rel=1e-15)

    def test_gradient_dimension_is_inverse_length(self):
        """Dimension [1/m]: Skalierung mit M muss r_s⁻¹ folgen (Massenvariation)."""
        rs_e = schwarzschild_radius(M_EARTH)
        for mass_factor in (1e-6, 1.0, 1e6):
            M = M_EARTH * mass_factor
            rs = schwarzschild_radius(M)
            g1 = xi_gradient(2.0 * rs, M, regime='strong')
            # Analytisch: -(phi*rs/r²)e^{...} bei r=2rs → -(phi/(4rs))e^{-phi/2}
            expected = -(PHI / (4.0 * rs)) * np.exp(-PHI / 2.0)
            assert g1 == pytest.approx(expected, rel=1e-12), f"M-Faktor={mass_factor}"

    def test_extreme_radii_no_overflow(self):
        """Extremwerte: sehr kleine und sehr große Radien liefern endliche Werte."""
        rs = schwarzschild_radius(M_EARTH)
        for x in (1e-12, 1e-6, 1.0, 1e6, 1e12):
            g = xi_gradient(x * rs, M_EARTH, regime='strong')
            assert np.isfinite(g), f"x={x}: {g!r}"

    def test_underflow_gives_tiny_gradient_not_garbage(self):
        """Floating-Point-Unterlauf: e^{-phi/x} → 0 für x→0 ⇒ dXi/dr → ~-phi*rs/r² (riesig, endlich)."""
        rs = schwarzschild_radius(M_EARTH)
        g = xi_gradient(1e-12 * rs, M_EARTH, regime='strong')
        assert np.isfinite(g)

    def test_invalid_inputs_raise(self):
        """r<=0 und nicht-finite Eingaben werden abgelehnt (kein stilles NaN)."""
        rs = schwarzschild_radius(M_EARTH)
        with pytest.raises(ValueError):
            xi_gradient(0.0, M_EARTH)
        with pytest.raises(ValueError):
            xi_gradient(-1.0 * rs, M_EARTH)
        with pytest.raises(ValueError):
            xi_gradient(float('nan'), M_EARTH)
        with pytest.raises(ValueError):
            xi_gradient(float('inf'), M_EARTH)

    def test_m_zero_is_flat_by_definition(self):
        """M=0: kein Gravitationskörper → Xi=0, Gradient=0, D=1 (DEFINIERT, nicht Zufall).
        Vor der Reparatur: ZeroDivisionError (r/r_s mit r_s=0)."""
        assert schwarzschild_radius(0.0) == 0.0
        assert xi_segment_density(1.0, 0.0) == 0.0
        assert xi_gradient(1.0, 0.0) == 0.0
        assert ssz_time_dilation(1.0, 0.0) == 1.0


# =============================================================================
# R3 — Zeitdifferenzen: stabil UND modelltreu
# =============================================================================

class TestR3TimeDifferenceModelConsistency:
    """ISSUE_MATRIX R3: Differenzfunktion muss zum selben Modell passen wie D(r)."""

    def test_strongfield_matches_direct_model_difference(self):
        """r1=r_s, r2=2r_s (strong): Differenzfunktion ≡ D(r1)−D(r2) desselben Modells.
        Audit: alt −0.13333333333 (weak-Formel), korrekt −0.08818137022."""
        rs = schwarzschild_radius(M_EARTH)
        r1, r2 = rs, 2.0 * rs
        d_direct = (ssz_time_dilation(r1, M_EARTH, regime='strong')
                    - ssz_time_dilation(r2, M_EARTH, regime='strong'))
        d_fn = ssz_time_dilation_difference(r1, r2, M_EARTH, regime='strong')
        assert d_fn == pytest.approx(d_direct, rel=1e-10)
        assert d_fn == pytest.approx(-0.08818137022, rel=1e-8)

    def test_strongfield_not_the_weak_closed_form(self):
        """Die weak-geschlossene Form darf im Strong-Regime nicht mehr zurückkommen."""
        rs = schwarzschild_radius(M_EARTH)
        r1, r2 = rs, 2.0 * rs
        weak_form = 2.0 * rs * (r1 - r2) / ((2.0 * r1 + rs) * (2.0 * r2 + rs))
        d_fn = ssz_time_dilation_difference(r1, r2, M_EARTH, regime='strong')
        assert not np.isclose(d_fn, weak_form, rtol=1e-3)

    def test_weakfield_unchanged_closed_form(self):
        """Back-Kompatibilität: weak bleibt exakt 2r_s(r1−r2)/((2r1+r_s)(2r2+r_s))."""
        rs = schwarzschild_radius(M_EARTH)
        r1, r2 = R_EARTH + 1.0, R_EARTH
        expected = 2.0 * rs * (r1 - r2) / ((2.0 * r1 + rs) * (2.0 * r2 + rs))
        assert ssz_time_dilation_difference(r1, r2, M_EARTH, regime='weak') \
            == pytest.approx(expected, rel=1e-15)

    def test_antisymmetric(self):
        """ΔD(r1,r2) = −ΔD(r2,r1) über beide Regime-Bänder."""
        rs = schwarzschild_radius(M_EARTH)
        for (r1, r2) in ((0.5 * rs, 2.0 * rs), (rs, 100.0 * rs),
                         (R_EARTH + 1.0, R_EARTH), (2.0 * rs, 500.0 * rs)):
            f12 = ssz_time_dilation_difference(r1, r2, M_EARTH)
            f21 = ssz_time_dilation_difference(r2, r1, M_EARTH)
            assert f12 == pytest.approx(-f21, rel=1e-12, abs=0.0), f"(r1,r2)=({r1},{r2})"

    def test_equal_radii_is_exactly_zero(self):
        rs = schwarzschild_radius(M_EARTH)
        for r in (rs, 2.0 * rs, R_EARTH):
            assert ssz_time_dilation_difference(r, r, M_EARTH) == 0.0

    def test_one_mm_height_not_zero(self):
        """Audit: 1 mm Höhendifferenz → |ΔD| ≈ 1.0926e−19, NICHT 0.0 (Auslöschung)."""
        delta = abs(ssz_time_dilation_difference(R_EARTH + 1e-3, R_EARTH, M_EARTH))
        assert delta > 0.0
        assert delta == pytest.approx(1.0926195757e-19, rel=1e-4)

    def test_height_range_1um_to_1m_monotone(self):
        """Höhen 1 µm … 1 m auf der Erde: |ΔD| monoton wachsend, alle > 0."""
        prev = 0.0
        for h in (1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1.0):
            d = abs(ssz_time_dilation_difference(R_EARTH + h, R_EARTH, M_EARTH))
            assert d > 0.0, f"h={h}: Auslöschung auf 0"
            assert d > prev, f"h={h}: nicht monoton ({d} <= {prev})"
            prev = d

    def test_mismatch_uses_stable_difference(self):
        """qubit_pair_segment_mismatch: delta_time_dilation bei 1 mm ≠ 0.0."""
        a = Qubit(id="A", x=0.0, y=0.0, z=0.001, gate_time=50e-9)
        b = Qubit(id="B", x=0.0, y=0.0, z=0.0, gate_time=50e-9)
        pair = QubitPair(qubit_a=a, qubit_b=b)
        res = qubit_pair_segment_mismatch(pair, M_EARTH)
        assert res['delta_time_dilation'] > 0.0
        assert res['delta_time_dilation'] == pytest.approx(1.0926195757e-19, rel=1e-4)

    def test_phase_drift_per_gate_magnitude(self):
        """Audit-Größenordnung: 5 GHz, 50 ns → ≈ 1.71628e−16 rad/Gate (1 mm).
        Rechenvorhersage unter Modellannahmen — KEINE Messung (gelabelt)."""
        a = Qubit(id="A", x=0.0, y=0.0, z=0.001, gate_time=50e-9)
        b = Qubit(id="B", x=0.0, y=0.0, z=0.0, gate_time=50e-9)
        pair = QubitPair(qubit_a=a, qubit_b=b)
        res = qubit_pair_segment_mismatch(pair, M_EARTH)
        assert res['phase_drift_per_gate'] == pytest.approx(1.71628e-16, rel=1e-3)


class TestR3HighPrecisionOracle:
    """mpmath-Orakel (unabhängig von numpy-Implementierung)."""

    def test_high_precision_across_regimes(self):
        mpmath = pytest.importorskip("mpmath")
        mp = mpmath
        mp.mp.dps = 40
        PHI_MP = (1 + mp.sqrt(5)) / 2
        G_MP = mp.mpf('6.67430e-11')
        C_MP = mp.mpf('299792458')
        M_MP = mp.mpf('5.972e24')
        rs = 2 * G_MP * M_MP / C_MP**2

        def D(r, model):
            x = mp.mpf(r) / rs
            if model == 'weak':
                xi = 1 / (2 * x)
            else:
                xi = 1 - mp.e**(-PHI_MP / x)
            return 1 / (1 + xi)

        rs_f = float(rs)
        cases = [
            (0.5 * rs_f, 0.25 * rs_f, 'strong'),
            (2.0 * rs_f, 1.0 * rs_f, 'strong'),
            (50.0 * rs_f, 10.0 * rs_f, 'strong'),
            (R_EARTH + 1.0, R_EARTH, 'weak'),
        ]
        for r1, r2, model in cases:
            expected = D(r1, model) - D(r2, model)
            got = ssz_time_dilation_difference(r1, r2, M_EARTH, regime=model)
            assert got == pytest.approx(float(expected), rel=1e-10, abs=1e-18), \
                f"model={model} r1={r1:.6g} r2={r2:.6g}: {got!r} vs {float(expected)!r}"
