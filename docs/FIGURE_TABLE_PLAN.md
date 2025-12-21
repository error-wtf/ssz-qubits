# SSZ Paper Suite: Figure & Table Plan

**Version:** 1.0  
**Date:** 2025-12-21  
**Authors:** Carmen Wrede & Lino Casu

---

## Overview

This document specifies all figures and tables for the unified SSZ paper suite, including data sources, generation scripts, and quality requirements.

---

## Paper D (Master Document) - 7 Figures

### Figure D.1: Local vs Global Phase Comparison
**Purpose:** Address equivalence principle objection; show SSZ emerges from comparing separated systems  
**Type:** Conceptual diagram  
**Elements:**
- Left panel: "LOCAL FRAME" - single clock, t = t' always
- Right panel: "GLOBAL COMPARISON" - two separated clocks, Δt accumulates
- Key insight box: "SSZ is NOT local — it emerges from comparing phase evolution at different Ξ(r)"

**Source:** `generate_paper_d_master_plots.py::fig1_local_vs_global()`  
**Output:** `outputs/paper_d_fig1_local_vs_global.png`

---

### Figure D.2: Phase Shift vs Height Difference
**Purpose:** Show linear scaling ΔΦ ∝ Δh (slope=1 on log-log)  
**Type:** Log-log plot  
**Elements:**
- X-axis: Δh [m] (10⁻⁴ to 10³)
- Y-axis: ΔΦ [rad] (10⁻²⁰ to 10¹)
- Orange line: Transmon (5 GHz, 100 μs)
- Green line: Optical clock (429 THz, 1 s)
- Gray dashed: Slope=1 reference
- Red dashed: Detection threshold (~1 rad)
- Shaded regions: "On-chip regime" (yellow), "Tower/remote regime" (green)
- Annotation: Optical clock @ 1m = 0.59 rad (detectable!)

**Data Source:** Calculated from ΔΦ = ω × (r_s × Δh / R²) × t  
**Source:** `generate_paper_d_master_plots.py::fig2_phase_vs_height()`  
**Output:** `outputs/paper_d_fig2_phase_vs_height.png`

---

### Figure D.3: Scaling Laws (ω and t)
**Purpose:** Demonstrate linear scaling with frequency and time  
**Type:** Dual panel plot  
**Elements:**
- Left panel: ΔΦ vs ω at fixed Δh, t
- Right panel: ΔΦ vs t at fixed Δh, ω
- Both show slope=1 on log-log

**Data Source:** Calculated from ΔΦ = ω × ΔD × t  
**Source:** `generate_paper_d_master_plots.py::fig3_scaling_omega_t()`  
**Output:** `outputs/paper_d_fig3_scaling.png`

---

### Figure D.4: Platform Feasibility Comparison
**Purpose:** Show why optical clocks are gold standard  
**Type:** Bar chart  
**Elements:**
- X-axis: Platform configurations
- Y-axis: |ΔΦ| [rad] (log scale)
- Red bars: Transmon (on-chip, 5° tilt, 1m remote) - "BOUND REGIME"
- Green bars: Optical (1m, 10m, 100m) - "DETECTION REGIME"
- Horizontal lines: Detection threshold (~1 rad), Good SNR (~0.1 rad)
- Labels: "No" / "Yes" for each bar
- Annotations: Required N for SNR=3

**Data Source:** Verified calculations from paper_suite_integrator.py  
**Source:** `generate_paper_d_master_plots.py::fig4_platform_feasibility()`  
**Output:** `outputs/paper_d_fig4_feasibility.png`

---

### Figure D.5: Experimental Setup Configurations
**Purpose:** Show hardware options for Δh generation  
**Type:** Schematic diagram (3 panels)  
**Elements:**
- Panel A: "Chip Tilt" - tilted chip with angle θ, formula Δh = L×sin(θ)
- Panel B: "Remote Entanglement" - two refrigerators at different heights
- Panel C: "3D Chiplet Stack" - vertically stacked chips with TSVs

