#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSZ Entanglement Module - Paper B Support

This module provides functions for analyzing gravitational effects
on entangled qubit pairs, as described in Paper B.

All functions are consistent with the core ssz_qubits module and
reproduce the numerical values in the paper.
"""
import numpy as np
from typing import Dict, Tuple, Optional
from dataclasses import dataclass

from ssz_qubits import (
    Qubit, QubitPair, 
    ssz_time_dilation_difference, 
    qubit_pair_segment_mismatch,
    segment_coherent_zone,
    R_EARTH, M_EARTH
)


@dataclass
class EntangledPairAnalysis:
    """Analysis results for an entangled qubit pair."""
    height_difference: float  # [m]
    delta_D: float  # Time dilation difference (signed)
    phase_drift_per_gate: float  # [rad]
    phase_drift_per_second: float  # [rad/s]
    T_SSZ: float  # Characteristic time to pi phase [s]
    fidelity_after_N_gates: float  # F = cos^2(Delta_Phi/2)
    CHSH_parameter: float  # S = 2*sqrt(2)*cos(Delta_Phi)
    in_coherent_zone: bool  # Whether pair is in same coherent zone


def entangled_pair_phase_drift(
    pair: QubitPair,
    qubit_frequency: float = 5e9,
    M: float = M_EARTH
) -> Dict[str, float]:
    """
    Calculate phase drift for an entangled qubit pair.
    
    The phase drift is deterministic and geometry-locked:
    Delta_Phi(t) = omega * Delta_D * t
    
    For discrete gates:
    Delta_Phi = N * omega * Delta_D * t_gate
    
    Parameters
    ----------
    pair : QubitPair
        The entangled qubit pair
    qubit_frequency : float
        Qubit transition frequency [Hz], default 5 GHz
    M : float
        Central mass [kg], default Earth
        
    Returns
    -------
    dict
        Phase drift analysis including:
        - delta_D: Signed time dilation difference D(r_A) - D(r_B)
        - phase_drift_per_gate: |Delta_Phi| per gate [rad]
        - phase_drift_per_second: |Delta_Phi| per second [rad/s]
        - omega: Angular frequency [rad/s]
    """
    r_a = pair.qubit_a.radius_from_earth_center
    r_b = pair.qubit_b.radius_from_earth_center
    
    # Signed time dilation difference: D(r_A) - D(r_B)
    # Positive if qubit A is higher (accumulates phase faster)
    delta_D = ssz_time_dilation_difference(r_a, r_b, M)
    
    omega = 2 * np.pi * qubit_frequency
    avg_gate_time = (pair.qubit_a.gate_time + pair.qubit_b.gate_time) / 2
    
    # Phase drift per gate (magnitude)
    phase_drift_per_gate = abs(omega * delta_D * avg_gate_time)
    
    # Phase drift per second of continuous evolution
    phase_drift_per_second = abs(omega * delta_D)
    
    return {
        'delta_D': delta_D,
        'delta_D_magnitude': abs(delta_D),
        'phase_drift_per_gate': phase_drift_per_gate,
        'phase_drift_per_second': phase_drift_per_second,
        'omega': omega,
        'gate_time': avg_gate_time
    }


def bell_state_fidelity(delta_phi: float) -> float:
    """
    Calculate Bell state fidelity after phase drift.
    
    F = |<Psi+|Psi(t)>|^2 = cos^2(Delta_Phi/2)
    
    Parameters
    ----------
    delta_phi : float
        Accumulated phase difference [rad]
        
    Returns
    -------
    float
        Fidelity with respect to initial |Psi+> state
    """
    return np.cos(delta_phi / 2)**2


def bell_state_fidelity_approx(delta_phi: float) -> float:
    """
    Small-angle approximation for Bell state fidelity.
    
    F ≈ 1 - Delta_Phi^2/4 for Delta_Phi << 1
    
    Parameters
    ----------
    delta_phi : float
        Accumulated phase difference [rad]
        
    Returns
    -------
    float
        Approximate fidelity (valid for small phases)
    """
    return 1 - delta_phi**2 / 4


def chsh_parameter(delta_phi: float) -> float:
    """
    Calculate CHSH parameter for fixed measurement settings.
    
    For fixed measurement settings optimized for |Psi+> (and not
    re-optimized as the state evolves):
    
    S(Delta_Phi) = 2*sqrt(2) * cos(Delta_Phi)
    
    Parameters
    ----------
    delta_phi : float
        Accumulated phase difference [rad]
        
    Returns
    -------
    float
        CHSH parameter S (max 2*sqrt(2) ≈ 2.83)
    """
    return 2 * np.sqrt(2) * np.cos(delta_phi)


def characteristic_time_T_SSZ(
    height_difference: float,
    qubit_frequency: float = 5e9,
    M: float = M_EARTH
) -> float:
    """
    Calculate characteristic SSZ time T_SSZ.
    
    T_SSZ = pi / (omega * |Delta_D|)
    
    This is the time for the accumulated phase to reach pi,
    at which point the Bell state has rotated from |Psi+> to |Psi->.
    
    NOTE: T_SSZ is NOT a decoherence time. It is a deterministic
    geometric timescale, not a coherence lifetime.
    
    Parameters
    ----------
    height_difference : float
        Height separation between qubits [m]
    qubit_frequency : float
        Qubit transition frequency [Hz], default 5 GHz
    M : float
        Central mass [kg], default Earth
        
    Returns
    -------
    float
        Characteristic time T_SSZ [s]
    """
    r1 = R_EARTH
    r2 = R_EARTH + height_difference
    delta_D = abs(ssz_time_dilation_difference(r1, r2, M))
    omega = 2 * np.pi * qubit_frequency
    
    if delta_D == 0:
        return np.inf
    
    return np.pi / (omega * delta_D)


def correction_interval(
    phase_tolerance: float,
    phase_drift_per_gate: float
) -> float:
    """
    Calculate maximum gates before phase correction needed.
    
    N_corr = epsilon / |Delta_Phi_gate|
    
    Parameters
    ----------
    phase_tolerance : float
        Maximum allowed phase drift [rad]
    phase_drift_per_gate : float
        Phase drift per gate operation [rad]
        
    Returns
    -------
    float
        Maximum number of gates before correction
    """
    if phase_drift_per_gate == 0:
        return np.inf
    return phase_tolerance / phase_drift_per_gate


def correction_gate(delta_phi: float, higher_qubit: str = 'A') -> Dict[str, float]:
    """
    Calculate the required correction gate.
    
    The sign convention Delta_D = D(r_A) - D(r_B) determines which
    qubit requires correction:
    - If Delta_D > 0 (qubit A higher): apply Rz(-Delta_Phi) to A
    - If Delta_D < 0 (qubit B higher): apply Rz(-Delta_Phi) to B
    
    Parameters
    ----------
    delta_phi : float
        Accumulated phase drift [rad] (signed)
    higher_qubit : str
        Which qubit is at higher altitude ('A' or 'B')
        
    Returns
    -------
    dict
        Correction specification including:
        - target_qubit: Which qubit to correct
        - rotation_angle: Rz rotation angle [rad]
    """
    if higher_qubit == 'A':
        return {
            'target_qubit': 'A',
            'rotation_angle': -delta_phi,
            'gate': f'Rz({-delta_phi:.6e})'
        }
    else:
        return {
            'target_qubit': 'B', 
            'rotation_angle': delta_phi,
            'gate': f'Rz({delta_phi:.6e})'
        }


def is_in_coherent_zone(
    pair: QubitPair,
    tolerance: float = 1e-18,
    M: float = M_EARTH
) -> bool:
    """
    Check if entangled pair is within same segment-coherent zone.
    
    Entangled qubits placed within the same segment-coherent zone
    experience no relative SSZ phase drift (within tolerance).
    
    Parameters
    ----------
    pair : QubitPair
        The entangled qubit pair
    tolerance : float
        Maximum allowed Xi variation (epsilon)
    M : float
        Central mass [kg]
        
    Returns
    -------
    bool
        True if both qubits are in same coherent zone
    """
    h_a = pair.qubit_a.z
    h_b = pair.qubit_b.z
    
    # Get coherent zone centered at lower qubit
    h_center = min(h_a, h_b)
    zone = segment_coherent_zone(h_center, tolerance, M)
    
    # Check if both qubits are within zone
    h_min, h_max = zone
    return h_min <= h_a <= h_max and h_min <= h_b <= h_max


def analyze_entangled_pair(
    pair: QubitPair,
    N_gates: int = 10**9,
    qubit_frequency: float = 5e9,
    coherence_tolerance: float = 1e-18,
    M: float = M_EARTH
) -> EntangledPairAnalysis:
    """
    Complete analysis of an entangled qubit pair.
    
    This function computes all quantities relevant to Paper B:
    - Phase drift (per gate and continuous)
    - Bell state fidelity after N gates
    - CHSH parameter
    - Characteristic time T_SSZ
    - Coherent zone membership
    
    Parameters
    ----------
    pair : QubitPair
        The entangled qubit pair
    N_gates : int
        Number of gate operations for fidelity calculation
    qubit_frequency : float
        Qubit transition frequency [Hz]
    coherence_tolerance : float
        Tolerance for coherent zone check
    M : float
        Central mass [kg]
        
    Returns
    -------
    EntangledPairAnalysis
        Complete analysis results
    """
    # Height difference
    h_diff = pair.qubit_a.z - pair.qubit_b.z
    
    # Phase drift analysis
    drift = entangled_pair_phase_drift(pair, qubit_frequency, M)
    
    # Accumulated phase after N gates
    delta_phi_total = N_gates * drift['phase_drift_per_gate']
    
    # Fidelity and CHSH
    F = bell_state_fidelity(delta_phi_total)
    S = chsh_parameter(delta_phi_total)
    
    # Characteristic time
    T = characteristic_time_T_SSZ(abs(h_diff), qubit_frequency, M)
    
    # Coherent zone check
    in_zone = is_in_coherent_zone(pair, coherence_tolerance, M)
    
    return EntangledPairAnalysis(
        height_difference=h_diff,
        delta_D=drift['delta_D'],
        phase_drift_per_gate=drift['phase_drift_per_gate'],
        phase_drift_per_second=drift['phase_drift_per_second'],
        T_SSZ=T,
        fidelity_after_N_gates=F,
        CHSH_parameter=S,
        in_coherent_zone=in_zone
    )


def print_entangled_pair_analysis(analysis: EntangledPairAnalysis, N_gates: int = 10**9):
    """Pretty-print entangled pair analysis results."""
    print("=" * 60)
    print("ENTANGLED PAIR ANALYSIS")
    print("=" * 60)
    print(f"Height difference: {analysis.height_difference*1000:.3f} mm")
    print(f"Delta_D (signed): {analysis.delta_D:.6e}")
    print()
    print("Phase Drift:")
    print(f"  Per gate: {analysis.phase_drift_per_gate:.6e} rad")
    print(f"  Per second: {analysis.phase_drift_per_second:.6e} rad/s")
    print(f"  After {N_gates:.0e} gates: {N_gates * analysis.phase_drift_per_gate:.6e} rad")
    print()
    print("Entanglement Metrics:")
    print(f"  Fidelity F: {analysis.fidelity_after_N_gates:.15f}")
    print(f"  1 - F: {1 - analysis.fidelity_after_N_gates:.2e}")
    print(f"  CHSH S: {analysis.CHSH_parameter:.6f}")
    print(f"  S/S_max: {analysis.CHSH_parameter / (2*np.sqrt(2)):.15f}")
    print()
    print("Characteristic Time:")
    print(f"  T_SSZ: {analysis.T_SSZ:.6e} s")
    print(f"  T_SSZ: {analysis.T_SSZ / (365.25*24*3600):.1f} years")
    print()
    print(f"In coherent zone: {'YES' if analysis.in_coherent_zone else 'NO'}")
    print("=" * 60)


# =============================================================================
# DEMO
# =============================================================================
if __name__ == '__main__':
    print("SSZ Entanglement Module - Demo")
    print()
    
    # Create entangled pair with 1 mm height difference
    q1 = Qubit(id='Alice', x=0, y=0, z=0, gate_time=50e-9)
    q2 = Qubit(id='Bob', x=0, y=0, z=1e-3, gate_time=50e-9)  # 1 mm higher
    pair = QubitPair(q1, q2)
    
    # Full analysis
    analysis = analyze_entangled_pair(pair, N_gates=10**9)
    print_entangled_pair_analysis(analysis)
    
    print()
    print("Correction Protocol:")
    delta_phi = 10**9 * analysis.phase_drift_per_gate
    corr = correction_gate(delta_phi, higher_qubit='B')
    print(f"  Target: Qubit {corr['target_qubit']}")
    print(f"  Gate: {corr['gate']}")
