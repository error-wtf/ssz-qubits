#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Final Plots for Paper C v1.2 (Bulletproof Edition)

All values corrected and verified.

(c) 2025 Carmen Wrede, Lino Casu
"""

import os
import sys

if sys.platform.startswith('win'):
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator

from ssz_qubits import (
    M_EARTH, R_EARTH, schwarzschild_radius,
    ssz_time_dilation_difference
)

# Constants
R_S_EARTH = schwarzschild_radius(M_EARTH)
OMEGA_5GHZ = 2 * np.pi * 5e9
OMEGA_OPTICAL = 2 * np.pi * 429e12  # 429 THz optical clock

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'outputs')
os.makedirs(OUTPUT_DIR, exist_ok=True)

plt.style.use('seaborn-v0_8-whitegrid')
COLORS = {
    'ssz': '#2E86AB',
    'optical': '#28A745',
    'threshold': '#DC3545',
    'qubit': '#FFC107'
}


def fig1_platform_comparison():
    """Figure 1: Platform comparison - Transmon vs Optical Clock."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Left: Signal size vs height
    heights = np.logspace(-3, 2, 100)  # 1 mm to 100 m
    
    # Transmon: 5 GHz, 100 us
    signal_transmon = []
    for h in heights:
        dd = abs(ssz_time_dilation_difference(R_EARTH + h, R_EARTH, M_EARTH))
        phi = OMEGA_5GHZ * dd * 100e-6
        signal_transmon.append(phi)
    
    # Optical clock: 429 THz, 1 s
    signal_optical = []
    for h in heights:
        dd = abs(ssz_time_dilation_difference(R_EARTH + h, R_EARTH, M_EARTH))
        phi = OMEGA_OPTICAL * dd * 1.0
        signal_optical.append(phi)
    
    ax1.loglog(heights, signal_transmon, '-', color=COLORS['qubit'], 
               linewidth=2.5, label='Transmon (5 GHz, 100 $\mu$s)')
    ax1.loglog(heights, signal_optical, '-', color=COLORS['optical'],
               linewidth=2.5, label='Optical Clock (429 THz, 1 s)')
    
    # Detection threshold (~1 rad for single shot)
    ax1.axhline(y=1, color=COLORS['threshold'], linestyle='--', 
                label='Single-shot noise floor (~1 rad)')
    ax1.axhline(y=1e-5, color=COLORS['threshold'], linestyle=':', alpha=0.7,
                label='After $10^{10}$ averages')
    
    # Key points
    ax1.scatter([1], [signal_optical[np.searchsorted(heights, 1)]], 
                color=COLORS['optical'], s=100, zorder=5)
    ax1.annotate('1 m: 0.29 rad\n(detectable!)', xy=(1, 0.3), xytext=(3, 0.05),
                fontsize=10, arrowprops=dict(arrowstyle='->', color='gray'))
    
    ax1.set_xlabel('Height difference $\Delta h$ [m]', fontsize=12)
    ax1.set_ylabel('Phase shift $\Delta\Phi$ [rad]', fontsize=12)
    ax1.set_title('(a) Signal Size: Transmon vs Optical Clock', fontsize=12)
    ax1.legend(loc='lower right', fontsize=9)
    ax1.set_xlim(1e-3, 100)
    ax1.set_ylim(1e-15, 100)
    ax1.grid(True, which='both', alpha=0.3)
    
    # Right: Required averages for SNR=3
    n_transmon = []
    n_optical = []
    for i, h in enumerate(heights):
        if signal_transmon[i] > 0:
            n = (3 * 1.0 / signal_transmon[i])**2
            n_transmon.append(n)
        else:
            n_transmon.append(np.inf)
        if signal_optical[i] > 0:
            n = (3 * 1.0 / signal_optical[i])**2
            n_optical.append(n)
        else:
            n_optical.append(np.inf)
    
    ax2.loglog(heights, n_transmon, '-', color=COLORS['qubit'],
               linewidth=2.5, label='Transmon')
    ax2.loglog(heights, n_optical, '-', color=COLORS['optical'],
               linewidth=2.5, label='Optical Clock')
    
    # Feasibility lines
    ax2.axhline(y=1e9, color='gray', linestyle='--', alpha=0.7, label='$10^9$ shots (~1 day)')
    ax2.axhline(y=1e12, color='gray', linestyle=':', alpha=0.7, label='$10^{12}$ shots (~3 years)')
    
    ax2.fill_between(heights, 1, 1e9, alpha=0.1, color=COLORS['optical'], label='Feasible region')
    
    ax2.set_xlabel('Height difference $\Delta h$ [m]', fontsize=12)
    ax2.set_ylabel('Required shots N for SNR=3', fontsize=12)
    ax2.set_title('(b) Averaging Requirements', fontsize=12)
    ax2.legend(loc='upper right', fontsize=9)
    ax2.set_xlim(1e-3, 100)
    ax2.set_ylim(1, 1e30)
    ax2.grid(True, which='both', alpha=0.3)
    
    plt.suptitle('Figure 1: Platform Comparison for SSZ Detection', fontsize=14, y=1.02)
    plt.tight_layout()
    
    filepath = os.path.join(OUTPUT_DIR, 'paper_c_final_fig1_platform.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {filepath}")
    return filepath


def fig2_chip_tilt_geometry():
    """Figure 2: Chip tilt geometry and Δh generation."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Left: Schematic of tilted chip
    ax1.set_xlim(-0.5, 2.5)
    ax1.set_ylim(-0.3, 1.2)
    
    # Chip at angle
    theta = 10  # degrees
    L = 2.0  # chip length (arbitrary units)
    
    # Reference (horizontal)
    ax1.plot([0, L], [0, 0], 'k--', alpha=0.3, linewidth=1)
    ax1.text(L/2, -0.1, 'Reference (horizontal)', ha='center', fontsize=10, alpha=0.5)
    
    # Tilted chip
    x_end = L * np.cos(np.radians(theta))
    y_end = L * np.sin(np.radians(theta))
    ax1.plot([0, x_end], [0, y_end], 'b-', linewidth=4, label='Tilted chip')
    ax1.fill([0, x_end, x_end, 0], [0, y_end, y_end-0.05, -0.05], 
             color=COLORS['ssz'], alpha=0.3)
    
    # Qubits
    ax1.scatter([0.1], [0.1*np.tan(np.radians(theta))], color='red', s=150, zorder=5)
    ax1.scatter([x_end-0.1], [y_end-0.1*np.tan(np.radians(theta))], color='red', s=150, zorder=5)
    ax1.text(0.1, 0.1*np.tan(np.radians(theta))+0.1, 'Qubit A\n(lower)', ha='center', fontsize=10)
    ax1.text(x_end-0.1, y_end+0.1, 'Qubit B\n(higher)', ha='center', fontsize=10)
    
    # Height difference arrow
    ax1.annotate('', xy=(x_end+0.1, y_end), xytext=(x_end+0.1, 0),
                arrowprops=dict(arrowstyle='<->', color='green', lw=2))
    ax1.text(x_end+0.2, y_end/2, f'$\Delta h = L \cdot \sin(\\theta)$\n= {L*np.sin(np.radians(theta))*10:.1f} mm\n(for L=20mm, $\\theta$={theta}°)', 
             fontsize=10, va='center')
    
    # Angle arc
    angle_arc = np.linspace(0, np.radians(theta), 20)
    arc_r = 0.5
    ax1.plot(arc_r*np.cos(angle_arc), arc_r*np.sin(angle_arc), 'k-', linewidth=1)
    ax1.text(0.55, 0.08, f'$\\theta$={theta}°', fontsize=11)
    
    ax1.set_aspect('equal')
    ax1.axis('off')
    ax1.set_title('(a) Chip Tilt Geometry', fontsize=12)
    
    # Right: Δh vs tilt angle
    angles = np.linspace(0, 15, 100)
    L_chip = 20  # mm
    dh = L_chip * np.sin(np.radians(angles))
    
    ax2.plot(angles, dh, '-', color=COLORS['ssz'], linewidth=2.5)
    
    # Key points
    key_angles = [1, 5, 10]
    for a in key_angles:
        dh_val = L_chip * np.sin(np.radians(a))
        ax2.scatter([a], [dh_val], color=COLORS['ssz'], s=80, zorder=5)
        ax2.annotate(f'{a}°: {dh_val:.2f} mm', xy=(a, dh_val), 
                    xytext=(a+1, dh_val+0.3), fontsize=10,
                    arrowprops=dict(arrowstyle='->', color='gray', lw=0.5))
    
    ax2.set_xlabel('Tilt angle $\\theta$ [degrees]', fontsize=12)
    ax2.set_ylabel('Height difference $\Delta h$ [mm]', fontsize=12)
    ax2.set_title('(b) $\Delta h$ vs Tilt Angle (L = 20 mm chip)', fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, 15)
    ax2.set_ylim(0, 6)
    
    plt.suptitle('Figure 2: Hardware Configuration - Chip Tilt', fontsize=14, y=1.02)
    plt.tight_layout()
    
    filepath = os.path.join(OUTPUT_DIR, 'paper_c_final_fig2_tilt.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {filepath}")
    return filepath


def fig3_statistical_framework():
    """Figure 3: Statistical framework - slope fitting and upper bound."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    np.random.seed(42)
    
    # Left: Simulated data with slope fit
    dh_points = np.array([0.35, 1.0, 1.74, 2.5, 3.47]) * 1e-3  # mm to m
    
    # SSZ predicted slope
    alpha_ssz = OMEGA_5GHZ * R_S_EARTH * 100e-6 / R_EARTH**2  # rad/m
    
    # Simulated measurements (null result - no signal, only noise)
    n_measurements = 1000
    noise_after_avg = 1.0 / np.sqrt(1e9)  # 10^9 averages
    
    measured_phi = np.zeros_like(dh_points)
    measured_err = np.ones_like(dh_points) * noise_after_avg
    
    # Add small random scatter
    measured_phi = np.random.normal(0, noise_after_avg, len(dh_points))
    
    ax1.errorbar(dh_points * 1e3, measured_phi, yerr=measured_err, 
                fmt='o', color=COLORS['ssz'], capsize=5, capthick=2,
                markersize=8, label='Measured (simulated null)')
    
    # Fit line
    from numpy.polynomial import polynomial as P
    coeffs = np.polyfit(dh_points, measured_phi, 1)
    fit_line = np.polyval(coeffs, dh_points)
    ax1.plot(dh_points * 1e3, fit_line, '--', color=COLORS['threshold'], 
             linewidth=2, label=f'Linear fit: slope = {coeffs[0]:.2e} rad/m')
    
    # SSZ prediction (too small to see)
    ssz_line = alpha_ssz * dh_points
    ax1.plot(dh_points * 1e3, ssz_line, ':', color=COLORS['optical'],
             linewidth=2, label=f'SSZ prediction: slope = {alpha_ssz:.2e} rad/m')
    
    ax1.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
    ax1.set_xlabel('Height difference $\Delta h$ [mm]', fontsize=12)
    ax1.set_ylabel('Measured phase shift $\Delta\Phi$ [rad]', fontsize=12)
    ax1.set_title('(a) Slope Fitting (Simulated Null Result)', fontsize=12)
    ax1.legend(loc='upper left', fontsize=9)
    ax1.grid(True, alpha=0.3)
    
    # Right: Upper bound visualization
    sigma_slope = noise_after_avg / (3.47e-3)  # uncertainty in slope
    
    slopes = np.linspace(-3*sigma_slope, 3*sigma_slope, 1000)
    likelihood = np.exp(-0.5 * (slopes / sigma_slope)**2)
    
    ax2.fill_between(slopes, 0, likelihood, alpha=0.3, color=COLORS['ssz'])
    ax2.plot(slopes, likelihood, '-', color=COLORS['ssz'], linewidth=2)
    
    # 95% confidence interval
    ci_95 = 1.96 * sigma_slope
    ax2.axvline(x=-ci_95, color=COLORS['threshold'], linestyle='--', linewidth=2)
    ax2.axvline(x=ci_95, color=COLORS['threshold'], linestyle='--', linewidth=2,
               label=f'95% CL: |$\\alpha$| < {ci_95:.2e} rad/m')
    ax2.fill_between(slopes, 0, likelihood, where=(np.abs(slopes) <= ci_95),
                    alpha=0.3, color=COLORS['optical'])
    
    # SSZ prediction (mark it)
    ax2.axvline(x=alpha_ssz, color=COLORS['optical'], linestyle=':', linewidth=2,
               label=f'SSZ prediction: {alpha_ssz:.2e} rad/m')
    
    ax2.set_xlabel('Slope $\\alpha$ [rad/m]', fontsize=12)
    ax2.set_ylabel('Likelihood', fontsize=12)
    ax2.set_title('(b) Upper Bound Determination', fontsize=12)
    ax2.legend(loc='upper right', fontsize=9)
    ax2.set_xlim(-3*sigma_slope, 3*sigma_slope)
    ax2.grid(True, alpha=0.3)
    
    # Add text box with upper bound
    textstr = f'Upper Bound:\n|$\\alpha_{{anom}}$| < {ci_95:.1e} rad/m\n(95% CL)\n\nSSZ predicted:\n$\\alpha_{{SSZ}}$ = {alpha_ssz:.1e} rad/m\n\nRatio: < {ci_95/alpha_ssz:.0e}'
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
    ax2.text(0.02, 0.98, textstr, transform=ax2.transAxes, fontsize=9,
            verticalalignment='top', bbox=props)
    
    plt.suptitle('Figure 3: Statistical Framework for Upper Bound', fontsize=14, y=1.02)
    plt.tight_layout()
    
    filepath = os.path.join(OUTPUT_DIR, 'paper_c_final_fig3_statistics.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {filepath}")
    return filepath


def fig4_confound_signatures():
    """Figure 4: Confound discrimination by scaling signatures."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # (a) Δh scaling
    ax1 = axes[0, 0]
    dh = np.linspace(0, 5, 50)
    
    ssz_signal = dh  # Linear
    temp_signal = 0.5 + 0.3 * np.sin(dh * 2)  # Oscillatory
    
    ax1.plot(dh, ssz_signal / ssz_signal[-1], '-', color=COLORS['ssz'], 
             linewidth=2.5, label='SSZ: Linear')
    ax1.plot(dh, temp_signal / temp_signal.max(), '--', color=COLORS['threshold'],
             linewidth=2.5, label='Temperature: Non-monotonic')
    ax1.set_xlabel('$\Delta h$ [mm]', fontsize=11)
    ax1.set_ylabel('Normalized signal', fontsize=11)
    ax1.set_title('(a) $\Delta h$ Scaling', fontsize=12)
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)
    
    # (b) ω scaling
    ax2 = axes[0, 1]
    omega = np.linspace(1, 10, 50)
    
    ssz_omega = omega  # Linear
    temp_omega = np.ones_like(omega)  # Independent
    
    ax2.plot(omega, ssz_omega / ssz_omega[-1], '-', color=COLORS['ssz'],
             linewidth=2.5, label='SSZ: Linear')
    ax2.plot(omega, temp_omega, '--', color=COLORS['threshold'],
             linewidth=2.5, label='Confounds: Independent')
    ax2.set_xlabel('Frequency $\\omega$ [GHz]', fontsize=11)
    ax2.set_ylabel('Normalized signal', fontsize=11)
    ax2.set_title('(b) $\\omega$ Scaling', fontsize=12)
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)
    
    # (c) t scaling
    ax3 = axes[1, 0]
    t = np.linspace(0, 100, 50)
    
    ssz_t = t  # Linear
    noise_t = np.sqrt(t)  # sqrt(t)
    
    ax3.plot(t, ssz_t / ssz_t[-1], '-', color=COLORS['ssz'],
             linewidth=2.5, label='SSZ: Linear')
    ax3.plot(t, noise_t / noise_t[-1], '--', color=COLORS['threshold'],
             linewidth=2.5, label='LO noise: $\\sqrt{t}$')
    ax3.set_xlabel('Time $t$ [$\\mu$s]', fontsize=11)
    ax3.set_ylabel('Normalized signal', fontsize=11)
    ax3.set_title('(c) $t$ Scaling', fontsize=12)
    ax3.legend(fontsize=9)
    ax3.grid(True, alpha=0.3)
    
    # (d) Randomization response
    ax4 = axes[1, 1]
    
    runs = np.arange(1, 11)
    np.random.seed(123)
    
    ssz_runs = np.ones(10) * 0.8  # Constant (deterministic)
    temp_runs = 0.5 + 0.4 * np.random.randn(10)  # Variable
    
    ax4.plot(runs, ssz_runs, 'o-', color=COLORS['ssz'], 
             linewidth=2, markersize=8, label='SSZ: Invariant')
    ax4.plot(runs, temp_runs, 's--', color=COLORS['threshold'],
             linewidth=2, markersize=8, label='Confounds: Variable')
    ax4.set_xlabel('Run number', fontsize=11)
    ax4.set_ylabel('Normalized signal', fontsize=11)
    ax4.set_title('(d) Randomization Response', fontsize=12)
    ax4.legend(fontsize=9)
    ax4.grid(True, alpha=0.3)
    ax4.set_xlim(0.5, 10.5)
    
    plt.suptitle('Figure 4: Confound Discrimination by Scaling Signatures', fontsize=14, y=1.02)
    plt.tight_layout()
    
    filepath = os.path.join(OUTPUT_DIR, 'paper_c_final_fig4_confounds.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {filepath}")
    return filepath


def fig5_mathematical_derivation():
    """Figure 5: Mathematical derivation visualization."""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # (a) Time dilation D_SSZ vs r
    ax1 = axes[0]
    r_over_rs = np.logspace(-0.5, 4, 1000)
    
    # SSZ weak field
    xi_weak = 1 / (2 * r_over_rs)
    d_ssz_weak = 1 / (1 + xi_weak)
    
    # GR Schwarzschild
    d_gr = np.sqrt(1 - 1/r_over_rs)
    d_gr[r_over_rs < 1] = 0
    
    ax1.semilogx(r_over_rs, d_ssz_weak, '-', color=COLORS['ssz'],
                 linewidth=2.5, label='SSZ: $D = 1/(1+\\Xi)$')
    ax1.semilogx(r_over_rs, d_gr, '--', color=COLORS['threshold'],
                 linewidth=2.5, label='GR: $D = \\sqrt{1-r_s/r}$')
    
    ax1.axvline(x=1, color='gray', linestyle=':', alpha=0.7)
    ax1.text(1.1, 0.1, '$r = r_s$', fontsize=10)
    
    ax1.axvline(x=R_EARTH/R_S_EARTH, color='gray', linestyle=':', alpha=0.7)
    ax1.text(R_EARTH/R_S_EARTH * 1.2, 0.5, 'Earth surface', fontsize=10, rotation=90)
    
    ax1.set_xlabel('$r / r_s$', fontsize=12)
    ax1.set_ylabel('Time dilation factor $D$', fontsize=12)
    ax1.set_title('(a) Time Dilation $D(r)$', fontsize=12)
    ax1.legend(fontsize=9)
    ax1.set_xlim(0.5, 1e4)
    ax1.set_ylim(0, 1.05)
    ax1.grid(True, alpha=0.3)
    
    # (b) ΔD vs Δh (linearized)
    ax2 = axes[1]
    dh = np.logspace(-6, 2, 100)
    
    dd = R_S_EARTH * dh / R_EARTH**2
    
    ax2.loglog(dh, dd, '-', color=COLORS['ssz'], linewidth=2.5)
    
    # Key points
    key_dh = [1e-3, 1, 100]
    for d in key_dh:
        dd_val = R_S_EARTH * d / R_EARTH**2
        ax2.scatter([d], [dd_val], color=COLORS['ssz'], s=80, zorder=5)
    
    ax2.set_xlabel('Height difference $\Delta h$ [m]', fontsize=12)
    ax2.set_ylabel('$\Delta D_{SSZ}$', fontsize=12)
    ax2.set_title('(b) Differential: $\Delta D \\approx r_s \\Delta h / R^2$', fontsize=12)
    ax2.grid(True, which='both', alpha=0.3)
    
    # Add formula
    ax2.text(0.05, 0.95, '$\\Delta D_{SSZ} = \\frac{r_s \\cdot \\Delta h}{R^2}$\n\n'
             f'$r_s$ = {R_S_EARTH:.2e} m\n$R$ = {R_EARTH:.2e} m',
             transform=ax2.transAxes, fontsize=10, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # (c) Phase drift ΔΦ formula breakdown
    ax3 = axes[2]
    
    # Create a text-based visualization of the formula
    ax3.axis('off')
    
    formula_text = (
        "PHASE DRIFT FORMULA\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        r"$\Delta\Phi = \omega \times \Delta D_{SSZ} \times t$" + "\n\n"
        "where:\n"
        r"  $\omega = 2\pi f$  (angular frequency)" + "\n"
        r"  $\Delta D_{SSZ} = r_s \cdot \Delta h / R^2$" + "\n"
        r"  $t$  (integration time)" + "\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "EXAMPLE (5 GHz, 1 mm, 100 μs):\n\n"
        r"$\Delta\Phi = 3.14 \times 10^{10} \times 1.09 \times 10^{-19} \times 10^{-4}$" + "\n\n"
        r"$\Delta\Phi = 3.43 \times 10^{-13}$ rad"
    )
    
    ax3.text(0.5, 0.5, formula_text, transform=ax3.transAxes,
             fontsize=12, verticalalignment='center', horizontalalignment='center',
             family='serif')
    ax3.set_title('(c) Phase Drift Formula', fontsize=12)
    
    plt.suptitle('Figure 5: Mathematical Derivation', fontsize=14, y=1.02)
    plt.tight_layout()
    
    filepath = os.path.join(OUTPUT_DIR, 'paper_c_final_fig5_derivation.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {filepath}")
    return filepath


def fig6_feasibility_summary():
    """Figure 6: Feasibility summary matrix."""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Data
    setups = ['On-chip\n(no tilt)', 'Chip tilt\n(5°)', '3D Stack\n(2mm)', 
              'Remote\n(1m)', 'Remote\n(10m)', 'Optical\nClock (1m)']
    dh = [0, 1.74, 2, 1000, 10000, 1000]  # mm
    signal = [0, 5.98e-13, 6.87e-13, 3.43e-10, 3.43e-9, 0.29]  # rad
    n_shots = [np.inf, 2.8e25, 2.1e25, 7.6e19, 7.6e17, 100]
    feasible = ['No', 'No', 'No', 'No', 'Marginal', 'YES']
    colors_bar = ['#DC3545', '#DC3545', '#DC3545', '#DC3545', '#FFC107', '#28A745']
    
    x = np.arange(len(setups))
    
    # Plot signal strength (log scale)
    bars = ax.bar(x, [max(s, 1e-15) for s in signal], color=colors_bar, alpha=0.8, edgecolor='black')
    
    ax.set_yscale('log')
    ax.set_ylabel('Phase Signal $|\Delta\Phi|$ [rad]', fontsize=12)
    ax.set_xlabel('Experimental Setup', fontsize=12)
    ax.set_title('Figure 6: Feasibility Summary - Signal Strength by Setup', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(setups, fontsize=10)
    
    # Detection threshold
    ax.axhline(y=1, color='red', linestyle='--', linewidth=2, label='Single-shot noise (~1 rad)')
    ax.axhline(y=1e-5, color='orange', linestyle=':', linewidth=2, label='After $10^{10}$ averages')
    
    # Add feasibility labels
    for i, (bar, feas, n) in enumerate(zip(bars, feasible, n_shots)):
        height = bar.get_height()
        if n < np.inf:
            if n > 1e20:
                n_str = f'N~10$^{{{int(np.log10(n))}}}$'
            else:
                n_str = f'N~{n:.0e}'
        else:
            n_str = 'N=∞'
        ax.text(bar.get_x() + bar.get_width()/2., height * 2, 
                f'{feas}\n{n_str}', ha='center', va='bottom', fontsize=9,
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    ax.set_ylim(1e-15, 10)
    ax.legend(loc='lower right', fontsize=10)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    
    filepath = os.path.join(OUTPUT_DIR, 'paper_c_final_fig6_feasibility.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {filepath}")
    return filepath


def main():
    print("="*70)
    print("Generating Final Paper C Plots (v1.2 Bulletproof)")
    print("="*70)
    
    filepaths = []
    
    print("\nFigure 1: Platform Comparison...")
    filepaths.append(fig1_platform_comparison())
    
    print("\nFigure 2: Chip Tilt Geometry...")
    filepaths.append(fig2_chip_tilt_geometry())
    
    print("\nFigure 3: Statistical Framework...")
    filepaths.append(fig3_statistical_framework())
    
    print("\nFigure 4: Confound Signatures...")
    filepaths.append(fig4_confound_signatures())
    
    print("\nFigure 5: Mathematical Derivation...")
    filepaths.append(fig5_mathematical_derivation())
    
    print("\nFigure 6: Feasibility Summary...")
    filepaths.append(fig6_feasibility_summary())
    
    print("\n" + "="*70)
    print(f"All 6 figures saved to: {OUTPUT_DIR}")
    print("="*70)
    
    return filepaths


if __name__ == "__main__":
    main()
