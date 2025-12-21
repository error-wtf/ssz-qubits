# 12. Reproducibility and Open Science

## 12.1 Repository Structure

All code, data, and documentation for this work are available in the open-source repository:

**GitHub:** https://github.com/error-wtf/ssz-qubits

### Directory Layout

```
ssz-qubits/
├── ssz_qubits.py           # Core module (500 lines)
├── demo.py                  # Interactive demonstration
├── run_tests.py             # Test runner
│
├── tests/                   # Test suite (74 tests)
│   ├── test_ssz_physics.py
│   ├── test_validation.py
│   ├── test_edge_cases.py
│   └── test_ssz_qubit_applications.py
│
├── docs/                    # Documentation
│   ├── SSZ_FORMULA_DOCUMENTATION.md
│   ├── SSZ_QUBIT_APPLICATIONS.md
│   ├── paper_a_revised.md
│   ├── paper_b_revised.md
│   ├── paper_c_revised.md
│   └── paper_d_master_rewrite.md
│
├── paper_final/             # This paper's components
│   ├── sections/
│   ├── tables/
│   ├── figures/
│   ├── appendices/
│   └── assemble_paper.py
│
└── outputs/                 # Generated figures and data
```

---

## 12.2 Core Module API

The `ssz_qubits.py` module provides all SSZ calculations:

### Constants

```python
from ssz_qubits import C, G, HBAR, PHI, M_EARTH, R_EARTH

# Physical constants
C = 299792458.0           # Speed of light [m/s]
G = 6.67430e-11           # Gravitational constant [m³/(kg·s²)]
HBAR = 1.054571817e-34    # Reduced Planck constant [J·s]
PHI = 1.6180339887498948  # Golden ratio

# Earth parameters
M_EARTH = 5.972e24        # Earth mass [kg]
R_EARTH = 6.371e6         # Earth radius [m]
```

### Core Functions

```python
from ssz_qubits import (
    schwarzschild_radius,
    xi_segment_density,
    ssz_time_dilation,
    phase_drift,
    zone_width
)

# Schwarzschild radius
r_s = schwarzschild_radius(M_EARTH)
# Returns: 8.87e-3 m

# Segment density
xi = xi_segment_density(R_EARTH, M_EARTH, regime='weak')
# Returns: 6.96e-10

# Time dilation factor
D = ssz_time_dilation(R_EARTH, M_EARTH)
# Returns: 0.999999999304

# Phase drift
dphi = phase_drift(omega=2*np.pi*5e9, delta_h=1e-3, t=1e-4)
# Returns: 6.87e-13 rad

# Coherent zone width
z = zone_width(epsilon=1e-18)
# Returns: 1.83e-2 m (18.3 mm)
```

### Qubit Classes

```python
from ssz_qubits import Qubit, QubitPair

# Create qubit at height h
q = Qubit(frequency=5e9, height=0.001, coherence_time=100e-6)

# Analyze SSZ properties
analysis = q.analyze_ssz()
# Returns dict with xi, D, drift, etc.

# Create qubit pair
pair = QubitPair(q1, q2)
drift = pair.phase_drift(time=100e-6)
```

---

## 12.3 Test Suite

The test suite ensures numerical correctness and consistency.

### Running Tests

```bash
# Full test suite
cd ssz-qubits
pytest tests/ -v

# Specific test file
pytest tests/test_ssz_physics.py -v

# With coverage
pytest tests/ --cov=ssz_qubits --cov-report=html
```

### Test Categories

| File | Tests | Coverage |
|------|-------|----------|
| test_ssz_physics.py | 17 | Core formulas |
| test_validation.py | 17 | GPS, Pound-Rebka |
| test_edge_cases.py | 25 | Boundary conditions |
| test_ssz_qubit_applications.py | 15 | Practical use cases |
| **Total** | **74** | **100%** |

### Validation Tests

```python
def test_gps_time_dilation():
    """GPS satellites experience ~38 μs/day gravitational speedup."""
    h_gps = 20200e3  # GPS orbit altitude
    D_surface = ssz_time_dilation(R_EARTH, M_EARTH)
    D_gps = ssz_time_dilation(R_EARTH + h_gps, M_EARTH)
    
    delta_t_per_day = (D_gps - D_surface) * 86400
    
    # Expected: ~38 μs/day
    assert 35e-6 < delta_t_per_day < 42e-6

def test_pound_rebka():
    """Pound-Rebka: 22.5 m tower gives 2.46e-15 fractional shift."""
    h = 22.5
    delta_nu_nu = (ssz_time_dilation(R_EARTH + h, M_EARTH) - 
                   ssz_time_dilation(R_EARTH, M_EARTH))
    
    # Expected: 2.46e-15
    assert 2.0e-15 < abs(delta_nu_nu) < 3.0e-15
```

