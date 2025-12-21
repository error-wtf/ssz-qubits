# 5. Entanglement and Phase Preservation — Extended Version

## 5.x Lindblad Master Equation Treatment

The complete description of open quantum system dynamics requires the density matrix formalism and the Lindblad master equation. This treatment enables a precise distinction between the deterministic SSZ contribution and stochastic decoherence processes.

### 5.x.1 Density Matrix Formalism

For a system of two qubits at different heights, we describe the state by the density matrix ρ(t) in the 4×4 space of two-qubit states. The basis is {|00⟩, |01⟩, |10⟩, |11⟩}.

An initial Bell state |Φ⁺⟩ = (|00⟩ + |11⟩)/√2 has the density matrix:

```
ρ(0) = |Φ⁺⟩⟨Φ⁺| = 1/2 × | 1  0  0  1 |
                         | 0  0  0  0 |
                         | 0  0  0  0 |
                         | 1  0  0  1 |
```

The elements critical for entanglement are the off-diagonal terms ρ₀₀,₁₁ and ρ₁₁,₀₀ (also known as "coherences").

### 5.x.2 Lindblad Master Equation

The general form of the Lindblad master equation is:

```
dρ/dt = -i[H, ρ] + Σₖ γₖ (Lₖ ρ Lₖ† - ½{Lₖ†Lₖ, ρ})
```

where:
- H is the system Hamiltonian
- Lₖ are the Lindblad operators (jump operators)
- γₖ are the associated rates
- [·,·] is the commutator and {·,·} is the anticommutator

The first term describes unitary (coherent) evolution, the second term the dissipative (incoherent) dynamics.

### 5.x.3 SSZ as Deterministic Hamiltonian Contribution

The SSZ effect manifests as an additional term in the Hamiltonian. For two qubits at heights h₁ and h₂ = h₁ + Δh:

```
H_SSZ = ℏω₁ D(h₁) σ_z^(1)/2 + ℏω₂ D(h₂) σ_z^(2)/2
```

where σ_z^(i) is the Pauli-Z operator on qubit i and D(h) = 1/(1+Ξ(h)) is the SSZ time dilation.

In the interaction picture (rotating frame) at the mean frequency ω̄, this reduces to:

```
H_SSZ^(int) = ℏω ΔD/2 × (σ_z^(2) - σ_z^(1))
```

with ΔD = D(h₂) - D(h₁) = r_s × Δh / R².

**Effect on the Density Matrix:**

The unitary evolution under H_SSZ^(int) generates:

```
ρ(t) = U(t) ρ(0) U†(t)
```

with U(t) = exp(-i H_SSZ^(int) t / ℏ).

For the Bell state, this results in:

```
ρ(t) = 1/2 × | 1       0  0  e^(iΔΦ) |
             | 0       0  0  0       |
             | 0       0  0  0       |
             | e^(-iΔΦ) 0  0  1       |
```

where ΔΦ = ω × ΔD × t.

**Critical Observation:** The diagonal elements (populations) remain unchanged. Only the off-diagonal elements (coherences) accumulate a phase. The state remains a pure, maximally entangled state—it merely rotates within the Bell basis.

### 5.x.4 Decoherence via Lindblad Dissipators

In contrast to deterministic SSZ evolution, the Lindblad terms describe stochastic processes:

**Dephasing (T₂ Process):**
```
L_φ = √(1/T₂) × σ_z
γ_φ = 1
```

This operator models random phase fluctuations due to charge noise, magnetic disturbances, or LO instabilities.

**Relaxation (T₁ Process):**
```
L₋ = √(1/T₁) × σ₋ = √(1/T₁) × |0⟩⟨1|
γ₋ = 1
```

This operator describes spontaneous emission from excited to ground state.

**Effect on Coherences:**

Under purely dissipative evolution (without unitary part), the off-diagonal elements decay exponentially:

```
ρ₀₀,₁₁(t) = ρ₀₀,₁₁(0) × exp(-t/T₂)
```

This is fundamentally different from SSZ-induced phase rotation:
- **Decoherence:** |ρ₀₀,₁₁| decreases → entanglement is destroyed
- **SSZ:** |ρ₀₀,₁₁| remains constant, only phase changes → entanglement is preserved

### 5.x.5 Combined Dynamics

The complete master equation with SSZ and decoherence:

```
dρ/dt = -i[H_SSZ, ρ] + (1/T₂)(σ_z ρ σ_z - ρ) + (1/T₁)(σ₋ ρ σ₊ - ½{σ₊σ₋, ρ})
```

For the coherence ρ₀₀,₁₁, this yields:

```
ρ₀₀,₁₁(t) = ρ₀₀,₁₁(0) × exp(iΔΦ(t)) × exp(-t/T₂)
```

The solution factorizes into:
1. **Deterministic phase rotation:** exp(iΔΦ) from SSZ
2. **Stochastic amplitude decay:** exp(-t/T₂) from decoherence

### 5.x.6 Implications for Measurements

**Fidelity with Target State:**

The fidelity of the evolved state with the original Bell state is:

```
F(t) = ⟨Φ⁺|ρ(t)|Φ⁺⟩ = (1 + cos(ΔΦ) × exp(-t/T₂)) / 2
```

Without SSZ (ΔΦ = 0):
```
F(t) = (1 + exp(-t/T₂)) / 2  →  1/2  for t → ∞
```

