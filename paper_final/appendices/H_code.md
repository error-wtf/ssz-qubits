# Appendix H: Code Listings

## H.1 Core SSZ Module

The complete `ssz_qubits.py` module provides all SSZ calculations.

### Constants

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSZ-Qubits: Segmented Spacetime Analysis for Quantum Computing

Core module for calculating SSZ effects on qubit systems.

© 2025 Carmen Wrede & Lino Casu
Licensed under ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""

import numpy as np

# Fundamental constants (CODATA 2018)
C = 299792458.0              # Speed of light [m/s]
G = 6.67430e-11              # Gravitational constant [m³/(kg·s²)]
HBAR = 1.054571817e-34       # Reduced Planck constant [J·s]
PHI = 1.6180339887498948     # Golden ratio

# Earth parameters
M_EARTH = 5.9722e24          # Earth mass [kg]
R_EARTH = 6.371e6            # Earth mean radius [m]
```

### Core Functions

```python
def schwarzschild_radius(M):
    """
    Calculate Schwarzschild radius.
    
    Parameters
    ----------
    M : float
        Mass [kg]
    
    Returns
    -------
    float
        Schwarzschild radius r_s = 2GM/c² [m]
    """
    return 2 * G * M / C**2


def xi_segment_density(r, M, regime='auto'):
    """
    Calculate SSZ segment density Ξ(r).
    
    Parameters
    ----------
    r : float
        Radial distance from center [m]
    M : float
        Central mass [kg]
    regime : str
        'weak', 'strong', or 'auto' (default)
    
    Returns
    -------
    float
        Segment density Ξ (dimensionless)
    """
    r_s = schwarzschild_radius(M)
    x = r / r_s
    
    if regime == 'weak' or (regime == 'auto' and x > 110):
        return r_s / (2 * r)
    elif regime == 'strong' or (regime == 'auto' and x < 90):
        return 1 - np.exp(-PHI * x)
    else:
        # Transition zone: smooth blend
        t = (x - 90) / 20
        b = 6*t**5 - 15*t**4 + 10*t**3
        xi_weak = r_s / (2 * r)
        xi_strong = 1 - np.exp(-PHI * x)
        return b * xi_weak + (1 - b) * xi_strong


def ssz_time_dilation(r, M):
    """
    Calculate SSZ time dilation factor D(r).
    
    Parameters
    ----------
    r : float
        Radial distance [m]
    M : float
        Central mass [kg]
    
    Returns
    -------
    float
        Time dilation factor D = 1/(1+Ξ)
    """
    xi = xi_segment_density(r, M)
    return 1 / (1 + xi)


def differential_time_dilation(delta_h, M=M_EARTH, R=R_EARTH):
    """
    Calculate differential time dilation ΔD for height difference.
    
    Parameters
    ----------
    delta_h : float
        Height difference [m]
    M : float
        Central mass [kg]
    R : float
        Reference radius [m]
    
    Returns
    -------
    float
        Differential time dilation ΔD ≈ r_s × Δh / R²
    """
    r_s = schwarzschild_radius(M)
    return r_s * delta_h / R**2


def phase_drift(omega, delta_h, t, M=M_EARTH, R=R_EARTH):
    """
    Calculate SSZ phase drift.
    
    Parameters
    ----------
    omega : float
        Angular frequency [rad/s]
    delta_h : float
        Height difference [m]
    t : float
        Evolution time [s]
    M : float
        Central mass [kg]
    R : float
        Reference radius [m]
    
    Returns
    -------
    float
        Phase drift ΔΦ = ω × ΔD × t [rad]
    """
    delta_D = differential_time_dilation(delta_h, M, R)
    return omega * delta_D * t


def zone_width(epsilon, M=M_EARTH, R=R_EARTH):
    """
    Calculate segment-coherent zone width.
    
    Parameters
    ----------
    epsilon : float
        Phase tolerance [rad]
    M : float
        Central mass [kg]
    R : float
        Reference radius [m]
    
    Returns
    -------
    float
        Zone width z(ε) = 4ε × R² / r_s [m]
    """
    r_s = schwarzschild_radius(M)
    return 4 * epsilon * R**2 / r_s