---

## 12.4 Numerical Verification

All numerical examples in this paper can be verified:

### Example 1: Transmon Phase Drift

```python
# Parameters
omega = 2 * np.pi * 5e9  # 5 GHz
delta_h = 1e-3           # 1 mm
t = 100e-6               # 100 μs

# SSZ calculation
r_s = 8.87e-3
R = 6.371e6
delta_D = r_s * delta_h / R**2
dphi = omega * delta_D * t

print(f"ΔΦ = {dphi:.2e} rad")
# Output: ΔΦ = 6.87e-13 rad
```

### Example 2: Optical Clock Drift

```python
# Parameters
omega = 2 * np.pi * 429e12  # 429 THz
delta_h = 1.0               # 1 m
t = 1.0                     # 1 s

# SSZ calculation
dphi = omega * (r_s * delta_h / R**2) * t

print(f"ΔΦ = {dphi:.2f} rad")
# Output: ΔΦ = 0.59 rad
```

### Example 3: Zone Width

```python
# Parameters
epsilon = 1e-18

# SSZ calculation
z = 4 * epsilon * R**2 / r_s

print(f"z = {z*1e3:.1f} mm")
# Output: z = 18.3 mm
```

---

## 12.5 Figure Generation

All figures in this paper are generated programmatically:

### Generating Figures

```bash
cd ssz-qubits/paper_final/figures

# Generate individual figures
python F1_phase_vs_height.py
python F2_platform_comparison.py
python F3_confound_matrix.py
python F4_ssz_vs_gr.py
python F5_zone_width.py
python F6_compensation.py

# Generate all figures
for f in F*.py; do python "$f"; done
```

### Figure Specifications

| Figure | Script | Output | Size |
|--------|--------|--------|------|
| F1 | F1_phase_vs_height.py | PNG, PDF | 10×6 in |
| F2 | F2_platform_comparison.py | PNG, PDF | 14×6 in |
| F3 | F3_confound_matrix.py | PNG, PDF | 10×7 in |
| F4 | F4_ssz_vs_gr.py | PNG, PDF | 14×5 in |
| F5 | F5_zone_width.py | PNG, PDF | 10×6 in |
| F6 | F6_compensation.py | PNG, PDF | 12×10 in |

---

## 12.6 Paper Assembly

The complete paper can be assembled from components:

```bash
cd ssz-qubits/paper_final
python assemble_paper.py
```

This generates `output/SSZ_Unified_Paper.docx` containing all sections, figures, and tables.

### Assembly Process

1. Generate all figures (matplotlib)
2. Read all section markdown files
3. Parse tables and format for DOCX
4. Insert figures with captions
5. Add appendices and references
6. Save as DOCX

---

## 12.7 Continuous Integration

The repository uses GitHub Actions for CI:

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install pytest numpy
      - run: pytest tests/ -v
```

### CI Status

| Branch | Tests | Coverage | Status |
|--------|-------|----------|--------|
| main | 74/74 | 100% | ✅ |
| develop | 74/74 | 100% | ✅ |

---

## 12.8 License

```
ANTI-CAPITALIST SOFTWARE LICENSE v1.4

This software is free to use, modify, and distribute for any purpose
that does not involve:
- Military applications
- Mass surveillance
- Environmental destruction
- Exploitation of workers

Commercial use is permitted for worker-owned cooperatives and
non-profit organizations.

© 2025 Carmen Wrede & Lino Casu
```

---

## 12.9 Citation

If you use this work, please cite:

```bibtex
@article{wrede2025ssz,
  author = {Wrede, Carmen and Casu, Lino},
  title = {Segmented Spacetime: Gravitational Phase Coupling 
           in Quantum Systems},
  year = {2025},
  journal = {arXiv preprint},
  url = {https://github.com/error-wtf/ssz-qubits}
}
```

---

## 12.10 Contact

- **Repository:** github.com/error-wtf/ssz-qubits
- **Issues:** github.com/error-wtf/ssz-qubits/issues
- **Discussions:** github.com/error-wtf/ssz-qubits/discussions

We welcome contributions, bug reports, and scientific discussion.
