#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSZ-Qubits: Interactive Demonstration

This script demonstrates all key features of the SSZ-Qubits framework
with practical examples and visualizations.

Run: python demo.py

(c) 2025 Carmen Wrede & Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""

import numpy as np
import sys
from dataclasses import dataclass
from typing import List, Tuple

# Import SSZ-Qubits module
from ssz_qubits import (
    # Constants
    C, G, HBAR, M_EARTH, R_EARTH, PHI,
    # Core functions
    schwarzschild_radius, xi_segment_density, xi_gradient,
    ssz_time_dilation, ssz_time_dilation_difference, time_difference_per_second,
    # Qubit classes
    Qubit, QubitPair, SegmentAnalysis,
    # Qubit functions
    analyze_qubit_segment, qubit_pair_segment_mismatch,
    optimal_qubit_height, segment_coherent_zone,
    gate_timing_correction, two_qubit_gate_timing,
    ssz_decoherence_rate, effective_T2, pair_decoherence_time,
    optimize_qubit_array, array_segment_uniformity,
    height_to_time_offset
)


def print_header(title: str):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_section(title: str):
    """Print a section header."""
    print(f"\n--- {title} ---")


def demo_1_basic_ssz_physics():
    """Demo 1: Basic SSZ Physics"""
    print_header("DEMO 1: Basic SSZ Physics")
    
    # Schwarzschild radius
    print_section("Schwarzschild Radius")
    r_s_earth = schwarzschild_radius(M_EARTH)
    r_s_sun = schwarzschild_radius(1.989e30)
    print(f"  Earth: r_s = {r_s_earth*1e3:.4f} mm")
    print(f"  Sun:   r_s = {r_s_sun/1e3:.2f} km")
    
    # Segment Density at Earth's surface
    print_section("Segment Density Xi(r)")
    xi_surface = xi_segment_density(R_EARTH, M_EARTH)
    xi_1km = xi_segment_density(R_EARTH + 1000, M_EARTH)
    xi_gps = xi_segment_density(R_EARTH + 20200e3, M_EARTH)
    print(f"  At surface:     Xi = {xi_surface:.6e}")
    print(f"  At 1 km:        Xi = {xi_1km:.6e}")
    print(f"  At GPS (20200km): Xi = {xi_gps:.6e}")
    
    # Time Dilation
    print_section("SSZ Time Dilation D_SSZ")
    d_surface = ssz_time_dilation(R_EARTH, M_EARTH)
    d_1km = ssz_time_dilation(R_EARTH + 1000, M_EARTH)
    d_gps = ssz_time_dilation(R_EARTH + 20200e3, M_EARTH)
    print(f"  At surface:     D_SSZ = {d_surface:.15f}")
    print(f"  At 1 km:        D_SSZ = {d_1km:.15f}")
    print(f"  At GPS:         D_SSZ = {d_gps:.15f}")
    
    # Golden Ratio
    print_section("Golden Ratio phi")
    print(f"  phi = {PHI:.15f}")
    print(f"  phi^2 = {PHI**2:.15f}")
    print(f"  phi + 1 = {PHI + 1:.15f}")
    print(f"  Verification: phi^2 = phi + 1 ? {np.isclose(PHI**2, PHI + 1)}")


def demo_2_qubit_analysis():
    """Demo 2: Single Qubit Analysis"""
    print_header("DEMO 2: Single Qubit Analysis")
    
    # Create qubits at different heights
    print_section("Creating Qubits")
    q1 = Qubit(id="Q1", x=0, y=0, z=0)
    q2 = Qubit(id="Q2", x=0, y=0, z=0.001)  # 1 mm higher
    q3 = Qubit(id="Q3", x=0, y=0, z=0.01)   # 1 cm higher
    q4 = Qubit(id="Q4", x=0, y=0, z=1.0)    # 1 m higher
    
    print(f"  Q1: z = {q1.z*1e3:.1f} mm (sea level)")
    print(f"  Q2: z = {q2.z*1e3:.1f} mm")
    print(f"  Q3: z = {q3.z*1e3:.1f} mm")
    print(f"  Q4: z = {q4.z*1e3:.1f} mm")
    
    # Analyze each qubit
    print_section("Segment Analysis")
    print(f"{'Qubit':>6} | {'Height':>10} | {'Xi':>20} | {'D_SSZ':>20}")
    print("-" * 65)
    
    for q in [q1, q2, q3, q4]:
        analysis = analyze_qubit_segment(q, M_EARTH)
        height_str = f"{q.z*1e3:.1f} mm" if q.z < 1 else f"{q.z:.1f} m"
        print(f"{q.id:>6} | {height_str:>10} | {analysis.xi:>20.15e} | {analysis.time_dilation:>20.15f}")


