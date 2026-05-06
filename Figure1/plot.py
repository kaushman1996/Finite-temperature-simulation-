import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import networkx as nx
from mpl_toolkits.axes_grid1.inset_locator import inset_axes


# ---- global plot style ----
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Times New Roman"],
    "font.size": 20.5
})

SCALE = 1.0  # or 3.9/4.67 if needed

# ---- datasets grouped by filling ----
filling_datasets = {
    "1_2": [
        {"fname": "fft_20site_1_2.txt", "marker": "o", "N": 20},
        {"fname": "fft_28site_1_2.txt", "marker": "s", "N": 28},
    ],
    "1_3": [
        {"fname": "fft_24site_1_3.txt", "marker": "o", "N": 24},
        {"fname": "fft_27site_1_3.txt", "marker": "s", "N": 27},
        #{"fname": "fft_36site_1_3.txt", "marker": "s", "N": 36},

    ],
    "1_4": [
        {"fname": "fft_24site_1_4.txt", "marker": "o", "N": 24},
        #{"fname": "fft_32site_1_4.txt", "marker": "s", "N": 32},
        {"fname": "fft_36site_1_4.txt", "marker": "^", "N": 36},
        #{"fname": "fft_16site_1_4.txt", "marker": "^", "N": 36},

    ],
}

# ---- geometry inset function ----
def plot_27_geometry(ax):
    a1 = np.array([1, 0])
    a2 = np.array([0.5, -np.sqrt(3)/2])

    def cor(n1, n2):
        return n1 * a1 + n2 * a2

    coordinates = np.array([
        cor(0,0), cor(1,0), cor(2,0), cor(3,0),
        cor(-1,1), cor(0,1), cor(1,1), cor(2,1), cor(3,1),
        cor(-2,2), cor(-1,2), cor(0,2), cor(1,2), cor(2,2), cor(3,2),
        cor(-2,3), cor(-1,3), cor(0,3), cor(1,3), cor(2,3),
        cor(-2,4), cor(-1,4), cor(0,4), cor(1,4),
        cor(-2,5), cor(-1,5), cor(0,5),
        cor(-3,3), cor(-3,4), cor(-3,5), cor(0,6), cor(-1,6),
        cor(-2,6), cor(-3,6), cor(1,5), cor(2,4), cor(3,3)
    ])

    G = nx.Graph()
    for idx, pos in enumerate(coordinates):
        G.add_node(idx, pos=pos)

    neighbor_dist = np.linalg.norm(a1)

    for i in range(len(coordinates)):
        for j in range(i+1, len(coordinates)):
            dist = np.linalg.norm(coordinates[i] - coordinates[j])
            if np.isclose(dist, neighbor_dist, atol=1e-5):
                G.add_edge(i, j)

    pos = nx.get_node_attributes(G, 'pos')

    filled_nodes = {0,3,6,10,13,17,20,23,25,27,30,33,36}
    unfilled_nodes = [n for n in G.nodes if n not in filled_nodes]

    nx.draw_networkx_edges(G, pos, edge_color='gray', ax=ax)

    nx.draw_networkx_nodes(G, pos, nodelist=filled_nodes,
                           node_color='dodgerblue', node_size=40, ax=ax)

    nx.draw_networkx_nodes(G, pos, nodelist=unfilled_nodes,
                           node_color='white', edgecolors='black',
                           linewidths=1.0, node_size=40, ax=ax)

    ax.axis("equal")
    ax.axis("off")
