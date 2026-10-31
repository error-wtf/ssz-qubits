#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSZ-Qubits: Segmented Spacetime Framework for Quantum Computing

Core module implementing:
- SSZ time dilation for qubit systems
- Segment density analysis (Xi)
- Decoherence prediction based on segment geometry
- Gate timing corrections
- Qubit placement optimization

Based on the Casu & Wrede Segmented Spacetime (SSZ) framework.

© 2025 Carmen Wrede, Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""

import numpy as np
from dataclasses import dataclass
from typing import Tuple, List, Optional, Dict
import warnings

# =============================================================================
# PHYSICAL CONSTANTS
# =============================================================================

# Fundamental constants (SI units)
C = 299792458.0           # Speed of light [m/s]
G = 6.67430e-11           # Gravitational constant [m³/(kg·s²)]
HBAR = 1.054571817e-34    # Reduced Planck constant [J·s]
M_EARTH = 5.972e24        # Earth mass [kg]
R_EARTH = 6.371e6         # Earth radius [m]

# Golden ratio (fundamental to SSZ)
PHI = (1 + np.sqrt(5)) / 2  # φ ≈ 1.618033988749895

# SSZ-specific constants
ALPHA_SSZ = 1.0           # Coupling constant for segment density
KAPPA_SSZ = 1e-9          # Refractive index coupling (dimensionless)

# -----------------------------------------------------------------------------
# MODEL TAXONOMY (repair 2026-10-31, audit R2):
#   'weak'                     Xi = 1/(2x)                      [established]
#   'strong_A' (alias 'strong') Xi = 1 - exp(-phi/x)            [established]
#   'strong_B'                 Xi = 1 - exp(-phi*x)             [documented variant]
#   'smooth_bridge_hypothesis' C2 quintic blend A->weak on [BLEND_X0, BLEND_X1]
#                              RESEARCH HYPOTHESIS (construction, NOT a field-
#                              equation solution; never used by default).
#   'auto' / 'legacy_auto'     historical DISCONTINUOUS switch at x=100
#                              (DEPRECATED — kept for old code, warns).
# The legacy switch jumps at x=100: Xi(100)=0.01605014135 vs
# Xi(100+eps)=0.00499999995 (documented in tests/test_regressions_r2_models.py).
# -----------------------------------------------------------------------------
BLEND_X0 = 50.0           # blend start [x = r/r_s] (construction choice — OPEN_MODEL_CHOICE)
BLEND_X1 = 150.0          # blend end   [x = r/r_s] (construction choice — OPEN_MODEL_CHOICE)

# Didactic scaling factor (S=1e8) used ONLY in Paper B simulations
# to visualize SSZ effects above noise floors.
# Physical ΔΦ is S times smaller; set S=1 for real-world predictions.
# At Δh=1mm, f=5GHz: ΔΦ ≈ 1.7e-16 rad/gate → 1.7e-10 rad after 10⁶ gates.
DIDACTIC_SCALING = 1e8    # For educational/visualization purposes only


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class Qubit:
    """Represents a single qubit with spatial position and properties."""
    id: str
    x: float  # Position [m]
    y: float  # Position [m]
    z: float  # Height above reference [m]
    coherence_time_T2: float = 100e-6  # Typical T2 time [s]
    gate_time: float = 50e-9  # Typical gate time [s]
    
    @property
    def position(self) -> np.ndarray:
        return np.array([self.x, self.y, self.z])
    
    @property
    def radius_from_earth_center(self) -> float:
        """Distance from Earth's center (assuming z is height above sea level)."""
        return R_EARTH + self.z


@dataclass
class QubitPair:
    """Represents a pair of qubits for two-qubit operations."""
    qubit_a: Qubit
    qubit_b: Qubit
    
    @property
    def separation(self) -> float:
        """Euclidean distance between qubits [m]."""
        return np.linalg.norm(self.qubit_a.position - self.qubit_b.position)
    
    @property
    def height_difference(self) -> float:
        """Height difference between qubits [m]."""
        return abs(self.qubit_a.z - self.qubit_b.z)


@dataclass
class SegmentAnalysis:
    """Results of SSZ segment analysis for a qubit or region."""
    xi: float                    # Segment density Ξ(r)
    time_dilation: float         # D_SSZ = 1/(1 + Ξ)
    local_time_rate: float       # τ_local/τ_∞
    segment_gradient: float      # dΞ/dr [1/m]
    coherence_factor: float      # SSZ-based coherence modifier
    

# =============================================================================
# CORE SSZ FUNCTIONS
# =============================================================================

def schwarzschild_radius(M: float) -> float:
    """
    Calculate Schwarzschild radius for mass M.
    
    r_s = 2GM/c²
    
    Parameters
    ----------
    M : float
        Mass [kg]
        
    Returns
    -------
    float
        Schwarzschild radius [m]
    """
    return 2 * G * M / (C**2)


# =============================================================================
# INPUT VALIDATION (repair 2026-10-31: explicit guards against division by
# zero, NaN/Inf propagation, and undefined M=0 behavior — audit R1/R3)
# =============================================================================

def _validate_radius(r: float) -> float:
    """Reject r <= 0 and non-finite radii (no silent NaN/Inf propagation)."""
    if not np.isfinite(r):
        raise ValueError(f"Radius must be finite, got r={r}")
    if r <= 0:
        raise ValueError(f"Radius must be positive, got r={r}")
    return float(r)


