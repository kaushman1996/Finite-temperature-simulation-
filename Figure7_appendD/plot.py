import matplotlib.pyplot as plt
import numpy as np
import glob
import os
import matplotlib as mpl
import re

# -------------------------
# Matplotlib style
# -------------------------
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Times New Roman"],
    "font.size": 16.5
})

# -------------------------
# Directories
# -------------------------
dirs = {
    "LR": "LR",
    "NN": "NN"
}

# -------------------------
# J colormap setup
# -------------------------
J_min = 0
J_max = 3

cm = plt.get_cmap('viridis')

def get_color_for_J(J_val):
    normalized = (min(max(J_val, J_min), J_max) - J_min) / (J_max - J_min)
    return cm(normalized)

# -------------------------
# Figure
# -------------------------
fig, axs = plt.subplots(2, 2, figsize=(8, 6))

# -------------------------
# CV plotting (UPDATED)
# -------------------------
def plot_dir(ax, base_dir, show_ylabel=False):
    file_list = glob.glob(os.path.join(base_dir, "cv_J*_Nsample.txt"))

    files_with_J = []
    for fname in file_list:
        base = os.path.basename(fname)

        match = re.search(r'cv_J([0-9.]+)_Nsample\.txt', base)
        if not match:
            continue

        J_val = float(match.group(1))

        if J_val <= J_max:
            files_with_J.append((J_val, fname))

    files_with_J.sort(key=lambda x: x[0])

    # store peaks ONLY for t=0 and t=1.8
    selected_peaks = {}

    for J_val, fname in files_with_J:
        try:
            data = np.loadtxt(fname)
        except Exception:
            continue

        T = data[:, 0]
        Cv = data[:, 1]

        ax.plot(T, Cv, color=get_color_for_J(J_val))

        # -------------------------
        # ONLY TWO SPECIAL t VALUES
        # -------------------------
        if np.isclose(J_val, 0.0, atol=1e-6) or np.isclose(J_val, 1.8, atol=1e-6):

            peak_idx = np.argmax(Cv)
            T_peak = T[peak_idx]

            selected_peaks[J_val] = (T_peak, Cv[peak_idx])

            ax.scatter(T_peak, Cv[peak_idx],
                       color=get_color_for_J(J_val),
                       s=30,
                       zorder=4)

    # axis limits
    ax.set_xlim(11, 100)
    ax.set_ylim(0.09, 0.38)

    if show_ylabel:
        ax.set_ylabel('$C_v/N$')

    # -------------------------
    # DRAW ONLY TWO VERTICAL LINES
    # -------------------------
    for J_val, (T_peak, Cv_peak) in selected_peaks.items():
        ax.axvline(T_peak,
                   color=get_color_for_J(J_val),
                   linestyle='--',
                   linewidth=2.0)


# -------------------------
# Tc plotting
# -------------------------
def plot_Tc(ax, base_dir, show_ylabel=False, show_xlabel=False):
    fname = os.path.join(base_dir, "Tc.txt")

    if not os.path.exists(fname):
        print(f"Missing {fname}")
        return

    data = np.loadtxt(fname)

    t = data[:, 0]
    Tc = data[:, 1]

    Tc0 = Tc[0]
    Tc_norm = (Tc - Tc0) / Tc0

    ax.plot(t, Tc_norm, marker='o', color='black')

    # green dotted line
    ax.axvline(1.8, color='green', linestyle=':', linewidth=1.5)

    if show_xlabel:
        ax.set_xlabel('$t$ (meV)')

    if show_ylabel:
        ax.set_ylabel(r'$(T_c(t) - T_c(0))/T_c(0)$')


# -------------------------
# Top row (Cv)
# -------------------------
plot_dir(axs[0, 0], dirs["LR"], show_ylabel=True)
plot_dir(axs[0, 1], dirs["NN"], show_ylabel=False)

axs[0, 0].set_title(r'$n = 2/5,\ N = 25,\ \mathrm{LR}$')
axs[0, 1].set_title(r'$n = 2/5,\ N = 25,\ \mathrm{NN}$')

axs[0, 0].set_xlabel(r'$T_c(K)$')
axs[0, 1].set_xlabel(r'$T_c(K)$')

# -------------------------
# Bottom row (Tc normalized)
# -------------------------
plot_Tc(axs[1, 0], dirs["LR"], show_ylabel=True, show_xlabel=True)
plot_Tc(axs[1, 1], dirs["NN"], show_ylabel=False, show_xlabel=True)

# -------------------------
# Colorbar
# -------------------------
norm = mpl.colors.Normalize(vmin=J_min, vmax=J_max)
sm = mpl.cm.ScalarMappable(cmap=cm, norm=norm)
sm.set_array([])

cbar = fig.colorbar(sm, ax=axs, orientation='vertical', fraction=0.04, pad=0.32)
cbar.ax.set_title('$t$ (meV)', fontsize=16, pad=10)
labels = ['$(a)$', '$(b)$', '$(c)$', '$(d)$']
for i, (ax, label) in enumerate(zip(axs.flat, labels)):
    if i < 2:  # top row: (a), (b)
        ax.text(0.85, 0.95, label,
                transform=ax.transAxes,
                fontsize=20, fontweight='bold',
                va='top')
    else:      # bottom row: (c), (d)
        ax.text(0.02, 0.95, label,
                transform=ax.transAxes,
                fontsize=20, fontweight='bold',
                va='top')

# -------------------------
# Layout
# -------------------------
plt.tight_layout(rect=[0, 0, 0.85, 1])
fig.subplots_adjust(wspace=0.15, hspace=0.35)

# -------------------------
# Save + show
# -------------------------
plt.savefig('Figure_2_5.pdf')
plt.show()