```

---

## H.2 Qubit Classes

```python
class Qubit:
    """
    Represents a qubit with SSZ-relevant properties.
    """
    
    def __init__(self, frequency, height, coherence_time=100e-6, name=None):
        """
        Initialize qubit.
        
        Parameters
        ----------
        frequency : float
            Qubit frequency [Hz]
        height : float
            Height above reference [m]
        coherence_time : float
            T₂ coherence time [s]
        name : str
            Optional identifier
        """
        self.frequency = frequency
        self.omega = 2 * np.pi * frequency
        self.height = height
        self.coherence_time = coherence_time
        self.name = name or f"Q_{id(self)}"
    
    def analyze_ssz(self, M=M_EARTH, R=R_EARTH):
        """
        Analyze SSZ properties at qubit location.
        
        Returns
        -------
        dict
            SSZ analysis results
        """
        r = R + self.height
        xi = xi_segment_density(r, M)
        D = ssz_time_dilation(r, M)
        
        return {
            'name': self.name,
            'frequency_Hz': self.frequency,
            'height_m': self.height,
            'xi': xi,
            'D': D,
            'effective_frequency': self.frequency * D,
        }


class QubitPair:
    """
    Represents a pair of qubits for SSZ drift analysis.
    """
    
    def __init__(self, q1, q2):
        """
        Initialize qubit pair.
        
        Parameters
        ----------
        q1, q2 : Qubit
            The two qubits
        """
        self.q1 = q1
        self.q2 = q2
        self.delta_h = abs(q2.height - q1.height)
    
    def phase_drift(self, time, M=M_EARTH, R=R_EARTH):
        """
        Calculate phase drift between qubits.
        
        Parameters
        ----------
        time : float
            Evolution time [s]
        
        Returns
        -------
        float
            Phase drift [rad]
        """
        omega_avg = (self.q1.omega + self.q2.omega) / 2
        return phase_drift(omega_avg, self.delta_h, time, M, R)
    
    def compensation_phase(self, time, M=M_EARTH, R=R_EARTH):
        """
        Calculate required compensation phase.
        
        Returns
        -------
        float
            Compensation phase Φ_corr = -ΔΦ [rad]
        """
        return -self.phase_drift(time, M, R)
```

---

## H.3 Validation Functions

```python
def validate_gps():
    """
    Validate SSZ against GPS time dilation.
    
    GPS satellites at ~20,200 km experience ~38 μs/day speedup.
    """
    h_gps = 20200e3  # GPS orbit altitude [m]
    
    D_surface = ssz_time_dilation(R_EARTH, M_EARTH)
    D_gps = ssz_time_dilation(R_EARTH + h_gps, M_EARTH)
    
    delta_D = D_gps - D_surface
    delta_t_per_day = delta_D * 86400  # seconds per day
    
    expected = 38e-6  # ~38 μs/day
    relative_error = abs(delta_t_per_day - expected) / expected
    
    return {
        'D_surface': D_surface,
        'D_gps': D_gps,
        'delta_t_per_day_s': delta_t_per_day,
        'delta_t_per_day_us': delta_t_per_day * 1e6,
        'expected_us': expected * 1e6,
        'relative_error': relative_error,
        'pass': relative_error < 0.15  # Within 15%
    }


def validate_pound_rebka():
    """
    Validate SSZ against Pound-Rebka experiment.
    
    22.5 m tower gave fractional shift of 2.46e-15.
    """
    h = 22.5  # Tower height [m]
    
    D_bottom = ssz_time_dilation(R_EARTH, M_EARTH)
    D_top = ssz_time_dilation(R_EARTH + h, M_EARTH)
    
    delta_nu_nu = D_top - D_bottom
    
    expected = 2.46e-15
    relative_error = abs(abs(delta_nu_nu) - expected) / expected
    
    return {
        'h_m': h,
        'delta_nu_nu': delta_nu_nu,
        'expected': expected,
        'relative_error': relative_error,
        'pass': relative_error < 0.20  # Within 20%
    }
