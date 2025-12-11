# SSZ-Qubits: Segmented Spacetime Framework for Quantum Computing

[![License: ACSL](https://img.shields.io/badge/License-Anti--Capitalist-red.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Tests: 74/74](https://img.shields.io/badge/Tests-74%2F74%20Passed-brightgreen.svg)](tests/)

## Overview

**SSZ-Qubits** applies the Segmented Spacetime (SSZ) framework to quantum computing, providing tools to analyze and mitigate gravitational effects on qubit systems.

> **"Die Qubits leben nicht nur im Raum, sondern auch in Segmenten der Raumzeit."**

### The Problem

Qubits are extremely sensitive to:
- **Decoherence**: Loss of quantum coherence from environmental fluctuations
- **Timing Errors**: Synchronization issues in gate operations
- **Spatial Drift**: Position-dependent phase errors
- **Gravitational Gradients**: Height-dependent time dilation effects

### The SSZ Solution

SSZ provides a geometric framework where:
- **Segment Density Xi(r)** quantifies local spacetime structure
- **Time Dilation D_SSZ = 1/(1+Xi)** determines local clock rates
- **Segment-Coherent Zones** define optimal qubit placement regions
- **Geometry-Aware QEC** enables gravitationally-informed error correction
- **Golden Ratio phi** governs segment saturation in strong fields

## Key Equations

### Segment Density
```
Xi(r) = r_s / (2r) = GM / (c^2 * r)
```

### SSZ Time Dilation
```
D_SSZ = 1 / (1 + Xi)
```

### Segment Gradient
```
dXi/dr = -r_s / (2r^2)
```

## Installation

```bash
# Clone repository
git clone https://github.com/error-wtf/ssz-qubits.git
cd ssz-qubits

# Install dependencies
pip install -r requirements.txt

# Run tests
python run_tests.py
```

## Quick Start

```python
from ssz_qubits import (
    Qubit, QubitPair, 
    analyze_qubit_segment, 
    qubit_pair_segment_mismatch,
    ssz_time_dilation
)

# Create qubits at different heights
q1 = Qubit(id="Q1", x=0, y=0, z=0)        # Sea level
q2 = Qubit(id="Q2", x=0, y=0, z=0.01)     # 1 cm higher

# Analyze segment properties
analysis = analyze_qubit_segment(q1)
print(f"Xi = {analysis.xi:.6e}")
print(f"D_SSZ = {analysis.time_dilation:.15f}")

# Analyze pair mismatch
pair = QubitPair(q1, q2)
mismatch = qubit_pair_segment_mismatch(pair)
print(f"Delta Xi = {mismatch['delta_xi']:.6e}")
print(f"Phase drift/gate = {mismatch['phase_drift_per_gate']:.6e} rad")
```

## Features

### Core Physics
- **Schwarzschild radius calculation**
- **Segment density Xi(r)**
- **SSZ time dilation D_SSZ**
- **Segment gradient dXi/dr**

### Qubit Analysis
- **Single qubit segment analysis**
- **Qubit pair mismatch calculation**
- **Optimal height determination**
- **Segment-coherent zone calculation**

### Gate Timing
- **Gate timing corrections**
- **Two-qubit gate optimization**
- **Timing asymmetry compensation**

### Decoherence Modeling
- **SSZ-enhanced decoherence rates**
- **Effective T2 calculation**
- **Pair decoherence time**

### Array Optimization
- **Optimal qubit array placement**
- **Segment uniformity analysis**
- **Geometry-aware QEC support**

## Test Suite

The test suite includes **74 tests** covering:

### Physics Tests (`test_ssz_physics.py`)
- Schwarzschild radius validation
- Segment density calculations
- Time dilation verification
- Gradient consistency
- Physical limits

### Edge Cases (`test_edge_cases.py`)
- Extreme radii (near r_s to 1 AU)
- Extreme masses (0 to black holes)
- Unusual qubit configurations
- Numerical precision
- Error handling

### Validation (`test_validation.py`)
- GR weak-field comparison
- GPS satellite time dilation
- Pound-Rebka experiment
- NIST optical clock
- Tokyo Skytree experiment
- Theoretical consistency

### Qubit Applications (`test_ssz_qubit_applications.py`)
- Segmented time logic as qubit clock
- Decoherence as geometry phenomenon
- Gravitational drift prediction
- Segment-aware QEC
- Quantum communication sync

## Run Tests

```bash
# Run all tests with detailed output
python run_tests.py

# Run specific test file
python tests/test_ssz_physics.py

# Run with pytest
pytest tests/ -v -s
```

## Visualization

```bash
# Generate all plots
python visualize_ssz_qubits.py
```

Generates:
- `time_dilation_vs_height.png` - SSZ effects vs altitude
- `qubit_pair_mismatch.png` - Mismatch analysis
- `coherent_zone.png` - Optimal placement zones
- `qubit_array_analysis.png` - Array optimization
- `ssz_vs_gr_comparison.png` - SSZ vs GR comparison
- `golden_ratio_structure.png` - Phi in SSZ framework

## Physical Results

### At Earth's Surface
- **Xi ~ 7×10^-10** (weak field)
- **D_SSZ ~ 1 - 7×10^-10**
- **Time offset: ~0.1 ps/s per meter height**

### For Qubits
- **1 cm height difference**: Delta Xi ~ 10^-18
- **1 mm height difference**: Delta Xi ~ 10^-19
- **Phase drift**: Scales linearly with height difference

### Validation
- Matches GR in weak field to O(Xi^2)
- Reproduces GPS time dilation (~45 μs/day)
- Consistent with Pound-Rebka experiment
- Agrees with NIST optical clock measurements

## Project Structure

```
ssz-qubits/
├── ssz_qubits.py               # Core module (933 lines)
├── demo.py                     # Interactive demonstration
├── run_tests.py                # Test runner
├── visualize_ssz_qubits.py     # Visualization
├── requirements.txt            # Dependencies
├── README.md                   # This file
├── FINAL_REPORT.md             # Complete project report
├── docs/
│   ├── SSZ_FORMULA_DOCUMENTATION.md
│   ├── SSZ_MATHEMATICAL_PHYSICS.md
│   ├── SSZ_QUBIT_APPLICATIONS.md
│   └── SSZ_QUBIT_THEORY_SUMMARY.md
├── tests/
│   ├── test_ssz_physics.py         # 17 physics tests
│   ├── test_edge_cases.py          # 25 edge case tests
│   ├── test_validation.py          # 17 validation tests
│   └── test_ssz_qubit_applications.py  # 15 application tests
├── outputs/                    # Generated plots (6 visualizations)
└── reports/                    # Test reports
```

## Applications

1. **Qubit Placement Optimization**
   - Minimize SSZ mismatch between qubits
   - Define segment-coherent zones

2. **Gate Timing Correction**
   - Compensate for height-dependent time dilation
   - Optimize two-qubit gate timing

3. **Decoherence Prediction**
   - Model SSZ contribution to decoherence
   - Identify optimal operating conditions

4. **Geometry-Aware QEC**
   - Segment-aware syndrome weights
   - Gravitationally-informed error correction

## References

- Casu & Wrede, "Segmented Spacetime" (2025)
- Pound & Rebka, "Apparent Weight of Photons" (1960)
- NIST Optical Clock Experiments (2010)
- GPS Relativistic Corrections

## Authors

**Carmen Wrede** & **Lino Casu**

## License

Licensed under the **Anti-Capitalist Software License v1.4**

© 2025 Carmen Wrede, Lino Casu