**Source:** `generate_paper_d_master_plots.py::fig5_experimental_setups()`  
**Output:** `outputs/paper_d_fig5_setups.png`

---

### Figure D.6: Confound Discrimination Matrix
**Purpose:** Show how SSZ signature differs from confounds  
**Type:** Table/matrix visualization  
**Elements:**
- Rows: SSZ, Temperature, LO noise, Vibration, EM crosstalk
- Columns: Δh scaling, ω scaling, t scaling, Randomization response
- Color coding: Green (linear), Yellow (weak/none), Red (varies)
- Key insight: SSZ is LINEAR in all three + INVARIANT under randomization

**Source:** `generate_paper_d_master_plots.py::fig6_confound_matrix()`  
**Output:** `outputs/paper_d_fig6_confounds.png`

---

### Figure D.7: Claim Taxonomy
**Purpose:** Clear visual of what SSZ claims vs doesn't claim  
**Type:** Three-column layout  
**Elements:**
- Column 1 (Pink): "BOUNDED TODAY" - Transmon/mm, upper bound, null=SSZ-consistent
- Column 2 (Yellow): "DETECTABLE SOON" - Optical clocks/m-scale, 0.3-3 rad, direct test
- Column 3 (Green): "ENGINEERING RELEVANCE" - Future QC, distributed networks, compensation needed

**Source:** `generate_paper_d_master_plots.py::fig7_claim_taxonomy()`  
**Output:** `outputs/paper_d_fig7_taxonomy.png`

---

## Paper D - Tables

### Table D.1: Symbol Definitions
| Symbol | Definition | Units |
|--------|------------|-------|
| Ξ(r) | Segment density | - |
| D_SSZ(r) | Time dilation factor | - |
| ΔD | Differential time dilation | - |
| ω | Angular frequency | rad/s |
| t | Integration time | s |
| Δh | Height difference | m |
| ΔΦ | Phase drift | rad |
| r_s | Schwarzschild radius | m |
| R | Earth radius | m |

---

### Table D.2: Verified Constants
| Constant | Value | Unit |
|----------|-------|------|
| r_s (Earth) | 8.870×10⁻³ | m |
| R (Earth) | 6.371×10⁶ | m |
| φ (Golden ratio) | 1.618034 | - |

---

### Table D.3: Phase Drift Predictions
| Platform | f | Δh | t | ΔΦ | Detectable? |
|----------|---|-----|---|-----|-------------|
| Transmon | 5 GHz | 1 mm | 100 μs | 6.9×10⁻¹³ rad | No |
| Transmon | 5 GHz | 1 m | 100 μs | 6.9×10⁻¹⁰ rad | No |
| Optical | 429 THz | 1 m | 1 s | 0.59 rad | **Yes** |

---

### Table D.4: Platform Comparison
| Parameter | Transmon | Optical Clock | Ratio |
|-----------|----------|---------------|-------|
| Frequency | 5 GHz | 429 THz | 8.6×10⁴ |
| Coherence | 100 μs | 1 s | 10⁴ |
| ΔΦ @ 1m | 6.9×10⁻¹⁰ rad | 0.59 rad | 8.6×10⁸ |
| Feasible? | No | **Yes** | - |

---

### Table D.5: Coherent Zone Widths
| Tolerance ε | z(ε) | Interpretation |
|-------------|------|----------------|
| 10⁻¹⁸ | 18 mm | Ultracoherent |
| 10⁻¹⁵ | 18 m | Standard QC |
| 10⁻¹² | 18 km | Global networks |

---

### Table D.6: Confound Signatures
| Source | Δh | ω | t | Randomization |
|--------|-----|---|---|---------------|
| **SSZ** | **Linear** | **Linear** | **Linear** | **Invariant** |
| Temperature | Correlates | Weak | Non-linear | Varies |
| LO noise | None | None | √t | Varies |
| Vibration | Correlated | None | AC | Varies |

---

## Paper C - Figures

### Figure C.1: Platform Feasibility
**Reuse:** Paper D Figure D.4  
**Location:** `outputs/paper_d_fig4_feasibility.png`

