"""
Figure F3: Confound Discrimination Matrix
Heatmap showing which signatures discriminate SSZ from confounds
"""
import numpy as np
import matplotlib.pyplot as plt

# Effects (rows)
effects = ['SSZ Drift', 'Thermal Gradient', 'LO Phase Noise', 
           'Vibration/Tilt', 'Magnetic Drift', 'Charge Noise']

# Signatures (columns)
signatures = ['Height\nScaling', 'Frequency\nScaling', 'Time\nScaling', 
              'Compensation\nReversal', 'Randomization\nInvariant']

# Matrix: 1 = discriminates SSZ, 0 = does not, 0.5 = partial
# Row = effect, Col = signature
# SSZ should be 1 where it's unique
matrix = np.array([
    [1, 1, 1, 1, 1],    # SSZ: all signatures work
    [0.3, 0.2, 0.8, 0, 0.5],  # Thermal: some overlap
    [0, 0.5, 0.5, 0, 0.8],    # LO noise
    [0.2, 0, 0.2, 0, 0.3],    # Vibration
    [0.4, 0.1, 0.7, 0, 0.6],  # Magnetic
    [0, 0.3, 0.5, 0, 0.7],    # Charge
])

fig, ax = plt.subplots(figsize=(10, 7))

im = ax.imshow(matrix, cmap='RdYlGn', aspect='auto', vmin=0, vmax=1)

# Labels
ax.set_xticks(np.arange(len(signatures)))
ax.set_yticks(np.arange(len(effects)))
ax.set_xticklabels(signatures, fontsize=11)
ax.set_yticklabels(effects, fontsize=11)

# Rotate x labels
plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

# Add values
for i in range(len(effects)):
    for j in range(len(signatures)):
        val = matrix[i, j]
        color = 'white' if val > 0.5 else 'black'
        text = '✓' if val == 1 else ('~' if val >= 0.5 else '✗')
        ax.text(j, i, text, ha="center", va="center", color=color, fontsize=14, fontweight='bold')

ax.set_title('Confound Discrimination Matrix\n(Green = SSZ distinguishable)', fontsize=14)

# Colorbar
cbar = ax.figure.colorbar(im, ax=ax, shrink=0.8)
cbar.set_label('Discrimination Power', fontsize=11)

# Highlight SSZ row
ax.add_patch(plt.Rectangle((-0.5, -0.5), len(signatures), 1, 
                            fill=False, edgecolor='blue', lw=3))
ax.text(-0.7, 0, '→', fontsize=16, color='blue', ha='right', va='center')

plt.tight_layout()
plt.savefig('F3_confound_matrix.png', dpi=300, bbox_inches='tight')
plt.savefig('F3_confound_matrix.pdf', bbox_inches='tight')
print("Saved: F3_confound_matrix.png/pdf")