def _validate_mass(M: float) -> float:
    """Reject non-finite or negative masses. M = 0 is allowed (flat spacetime)."""
    if not np.isfinite(M):
        raise ValueError(f"Mass must be finite, got M={M}")
    if M < 0:
        raise ValueError(f"Mass must be non-negative, got M={M}")
    return float(M)


def _canonical_model(regime: str) -> str:
    """Map public regime strings to canonical model names (audit R2).

    'auto' and 'legacy_auto' emit a DeprecationWarning: the historical
    auto-selection is discontinuous at r/r_s = 100 and must not be used
    implicitly in new code. Explicit models: 'weak', 'strong_A' (alias
    'strong'), 'strong_B', 'smooth_bridge_hypothesis'.
    """
    if regime in ('auto', 'legacy_auto'):
        warnings.warn(
            "regime='auto'/'legacy_auto' is DEPRECATED (discontinuous at "
            "r/r_s=100). Use an explicit model: 'weak', 'strong_A', "
            "'strong_B' or — as labeled research hypothesis — "
            "'smooth_bridge_hypothesis'. See docs/audit/ISSUE_MATRIX.md R2.",
            DeprecationWarning,
            stacklevel=3,
        )
        return 'legacy_auto'
    if regime == 'strong':
        return 'strong_A'
    if regime in ('weak', 'strong_A', 'strong_B', 'smooth_bridge_hypothesis'):
        return regime
    raise ValueError(
        f"Unknown regime/model {regime!r}. Valid: 'weak', 'strong_A', 'strong', "
        "'strong_B', 'smooth_bridge_hypothesis', 'legacy_auto' (deprecated), "
        "'auto' (deprecated alias of legacy_auto).")


def _smoothstep_quintic(x: np.ndarray) -> np.ndarray:
    """C2-continuous quintic smoothstep on [BLEND_X0, BLEND_X1] (0 outside)."""
    t = np.clip((x - BLEND_X0) / (BLEND_X1 - BLEND_X0), 0.0, 1.0)
    return t**3 * (10.0 - 15.0 * t + 6.0 * t**2)


def _smoothstep_quintic_dx(x: np.ndarray) -> np.ndarray:
    """d(smoothstep)/dx — 30 t²(1−t)²/(X1−X0), zero outside the blend band."""
    t = np.clip((x - BLEND_X0) / (BLEND_X1 - BLEND_X0), 0.0, 1.0)
    return 30.0 * t**2 * (1.0 - t)**2 / (BLEND_X1 - BLEND_X0)


def _xi_by_model(r: float, r_s: float, model: str) -> float:
    """Xi(r) for a canonical model — single closed form per model."""
    x = r / r_s
    if model == 'weak':
        return r_s / (2.0 * r)
    if model == 'strong_A':
        # 1 - exp(-phi/x), expm1-stable
        return -np.expm1(-PHI / x)
    if model == 'strong_B':
        # 1 - exp(-phi*x), expm1-stable
        return -np.expm1(-PHI * x)
    if model == 'smooth_bridge_hypothesis':
        # RESEARCH HYPOTHESIS: C2 blend (1-s)*A + s*weak. Construction, not
        # physics: no field equation derives this (ISSUE_MATRIX R2).
        s = float(_smoothstep_quintic(x))
        xi_a = -np.expm1(-PHI / x)
        xi_w = 1.0 / (2.0 * x)
        return (1.0 - s) * xi_a + s * xi_w
    raise ValueError(f"No closed form for model {model!r}")


def _u_exponent(model: str, r: float, r_s: float):
    """Exponent u(r) in Xi = 1 − exp(−u(r)) for the exponential models
    (strong_A: u = φ r_s/r; strong_B: u = φ r/r_s). None otherwise."""
    if model == 'strong_A':
        return PHI * r_s / r
    if model == 'strong_B':
        return PHI * r / r_s
    return None


def _du_analytic(model: str, r1: float, r2: float, r_s: float) -> float:
    """Exact u(r1) − u(r2) — analytic form, no cancellation of nearly-equal u."""
    if model == 'strong_A':
        return PHI * r_s * (r2 - r1) / (r1 * r2)
    if model == 'strong_B':
        return PHI * (r1 - r2) / r_s
    raise ValueError(f"No analytic u-difference for model {model!r}")


def _dxi_by_model(r: float, r_s: float, model: str) -> float:
    """Exact dXi/dr for a canonical model — SAME model API as _xi_by_model."""
    x = r / r_s
    if model == 'weak':
        return -r_s / (2.0 * r**2)
    if model == 'strong_A':
        return -(PHI * r_s / r**2) * np.exp(-PHI / x)
    if model == 'strong_B':
        return (PHI / r_s) * np.exp(-PHI * x)
    if model == 'smooth_bridge_hypothesis':
        # dXi/dr = (1/r_s) * [ (1-s)*A_x + s*W_x + s_x*(W - A) ]
        t = float(np.clip((x - BLEND_X0) / (BLEND_X1 - BLEND_X0), 0.0, 1.0))
        s = t**3 * (10.0 - 15.0 * t + 6.0 * t**2)
        s_x = 30.0 * t**2 * (1.0 - t)**2 / (BLEND_X1 - BLEND_X0)
        a_x = -(PHI / x**2) * np.exp(-PHI / x)
        w_x = -1.0 / (2.0 * x**2)
        xi_a = -np.expm1(-PHI / x)
        xi_w = 1.0 / (2.0 * x)
        return ((1.0 - s) * a_x + s * w_x + s_x * (xi_w - xi_a)) / r_s
    raise ValueError(f"No closed derivative for model {model!r}")


