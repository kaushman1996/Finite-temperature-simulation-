import matplotlib.pyplot as plt
import numpy as np
import glob
import os
import matplotlib as mpl
import re
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Times New Roman"],
    "font.size": 16.5
})

# Directories
dirs = {
    "LR": "LR_N_28",
    "NN": "NN_N_28"
}

# J range for colormap
J_min = 0
J_max = 3  # maximum J considered

# Colormap function
cm = plt.get_cmap('viridis')
def get_color_for_J(J_val):
    normalized = (min(max(J_val, J_min), J_max) - J_min) / (J_max - J_min)
    return cm(normalized)

# Create small 2x1 figure
fig, axs = plt.subplots(2, 1, figsize=(4, 5), sharex=True)
axs[0].tick_params(axis='both', which='major', labelsize=10)
axs[1].tick_params(axis='both', which='major', labelsize=10)

# Plotting function with sorted J
tick_label_size = 16  # adjust as needed
axs[0].tick_params(axis='both', which='major', labelsize=tick_label_size)
axs[1].tick_params(axis='both', which='major', labelsize=tick_label_size)
import re

def plot_dir(ax, base_dir, title):
    file_list = glob.glob(os.path.join(base_dir, "cv_J*_Nsample.txt"))

    files_with_J = []

    for fname in file_list:
        base = os.path.basename(fname)

        # extract J value
        match = re.search(r'cv_J([0-9.]+)\_Nsample.txt', base)
        if not match:
            continue

        J_val = float(match.group(1))

        if J_val <= J_max:
            files_with_J.append((J_val, fname))

    files_with_J.sort(key=lambda x: x[0])

    for J_val, fname in files_with_J:
        data = np.loadtxt(fname)
        x = data[:,0]
        y = data[:,1]

        color = get_color_for_J(J_val)
        ax.plot(x, y, color=color)

    ax.set_ylabel('$C_v/N$', fontsize=16)
    ax.set_title(title, fontsize=16)
    ax.set_xlim(20, 100)
    ax.set_ylim(0.1, 0.24)


    ax.text(0.95, 0.85, r'$n = 1/2$', transform=ax.transAxes,
            fontsize=16, ha='right', va='top',
            bbox=dict(facecolor='white', alpha=0.6, edgecolor='none'))

# Plot LR and NN
plot_dir(axs[0], dirs["LR"], "$N = 28$, Long range")
plot_dir(axs[1], dirs["NN"], "$N = 28, V_1$ model")

# Shared X-label
axs[1].set_xlabel('$T_c(K)$ ')

# Add colorbar for J values
norm = mpl.colors.Normalize(vmin=J_min, vmax=J_max)
sm = mpl.cm.ScalarMappable(cmap=cm, norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, ax=axs, orientation='vertical', fraction=0.05, pad=-0.15)
cbar.set_label('J value', fontsize=16)

plt.tight_layout(rect=[0, 0, 0.95, 1])
plt.savefig('Figure2.pdf')

plt.show()
