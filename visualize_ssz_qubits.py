#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSZ-Qubits Visualization

Visualizes SSZ effects on qubit systems:
- Time dilation vs height
- Segment density maps
- Qubit pair mismatch analysis
- Coherent zone visualization

© 2025 Carmen Wrede, Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from ssz_qubits import (
    R_EARTH, M_EARTH, C, G, PHI,
    schwarzschild_radius, xi_segment_density, xi_gradient,
    ssz_time_dilation, time_difference_per_second,
    Qubit, QubitPair,
    analyze_qubit_segment, qubit_pair_segment_mismatch,
    segment_coherent_zone, optimize_qubit_array, array_segment_uniformity
)

# Output directory
OUTPUT_DIR = Path(__file__).parent / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)


def plot_time_dilation_vs_height():
    """Plot SSZ time dilation as function of height above sea level."""
    print("Generating: Time Dilation vs Height...")
    
    heights = np.logspace(-3, 5, 1000)  # 1mm to 100km
    
    xi_values = []
    d_values = []
    dt_per_second = []
    
    for h in heights:
        r = R_EARTH + h
        xi = xi_segment_density(r, M_EARTH)
        d = ssz_time_dilation(r, M_EARTH)
        dt = time_difference_per_second(r, R_EARTH, M_EARTH) * 1e12  # picoseconds
        
        xi_values.append(xi)
        d_values.append(d)
        dt_per_second.append(dt)
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Plot 1: Xi vs height
    ax1 = axes[0, 0]
    ax1.loglog(heights, xi_values, 'b-', linewidth=2)
    ax1.set_xlabel('Height above sea level [m]')
    ax1.set_ylabel('Segment Density Xi')
    ax1.set_title('SSZ Segment Density vs Height')
    ax1.grid(True, alpha=0.3)
    ax1.axvline(x=1, color='r', linestyle='--', alpha=0.5, label='1 m')
    ax1.axvline(x=1000, color='g', linestyle='--', alpha=0.5, label='1 km')
    ax1.legend()
    
    # Plot 2: D_SSZ vs height
    ax2 = axes[0, 1]
    deviation = [(1 - d) * 1e9 for d in d_values]  # parts per billion
    ax2.semilogx(heights, deviation, 'r-', linewidth=2)
    ax2.set_xlabel('Height above sea level [m]')
    ax2.set_ylabel('(1 - D_SSZ) [ppb]')
    ax2.set_title('SSZ Time Dilation Deviation from Unity')
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Time difference per second
    ax3 = axes[1, 0]
    ax3.loglog(heights, dt_per_second, 'g-', linewidth=2)
    ax3.set_xlabel('Height above sea level [m]')
    ax3.set_ylabel('Time difference per second [ps]')
    ax3.set_title('Accumulated Time Difference vs Sea Level')
    ax3.grid(True, alpha=0.3)
    
    # Add reference lines
    ax3.axhline(y=1, color='orange', linestyle='--', alpha=0.5, label='1 ps')
    ax3.axhline(y=0.001, color='purple', linestyle='--', alpha=0.5, label='1 fs')
    ax3.legend()
    
    # Plot 4: Gradient vs height
    ax4 = axes[1, 1]
    gradients = [abs(xi_gradient(R_EARTH + h, M_EARTH)) for h in heights]
    ax4.loglog(heights, gradients, 'm-', linewidth=2)
    ax4.set_xlabel('Height above sea level [m]')
    ax4.set_ylabel('|dXi/dr| [1/m]')
    ax4.set_title('Segment Density Gradient Magnitude')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    output_file = OUTPUT_DIR / "time_dilation_vs_height.png"
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {output_file}")