def xi_segment_density(r: float, M: float = M_EARTH, regime: str = 'auto') -> float:
    """
    Calculate SSZ segment density Xi(r) at radius r from mass M.
    
    SSZ has TWO REGIMES:
    
    1. WEAK FIELD (r >> r_s, e.g. Earth surface):
        Xi(r) = r_s / (2r)
        This is the Newtonian/weak-field limit, valid for r/r_s > 100
    
    2. STRONG FIELD (r ~ r_s, e.g. near black holes):
        Xi(r) = 1 - exp(-phi * r_s / r)
        This is the saturation form, valid for r/r_s < 10
    
    Parameters
    ----------
    r : float
        Distance from center of mass [m]
    M : float
        Central mass [kg], default is Earth
    regime : str
        'weak' - Use weak-field formula (for Earth, GPS, atomic clocks)
        'strong' - Use saturation formula (for black holes)
        'auto' - Automatically select based on r/r_s ratio (default)
        
    Returns
    -------
    float
        Segment density Xi (dimensionless)
        
    Raises
    ------
    ValueError
        If r <= 0
        
    Notes
    -----
    For qubit applications on Earth (r/r_s ~ 10^9), use 'weak' regime.
    The weak-field formula gives measurable effects (GPS, atomic clocks).
    The saturation formula is for strong-field physics (black holes).

    M = 0 is DEFINED as flat spacetime: Xi = 0 (documented repair
    2026-10-31; previously raised ZeroDivisionError via r/r_s with r_s=0).
    """
    r = _validate_radius(r)
    _validate_mass(M)

    r_s = schwarzschild_radius(M)
    if r_s == 0.0:  # M = 0: flat spacetime by definition
        return 0.0

    model = _canonical_model(regime)

    if model == 'legacy_auto':
        # DEPRECATED historical semantics (kept bit-compatible for old code):
        ratio = r / r_s
        if ratio > 100:
            return r_s / (2 * r)
        return 1.0 - np.exp(-PHI * r_s / r)

    return _xi_by_model(r, r_s, model)


def xi_gradient(r: float, M: float = M_EARTH, regime: str = 'auto') -> float:
    """
    Calculate gradient of segment density dXi/dr.

    TWO REGIMES (each derivative is the EXACT derivative of the density
    formula selected by xi_segment_density for the same regime):

    1. WEAK FIELD:  Xi(r)  = r_s / (2r)
                    dXi/dr = -r_s / (2r^2)
       Negative gradient (Xi decreases with r)

    2. STRONG FIELD (Ansatz A):  Xi_A(r)  = 1 - exp(-phi * r_s / r)
                    dXi_A/dr = -(phi * r_s / r^2) * exp(-phi * r_s / r)
       Negative gradient (Xi_A decreases monotonically with r).

       REPAIR 2026-10-31 (audit R1, commit history of branch
       audit/ssz-qubits-repair-8to6-20261031): the previous implementation
       returned +(phi / r_s) * exp(-phi * r_s / r) — wrong sign AND wrong
       radial factor. Verified against central finite differences and
       mpmath; control value (Earth mass, r = 2 r_s): -20.3077552198 m^-1
       (old buggy value was +81.2310208790 m^-1).

    Parameters
    ----------
    r : float
        Distance from center of mass [m]. Must be finite and > 0.
    M : float
        Central mass [kg]. M = 0 is DEFINED as flat spacetime
        (Xi = 0, gradient = 0) — no division by r_s = 0.
    regime : str
        'weak', 'strong', or 'auto' (default)

    Returns
    -------
    float
        Segment density gradient [1/m]
    """
    r = _validate_radius(r)
    _validate_mass(M)

    r_s = schwarzschild_radius(M)
    if r_s == 0.0:  # M = 0: flat spacetime by definition
        return 0.0

    model = _canonical_model(regime)

    if model == 'legacy_auto':
        # DEPRECATED historical semantics (kept bit-compatible): weak formula
        # above 100 r_s, Ansatz-A derivative below (REPAIRED in R1).
        ratio = r / r_s
        if ratio > 100:
            return -r_s / (2 * r**2)
        return -(PHI * r_s / r**2) * np.exp(-PHI * r_s / r)

    return _dxi_by_model(r, r_s, model)


def ssz_time_dilation(r: float, M: float = M_EARTH, regime: str = 'auto') -> float:
    """
    Calculate SSZ time dilation factor D_SSZ.

    D_SSZ = 1 / (1 + Xi(r))

    This gives the ratio of local proper time to coordinate time.
    D_SSZ < 1 means time runs slower (closer to mass).

    Parameters
    ----------
    r : float
        Distance from center of mass [m]
    M : float
        Central mass [kg]
    regime : str
        'weak', 'strong', or 'auto' (default). 'auto' selects per radius
        exactly as xi_segment_density does, so this function and
        ssz_time_dilation_difference (same regime argument) always refer
        to the SAME model. (regime kwarg added in repair 2026-10-31, R3.)

    Returns
    -------
    float
        Time dilation factor (dimensionless, 0 < D_SSZ <= 1)
    """
    xi = xi_segment_density(r, M, regime=regime)
    return 1.0 / (1.0 + xi)


