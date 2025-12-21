"""
Figure F7: SSZ vs GR in Strong Field
Shows divergence near compact objects
"""
import numpy as np
import matplotlib.pyplot as plt

# Golden ratio
PHI = 1.618033988749895

def gr_time_dilation(r_norm):
    """GR Schwarzschild: D = sqrt(1 - 1/x) where x = r/r_s"""
    with np.errstate(invalid='ignore', divide='ignore'):
        result = np.sqrt(np.maximum(0, 1 - 1/r_norm))
    return result

def ssz_time_dilation(r_norm):
    """SSZ with weak/strong blend"""
    result = np.zeros_like(r_norm)
    
    # Strong field (x < 90)
    strong = r_norm < 90
    xi_s = 1 - np.exp(-PHI * r_norm[strong])
    result[strong] = 1 / (1 + xi_s)
    
    # Weak field (x > 110)
    weak = r_norm > 110
    xi_w = 1 / (2 * r_norm[weak])
    result[weak] = 1 / (1 + xi_w)
    
    # Transition (90 <= x <= 110)
    trans = ~strong & ~weak
    t = (r_norm[trans] - 90) / 20
    b = 6*t**5 - 15*t**4 + 10*t**3
    xi_w_t = 1 / (2 * r_norm[trans])
    xi_s_t = 1 - np.exp(-PHI * r_norm[trans])
    xi_blend = b * xi_w_t + (1 - b) * xi_s_t
    result[trans] = 1 / (1 + xi_blend)
    
    return result

# Radius range (in units of r_s)
r_norm = np.logspace(-0.3, 3, 500)  # 0.5 to 1000 r_s

D_gr = gr_time_dilation(r_norm)
D_ssz = ssz_time_dilation(r_norm)

# Difference
diff = D_ssz - D_gr
rel_diff = np.abs(diff) / np.maximum(D_gr, 1e-10) * 100

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Top left: Full comparison
ax1 = axes[0, 0]
ax1.semilogx(r_norm, D_gr, 'b-', lw=2, label='GR (Schwarzschild)')
ax1.semilogx(r_norm, D_ssz, 'r--', lw=2, label='SSZ')
ax1.axvline(1, color='purple', ls=':', lw=1.5, label='Horizon (r = r_s)')
ax1.axvline(100, color='orange', ls=':', alpha=0.5, label='Transition zone')
ax1.fill_betweenx([0, 1.1], 90, 110, alpha=0.1, color='orange')
ax1.set_xlabel('r / r_s', fontsize=12)
ax1.set_ylabel('Time Dilation D', fontsize=12)
ax1.set_title('Time Dilation: SSZ vs GR (Full Range)', fontsize=14)
ax1.legend(loc='lower right')
ax1.grid(True, alpha=0.3)
ax1.set_ylim(0, 1.05)
ax1.set_xlim(0.5, 1000)

# Top right: Near horizon zoom
ax2 = axes[0, 1]
r_near = np.linspace(0.5, 5, 200)
D_gr_near = gr_time_dilation(r_near)
D_ssz_near = ssz_time_dilation(r_near)

ax2.plot(r_near, D_gr_near, 'b-', lw=2, label='GR')
ax2.plot(r_near, D_ssz_near, 'r--', lw=2, label='SSZ')
ax2.axvline(1, color='purple', ls=':', lw=1.5)
ax2.set_xlabel('r / r_s', fontsize=12)
ax2.set_ylabel('Time Dilation D', fontsize=12)
ax2.set_title('Near-Horizon Region', fontsize=14)
ax2.legend()
ax2.grid(True, alpha=0.3)

# Annotate key values
ax2.annotate(f'GR: D = 0\nSSZ: D = {D_ssz_near[np.argmin(np.abs(r_near-1))]:.3f}', 
             xy=(1, 0.3), xytext=(2, 0.5),
             fontsize=10, arrowprops=dict(arrowstyle='->', color='black'))

# Bottom left: Relative difference
ax3 = axes[1, 0]
ax3.semilogx(r_norm, rel_diff, 'g-', lw=2)
ax3.axhline(1, color='gray', ls='--', label='1% difference')
ax3.axhline(10, color='orange', ls='--', label='10% difference')
ax3.set_xlabel('r / r_s', fontsize=12)
ax3.set_ylabel('|SSZ - GR| / GR [%]', fontsize=12)
ax3.set_title('Relative Difference', fontsize=14)
ax3.legend()
ax3.grid(True, alpha=0.3)
ax3.set_ylim(0, 100)
ax3.set_xlim(0.5, 1000)

# Bottom right: Astrophysical objects
ax4 = axes[1, 1]
objects = [
    ('Earth surface', 7.2e8, 'green'),
    ('Sun surface', 2.4e5, 'yellow'),
    ('White dwarf', 1000, 'cyan'),
    ('Neutron star', 2.5, 'orange'),
    ('BH photon sphere', 1.5, 'red'),
    ('BH horizon', 1.0, 'purple'),
]

for name, r_rs, color in objects:
    ax4.axvline(r_rs, color=color, ls='-', lw=2, label=name)

ax4.set_xscale('log')
ax4.set_xlim(0.5, 1e9)
ax4.set_ylim(0, 1)
ax4.set_xlabel('r / r_s', fontsize=12)
ax4.set_title('Astrophysical Objects by Compactness', fontsize=14)
ax4.legend(loc='upper left', fontsize=9)

# Add regime labels
ax4.text(3e8, 0.5, 'Weak Field\n(SSZ = GR)', ha='center', fontsize=10)
ax4.text(50, 0.5, 'Transition', ha='center', fontsize=10)
ax4.text(1.2, 0.5, 'Strong Field\n(SSZ != GR)', ha='center', fontsize=10, rotation=90)

plt.tight_layout()
plt.savefig('F7_strong_field.png', dpi=300, bbox_inches='tight')
plt.savefig('F7_strong_field.pdf', bbox_inches='tight')
print("Saved: F7_strong_field.png/pdf")
