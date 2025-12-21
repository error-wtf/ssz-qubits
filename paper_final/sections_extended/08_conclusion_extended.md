# 8.1 Conclusion — Extended Version (5 Points as Paragraphs)

The results of this work can be summarized in five central statements, each illuminating an essential aspect of SSZ theory and its experimental implications.

---

## 8.1.1 The Twelve Orders-of-Magnitude Gap

Perhaps the most surprising finding of this analysis is the extent of the discrepancy between the predicted SSZ signal and the noise floor of today's superconducting quantum processors. For a typical transmon qubit with a frequency of 5 GHz, at a height difference of 1 mm and a coherence time of 100 μs, the SSZ-induced phase drift amounts to approximately 6.9 × 10⁻¹³ radians. The T₂-limited phase noise floor, in contrast, is approximately 1 radian—a difference of twelve orders of magnitude.

This enormous gap has a dual significance. On one hand, it explains why SSZ effects have not been observed in any qubit experiment to date: the signal literally disappears into the noise, even with the most careful data analysis. On the other hand, this prediction itself is a test of the theory. An alternative theory predicting stronger height-dependent couplings could be falsified by the absence of corresponding signals.

The physical cause of the gap lies in the combination of three factors: the tiny size of Earth's Schwarzschild radius (8.87 mm) relative to Earth's radius (6371 km), the short coherence times of superconducting qubits (microseconds), and the relatively low microwave frequencies (gigahertz). Each of these factors contributes several orders of magnitude to the suppression.

For quantum computing practice, this means: SSZ is not an error source that needs to be considered in today's superconducting systems. The prediction of undetectability is itself a testable statement—and all experimental findings to date are consistent with it.

---

## 8.1.2 Null Results as Positive Confirmation

In the philosophy of science, it is often emphasized that a theory must be falsifiable to have scientific value. Less frequently discussed is that non-refutation under clearly defined conditions also possesses evidential value. For SSZ theory: An experiment in the Bounded Regime that detects no height-dependent phase drift does not falsify the theory—on the contrary, it confirms the quantitative prediction that the effect is undetectable at these scales.

This logic differs fundamentally from situations where a theory predicts a detectable effect and the experiment does not find it. In our case, the theory explicitly states: At Δh ~ mm, ω ~ GHz, and t ~ μs, the signal is more than ten orders of magnitude below the detection threshold. An experiment observing precisely this non-detection is therefore a positive confirmation.

Furthermore, a carefully conducted null result provides additional scientific value: it establishes an upper bound on anomalous height-dependent couplings. If the measured slope α = ∂ΔΦ/∂Δh is consistent with zero, with an uncertainty σ_α, then the upper bound α < 2σ_α follows (at 95% confidence). This bound excludes alternative theories predicting stronger effects.

The correct interpretation of null results requires a clear distinction between "effect not detectable" and "effect does not exist." In the Bounded Regime, non-detection confirms the SSZ prediction; in the Detection Regime, it would falsify the theory.

---

## 8.1.3 Optical Atomic Clocks as Gold Standard

While superconducting qubits operate in the Bounded Regime, optical atomic clocks provide direct access to the Detection Regime. The key property is the dramatically higher frequency: Optical transitions in strontium or ytterbium clocks lie at approximately 429 THz, a factor of 10⁵ compared to typical microwave qubits. Since SSZ phase drift scales linearly with frequency, this increase leads to a proportionally amplified signal.

At a height difference of 1 meter and a measurement time of 1 second, the predicted phase drift is approximately 0.59 radians. The noise floor of optical clocks is approximately 10⁻³ radians, yielding a signal-to-noise ratio of nearly 600—more than sufficient for unambiguous detection.

Crucially, the technological foundation for this experiment already exists. The experiments by Chou et al. (2010) at NIST demonstrated gravitational frequency shift at a height difference of only 33 cm. More recent work at Tokyo Skytree with Δh = 450 m achieved even higher precision. These experiments already measure the effect that SSZ predicts—they confirm the equivalence of SSZ and General Relativity in the weak field.

The next step would be implementation of the with/without compensation protocol: In addition to measuring phase drift, active compensation and verification of drift reversal would provide the decisive SSZ-specific test. This experiment requires no fundamentally new technology, but rather the integration of existing methods into a new protocol.