def ssz_time_dilation_difference(r1: float, r2: float, M: float = M_EARTH,
                                 regime: str = 'auto') -> float:
    """
    Calculate relative time dilation between two radii — model-consistent
    and numerically stable.

    ΔD = D_SSZ(r1) - D_SSZ(r2)

    Positive means r1 has faster time flow than r2.

    REPAIR 2026-10-31 (audit R3/R5-mini): the previous implementation used
    the weak-field closed form D_weak = 2r/(2r+r_s) for ALL radii, which is
    inconsistent with ssz_time_dilation whenever the auto-selection picks
    the strong-field branch (e.g. r1=r_s, r2=2r_s: old -0.13333333333 vs
    true model difference -0.08818137022). The repair computes the
    difference FOR THE SAME MODEL the single-radius function uses:

    - weak model at both radii (explicit 'weak', or auto for r/r_s > 100):
        exact rational form  ΔD = 2 r_s (r1-r2) / ((2r1+r_s)(2r2+r_s))
        (identical to the previous behavior — no back-compat change).
    - strong model (Ansatz A, Xi = 1 - exp(-phi r_s/r)) at one or both
      radii: stable expm1-based evaluation
        Xi_i     = -expm1(-u_i),  u_i = phi r_s / r_i
        Xi2-Xi1  = -exp(-u_1) * expm1(u_1 - u_2)
        ΔD       = (Xi2 - Xi1) / ((1+Xi_1)(1+Xi_2))
      both facts avoid catastrophic cancellation; ΔD is exact to
      machine precision even for Δr/r ~ 1e-10.

    Parameters
    ----------
    r1, r2 : float
        Distances from center of mass [m] (finite, > 0)
    M : float
        Central mass [kg]; M = 0 → ΔD = 0 (flat spacetime)
    regime : str
        'weak'/'strong' → BOTH radii evaluated in that model.
        'auto' (default) → per-radius selection identical to
        ssz_time_dilation (mixed regimes possible near r/r_s = 100;
        each D uses its own branch, matching the single-radius semantics).

    Returns
    -------
    float
        Time dilation difference (dimensionless, signed)
    """
    r1 = _validate_radius(r1)
    r2 = _validate_radius(r2)
    _validate_mass(M)

    r_s = schwarzschild_radius(M)
    if r_s == 0.0:  # M = 0: flat spacetime
        return 0.0

    model = _canonical_model(regime)

    # DEPRECATED historical semantics: per-radius weak/strong-A switch
    if model == 'legacy_auto':
        eff1 = 'weak' if (r1 / r_s) > 100 else 'strong_A'
        eff2 = 'weak' if (r2 / r_s) > 100 else 'strong_A'
    else:
        eff1 = eff2 = model

    # Weak model at both radii: exact stable rational closed form
    if eff1 == 'weak' and eff2 == 'weak':
        return 2 * r_s * (r1 - r2) / ((2 * r1 + r_s) * (2 * r2 + r_s))

    # Same exponential model (A or B) at both radii: Xi = 1 - exp(-u(r)),
    # stable expm1 evaluation with ANALYTIC u-difference (no float
    # cancellation of nearly-equal u values).
    u1 = _u_exponent(eff1, r1, r_s)
    if eff1 == eff2 and u1 is not None:
        du = _du_analytic(eff1, r1, r2, r_s)
        # Xi2 − Xi1 = exp(-u1) − exp(-u2) = -exp(-u1) * expm1(u1 − u2)
        d_xi = -np.exp(-u1) * np.expm1(du)
        u2 = u1 - du
        xi1 = -np.expm1(-u1)
        xi2 = -np.expm1(-u2)
        return d_xi / ((1.0 + xi1) * (1.0 + xi2))

    # General path: mixed regimes (deprecated legacy auto at the 100 r_s
    # boundary) or the bridge hypothesis. No harmful cancellation at the
    # boundary scale (Xi ~ 5e-3..1e-2, ΔXi ~ dXi/dr * Δr >> eps * Xi).
    xi1 = _xi_by_model(r1, r_s, eff1)
    xi2 = _xi_by_model(r2, r_s, eff2)
    return (xi2 - xi1) / ((1.0 + xi1) * (1.0 + xi2))


def time_difference_per_second(r1: float, r2: float, M: float = M_EARTH) -> float:
    """
    Calculate accumulated time difference per coordinate second.
    
    Δt = |D_SSZ(r1) - D_SSZ(r2)| × 1 second
    
    Parameters
    ----------
    r1, r2 : float
        Distances from center of mass [m]
    M : float
        Central mass [kg]
        
    Returns
    -------
    float
        Time difference [s] per coordinate second
    """
    return abs(ssz_time_dilation_difference(r1, r2, M))


# =============================================================================
# QUBIT-SPECIFIC SSZ FUNCTIONS
# =============================================================================

