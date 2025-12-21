#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Master Paper D Plots - Complete Figure Pack

6 Required Figures:
1. Concept sketch: local vs global comparison
2. ΔΦ vs Δh (log-log) + slope=1 reference
3. ΔΦ scaling with ω and t
4. Feasibility plot: Transmon vs Optical clocks
5. Upper-bound protocol diagram (tilt/stack/remote)
6. Confound signature matrix

(c) 2025 Carmen Wrede, Lino Casu
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Arrow, Circle, Rectangle
from matplotlib.lines import Line2D
import matplotlib.patches as mpatches

if sys.platform.startswith('win'):
    os.environ['PYTHONIOENCODING'] = 'utf-8'

from ssz_qubits import (
    M_EARTH, R_EARTH, schwarzschild_radius,
    ssz_time_dilation_difference
)

R_S_EARTH = schwarzschild_radius(M_EARTH)
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'outputs')
os.makedirs(OUTPUT_DIR, exist_ok=True)

plt.style.use('seaborn-v0_8-whitegrid')
COLORS = {
    'ssz': '#2E86AB',
    'gr': '#A23B72',
    'optical': '#28A745',
    'transmon': '#FFC107',
    'threshold': '#DC3545',
    'zone': '#F18F01',
    'dark': '#1B1B1E'
}


