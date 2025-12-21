# Appendix G: Statistical Methods

## G.1 Model Comparison Framework

We compare three models for the observed phase drift as a function of height:

### M₀: Null Model
```
ΔΦ = 0 + ε
```
No height dependence; all drift is noise.

### M_SSZ: SSZ Model (Fixed Slope)
```
ΔΦ = α_SSZ × Δh + ε
α_SSZ = ω × r_s / R²
```
SSZ prediction with no free parameters.

### M_anom: Anomalous Model (Free Slope)
```
ΔΦ = α × Δh + ε
α = free parameter
```
Linear fit to detect any height dependence.

---

## G.2 Least Squares Estimation

### Data Model

Given N measurements at heights Δh_i with results ΔΦ_i and uncertainties σ_i:

```
ΔΦ_i = α × Δh_i + ε_i
ε_i ~ N(0, σ_i²)
```

### Weighted Least Squares

Define weights w_i = 1/σ_i².

The optimal slope estimate:
```
α_hat = Σᵢ wᵢ Δhᵢ ΔΦᵢ / Σᵢ wᵢ Δhᵢ²
```

Standard error of the slope:
```
σ_α = √(1 / Σᵢ wᵢ Δhᵢ²)
```

### Goodness of Fit

Chi-squared statistic:
```
χ² = Σᵢ (ΔΦᵢ - α_hat × Δhᵢ)² / σᵢ²
```

Degrees of freedom: ν = N - 1 (one parameter).

Reduced chi-squared: χ²_red = χ² / ν.

---

## G.3 Confidence Intervals

### Slope Confidence Interval

For confidence level 1-α (e.g., 95% → α = 0.05):

```
α_hat ± t_{ν,α/2} × σ_α
```

where t_{ν,α/2} is the Student's t critical value.

For large N: t → 1.96 (95% CI).

### Example

If α_hat = 0.001 rad/m and σ_α = 0.003 rad/m:
```
95% CI: 0.001 ± 1.96 × 0.003 = [-0.005, 0.007] rad/m
```

Since 0 is in the CI, we cannot reject M₀.

---

## G.4 Hypothesis Testing

### Test 1: Is slope non-zero?

**H₀**: α = 0 (M₀)
**H₁**: α ≠ 0 (M_anom)

Test statistic:
```
t = α_hat / σ_α
```

Reject H₀ if |t| > t_{ν,α/2}.

### Test 2: Is slope equal to SSZ prediction?

**H₀**: α = α_SSZ (M_SSZ)
**H₁**: α ≠ α_SSZ

Test statistic:
```
t = (α_hat - α_SSZ) / σ_α
```

Reject H₀ if |t| > t_{ν,α/2}.

---

## G.5 Model Selection

### Likelihood Ratio Test

For nested models (M₀ ⊂ M_anom):

```
Λ = -2 × [ln L(M₀) - ln L(M_anom)]
```

Under H₀: Λ ~ χ²(1).

Reject M₀ if Λ > χ²_{1,α}.

### Akaike Information Criterion (AIC)

```
AIC = 2k - 2 ln L
```

where k is the number of parameters.

| Model | k | Formula |
|-------|---|---------|
| M₀ | 0 | AIC₀ = -2 ln L₀ |
| M_SSZ | 0 | AIC_SSZ = -2 ln L_SSZ |
| M_anom | 1 | AIC_anom = 2 - 2 ln L_anom |

Select model with lowest AIC.

### Bayesian Information Criterion (BIC)

```
BIC = k ln N - 2 ln L
```

BIC penalizes complexity more for large N.

---

## G.6 Upper Bound Calculation

When no signal is detected, we place an upper bound on the slope.

### Frequentist Upper Limit

At confidence level 1-α:
```
α_upper = α_hat + t_{ν,α} × σ_α
```

For 95% one-sided limit: t_{ν,0.05} ≈ 1.645.

### Example

If α_hat = 0.001 rad/m, σ_α = 0.003 rad/m:
```
95% upper limit: 0.001 + 1.645 × 0.003 = 0.006 rad/m
```

We can say: "α < 0.006 rad/m at 95% confidence."

### Bayesian Upper Limit

With flat prior on α:
```
P(α | data) ∝ exp(-χ²(α)/2)
```

The 95% credible interval upper bound:
```
∫_{-∞}^{α_upper} P(α | data) dα = 0.95
```

---

## G.7 Sample Size Calculation

### Required N for Detection

To detect slope α with power 1-β at significance α_s:

```
N = (z_{α_s/2} + z_β)² × σ_ε² / (α² × Var(Δh))
```

where:
- z_{α_s/2}: critical value for significance
- z_β: critical value for power
- σ_ε: noise standard deviation
- Var(Δh): variance of height settings

### Example: Transmon Experiment

Parameters:
- α_SSZ = 6.87e-9 rad/m
- σ_ε = 1 rad (phase noise)
- Δh range: 0-10 mm → Var(Δh) ≈ 8e-6 m²
- α_s = 0.05, β = 0.20 (80% power)

