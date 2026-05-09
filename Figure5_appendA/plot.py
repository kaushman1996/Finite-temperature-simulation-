import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Times New Roman"],
    "font.size": 20.5
})      
            
K_PER_UNIT = 11.6*1441.2/(7.98*4.665)
def load_and_scale(filename, N):
    data = np.loadtxt(filename)
    T = data[:, 0] * K_PER_UNIT
    cv = data[:, 1] / N
    return T, cv
            
def Tc_from_peak(T, cv):
    return T[np.argmax(cv)]
        
MARKERS = ["o", "s", "^", "D", "v", "P", "X", "<", ">"]

# --- reordered panels ---
panels = [
    dict(filling=r"$n=1/7$", datasets=[
        dict(fname="n_1_7_N_14X14.txt", L=14),
        dict(fname="n_1_7_N_21X21.txt", L=21),
        dict(fname="n_1_7_N_28X28.txt", L=28),
        dict(fname="n_1_7_N_35X35.txt", L=35),
    ]),  
    dict(filling=r"$n=1/4$", datasets=[
        dict(fname="n_1_4_N_16X16.txt", L=16),
        dict(fname="n_1_4_N_20X20.txt", L=20),
        dict(fname="n_1_4_N_24X24.txt", L=24),
        dict(fname="n_1_4_N_30X30.txt", L=30),
    ]),     
    dict(filling=r"$n=2/5$", datasets=[
        dict(fname="n_2_5_N_20X20.txt", L=20),
        dict(fname="n_2_5_N_25X25.txt", L=25),
        dict(fname="n_2_5_N_30X30.txt", L=30),
    ]),         
    dict(filling=r"$n=1/2$", datasets=[
        dict(fname="n_1_2_N_12X12.txt", L=12),
        dict(fname="n_1_2_N_16X16.txt", L=16),
        dict(fname="n_1_2_N_20X20.txt", L=20),
        dict(fname="n_1_2_N_24X24.txt", L=24),
        dict(fname="n_1_2_N_30X30.txt", L=30),
    ]), 
]

# no shared axes
fig, axes = plt.subplots(2, 2, figsize=(10, 8))

for idx, (ax, panel) in enumerate(zip(axes.flat, panels)):

    rows = []

    for j, ds in enumerate(panel["datasets"]):
        L = ds["L"]
        N = L * L
        T, cv = load_and_scale(ds["fname"], N)
        Tc = Tc_from_peak(T, cv)

        marker = MARKERS[j % len(MARKERS)]

        (line,) = ax.plot(
            T, cv,
            lw=2,
            ls=ds.get("ls", "-"),
            marker=marker,
            markersize=3,
        )

        rows.append(dict(
            size_str=rf"${L}\times{L}$",
            Tc=Tc,
            marker=marker,
            color=line.get_color(),
            fname=ds["fname"],
        ))

    # ---------- TABLE ----------
    cell_text = [["", r["size_str"], f"{r['Tc']:.2f}"] for r in rows]
    # shift table slightly right only for 1/7
    if panel["filling"] == r"$n=1/7$":
        tbx = [0.3, 0.6, 0.63, 0.35]  # moved x0 from 0.2 → 0.3
    else:
        tbx = [0.35, 0.5, 0.63, 0.42]

    table = ax.table(
        cellText=cell_text,
        colLabels=[panel["filling"], r"$N$", r"$T_c$ (K)"],
        colLoc="center",
        cellLoc="center",
        bbox=tbx,
    )
    table.auto_set_font_size(False)
    table.set_fontsize(17)

    # markers inside table
    x0, y0, w, h = tbx
    nrows = len(rows) + 1
    row_h = h / nrows
    marker_x = x0 + w / 6

    for r_i, r in enumerate(rows, start=1):
        y_center = y0 + h - (r_i + 0.5) * row_h
        ax.scatter(
            [marker_x], [y_center],
            transform=ax.transAxes,
            marker=r["marker"],
            s=45,
            color=r["color"],
            zorder=10
        )

    # ---------- labels & axes ----------
    # x-axis label only for bottom row
    if idx >= 2:  
        ax.set_xlabel(r"$T$ (K)")
    # y-axis label only for left column
    if idx % 2 == 0:
        ax.set_ylabel(r"$C_v/N$")
    # set x-limits
    if panel["filling"] == r"$n=1/7$":
        ax.set_xlim(5, 20)
    else:
        ax.set_xlim(5, 41)

# bottom-right panel → hide offset text
for ax in axes.flat:
    ax.ticklabel_format(axis='y', style='plain', useOffset=False)
    ax.yaxis.get_offset_text().set_visible(False)
labels = ['$(a)$', '$(b)$', '$(c)$', '$(d)$']

for ax, label in zip(axes.flat, labels):
    ax.text(0.05, 0.95, label, transform=ax.transAxes,
            fontsize=24, fontweight='bold', va='top')
plt.subplots_adjust(hspace=0.15, wspace=0.14)
plt.savefig("Classical_cv_2x2_first_xlim0_30_table_right.pdf")
plt.show()
