"""
Figure F2: Platform Feasibility Comparison
Bar chart showing signal-to-noise for different platforms
"""
import numpy as np
import matplotlib.pyplot as plt

# Platform data: [name, ΔΦ_signal, noise_floor, color]
platforms = [
    ('Transmon\n(1mm, 100μs)', 6.9e-13, 1.0, 'orange'),
    ('Trapped Ion\n(1mm, 1ms)', 8.8e-12, 0.1, 'orange'),
    ('NV Center\n(1mm, 1ms)', 4.0e-12, 0.01, 'orange'),
    ('Optical Clock\n(1m, 1s)', 0.59, 1e-3, 'green'),
    ('Optical Clock\n(10cm, 1s)', 0.059, 1e-3, 'green'),
    ('Future Optical\n(1mm, 10s)', 1.4e-4, 1e-5, 'blue'),
]

names = [p[0] for p in platforms]
signals = [p[1] for p in platforms]
noises = [p[2] for p in platforms]
colors = [p[3] for p in platforms]
snr = [s/n for s, n in zip(signals, noises)]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Left: Signal vs Noise
x = np.arange(len(names))
width = 0.35

bars1 = ax1.bar(x - width/2, signals, width, label='SSZ Signal', color='steelblue')
bars2 = ax1.bar(x + width/2, noises, width, label='Noise Floor', color='salmon')

ax1.set_yscale('log')
ax1.set_ylabel('Phase [rad]', fontsize=12)
ax1.set_title('SSZ Signal vs Noise Floor', fontsize=14)
ax1.set_xticks(x)
ax1.set_xticklabels(names, fontsize=9)
ax1.legend()
ax1.grid(True, alpha=0.3, axis='y')
ax1.axhline(1, color='gray', ls='--', lw=0.5)

# Right: SNR with regime colors
bars3 = ax2.bar(x, snr, color=colors, edgecolor='black')
ax2.axhline(1, color='red', ls='--', lw=2, label='Detection threshold (SNR=1)')
ax2.axhline(10, color='green', ls='--', lw=2, label='Strong detection (SNR=10)')

ax2.set_yscale('log')
ax2.set_ylabel('Signal-to-Noise Ratio', fontsize=12)
ax2.set_title('Detectability by Platform', fontsize=14)
ax2.set_xticks(x)
ax2.set_xticklabels(names, fontsize=9)
ax2.legend(loc='upper left')
ax2.grid(True, alpha=0.3, axis='y')

# Add regime labels
for i, (bar, c) in enumerate(zip(bars3, colors)):
    regime = {'orange': 'Bounded', 'green': 'Detectable', 'blue': 'Future'}[c]
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height()*1.5, 
             regime, ha='center', va='bottom', fontsize=8, rotation=45)

plt.tight_layout()
plt.savefig('F2_platform_comparison.png', dpi=300, bbox_inches='tight')
plt.savefig('F2_platform_comparison.pdf', bbox_inches='tight')
print("Saved: F2_platform_comparison.png/pdf")
