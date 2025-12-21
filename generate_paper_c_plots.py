#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Publication-Quality Plots for Paper C

Figures:
1. Phase drift vs height difference (log-log)
2. Segment-coherent zone width vs tolerance
3. Compensation efficiency (with/without)
4. Falsification experiment expected results

(c) 2025 Carmen Wrede, Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""

import os
import sys

# UTF-8 for Windows
if sys.platform.startswith('win'):
    os.environ['PYTHONIOENCODING'] = 'utf-8'

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator, LogFormatterMathtext
import matplotlib.patches as mpatches

from ssz_qubits import (
    M_EARTH, R_EARTH, schwarzschild_radius,
    ssz_time_dilation_difference, segment_coherent_zone
)

# Constants
OMEGA_5GHZ = 2 * np.pi * 5e9
OMEGA_7GHZ = 2 * np.pi * 7e9
GATE_TIME = 50e-9
R_S_EARTH = schwarzschild_radius(M_EARTH)

# Output directory
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'outputs')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Style settings
plt.style.use('seaborn-v0_8-whitegrid')
COLORS = {
    'ssz': '#2E86AB',      # Blue
    'baseline': '#A23B72', # Magenta
    'compensated': '#28A745', # Green
    'threshold': '#DC3545',   # Red
    'zone': '#FFC107'      # Yellow
}


