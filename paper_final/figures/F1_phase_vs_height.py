"""
Figure F1: Phase Drift vs Height - ENHANCED VERSION
Shows the 12 orders of magnitude gap between transmon signal and noise
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import matplotlib.patches as mpatches

# Constants
r_s = 8.87e-3  # Earth Schwarzschild radius [m]
R = 6.371e6    # Earth radius [m]

# Platform parameters: (name, omega, t, color, marker)
platforms = [
    ('Transmon (5 GHz, 100 μs)', 2*np.pi*5e9, 100e-6, '#E74C3C', 'o'),
    ('Trapped Ion (10 MHz, 10 s)', 2*np.pi*10e6, 10, '#F39C12', 's'),
    ('NV Center (3 GHz, 1 ms)', 2*np.pi*3e9, 1e-3, '#9B59B6', '^'),
    ('Optical Clock (429 THz, 1 s)', 2*np.pi*429e12, 1, '#27AE60', 'D'),
    ('Optical Clock (429 THz, 10 s)', 2*np.pi*429e12, 10, '#2ECC71', 'v'),
]

# Noise floors
noise_floors = {
    'Transmon': 1.0,
    'Trapped Ion': 0.01,
    'NV Center': 0.01,
    'Optical Clock': 1e-3,
}

# Height range
dh = np.logspace(-4, 2, 200)  # 0.1 mm to 100 m

def phase_drift(omega, dh, t):
    return omega * (r_s * dh / R**2) * t

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

# === LEFT PANEL: Full comparison ===
for name, omega, t, color, marker in platforms:
    phi = phase_drift(omega, dh, t)
    ax1.loglog(dh * 1000, phi, '-', lw=2.5, color=color, label=name)

# Noise floor lines
ax1.axhline(1, color='#E74C3C', ls='--', lw=1.5, alpha=0.7)
ax1.axhline(0.01, color='#9B59B6', ls='--', lw=1.5, alpha=0.7)
ax1.axhline(1e-3, color='#27AE60', ls='--', lw=1.5, alpha=0.7)

# Add noise labels
ax1.text(12000, 1.5, 'Transmon noise (~1 rad)', fontsize=9, color='#E74C3C')
ax1.text(12000, 0.015, 'Ion/NV noise (~10⁻² rad)', fontsize=9, color='#9B59B6')
ax1.text(12000, 1.5e-3, 'Optical noise (~10⁻³ rad)', fontsize=9, color='#27AE60')

# Regime shading
ax1.axvspan(0.1, 100, alpha=0.08, color='orange')
ax1.axvspan(100, 100000, alpha=0.08, color='green')

# Labels
ax1.text(3, 1e-16, 'BOUNDED\nREGIME', fontsize=11, fontweight='bold', 
         color='#E67E22', ha='center')
ax1.text(3000, 1e-16, 'DETECTION\nREGIME', fontsize=11, fontweight='bold', 
         color='#27AE60', ha='center')

ax1.set_xlabel('Height Difference Δh [mm]', fontsize=13)
ax1.set_ylabel('Phase Drift ΔΦ [rad]', fontsize=13)
ax1.set_title('SSZ Phase Drift: Platform Comparison', fontsize=14, fontweight='bold')
ax1.legend(loc='lower right', fontsize=10, framealpha=0.95)
ax1.grid(True, alpha=0.3, which='both')
ax1.set_xlim(0.1, 100000)
ax1.set_ylim(1e-17, 100)

# === RIGHT PANEL: The 12 Orders of Magnitude Gap ===
# Focus on transmon at 1mm
dh_focus = 1e-3  # 1 mm
t_focus = 100e-6  # 100 μs
omega_transmon = 2*np.pi*5e9

ssz_signal = phase_drift(omega_transmon, dh_focus, t_focus)
noise = 1.0

# Create bar comparison
categories = ['SSZ Signal\n(Δh=1mm, t=100μs)', 'Noise Floor\n(T₂ limited)']
values = [ssz_signal, noise]
colors = ['#3498DB', '#E74C3C']

bars = ax2.bar(categories, values, color=colors, edgecolor='black', lw=2)
ax2.set_yscale('log')

# Add value annotations
ax2.text(0, ssz_signal * 3, f'{ssz_signal:.2e} rad', ha='center', fontsize=12, fontweight='bold')
ax2.text(1, noise * 2, f'{noise:.0f} rad', ha='center', fontsize=12, fontweight='bold')

# Add the gap annotation with arrow
gap = noise / ssz_signal
ax2.annotate('', xy=(0.5, ssz_signal), xytext=(0.5, noise),
             arrowprops=dict(arrowstyle='<->', color='purple', lw=3))
ax2.text(0.7, 1e-6, f'12 ORDERS\nOF MAGNITUDE\nGAP', fontsize=14, fontweight='bold',
         color='purple', ha='left', va='center',
         bbox=dict(boxstyle='round', facecolor='white', edgecolor='purple', alpha=0.9))

# Add interpretation box
interp_text = """Interpretation:
• SSZ predicts signal ~10⁻¹³ rad
• Transmon noise floor ~1 rad
• Signal-to-Noise Ratio = 10⁻¹²
• Detection IMPOSSIBLE with current technology
• This is SSZ-CONSISTENT (not falsifying!)"""

props = dict(boxstyle='round', facecolor='lightyellow', alpha=0.9, edgecolor='orange')
ax2.text(0.02, 0.02, interp_text, transform=ax2.transAxes, fontsize=10,
         verticalalignment='bottom', bbox=props, family='sans-serif')

ax2.set_ylabel('Phase [rad]', fontsize=13)
ax2.set_title('The 12 Orders of Magnitude Gap\n(Transmon at 1mm height difference)', 
              fontsize=14, fontweight='bold')
ax2.set_ylim(1e-15, 10)
ax2.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('F1_phase_vs_height.png', dpi=300, bbox_inches='tight')
plt.savefig('F1_phase_vs_height.pdf', bbox_inches='tight')
print("Saved: F1_phase_vs_height.png/pdf (ENHANCED)")
