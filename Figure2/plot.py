import matplotlib.pyplot as plt
import numpy as np
import glob
import os
import matplotlib as mpl
import re

# ---------------- Matplotlib settings ---------------- #
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Times New Roman"],
    "font.size": 16.5
})

J_min = 0
J_max = 3
cm = plt.get_cmap('viridis')

def get_color_for_J(J_val):
    normalized = (min(max(J_val, J_min), J_max) - J_min) / (J_max - J_min)
    return cm(normalized)

# ---------------- Systems ---------------- #
systems = [
    ("n_1_3", "LR_N_27", "NN_N_27", r"$N=27$", r"$n=1/3$"),
    ("n_1_2", "LR_N_28", "NN_N_28", r"$N=28$", r"$n=1/2$"),
    ("n_1_4", "LR_36",   "NN_36",   r"$N=36$", r"$n=1/4$")
]

# ---------------- Figure and axes ---------------- #
fig, axs = plt.subplots(2, 3, figsize=(12, 6), sharex=True)

for ax in axs.flatten():
    ax.tick_params(axis='both', labelsize=12)

# ---------------- Functions ---------------- #
def extract_J(base):
    patterns = [
        r'cv_J([0-9.]+)',
        r'specific_heat_J([0-9.]+)',
        r'J([0-9.]+)'
    ]
    for p in patterns:
        m = re.search(p, base)
        if m:
            val = m.group(1).rstrip('.')
            try:
                return float(val)
            except:
                return None
    return None

def plot_dir(ax, base_dir, row_type, xlim_range, ylim_range,
             mark_peaks=False, special_files=None, add_label=False):

    file_list = glob.glob(os.path.join(base_dir, "*.txt"))
    files_with_J = []

    for fname in file_list:
        base = os.path.basename(fname)
        J_val = extract_J(base)
        if J_val is None or J_val > J_max:
            continue
        files_with_J.append((J_val, fname))

    files_with_J.sort(key=lambda x: x[0])

    for J_val, fname in files_with_J:
        data = np.loadtxt(fname)
        T = data[:, 0]
        Cv = data[:, 1]

        ax.plot(T, Cv, color=get_color_for_J(J_val))

        # ---- Case 1: general peak marking (for 1/2 and 1/4) ---- #
        if mark_peaks:
            if np.isclose(J_val, 0.0) or np.isclose(J_val, 1.8):
                peak_idx = np.argmax(Cv)
                T_peak = T[peak_idx]

                ax.axvline(T_peak,
                           color=get_color_for_J(J_val),
                           linestyle='--',
                           linewidth=1.5)

                ax.scatter(T_peak, Cv[peak_idx],
                           color=get_color_for_J(J_val),
                           s=25, zorder=3)

        # ---- Case 2: specific files (for 1/3) ---- #
        if special_files is not None:
            if os.path.basename(fname) in special_files:
                peak_idx = np.argmax(Cv)
                T_peak = T[peak_idx]

                ax.axvline(T_peak,
                           color=get_color_for_J(J_val),
                           linestyle='--',
                           linewidth=1.8)

                ax.scatter(T_peak, Cv[peak_idx],
                           color=get_color_for_J(J_val),
                           s=30, zorder=4)

    ax.set_xlim(*xlim_range)
    ax.set_ylim(*ylim_range)

    if add_label:
        if row_type == "LR":
            text_str = r"$\mathrm{LR},\ \epsilon = 4.67\ \rightarrow$"
        else:
            text_str = r"$\mathrm{NN},\\ V_1 = 9\ \mathrm{meV}\ \rightarrow$"

        ax.text(0.43, 0.96, text_str,
                transform=ax.transAxes,
                fontsize=15,
                ha='left', va='top',
                bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'))

# ---------------- Plotting loop ---------------- #
for col, (root, lr_dir, nn_dir, size_label, density_label) in enumerate(systems):
    lr_path = os.path.join(root, lr_dir)
    nn_path = os.path.join(root, nn_dir)

    # ----- X limits ----- #
    if col == 0:
        xlim_range = (20, 100)
    #if col == 1:
    #    xlim_range = (5, 100)

    #else:
    #    xlim_range = (20, 100)

    # ----- Y limits ----- #
    if col == 0:
        ylim_top = (0, 1)
        ylim_bottom = (0, 1)

    elif col == 1:
        ylim_top = (0.1, 0.25)
        ylim_bottom = (0.1, 0.21)


    else:
        ylim_top = (0.06, 0.32)
        ylim_bottom = (0.06, 0.26)

    # ---- Peak logic ---- #
    mark_peaks_flag = (col == 1 or col == 2)

    special_files_lr = None
    special_files_nn = None

    # ✅ Special handling for n = 1/3
    if col == 0:
        special_files_lr = ["cv_J1.8372_Nsample_200.txt", "cv_J0_Nsample_200.txt"]
        special_files_nn = ["cv_J1.8_Nsample_200.txt","cv_J0.0_Nsample_200.txt"]

    # ----- Top row (LR) ----- #
    print(col ,xlim_range)
    plot_dir(axs[0, col], lr_path, "LR",
             xlim_range, ylim_top,
             mark_peaks=mark_peaks_flag,
             special_files=special_files_lr,
             add_label=(col == 0))

    axs[0, col].set_title(f"{density_label}, {size_label}")

    # ----- Bottom row (NN) ----- #
    plot_dir(axs[1, col], nn_path, "NN",
             xlim_range, ylim_bottom,
             mark_peaks=mark_peaks_flag,
             special_files=special_files_nn,
             add_label=(col == 0))

# ---------------- Axis labels ---------------- #
for ax in axs[:, 0]:
    ax.set_ylabel(r"$C_v/N$")

for ax in axs[1, :]:
    ax.set_xlabel(r"$T \, (\mathrm{K})$")

# ---------------- Colorbar ---------------- #
norm = mpl.colors.Normalize(vmin=J_min, vmax=J_max)
sm = mpl.cm.ScalarMappable(cmap=cm, norm=norm)
sm.set_array([])

fig.subplots_adjust(right=0.88)
cbar_ax = fig.add_axes([0.91, 0.15, 0.02, 0.7])
cbar = fig.colorbar(sm, cax=cbar_ax)
cbar.ax.set_title('$t$ (meV)', fontsize=16, pad=10)
labels = ['$(a)$', '$(b)$', '$(c)$', '$(d)$', '$(e)$', '$(f)$']

for i, (ax, label) in enumerate(zip(axs.flat, labels)):
    if i in [1, 2]:  # (b), (c)
        ax.text(0.95, 0.95, label, transform=ax.transAxes,
                fontsize=17, va='top', ha='right')
    if i in [4, 5]:  # (b), (c)
        ax.text(0.95, 0.95, label, transform=ax.transAxes,
                fontsize=17, va='top', ha='right')
    if i in [0, 3]:  # (b), (c)
        ax.text(0.15, 0.95, label, transform=ax.transAxes,
                fontsize=17, va='top', ha='right')


# ---------------- Save and show ---------------- #
plt.savefig("Figure_combined.pdf", bbox_inches='tight')
plt.show()