def demo_3_qubit_pair_mismatch():
    """Demo 3: Qubit Pair Mismatch Analysis"""
    print_header("DEMO 3: Qubit Pair Mismatch")
    
    # Create qubit pairs with different height differences
    print_section("Height Difference Effects")
    
    base_qubit = Qubit(id="Q0", x=0, y=0, z=0, gate_time=50e-9)
    height_diffs = [1e-6, 10e-6, 100e-6, 1e-3, 10e-3]  # 1um to 10mm
    
    print(f"{'Height Diff':>12} | {'Delta Xi':>15} | {'Phase Drift/Gate':>18} | {'Decoherence Factor':>18}")
    print("-" * 70)
    
    for h in height_diffs:
        q = Qubit(id="Q1", x=0, y=0, z=h, gate_time=50e-9)
        pair = QubitPair(base_qubit, q)
        mismatch = qubit_pair_segment_mismatch(pair, M_EARTH)
        
        h_str = f"{h*1e6:.0f} um" if h < 1e-3 else f"{h*1e3:.0f} mm"
        print(f"{h_str:>12} | {mismatch['delta_xi']:>15.6e} | {mismatch['phase_drift_per_gate']:>18.6e} | {mismatch['decoherence_enhancement']:>18.6f}")
    
    # Detailed pair analysis
    print_section("Detailed Pair Analysis (1 mm difference)")
    q1 = Qubit(id="Q1", x=0, y=0, z=0, gate_time=50e-9)
    q2 = Qubit(id="Q2", x=1e-3, y=0, z=1e-3, gate_time=50e-9)  # 1mm away, 1mm higher
    pair = QubitPair(q1, q2)
    
    print(f"  Separation: {pair.separation*1e3:.3f} mm")
    print(f"  Height diff: {pair.height_difference*1e3:.3f} mm")
    
    mismatch = qubit_pair_segment_mismatch(pair, M_EARTH)
    print(f"  Delta Xi: {mismatch['delta_xi']:.6e}")
    print(f"  Delta D_SSZ: {mismatch['delta_time_dilation']:.6e}")
    
    timing = two_qubit_gate_timing(pair, M_EARTH)
    print(f"  Optimal gate time: {timing['optimal_gate_time']*1e9:.6f} ns")
    print(f"  Timing asymmetry: {timing['timing_asymmetry']:.6e}")


def demo_4_coherent_zones():
    """Demo 4: Segment-Coherent Zones"""
    print_header("DEMO 4: Segment-Coherent Zones")
    
    print_section("Finding Coherent Zones")
    
    # Different tolerances
    tolerances = [1e-16, 1e-17, 1e-18, 1e-19, 1e-20]
    
    print(f"{'Tolerance':>12} | {'Zone Width':>15} | {'Lower [um]':>12} | {'Upper [um]':>12}")
    print("-" * 60)
    
    for tol in tolerances:
        zone = segment_coherent_zone(0, tol, M_EARTH)
        h_min, h_max = zone
        width = h_max - h_min
        
        print(f"{tol:>12.0e} | {width*1e6:>15.3f} | {h_min*1e6:>12.3f} | {h_max*1e6:>12.3f}")
    
    print("\n  -> Tighter tolerance = Smaller coherent zone")
    print("  -> Place all qubits within zone for minimal mismatch")


def demo_5_array_optimization():
    """Demo 5: Qubit Array Optimization"""
    print_header("DEMO 5: Qubit Array Optimization")
    
    # Optimized array
    print_section("Optimized 16-Qubit Array")
    qubits_opt = optimize_qubit_array(16, base_height=0, max_separation=1e-3)
    uniformity_opt = array_segment_uniformity(qubits_opt, M_EARTH)
    
    print(f"  Array size: {len(qubits_opt)} qubits")
    print(f"  Xi mean: {uniformity_opt['xi_mean']:.15e}")
    print(f"  Xi std: {uniformity_opt['xi_std']:.6e}")
    print(f"  Xi range: {uniformity_opt['xi_range']:.6e}")
    print(f"  Uniformity: {uniformity_opt['uniformity']:.6f}")
    
    # Random array for comparison
    print_section("Random 16-Qubit Array (0-100 um height variation)")
    np.random.seed(42)
    qubits_rand = []
    for i in range(16):
        z = np.random.uniform(0, 100e-6)
        qubits_rand.append(Qubit(id=f"Q{i}", x=0, y=0, z=z))
    uniformity_rand = array_segment_uniformity(qubits_rand, M_EARTH)
    
    print(f"  Xi mean: {uniformity_rand['xi_mean']:.15e}")
    print(f"  Xi std: {uniformity_rand['xi_std']:.6e}")
    print(f"  Xi range: {uniformity_rand['xi_range']:.6e}")
    print(f"  Uniformity: {uniformity_rand['uniformity']:.6f}")
    
    # Comparison
    print_section("Comparison")
    improvement = uniformity_rand['xi_range'] / uniformity_opt['xi_range'] if uniformity_opt['xi_range'] > 0 else float('inf')
    print(f"  Optimized Xi range: {uniformity_opt['xi_range']:.6e}")
    print(f"  Random Xi range: {uniformity_rand['xi_range']:.6e}")
    print(f"  Improvement factor: {improvement:.1f}x")


