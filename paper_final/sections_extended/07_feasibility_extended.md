# 7. Feasibility Landscape — Extended Version

## 7.5 Path to Detection — Detailed Institutional Roadmap

Realizing a definitive SSZ detection experiment requires coordination among several research institutions with complementary capabilities. This section provides a detailed analysis of necessary steps, resources, and potential partnerships.

### 7.5.1 NIST Boulder: Primary Candidate for First Detection

The National Institute of Standards and Technology in Boulder, Colorado, has the world's most advanced optical atomic clocks and is the natural candidate for the first SSZ compensation experiment.

**Existing Infrastructure:**

NIST operates multiple strontium and ytterbium clocks with fractional instability below 10⁻¹⁸. The laboratories are housed in a multi-story building, enabling height differences of 1–10 m without additional construction.

The Jun Ye group (JILA/NIST) has already conducted experiments with vertical clock comparisons, including the groundbreaking work by Chou et al. (2010) that demonstrated gravitational redshift at 33 cm. Technical expertise for precise height measurements and clock comparisons is thus available.

**Required Extensions:**

For a complete SSZ compensation experiment, the following extensions are necessary:

1. **Active phase correction hardware:** A system for real-time application of the SSZ compensation phase Φ_corr must be integrated into the clock control loop. This requires:
   - Acousto-optic modulators (AOM) with mrad phase precision
   - FPGA-based control logic for < 1 μs latency
   - Software integration into existing clock management system

2. **Precision height measurement:** Current height knowledge between laboratory rooms must be improved from ~10 cm to ~1 mm. This requires:
   - Differential leveling by surveyors
   - Installation of permanent height reference points
   - Periodic revalidation (annually)

3. **Data analysis pipeline:** A dedicated software system for analyzing with/without comparisons:
   - Automated data acquisition and storage
   - Statistical analysis following the M₀/M_SSZ/M_anom framework
   - Visualization and reporting

**Estimated Resources:**

| Item | Cost | Timeframe |
|--------|--------|------------|
| Hardware modifications | $150,000 | 6 months |
| Height surveying | $20,000 | 1 month |
| Personnel (2 postdocs, 1 year) | $200,000 | 12 months |
| Measurement campaign | $30,000 | 6 months |
| Data analysis, publication | $50,000 | 6 months |
| **Total** | **~$450,000** | **18-24 months** |

**Expected Results:**

- First definitive demonstration of SSZ compensation
- Quantitative confirmation: Drift without compensation = 0.59 ± 0.01 rad/m/s
- Verification of compensation reversal to < 1% residual
- Publication in Nature Physics or Physical Review Letters

### 7.5.2 PTB Braunschweig: European Validation

The Physikalisch-Technische Bundesanstalt in Braunschweig is the German national metrology institute and also operates world-class optical clock laboratories.

**Particular Strengths:**

PTB has pioneered fiber connections between remote clocks, with stable links over hundreds of kilometers. This expertise is valuable for future network experiments.

The PTB campus includes multiple buildings at different heights, including a historical tower that could enable height differences of > 30 m.

**Complementary Contributions:**

- Independent replication of NIST results
- Expertise in long-distance fiber links for future network SSZ
- European reference measurement for international consistency

**Estimated Resources:**

| Item | Cost | Timeframe |
|--------|--------|------------|
| Tower-to-laboratory fiber link | €100,000 | 6 months |
| Clock modifications | €80,000 | 3 months |
| Personnel | €150,000 | 12 months |
| **Total** | **~€330,000** | **15-18 months** |

### 7.5.3 RIKEN/Tokyo: Asian Perspective

The RIKEN Institute and the University of Tokyo have conducted optical clock experiments at Tokyo Skytree (Δh = 450 m), representing the largest terrestrial height difference for clock comparisons.

**Unique Opportunities:**

- Extreme height difference: 450 m offers ΔΦ ~ 260 rad/s
- Already established infrastructure (Skytree experiments)
- Possibility for precision tests of height scaling

**Challenges:**

- Long fiber distance increases noise contributions
- Environmental conditions (tourism, vibrations)
- Coordination between academic and commercial interests

**Potential Contributions:**

