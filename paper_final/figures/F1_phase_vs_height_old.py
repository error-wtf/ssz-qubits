"""
Figure F1: Phase Drift vs Height Difference
Shows ΔΦ as function of Δh for transmon and optical clock
"""
import numpy as np
import matplotlib.pyplot as plt

# Constants
r_s = 8.87e-3  # Earth Schwarzschild radius [m]
R = 6.371e6    # Earth radius [m]

# Frequencies
omega_transmon = 2 * np.pi * 5e9      # 5 GHz
omega_optical = 2 * np.pi * 429e12    # 429 THz

# Times
t_transmon = 100e-6  # 100 μs
t_optical = 1.0      # 1 s

# Height range
dh = np.logspace(-4, 1, 100)  # 0.1 mm to 10 m

# Phase drift: ΔΦ = ω × (r_s × Δh / R²) × t
def phase_drift(omega, dh, t):
    return omega * (r_s * dh / R**2) * t

phi_transmon = phase_drift(omega_transmon, dh, t_transmon)
phi_optical = phase_drift(omega_optical, dh, t_optical)

# Plot
fig, ax = plt.subplots(figsize=(10, 6))

ax.loglog(dh * 1000, phi_transmon, 'b-', lw=2, label='Transmon (5 GHz, 100 μs)')
ax.loglog(dh * 1000, phi_optical, 'r-', lw=2, label='Optical Clock (429 THz, 1 s)')

# Detection threshold
ax.axhline(1, color='gray', ls='--', lw=1, label='Transmon noise floor (~1 rad)')
ax.axhline(1e-3, color='gray', ls=':', lw=1, label='Optical clock noise (~10⁻³ rad)')

# Regime annotations
ax.axvspan(0.1, 10, alpha=0.1, color='orange', label='Bounded regime')
ax.axvspan(100, 10000, alpha=0.1, color='green', label='Detection regime')

ax.set_xlabel('Height Difference Δh [mm]', fontsize=12)
ax.set_ylabel('Phase Drift ΔΦ [rad]', fontsize=12)
ax.set_title('SSZ Phase Drift vs Height Difference', fontsize=14)
ax.legend(loc='lower right', fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_xlim(0.1, 10000)
ax.set_ylim(1e-15, 100)

plt.tight_layout()
plt.savefig('F1_phase_vs_height.png', dpi=300, bbox_inches='tight')
plt.savefig('F1_phase_vs_height.pdf', bbox_inches='tight')
print("Saved: F1_phase_vs_height.png/pdf")