def plot_36_geometry(ax):
    def rescale_positions(pos):
        coords = np.array(list(pos.values()))
        min_xy = coords.min(axis=0)
        max_xy = coords.max(axis=0)
        scale = max(max_xy - min_xy)

        return {k: (v - min_xy) / scale for k, v in pos.items()}

    LX, LY = 6, 6
    a = 1.0

    a1 = a * np.array([np.sqrt(3), 0])
    a2 = a * np.array([np.sqrt(3)/2, 1.5])

    pos_dict = {}
    index_dict = {}
    idx = 0

    for i in range(LY):
        for j in range(LX):
            pos = j*a1 + i*a2
            pos_dict[(i,j)] = pos
            index_dict[(i,j)] = idx
            idx += 1

    G = nx.Graph()

    for (i,j), pos in pos_dict.items():
        G.add_node(index_dict[(i,j)], pos=pos)

    neighbor_shifts = [(0,1),(-1,1),(-1,0),(0,-1),(1,-1),(1,0)]

    for (i,j) in index_dict.keys():
        for di,dj in neighbor_shifts:
            ni, nj = i+di, j+dj
            if 0 <= ni < LY and 0 <= nj < LX:
                G.add_edge(index_dict[(i,j)], index_dict[(ni,nj)])

    filled_nodes = {0,1,2,3,4,5,12,13,14,15,16,17,24,25,26,27,28,29}
    unfilled_nodes = [n for n in G.nodes if n not in filled_nodes]

    pos = rescale_positions(nx.get_node_attributes(G, 'pos'))

    nx.draw_networkx_edges(G, pos, edge_color='gray', ax=ax)

    nx.draw_networkx_nodes(G, pos, nodelist=filled_nodes,
                           node_color='dodgerblue', node_size=40, ax=ax)

    nx.draw_networkx_nodes(G, pos, nodelist=unfilled_nodes,
                           node_color='white', edgecolors='black',
                           linewidths=1.0, node_size=40, ax=ax)

    ax.axis("equal")
    ax.axis("off")
def plot_36_geometry_1_4(ax):
    def rescale_positions(pos):
        coords = np.array(list(pos.values()))
        min_xy = coords.min(axis=0)
        max_xy = coords.max(axis=0)
        scale = max(max_xy - min_xy)

        return {k: (v - min_xy) / scale for k, v in pos.items()}

    LX, LY = 6, 6
    a = 1.0

    a1 = a * np.array([np.sqrt(3), 0])
    a2 = a * np.array([np.sqrt(3)/2, 1.5])

    pos_dict = {}
    index_dict = {}
    idx = 0

    for i in range(LY):
        for j in range(LX):
            pos = j*a1 + i*a2
            pos_dict[(i,j)] = pos
            index_dict[(i,j)] = idx
            idx += 1

    G = nx.Graph()

    for (i,j), pos in pos_dict.items():
        G.add_node(index_dict[(i,j)], pos=pos)

    neighbor_shifts = [(0,1),(-1,1),(-1,0),(0,-1),(1,-1),(1,0)]

    for (i,j) in index_dict.keys():
        for di,dj in neighbor_shifts:
            ni, nj = i+di, j+dj
            if 0 <= ni < LY and 0 <= nj < LX:
                G.add_edge(index_dict[(i,j)], index_dict[(ni,nj)])

    filled_nodes = {0,12,24,2,14,26,4,16,28}
    unfilled_nodes = [n for n in G.nodes if n not in filled_nodes]

    pos = rescale_positions(nx.get_node_attributes(G, 'pos'))

    nx.draw_networkx_edges(G, pos, edge_color='gray', ax=ax)

    nx.draw_networkx_nodes(G, pos, nodelist=filled_nodes,
                           node_color='dodgerblue', node_size=40, ax=ax)

    nx.draw_networkx_nodes(G, pos, nodelist=unfilled_nodes,
                           node_color='white', edgecolors='black',
                           linewidths=1.0, node_size=40, ax=ax)

    ax.axis("equal")
    ax.axis("off")


# ---- horizontal reference lines ----
y_lines = {
    "1_2": (1/2, r"$1/2$"),
    "1_3": (1/3, r"$1/3$"),
    "1_4": (1/4, r"$1/4$"),
}