---

## 8.1.4 Upper Bounds on Anomalous Couplings

Even if experiments in the Bounded Regime cannot directly detect the SSZ effect, they provide valuable scientific results in the form of upper bounds. An upper bound is a statement of the form: "The sought effect, if present, is smaller than X."

For SSZ theory, this means concretely: If the measured slope α = ∂ΔΦ/∂Δh is consistent with zero, this excludes theories predicting larger height-dependent couplings. The practical consequence is:

- SSZ prediction: α_SSZ ≈ 7 × 10⁻⁹ rad/m (for 5 GHz qubits)
- Typical experimental bound: α < 10⁻² rad/m
- Exclusion factor: ~10⁶

This means: Any alternative theory predicting an effect more than about a million times stronger than SSZ would already be falsified by existing null results.

The systematic collection of such bounds across different platforms (transmons, trapped ions, NV centers) and configurations (tilt, remote, stack) builds a network of constraints that increasingly restricts the parameter space of alternative theories. Even without direct SSZ detection, this work therefore has immediate scientific value.

---

## 8.1.5 Future Self-Calibration in Quantum Processors

Looking beyond the current state of technology, a future emerges in which SSZ is no longer merely a subject of fundamental physics curiosity, but becomes a practical engineering constraint. In advanced quantum processors with high coherence and in quantum networks with significant height differences, SSZ compensation will become a necessary component of system calibration.

**Vision: SSZ-aware Quantum Processors**

In an SSZ-aware processor, the calibration routine would include the following additional steps:

1. **Height Profiling:** A profilometer or interferometric measurement system maps height variations across the chip with μm accuracy.

2. **Pairwise ΔD Calculation:** For each qubit pair, the differential time dilation ΔD = r_s × Δh / R² is calculated and stored in the calibration database.

3. **Compiler Integration:** The quantum compiler accesses this data and automatically inserts compensation phases before or after two-qubit gates.

4. **Static Calibration:** Since SSZ depends on fixed geometry (not time-varying parameters), calibration is required only once per chip installation.

**Overhead Estimate:**
- Additional storage: O(N²) values for N qubits (symmetric, ~N²/2)
- Additional compute time: O(1) per gate (simple lookup table)
- Additional gate time: Zero (virtual Z-rotations are pulseless)

**Practical Implementation:**

```python
class SSZAwareCompiler:
    def __init__(self, height_map, qubit_frequencies):
        """
        Initialize SSZ-aware compiler with chip height profile.
        
        Args:
            height_map: dict, {qubit_id: height_in_meters}
            qubit_frequencies: dict, {qubit_id: omega_in_rad_per_s}
        """
        self.height_map = height_map
        self.frequencies = qubit_frequencies
        self.r_s = 8.87e-3  # m
        self.R = 6.371e6    # m
        
    def get_compensation(self, q1, q2, gate_duration):
        """
        Calculate compensation phase for two-qubit gate.
        """
        delta_h = self.height_map[q2] - self.height_map[q1]
        omega = (self.frequencies[q1] + self.frequencies[q2]) / 2
        phi_corr = -omega * self.r_s * delta_h / self.R**2 * gate_duration
        return phi_corr
```

This vision may seem premature for today's systems, but quantum computing technology is developing rapidly. Systems with millisecond coherence times, 3D chiplet stacks, and distributed quantum networks are already in development. Early consideration of SSZ in compiler architectures enables seamless integration when the need arises.

---

## Summary of Five Core Statements

| # | Statement | Implication |
|---|---------|-------------|
| 1 | 12 OoM Gap | SSZ fundamentally undetectable in today's transmons |
| 2 | Null = Positive | Non-detection in Bounded Regime confirms prediction |
| 3 | Optical Clocks | Direct SSZ detection possible with existing technology |
| 4 | Upper Bounds | Null results exclude alternative theories |
| 5 | Self-Calibration | SSZ becomes engineering constraint in future systems |

These five statements form the framework for the scientific classification of SSZ theory and define the path from theoretical prediction through experimental validation to practical application.

---

© 2025 Carmen Wrede & Lino Casu
