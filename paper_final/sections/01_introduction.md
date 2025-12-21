# 1. Introduction and Scope

## 1.1 Motivation

Gravitational redshift has been observed in optical clocks [Chou2010, Bothwell2022] and spaceborne experiments [Hafele1972], but its influence on solid-state quantum information processors remains largely unexplored. The gravitational potential difference across a centimetre-scale device corresponds to a fractional frequency shift of order 10⁻¹⁸, far below the noise floor of current superconducting qubits but within reach of state-of-the-art optical clocks.

Recent proposals by Wrede and colleagues posit that small but deterministic time-dilation differences arise when qubits occupy slightly different gravitational potentials, leading to an accumulated phase drift. Because the drift is deterministic, it can be predicted and compensated; however, the predicted magnitude in existing superconducting circuits is many orders of magnitude below typical noise.

## 1.2 Scope of This Paper

This paper unifies four previously separate works into a single, comprehensive treatment:

| Paper | Focus | Key Contribution |
|-------|-------|-----------------|
| Paper A | Geometry optimization | Segment density, zone width |
| Paper B | Phase coherence | Entanglement preservation, compensation |
| Paper C | Experimental framework | Feasibility, statistics, upper bounds |
| Paper D | Master summary | Unified notation, claim taxonomy |

We seek to answer three questions:

1. **Theory**: How does the SSZ model modify the standard time-dilation formula?
2. **Discrimination**: What experimental signatures discriminate SSZ from conventional dephasing?
3. **Feasibility**: Under what conditions can SSZ effects be measured or bounded?

## 1.3 Claim Boundaries

Our claims are bounded by three regimes:

### Bounded Regime (Today's Superconducting Qubits)
- Δh ~ mm scale, t ~ 100 μs
- Predicted drift: ~10⁻¹³ rad
- 12 orders of magnitude below noise floor (~1 rad)
- **Outcome**: Upper bounds on anomalous couplings only
- **Interpretation**: Null result is SSZ-consistent

### Detection Regime (Optical Atomic Clocks)
- Δh ~ 1 m, t ~ 1 s
- Predicted drift: ~0.6 rad
- Within measurement resolution (~10⁻³ rad)
- **Outcome**: Direct detection and compensation testing
- **Interpretation**: Gold standard for SSZ validation

### Future Regime (Advanced Quantum Networks)
- High-coherence optical qubits, satellite QKD
- SSZ drift becomes operational constraint
- **Outcome**: SSZ-aware design required
- **Interpretation**: Engineering consideration

**We explicitly exclude claims that SSZ is detectable in current mm-scale devices.** Simulations showing visible drifts use didactic scaling for visualization and do not represent physical predictions.

## 1.4 Relativity Hygiene

Local measurements of the speed of light obey special relativity; a falling observer sees no difference between electromagnetic waves of different frequencies. However, when comparing two separated clocks, general relativity predicts a redshift proportional to the gravitational potential difference.

The SSZ model modifies the redshift by introducing a segment density Ξ(h) that encodes how segments of spacetime accumulate. Importantly:

- **Local frames remain Lorentz-invariant**
- SSZ effects only manifest in **global comparisons** of separated clocks
- The condition t = t' holds locally
- Accumulated differences appear over time t when comparing clocks at heights h and h+Δh

This is consistent with the equivalence principle: no local experiment can detect the gravitational field, but non-local comparisons reveal potential differences.

## 1.5 Paper Structure

| Section | Content |
|---------|---------|
| 2 | Theory: Segment density, time dilation, phase drift |
| 3 | Control: Compensation protocol, scaling signatures |
| 4 | Experiments: Upper-bound designs, statistical framework |
| 5 | Entanglement: Phase preservation analysis |
| 6 | Engineering: Layout guidelines, compiler integration |
| 7 | Feasibility: Platform comparison, future regimes |
| 8 | Conclusion: Summary, falsification criteria |
| App. A | Full mathematical derivation |
| App. B | Didactic scaling definition |
| App. C | Confound playbook |
| App. D | Physical constants |

→ **See Table 1** for symbol definitions used throughout.