- Highest-SNR measurement of SSZ drift
- Test of linearity over large Δh range
- Demonstration of compensation under extreme conditions

### 7.5.4 Multi-Institutional Coordination

A complete validation program should involve multiple institutions:

```
Phase 1: Individual Laboratories (2025-2026)
├── NIST: First detection
├── PTB: Replication
└── RIKEN: Extreme Δh test

Phase 2: Bilateral Comparisons (2027-2028)
├── NIST-PTB comparison via satellite (GPS common-view)
├── PTB-SYRTE comparison via fiber
└── Consistency check of SSZ parameters

Phase 3: Global Network (2029-2030)
├── BIPM-coordinated measurement campaign
├── Worldwide height reference
└── SSZ constraint at global level
```

**Governance Structure:**

An international coordination committee should be established, consisting of:
- Representatives from each participating institution
- Theoreticians with SSZ expertise
- Metrology experts (BIPM)
- Industry observers (for future applications)

---

## 7.6 Why Null Results Matter — Extended Philosophical Analysis

### 7.6.1 The Logic of Non-Detection

In the philosophy of science, it is often emphasized that negative results are less publishable and less cited than positive ones. This asymmetry leads to an underestimation of the scientific value of null results. In the case of SSZ, this underestimation is particularly inappropriate.

**Bayesian Perspective:**

Consider the prior probabilities before a Bounded Regime experiment:

```
P(SSZ correct) = p_SSZ
P(SSZ wrong, anomalous coupling exists) = p_anom
P(SSZ wrong, no coupling) = p_null = 1 - p_SSZ - p_anom
```

SSZ predicts for transmons: "Signal undetectable" (ΔΦ ~ 10⁻¹³ rad << σ).
An anomalous theory might predict: "Signal detectable" (ΔΦ ~ 10⁻³ rad).

After a null result (no detection):

```
Likelihood:
P(Null | SSZ correct) ≈ 1 (SSZ predicts null)
P(Null | anomalous) ≈ 0 (anomalous predicts signal)
P(Null | no coupling) ≈ 1

Posterior (Bayes):
P(SSZ correct | Null) ∝ P(Null | SSZ) × P(SSZ) = 1 × p_SSZ
P(anomalous | Null) ∝ P(Null | anomalous) × P(anomalous) ≈ 0
```

The null result eliminates the anomalous hypothesis and strengthens both SSZ and the null hypothesis. The relative support for SSZ versus null depends on further experimental tests (e.g., Optical Regime detection).

### 7.6.2 Upper Bounds as Scientific Results

Even without detection, a carefully conducted experiment yields quantitative scientific results in the form of upper bounds:

**Formalization:**

The measured slope α = ∂ΔΦ/∂Δh has an uncertainty σ_α. For measured α ≈ 0:

```
95% Confidence Upper Limit: α < 1.96 × σ_α
```

This bound excludes all theories predicting α > α_upper.

**Physical Interpretation:**

An upper bound of α < 10⁻² rad/m means:
- Any height-dependent coupling is weaker than 10⁻² rad/m
- SSZ prediction (α_SSZ ~ 10⁻⁸ rad/m) is 10⁶× smaller than bound
- Theories with stronger coupling are falsified

**Historical Analogies:**

Important null results in physics history:
- **Michelson-Morley (1887):** No aether drift → Special Relativity
- **Eötvös (1922):** No violation of equivalence principle → confirms GR
- **Proton decay experiments:** No detection → bounds on GUT parameters

SSZ Bounded experiments join this tradition.

### 7.6.3 Methodology Validation Without Detection

Even if the Bounded Regime allows no detection, the experimental protocol can be validated:

**Control Experiments:**

1. **Positive Control:** Intentional injection of an artificial height-dependent phase (e.g., via LO modulation). Expectation: Detection.

2. **Negative Control:** Application of a random (not SSZ-calculated) compensation. Expectation: No improvement.

3. **Scaling Test:** Variation of ω (different qubits) and t (different wait times). Expectation: Consistency with scaling laws.

