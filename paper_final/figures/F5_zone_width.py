"""
Figure F5: Segment-Coherent Zone Width z(ε)
Shows zone width as function of phase tolerance
"""
import numpy as np
import matplotlib.pyplot as plt

# Constants
r_s = 8.87e-3  # Earth Schwarzschild radius [m]
R = 6.371e6    # Earth radius [m]

# Zone width formula: z(ε) = 4ε × R² / r_s
def zone_width(epsilon):
    return 4 * epsilon * R**2 / r_s

# Tolerance range
epsilon = np.logspace(-20, -10, 100)

z = zone_width(epsilon)

fig, ax = plt.subplots(figsize=(10, 6))

ax.loglog(epsilon, z * 1e6, 'b-', lw=2)  # Convert to μm

# Reference lines
ax.axhline(1, color='gray', ls='--', label='1 μm (lithography limit)')
ax.axhline(1000, color='orange', ls='--', label='1 mm (chip scale)')
ax.axhline(1e6, color='green', ls='--', label='1 m (cryostat scale)')

# Tolerance annotations
tolerances = [
    (1e-18, 'Quantum error correction\n(ε = 10⁻¹⁸)'),
    (1e-15, 'High-fidelity gates\n(ε = 10⁻¹⁵)'),
    (1e-12, 'Standard gates\n(ε = 10⁻¹²)'),
]

for eps, label in tolerances:
    z_val = zone_width(eps) * 1e6
    ax.plot(eps, z_val, 'ro', markersize=8)
    ax.annotate(label, xy=(eps, z_val), xytext=(eps*5, z_val*0.3),
                fontsize=9, arrowprops=dict(arrowstyle='->', color='red', lw=0.5))

ax.set_xlabel('Phase Tolerance ε [rad]', fontsize=12)
ax.set_ylabel('Coherent Zone Width z(ε) [μm]', fontsize=12)
ax.set_title('Segment-Coherent Zone Width\nz(ε) = 4ε R² / r_s', fontsize=14)
ax.legend(loc='upper left')
ax.grid(True, alpha=0.3)

# Add formula box
textstr = r'$z(\varepsilon) = \frac{4\varepsilon R^2}{r_s}$'
props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
ax.text(0.95, 0.05, textstr, transform=ax.transAxes, fontsize=14,
        verticalalignment='bottom', horizontalalignment='right', bbox=props)

plt.tight_layout()
plt.savefig('F5_zone_width.png', dpi=300, bbox_inches='tight')
plt.savefig('F5_zone_width.pdf', bbox_inches='tight')
print("Saved: F5_zone_width.png/pdf")
