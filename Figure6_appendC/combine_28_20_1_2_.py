import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Times New Roman"],
    "font.size": 23
})

fig = plt.figure(figsize=(12, 6))

##############################
# --------- First Plot -------
##############################

plt.subplot(1, 2, 1)

# --- Primitive Vectors ---
a1 = np.array([1, 0])
a2 = np.array([-0.5, np.sqrt(3)/2])

def cor(n1, n2):
    return n1 * a1 + n2 * a2

# --- Background Lattice ---
a11 = np.array([1, 0])
a21 = np.array([0.5, np.sqrt(3)/2])
def cor1(n1, n2):
    return n1 * a11 + n2 * a21

lattice_nodes = {}
for i in range(-7, 11):
    for j in range(-7, 11):
        lattice_nodes[(i, j)] = cor1(i, j)

BG = nx.Graph()
for key, pos in lattice_nodes.items():
    BG.add_node(key, pos=pos)
neighbor_shifts = [(1, 0), (0, 1), (-1, 1)]
for (i, j) in lattice_nodes:
    for dx, dy in neighbor_shifts:
        neighbor = (i + dx, j + dy)
        if neighbor in lattice_nodes:
            BG.add_edge((i, j), neighbor)

bg_pos = nx.get_node_attributes(BG, 'pos')
nx.draw_networkx_edges(BG, bg_pos, edge_color='lightgray', width=0.5)
nx.draw_networkx_nodes(BG, bg_pos, node_size=20, node_color='lightgray')

coordinates = np.array([
    cor(0,0), cor(3,1), cor(2,1), cor(5,2),
    cor(1,1), cor(4,2), cor(3,2), cor(6,3), cor(2,2),
    cor(5,3), cor(1,2), cor(4,3), cor(3,3), cor(6,4), cor(2,3),
    cor(5,4), cor(1,3), cor(4,4), cor(3,4), cor(6,5),
    cor(2,4), cor(5,5), cor(1,4), cor(4,5),
    cor(3,5), cor(6,6), cor(2,5), cor(5,6),
    cor(1,5), cor(6,2), cor(7,7), cor(4,6)
])
G = nx.Graph()
for idx, pos in enumerate(coordinates):
    G.add_node(idx, pos=pos)
neighbor_dist = np.linalg.norm(a1)
for i in range(len(coordinates)):
    for j in range(i+1, len(coordinates)):
        if np.isclose(np.linalg.norm(coordinates[i] - coordinates[j]), neighbor_dist, atol=1e-5):
            G.add_edge(i, j)
pos_dict = nx.get_node_attributes(G, 'pos')

last_n = 4
custom_labels = [0, 0, 0, 1]
labels = {i: str(i) for i in G.nodes}
for i, val in zip(range(len(coordinates) - last_n, len(coordinates)), custom_labels):
    labels[i] = str(val)

filled_nodes = {0,4,8,12,17,21,25,16,20,24,1,5,9,13,29,30,31,32,33,28}
filled_nodes = {i for i in filled_nodes if i < len(coordinates)}
unfilled_nodes = [n for n in G.nodes if n not in filled_nodes]

nx.draw_networkx_edges(G, pos_dict, edge_color='gray', width=1.0)
nx.draw_networkx_nodes(G, pos_dict, nodelist=list(filled_nodes), node_color='dodgerblue', node_size=100)
nx.draw_networkx_nodes(G, pos_dict, nodelist=unfilled_nodes, node_color='white', edgecolors='black', linewidths=1.5, node_size=100)

loop_points = [cor(0,0), cor(6,2), cor(7,7), cor(1,5), cor(0,0)]
x_vals, y_vals = zip(*loop_points)
plt.plot(x_vals, y_vals, 'r--', linewidth=2, zorder=3)

nx.draw_networkx_labels(G, pos_dict, labels=labels, font_size=6)
plt.axis('equal')
plt.axis('off')
plt.xlim(-1.5, 5)
plt.ylim(-1, 7)
plt.title("$N = 28,\t n = 1/2$")

##############################
# --------- Second Plot ------
##############################

plt.subplot(1, 2, 2)

a1 = np.array([1, 0])
a2 = np.array([0.5, np.sqrt(3)/2])
def cor(n1, n2):
    return n1 * a1 + n2 * a2

lattice_nodes = {}
for i in range(-5, 14):
    for j in range(-5, 14):
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

nx.draw_networkx_edges(BG, nx.get_node_attributes(BG, 'pos'), edge_color='lightgray', width=0.5)
bg_pos = nx.get_node_attributes(BG, 'pos')
nx.draw_networkx_nodes(BG, bg_pos, node_size=20, node_color='lightgray')

custom_coords = [
    cor(0,0), cor(0,1), cor(0,2), cor(0,3), cor(0,4),
    cor(1,1), cor(1,2), cor(1,3), cor(1,4), cor(1,5),
    cor(2,1), cor(2,2), cor(2,3), cor(2,4), cor(2,5), cor(3,2),
    cor(3,3), cor(3,4), cor(3,5), cor(3,6), cor(4,2),
    cor(4,3), cor(4,4), cor(4,5), cor(4,6), cor(4,7), cor(0,5), cor(2,6)
]
coordinates = np.array(custom_coords)

G = nx.Graph()
for idx, pos in enumerate(coordinates):
    G.add_node(idx, pos=pos)
neighbor_dist = np.linalg.norm(a1)
for i in range(len(coordinates)):
    for j in range(i+1, len(coordinates)):
        if np.isclose(np.linalg.norm(coordinates[i] - coordinates[j]), neighbor_dist, atol=1e-5):
            G.add_edge(i, j)
pos_dict = nx.get_node_attributes(G, 'pos')

last_n = 8
custom_labels = [0, 1, 2, 3, 4, 0, 0, 10]
labels = {i: str(i) for i in G.nodes}
for i, val in zip(range(len(coordinates) - last_n, len(coordinates)), custom_labels):
    labels[i] = str(val)

filled_nodes = {0,1,2,3,4,10,11,12,13,14,20,21,22,23,24,25,26,27} 
filled_nodes = {i for i in filled_nodes if i < len(coordinates)}
unfilled_nodes = [n for n in G.nodes if n not in filled_nodes]

nx.draw_networkx_edges(G, pos_dict, edge_color='gray', width=1.0)
nx.draw_networkx_nodes(G, pos_dict, nodelist=list(filled_nodes), node_color='dodgerblue', node_size=100)
nx.draw_networkx_nodes(G, pos_dict, nodelist=unfilled_nodes, node_color='white', edgecolors='black', linewidths=1.5, node_size=100)

loop_points = [cor(0,0), cor(0,5), cor(4,7), cor(4,2), cor(0,0)]
x_vals, y_vals = zip(*loop_points)
plt.plot(x_vals, y_vals, 'r--', linewidth=2, zorder=3)

nx.draw_networkx_labels(G, pos_dict, labels=labels, font_size=8)
plt.axis('equal')
plt.axis('off')
plt.xlim(0.5, 7)
plt.ylim(-1, 7)
plt.title("$N = 20, \t n = 1/2$")

##############################

plt.tight_layout()
plt.savefig("combined_lattices_20_28.pdf", bbox_inches='tight')
plt.show()