### Figure C.2: Chip Tilt Geometry
**Purpose:** Show Δh = L×sin(θ) relationship  
**Source:** `generate_paper_c_final_plots.py::fig2_chip_tilt()`  
**Output:** `outputs/paper_c_final_fig2_tilt.png`

### Figure C.3: Statistical Framework
**Purpose:** Show M₀, M_SSZ, M_anom model comparison  
**Source:** `generate_paper_c_final_plots.py::fig3_statistics()`  
**Output:** `outputs/paper_c_final_fig3_statistics.png`

### Figure C.4: Confound Signatures
**Reuse:** Paper D Figure D.6  
**Location:** `outputs/paper_d_fig6_confounds.png`

---

## Paper A/B - Figures

Papers A and B retain their original conceptual figures but add:

### Figure A/B.X: Feasibility Context (NEW)
**Purpose:** Show where current experiments sit on the feasibility landscape  
**Recommendation:** Reference Paper D Figure D.4 or include simplified version

---

## Data Sources & Reproducibility

### Python Scripts
| Script | Figures Generated |
|--------|-------------------|
| `generate_paper_d_master_plots.py` | D.1 - D.7 |
| `generate_paper_c_final_plots.py` | C.1 - C.6 |
| `paper_suite_integrator.py` | Numerical verification |

### Reproduction Commands
```bash
cd E:\clone\ssz-qubits

# Generate all Paper D figures
python generate_paper_d_master_plots.py

# Generate all Paper C figures
python generate_paper_c_final_plots.py

# Verify all numerical values
python paper_suite_integrator.py
```

### Output Directory
All figures saved to: `E:\clone\ssz-qubits\outputs\`

---

## Quality Requirements

### Resolution
- **Print:** 300 DPI minimum
- **Format:** PNG (raster) or PDF (vector)

### Fonts
- **Primary:** Arial or Helvetica
- **Math:** LaTeX-rendered where possible

### Colors
- **Consistent palette** across all figures
- **Colorblind-friendly** alternatives available

### Annotations
- All axes labeled with units
- Legend present where needed
- Key values annotated directly on plot

---

## Figure Checklist

| Figure | Generated | Verified | In Paper |
|--------|-----------|----------|----------|
| D.1 Local vs Global | ✓ | ✓ | ✓ |
| D.2 Phase vs Height | ✓ | ✓ | ✓ |
| D.3 Scaling Laws | ✓ | ✓ | ✓ |
| D.4 Platform Feasibility | ✓ | ✓ | ✓ |
| D.5 Experimental Setups | ✓ | ✓ | ✓ |
| D.6 Confound Matrix | ✓ | ✓ | ✓ |
| D.7 Claim Taxonomy | ✓ | ✓ | ✓ |
| C.1 Platform | ✓ | ✓ | ✓ |
| C.2 Chip Tilt | ✓ | ✓ | ✓ |
| C.3 Statistics | ✓ | ✓ | ✓ |
| C.4 Confounds | ✓ | ✓ | ✓ |

### NEW: Supplementary Figures (2025-12-21)

| Figure | Generated | Purpose | File |
|--------|-----------|---------|------|
| S.1 Strong Field SSZ vs GR | ✓ | Singularity resolution proof | `fig_strong_field_ssz_vs_gr.png` |
| S.2 Validation Summary | ✓ | GPS/Pound-Rebka/NIST/Skytree | `fig_validation_summary.png` |
| S.3 φ-Geometry | ✓ | Why golden ratio matters | `fig_phi_geometry.png` |
| S.4 Coherent Zone Scaling | ✓ | Zone width vs tolerance ε | `fig_coherent_zone_scaling.png` |
| S.5 Time Drift Accumulation | ✓ | Phase drift over time/gates | `fig_time_drift_accumulation.png` |
| S.6 Qubit Height Sensitivity | ✓ | ΔΞ maps + sensitivity table | `fig_qubit_height_sensitivity.png` |

**Generation Script:** `generate_improved_plots.py`

---

© 2025 Carmen Wrede & Lino Casu  
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
