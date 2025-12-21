"""
Figure F8: SSZ Research Roadmap Timeline
Gantt-style visualization of milestones
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig, ax = plt.subplots(figsize=(14, 8))

# Define phases and milestones
phases = [
    # (name, start_year, duration, y_position, color)
    ('Phase 1: Foundation', 2025, 2, 7, '#2ecc71'),
    ('Phase 2: Validation', 2027, 2, 6, '#3498db'),
    ('Phase 3: Strong-Field', 2027, 6, 5, '#e74c3c'),
    ('Phase 4: Space', 2032, 8, 4, '#9b59b6'),
]

milestones = [
    # (name, year, y_position, color)
    ('Code v1.0', 2025, 7.3, '#2ecc71'),
    ('First compensation test', 2025.8, 7.3, '#2ecc71'),
    ('Two-site comparison', 2027, 6.3, '#3498db'),
    ('Network protocol', 2027.8, 6.3, '#3498db'),
    ('NS redshift (NICER)', 2027, 5.3, '#e74c3c'),
    ('Pulsar timing', 2028, 5.3, '#e74c3c'),
    ('BH shadow (ngEHT)', 2030, 5.3, '#e74c3c'),
    ('ISS optical clock', 2032, 4.3, '#9b59b6'),
    ('Dedicated satellite', 2035, 4.3, '#9b59b6'),
    ('Lunar comparison', 2038, 4.3, '#9b59b6'),
]

# Draw phases as horizontal bars
for name, start, duration, y, color in phases:
    ax.barh(y, duration, left=start, height=0.6, color=color, alpha=0.7, 
            edgecolor='black', linewidth=1)
    ax.text(start + duration/2, y, name, ha='center', va='center', 
            fontsize=10, fontweight='bold', color='white')

# Draw milestones as diamonds
for name, year, y, color in milestones:
    ax.scatter(year, y, marker='D', s=100, color=color, edgecolors='black', zorder=5)
    ax.annotate(name, xy=(year, y), xytext=(year, y + 0.4),
                fontsize=8, ha='center', rotation=45,
                arrowprops=dict(arrowstyle='-', color='gray', lw=0.5))

# Add vertical lines for key years
for year in [2025, 2030, 2035, 2040]:
    ax.axvline(year, color='gray', ls='--', alpha=0.5, lw=0.5)

# Formatting
ax.set_xlim(2024, 2041)
ax.set_ylim(3.5, 8)
ax.set_xlabel('Year', fontsize=12)
ax.set_title('SSZ Research Roadmap (2025-2040)', fontsize=14, fontweight='bold')

# Remove y-axis ticks
ax.set_yticks([])

# Add legend
legend_elements = [
    mpatches.Patch(color='#2ecc71', label='Foundation (Optical clocks)'),
    mpatches.Patch(color='#3498db', label='Validation (Networks)'),
    mpatches.Patch(color='#e74c3c', label='Strong-Field (Astrophysics)'),
    mpatches.Patch(color='#9b59b6', label='Space (Satellites)'),
]
ax.legend(handles=legend_elements, loc='upper left', fontsize=10)

# Add annotations for key capabilities
capabilities = [
    (2026, 2.8, 'First SSZ\ncompensation'),
    (2028, 2.8, 'Network\nprotocols'),
    (2032, 2.8, 'Space-based\ntests'),
    (2040, 2.8, 'Full\nvalidation'),
]
for year, y, text in capabilities:
    ax.annotate(text, xy=(year, 3.5), xytext=(year, y),
                fontsize=9, ha='center', va='top',
                arrowprops=dict(arrowstyle='->', color='black', lw=1))

ax.set_ylim(2.5, 8.5)

plt.tight_layout()
plt.savefig('F8_timeline.png', dpi=300, bbox_inches='tight')
plt.savefig('F8_timeline.pdf', bbox_inches='tight')
print("Saved: F8_timeline.png/pdf")