# ---- panel text ----
panel_texts = {
    "1_2": r"$n=\frac{1}{2}$",
    "1_3": (
        r"$n=\frac{1}{3}$" "\n"
        r"$\vec{k}=\left(\frac{4\pi}{3},\ 0\right)$"
    ),
    "1_4": (
        r"$n=\frac{1}{4}$" "\n"
        r"$\vec{k}=\left(\frac{2\pi}{\sqrt{3}},\ 0\right)$"
    ),
}

def load_xy(fname):
    data = np.loadtxt(fname)
    data = data[np.argsort(data[:, 0])]
    x = data[:, 0] * SCALE
    y = data[:, 1]
    return x, y

# ---- figure ----
fig, axes = plt.subplots(
    1, 3,
    figsize=(16, 4.5),
    sharex=True,
    gridspec_kw=dict(wspace=0.2)
)

panel_order = ["1_3", "1_2", "1_4"]

for idx, filling in enumerate(panel_order):
    ax = axes[idx]

    # ---- plot all datasets for this filling ----
    for ds in filling_datasets[filling]:
        x, y = load_xy(ds["fname"])

        if ds["fname"] == "fft_24site_1_3.txt":
            label = r"$N=24\,b$"
        elif ds["fname"] == "fft_24site_1_4.txt":
            label = r"$N=24\,a$"
        else:
            label = fr"$N={ds['N']}$"
        ax.plot(x, y,
                   marker=ds["marker"],
                   linestyle='-',
                   alpha=0.8,
                   label=label)#,
                   #label=fr"$N={ds['N']}$")


    # ---- legend ----
    #ax.legend(frameon=False, fontsize=16)
    ax.legend(frameon=False, fontsize=16, loc="center right")

    # ---- axes formatting ----
    ax.set_xlim(0, 3)
    ax.axvline(x=1.81, color="black", linestyle=":", linewidth=1.5)

    # ---- horizontal filling line ----
    yv, yl = y_lines[filling]
    ax.axhline(y=yv, color="red", linestyle="--", linewidth=1)
    ax.text(0.95, yv, yl,
            color="red",
            fontsize=20,
            ha="right",
            va="bottom",
            transform=ax.get_yaxis_transform())

    # ---- panel text ----
    """ax.text(0.6, 0.89,
            panel_texts[filling],
            transform=ax.transAxes,
            fontsize=18,
            ha="left",
            va="top",
            bbox=dict(boxstyle="round,pad=0.2",
                      facecolor="white",
                      edgecolor="gray"))"""

    # ---- insets ----
    if filling == "1_3":
        axins = inset_axes(ax, width="55%", height="55%",
                           loc="lower left", borderpad=-0.2)
        plot_27_geometry(axins)

    if filling == "1_2":
        axins = inset_axes(ax, width="65%", height="65%",
                           loc="lower left", borderpad=-0.3)
        plot_36_geometry(axins)
        ax.legend(frameon=False, fontsize=16,
                  loc="upper left",
                  bbox_to_anchor=(-0.05, 0.8))

    if filling == "1_4":
        axins = inset_axes(ax, width="63%", height="63%",
                           loc="lower left", borderpad=-0.5)
        plot_36_geometry_1_4(axins)

        ax.legend(frameon=False, fontsize=16,
                  loc="upper left",
                  bbox_to_anchor=(-0.05, 0.7))

    if filling == "1_3":
        ax.set_ylim(0.22,0.34)
        #ax.legend(frameon=False, fontsize=16, loc="upper left")
        ax.legend(frameon=False, fontsize=16,
                  loc="upper left",
                  bbox_to_anchor=(-0.05, 0.8))


# ---- labels ----
axes[0].set_ylabel(r"$\sqrt{S(k)/N}$")
for ax in axes:
    ax.set_xlabel(r"$t(\mathrm{meV})$")

plt.savefig("S_k_1x3_with_inset.pdf", bbox_inches="tight")
plt.show()