def analyze_qubit_segment(qubit: Qubit, M: float = M_EARTH) -> SegmentAnalysis:
    """
    Perform complete SSZ segment analysis for a qubit.
    
    Parameters
    ----------
    qubit : Qubit
        The qubit to analyze
    M : float
        Central mass [kg]
        
    Returns
    -------
    SegmentAnalysis
        Complete segment analysis results
    """
    r = qubit.radius_from_earth_center
    
    xi = xi_segment_density(r, M)
    d_ssz = ssz_time_dilation(r, M)
    gradient = xi_gradient(r, M)
    
    # Coherence factor: how much SSZ affects coherence
    # Higher gradient = faster decoherence
    coherence_factor = 1.0 / (1.0 + abs(gradient) * 1e6)  # Normalized
    
    return SegmentAnalysis(
        xi=xi,
        time_dilation=d_ssz,
        local_time_rate=d_ssz,
        segment_gradient=gradient,
        coherence_factor=coherence_factor
    )


def qubit_pair_segment_mismatch(pair: QubitPair, M: float = M_EARTH) -> Dict[str, float]:
    """
    Calculate segment mismatch between two qubits.
    
    This is critical for two-qubit gates: segment mismatch causes
    phase errors and decoherence.
    
    Parameters
    ----------
    pair : QubitPair
        The qubit pair to analyze
    M : float
        Central mass [kg]
        
    Returns
    -------
    dict
        Mismatch metrics including:
        - delta_xi: Segment density difference
        - delta_time_dilation: Time dilation difference
        - phase_drift_per_gate: Expected phase drift per gate operation
        - decoherence_enhancement: Factor by which decoherence is enhanced
    """
    r_a = pair.qubit_a.radius_from_earth_center
    r_b = pair.qubit_b.radius_from_earth_center
    
    xi_a = xi_segment_density(r_a, M)
    xi_b = xi_segment_density(r_b, M)
    delta_xi = abs(xi_a - xi_b)

    # REPAIR 2026-10-31 (audit R3): direct subtraction of two nearly-equal
    # D values cancels to 0.0 for small height differences (1 mm → 0.0).
    # Use the model-consistent stable difference instead.
    delta_d = abs(ssz_time_dilation_difference(r_a, r_b, M))
    
    # Phase drift per gate: Δφ = ω × ΔΞ × t_gate
    # where ω = 2π × f_qubit (typically 5 GHz for superconducting qubits)
    avg_gate_time = (pair.qubit_a.gate_time + pair.qubit_b.gate_time) / 2
    omega = 2 * np.pi * 5e9  # 5 GHz qubit frequency
    phase_drift = omega * delta_xi * avg_gate_time
    
    # Decoherence enhancement: 1 + (ΔΞ/Ξ_ref)² where Ξ_ref ~ 10^-10
    # For Earth-scale effects, this is essentially 1.0
    xi_ref = 1e-10  # Reference segment density
    decoherence_enhancement = 1.0 + (delta_xi / xi_ref)**2
    
    return {
        'delta_xi': delta_xi,
        'delta_time_dilation': delta_d,
        'phase_drift_per_gate': phase_drift,
        'decoherence_enhancement': decoherence_enhancement,
        'time_diff_per_microsecond': delta_d * 1e-6  # [s]
    }


def optimal_qubit_height(target_xi: float, M: float = M_EARTH) -> float:
    """
    Calculate optimal height above sea level for target segment density.
    
    Given Ξ_target, find h such that Ξ(R_Earth + h) = Ξ_target.
    
    Parameters
    ----------
    target_xi : float
        Desired segment density
    M : float
        Central mass [kg]
        
    Returns
    -------
    float
        Height above sea level [m]
    """
    if target_xi <= 0:
        raise ValueError("Target Xi must be positive")
    
    r_s = schwarzschild_radius(M)
    r_optimal = r_s / (2 * target_xi)
    height = r_optimal - R_EARTH
    
    return height


def segment_coherent_zone(center_height: float, 
                          max_xi_variation: float = 1e-16,
                          M: float = M_EARTH) -> Tuple[float, float]:
    """
    Calculate the height range where segment density varies by less than max_xi_variation.
    
    This defines a "segment-coherent zone" where qubits can operate
    with minimal SSZ-induced decoherence.
    
    The zone width is calculated using the linear approximation:
        z = 4 * epsilon * R^2 / r_s
    
    This matches the formula in the SSZ Qubit papers.
    
    Parameters
    ----------
    center_height : float
        Center height above sea level [m]
    max_xi_variation : float
        Maximum allowed Ξ variation (epsilon)
    M : float
        Central mass [kg]
        
    Returns
    -------
    tuple
        (min_height, max_height) defining the coherent zone [m]
    """
    r_s = schwarzschild_radius(M)
    r_center = R_EARTH + center_height
    
    # Linear approximation for zone width: z = 4 * eps * R^2 / r_s
    # This comes from: dXi/dh = -r_s / (2*R^2)
    # So: dh = eps / |dXi/dh| = eps * 2 * R^2 / r_s (one direction)
    # Total zone width = 2 * dh = 4 * eps * R^2 / r_s
    zone_width = 4 * max_xi_variation * r_center**2 / r_s
    
    # For center_height = 0 (sea level), the zone extends upward only
    # since we can't go below sea level. The zone width is still the
    # theoretical value, but h_min is clamped to 0.
    h_min = max(0, center_height - zone_width / 2)
    h_max = center_height + zone_width / 2
    
    # If center is at sea level, extend the full zone upward
    if center_height == 0:
        h_max = zone_width
    
    return (h_min, h_max)


# =============================================================================
# GATE TIMING CORRECTIONS
# =============================================================================

