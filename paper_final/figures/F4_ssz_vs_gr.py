"""
Figure F4: SSZ vs GR Time Dilation Comparison
Shows equivalence in weak field, divergence in strong field
"""
import numpy as np
import matplotlib.pyplot as plt

# Constants
phi = 1.618033988749895  # Golden ratio

def ssz_weak(r, r_s):
    """SSZ time dilation in weak field: D = 1/(1 + Xi), Xi = r_s/(2r)"""
    xi = r_s / (2 * r)
    return 1 / (1 + xi)

def ssz_strong(r, r_s):
    """SSZ time dilation in strong field: D = 1/(1 + Xi), Xi = 1 - exp(-phi*r/r_s)"""
    xi = 1 - np.exp(-phi * r / r_s)
    return 1 / (1 + xi)

def gr_schwarzschild(r, r_s):
    """GR Schwarzschild: D = sqrt(1 - r_s/r)"""
    with np.errstate(invalid='ignore'):
        result = np.sqrt(np.maximum(0, 1 - r_s / r))
    return result

# Normalized radius range
r_norm = np.logspace(-0.5, 3, 500)  # 0.3 to 1000 × r_s

# Calculate
D_gr = gr_schwarzschild(r_norm, 1)
D_ssz_weak = ssz_weak(r_norm, 1)
D_ssz_strong = ssz_strong(r_norm, 1)

# Blend SSZ weak/strong at r/r_s = 100
blend_center = 100
blend_width = 20
blend = 1 / (1 + np.exp(-(r_norm - blend_center) / blend_width))
D_ssz = blend * D_ssz_weak + (1 - blend) * D_ssz_strong

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Left: Full range
ax1.semilogx(r_norm, D_gr, 'b-', lw=2, label='GR (Schwarzschild)')
ax1.semilogx(r_norm, D_ssz, 'r--', lw=2, label='SSZ (blended)')
ax1.axvline(1, color='gray', ls=':', label='Horizon (r = r_s)')
ax1.axvline(100, color='orange', ls=':', alpha=0.5, label='Weak/Strong boundary')

ax1.set_xlabel('r / r_s', fontsize=12)
ax1.set_ylabel('Time Dilation D', fontsize=12)
ax1.set_title('Time Dilation: SSZ vs GR', fontsize=14)
ax1.legend(loc='lower right')
ax1.grid(True, alpha=0.3)
ax1.set_ylim(0, 1.05)

# Highlight key difference
ax1.annotate('GR: D → 0\nSSZ: D → 0.556', xy=(1, 0.1), xytext=(3, 0.3),
             fontsize=10, arrowprops=dict(arrowstyle='->', color='purple'))

# Right: Weak field zoom (Earth surface region)
r_earth = np.linspace(0.99, 1.01, 100) * 6.371e6 / 8.87e-3  # Around Earth surface in r/r_s
D_gr_earth = gr_schwarzschild(r_earth, 1)
D_ssz_earth = ssz_weak(r_earth, 1)

# Difference
diff = np.abs(D_ssz_earth - D_gr_earth)

ax2.plot(r_earth / 1e9, D_gr_earth, 'b-', lw=2, label='GR')
ax2.plot(r_earth / 1e9, D_ssz_earth, 'r--', lw=2, label='SSZ')
ax2.set_xlabel('r / r_s [×10⁹]', fontsize=12)
ax2.set_ylabel('Time Dilation D', fontsize=12)
ax2.set_title('Weak Field (Earth Surface): SSZ ≈ GR', fontsize=14)
ax2.legend()
ax2.grid(True, alpha=0.3)

# Add difference inset
ax2_inset = ax2.inset_axes([0.55, 0.1, 0.4, 0.35])
ax2_inset.plot(r_earth / 1e9, diff, 'purple', lw=1.5)
ax2_inset.set_ylabel('|SSZ - GR|', fontsize=8)
ax2_inset.set_xlabel('r/r_s [×10⁹]', fontsize=8)
ax2_inset.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
ax2_inset.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('F4_ssz_vs_gr.png', dpi=300, bbox_inches='tight')
plt.savefig('F4_ssz_vs_gr.pdf', bbox_inches='tight')
print("Saved: F4_ssz_vs_gr.png/pdf")
