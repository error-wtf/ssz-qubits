"""
Figure F6: With/Without Compensation Protocol - ENHANCED VERSION
Shows phase evolution, fidelity, and Bloch sphere visualization
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch
from mpl_toolkits.mplot3d import Axes3D

# Constants
r_s = 8.87e-3
R = 6.371e6
omega = 2 * np.pi * 429e12  # Optical clock
dh = 1.0  # 1 meter

# Time range
t = np.linspace(0, 2, 1000)

# Phase drift without compensation
delta_D = r_s * dh / R**2
phi_drift = omega * delta_D * t

# With compensation
phi_compensated = np.zeros_like(t)

# Fidelity
F_without = (1 + np.cos(phi_drift)) / 2
F_with = np.ones_like(t)

fig = plt.figure(figsize=(16, 12))

# === Top Left: Phase accumulation ===
ax1 = fig.add_subplot(2, 3, 1)
ax1.plot(t, phi_drift, 'r-', lw=2.5, label='Without compensation')
ax1.plot(t, phi_compensated, 'g-', lw=2.5, label='With compensation')
ax1.fill_between(t, 0, phi_drift, alpha=0.2, color='red')
ax1.set_xlabel('Time [s]', fontsize=11)
ax1.set_ylabel('Phase Drift ΔΦ [rad]', fontsize=11)
ax1.set_title('Phase Accumulation\n(Δh = 1 m, 429 THz Optical Clock)', fontsize=12, fontweight='bold')
ax1.legend(loc='upper left')
ax1.grid(True, alpha=0.3)

# Add rate annotation
rate = phi_drift[-1] / t[-1]
ax1.text(1.5, phi_drift[int(len(t)*0.75)], f'Rate: {rate:.2f} rad/s', 
         fontsize=10, color='red', fontweight='bold')

# === Top Middle: Fidelity ===
ax2 = fig.add_subplot(2, 3, 2)
ax2.plot(t, F_without, 'r-', lw=2.5, label='Without compensation')
ax2.plot(t, F_with, 'g-', lw=2.5, label='With compensation')
ax2.axhline(0.9, color='orange', ls='--', lw=1.5, label='90% threshold')
ax2.axhline(0.5, color='gray', ls=':', lw=1, label='Classical limit')
ax2.fill_between(t, F_without, 1, alpha=0.2, color='red')
ax2.set_xlabel('Time [s]', fontsize=11)
ax2.set_ylabel('Bell State Fidelity', fontsize=11)
ax2.set_title('Entanglement Fidelity', fontsize=12, fontweight='bold')
ax2.legend(loc='lower left', fontsize=9)
ax2.grid(True, alpha=0.3)
ax2.set_ylim(0, 1.05)

# === Top Right: Bloch Sphere Visualization ===
ax3 = fig.add_subplot(2, 3, 3, projection='3d')

# Draw Bloch sphere wireframe
u = np.linspace(0, 2 * np.pi, 50)
v = np.linspace(0, np.pi, 50)
x_sphere = np.outer(np.cos(u), np.sin(v))
y_sphere = np.outer(np.sin(u), np.sin(v))
z_sphere = np.outer(np.ones(np.size(u)), np.cos(v))
ax3.plot_wireframe(x_sphere, y_sphere, z_sphere, color='lightgray', alpha=0.3, linewidth=0.5)

# Draw equator and axes
theta_eq = np.linspace(0, 2*np.pi, 100)
ax3.plot(np.cos(theta_eq), np.sin(theta_eq), np.zeros_like(theta_eq), 'k-', lw=1, alpha=0.5)
ax3.plot([-1.2, 1.2], [0, 0], [0, 0], 'k-', lw=0.5, alpha=0.5)
ax3.plot([0, 0], [-1.2, 1.2], [0, 0], 'k-', lw=0.5, alpha=0.5)
ax3.plot([0, 0], [0, 0], [-1.2, 1.2], 'k-', lw=0.5, alpha=0.5)

# Draw state evolution WITHOUT compensation (drifting around equator)
phases = np.linspace(0, phi_drift[-1], 50)
x_drift = np.cos(phases)
y_drift = np.sin(phases)
z_drift = np.zeros_like(phases)
ax3.plot(x_drift, y_drift, z_drift, 'r-', lw=3, label='Without comp.')
ax3.scatter([x_drift[-1]], [y_drift[-1]], [z_drift[-1]], color='red', s=100, marker='o')

# Draw state WITH compensation (stays at start)
ax3.scatter([1], [0], [0], color='green', s=150, marker='*', label='With comp.')

# Labels
ax3.set_xlabel('X')
ax3.set_ylabel('Y')
ax3.set_zlabel('Z')
ax3.set_title('Bloch Sphere\n(State Evolution)', fontsize=12, fontweight='bold')
ax3.legend(loc='upper left', fontsize=9)

# Set view angle
ax3.view_init(elev=20, azim=45)

# === Bottom Left: Protocol Steps ===
ax4 = fig.add_subplot(2, 3, 4)
ax4.axis('off')

steps = [
    ('1', 'PREPARE', 'Bell state |Φ⁺⟩ = (|00⟩+|11⟩)/√2\nat heights h and h+Δh', '#3498DB'),
    ('2', 'EVOLVE (A)', 'WITHOUT compensation\nMeasure phase drift ΔΦ_measured', '#E74C3C'),
    ('3', 'EVOLVE (B)', 'WITH compensation Φ_corr\nExpect ΔΦ ≈ 0', '#27AE60'),
    ('4', 'COMPARE', 'If SSZ: Δ(A) matches prediction,\nΔ(B) ≈ 0', '#9B59B6'),
]

y_positions = [0.85, 0.6, 0.35, 0.1]
for (num, title, desc, color), y in zip(steps, y_positions):
    # Step number circle
    circle = plt.Circle((0.05, y + 0.05), 0.04, color=color, transform=ax4.transAxes)
    ax4.add_patch(circle)
    ax4.text(0.05, y + 0.05, num, transform=ax4.transAxes, ha='center', va='center',
             fontsize=12, fontweight='bold', color='white')
    # Title and description
    ax4.text(0.12, y + 0.08, title, transform=ax4.transAxes, fontsize=11, 
             fontweight='bold', color=color)
    ax4.text(0.12, y - 0.02, desc, transform=ax4.transAxes, fontsize=9)

ax4.set_title('Protocol Steps', fontsize=12, fontweight='bold')

# === Bottom Middle: Discrimination Power ===
ax5 = fig.add_subplot(2, 3, 5)

effects = ['SSZ Drift', 'Thermal\nGradient', 'LO Phase\nNoise', 'Vibration', 'Magnetic\nDrift']
reversal = [1.0, 0.0, 0.0, 0.0, 0.0]
height_scaling = [1.0, 0.3, 0.0, 0.2, 0.4]
frequency_scaling = [1.0, 0.2, 0.5, 0.0, 0.1]

x = np.arange(len(effects))
width = 0.25

bars1 = ax5.bar(x - width, reversal, width, label='Compensation Reversal', color='#27AE60')
bars2 = ax5.bar(x, height_scaling, width, label='Height Scaling', color='#3498DB')
bars3 = ax5.bar(x + width, frequency_scaling, width, label='Frequency Scaling', color='#E74C3C')

ax5.set_ylabel('Signature Strength', fontsize=11)
ax5.set_xticks(x)
ax5.set_xticklabels(effects, fontsize=9)
ax5.set_title('Discrimination Signatures\n(SSZ vs Confounds)', fontsize=12, fontweight='bold')
ax5.legend(loc='upper right', fontsize=8)
ax5.set_ylim(0, 1.3)
ax5.grid(True, alpha=0.3, axis='y')

# Highlight SSZ
ax5.annotate('SSZ: All signatures = 1', xy=(0, 1.1), fontsize=10, 
             fontweight='bold', color='#27AE60')

# === Bottom Right: Key Result ===
ax6 = fig.add_subplot(2, 3, 6)
ax6.axis('off')

result_text = """
┌─────────────────────────────────────────────┐
│           KEY DISCRIMINATOR                 │
├─────────────────────────────────────────────┤
│                                             │
│   Compensation Reversal:                    │
│                                             │
│   • SSZ: Apply Φ_corr → drift cancels       │
│                                             │
│   • Confounds: Apply Φ_corr → no effect     │
│                                             │
│   ─────────────────────────────────────     │
│                                             │
│   IF drift cancels exactly with SSZ         │
│   formula, THEN gravitational coupling      │
│   is confirmed.                             │
│                                             │
│   IF drift persists, THEN confound          │
│   dominates.                                │
│                                             │
└─────────────────────────────────────────────┘
"""

ax6.text(0.5, 0.5, result_text, transform=ax6.transAxes, fontsize=10,
         verticalalignment='center', horizontalalignment='center',
         family='monospace', 
         bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor='orange', alpha=0.9))

ax6.set_title('Why Compensation Matters', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('F6_compensation.png', dpi=300, bbox_inches='tight')
plt.savefig('F6_compensation.pdf', bbox_inches='tight')
print("Saved: F6_compensation.png/pdf (ENHANCED)")
