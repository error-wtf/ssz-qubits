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


def xi_segment_density(r: float, M: float = M_EARTH, regime: str = 'auto') -> float:
    """
    Calculate SSZ segment density Xi(r) at radius r from mass M.
    
    SSZ has TWO REGIMES:
    
    1. WEAK FIELD (r >> r_s, e.g. Earth surface):
        Xi(r) = r_s / (2r)
        This is the Newtonian/weak-field limit, valid for r/r_s > 100
    
    2. STRONG FIELD (r ~ r_s, e.g. near black holes):
        Xi(r) = 1 - exp(-phi * r / r_s)
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
    """
    if r <= 0:
        raise ValueError(f"Radius must be positive, got r={r}")
    
    r_s = schwarzschild_radius(M)
    ratio = r / r_s
    
    # Auto-select regime based on r/r_s ratio
    if regime == 'auto':
        if ratio > 100:  # Weak field (Earth, Solar System)
            regime = 'weak'
        else:  # Strong field (near compact objects)
            regime = 'strong'
    
    if regime == 'weak':
        # WEAK FIELD: Xi(r) = r_s / (2r)
        # This gives measurable effects on Earth
        return r_s / (2 * r)
    else:
        # STRONG FIELD (Saturation): Xi(r) = 1 - exp(-phi * r / r_s)
        # This is singularity-free for black holes
        return 1.0 - np.exp(-PHI * r / r_s)


def xi_gradient(r: float, M: float = M_EARTH, regime: str = 'auto') -> float:
    """
    Calculate gradient of segment density dXi/dr.
    
    TWO REGIMES:
    
    1. WEAK FIELD: dXi/dr = -r_s / (2r^2)
       Negative gradient (Xi decreases with r)
    
    2. STRONG FIELD: dXi/dr = (phi / r_s) * exp(-phi * r / r_s)
       Positive gradient (Xi increases with r in saturation form)
    
    Parameters
    ----------
    r : float
        Distance from center of mass [m]
    M : float
        Central mass [kg]
    regime : str
        'weak', 'strong', or 'auto' (default)
        
    Returns
    -------
    float
        Segment density gradient [1/m]
    """
    if r <= 0:
        raise ValueError(f"Radius must be positive, got r={r}")
    
    r_s = schwarzschild_radius(M)
    ratio = r / r_s
    
    if regime == 'auto':
        regime = 'weak' if ratio > 100 else 'strong'
    
    if regime == 'weak':
        # WEAK FIELD: dXi/dr = -r_s / (2r^2)
        return -r_s / (2 * r**2)
    else:
        # STRONG FIELD: dXi/dr = (phi / r_s) * exp(-phi * r / r_s)
        return (PHI / r_s) * np.exp(-PHI * r / r_s)


def ssz_time_dilation(r: float, M: float = M_EARTH) -> float:
    """
    Calculate SSZ time dilation factor D_SSZ.
    
    D_SSZ = 1 / (1 + Ξ(r))
    
    This gives the ratio of local proper time to coordinate time.
    D_SSZ < 1 means time runs slower (closer to mass).
    
    Parameters
    ----------
    r : float
        Distance from center of mass [m]
    M : float
        Central mass [kg]
        
    Returns
    -------
    float
        Time dilation factor (dimensionless, 0 < D_SSZ <= 1)
    """
    xi = xi_segment_density(r, M)
    return 1.0 / (1.0 + xi)


def ssz_time_dilation_difference(r1: float, r2: float, M: float = M_EARTH) -> float:
    """
    Calculate relative time dilation between two radii.
    
    ΔD = D_SSZ(r1) - D_SSZ(r2)
    
    Positive means r1 has faster time flow than r2.
    
    Parameters
    ----------
    r1, r2 : float
        Distances from center of mass [m]
    M : float
        Central mass [kg]
        
    Returns
    -------
    float
        Time dilation difference (dimensionless)
    """
    return ssz_time_dilation(r1, M) - ssz_time_dilation(r2, M)


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
    
    d_a = ssz_time_dilation(r_a, M)
    d_b = ssz_time_dilation(r_b, M)
    delta_d = abs(d_a - d_b)
    
    # Phase drift per gate: Δφ = 2π × Δt/T_gate × (gate_time)
    # Using average gate time
    avg_gate_time = (pair.qubit_a.gate_time + pair.qubit_b.gate_time) / 2
    phase_drift = 2 * np.pi * delta_d * avg_gate_time / avg_gate_time  # Simplified
    
    # Decoherence enhancement: exponential in segment mismatch
    decoherence_enhancement = np.exp(delta_xi * 1e9)  # Scaled for visibility
    
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
    
    Parameters
    ----------
    center_height : float
        Center height above sea level [m]
    max_xi_variation : float
        Maximum allowed Ξ variation
    M : float
        Central mass [kg]
        
    Returns
    -------
    tuple
        (min_height, max_height) defining the coherent zone [m]
    """
    r_center = R_EARTH + center_height
    xi_center = xi_segment_density(r_center, M)
    
    # Find heights where Ξ = Ξ_center ± max_xi_variation/2
    r_s = schwarzschild_radius(M)
    
    xi_min = xi_center - max_xi_variation / 2
    xi_max = xi_center + max_xi_variation / 2
    
    if xi_min <= 0:
        xi_min = 1e-20  # Prevent division by zero
    
    r_max = r_s / (2 * xi_min)  # Higher r = lower Ξ
    r_min = r_s / (2 * xi_max)  # Lower r = higher Ξ
    
    h_min = max(0, r_min - R_EARTH)
    h_max = r_max - R_EARTH
    
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
    xi = xi_segment_density(r, M)
    gamma_xi = gamma_base * (1 + xi * 1e9)  # Scaled for Earth's weak field
    
    if environment_gradient:
        # Additional contribution from gradient
        grad = abs(xi_gradient(r, M))
        # Gradient causes dephasing over qubit's spatial extent (~1 μm)
        qubit_size = 1e-6  # Typical qubit size [m]
        delta_xi = grad * qubit_size
        gamma_grad = gamma_base * delta_xi * 1e15  # Scaled
        gamma_xi += gamma_grad
    
    return gamma_xi


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
    
    # Mismatch contribution
    mismatch = qubit_pair_segment_mismatch(pair, M)
    gamma_mismatch = mismatch['delta_xi'] * 1e12  # Scaled
    
    # Total rate (sum of individual rates plus mismatch)
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