```python
def validate_methodology(experiment_data):
    """
    Validate experimental methodology even without SSZ detection.
    """
    results = {}
    
    # Positive control
    artificial_drift = 0.01  # rad/m (detectable)
    inject_artificial_phase(artificial_drift)
    detected = run_detection_protocol()
    results['positive_control'] = detected  # Should be True
    
    # Negative control
    random_compensation = np.random.uniform(-1, 1)  # Wrong correction
    apply_compensation(random_compensation)
    improved = measure_coherence_improvement()
    results['negative_control'] = not improved  # Should be True
    
    # Scaling test
    omega_values = [4e9, 5e9, 6e9]  # GHz
    slopes = []
    for omega in omega_values:
        slope = measure_slope_at_frequency(omega)
        slopes.append(slope / omega)  # Normalized
    results['scaling_consistent'] = np.std(slopes) < tolerance
    
    return results
```

These controls prove the experiment works, even if the physical signal is too small.

---

## 7.7 Comparison with Related Proposals — Extended Discussion

### 7.7.1 Pikovski et al. (2015): Gravitationally Induced Decoherence

The work by Pikovski, Zych, Costa and Brukner in Nature Physics 2015 proposed that gravitational effects could be a fundamental source of decoherence in quantum systems.

**Core Argument:**

When a massive object is in a spatial superposition (Δx), its proper time is also in superposition. The superposition of different proper times leads to entanglement between the internal state of the object and its position, which effectively appears as decoherence.

The proposed decoherence rate:

```
Γ_Pikovski = (m × g × Δx)² × τ / ℏ²
```

where τ is the characteristic time of the internal degree of freedom.

**Difference from SSZ:**

| Aspect | Pikovski | SSZ |
|--------|----------|-----|
| **Nature** | Decoherence (irreversible) | Drift (reversible) |
| **Cause** | Proper time superposition | Proper time difference |
| **Prerequisite** | Spatial superposition | Spatial separation |
| **Scaling** | ∝ m² × (Δx)² | ∝ ω × Δh |
| **Compensation** | Impossible | Possible |

**Experimental Distinction:**

- Pikovski effect requires macroscopic superpositions (experimentally extremely difficult)
- SSZ acts on localized, separated qubits (experimentally accessible)
- Pikovski is stochastic, SSZ deterministic

The two effects are complementary, not competing. SSZ describes the effect on separated, localized systems; Pikovski describes effects on delocalized superpositions.

### 7.7.2 Zych et al. (2011): Proper Time Interferometry

Zych, Costa, Pikovski and Brukner proposed detecting proper time differences using atom interferometry.

**Concept:**

An atom is placed in a superposition of two paths that traverse different gravitational potentials. The accumulated phase difference contains a contribution from proper time:

```
ΔΦ = (m c² / ℏ) × ∫(√g₀₀(x₁(t)) - √g₀₀(x₂(t))) dt
```

**Connection to SSZ:**

The Zych prediction is mathematically equivalent to SSZ phase drift for the case where the two "qubits" are the two interferometer paths. The difference lies in experimental realization:

- Zych: Single atom in superposition (interferometer)
- SSZ: Two separate atoms/qubits (separate measurements)

**Experimental Status:**

Atom interferometers have not yet achieved the sensitivity to detect the Zych effect. The required arm length (> 1 m) with sufficient coherence time is technically challenging.

### 7.7.3 Quantum Geodesy

Quantum geodesy uses optical clocks as height measurement instruments. The idea is simple: Since clock frequency depends on gravitational potential, a precise frequency measurement can be converted into a height measurement.

**Current Precision:**

Optical clocks achieve fractional uncertainties of 10⁻¹⁸, corresponding to a height uncertainty of:

```
δh = c² × (δν/ν) / g ≈ (3×10⁸)² × 10⁻¹⁸ / 10 ≈ 1 cm
```

This is already competitive with classical geodesy.

**SSZ Implications:**

Quantum geodesy and SSZ are closely related:
- Both utilize gravity-induced frequency shifts
- SSZ adds the compensation dimension
- Future quantum networks could serve as distributed geodetic sensors

**Vision: Gravitational Quantum Sensor Network:**

A network of SSZ-aware quantum clocks could:
- Continuously monitor Earth's gravitational field
- Detect mass movements (groundwater, magma) in real time
- Provide more precise height references for climate research

---

© 2025 Carmen Wrede & Lino Casu