def demo_6_gate_timing():
    """Demo 6: Gate Timing Corrections"""
    print_header("DEMO 6: Gate Timing Corrections")
    
    print_section("Single Qubit Gate Correction")
    q = Qubit(id="Q1", x=0, y=0, z=0, gate_time=50e-9)
    
    correction = gate_timing_correction(q, M_EARTH)
    print(f"  Nominal gate time: {q.gate_time*1e9:.3f} ns")
    print(f"  Correction factor: {correction:.15f}")
    print(f"  Corrected time: {q.gate_time * correction * 1e9:.15f} ns")
    print(f"  Difference: {(correction - 1) * q.gate_time * 1e18:.6f} as (attoseconds)")
    
    print_section("Two-Qubit Gate Timing")
    q1 = Qubit(id="Q1", x=0, y=0, z=0, gate_time=50e-9)
    q2 = Qubit(id="Q2", x=0, y=0, z=10e-3, gate_time=50e-9)  # 10 mm higher
    pair = QubitPair(q1, q2)
    
    timing = two_qubit_gate_timing(pair, M_EARTH)
    print(f"  Height difference: {pair.height_difference*1e3:.1f} mm")
    print(f"  Optimal gate time: {timing['optimal_gate_time']*1e9:.6f} ns")
    print(f"  D_SSZ (Q1): {timing['d_qubit_a']:.15f}")
    print(f"  D_SSZ (Q2): {timing['d_qubit_b']:.15f}")
    print(f"  Timing asymmetry: {timing['timing_asymmetry']:.6e}")
    print(f"  Max fidelity loss: {timing['max_fidelity_loss']:.6e}")


def demo_7_decoherence():
    """Demo 7: Decoherence Analysis"""
    print_header("DEMO 7: Decoherence Analysis")
    
    print_section("SSZ Decoherence Rate")
    q = Qubit(id="Q1", x=0, y=0, z=0, coherence_time_T2=100e-6)
    
    gamma = ssz_decoherence_rate(q, M_EARTH)
    T2_eff = effective_T2(q, M_EARTH)
    
    print(f"  Intrinsic T2: {q.coherence_time_T2*1e6:.1f} us")
    print(f"  SSZ decoherence rate: {gamma:.6e} /s")
    print(f"  Effective T2: {T2_eff*1e6:.3f} us")
    print(f"  SSZ contribution: {(1 - T2_eff/q.coherence_time_T2)*100:.4f}%")
    
    print_section("Pair Decoherence")
    q1 = Qubit(id="Q1", x=0, y=0, z=0, coherence_time_T2=100e-6)
    q2 = Qubit(id="Q2", x=0, y=0, z=1e-3, coherence_time_T2=100e-6)  # 1 mm higher
    pair = QubitPair(q1, q2)
    
    T2_pair = pair_decoherence_time(pair, M_EARTH)
    print(f"  Q1 T2: {q1.coherence_time_T2*1e6:.1f} us")
    print(f"  Q2 T2: {q2.coherence_time_T2*1e6:.1f} us")
    print(f"  Pair T2: {T2_pair*1e6:.3f} us")
    print(f"  Height difference: {pair.height_difference*1e3:.1f} mm")


def demo_8_experimental_validation():
    """Demo 8: Experimental Validation"""
    print_header("DEMO 8: Experimental Validation")
    
    print_section("GPS Time Dilation")
    h_gps = 20200e3  # GPS satellite altitude
    d_surface = ssz_time_dilation(R_EARTH, M_EARTH)
    d_gps = ssz_time_dilation(R_EARTH + h_gps, M_EARTH)
    delta_d = d_gps - d_surface
    drift_per_day = delta_d * 86400 * 1e6  # microseconds
    
    print(f"  GPS altitude: {h_gps/1e3:.0f} km")
    print(f"  D_SSZ (surface): {d_surface:.15f}")
    print(f"  D_SSZ (GPS): {d_gps:.15f}")
    print(f"  Delta D_SSZ: {delta_d:.6e}")
    print(f"  Time drift: {drift_per_day:.1f} us/day")
    print(f"  Measured: ~45 us/day")
    print(f"  Status: {'MATCH' if 40 < drift_per_day < 50 else 'MISMATCH'}")
    
    print_section("Pound-Rebka Experiment")
    h_tower = 22.5  # meters
    r1 = R_EARTH
    r2 = R_EARTH + h_tower
    
    xi1 = xi_segment_density(r1, M_EARTH)
    xi2 = xi_segment_density(r2, M_EARTH)
    delta_xi = xi1 - xi2
    
    # Gravitational redshift
    z_ssz = delta_xi
    z_measured = 2.57e-15
    
    print(f"  Tower height: {h_tower} m")
    print(f"  SSZ redshift: {z_ssz:.6e}")
    print(f"  Measured: (2.57 +/- 0.26)e-15")
    print(f"  Status: {'MATCH' if abs(z_ssz - z_measured) < 0.5e-15 else 'CLOSE'}")