```
N = (1.96 + 0.84)² × 1² / ((6.87e-9)² × 8e-6)
  = 7.84 / 3.78e-22
  = 2.1 × 10²² measurements
```

**Completely infeasible.** This confirms the bounded regime.

### Example: Optical Clock

Parameters:
- α_SSZ = 0.59 rad/m
- σ_ε = 0.001 rad
- Δh range: 0-1 m → Var(Δh) ≈ 0.08 m²
- α_s = 0.05, β = 0.20

```
N = 7.84 × (0.001)² / ((0.59)² × 0.08)
  = 7.84e-6 / 0.028
  ≈ 0.3 measurements
```

**Single measurement sufficient.** Detection regime.

---

## G.8 Systematic Error Analysis

### Sources of Systematic Error

| Source | Effect on α | Mitigation |
|--------|-------------|------------|
| Height measurement error | Bias in slope | Precision survey |
| Frequency calibration | Scale factor | Reference oscillator |
| Temperature drift | False slope | Interleaving |
| Timing error | Scale factor | GPS synchronization |

### Combined Uncertainty

```
σ_α_total² = σ_α_stat² + Σᵢ σ_α_syst,i²
```

### Height Measurement Contribution

If height error is δh with systematic bias b:
```
α_measured = α_true × (1 + b/Δh_mean) + O(δh)
```

For Δh = 1 m with b = 1 cm:
```
Fractional error: 1 cm / 1 m = 1%
```

---

## G.9 Python Implementation

```python
import numpy as np
from scipy import stats

def fit_slope(delta_h, delta_phi, sigma):
    """
    Fit linear model ΔΦ = α × Δh and compute statistics.
    
    Parameters
    ----------
    delta_h : array
        Height differences [m]
    delta_phi : array
        Phase measurements [rad]
    sigma : array
        Measurement uncertainties [rad]
    
    Returns
    -------
    dict
        alpha: slope estimate
        sigma_alpha: standard error
        chi2: chi-squared statistic
        dof: degrees of freedom
        p_value: p-value for slope != 0
        upper_95: 95% upper limit
    """
    w = 1 / sigma**2
    
    # Weighted least squares
    alpha = np.sum(w * delta_h * delta_phi) / np.sum(w * delta_h**2)
    sigma_alpha = np.sqrt(1 / np.sum(w * delta_h**2))
    
    # Chi-squared
    residuals = delta_phi - alpha * delta_h
    chi2 = np.sum((residuals / sigma)**2)
    dof = len(delta_h) - 1
    
    # P-value for α ≠ 0
    t_stat = alpha / sigma_alpha
    p_value = 2 * (1 - stats.t.cdf(abs(t_stat), dof))
    
    # 95% upper limit
    upper_95 = alpha + 1.645 * sigma_alpha
    
    return {
        'alpha': alpha,
        'sigma_alpha': sigma_alpha,
        'chi2': chi2,
        'dof': dof,
        'chi2_red': chi2 / dof,
        'p_value': p_value,
        'upper_95': upper_95
    }

def compare_models(delta_h, delta_phi, sigma, alpha_ssz):
    """Compare M₀, M_SSZ, and M_anom models."""
    n = len(delta_h)
    w = 1 / sigma**2
    
    # M₀: ΔΦ = 0
    chi2_0 = np.sum((delta_phi / sigma)**2)
    
    # M_SSZ: ΔΦ = α_SSZ × Δh
    pred_ssz = alpha_ssz * delta_h
    chi2_ssz = np.sum(((delta_phi - pred_ssz) / sigma)**2)
    
    # M_anom: ΔΦ = α × Δh (fit)
    alpha_fit = np.sum(w * delta_h * delta_phi) / np.sum(w * delta_h**2)
    pred_anom = alpha_fit * delta_h
    chi2_anom = np.sum(((delta_phi - pred_anom) / sigma)**2)
    
    # AIC
    aic_0 = chi2_0
    aic_ssz = chi2_ssz
    aic_anom = 2 + chi2_anom
    
    # Likelihood ratio test: M₀ vs M_anom
    lr_stat = chi2_0 - chi2_anom
    lr_pvalue = 1 - stats.chi2.cdf(lr_stat, 1)
    
    return {
        'chi2_M0': chi2_0,
        'chi2_MSSZ': chi2_ssz,
        'chi2_Manom': chi2_anom,
        'aic_M0': aic_0,
        'aic_MSSZ': aic_ssz,
        'aic_Manom': aic_anom,
        'best_model': ['M0', 'MSSZ', 'Manom'][np.argmin([aic_0, aic_ssz, aic_anom])],
        'lr_pvalue': lr_pvalue,
        'alpha_fit': alpha_fit
    }
```

---

## G.10 Reporting Standards

Results should include:
1. **Slope estimate**: α = X ± Y rad/m
2. **Confidence interval**: 95% CI: [A, B] rad/m
3. **Upper limit** (if non-detection): α < Z rad/m (95% CL)
4. **Model comparison**: ΔAIC between M₀ and M_anom
5. **SSZ consistency**: |α - α_SSZ| / σ_α