With SSZ (ΔΦ ≠ 0):
```
F(t) oscillates with period 2π/(ω×ΔD), damped by exp(-t/T₂)
```

**With Compensation:**

When the compensation phase Φ_corr = -ΔΦ is applied:
```
F_comp(t) = (1 + exp(-t/T₂)) / 2
```

The SSZ-induced oscillation is eliminated, only fundamental decoherence remains.

---

## 5.y Compensation in Entangled Networks

The practical implementation of SSZ compensation in quantum networks requires careful considerations regarding architecture and timing.

### 5.y.1 Photon-Link Phase Correction

In photon-mediated entanglement protocols, compensation can occur at various points:

**Option A: Before Photon Emission**

1. Before entanglement attempt: Known height difference Δh
2. Pre-compensation: Z-rotation by Φ_pre = +ω × r_s × Δh / R² × τ_expected
3. Establish entanglement
4. After time τ: State is already compensated

Advantage: No real-time correction required
Disadvantage: τ must be known in advance

**Option B: After Successful Entanglement**

1. Establish entanglement (heralding)
2. Start timer upon successful herald detection
3. After evolution time τ: Post-compensation Φ_post = -ω × r_s × Δh / R² × τ
4. State is compensated for subsequent operations

Advantage: Flexible τ
Disadvantage: Requires real-time calculation

**Option C: Continuous Compensation**

1. Apply permanent frequency shift Δω = ω × ΔD
2. Qubit 2 effectively operates at ω' = ω(1 - ΔD)
3. Differential phase accumulation is continuously compensated

Advantage: No time-dependent correction needed
Disadvantage: Requires precise frequency control

### 5.y.2 Local Gate Correction

For systems where direct frequency modification is not practical, compensation can be achieved through local Z-rotations:

**Implementation in Qiskit:**

```python
from qiskit import QuantumCircuit, QuantumRegister

def create_compensated_bell_state(qc, q1, q2, delta_h, omega, tau):
    """
    Create Bell state with SSZ compensation.
    
    Args:
        qc: QuantumCircuit
        q1: Qubit 1 (lower height)
        q2: Qubit 2 (higher height, Δh relative to q1)
        delta_h: Height difference [m]
        omega: Qubit frequency [rad/s]
        tau: Expected evolution time [s]
    """
    r_s = 8.87e-3  # m
    R = 6.371e6    # m
    
    # Create Bell state
    qc.h(q1)
    qc.cx(q1, q2)
    
    # SSZ compensation
    phi_corr = -omega * r_s * delta_h / R**2 * tau
    qc.rz(phi_corr, q2)
```

**Implementation in Cirq:**

```python
import cirq
import numpy as np

def ssz_compensation_gate(delta_h, omega, tau):
    """
    Create SSZ compensation gate.
    """
    r_s = 8.87e-3
    R = 6.371e6
    phi_corr = -omega * r_s * delta_h / R**2 * tau
    return cirq.rz(phi_corr)
```

### 5.y.3 Feedforward vs. Feedback

**Feedforward Approach:**
- Compensation based on known system parameters (Δh, ω, τ)
- No real-time measurement required
- Precision limited by parameter uncertainties
- Suitable for static configurations

**Feedback Approach:**
- Regular phase measurements on reference qubit pairs
- Active adjustment based on measured deviation
- Can compensate slow drifts (thermal, magnetic)
- Higher overhead, but more robust

### 5.y.4 Multi-Node Scaling (GHZ States)

For N-qubit GHZ states across N network nodes at heights h₁, h₂, ..., hₙ:

```
|GHZ⟩ = (|00...0⟩ + |11...1⟩) / √2
```

The relative phase between the two terms accumulates as a sum:

```
Φ_total(t) = ω × t × Σⱼ (D(hⱼ) - D(h_ref))
           = ω × r_s × t / R² × Σⱼ (hⱼ - h_ref)
```

**Compensation Protocol:**

1. Choose lowest node as reference: h_ref = min(h₁, ..., hₙ)
2. For each node j: Calculate Δhⱼ = hⱼ - h_ref
3. Apply local compensations:
   ```
   Φ_corr,j = -ω × r_s × Δhⱼ / R² × t
   ```
4. Net effect: All relative phases vanish

**Scaling Properties:**
- Communication overhead: O(N) for height exchange
- Computational overhead: O(N) compensation calculations
- No global coordination required (local operations suffice)

### 5.y.5 Protocol Integration

For practical quantum network protocols, we recommend:

1. **Height metadata in header:** Each network node advertises its height h
2. **Dynamic compensation calculation:** Upon connection establishment, Δh and Φ_corr are calculated
3. **Periodic recalibration:** For long connections, compensation is updated
4. **Fallback:** Without height information, no compensation (Bounded Regime acceptable)

---

## Summary

The Lindblad analysis shows:
- **SSZ is a unitary process:** Rotation, not damping
- **Entanglement is preserved:** Only phase changes
- **Compensation is exact:** Deterministic effect can be fully canceled
- **Scaling is linear:** N-node networks require O(N) local operations

The fundamental difference between SSZ (deterministic, compensable) and decoherence (stochastic, irreversible) enables experimental discrimination and practical use of SSZ predictions.

---

© 2025 Carmen Wrede & Lino Casu
