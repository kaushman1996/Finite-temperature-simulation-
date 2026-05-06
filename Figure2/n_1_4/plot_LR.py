import matplotlib.pyplot as plt
import numpy as np
import glob
import os
import matplotlib as mpl

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Times New Roman"],
    "font.size": 16.5
})

# Directory (ONLY LR)
base_dir = "LR_32_"

# J range for colormap
J_min = 0
J_max = 3

# Colormap
cm = plt.get_cmap('viridis')
def get_color_for_J(J_val):
    normalized = (min(max(J_val, J_min), J_max) - J_min) / (J_max - J_min)
    return cm(normalized)

# Create figure (single panel)
fig, ax = plt.subplots(1, 1, figsize=(4, 3.5))

ax.tick_params(axis='both', which='major', labelsize=14)

# Get files and sort by J
file_list = glob.glob(os.path.join(base_dir, "cv_*.txt"))

files_with_J = []
for fname in file_list:
    base = os.path.basename(fname)
    J_val = float(base.split('_')[1].replace('J', ''))
    if J_val <= J_max:
        files_with_J.append((J_val, fname))

files_with_J.sort(key=lambda x: x[0])

# Plot
for J_val, fname in files_with_J:
    data = np.loadtxt(fname)
    x = data[:, 0]
    y = data[:, 1]
    color = get_color_for_J(J_val)
    ax.plot(x, y, color=color)

# Labels and styling
ax.set_ylabel(r'$C_v/N$', fontsize=16)
ax.set_xlabel(r'$T$ (K)', fontsize=16)
ax.set_title(r'$\epsilon = 4.6$, LR', fontsize=16)

ax.set_xlim(5, 100)

ax.text(0.95, 0.85, r'$n = 1/3$', transform=ax.transAxes,
        fontsize=14, ha='right', va='top',
        bbox=dict(facecolor='white', alpha=0.6, edgecolor='none'))

# Colorbar
norm = mpl.colors.Normalize(vmin=J_min, vmax=J_max)
sm = mpl.cm.ScalarMappable(cmap=cm, norm=norm)
sm.set_array([])

cbar = fig.colorbar(sm, ax=ax, orientation='vertical', fraction=0.05, pad=0.02)

# Put label on TOP
cbar.ax.set_title('$t (\r {meV})$', fontsize=14, pad=8)
plt.tight_layout()
plt.savefig('Figure_LR_only.pdf')
plt.show()
