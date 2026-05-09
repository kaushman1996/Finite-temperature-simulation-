import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Times New Roman"],
    "font.size": 20
})

# ==============================
# --- Primitive Vectors (consistent) ---
# ==============================
# --- Primitive Vectors ---
a1 = np.array([1, 0])
a2 = np.array([0.5, np.sqrt(3)/2])

def cor(n1, n2):
    return n1 * a1 + n2 * a2



# ==============================
# --- Background Lattice ---
# ==============================
lattice_nodes = {}
for i in range(-10, 14):
    for j in range(-10, 14):
        lattice_nodes[(i, j)] = cor(i, j)

BG = nx.Graph()
for key, pos in lattice_nodes.items():
    BG.add_node(key, pos=pos)

neighbor_shifts = [(1, 0), (0, 1), (-1, 1)]
for (i, j) in lattice_nodes:
    for dx, dy in neighbor_shifts:
        neighbor = (i + dx, j + dy)
        if neighbor in lattice_nodes:
            BG.add_edge((i, j), neighbor)

# Draw background
bg_pos = nx.get_node_attributes(BG, 'pos')
nx.draw_networkx_edges(BG, bg_pos, edge_color='lightgray', width=0.5)
nx.draw_networkx_nodes(BG, bg_pos, node_size=20, node_color='lightgray')


# ==============================
# --- 24-Site Cluster ---
# ==============================
a1 = np.array([1, 0])
a2 = np.array([0.5, np.sqrt(3)/2])   # use ONE convention

def cor(n1, n2):
    return n1 * a1 + n2 * a2

coordinates = np.array([
    cor(0,0), cor(1,2), cor(1,1), cor(2,3), cor(1,0), cor(2,2),
    cor(1,-1), cor(2,1), cor(2,0), cor(3,2), cor(2,-1), cor(3,1),
    cor(2,-2), cor(3,0), cor(3,-1), cor(4,1), cor(3,-2), cor(4,0),
    cor(3,-3), cor(4,-1), cor(4,-2), cor(5,0), cor(4,-3), cor(5,-1),
    cor(4,-4),cor(5,-2),cor(6,0),cor(2,4),cor(3,3),cor(4,2),cor(5,1)
])
coordinates = []

for j in range(4):
    for i in range(6):
        coordinates.append(j * np.array([0.5,np.sqrt(3)/2]) + i * np.array([1, 0]))

for j in range(4):
    for i in range(6,7):
        coordinates.append(j * np.array([0.5,np.sqrt(3)/2]) + i * np.array([1, 0]))
for j in range(4,5):
    for i in range(7):
        coordinates.append(j * np.array([0.5,np.sqrt(3)/2]) + i * np.array([1, 0]))


# Build graph
G = nx.Graph()
for i, pos in enumerate(coordinates):
    G.add_node(i, pos=pos)

# Nearest-neighbor edges
neighbor_dist = np.linalg.norm(a1)
for i in range(len(coordinates)):
    for j in range(i + 1, len(coordinates)):
        if np.isclose(np.linalg.norm(coordinates[i] - coordinates[j]),
                      neighbor_dist, atol=1e-5):
            G.add_edge(i, j)

pos_dict = nx.get_node_attributes(G, 'pos')


# ==============================
# --- Labels ---
# ==============================
labels = {i: str(i) for i in G.nodes}

# optional custom labeling (last few sites)
last_n = 11
custom_labels = [0, 6, 12 ,18, 0, 1, 2, 3, 4, 5, 0]
for i, val in zip(range(len(coordinates) - last_n, len(coordinates)), custom_labels):
    labels[i] = str(val)


# ==============================
# --- Node Styling ---
# ==============================
#filled_nodes = set()   # choose indices if needed
filled_nodes = {0,2,6,8,12,14,18,20,4,10,16,22,24,25,26,27,28,30,32,34}

unfilled_nodes = [n for n in G.nodes if n not in filled_nodes]

nx.draw_networkx_edges(G, pos_dict, edge_color='gray', width=1.0)

nx.draw_networkx_nodes(
    G, pos_dict,
    nodelist=list(filled_nodes),
    node_color='dodgerblue',
    node_size=100
)
nx.draw_networkx_nodes(
    G, pos_dict,
    nodelist=unfilled_nodes,
    node_color='white',
    edgecolors='black',
    linewidths=1.5,
    node_size=100
)


# ==============================
# --- Optional Loop (adjust if needed) ---
# ==============================
loop_points = [cor(0,0), cor(6,0), cor(6,4), cor(0,4), cor(0,0)]
x_vals, y_vals = zip(*loop_points)
plt.plot(x_vals, y_vals, 'r--', linewidth=2, zorder=3)


# ==============================
# --- Final Formatting ---
# ==============================
nx.draw_networkx_labels(G, pos_dict, labels=labels, font_size=8)

#plt.axis('equal')
#plt.axis('off')
ax = plt.gca()
#ax.set_aspect('equal', adjustable='box')

plt.axis('off')

#plt.xlim(min(coordinates[:,0]) +1, max(coordinates[:,0])-2)
#plt.ylim(min(coordinates[:,1]) -0.5, max(coordinates[:,1])+1) 
plt.xlim(-1.,9.0)
plt.ylim(-1.2, 5)

#plt.title("24-site lattice")
plt.title("$N = 24a, \t n = 1/2$")
plt.savefig("24_a.pdf", bbox_inches='tight')
plt.show()
