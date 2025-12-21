"""
Figure F6: With/Without Compensation Protocol
Shows phase evolution and fidelity with and without SSZ compensation
"""
import numpy as np
import matplotlib.pyplot as plt

# Constants
r_s = 8.87e-3
R = 6.371e6
omega = 2 * np.pi * 429e12  # Optical clock
dh = 1.0  # 1 meter

# Time range
t = np.linspace(0, 2, 1000)  # 2 seconds

# Phase drift without compensation
delta_D = r_s * dh / R**2
phi_drift = omega * delta_D * t

# With compensation: drift is cancelled
phi_compensated = np.zeros_like(t)

# Fidelity: F = (1 + cos(ΔΦ)) / 2
F_without = (1 + np.cos(phi_drift)) / 2
F_with = np.ones_like(t)  # Perfect fidelity

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Top left: Phase accumulation
ax1 = axes[0, 0]
ax1.plot(t, phi_drift, 'r-', lw=2, label='Without compensation')
ax1.plot(t, phi_compensated, 'g-', lw=2, label='With compensation')
ax1.set_xlabel('Time [s]', fontsize=11)
ax1.set_ylabel('Phase Drift ΔΦ [rad]', fontsize=11)
ax1.set_title('Phase Accumulation (Δh = 1 m, 429 THz)', fontsize=12)
ax1.legend()
ax1.grid(True, alpha=0.3)

# Top right: Fidelity
ax2 = axes[0, 1]
ax2.plot(t, F_without, 'r-', lw=2, label='Without compensation')
ax2.plot(t, F_with, 'g-', lw=2, label='With compensation')
ax2.axhline(0.9, color='orange', ls='--', lw=1, label='90% fidelity threshold')
ax2.set_xlabel('Time [s]', fontsize=11)
ax2.set_ylabel('Bell State Fidelity F', fontsize=11)
ax2.set_title('Entanglement Fidelity', fontsize=12)
ax2.legend(loc='lower left')
ax2.grid(True, alpha=0.3)
ax2.set_ylim(0, 1.05)

# Bottom left: Protocol diagram
ax3 = axes[1, 0]
ax3.axis('off')

protocol_text = """
WITH/WITHOUT COMPENSATION PROTOCOL

┌─────────────────────────────────────────────────┐
│  Step 1: Prepare Bell state |Φ⁺⟩ = (|00⟩+|11⟩)/√2 │
│          at heights h and h+Δh                    │
├─────────────────────────────────────────────────┤
│  Step 2: WITHOUT compensation                     │
│          • Let evolve for time t                  │
│          • Measure phase via tomography           │
│          • Record ΔΦ_measured                     │
├─────────────────────────────────────────────────┤
│  Step 3: WITH compensation                        │
│          • Apply Φ_corr = -ω(r_s·Δh/R²)t         │
│          • Let evolve for time t                  │
│          • Measure phase                          │
│          • Expect ΔΦ ≈ 0                          │
├─────────────────────────────────────────────────┤
│  Step 4: Compare                                  │
│          • If SSZ correct: Φ_with ≈ 0            │
│          • Confounds: Φ_with ≠ 0                 │
│          • Randomize run order                    │
└─────────────────────────────────────────────────┘
"""
ax3.text(0.05, 0.95, protocol_text, transform=ax3.transAxes, fontsize=10,
         verticalalignment='top', family='monospace',
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))
ax3.set_title('Protocol Steps', fontsize=12)

# Bottom right: Discrimination power
ax4 = axes[1, 1]
effects = ['SSZ Drift', 'Thermal', 'LO Noise', 'Vibration']
reversal = [1.0, 0.0, 0.0, 0.0]
colors = ['green', 'red', 'red', 'red']

bars = ax4.barh(effects, reversal, color=colors, edgecolor='black')
ax4.set_xlabel('Compensation Reversal', fontsize=11)
ax4.set_title('Key Discriminator: Only SSZ Reverses', fontsize=12)
ax4.set_xlim(0, 1.2)
ax4.axvline(0.5, color='gray', ls='--', alpha=0.5)

for bar, val in zip(bars, reversal):
    label = 'YES' if val > 0.5 else 'NO'
    ax4.text(val + 0.05, bar.get_y() + bar.get_height()/2, 
             label, va='center', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig('F6_compensation.png', dpi=300, bbox_inches='tight')
plt.savefig('F6_compensation.pdf', bbox_inches='tight')
print("Saved: F6_compensation.png/pdf")