def gate_timing_correction(qubit: Qubit, 
                           reference_height: float = 0.0,
                           M: float = M_EARTH) -> float:
    """
    Calculate gate timing correction factor relative to reference height.
    
    Gates designed for reference height need timing adjustment when
    executed at different heights due to SSZ time dilation.
    
    Parameters
    ----------
    qubit : Qubit
        The qubit where gate will be executed
    reference_height : float
        Reference height where gate was calibrated [m]
    M : float
        Central mass [kg]
        
    Returns
    -------
    float
        Correction factor (multiply gate time by this)
    """
    r_qubit = qubit.radius_from_earth_center
    r_ref = R_EARTH + reference_height
    
    d_qubit = ssz_time_dilation(r_qubit, M)
    d_ref = ssz_time_dilation(r_ref, M)
    
    # Gate time needs to be scaled by ratio of time dilation factors
    return d_ref / d_qubit


def two_qubit_gate_timing(pair: QubitPair, M: float = M_EARTH) -> Dict[str, float]:
    """
    Calculate optimal timing for two-qubit gate considering SSZ effects.
    
    Parameters
    ----------
    pair : QubitPair
        The qubit pair for the gate
    M : float
        Central mass [kg]
        
    Returns
    -------
    dict
        Timing recommendations including:
        - optimal_gate_time: Best gate duration
        - timing_asymmetry: Required timing difference between qubits
        - max_fidelity_loss: Expected fidelity loss from SSZ mismatch
    """
    r_a = pair.qubit_a.radius_from_earth_center
    r_b = pair.qubit_b.radius_from_earth_center
    
    d_a = ssz_time_dilation(r_a, M)
    d_b = ssz_time_dilation(r_b, M)
    
    # Average time dilation
    d_avg = (d_a + d_b) / 2
    
    # Timing asymmetry needed to compensate
    timing_asymmetry = abs(d_a - d_b) / d_avg
    
    # Optimal gate time (geometric mean of individual times, scaled)
    t_a = pair.qubit_a.gate_time
    t_b = pair.qubit_b.gate_time
    optimal_gate_time = np.sqrt(t_a * t_b) / d_avg
    
    # Fidelity loss estimate (simplified model)
    # Based on phase error from timing mismatch
    phase_error = 2 * np.pi * timing_asymmetry
    max_fidelity_loss = 1 - np.cos(phase_error / 2)**2
    
    return {
        'optimal_gate_time': optimal_gate_time,
        'timing_asymmetry': timing_asymmetry,
        'max_fidelity_loss': max_fidelity_loss,
        'd_qubit_a': d_a,
        'd_qubit_b': d_b
    }


# =============================================================================
# DECOHERENCE MODELING
# =============================================================================

def ssz_decoherence_rate(qubit: Qubit, 
                         environment_gradient: bool = True,
                         M: float = M_EARTH) -> float:
    """
    Calculate SSZ-enhanced decoherence rate.
    
    The decoherence rate is enhanced by:
    1. Local segment gradient (spatial variation of Ξ)
    2. Segment density itself (higher Ξ = more interaction with spacetime)
    
    Parameters
    ----------
    qubit : Qubit
        The qubit to analyze
    environment_gradient : bool
        Include gradient contribution
    M : float
        Central mass [kg]
        
    Returns
    -------
    float
        Decoherence rate [1/s]
    """
    r = qubit.radius_from_earth_center
    
    # Base decoherence rate from T2
    gamma_base = 1.0 / qubit.coherence_time_T2
    
    # SSZ enhancement from segment density
    # Physical model: SSZ causes dephasing via gravitational time dilation
    # The rate is: gamma_ssz = omega^2 * Xi^2 * tau_c
    # where tau_c is the correlation time (~1 ps for solid-state qubits)
    xi = xi_segment_density(r, M)
    
    omega = 2 * np.pi * 5e9  # 5 GHz qubit frequency
    tau_c = 1e-12  # Correlation time [s]
    gamma_ssz = omega**2 * xi**2 * tau_c
    
    if environment_gradient:
        # Additional contribution from gradient across qubit size
        grad = abs(xi_gradient(r, M))
        qubit_size = 1e-6  # Typical qubit size [m]
        delta_xi = grad * qubit_size
        # Gradient contribution: omega^2 * delta_xi^2 * tau_c
        gamma_grad = omega**2 * delta_xi**2 * tau_c
        gamma_ssz += gamma_grad
    
    # Total rate: base + SSZ contribution
    # Note: For Earth-scale, gamma_ssz << gamma_base (by ~14 orders of magnitude)
    gamma_total = gamma_base + gamma_ssz
    
    return gamma_total


def effective_T2(qubit: Qubit, M: float = M_EARTH) -> float:
    """
    Calculate effective T2 time including SSZ effects.
    
    Parameters
    ----------
    qubit : Qubit
        The qubit to analyze
    M : float
        Central mass [kg]
        
    Returns
    -------
    float
        Effective T2 time [s]
    """
    gamma = ssz_decoherence_rate(qubit, M=M)
    return 1.0 / gamma


