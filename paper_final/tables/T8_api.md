# Table 8: SSZ-Qubits API Reference

## Constants

| Name | Value | Unit | Description |
|------|-------|------|-------------|
| `C` | 2.998×10⁸ | m/s | Speed of light |
| `G` | 6.674×10⁻¹¹ | m³/(kg·s²) | Gravitational constant |
| `HBAR` | 1.055×10⁻³⁴ | J·s | Reduced Planck constant |
| `PHI` | 1.618... | - | Golden ratio |
| `M_EARTH` | 5.972×10²⁴ | kg | Earth mass |
| `R_EARTH` | 6.371×10⁶ | m | Earth radius |

## Core Functions

| Function | Signature | Returns | Description |
|----------|-----------|---------|-------------|
| `schwarzschild_radius` | `(M)` | float [m] | r_s = 2GM/c² |
| `xi_segment_density` | `(r, M, regime='auto')` | float | Ξ(r) segment density |
| `ssz_time_dilation` | `(r, M)` | float | D = 1/(1+Ξ) |
| `differential_time_dilation` | `(delta_h, M, R)` | float | ΔD = r_s·Δh/R² |
| `phase_drift` | `(omega, delta_h, t, M, R)` | float [rad] | ΔΦ = ω·ΔD·t |
| `zone_width` | `(epsilon, M, R)` | float [m] | z = 4ε·R²/r_s |

## Classes

### Qubit

| Attribute | Type | Description |
|-----------|------|-------------|
| `frequency` | float | Qubit frequency [Hz] |
| `omega` | float | Angular frequency [rad/s] |
| `height` | float | Height above reference [m] |
| `coherence_time` | float | T₂ time [s] |
| `name` | str | Identifier |

| Method | Signature | Returns | Description |
|--------|-----------|---------|-------------|
| `analyze_ssz` | `(M, R)` | dict | Full SSZ analysis |

### QubitPair

| Attribute | Type | Description |
|-----------|------|-------------|
| `q1`, `q2` | Qubit | The two qubits |
| `delta_h` | float | Height difference [m] |

| Method | Signature | Returns | Description |
|--------|-----------|---------|-------------|
| `phase_drift` | `(time, M, R)` | float | Phase drift [rad] |
| `compensation_phase` | `(time, M, R)` | float | Required correction [rad] |

## Validation Functions

| Function | Returns | Tests |
|----------|---------|-------|
| `validate_gps()` | dict | GPS ~38 μs/day |
| `validate_pound_rebka()` | dict | 22.5 m tower |

## Quick Examples

```python
# Import
from ssz_qubits import *

# Calculate phase drift
dphi = phase_drift(omega=2*np.pi*5e9, delta_h=1e-3, t=100e-6)
# Returns: 6.87e-13 rad

# Create qubit pair
q1 = Qubit(frequency=5e9, height=0)
q2 = Qubit(frequency=5e9, height=0.001)
pair = QubitPair(q1, q2)
drift = pair.phase_drift(100e-6)
# Returns: 6.87e-13 rad

# Zone width
z = zone_width(1e-18)
# Returns: 1.83e-4 m (183 μm)

# Validate
result = validate_gps()
print(result['pass'])  # True
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `ValueError` | r ≤ 0 | Use positive radius |
| `ValueError` | M ≤ 0 | Use positive mass |
| `RuntimeWarning` | r < r_s in weak field | Use regime='strong' |

## Performance

| Operation | Time (single) | Time (10⁶ array) |
|-----------|---------------|------------------|
| `schwarzschild_radius` | 0.1 μs | 10 ms |
| `xi_segment_density` | 0.5 μs | 50 ms |
| `phase_drift` | 0.3 μs | 30 ms |

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| numpy | ≥1.20 | Array operations |
| scipy | ≥1.7 | (Optional) Statistics |
| matplotlib | ≥3.4 | (Optional) Plotting |

## Installation

```bash
# From source
git clone https://github.com/error-wtf/ssz-qubits.git
cd ssz-qubits
pip install -e .

# Or direct import
# Just copy ssz_qubits.py to your project
```

## Usage in DOCX
```python
# Format as code documentation
# Syntax highlighting for examples
# Split into multiple sub-tables
```
