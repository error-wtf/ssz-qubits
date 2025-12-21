"""
Figure F10: Quantum Network with SSZ Compensation
Schematic diagram of SSZ-aware network architecture
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(14, 10))

# Define node positions (x, y, height_m, name)
nodes = [
    (2, 8, 0, 'Node A\n(Sea level)'),
    (6, 8, 10, 'Node B\n(h = 10 m)'),
    (10, 8, 50, 'Node C\n(h = 50 m)'),
    (4, 5, 5, 'Node D\n(h = 5 m)'),
    (8, 5, 100, 'Node E\n(h = 100 m)'),
    (6, 2, 0, 'Central\nController'),
]

# Draw nodes
for x, y, h, name in nodes:
    # Color based on height
    if h == 0:
        color = '#3498db'
    elif h < 20:
        color = '#2ecc71'
    elif h < 60:
        color = '#f39c12'
    else:
        color = '#e74c3c'
    
    circle = plt.Circle((x, y), 0.6, color=color, ec='black', lw=2, zorder=5)
    ax.add_patch(circle)
    ax.text(x, y - 1.2, name, ha='center', va='top', fontsize=9)

# Draw links with SSZ compensation annotations
links = [
    (0, 1, 10),   # A-B: 10 m difference
    (1, 2, 40),   # B-C: 40 m difference
    (0, 3, 5),    # A-D: 5 m difference
    (3, 4, 95),   # D-E: 95 m difference
    (1, 3, 5),    # B-D: 5 m difference
    (2, 4, 50),   # C-E: 50 m difference (negative)
]

for i, j, dh in links:
    x1, y1 = nodes[i][0], nodes[i][1]
    x2, y2 = nodes[j][0], nodes[j][1]
    
    # Line color based on SSZ drift magnitude
    # drift ~ 0.59 * dh rad/s for optical
    drift = 0.59 * dh
    if drift < 5:
        lcolor = 'green'
    elif drift < 30:
        lcolor = 'orange'
    else:
        lcolor = 'red'
    
    ax.plot([x1, x2], [y1, y2], color=lcolor, lw=2, zorder=1)
    
    # Annotation at midpoint
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    ax.text(mx, my + 0.3, f'Δh={dh}m\nΔΦ≈{drift:.0f} rad/s', 
            fontsize=7, ha='center', va='bottom',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# Draw controller connections
for i in range(5):
    x1, y1 = nodes[i][0], nodes[i][1]
    x2, y2 = nodes[5][0], nodes[5][1]
    ax.plot([x1, x2], [y1, y2], 'k--', lw=1, alpha=0.3, zorder=0)

# Add protocol stack box
stack_box = FancyBboxPatch((10.5, 3), 3, 6, boxstyle="round,pad=0.1",
                            facecolor='lightyellow', edgecolor='black', lw=2)
ax.add_patch(stack_box)

stack_layers = [
    ('Application', 8.3),
    ('SSZ Compensation', 7.3),
    ('Entanglement', 6.3),
    ('Physical', 5.3),
]
for name, y in stack_layers:
    ax.text(12, y, name, ha='center', va='center', fontsize=10, fontweight='bold')
    if y > 5.3:
        ax.plot([10.7, 13.3], [y - 0.4, y - 0.4], 'k-', lw=0.5)

ax.text(12, 9.2, 'Protocol Stack', ha='center', fontsize=11, fontweight='bold')

# Add legend
legend_elements = [
    mpatches.Patch(color='#3498db', label='Sea level (h = 0)'),
    mpatches.Patch(color='#2ecc71', label='Low (h < 20 m)'),
    mpatches.Patch(color='#f39c12', label='Medium (20 < h < 60 m)'),
    mpatches.Patch(color='#e74c3c', label='High (h > 60 m)'),
    plt.Line2D([0], [0], color='green', lw=2, label='Low SSZ (< 5 rad/s)'),
    plt.Line2D([0], [0], color='orange', lw=2, label='Medium SSZ (5-30 rad/s)'),
    plt.Line2D([0], [0], color='red', lw=2, label='High SSZ (> 30 rad/s)'),
]
ax.legend(handles=legend_elements, loc='lower left', fontsize=9)

# Add title and labels
ax.set_title('SSZ-Aware Quantum Network Architecture', fontsize=14, fontweight='bold')
ax.set_xlim(0, 14)
ax.set_ylim(0, 10)
ax.set_aspect('equal')
ax.axis('off')

# Add formula box
formula = r'$\Phi_{corr} = -\omega \cdot \frac{r_s \cdot \Delta h}{R^2} \cdot t$'
ax.text(1, 1, f'SSZ Compensation:\n{formula}', fontsize=10,
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.9),
        transform=ax.transData)

plt.tight_layout()
plt.savefig('F10_network.png', dpi=300, bbox_inches='tight')
plt.savefig('F10_network.pdf', bbox_inches='tight')
print("Saved: F10_network.png/pdf")