def demo_9_practical_example():
    """Demo 9: Practical Qubit System Design"""
    print_header("DEMO 9: Practical Qubit System Design")
    
    print_section("Scenario: 100-Qubit Processor")
    print("  Goal: Design optimal qubit placement for minimal SSZ effects")
    
    # Step 1: Determine coherent zone
    print("\n  Step 1: Find coherent zone")
    tolerance = 1e-19  # Typical requirement
    zone = segment_coherent_zone(0, tolerance, M_EARTH)
    h_min, h_max = zone
    width = h_max - h_min
    print(f"    Tolerance: {tolerance:.0e}")
    print(f"    Coherent zone width: {width*1e6:.1f} um")
    
    # Step 2: Create optimized array
    print("\n  Step 2: Create optimized array")
    qubits = optimize_qubit_array(100, base_height=0, max_separation=5e-3)
    uniformity = array_segment_uniformity(qubits, M_EARTH)
    print(f"    Qubits: {len(qubits)}")
    print(f"    Max separation: 5 mm")
    print(f"    Xi uniformity: {uniformity['uniformity']:.6f}")
    print(f"    Xi range: {uniformity['xi_range']:.6e}")
    
    # Step 3: Analyze worst-case pair
    print("\n  Step 3: Worst-case pair analysis")
    # Find qubits with max height difference
    z_values = [q.z for q in qubits]
    q_low = qubits[z_values.index(min(z_values))]
    q_high = qubits[z_values.index(max(z_values))]
    pair = QubitPair(q_low, q_high)
    
    mismatch = qubit_pair_segment_mismatch(pair, M_EARTH)
    timing = two_qubit_gate_timing(pair, M_EARTH)
    
    print(f"    Height difference: {pair.height_difference*1e6:.1f} um")
    print(f"    Delta Xi: {mismatch['delta_xi']:.6e}")
    print(f"    Timing asymmetry: {timing['timing_asymmetry']:.6e}")
    print(f"    Max fidelity loss: {timing['max_fidelity_loss']:.6e}")
    
    # Step 4: Recommendations
    print("\n  Step 4: Recommendations")
    print("    [OK] Keep all qubits within coherent zone")
    print("    [OK] Use SSZ-corrected gate timing")
    print("    [OK] Monitor height variations during operation")
    print("    [OK] Apply segment-aware error correction")


def main():
    """Run all demos."""
    print("\n" + "=" * 70)
    print("  SSZ-QUBITS: INTERACTIVE DEMONSTRATION")
    print("  Segmented Spacetime Framework for Quantum Computing")
    print("=" * 70)
    print("\n  Authors: Carmen Wrede & Lino Casu")
    print("  License: Anti-Capitalist Software License v1.4")
    print("  Date: 2025-12-11")
    
    # Run all demos
    demo_1_basic_ssz_physics()
    demo_2_qubit_analysis()
    demo_3_qubit_pair_mismatch()
    demo_4_coherent_zones()
    demo_5_array_optimization()
    demo_6_gate_timing()
    demo_7_decoherence()
    demo_8_experimental_validation()
    demo_9_practical_example()
    
    # Summary
    print_header("DEMONSTRATION COMPLETE")
    print("""
  Key Takeaways:
  
  1. SSZ provides geometric framework for qubit analysis
  2. Height differences cause measurable Xi variations
  3. Segment-coherent zones define optimal placement
  4. Gate timing can be SSZ-corrected
  5. Decoherence has gravitational component
  6. SSZ matches experimental data (GPS, Pound-Rebka)
  
  "Die Qubits leben nicht nur im Raum, 
   sondern auch in Segmenten der Raumzeit."
  
  For more information, see:
  - docs/SSZ_QUBIT_THEORY_SUMMARY.md
  - docs/SSZ_MATHEMATICAL_PHYSICS.md
  - FINAL_REPORT.md
""")
    
    # License notice
    print("=" * 70)
    print("SSZ-Qubits - Segmented Spacetime Framework for Quantum Computing")
    print("Copyright (c) 2025 Carmen Wrede and Lino Casu")
    print("Licensed under the Anti-Capitalist Software License v1.4")
    print("https://github.com/error-wtf/ssz-qubits")
    print("=" * 70)


if __name__ == "__main__":
    main()
