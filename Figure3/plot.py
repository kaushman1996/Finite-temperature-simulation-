import numpy as np
import matplotlib.pyplot as plt
import os

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Times New Roman"],
    "font.size": 16,
    "axes.linewidth": 1.2,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.major.size": 5,
    "ytick.major.size": 5
})

fig, ax = plt.subplots(4, 3, figsize=(13, 8), sharex=True, constrained_layout=True)

bases = {
    "n_1_3": "n_1_3",
    "n_1_2": "n_1_2",
    "n_1_4": "n_1_4"
}

models = {
    "LR": "LR_eps_4.67",
    "NN": "NN"
}

for col, (filling, root) in enumerate(bases.items()):

    row = 0

    for model, folder in models.items():

        base = os.path.join(root, folder)

        # =========================
        # Tc plots
        # =========================

        if filling == "n_1_3":

            data18 = np.loadtxt(os.path.join(base, "18site", "Tc_t.txt"))
            data27 = np.loadtxt(os.path.join(base, "27site", "Tc_t.txt"))
            data24 = np.loadtxt(os.path.join(base, "24site_", "Tc_t.txt"))


            J18, Tc18 = data18[:, 0], data18[:, 1]
            J27, Tc27 = data27[:, 0], data27[:, 1]
            J24, Tc24 = data24[:, 0], data24[:, 1]


            ax[row, col].plot(J18, (Tc18 - Tc18[0]) / Tc18[0],
                              'o-', color='red', lw=1.8, label=r"$N=18$")
            ax[row, col].plot(J24, (Tc24 - Tc24[0]) / Tc24[0],
                              's-', color='blue', lw=1.8, label=r"$N=24b$")
            ax[row, col].plot(J27, (Tc27 - Tc27[0]) / Tc27[0],
                              '^-', color='orange', lw=1.8, label=r"$N=27$")

            #ax[row, col].legend(loc='upper left')  # <-- add this lie
            ax[row, col].legend(loc='upper left', bbox_to_anchor=(0, 1))
            # ===== ADD FIT ONLY FOR NN =====
            if model == "NN":

                Tc0 = Tc27[0]   # use 27-site baseline

                Tc_class = 40.533
                V1 = 11.6 * 9

                t_fit = np.linspace(0, 3.0, 300)
                Tc_fit = Tc_class * (
                    1 - ( ((t_fit * 11.6) ** 2) / (Tc_class * V1))
                )

                Tc_fit_norm = (Tc_fit - Tc0) / Tc0

                ax[row, col].plot(
                    t_fit,
                    Tc_fit_norm,
                    '--',
                    color='black',
                    lw=2.2,
                    #label=r"$\left(- \frac{t^2}{T_{c}(0) V} \right)$"#, $V = 9$meV"
                    #label=r'Fit ($N=27$)'
                )

                """ax[row, col].text(
                    0.1, 0.1,
                    r"-- $-\frac{t^{2}}{T_{c,\mathrm{class}} V}$, $V=9\,\mathrm{meV}$",
                    fontsize=14,
                    bbox=dict(facecolor='white', edgecolor='black', boxstyle='round')
                )"""
                # small dashed line sample (acts like legend marker)
                ax[row, col].plot(
                    [0.08, 0.16], [0.14, 0.14],
                    transform=ax[row, col].transAxes,
                    linestyle='--',
                    color='black',
                    lw=2.2
                )
                # text label
                ax[row, col].text(
                    0.20, 0.14,
                    r"$-\frac{t^{2}}{T_{c}(0) V_1}$",#, $V=9\,\mathrm{meV}$",
                    transform=ax[row, col].transAxes,
                    fontsize=16,
                    va='center',
                    #bbox=dict(facecolor='white', edgecolor='black', boxstyle='round')
                )


            ax[row, col].set_ylim(-0.16, 0.2)

        elif filling == "n_1_2":

            files = [
                #("Tc_1_2_16_site.txt", 'o', 'red', r"$N=16$"),
                ("Tc_1_2_20site.txt", 'o', 'red', r"$N=20$"),
                ("Tc_1_2_24_site.txt", 's', 'blue', r"$N=24a$"),
                ("Tc_1_2_28_site.txt", '^', 'orange', r"$N=28$")

            ]

            for fname, marker, color, label in files:
                data = np.loadtxt(os.path.join(base, fname))
                J, Tc = data[:, 0], data[:, 1]

                ax[row, col].plot(J, (Tc - Tc[0]) / Tc[0],
                                  marker=marker, color=color, lw=1.8, label=label)
            if model == "NN":
                x_fit = np.linspace(0, 3, 200)
                y_fit = 0.097 * x_fit**2
                ax[row, col].plot(x_fit, y_fit, '--', color='black', lw=3, label=r"$0.097\,t^2$")
    
                ax[row, col].set_ylim(-0.15, 1.5)
                ax[row, col].legend()


            ax[row, col].set_ylim(-0.05, 1.4)


        elif filling == "n_1_4":

            files = [
                ("Tc_1_4_24_site.txt", 'o', 'red', r"$N=24a$"),
                ("Tc_1_4_32_site.txt", 's', 'blue', r"$N=32$"),
                ("Tc_1_4_36_site.txt", '^', 'orange', r"$N=36$")

            ]


            for fname, marker, color, label in files:
                data = np.loadtxt(os.path.join(base, fname))
                J, Tc = data[:, 0], data[:, 1]

                ax[row, col].plot(J, (Tc - Tc[0]) / Tc[0],
                                  marker=marker, color=color, lw=1.8, label=label)
            # ---- Add quadratic fit only for NN model ----
            if model == "NN":
                x_fit = np.linspace(0, 3, 200)
                y_fit = 0.077 * x_fit**2
                ax[row, col].plot(x_fit, y_fit, '--', color='black', lw=3, label=r"$0.077\,t^2$")
    
                ax[row, col].set_ylim(-0.15, 1.5)
                ax[row, col].legend()


            ax[row, col].set_ylim(-0.15, 1.5)

        ax[row, col].set_xlim(0, 3)

        if col == 0:
            ax[row, col].set_ylabel(r'$\frac{T_c(t)-T_c(0)}{T_c(0)}$')

        ax[row, col].legend(loc='upper left',frameon=False, fontsize=14)

        if row == 0:
            if filling == "n_1_3":
                ax[row, col].set_title(r"$n=1/3$")
            elif filling == "n_1_2":
                ax[row, col].set_title(r"$n=1/2$")
            else:
                ax[row, col].set_title(r"$n=1/4$")

        # =========================
        # spectrum plots
        # =========================

        if filling == "n_1_3":

            spec = np.loadtxt(os.path.join(base, "24site_", "spectrum_data.txt"))
            J_spec, dE = spec[:, 0], spec[:, 1]

            ax[row+1, col].scatter(J_spec, dE, s=12, color='black')

            ax[row+1, col].text(
                0.05, 0.85, r"$N=24b$",
                transform=ax[row+1, col].transAxes,
                bbox=dict(facecolor='white', edgecolor='black', boxstyle='round')
            )

        if filling == "n_1_4":

            spec = np.loadtxt(os.path.join(base, "spectrum_vs_J_24site.txt"))
            J_spec, dE = spec[:, 0], spec[:, 1]

            ax[row+1, col].scatter(J_spec, dE, s=12, color='black')

            ax[row+1, col].text(
                0.05, 0.85, r"$N=24a$",
                transform=ax[row+1, col].transAxes,
                bbox=dict(facecolor='white', edgecolor='black', boxstyle='round')
            )
        if filling == "n_1_2":

            spec = np.loadtxt(os.path.join(base, "spectrum_20site.txt"))
            J_spec, dE = spec[:, 0], spec[:, 1]

            ax[row+1, col].scatter(J_spec, dE, s=12, color='black')

            ax[row+1, col].text(
                0.05, 0.85, r"$N=20$",
                transform=ax[row+1, col].transAxes,
                bbox=dict(facecolor='white', edgecolor='black', boxstyle='round')
            )


        #"""else:
        """if filling == "n_1_2":
            spec = np.loadtxt(os.path.join(base, "spectrum_vs_J.txt"))

            J = spec[:, 0]
            spectrum = spec[:, 1:]

            E0 = spectrum[:, 0][:, None]
            deltaE = spectrum - E0

            for i in range(deltaE.shape[1]):
                ax[row+1, col].scatter(J, deltaE[:, i], s=10, color='black')

            ax[row+1, col].text(
                0.05, 0.35, r"$N=16$",
                transform=ax[row+1, col].transAxes,
                bbox=dict(facecolor='white', edgecolor='black', boxstyle='round')
            )"""

        # ===== LABELS =====
        if filling == "n_1_3" and model == "LR":
            ax[row+1, col].annotate(
                r"$\mathrm{LR}\   \uparrow \rightarrow   $",
                xy=(1.5, 4),
                xytext=(0.4, 6),
                fontsize=18,
            )

        if filling == "n_1_3" and model == "NN":
            ax[row+1, col].annotate(
                r"$\mathrm{NN}\   \uparrow \rightarrow   $",
                xy=(1.5, 4),
                xytext=(0.4, 2),
                fontsize=18,
            )

        ax[row+1, col].set_ylim(0, 12)

        if col == 0:
            ax[row+1, col].set_ylabel(r'$\Delta E$ (meV)')

        row += 2

# ===== AFTER ALL LOOPS =====
for i in range(ax.shape[0]):
    for j in range(ax.shape[1]):
        ax[i, j].axvline(1.81, color='green', linestyle=':', lw=2)

# x-labels
for c in range(3):
    ax[-1, c].set_xlabel(r"$t$ (meV)")
# x-labels
for c in range(3):
    ax[-1, c].set_xlabel(r"$t$ (meV)")

plt.savefig("combined_figure_3col.pdf", dpi=300, bbox_inches="tight")
plt.show()
