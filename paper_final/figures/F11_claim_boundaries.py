"""
Figure F11: Claim Boundaries Visualization
Shows the three regimes: Bounded, Detection, Future
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch
import matplotlib.patches as mpatches

fig, ax = plt.subplots(figsize=(16, 9))

# Define the three regimes as columns
regime_data = [
    {
        'name': 'BOUNDED REGIME',
        'subtitle': 'Today\'s Superconducting Qubits',
        'x_center': 2.5,
        'color': '#E74C3C',
        'delta_h': '~mm',
        'platform': 'Transmon, Fluxonium',
        'signal': '~10⁻¹³ rad',
        'noise': '~1 rad',
        'snr': '10⁻¹²',
        'result': 'Null Result\n= SSZ Consistent',
        'icon': '❌',
    },
    {
        'name': 'DETECTION REGIME',
        'subtitle': 'Optical Atomic Clocks',
        'x_center': 8,
        'color': '#27AE60',
        'delta_h': '~m',
        'platform': 'Sr/Yb Optical Clocks',
        'signal': '~0.6 rad',
        'noise': '~10⁻³ rad',
        'snr': '~600',
        'result': 'Direct Detection\n+ Compensation Test',
        'icon': '✓',
    },
    {
        'name': 'FUTURE REGIME',
        'subtitle': 'Quantum Networks & Satellites',
        'x_center': 13.5,
        'color': '#3498DB',
        'delta_h': '~km',
        'platform': 'Satellite QKD, ISS',
        'signal': '~10⁵ rad/s',
        'noise': 'N/A',
        'snr': '∞',
        'result': 'Engineering\nConstraint',
        'icon': '⚙',
    },
]

# Draw regime boxes
for regime in regime_data:
    x = regime['x_center']
    
    # Main box
    box = FancyBboxPatch((x - 2.3, 1), 4.6, 7.5, 
                          boxstyle="round,pad=0.1",
                          facecolor=regime['color'], alpha=0.15,
                          edgecolor=regime['color'], lw=3)
    ax.add_patch(box)
    
    # Title
    ax.text(x, 8.2, regime['name'], ha='center', va='bottom',
            fontsize=14, fontweight='bold', color=regime['color'])
    ax.text(x, 7.8, regime['subtitle'], ha='center', va='top',
            fontsize=10, style='italic', color='gray')
    
    # Content rows
    rows = [
        ('Height Δh:', regime['delta_h']),
        ('Platform:', regime['platform']),
        ('Signal:', regime['signal']),
        ('Noise:', regime['noise']),
        ('SNR:', regime['snr']),
    ]
    
    y_pos = 6.8
    for label, value in rows:
        ax.text(x - 2, y_pos, label, ha='left', va='center', fontsize=10)
        ax.text(x + 2, y_pos, value, ha='right', va='center', fontsize=10, fontweight='bold')
        y_pos -= 0.8
    
    # Result box
    result_box = FancyBboxPatch((x - 2, 1.3), 4, 1.8, 
                                 boxstyle="round,pad=0.05",
                                 facecolor=regime['color'], alpha=0.3,
                                 edgecolor=regime['color'], lw=2)
    ax.add_patch(result_box)
    ax.text(x, 2.2, regime['result'], ha='center', va='center',
            fontsize=11, fontweight='bold', color=regime['color'])

# Draw arrows between regimes
arrow_style = dict(arrowstyle='->', color='gray', lw=2, 
                   connectionstyle='arc3,rad=0')
ax.annotate('', xy=(5.5, 4.5), xytext=(4.8, 4.5),
            arrowprops=arrow_style)
ax.annotate('', xy=(11, 4.5), xytext=(10.3, 4.5),
            arrowprops=arrow_style)

# Arrow labels
ax.text(5.15, 5.2, 'Higher ω\nLarger Δh', ha='center', fontsize=9, color='gray')
ax.text(10.65, 5.2, 'Larger Δh\nLonger t', ha='center', fontsize=9, color='gray')

# Title
ax.text(8, 9.5, 'SSZ Claim Boundaries: Three Distinct Regimes', 
        ha='center', va='center', fontsize=18, fontweight='bold')

# Formula at bottom
formula_text = r'$\Delta\Phi = \omega \cdot \frac{r_s \cdot \Delta h}{R^2} \cdot t$'
ax.text(8, 0.3, f'Phase Drift Formula:  {formula_text}', ha='center', fontsize=12,
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

# Key message
key_msg = "Key Insight: Null results in Bounded Regime CONFIRM SSZ predictions (not falsify them)"
ax.text(8, -0.3, key_msg, ha='center', fontsize=11, style='italic', color='#2C3E50')

ax.set_xlim(0, 16)
ax.set_ylim(-0.5, 10)
ax.set_aspect('equal')
ax.axis('off')

plt.tight_layout()
plt.savefig('F11_claim_boundaries.png', dpi=300, bbox_inches='tight')
plt.savefig('F11_claim_boundaries.pdf', bbox_inches='tight')
print("Saved: F11_claim_boundaries.png/pdf")