def plot_qubit_pair_mismatch():
    """Plot segment mismatch for qubit pairs at various height differences."""
    print("Generating: Qubit Pair Mismatch Analysis...")
    
    height_diffs = np.logspace(-9, -1, 100)  # 1nm to 10cm
    
    delta_xi = []
    delta_d = []
    phase_drift = []
    
    for dh in height_diffs:
        q1 = Qubit(id="Q1", x=0, y=0, z=0)
        q2 = Qubit(id="Q2", x=0, y=0, z=dh)
        pair = QubitPair(q1, q2)
        
        mismatch = qubit_pair_segment_mismatch(pair, M_EARTH)
        
        delta_xi.append(mismatch['delta_xi'])
        delta_d.append(mismatch['delta_time_dilation'])
        phase_drift.append(mismatch['phase_drift_per_gate'])
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Plot 1: Delta Xi
    ax1 = axes[0]
    ax1.loglog(height_diffs * 1e6, delta_xi, 'b-', linewidth=2)
    ax1.set_xlabel('Height difference [um]')
    ax1.set_ylabel('Delta Xi')
    ax1.set_title('Segment Density Mismatch')
    ax1.grid(True, alpha=0.3)
    
    # Reference lines
    ax1.axvline(x=1, color='r', linestyle='--', alpha=0.5, label='1 um')
    ax1.axvline(x=1000, color='g', linestyle='--', alpha=0.5, label='1 mm')
    ax1.legend()
    
    # Plot 2: Delta D_SSZ
    ax2 = axes[1]
    ax2.loglog(height_diffs * 1e6, delta_d, 'r-', linewidth=2)
    ax2.set_xlabel('Height difference [um]')
    ax2.set_ylabel('Delta D_SSZ')
    ax2.set_title('Time Dilation Mismatch')
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Phase drift
    ax3 = axes[2]
    ax3.loglog(height_diffs * 1e6, phase_drift, 'g-', linewidth=2)
    ax3.set_xlabel('Height difference [um]')
    ax3.set_ylabel('Phase drift per gate [rad]')
    ax3.set_title('SSZ-Induced Phase Drift')
    ax3.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    output_file = OUTPUT_DIR / "qubit_pair_mismatch.png"
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {output_file}")


def plot_coherent_zone():
    """Visualize segment-coherent zones for qubit placement."""
    print("Generating: Segment Coherent Zone Visualization...")
    
    center_heights = [0, 1, 10, 100, 1000]  # meters
    xi_variations = [1e-17, 1e-16, 1e-15, 1e-14]
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    colors = plt.cm.viridis(np.linspace(0, 1, len(xi_variations)))
    
    for i, var in enumerate(xi_variations):
        widths = []
        for h in center_heights:
            h_min, h_max = segment_coherent_zone(h, max_xi_variation=var, M=M_EARTH)
            width = h_max - h_min
            widths.append(width)
        
        ax.semilogy(center_heights, widths, 'o-', color=colors[i], 
                   linewidth=2, markersize=8, label=f'Max dXi = {var:.0e}')
    
    ax.set_xlabel('Center Height [m]')
    ax.set_ylabel('Coherent Zone Width [m]')
    ax.set_title('Segment-Coherent Zone Width vs Height\n(Zone where Xi variation < threshold)')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    plt.tight_layout()
    
    output_file = OUTPUT_DIR / "coherent_zone.png"
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {output_file}")