```

---

## H.4 Figure Generation Example

```python
import matplotlib.pyplot as plt

def plot_phase_vs_height():
    """Generate Figure F1: Phase drift vs height."""
    
    # Parameters
    r_s = schwarzschild_radius(M_EARTH)
    omega_transmon = 2 * np.pi * 5e9
    omega_optical = 2 * np.pi * 429e12
    t_transmon = 100e-6
    t_optical = 1.0
    
    # Height range
    dh = np.logspace(-4, 1, 100)  # 0.1 mm to 10 m
    
    # Phase drift
    phi_transmon = omega_transmon * r_s * dh / R_EARTH**2 * t_transmon
    phi_optical = omega_optical * r_s * dh / R_EARTH**2 * t_optical
    
    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.loglog(dh * 1000, phi_transmon, 'b-', lw=2, 
              label='Transmon (5 GHz, 100 μs)')
    ax.loglog(dh * 1000, phi_optical, 'r-', lw=2, 
              label='Optical Clock (429 THz, 1 s)')
    
    ax.axhline(1, color='gray', ls='--', label='Noise floor (~1 rad)')
    ax.axhline(1e-3, color='gray', ls=':', label='Optical noise (~10⁻³ rad)')
    
    ax.set_xlabel('Height Difference Δh [mm]')
    ax.set_ylabel('Phase Drift ΔΦ [rad]')
    ax.set_title('SSZ Phase Drift vs Height Difference')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.savefig('F1_phase_vs_height.png', dpi=300)
    return fig
```

---

## H.5 Test Example

```python
import pytest

def test_schwarzschild_radius_earth():
    """Earth's Schwarzschild radius is ~8.87 mm."""
    r_s = schwarzschild_radius(M_EARTH)
    assert 8.8e-3 < r_s < 8.9e-3

def test_segment_density_earth_surface():
    """Segment density at Earth surface is ~7e-10."""
    xi = xi_segment_density(R_EARTH, M_EARTH)
    assert 6e-10 < xi < 8e-10

def test_time_dilation_earth_surface():
    """Time dilation at Earth surface is ~1 - 7e-10."""
    D = ssz_time_dilation(R_EARTH, M_EARTH)
    assert 0.9999999990 < D < 0.9999999995

def test_phase_drift_transmon():
    """Phase drift for transmon is ~6.87e-13 rad."""
    dphi = phase_drift(
        omega=2*np.pi*5e9,
        delta_h=1e-3,
        t=100e-6
    )
    assert 6e-13 < dphi < 8e-13

def test_zone_width():
    """Zone width at ε=10⁻¹⁸ is ~18.3 mm."""
    z = zone_width(1e-18)
    assert 1.5e-2 < z < 2.0e-2
```

---

## H.6 Usage Examples

```python
# Quick calculation
from ssz_qubits import *

# Transmon phase drift
dphi = phase_drift(omega=2*np.pi*5e9, delta_h=1e-3, t=100e-6)
print(f"Transmon drift: {dphi:.2e} rad")
# Output: Transmon drift: 6.87e-13 rad

# Optical clock drift
dphi = phase_drift(omega=2*np.pi*429e12, delta_h=1.0, t=1.0)
print(f"Optical drift: {dphi:.2f} rad")
# Output: Optical drift: 0.59 rad

# Create qubit pair
q1 = Qubit(frequency=5e9, height=0)
q2 = Qubit(frequency=5e9, height=0.001)
pair = QubitPair(q1, q2)
print(f"Pair drift (100 μs): {pair.phase_drift(100e-6):.2e} rad")

# Validate against experiments
print(validate_gps())
print(validate_pound_rebka())
```