def pair_decoherence_time(pair: QubitPair, M: float = M_EARTH) -> float:
    """
    Calculate joint decoherence time for entangled qubit pair.
    
    Entangled pairs decohere faster due to combined SSZ effects
    and segment mismatch.
    
    Parameters
    ----------
    pair : QubitPair
        The entangled qubit pair
    M : float
        Central mass [kg]
        
    Returns
    -------
    float
        Joint decoherence time [s]
    """
    # Individual rates
    gamma_a = ssz_decoherence_rate(pair.qubit_a, M=M)
    gamma_b = ssz_decoherence_rate(pair.qubit_b, M=M)
    
    # Mismatch contribution: omega^2 * delta_xi^2 * tau_c
    mismatch = qubit_pair_segment_mismatch(pair, M)
    omega = 2 * np.pi * 5e9  # 5 GHz
    tau_c = 1e-12  # Correlation time [s]
    gamma_mismatch = omega**2 * mismatch['delta_xi']**2 * tau_c
    
    # Total rate (sum of individual rates plus mismatch)
    # For entangled pairs, rates add
    gamma_total = gamma_a + gamma_b + gamma_mismatch
    
    return 1.0 / gamma_total


# =============================================================================
# ARRAY OPTIMIZATION
# =============================================================================

def optimize_qubit_array(n_qubits: int,
                         base_height: float = 0.0,
                         max_separation: float = 1e-3,
                         M: float = M_EARTH) -> List[Qubit]:
    """
    Generate optimally placed qubit array for minimal SSZ mismatch.
    
    Places qubits in a plane at constant height to minimize
    segment density variation.
    
    Parameters
    ----------
    n_qubits : int
        Number of qubits
    base_height : float
        Base height above sea level [m]
    max_separation : float
        Maximum allowed separation [m]
    M : float
        Central mass [kg]
        
    Returns
    -------
    list
        List of optimally placed Qubit objects
    """
    qubits = []
    
    # Arrange in a grid at constant height
    n_side = int(np.ceil(np.sqrt(n_qubits)))
    spacing = max_separation / n_side
    
    for i in range(n_qubits):
        row = i // n_side
        col = i % n_side
        
        x = col * spacing - (n_side - 1) * spacing / 2
        y = row * spacing - (n_side - 1) * spacing / 2
        z = base_height  # All at same height!
        
        qubit = Qubit(
            id=f"Q{i:03d}",
            x=x,
            y=y,
            z=z
        )
        qubits.append(qubit)
    
    return qubits


def array_segment_uniformity(qubits: List[Qubit], M: float = M_EARTH) -> Dict[str, float]:
    """
    Analyze segment uniformity across qubit array.
    
    Parameters
    ----------
    qubits : list
        List of Qubit objects
    M : float
        Central mass [kg]
        
    Returns
    -------
    dict
        Uniformity metrics
    """
    xi_values = []
    for q in qubits:
        r = q.radius_from_earth_center
        xi_values.append(xi_segment_density(r, M))
    
    xi_array = np.array(xi_values)
    
    return {
        'xi_mean': np.mean(xi_array),
        'xi_std': np.std(xi_array),
        'xi_min': np.min(xi_array),
        'xi_max': np.max(xi_array),
        'xi_range': np.max(xi_array) - np.min(xi_array),
        'uniformity': 1.0 - np.std(xi_array) / np.mean(xi_array) if np.mean(xi_array) > 0 else 0
    }


# =============================================================================
# QUANTUM ERROR CORRECTION (QEC) SUPPORT
# =============================================================================

def segment_aware_syndrome_weight(qubit: Qubit, 
                                  syndrome_type: str = 'X',
                                  M: float = M_EARTH) -> float:
    """
    Calculate segment-aware weight for QEC syndrome measurement.
    
    In SSZ-aware QEC, syndrome weights depend on local segment density.
    
    Parameters
    ----------
    qubit : Qubit
        The qubit being measured
    syndrome_type : str
        'X' or 'Z' syndrome
    M : float
        Central mass [kg]
        
    Returns
    -------
    float
        Syndrome weight (0 to 1)
    """
    analysis = analyze_qubit_segment(qubit, M)
    
    # Base weight
    weight = 1.0
    
    # Modify based on segment properties
    if syndrome_type == 'X':
        # X errors more sensitive to time dilation
        weight *= analysis.time_dilation
    elif syndrome_type == 'Z':
        # Z errors more sensitive to gradient
        weight *= analysis.coherence_factor
    
    return np.clip(weight, 0.0, 1.0)


def calculate_logical_error_rate(qubits: List[Qubit],
                                 code_distance: int = 3,
                                 physical_error_rate: float = 1e-3,
                                 M: float = M_EARTH) -> float:
    """
    Estimate logical error rate for SSZ-aware surface code.
    
    Parameters
    ----------
    qubits : list
        List of physical qubits
    code_distance : int
        Surface code distance
    physical_error_rate : float
        Base physical error rate
    M : float
        Central mass [kg]
        
    Returns
    -------
    float
        Estimated logical error rate
    """
    # Get segment uniformity
    uniformity = array_segment_uniformity(qubits, M)
    
    # SSZ correction factor
    ssz_factor = 1.0 + uniformity['xi_range'] * 1e12
    
    # Effective physical error rate
    p_eff = physical_error_rate * ssz_factor
    
    # Standard surface code scaling: p_L ~ (p/p_th)^((d+1)/2)
    p_threshold = 0.01  # Typical threshold
    if p_eff < p_threshold:
        logical_error_rate = (p_eff / p_threshold) ** ((code_distance + 1) / 2)
    else:
        logical_error_rate = 1.0  # Above threshold
    
    return logical_error_rate


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def height_to_time_offset(height_m: float, 
                          duration_s: float = 1.0,
                          M: float = M_EARTH) -> float:
    """
    Calculate time offset accumulated over duration at given height.
    
    Parameters
    ----------
    height_m : float
        Height above sea level [m]
    duration_s : float
        Duration [s]
    M : float
        Central mass [kg]
        
    Returns
    -------
    float
        Time offset relative to sea level [s]
    """
    r_height = R_EARTH + height_m
    r_sea = R_EARTH
    
    delta_d = ssz_time_dilation_difference(r_height, r_sea, M)
    
    return delta_d * duration_s