def plot_qubit_array_analysis():
    """Analyze and visualize optimized qubit array."""
    print("Generating: Qubit Array Analysis...")
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Plot 1: Array layout (top view)
    ax1 = axes[0, 0]
    qubits = optimize_qubit_array(25, base_height=0, max_separation=1e-3)
    
    x_coords = [q.x * 1e3 for q in qubits]  # mm
    y_coords = [q.y * 1e3 for q in qubits]  # mm
    
    ax1.scatter(x_coords, y_coords, s=100, c='blue', alpha=0.7)
    for i, q in enumerate(qubits):
        ax1.annotate(f'{i}', (q.x*1e3, q.y*1e3), fontsize=8, ha='center', va='center')
    
    ax1.set_xlabel('X position [mm]')
    ax1.set_ylabel('Y position [mm]')
    ax1.set_title('Optimized 25-Qubit Array Layout (Top View)')
    ax1.set_aspect('equal')
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Xi uniformity vs array size
    ax2 = axes[0, 1]
    array_sizes = [4, 9, 16, 25, 36, 49, 64, 81, 100]
    uniformities = []
    
    for n in array_sizes:
        qubits = optimize_qubit_array(n, base_height=0, max_separation=1e-3)
        u = array_segment_uniformity(qubits, M_EARTH)
        uniformities.append(u['uniformity'])
    
    ax2.plot(array_sizes, uniformities, 'go-', linewidth=2, markersize=8)
    ax2.set_xlabel('Number of Qubits')
    ax2.set_ylabel('Segment Uniformity')
    ax2.set_title('Array Segment Uniformity vs Size')
    ax2.set_ylim([0.999, 1.001])
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Effect of height variation
    ax3 = axes[1, 0]
    
    # Create array with intentional height variation
    n_qubits = 16
    height_variations = np.linspace(0, 1e-3, 20)  # 0 to 1mm variation
    xi_ranges = []
    
    for h_var in height_variations:
        qubits = []
        for i in range(n_qubits):
            z = np.random.uniform(0, h_var)
            qubits.append(Qubit(id=f"Q{i}", x=0, y=0, z=z))
        
        u = array_segment_uniformity(qubits, M_EARTH)
        xi_ranges.append(u['xi_range'])
    
    ax3.semilogy(height_variations * 1e6, xi_ranges, 'r-', linewidth=2)
    ax3.set_xlabel('Height Variation Range [um]')
    ax3.set_ylabel('Xi Range in Array')
    ax3.set_title('Segment Non-Uniformity vs Height Variation')
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Comparison with/without SSZ optimization
    ax4 = axes[1, 1]
    
    # Optimized (constant height)
    qubits_opt = optimize_qubit_array(16, base_height=0, max_separation=1e-3)
    u_opt = array_segment_uniformity(qubits_opt, M_EARTH)
    
    # Non-optimized (random heights)
    qubits_rand = []
    for i in range(16):
        z = np.random.uniform(0, 1e-4)  # 0-100um random height
        qubits_rand.append(Qubit(id=f"Q{i}", x=0, y=0, z=z))
    u_rand = array_segment_uniformity(qubits_rand, M_EARTH)
    
    categories = ['Optimized\n(constant h)', 'Random\n(0-100um)']
    xi_ranges = [u_opt['xi_range'], u_rand['xi_range']]
    
    bars = ax4.bar(categories, xi_ranges, color=['green', 'red'], alpha=0.7)
    ax4.set_ylabel('Xi Range')
    ax4.set_title('Segment Uniformity: Optimized vs Random Placement')
    ax4.set_yscale('log')
    
    # Add value labels
    for bar, val in zip(bars, xi_ranges):
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height(), 
                f'{val:.2e}', ha='center', va='bottom', fontsize=10)
    
    try:
        plt.tight_layout()
    except:
        pass
    
    output_file = OUTPUT_DIR / "qubit_array_analysis.png"
    fig.savefig(output_file, dpi=100, bbox_inches='tight')
    plt.close(fig)
    print(f"  Saved: {output_file}")


def plot_ssz_vs_gr_comparison():
    """Compare SSZ and GR time dilation predictions."""
    print("Generating: SSZ vs GR Comparison...")
    
    # Range of radii from 2*r_s to 1000*r_s
    r_s = schwarzschild_radius(M_EARTH)
    r_factors = np.logspace(0.3, 3, 100)  # 2 to 1000 times r_s
    radii = r_factors * r_s
    
    d_ssz = []
    d_gr = []
    
    for r in radii:
        xi = xi_segment_density(r, M_EARTH)
        d_ssz.append(1.0 / (1.0 + xi))
        d_gr.append(np.sqrt(1 - r_s/r))
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Plot 1: Both predictions
    ax1 = axes[0]
    ax1.semilogx(r_factors, d_ssz, 'b-', linewidth=2, label='SSZ: 1/(1+Xi)')
    ax1.semilogx(r_factors, d_gr, 'r--', linewidth=2, label='GR: sqrt(1-r_s/r)')
    ax1.set_xlabel('r / r_s')
    ax1.set_ylabel('Time Dilation Factor')
    ax1.set_title('SSZ vs GR Time Dilation')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Relative difference
    ax2 = axes[1]
    rel_diff = [abs(s - g) / g * 100 for s, g in zip(d_ssz, d_gr)]
    ax2.loglog(r_factors, rel_diff, 'g-', linewidth=2)
    ax2.set_xlabel('r / r_s')
    ax2.set_ylabel('Relative Difference [%]')
    ax2.set_title('SSZ vs GR Relative Difference')
    ax2.grid(True, alpha=0.3)
    
    # Mark Earth's surface
    r_earth_factor = R_EARTH / r_s
    ax2.axvline(x=r_earth_factor, color='orange', linestyle='--', 
               alpha=0.7, label=f'Earth surface (r/r_s = {r_earth_factor:.0e})')
    ax2.legend()
    
    plt.tight_layout()
    
    output_file = OUTPUT_DIR / "ssz_vs_gr_comparison.png"
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {output_file}")