def fig1_local_vs_global():
    """Figure 1: Concept sketch - Local vs Global Phase Comparison."""
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 9)
    ax.axis('off')
    
    # Title
    ax.text(6, 8.5, 'Local vs Global Phase Comparison', fontsize=16, 
            ha='center', fontweight='bold')
    
    # LEFT SIDE: Local Frame
    ax.add_patch(FancyBboxPatch((0.5, 3), 4.5, 4.5, boxstyle="round,pad=0.1",
                                facecolor='#E8F4F8', edgecolor=COLORS['ssz'], lw=2))
    ax.text(2.75, 7.2, 'LOCAL FRAME', fontsize=12, ha='center', fontweight='bold')
    ax.text(2.75, 6.6, "(Observer's rest frame)", fontsize=9, ha='center', style='italic')
    
    # Single clock in local frame
    ax.add_patch(Circle((2.75, 5), 0.8, facecolor='white', edgecolor=COLORS['dark'], lw=2))
    ax.text(2.75, 5, 't', fontsize=14, ha='center', va='center')
    ax.text(2.75, 3.8, 'Proper time t = t\'', fontsize=10, ha='center')
    ax.text(2.75, 3.3, '(always!)', fontsize=9, ha='center', style='italic', color='gray')
    
    # RIGHT SIDE: Global Comparison
    ax.add_patch(FancyBboxPatch((6, 3), 5.5, 4.5, boxstyle="round,pad=0.1",
                                facecolor='#FFF3E0', edgecolor=COLORS['zone'], lw=2))
    ax.text(8.75, 7.2, 'GLOBAL COMPARISON', fontsize=12, ha='center', fontweight='bold')
    ax.text(8.75, 6.6, "(Two separated systems)", fontsize=9, ha='center', style='italic')
    
    # Two clocks at different heights
    ax.add_patch(Circle((7.5, 5.5), 0.6, facecolor='white', edgecolor=COLORS['ssz'], lw=2))
    ax.text(7.5, 5.5, r'$t_1$', fontsize=12, ha='center', va='center')
    ax.text(7.5, 4.7, r'$h_1$', fontsize=10, ha='center')
    
    ax.add_patch(Circle((10, 5.5), 0.6, facecolor='white', edgecolor=COLORS['threshold'], lw=2))
    ax.text(10, 5.5, r'$t_2$', fontsize=12, ha='center', va='center')
    ax.text(10, 4.7, r'$h_2 > h_1$', fontsize=10, ha='center')
    
    # Arrow showing comparison
    ax.annotate('', xy=(9.3, 5.5), xytext=(8.2, 5.5),
                arrowprops=dict(arrowstyle='<->', color=COLORS['dark'], lw=2))
    ax.text(8.75, 5.9, r'$\Delta t$', fontsize=11, ha='center')
    
    # Phase difference
    ax.text(8.75, 3.8, r'$\Delta\Phi = \omega \cdot \Delta D_{SSZ} \cdot t$', 
            fontsize=12, ha='center', color=COLORS['threshold'])
    ax.text(8.75, 3.3, 'MEASURABLE!', fontsize=10, ha='center', 
            fontweight='bold', color=COLORS['threshold'])
    
    # Bottom explanations
    ax.text(2.75, 2.3, 'Equivalence Principle:\nLocally, gravity = acceleration\n→ No "absolute" time difference',
            fontsize=9, ha='center', va='top', 
            bbox=dict(boxstyle='round', facecolor='white', edgecolor='gray'))
    
    ax.text(8.75, 2.3, 'Gravitational Redshift:\nComparing separated clocks\n→ Relative phase drift accumulates',
            fontsize=9, ha='center', va='top',
            bbox=dict(boxstyle='round', facecolor='white', edgecolor='gray'))
    
    # Key insight box
    ax.add_patch(FancyBboxPatch((3, 0.3), 6, 1.2, boxstyle="round,pad=0.1",
                                facecolor='#E8F8E8', edgecolor=COLORS['optical'], lw=2))
    ax.text(6, 1.1, 'KEY INSIGHT', fontsize=11, ha='center', fontweight='bold')
    ax.text(6, 0.6, r'SSZ effect is NOT local — it emerges from comparing phase evolution at different $\Xi(r)$',
            fontsize=10, ha='center')
    
    plt.tight_layout()
    filepath = os.path.join(OUTPUT_DIR, 'paper_d_fig1_local_vs_global.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Saved: {filepath}")
    return filepath


def fig2_phase_vs_height():
    """Figure 2: ΔΦ vs Δh (log-log) with slope=1 reference."""
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Height range
    dh = np.logspace(-4, 3, 200)  # 0.1 mm to 1 km
    
    # Calculate phase drift for different platforms
    omega_5ghz = 2 * np.pi * 5e9
    omega_optical = 2 * np.pi * 429e12
    t_ramsey = 100e-6
    t_optical = 1.0
    
    phi_transmon = []
    phi_optical = []
    
    for h in dh:
        dd = abs(ssz_time_dilation_difference(R_EARTH + h, R_EARTH, M_EARTH))
        phi_transmon.append(omega_5ghz * dd * t_ramsey)
        phi_optical.append(omega_optical * dd * t_optical)
    
    # Plot
    ax.loglog(dh, phi_transmon, '-', color=COLORS['transmon'], lw=2.5,
              label='Transmon (5 GHz, 100 μs)')
    ax.loglog(dh, phi_optical, '-', color=COLORS['optical'], lw=2.5,
              label='Optical Clock (429 THz, 1 s)')
    
    # Slope=1 reference line
    ref_line = 1e-10 * dh
    ax.loglog(dh, ref_line, '--', color='gray', lw=1.5, alpha=0.7,
              label='Slope = 1 reference')
    
    # Detection thresholds
    ax.axhline(y=1, color=COLORS['threshold'], linestyle='--', lw=2,
               label='Single-shot noise (~1 rad)')
    ax.axhline(y=1e-5, color=COLORS['threshold'], linestyle=':', lw=1.5, alpha=0.7,
               label=r'After $10^{10}$ averages')
    
    # Regime annotations
    ax.fill_between([1e-4, 1e-2], 1e-20, 1e2, alpha=0.1, color=COLORS['transmon'])
    ax.text(3e-3, 1e-17, 'On-chip\nregime', fontsize=9, ha='center', color=COLORS['transmon'])
    
    ax.fill_between([1e-1, 1e2], 1e-20, 1e2, alpha=0.1, color=COLORS['optical'])
    ax.text(3, 1e-2, 'Tower/remote\nregime', fontsize=9, ha='center', color=COLORS['optical'])
    
    # Key point annotations
    ax.scatter([1], [phi_optical[np.searchsorted(dh, 1)]], s=100, color=COLORS['optical'], zorder=5)
    ax.annotate('0.29 rad\n(detectable!)', xy=(1, 0.29), xytext=(3, 0.05),
                fontsize=10, arrowprops=dict(arrowstyle='->', color='gray'))
    
    ax.set_xlabel(r'Height difference $\Delta h$ [m]', fontsize=12)
    ax.set_ylabel(r'Phase shift $\Delta\Phi$ [rad]', fontsize=12)
    ax.set_title('Figure 2: Phase Shift vs Height Difference (SSZ Prediction)', fontsize=13)
    ax.legend(loc='lower right', fontsize=9)
    ax.set_xlim(1e-4, 1e3)
    ax.set_ylim(1e-20, 1e2)
    ax.grid(True, which='both', alpha=0.3)
    
    # Formula box
    ax.text(0.02, 0.98, r'$\Delta\Phi = \omega \cdot \frac{r_s \cdot \Delta h}{R^2} \cdot t$',
            transform=ax.transAxes, fontsize=11, va='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.9))
    
    plt.tight_layout()
    filepath = os.path.join(OUTPUT_DIR, 'paper_d_fig2_phase_vs_height.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {filepath}")
    return filepath


def fig3_scaling_omega_t():
    """Figure 3: ΔΦ scaling with ω and t (two panels)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    dh = 1.0  # 1 m height difference
    dd = abs(ssz_time_dilation_difference(R_EARTH + dh, R_EARTH, M_EARTH))
    
    # LEFT: ω scaling
    freq = np.logspace(9, 15, 100)  # 1 GHz to 1 PHz
    omega = 2 * np.pi * freq
    t_fixed = 100e-6
    
    phi_omega = omega * dd * t_fixed
    
    ax1.loglog(freq, phi_omega, '-', color=COLORS['ssz'], lw=2.5)
    
    # Mark key frequencies
    key_freq = [(5e9, 'Transmon\n5 GHz'), (429e12, 'Optical\n429 THz')]
    for f, label in key_freq:
        phi = 2*np.pi*f * dd * t_fixed
        ax1.scatter([f], [phi], s=100, color=COLORS['threshold'], zorder=5)
        ax1.annotate(label, xy=(f, phi), xytext=(f*2, phi*3),
                    fontsize=9, arrowprops=dict(arrowstyle='->', color='gray'))
    
    ax1.set_xlabel('Frequency [Hz]', fontsize=12)
    ax1.set_ylabel(r'$\Delta\Phi$ [rad]', fontsize=12)
    ax1.set_title(r'(a) $\omega$ Scaling ($\Delta h = 1$ m, $t = 100$ μs)', fontsize=12)
    ax1.grid(True, which='both', alpha=0.3)
    
    # Slope annotation
    ax1.text(0.7, 0.15, 'Slope = 1\n(linear in ω)', transform=ax1.transAxes,
             fontsize=10, color=COLORS['ssz'],
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # RIGHT: t scaling
    t = np.logspace(-6, 1, 100)  # 1 μs to 10 s
    omega_fixed = 2 * np.pi * 5e9
    
    phi_t = omega_fixed * dd * t
    
    ax2.loglog(t, phi_t, '-', color=COLORS['zone'], lw=2.5)
    
    # Mark key times
    key_t = [(100e-6, 'Ramsey\n100 μs'), (1, 'Optical\n1 s')]
    for tm, label in key_t:
        phi = omega_fixed * dd * tm
        ax2.scatter([tm], [phi], s=100, color=COLORS['threshold'], zorder=5)
        ax2.annotate(label, xy=(tm, phi), xytext=(tm*3, phi*5),
                    fontsize=9, arrowprops=dict(arrowstyle='->', color='gray'))
    
    ax2.set_xlabel('Integration time [s]', fontsize=12)
    ax2.set_ylabel(r'$\Delta\Phi$ [rad]', fontsize=12)
    ax2.set_title(r'(b) $t$ Scaling ($\Delta h = 1$ m, $\omega = 5$ GHz)', fontsize=12)
    ax2.grid(True, which='both', alpha=0.3)
    
    # Slope annotation
    ax2.text(0.7, 0.15, 'Slope = 1\n(linear in t)', transform=ax2.transAxes,
             fontsize=10, color=COLORS['zone'],
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.suptitle('Figure 3: SSZ Phase Drift Scaling Laws', fontsize=14, y=1.02)
    plt.tight_layout()
    
    filepath = os.path.join(OUTPUT_DIR, 'paper_d_fig3_scaling.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {filepath}")
    return filepath


def fig4_platform_feasibility():
    """Figure 4: Platform feasibility - Transmon vs Optical clocks."""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Data
    platforms = ['Transmon\n(on-chip)', 'Transmon\n(5° tilt)', 'Transmon\n(1m remote)', 
                 'Optical\n(1m)', 'Optical\n(10m)', 'Optical\n(100m)']
    signal = [3.4e-17, 6e-13, 3.4e-10, 0.29, 2.9, 29]
    n_shots = [np.inf, 2.8e25, 7.6e19, 100, 10, 1]
    feasible = ['No', 'No', 'No', 'YES', 'YES', 'YES']
    colors = ['#DC3545', '#DC3545', '#DC3545', '#28A745', '#28A745', '#28A745']
    
    x = np.arange(len(platforms))
    bars = ax.bar(x, [max(s, 1e-18) for s in signal], color=colors, alpha=0.8, edgecolor='black')
    
    ax.set_yscale('log')
    ax.set_ylabel(r'Phase Signal $|\Delta\Phi|$ [rad]', fontsize=12)
    ax.set_xlabel('Experimental Platform', fontsize=12)
    ax.set_title('Figure 4: Platform Feasibility Comparison', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(platforms, fontsize=10)
    
    # Detection threshold
    ax.axhline(y=1, color=COLORS['threshold'], linestyle='--', lw=2, 
               label='Detection threshold (~1 rad)')
    ax.axhline(y=0.1, color=COLORS['threshold'], linestyle=':', lw=1.5, alpha=0.7,
               label='Good SNR threshold (~0.1 rad)')
    
    # Labels
    for i, (bar, feas, n) in enumerate(zip(bars, feasible, n_shots)):
        height = max(bar.get_height(), 1e-17)
        if n == np.inf:
            n_str = 'N = ∞'
        elif n >= 1e10:
            n_str = f'N ~ 10$^{{{int(np.log10(n))}}}$'
        else:
            n_str = f'N ~ {int(n)}'
        
        label = f'{feas}\n{n_str}'
        ax.text(bar.get_x() + bar.get_width()/2., height * 3, 
                label, ha='center', va='bottom', fontsize=9,
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))
    
    # Regime separator
    ax.axvline(x=2.5, color='gray', linestyle='--', alpha=0.5)
    ax.text(1, 1e-1, 'BOUND REGIME\n(Superconducting)', fontsize=11, ha='center',
            color=COLORS['threshold'], fontweight='bold')
    ax.text(4.5, 1e-1, 'DETECTION REGIME\n(Optical Clocks)', fontsize=11, ha='center',
            color=COLORS['optical'], fontweight='bold')
    
    ax.set_ylim(1e-18, 1e3)
    ax.legend(loc='lower right', fontsize=10)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    filepath = os.path.join(OUTPUT_DIR, 'paper_d_fig4_feasibility.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {filepath}")
    return filepath


def fig5_experimental_setups():
    """Figure 5: Upper-bound protocol diagram (tilt/stack/remote)."""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    for ax in axes:
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 8)
        ax.axis('off')
    
    # (a) Chip Tilt
    ax1 = axes[0]
    ax1.set_title('(a) Chip Tilt', fontsize=12, fontweight='bold')
    
    # Tilted chip
    theta = 15
    L = 6
    x0, y0 = 2, 2
    x1 = x0 + L * np.cos(np.radians(theta))
    y1 = y0 + L * np.sin(np.radians(theta))
    
    ax1.plot([x0, x1], [y0, y1], 'b-', lw=8, solid_capstyle='round')
    ax1.plot([x0, x1], [y0-0.2, y1-0.2], 'b-', lw=8, alpha=0.3)
    
    # Qubits
    ax1.scatter([x0+0.5], [y0+0.5*np.tan(np.radians(theta))], s=200, c='red', zorder=5)
    ax1.scatter([x1-0.5], [y1-0.5*np.tan(np.radians(theta))], s=200, c='red', zorder=5)
    ax1.text(x0+0.5, y0+1.2, 'Q1', fontsize=10, ha='center')
    ax1.text(x1-0.5, y1+0.8, 'Q2', fontsize=10, ha='center')
    
    # Δh arrow
    ax1.annotate('', xy=(x1+0.3, y1), xytext=(x1+0.3, y0),
                arrowprops=dict(arrowstyle='<->', color='green', lw=2))
    ax1.text(x1+0.8, (y0+y1)/2, r'$\Delta h$', fontsize=12, va='center', color='green')
    
    # Angle
    angle_arc = np.linspace(0, np.radians(theta), 20)
    arc_r = 1.5
    ax1.plot(x0 + arc_r*np.cos(angle_arc), y0 + arc_r*np.sin(angle_arc), 'k-', lw=1)
    ax1.text(x0+1.8, y0+0.4, r'$\theta$', fontsize=11)
    
    # Formula
    ax1.text(5, 0.5, r'$\Delta h = L \cdot \sin(\theta)$', fontsize=11, ha='center',
             bbox=dict(boxstyle='round', facecolor='wheat'))
    
    # (b) 3D Chiplet Stack
    ax2 = axes[1]
    ax2.set_title('(b) 3D Chiplet Stack', fontsize=12, fontweight='bold')
    
    # Lower chip
    ax2.add_patch(FancyBboxPatch((2, 2), 6, 1, boxstyle="round,pad=0.05",
                                 facecolor='#4A90D9', edgecolor='black', lw=2))
    ax2.scatter([3.5, 6.5], [2.5, 2.5], s=200, c='red', zorder=5)
    ax2.text(5, 2.5, 'Chip A', fontsize=10, ha='center', color='white', fontweight='bold')
    
    # Upper chip
    ax2.add_patch(FancyBboxPatch((2, 5), 6, 1, boxstyle="round,pad=0.05",
                                 facecolor='#D94A4A', edgecolor='black', lw=2))
    ax2.scatter([3.5, 6.5], [5.5, 5.5], s=200, c='red', zorder=5)
    ax2.text(5, 5.5, 'Chip B', fontsize=10, ha='center', color='white', fontweight='bold')
    
    # Interposer
    ax2.add_patch(Rectangle((4, 3), 2, 2, facecolor='gray', edgecolor='black', alpha=0.5))
    ax2.text(5, 4, 'TSV\nLink', fontsize=9, ha='center', va='center')
    
    # Δh arrow
    ax2.annotate('', xy=(8.5, 5.5), xytext=(8.5, 2.5),
                arrowprops=dict(arrowstyle='<->', color='green', lw=2))
    ax2.text(9, 4, r'$\Delta h$' + '\n~2mm', fontsize=10, va='center', color='green')
    
    # (c) Remote Entanglement
    ax3 = axes[2]
    ax3.set_title('(c) Remote Entanglement', fontsize=12, fontweight='bold')
    
    # Two fridges
    for x, label, h in [(1.5, 'Fridge A\n(lower)', 2), (6.5, 'Fridge B\n(higher)', 4)]:
        ax3.add_patch(FancyBboxPatch((x, h), 2, 3, boxstyle="round,pad=0.1",
                                     facecolor='#E8E8E8', edgecolor='black', lw=2))
        ax3.scatter([x+1], [h+1.5], s=200, c='red', zorder=5)
        ax3.text(x+1, h+2.8, label, fontsize=9, ha='center')
    
    # Microwave link
    ax3.annotate('', xy=(6.5, 4.5), xytext=(3.5, 3.5),
                arrowprops=dict(arrowstyle='<->', color='orange', lw=2, 
                               connectionstyle='arc3,rad=0.2'))
    ax3.text(5, 5.5, 'Microwave\nLink', fontsize=9, ha='center', color='orange')
    
    # Δh arrow
    ax3.annotate('', xy=(9, 5.5), xytext=(9, 3.5),
                arrowprops=dict(arrowstyle='<->', color='green', lw=2))
    ax3.text(9.5, 4.5, r'$\Delta h$' + '\n1-100m', fontsize=10, va='center', color='green')
    
    plt.suptitle('Figure 5: Hardware Configurations for Height Difference Generation', 
                 fontsize=14, y=1.02)
    plt.tight_layout()
    
    filepath = os.path.join(OUTPUT_DIR, 'paper_d_fig5_setups.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Saved: {filepath}")
    return filepath


def fig6_confound_matrix():
    """Figure 6: Confound signature discrimination matrix."""
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis('off')
    
    # Table data
    headers = ['Source', 'Δh Scaling', 'ω Scaling', 't Scaling', 'Randomization', 'Control']
    data = [
        ['SSZ Effect', 'Linear ✓', 'Linear ✓', 'Linear ✓', 'Invariant ✓', 'SIGNATURE'],
        ['Temperature', 'May correlate', 'Weak (~0)', 'Complex', 'Varies', 'Thermometry'],
        ['LO Phase Noise', 'None', 'None', '√t', 'Varies', 'Reference LO'],
        ['Magnetic Flux', 'Position dep.', 'Nonlinear', 'DC/AC', 'Varies', 'Shielding'],
        ['Vibration', 'Mechanical', 'None', 'AC spectrum', 'Varies', 'Accelerometer'],
        ['EM Crosstalk', 'Position', 'Resonant', 'Constant', 'Varies', 'Filtering'],
    ]
    
    # Colors
    header_color = '#2E86AB'
    ssz_color = '#D4EDDA'
    confound_color = '#FFF3CD'
    
    # Create table
    n_rows = len(data) + 1
    n_cols = len(headers)
    cell_height = 0.8
    cell_widths = [2.2, 2, 2, 2, 2, 2]
    
    y_start = 7
    x_start = 0.5
    
    # Headers
    x = x_start
    for i, (header, width) in enumerate(zip(headers, cell_widths)):
        ax.add_patch(FancyBboxPatch((x, y_start), width, cell_height,
                                    boxstyle="round,pad=0.02",
                                    facecolor=header_color, edgecolor='white', lw=2))
        ax.text(x + width/2, y_start + cell_height/2, header,
                fontsize=10, ha='center', va='center', color='white', fontweight='bold')
        x += width
    
    # Data rows
    for row_idx, row in enumerate(data):
        y = y_start - (row_idx + 1) * cell_height
        x = x_start
        
        row_color = ssz_color if row_idx == 0 else confound_color
        
        for col_idx, (cell, width) in enumerate(zip(row, cell_widths)):
            ax.add_patch(FancyBboxPatch((x, y), width, cell_height,
                                        boxstyle="round,pad=0.02",
                                        facecolor=row_color, edgecolor='gray', lw=1))
            
            fontweight = 'bold' if col_idx == 0 or (row_idx == 0 and '✓' in cell) else 'normal'
            color = COLORS['optical'] if '✓' in cell else 'black'
            
            ax.text(x + width/2, y + cell_height/2, cell,
                    fontsize=9, ha='center', va='center', fontweight=fontweight, color=color)
            x += width
    
    # Title
    ax.text(6.5, 8, 'Figure 6: Confound Discrimination Matrix', 
            fontsize=14, ha='center', fontweight='bold')
    
    # Legend
    ax.add_patch(Rectangle((1, 0.3), 0.5, 0.4, facecolor=ssz_color, edgecolor='gray'))
    ax.text(1.7, 0.5, 'SSZ Signature (target)', fontsize=10, va='center')
    
    ax.add_patch(Rectangle((5, 0.3), 0.5, 0.4, facecolor=confound_color, edgecolor='gray'))
    ax.text(5.7, 0.5, 'Confound (to separate)', fontsize=10, va='center')
    
    # Key insight
    ax.text(6.5, -0.5, 
            'KEY: SSZ is uniquely identified by LINEAR scaling in ALL THREE parameters (Δh, ω, t)\n'
            'AND invariance under randomization. No confound matches this full signature.',
            fontsize=10, ha='center', style='italic',
            bbox=dict(boxstyle='round', facecolor='#E8F8E8', edgecolor=COLORS['optical']))
    
    ax.set_xlim(0, 13)
    ax.set_ylim(-1.5, 8.5)
    
    plt.tight_layout()
    filepath = os.path.join(OUTPUT_DIR, 'paper_d_fig6_confounds.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Saved: {filepath}")
    return filepath


def fig7_claim_taxonomy():
    """Figure 7: Claim taxonomy box."""
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.axis('off')
    
    # Title
    ax.text(0.5, 0.95, 'SSZ CLAIM TAXONOMY', fontsize=16, ha='center', 
            fontweight='bold', transform=ax.transAxes)
    
    # Three columns
    columns = [
        ('BOUNDED TODAY', '#FFCDD2', [
            'Transmon qubits at mm-scale Δh',
            'Upper bound: |α| < 10⁻² rad/m',
            'Constrains anomalous couplings',
            'Null result = SSZ-consistent',
        ]),
        ('DETECTABLE SOON', '#FFF9C4', [
            'Optical clocks at 1-10 m Δh',
            'Signal: 0.3-3 rad (SNR >> 1)',
            'Existing technology sufficient',
            'Direct SSZ test possible',
        ]),
        ('ENGINEERING RELEVANCE', '#C8E6C9', [
            'QEC with T₂ >> 1 s',
            'Distributed quantum computing',
            'Multi-story quantum networks',
            'Phase compensation required',
        ]),
    ]
    
    x_positions = [0.17, 0.5, 0.83]
    
    for x, (title, color, items) in zip(x_positions, columns):
        # Box
        ax.add_patch(FancyBboxPatch((x-0.14, 0.15), 0.28, 0.7,
                                    boxstyle="round,pad=0.02",
                                    facecolor=color, edgecolor='gray', lw=2,
                                    transform=ax.transAxes))
        
        # Title
        ax.text(x, 0.82, title, fontsize=11, ha='center', fontweight='bold',
                transform=ax.transAxes)
        
        # Items
        for i, item in enumerate(items):
            ax.text(x, 0.72 - i*0.13, f'• {item}', fontsize=9, ha='center',
                    transform=ax.transAxes, wrap=True)
    
    # Bottom note
    ax.text(0.5, 0.05, 
            'All claims are testable. SSZ is falsified if measured slope significantly differs from prediction\n'
            'at >3σ in a regime where detection is feasible (optical clocks).',
            fontsize=10, ha='center', transform=ax.transAxes, style='italic')
    
    plt.tight_layout()
    filepath = os.path.join(OUTPUT_DIR, 'paper_d_fig7_taxonomy.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Saved: {filepath}")
    return filepath


def main():
    print("="*70)
    print("Generating Master Paper D - Complete Figure Pack")
    print("="*70)
    
    figures = []
    
    print("\nFigure 1: Local vs Global Comparison...")
    figures.append(fig1_local_vs_global())
    
    print("\nFigure 2: Phase vs Height...")
    figures.append(fig2_phase_vs_height())
    
    print("\nFigure 3: omega and t Scaling...")
    figures.append(fig3_scaling_omega_t())
    
    print("\nFigure 4: Platform Feasibility...")
    figures.append(fig4_platform_feasibility())
    
    print("\nFigure 5: Experimental Setups...")
    figures.append(fig5_experimental_setups())
    
    print("\nFigure 6: Confound Matrix...")
    figures.append(fig6_confound_matrix())
    
    print("\nFigure 7: Claim Taxonomy...")
    figures.append(fig7_claim_taxonomy())
    
    print("\n" + "="*70)
    print(f"All 7 figures saved to: {OUTPUT_DIR}")
    print("="*70)
    
    return figures


if __name__ == "__main__":
    main()