def print_qubit_analysis(qubit: Qubit, M: float = M_EARTH) -> None:
    """Print detailed SSZ analysis for a qubit."""
    analysis = analyze_qubit_segment(qubit, M)
    
    print(f"\n{'='*60}")
    print(f"SSZ ANALYSIS: Qubit {qubit.id}")
    print(f"{'='*60}")
    print(f"Position: ({qubit.x*1e3:.3f}, {qubit.y*1e3:.3f}, {qubit.z*1e3:.3f}) mm")
    print(f"Height above sea level: {qubit.z*1e3:.6f} mm")
    print(f"Distance from Earth center: {qubit.radius_from_earth_center/1e6:.6f} Mm")
    print(f"\nSegment Properties:")
    print(f"  Xi(r) = {analysis.xi:.6e}")
    print(f"  D_SSZ = {analysis.time_dilation:.15f}")
    print(f"  dXi/dr = {analysis.segment_gradient:.6e} /m")
    print(f"  Coherence factor = {analysis.coherence_factor:.6f}")
    print(f"\nTiming:")
    print(f"  Base T2 = {qubit.coherence_time_T2*1e6:.1f} us")
    print(f"  Effective T2 = {effective_T2(qubit, M)*1e6:.1f} us")
    print(f"  Gate time = {qubit.gate_time*1e9:.1f} ns")
    print(f"{'='*60}")


def print_pair_analysis(pair: QubitPair, M: float = M_EARTH) -> None:
    """Print detailed SSZ analysis for a qubit pair."""
    mismatch = qubit_pair_segment_mismatch(pair, M)
    timing = two_qubit_gate_timing(pair, M)
    
    print(f"\n{'='*60}")
    print(f"SSZ PAIR ANALYSIS: {pair.qubit_a.id} <-> {pair.qubit_b.id}")
    print(f"{'='*60}")
    print(f"Separation: {pair.separation*1e3:.6f} mm")
    print(f"Height difference: {pair.height_difference*1e6:.3f} um")
    print(f"\nSegment Mismatch:")
    print(f"  Delta Xi = {mismatch['delta_xi']:.6e}")
    print(f"  Delta D_SSZ = {mismatch['delta_time_dilation']:.6e}")
    print(f"  Phase drift/gate = {mismatch['phase_drift_per_gate']:.6e} rad")
    print(f"  Decoherence enhancement = {mismatch['decoherence_enhancement']:.6f}x")
    print(f"\nGate Timing:")
    print(f"  Optimal gate time = {timing['optimal_gate_time']*1e9:.3f} ns")
    print(f"  Timing asymmetry = {timing['timing_asymmetry']:.6e}")
    print(f"  Max fidelity loss = {timing['max_fidelity_loss']:.6e}")
    print(f"\nJoint Decoherence:")
    print(f"  T2_pair = {pair_decoherence_time(pair, M)*1e6:.3f} us")
    print(f"{'='*60}")


# =============================================================================
# MAIN (Demo)
# =============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("SSZ-QUBITS: Segmented Spacetime Framework for Quantum Computing")
    print("="*70)
    
    # Create two qubits at different heights
    q1 = Qubit(id="Q001", x=0, y=0, z=0)           # Sea level
    q2 = Qubit(id="Q002", x=0, y=0, z=0.01)        # 1 cm higher
    
    print_qubit_analysis(q1)
    print_qubit_analysis(q2)
    
    # Analyze as pair
    pair = QubitPair(q1, q2)
    print_pair_analysis(pair)
    
    # Time difference calculation
    print(f"\n{'='*70}")
    print("TIME DILATION EFFECTS")
    print(f"{'='*70}")
    
    heights = [0, 0.001, 0.01, 0.1, 1.0, 10.0]  # meters
    print(f"\n{'Height [m]':>12} | {'Xi(r)':>15} | {'D_SSZ':>18} | {'dt/s [ps]':>12}")
    print("-" * 65)
    
    for h in heights:
        r = R_EARTH + h
        xi = xi_segment_density(r)
        d = ssz_time_dilation(r)
        dt = time_difference_per_second(r, R_EARTH) * 1e12  # picoseconds
        print(f"{h:>12.3f} | {xi:>15.6e} | {d:>18.15f} | {dt:>12.6f}")
    
    print(f"\n{'='*70}")
    print("Demo complete. Import ssz_qubits for full functionality.")
    print(f"{'='*70}")
    print()
    print("=" * 70)
    print("SSZ-Qubits - Segmented Spacetime Framework for Quantum Computing")
    print("Copyright (c) 2025 Carmen Wrede and Lino Casu")
    print("Licensed under the Anti-Capitalist Software License v1.4")
    print("https://github.com/error-wtf/ssz-qubits")
    print("=" * 70)
