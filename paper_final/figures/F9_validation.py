"""
Figure F9: Experimental Validation History
Shows precision improvement over time
"""
import numpy as np
import matplotlib.pyplot as plt

# Validation experiments
experiments = [
    # (name, year, height_m, precision, marker, color)
    ('Pound-Rebka', 1959, 22.5, 0.10, 'o', 'blue'),
    ('Hafele-Keating', 1971, 10000, 0.25, 's', 'green'),
    ('Gravity Probe A', 1976, 1e7, 7e-5, '^', 'red'),
    ('GPS (daily)', 1990, 2.02e7, 1e-10, 'D', 'purple'),
    ('Chou et al.', 2010, 0.33, 0.40, 'v', 'orange'),
    ('Bothwell et al.', 2022, 0.001, 1e-19, 'p', 'magenta'),
]

years = [e[1] for e in experiments]
heights = [e[2] for e in experiments]
precisions = [e[3] for e in experiments]
markers = [e[4] for e in experiments]
colors = [e[5] for e in experiments]

fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# Left: Precision vs Year
ax1 = axes[0]
for exp in experiments:
    ax1.semilogy(exp[1], exp[3], marker=exp[4], color=exp[5], 
                 markersize=12, label=exp[0])
ax1.set_xlabel('Year', fontsize=12)
ax1.set_ylabel('Relative Precision', fontsize=12)
ax1.set_title('Precision Improvement Over Time', fontsize=14)
ax1.legend(loc='upper right', fontsize=9)
ax1.grid(True, alpha=0.3)
ax1.set_xlim(1955, 2025)

# Add trend line
years_arr = np.array(years)
prec_arr = np.array(precisions)
z = np.polyfit(years_arr, np.log10(prec_arr), 1)
trend_years = np.linspace(1955, 2025, 100)
trend_prec = 10**(z[0] * trend_years + z[1])
ax1.semilogy(trend_years, trend_prec, 'k--', alpha=0.5, label='Trend')

# Middle: Height Range Tested
ax2 = axes[1]
for exp in experiments:
    ax2.semilogy(exp[1], exp[2], marker=exp[4], color=exp[5], 
                 markersize=12, label=exp[0])
ax2.set_xlabel('Year', fontsize=12)
ax2.set_ylabel('Height Difference Δh [m]', fontsize=12)
ax2.set_title('Height Range Tested', fontsize=14)
ax2.grid(True, alpha=0.3)
ax2.set_xlim(1955, 2025)
ax2.axhline(1, color='gray', ls='--', alpha=0.5)
ax2.text(1960, 1.5, '1 m', fontsize=9, color='gray')

# Right: SSZ Detection Capability
ax3 = axes[2]

# For each experiment, calculate SSZ drift that would be detectable
# SSZ drift = precision (if precision = noise floor)
# Detectable if SNR > 1, i.e., drift > noise

for exp in experiments:
    # Assume optical clock frequency for scaling
    # SSZ drift at height h: dphi ~ 0.59 * h rad (for 1m, 1s, 429 THz)
    ssz_drift = 0.59 * exp[2]  # rad at that height for 1s
    noise = exp[3] * 2 * np.pi  # Convert fractional to rad (rough)
    snr = ssz_drift / max(noise, 1e-20)
    
    color = 'green' if snr > 1 else 'red'
    ax3.semilogy(exp[1], snr, marker=exp[4], color=color, 
                 markersize=12, label=exp[0])

ax3.axhline(1, color='black', ls='-', lw=2, label='Detection threshold')
ax3.axhline(10, color='gray', ls='--', alpha=0.5)
ax3.set_xlabel('Year', fontsize=12)
ax3.set_ylabel('Signal-to-Noise Ratio', fontsize=12)
ax3.set_title('SSZ Detection Capability', fontsize=14)
ax3.grid(True, alpha=0.3)
ax3.set_xlim(1955, 2025)

# Add legend with color coding
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='green', 
           markersize=10, label='Detectable (SNR > 1)'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='red', 
           markersize=10, label='Bounded (SNR < 1)'),
]
ax3.legend(handles=legend_elements, loc='lower right', fontsize=9)

plt.tight_layout()
plt.savefig('F9_validation.png', dpi=300, bbox_inches='tight')
plt.savefig('F9_validation.pdf', bbox_inches='tight')
print("Saved: F9_validation.png/pdf")