def plot_golden_ratio_structure():
    """Visualize golden ratio (phi) in SSZ framework."""
    print("Generating: Golden Ratio Structure...")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Plot 1: Phi spiral
    ax1 = axes[0]
    
    theta = np.linspace(0, 6*np.pi, 1000)
    r = PHI ** (theta / (2*np.pi))
    
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    
    ax1.plot(x, y, 'b-', linewidth=2)
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_title(f'Golden Spiral (phi = {PHI:.6f})')
    ax1.set_aspect('equal')
    ax1.grid(True, alpha=0.3)
    
    # Mark phi points
    for n in range(7):
        theta_n = n * np.pi / 2
        r_n = PHI ** (theta_n / (2*np.pi))
        x_n = r_n * np.cos(theta_n)
        y_n = r_n * np.sin(theta_n)
        ax1.plot(x_n, y_n, 'ro', markersize=8)
        ax1.annotate(f'n={n}', (x_n, y_n), fontsize=8)
    
    # Plot 2: Phi properties
    ax2 = axes[1]
    
    # Show phi^n sequence
    n_values = np.arange(0, 10)
    phi_powers = [PHI**n for n in n_values]
    
    ax2.semilogy(n_values, phi_powers, 'go-', linewidth=2, markersize=10, label='phi^n')
    
    # Show Fibonacci approximation
    fib = [1, 1]
    for _ in range(8):
        fib.append(fib[-1] + fib[-2])
    fib_ratios = [fib[i+1]/fib[i] for i in range(len(fib)-1)]
    
    ax2.semilogy(range(len(fib_ratios)), [PHI**n for n in range(len(fib_ratios))], 
                'b--', alpha=0.5, label='Reference')
    
    ax2.set_xlabel('n')
    ax2.set_ylabel('Value')
    ax2.set_title('Golden Ratio Powers\nphi^2 = phi + 1')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Add text box with phi properties
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    textstr = f'phi = {PHI:.10f}\nphi^2 = {PHI**2:.10f}\nphi + 1 = {PHI+1:.10f}\n1/phi = {1/PHI:.10f}\nphi - 1 = {PHI-1:.10f}'
    ax2.text(0.05, 0.95, textstr, transform=ax2.transAxes, fontsize=10,
            verticalalignment='top', bbox=props)
    
    plt.tight_layout()
    
    output_file = OUTPUT_DIR / "golden_ratio_structure.png"
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {output_file}")


def generate_all_plots():
    """Generate all visualization plots."""
    print("\n" + "="*70)
    print("SSZ-QUBITS VISUALIZATION")
    print("="*70)
    print(f"Output directory: {OUTPUT_DIR}")
    print("="*70 + "\n")
    
    plot_time_dilation_vs_height()
    plot_qubit_pair_mismatch()
    plot_coherent_zone()
    plot_qubit_array_analysis()
    plot_ssz_vs_gr_comparison()
    plot_golden_ratio_structure()
    
    print("\n" + "="*70)
    print("All visualizations generated successfully!")
    print(f"Output directory: {OUTPUT_DIR}")
    print("="*70)
    
    # License notice
    print()
    print("=" * 70)
    print("SSZ-Qubits - Segmented Spacetime Framework for Quantum Computing")
    print("Copyright (c) 2025 Carmen Wrede and Lino Casu")
    print("Licensed under the Anti-Capitalist Software License v1.4")
    print("https://github.com/error-wtf/ssz-qubits")
    print("=" * 70)


if __name__ == "__main__":
    generate_all_plots()
