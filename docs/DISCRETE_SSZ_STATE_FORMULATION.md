# Discrete SSZ State Formulation: Canonical Technical Reference

**Version:** 1.0
**Date:** 2026-03-16
**Authors:** Carmen Wrede & Lino Casu
**Status:** CANONICAL — Technical reference for the discrete φ-ladder formulation

---

## Table of Contents

1. [Overview and Concept](#1-overview-and-concept)
2. [φ-Ladder and Dimensionless Coordinate](#2-φ-ladder-and-dimensionless-coordinate)
3. [Discrete SSZ State Vector Y_k](#3-discrete-ssz-state-vector-y_k)
4. [Canonical Piecewise Regime Form](#4-canonical-piecewise-regime-form)
5. [Natural Boundary Values at the Schwarzschild Radius](#5-natural-boundary-values-at-the-schwarzschild-radius)
6. [Weak-Field Recursion](#6-weak-field-recursion)
7. [Strong-Field Recursion](#7-strong-field-recursion)
8. [Conceptual Core](#8-conceptual-core)
9. [Implementation Reference](#9-implementation-reference)
10. [Cross-References](#10-cross-references)

---

## 1. Overview and Concept

The discrete SSZ formulation answers the question: *What happens to the SSZ state variables when we step along the radial φ-ladder r_k = r_s · φ^k from grid point to grid point?*

**Core principle:** SSZ is not a discrete spacetime theory. The field Ξ(r) is smooth and continuous for all r > 0. The discreteness lies in three structures:

1. **φ-Segment counting**: N'(r) = 4·s(r) as a state variable, where N' = 4 in flat spacetime.
2. **φ-Level classification**: ν(r) = ln(1 + Ξ(r)) / ln(φ) — local logarithmic classification of the segmentation state.
3. **φ-Ladder recursion**: Exact algebraic recursion formulas on the lattice x_k = φ^k.

The continuous field Ξ(r) remains the primary physical quantity. The discrete recursions are consequences of the φ-lattice structure, not independent axioms.

**Relation to the continuous theory:**

```
Continuous:   Ξ(r), D(r), s(r)  for all r > 0
Discrete:     Y_k = Y(r_k)  on the lattice r_k = r_s · φ^k
Relation:     Y_k = evaluation of the continuous fields at lattice points
```

---

## 2. φ-Ladder and Dimensionless Coordinate

**Schwarzschild radius:**

```
r_s = 2GM / c²
```

**Dimensionless radial coordinate:**

```
x = r / r_s
```

**φ-Ladder:**

```
x_k = φ^k       (k ∈ ℤ)

φ = (1 + √5) / 2 = 1.6180339887498948482...
```

**Lattice points (examples):**

| k | x_k = φ^k | r_k = r_s · x_k | Regime |
|---|-----------|-----------------|--------|
| −3 | 0.2361 | 0.236 r_s | g₂: Strong field |
| −2 | 0.3820 | 0.382 r_s | g₂: Strong field |
| −1 | 0.6180 | 0.618 r_s | g₂: Strong field |
| 0 | 1.0000 | 1.000 r_s | g₂: Strong field |
| 1 | 1.6180 | 1.618 r_s | g₂/Blend |
| 2 | 2.6180 | 2.618 r_s | g₁: Weak field |
| 3 | 4.2361 | 4.236 r_s | g₁: Weak field |

**φ-Ladder properties:**

```
x_{k+1} = φ · x_k          [step outward]
x_{k+1} = x_k / φ          [step inward]
x_{k+n} = φ^n · x_k        [n steps outward]
```

Since φ² = φ + 1 (Fibonacci identity), the φ-ladder is self-similar: x_{k+2} = x_{k+1} + x_k.

---

## 3. Discrete SSZ State Vector Y_k

**Definition:**

Let Ξ_k := Ξ(x_k) be the value of the SSZ segment density at lattice point k. The discrete SSZ state at lattice point k is:

```
Y_k := (Ξ_k,  s_k,  D_k,  N'_k,  ν_k)
```

with:

```
Ξ_k   =  Ξ(x_k)                          [segment density]
s_k   =  1 + Ξ_k                          [scaling factor]
D_k   =  1 / (1 + Ξ_k)                    [time dilation]
N'_k  =  4 · (1 + Ξ_k)                    [effective segment count]
ν_k   =  ln(1 + Ξ_k) / ln(φ)             [local φ-level]
```

**State conversions (complete):**

From Ξ:
```
s    = 1 + Ξ
D    = 1 / (1 + Ξ)
N'   = 4 · (1 + Ξ)
ν    = ln(1 + Ξ) / ln(φ)
```

From D:
```
Ξ    = 1/D - 1
s    = 1/D
N'   = 4/D
ν    = ln(1/D) / ln(φ)
```

From ν:
```
s    = φ^ν
Ξ    = φ^ν - 1
D    = φ^{-ν}
N'   = 4 · φ^ν
```

From s:
```
Ξ    = s - 1
D    = 1/s
N'   = 4s
ν    = ln(s) / ln(φ)
```

**Theorem (State equivalence):** Each of the five components of Y_k uniquely determines the remaining four. In particular: D_k = φ^{−ν_k} and N'_k = 4φ^{ν_k}.

**Physical meaning:**

| Component | Physical role | Limit (r → ∞) | Value at r = r_s |
|-----------|--------------|----------------|------------------|
| Ξ_k | Local spacetime segmentation (primary field) | 0 | 0.8017 |
| s_k | Local time stretching; s = 1/D | 1 | 1.8017 |
| D_k | Local time / coordinate time | 1 | 0.5550 |
| N'_k | Effective segments per wave period | 4 | 7.207 |
| ν_k | Logarithmic φ-segmentation state | 0 | ≈ 1.22 |

---

## 4. Canonical Piecewise Regime Form

```
            1 / (2 x_k)                            x_k > 2.2     [g₁: Weak field]
Ξ_k  :=    Ξ_blend(x_k)                            1.8 ≤ x_k ≤ 2.2   [C²-Transition]
            min(1 - exp(-φ · x_k),  Ξ_max)         x_k < 1.8     [g₂: Strong field]
```

with:

```
Ξ_max = 1 - exp(-φ) ≈ 0.801711847
```

**Blend zone:** Quintic Hermite C²-interpolation between g₁ and g₂. Matches value, first and second derivative at both boundaries (x = 1.8 and x = 2.2). Normalized parameter t = (x − 1.8) / 0.4 ∈ [0,1].

**Canonical strong-field form — saturation form:**

```
Ξ_g2(x) = 1 - exp(-φ · x)    with x = r/r_s
```

Properties:
- Ξ(0) = 0 — singularity-free
- Ξ(r_s) = 1 - exp(-φ) = Ξ_max ≈ 0.8017
- Monotonically increasing for x > 0

**Note:** The decay form `1 - exp(-φ r_s/r)` is complementary/historical. The operative canonical form for all recursions in this document is the saturation form.

---

## 5. Natural Boundary Values at the Schwarzschild Radius

At the Schwarzschild radius (x = 1, k = 0):

```
Ξ_*  =  1 - exp(-φ)              =  0.801711847...
s_*  =  2 - exp(-φ)              =  1.801711847...
D_*  =  1 / (2 - exp(-φ))        =  0.555027710...
N'_* =  4 · (2 - exp(-φ))        =  7.206847389...
ν_*  =  ln(2 - exp(-φ)) / ln(φ)  ≈  1.2248...  ≈ 1.22
```

**Complete table:**

| Quantity | Symbol | Exact expression | Numerical value |
|----------|--------|-----------------|-----------------|
| Segment density | Ξ_* | 1 − exp(−φ) | 0.801711847 |
| Scaling factor | s_* | 2 − exp(−φ) | 1.801711847 |
| Time dilation | D_* | [2 − exp(−φ)]⁻¹ | 0.555027710 |
| Segment count | N'_* | 4 · [2 − exp(−φ)] | 7.206847389 |
| φ-Level | ν_* | ln[2 − exp(−φ)] / ln(φ) | ≈ 1.22 |

**Equivalence family:** The values are not independent. The following equivalence holds:

```
0.555 ↔ 0.802 ↔ 1.802 ↔ 7.207 ↔ 1.22
```

Each value uniquely determines the others. In particular, D(r_s) = 0.555 is not a free parameter but a direct consequence of φ.

**Derivation of Ξ_* = 1 - exp(-φ):**

```
Ξ_* = Ξ_g2(x=1) = 1 - exp(-φ · 1) = 1 - exp(-φ) = 1 - e^{-1.6180...}
    = 1 - 0.19829...
    = 0.80171...
```

**Derivation of D_*:**

```
D_* = 1 / (1 + Ξ_*) = 1 / (1 + (1 - exp(-φ))) = 1 / (2 - exp(-φ))
    = 1 / (2 - 0.19829...)
    = 1 / 1.80171...
    = 0.55503...
```

**Derivation of ν_*:**

```
ν_* = ln(s_*) / ln(φ)
    = ln(1.80171...) / ln(1.61803...)
    = 0.58943... / 0.48121...
    = 1.2248...
```

---

## 6. Weak-Field Recursion

**Starting point:** Weak-field formula Ξ_g1(x) = 1/(2x), φ-ladder x_{k+1} = φ x_k.

**Recursion formulas:**

```
Ξ_{k+1} = Ξ_k / φ          [step outward, x_{k+1} = φ x_k]
Ξ_{k+1} = φ · Ξ_k          [step inward, x_{k+1} = x_k/φ]
```

**Complete derivation (outward):**

```
Ξ_{k+1} = 1 / (2 · x_{k+1})
         = 1 / (2 · φ · x_k)         [since x_{k+1} = φ · x_k]
         = (1 / (2 x_k)) · (1/φ)
         = Ξ_k · (1/φ)
         = Ξ_k / φ
```

**Complete derivation (inward):**

```
Ξ_{k+1} = 1 / (2 · x_{k+1})
         = 1 / (2 · x_k/φ)           [since x_{k+1} = x_k/φ]
         = (1 / (2 x_k)) · φ
         = Ξ_k · φ
```

**Multi-step:**

```
Ξ_{k+n} = Ξ_k / φ^n      [n steps outward]
Ξ_{k+n} = Ξ_k · φ^n      [n steps inward]
```

**Full state recursion (outward):**

```
Ξ_{k+1} = Ξ_k / φ
s_{k+1} = 1 + Ξ_k/φ
D_{k+1} = 1 / (1 + Ξ_k/φ)
N'_{k+1} = 4 · (1 + Ξ_k/φ)
ν_{k+1} = ln(1 + Ξ_k/φ) / ln(φ)
```

**Interpretation:** Since 1/φ ≈ 0.618, every outward step on the φ-ladder reduces the segment density by the golden ratio factor. The weak-field recursion is a geometric sequence: Ξ_k = Ξ_0 / φ^k — the Fibonacci self-similarity of the radial segment density profile.

---

## 7. Strong-Field Recursion

**Starting point:** Canonical saturation form Ξ_g2(x) = 1 - exp(-φx), φ-ladder x_{k+1} = φ x_k.

**Recursion formulas:**

```
Ξ_{k+1} = 1 - (1 - Ξ_k)^φ          [step outward, x_{k+1} = φ x_k]
Ξ_{k+1} = 1 - (1 - Ξ_k)^{1/φ}      [step inward, x_{k+1} = x_k/φ]
```

**Complete derivation (outward):**

Since Ξ_k = 1 - exp(-φ x_k), we first have:

```
1 - Ξ_k = exp(-φ · x_k)
```

Substituting x_{k+1} = φ · x_k:

```
Ξ_{k+1} = 1 - exp(-φ · x_{k+1})
         = 1 - exp(-φ · φ · x_k)
         = 1 - exp(-φ² · x_k)
```

Now applying the power rule exp(-φ² x) = (exp(-φx))^φ:

```
         = 1 - [exp(-φ · x_k)]^φ
         = 1 - (1 - Ξ_k)^φ
```

**Complete derivation (inward):**

Substituting x_{k+1} = x_k/φ:

```
Ξ_{k+1} = 1 - exp(-φ · x_{k+1})
         = 1 - exp(-φ · x_k/φ)
         = 1 - exp(-x_k)
```

Writing exp(-x_k) = exp(-φ · x_k / φ) and applying:

```
exp(-x_k) = [exp(-φ · x_k)]^{1/φ}     [since: -x_k = (-φ x_k) · (1/φ)]
```

Therefore:

```
Ξ_{k+1} = 1 - [exp(-φ · x_k)]^{1/φ}
         = 1 - (1 - Ξ_k)^{1/φ}
```

Since 1/φ = φ - 1, alternatively: Ξ_{k+1} = 1 - (1 - Ξ_k)^{φ-1}.

**Operative form with saturation cap:**

```
Ξ_{k+1}^{phys} = min(1 - (1 - Ξ_k)^φ,    Ξ_max)   [outward]
Ξ_{k+1}^{phys} = min(1 - (1 - Ξ_k)^{1/φ}, Ξ_max)  [inward]
```

**Algebraic linearization:**

The substitution q_k = 1 - Ξ_k = exp(-φ x_k) yields the linearized form:

```
q_{k+1} = q_k^φ          [outward]
q_{k+1} = q_k^{1/φ}      [inward]
```

This is a geometric sequence in logarithmic scale: ln(q_k) = -φ x_k.

**Example table (strong field, starting at x=1):**

| k | x_k | Ξ_k | s_k | D_k | N'_k | ν_k |
|---|-----|-----|-----|-----|------|-----|
| −2 | 0.382 | 0.4559 | 1.4559 | 0.6868 | 5.824 | 0.793 |
| −1 | 0.618 | 0.6329 | 1.6329 | 0.6124 | 6.532 | 1.011 |
| 0 | 1.000 | 0.8017 | 1.8017 | 0.5550 | 7.207 | 1.225 |
| 1 | 1.618 | 0.9286 | 1.9286 | 0.5185 | 7.714 | 1.404 |

*(k=2: x=2.618 > 2.2, lies in the blend/weak-field transition)*

---

## 8. Conceptual Core

### SSZ is continuous — the discreteness is structural

The φ-level ν_k = ln(1 + Ξ_k)/ln(φ) is a **local classification quantity**, not a dynamical field variable. Specifically:

- ν_k classifies the *instantaneous* segmentation state of an observer.
- The *cumulative* segment counter along a long radial path can grow without bound.
- The *local* segment density Ξ is bounded by Ξ_max ≤ 1 (saturation).

This separation — locally bounded φ-level, unbounded cumulative counter — is the physical basis for SSZ being singularity-free: the field saturates at Ξ_max rather than diverging.

### Both recursions are self-similar

```
Weak field:   Ξ_{k+1} = Ξ_k / φ          → geometric sequence in Ξ
Strong field: q_{k+1} = q_k^φ              → geometric sequence in ln(q)
```

Both have the same algebraic structure in their natural variables. This is not accidental but a direct consequence of the logarithmic spiral that generates the φ-lattice: the spiral reproduces itself at every revolution — the recursion reproduces itself at every lattice step.

### The φ-level as a unified scale

The φ-level ν unifies both regimes on a single scale:

```
ν → 0          (flat spacetime, r → ∞)
ν_* ≈ 1.22     (at the Schwarzschild radius, r = r_s)
```

With D_k = φ^{−ν_k}: every outward step decreases ν_k, every inward step increases ν_k. The Schwarzschild radius corresponds to the φ-level ν = ln(2−e^{−φ})/ln(φ) ≈ 1.22 — a natural, parameter-free value.

---

## 9. Implementation Reference

```python
import numpy as np

PHI = (1 + np.sqrt(5)) / 2       # 1.6180339887498948482...
XI_MAX = 1 - np.exp(-PHI)        # 0.801711847...

def xi_weak(x):
    """Weak field: Xi = 1/(2x), valid for x > 2.2"""
    return 1.0 / (2.0 * x)

def xi_strong(x):
    """Strong field (saturation form): Xi = min(1-exp(-phi*x), Xi_max), valid for x < 1.8"""
    return min(1.0 - np.exp(-PHI * x), XI_MAX)

def ssz_state(xi):
    """Complete SSZ state from Xi"""
    s   = 1.0 + xi
    D   = 1.0 / s
    Np  = 4.0 * s
    nu  = np.log(s) / np.log(PHI)
    return {'Xi': xi, 's': s, 'D': D, "N'": Np, 'nu': nu}

def recursion_weak_outward(xi_k):
    """Weak-field recursion: step outward (x → phi*x)"""
    return xi_k / PHI

def recursion_weak_inward(xi_k):
    """Weak-field recursion: step inward (x → x/phi)"""
    return xi_k * PHI

def recursion_strong_outward(xi_k):
    """Strong-field recursion: step outward (x → phi*x)"""
    xi_next = 1.0 - (1.0 - xi_k) ** PHI
    return min(xi_next, XI_MAX)

def recursion_strong_inward(xi_k):
    """Strong-field recursion: step inward (x → x/phi)"""
    xi_next = 1.0 - (1.0 - xi_k) ** (1.0 / PHI)
    return min(xi_next, XI_MAX)

# Boundary state at x = 1 (Schwarzschild radius):
boundary_state = ssz_state(XI_MAX)
# boundary_state = {'Xi': 0.8017, 's': 1.8017, 'D': 0.5550, "N'": 7.2068, 'nu': 1.22}
```

**Full implementation:** `E:\clone\SSZ_PHI_DISCRETIZATION.py`

---

## 10. Cross-References

### Book references (E:\clone\SSZ_BOOK_PROJECT)

| Section | Content |
|---------|---------|
| Chapter 4.6 | Complete derivations (Theorems 4.4–4.7, Corollaries 4.2–4.6) |
| Appendix B.10 | Canonical compact form with cross-reference table |
| Chapter 1 | SSZ overview, D_min = 0.555 derivation chain |
| Chapter 3 | φ as growth function, r_φ |
| Chapter 4.1–4.5 | Logarithmic spiral, Euler embedding, N₀=4 |
| Chapter 16 | Frequency framework, N₀=4, segment quantization |

### Technical references

| Document | Content |
|----------|---------|
| `SSZ_MATHEMATICAL_PHYSICS.md` (this repo) | Mathematical foundations, Ξ definitions |
| `SSZ_FORMULA_DOCUMENTATION.md` (this repo) | Regime formulas, implementation |
| `DISCRETE_SSZ_STATE_FORMULATION_DE.md` (DE) | German counterpart of this document |

### Formula cross-reference

| Formula | Appendix B | Chapter |
|---------|-----------|---------|
| Ξ_weak = 1/(2x) | B.1.1 | 1, 4.6.3 |
| Ξ_strong = 1-exp(-φx) | B.1.1, B.10.2 | 4.6.3 |
| D = 1/(1+Ξ) | B.1.2 | 1, 4.6.2 |
| s = 1+Ξ | B.1.5 | 4.6.2 |
| Hermite-C² blend | B.2.2 | 4.6.3 |
| Ξ(r_s) = 0.802 | B.7.1 | 4.6.4 |
| D(r_s) = 0.555 | B.7.1 | 4.6.4 |
| φ-recursion (weak field) | B.10.4 | 4.6.5 |
| φ-recursion (strong field) | B.10.5 | 4.6.6 |
| Y_k = (Ξ,s,D,N',ν) | B.10.1 | 4.6.2 |

---

© 2025–2026 Carmen Wrede & Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