def fig1_phase_vs_height():
    """Figure 1: Phase drift rate vs height difference."""
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Data
    heights = np.logspace(-6, 1, 100)  # 1 um to 10 m
    phase_drifts = []
    
    for h in heights:
        delta_d = abs(ssz_time_dilation_difference(R_EARTH + h, R_EARTH, M_EARTH))
        delta_phi = OMEGA_5GHZ * delta_d * 1e-6  # per us
        phase_drifts.append(delta_phi)
    
    # Main line
    ax.loglog(heights * 1e3, phase_drifts, color=COLORS['ssz'], 
              linewidth=2.5, label='SSZ prediction')
    
    # Highlight key points
    key_heights = [1e-3, 1e-2, 0.1, 1.0]  # 1mm, 1cm, 10cm, 1m
    for h in key_heights:
        delta_d = abs(ssz_time_dilation_difference(R_EARTH + h, R_EARTH, M_EARTH))
        delta_phi = OMEGA_5GHZ * delta_d * 1e-6
        ax.scatter([h * 1e3], [delta_phi], color=COLORS['ssz'], s=80, zorder=5)
        
        # Annotation
        if h == 1e-3:
            ax.annotate(f'1 mm\n{delta_phi:.2e} rad/us', 
                       xy=(h * 1e3, delta_phi), xytext=(h * 1e3 * 3, delta_phi * 3),
                       fontsize=9, ha='left',
                       arrowprops=dict(arrowstyle='->', color='gray', lw=0.5))
    
    # Falsification threshold (50% of predicted)
    threshold_phases = [p * 0.5 for p in phase_drifts]
    ax.loglog(heights * 1e3, threshold_phases, '--', color=COLORS['threshold'],
              linewidth=1.5, alpha=0.7, label='Falsification threshold (50%)')
    
    # Fill region below threshold
    ax.fill_between(heights * 1e3, 1e-25, threshold_phases, 
                    color=COLORS['threshold'], alpha=0.1, label='SSZ falsified region')
    
    ax.set_xlabel('Height difference $\\Delta h$ [mm]', fontsize=12)
    ax.set_ylabel('Phase drift rate $\\Delta\\Phi/t$ [rad/$\\mu$s]', fontsize=12)
    ax.set_title('Figure 1: SSZ Phase Drift vs Height Difference\n(5 GHz qubit)', fontsize=14)
    ax.legend(loc='lower right', fontsize=10)
    ax.set_xlim(1e-3, 1e4)
    ax.set_ylim(1e-20, 1e-10)
    ax.grid(True, which='both', alpha=0.3)
    
    # Add slope indicator
    ax.text(0.05, 0.95, 'Slope = 1\n(linear scaling)', transform=ax.transAxes,
            fontsize=10, verticalalignment='top', 
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    filepath = os.path.join(OUTPUT_DIR, 'paper_c_fig1_phase_vs_height.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {filepath}")
    return filepath


def fig2_coherent_zones():
    """Figure 2: Segment-coherent zone width vs tolerance."""
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Data
    epsilons = np.logspace(-22, -14, 100)
    zone_widths = []
    
    for eps in epsilons:
        z = 4 * eps * R_EARTH**2 / R_S_EARTH
        zone_widths.append(z)
    
    # Main line
    ax.loglog(epsilons, np.array(zone_widths) * 1e3, color=COLORS['zone'],
              linewidth=2.5, label='$z(\\varepsilon) = 4\\varepsilon R^2 / r_s$')
    
    # Key tolerance levels
    key_eps = [1e-16, 1e-18, 1e-20]
    labels = ['Current QEC', 'Near-term', 'Future']
    
    for eps, lbl in zip(key_eps, labels):
        z = 4 * eps * R_EARTH**2 / R_S_EARTH
        ax.scatter([eps], [z * 1e3], color=COLORS['ssz'], s=100, zorder=5)
        
        # Format zone width
        if z >= 1:
            z_str = f'{z:.1f} m'
        elif z >= 1e-3:
            z_str = f'{z*1e3:.1f} mm'
        else:
            z_str = f'{z*1e6:.0f} um'
        
        ax.annotate(f'{lbl}\n$\\varepsilon$={eps:.0e}\nz={z_str}',
                   xy=(eps, z * 1e3), xytext=(eps * 5, z * 1e3 * 2),
                   fontsize=9, ha='left',
                   arrowprops=dict(arrowstyle='->', color='gray', lw=0.5))
    
    # Typical chip scale reference
    ax.axhline(y=10, color='gray', linestyle=':', alpha=0.7, label='Typical chip scale (10 mm)')
    
    ax.set_xlabel('Tolerance $\\varepsilon$', fontsize=12)
    ax.set_ylabel('Zone width $z$ [mm]', fontsize=12)
    ax.set_title('Figure 2: Segment-Coherent Zone Width\nvs Timing Tolerance', fontsize=14)
    ax.legend(loc='upper left', fontsize=10)
    ax.set_xlim(1e-22, 1e-14)
    ax.set_ylim(1e-3, 1e6)
    ax.grid(True, which='both', alpha=0.3)
    
    plt.tight_layout()
    filepath = os.path.join(OUTPUT_DIR, 'paper_c_fig2_coherent_zones.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {filepath}")
    return filepath


def fig3_compensation():
    """Figure 3: Fidelity with/without SSZ compensation."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Left panel: Fidelity vs number of gates
    n_gates = np.logspace(0, 8, 100)
    delta_h = 0.001  # 1 mm
    delta_d = abs(ssz_time_dilation_difference(R_EARTH + delta_h, R_EARTH, M_EARTH))
    phase_per_gate = OMEGA_5GHZ * delta_d * GATE_TIME
    
    fidelity_baseline = np.ones_like(n_gates)
    fidelity_no_comp = np.cos(phase_per_gate * n_gates / 2)**2
    fidelity_with_comp = np.cos(phase_per_gate * n_gates * 0.01 / 2)**2  # 99% compensation
    
    ax1.semilogx(n_gates, fidelity_baseline, '-', color=COLORS['baseline'],
                linewidth=2, label='Baseline (no SSZ)')
    ax1.semilogx(n_gates, fidelity_no_comp, '-', color=COLORS['threshold'],
                linewidth=2, label='SSZ drift (no compensation)')
    ax1.semilogx(n_gates, fidelity_with_comp, '-', color=COLORS['compensated'],
                linewidth=2, label='SSZ + 99% compensation')
    
    ax1.set_xlabel('Number of gates', fontsize=12)
    ax1.set_ylabel('Bell state fidelity', fontsize=12)
    ax1.set_title('(a) Fidelity vs Gate Count ($\\Delta h$ = 1 mm)', fontsize=12)
    ax1.legend(loc='lower left', fontsize=10)
    ax1.set_xlim(1, 1e8)
    ax1.set_ylim(0.9, 1.01)
    ax1.grid(True, alpha=0.3)
    
    # Right panel: Compensation efficiency vs height
    heights = np.logspace(-4, 0, 50)  # 0.1 mm to 1 m
    
    phase_no_comp = []
    phase_with_comp = []
    
    for h in heights:
        delta_d = abs(ssz_time_dilation_difference(R_EARTH + h, R_EARTH, M_EARTH))
        phi = OMEGA_5GHZ * delta_d * 1e-6  # per us
        phase_no_comp.append(phi)
        phase_with_comp.append(phi * 0.01)  # 99% compensation
    
    ax2.loglog(heights * 1e3, phase_no_comp, '-', color=COLORS['threshold'],
              linewidth=2, label='Without compensation')
    ax2.loglog(heights * 1e3, phase_with_comp, '-', color=COLORS['compensated'],
              linewidth=2, label='With 99% compensation')
    
    # Show 99% reduction arrow
    h_demo = 0.01  # 10 mm
    delta_d = abs(ssz_time_dilation_difference(R_EARTH + h_demo, R_EARTH, M_EARTH))
    phi_no = OMEGA_5GHZ * delta_d * 1e-6
    phi_with = phi_no * 0.01
    
    ax2.annotate('', xy=(h_demo * 1e3, phi_with), xytext=(h_demo * 1e3, phi_no),
                arrowprops=dict(arrowstyle='<->', color='black', lw=1.5))
    ax2.text(h_demo * 1e3 * 1.5, np.sqrt(phi_no * phi_with), '99%\nreduction',
            fontsize=10, va='center')
    
    ax2.set_xlabel('Height difference $\\Delta h$ [mm]', fontsize=12)
    ax2.set_ylabel('Phase drift $\\Delta\\Phi$ [rad/$\\mu$s]', fontsize=12)
    ax2.set_title('(b) Phase Drift With/Without Compensation', fontsize=12)
    ax2.legend(loc='lower right', fontsize=10)
    ax2.grid(True, which='both', alpha=0.3)
    
    plt.suptitle('Figure 3: SSZ Compensation Efficiency', fontsize=14, y=1.02)
    plt.tight_layout()
    filepath = os.path.join(OUTPUT_DIR, 'paper_c_fig3_compensation.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {filepath}")
    return filepath


def fig4_falsification_experiment():
    """Figure 4: Expected results from falsification experiment."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # (a) Phase drift vs height - linear scale
    ax1 = axes[0, 0]
    heights = np.linspace(0.1, 10, 50) * 1e-3  # 0.1 mm to 10 mm
    
    for t_us, style, label in [(1, '-', '1 us'), (10, '--', '10 us'), (100, ':', '100 us')]:
        phases = []
        for h in heights:
            delta_d = abs(ssz_time_dilation_difference(R_EARTH + h, R_EARTH, M_EARTH))
            phi = OMEGA_5GHZ * delta_d * t_us * 1e-6
            phases.append(phi)
        ax1.plot(heights * 1e3, phases, style, linewidth=2, label=f't = {label}')
    
    ax1.set_xlabel('Height difference $\\Delta h$ [mm]', fontsize=11)
    ax1.set_ylabel('Phase drift $\\Delta\\Phi$ [rad]', fontsize=11)
    ax1.set_title('(a) Phase Drift vs Height\n(Expected linear relationship)', fontsize=11)
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)
    
    # (b) Frequency scaling test
    ax2 = axes[0, 1]
    delta_h = 0.001  # 1 mm
    freqs = np.linspace(3, 10, 50) * 1e9  # 3 to 10 GHz
    delta_d = abs(ssz_time_dilation_difference(R_EARTH + delta_h, R_EARTH, M_EARTH))
    
    phases_5ghz = 2 * np.pi * 5e9 * delta_d * 1e-6
    phases = [2 * np.pi * f * delta_d * 1e-6 for f in freqs]
    ratios = [p / phases_5ghz for p in phases]
    expected_ratios = [f / 5e9 for f in freqs]
    
    ax2.plot(freqs / 1e9, ratios, '-', color=COLORS['ssz'], linewidth=2, label='SSZ prediction')
    ax2.plot(freqs / 1e9, expected_ratios, '--', color='gray', linewidth=1.5, label='$\\omega/\\omega_{5GHz}$ (expected)')
    
    # Highlight 5 GHz and 7 GHz
    ax2.scatter([5], [1.0], color=COLORS['ssz'], s=100, zorder=5)
    ax2.scatter([7], [1.4], color=COLORS['ssz'], s=100, zorder=5)
    ax2.annotate('5 GHz\n(reference)', xy=(5, 1.0), xytext=(5.5, 0.85),
                fontsize=9, arrowprops=dict(arrowstyle='->', color='gray', lw=0.5))
    ax2.annotate('7 GHz\nratio = 1.40', xy=(7, 1.4), xytext=(7.5, 1.55),
                fontsize=9, arrowprops=dict(arrowstyle='->', color='gray', lw=0.5))
    
    # Falsification threshold
    ax2.axhline(y=1.2, color=COLORS['threshold'], linestyle=':', 
               label='Falsification threshold (1.2)')
    
    ax2.set_xlabel('Qubit frequency [GHz]', fontsize=11)
    ax2.set_ylabel('Phase ratio $\\Delta\\Phi(\\omega)/\\Delta\\Phi(5 GHz)$', fontsize=11)
    ax2.set_title('(b) Frequency Scaling Test\n(Expected linear in $\\omega$)', fontsize=11)
    ax2.legend(fontsize=9, loc='upper left')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(3, 10)
    ax2.set_ylim(0.5, 2.2)
    
    # (c) With/without compensation differential
    ax3 = axes[1, 0]
    heights = np.linspace(0.1, 10, 20) * 1e-3
    t = 10e-6  # 10 us
    
    phases_no = []
    phases_with = []
    
    for h in heights:
        delta_d = abs(ssz_time_dilation_difference(R_EARTH + h, R_EARTH, M_EARTH))
        phi = OMEGA_5GHZ * delta_d * t
        phases_no.append(phi)
        phases_with.append(phi * 0.01)
    
    x = np.arange(len(heights))
    width = 0.35
    
    bars1 = ax3.bar(x - width/2, phases_no, width, label='Without compensation',
                   color=COLORS['threshold'], alpha=0.8)
    bars2 = ax3.bar(x + width/2, phases_with, width, label='With compensation',
                   color=COLORS['compensated'], alpha=0.8)
    
    ax3.set_xlabel('Height difference $\\Delta h$ [mm]', fontsize=11)
    ax3.set_ylabel('Phase drift $\\Delta\\Phi$ [rad]', fontsize=11)
    ax3.set_title('(c) Compensation Differential Test\n(Key discriminator)', fontsize=11)
    ax3.set_xticks(x[::4])
    ax3.set_xticklabels([f'{h*1e3:.1f}' for h in heights[::4]])
    ax3.legend(fontsize=9)
    ax3.set_yscale('log')
    ax3.grid(True, alpha=0.3, axis='y')
    
    # (d) Reproducibility test
    ax4 = axes[1, 1]
    np.random.seed(42)
    
    # Simulate 10 runs at each height
    heights_test = [0.5, 1.0, 2.0, 5.0]  # mm
    n_runs = 10
    
    for i, h in enumerate(heights_test):
        delta_d = abs(ssz_time_dilation_difference(R_EARTH + h * 1e-3, R_EARTH, M_EARTH))
        phi_true = OMEGA_5GHZ * delta_d * 10e-6
        
        # SSZ is deterministic - all runs identical
        ssz_runs = np.ones(n_runs) * phi_true
        
        # Add small measurement noise (not SSZ noise)
        noise = np.random.normal(0, phi_true * 0.05, n_runs)
        measured_runs = ssz_runs + noise
        
        ax4.scatter(np.ones(n_runs) * (i + 1) + np.random.uniform(-0.1, 0.1, n_runs),
                   measured_runs, alpha=0.6, color=COLORS['ssz'], s=30)
        ax4.hlines(phi_true, i + 0.7, i + 1.3, colors=COLORS['threshold'], 
                  linestyles='-', linewidth=2, label='SSZ prediction' if i == 0 else '')
    
    ax4.set_xlabel('Height point', fontsize=11)
    ax4.set_ylabel('Measured phase drift [rad]', fontsize=11)
    ax4.set_title('(d) Reproducibility Test\n(10 runs per height)', fontsize=11)
    ax4.set_xticks([1, 2, 3, 4])
    ax4.set_xticklabels(['0.5 mm', '1.0 mm', '2.0 mm', '5.0 mm'])
    ax4.legend(['SSZ prediction', 'Measurements'], fontsize=9)
    ax4.grid(True, alpha=0.3, axis='y')
    
    plt.suptitle('Figure 4: Expected Results from Falsification Experiment', fontsize=14, y=1.02)
    plt.tight_layout()
    filepath = os.path.join(OUTPUT_DIR, 'paper_c_fig4_falsification.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {filepath}")
    return filepath


def fig5_confound_discrimination():
    """Figure 5: Confound discrimination summary."""
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Create comparison table as visual
    properties = [
        'Deterministic',
        'Monotonic in $\\Delta h$',
        'Scales with $\\omega$',
        'Compensable',
        'Reproducible'
    ]
    
    confounds = ['SSZ', 'Temperature', 'LO Noise', 'Vibration', 'EM/Crosstalk']
    
    # SSZ: all yes
    # Temperature: no, no, no, no, yes
    # LO Noise: no, no, no, no, no
    # Vibration: no, no, no, no, yes
    # EM/Crosstalk: no, no, no, no, yes
    
    data = np.array([
        [1, 0, 0, 0, 0],  # Deterministic
        [1, 0, 0, 0, 0],  # Monotonic in dh
        [1, 0, 0, 0, 0],  # Scales with omega
        [1, 0, 0, 0, 0],  # Compensable
        [1, 1, 0, 1, 1],  # Reproducible
    ])
    
    # Create heatmap
    cmap = plt.cm.RdYlGn
    im = ax.imshow(data, cmap=cmap, aspect='auto', vmin=0, vmax=1)
    
    # Set ticks
    ax.set_xticks(np.arange(len(confounds)))
    ax.set_yticks(np.arange(len(properties)))
    ax.set_xticklabels(confounds, fontsize=11)
    ax.set_yticklabels(properties, fontsize=11)
    
    # Rotate x labels
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right', rotation_mode='anchor')
    
    # Add text annotations
    for i in range(len(properties)):
        for j in range(len(confounds)):
            text = 'Yes' if data[i, j] == 1 else 'No'
            color = 'white' if data[i, j] == 1 else 'black'
            ax.text(j, i, text, ha='center', va='center', color=color, fontsize=10, fontweight='bold')
    
    ax.set_title('Figure 5: Confound Discrimination Matrix\n(SSZ vs Common Error Sources)', fontsize=14)
    
    # Add colorbar
    cbar = ax.figure.colorbar(im, ax=ax, shrink=0.6)
    cbar.ax.set_ylabel('Passes test', rotation=-90, va='bottom', fontsize=11)
    
    # Add note
    ax.text(0.5, -0.15, 'Key Discriminator: Only SSZ passes ALL five tests',
           transform=ax.transAxes, ha='center', fontsize=11, style='italic',
           bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))
    
    plt.tight_layout()
    filepath = os.path.join(OUTPUT_DIR, 'paper_c_fig5_confounds.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {filepath}")
    return filepath


def main():
    """Generate all Paper C figures."""
    print("="*60)
    print("Generating Paper C Figures")
    print("="*60)
    
    filepaths = []
    
    print("\nFigure 1: Phase drift vs height...")
    filepaths.append(fig1_phase_vs_height())
    
    print("\nFigure 2: Coherent zones...")
    filepaths.append(fig2_coherent_zones())
    
    print("\nFigure 3: Compensation efficiency...")
    filepaths.append(fig3_compensation())
    
    print("\nFigure 4: Falsification experiment...")
    filepaths.append(fig4_falsification_experiment())
    
    print("\nFigure 5: Confound discrimination...")
    filepaths.append(fig5_confound_discrimination())
    
    print("\n" + "="*60)
    print("All figures saved to:", OUTPUT_DIR)
    print("="*60)
    
    return filepaths


if __name__ == "__main__":
    main()
