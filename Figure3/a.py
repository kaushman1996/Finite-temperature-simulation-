import numpy as np
import matplotlib.pyplot as plt

# lattice vectors
a1 = np.array([1, 0])
a2 = np.array([-0.5, np.sqrt(3)/2])

def cor(n1, n2):
    return n1 * a1 + n2 * a2

# coordinates
coordinates = np.array([
    cor(0,0), cor(3,1), cor(2,1), cor(5,2),
    cor(1,1), cor(4,2), cor(3,2), cor(6,3), cor(2,2),
    cor(5,3), cor(1,2), cor(4,3), cor(3,3), cor(6,4), cor(2,3),
    cor(5,4), cor(1,3), cor(4,4), cor(3,4), cor(6,5),
    cor(2,4), cor(5,5), cor(1,4), cor(4,5),
    cor(3,5), cor(6,6), cor(2,5), cor(5,6)
])

# radii
radii = np.array([
    14., 1., 12., 1., 2., 12., 3., 11., 10., 4., 5., 9.,
    6., 8., 7., 7., 8., 6., 9., 5., 4., 10., 11., 3.,
    12., 2., 1., 12.
]) / 50.0
radii = np.array([14., 7., 0., 0., 14., 14., 0., 0., 14., 14., 0., 0., 14., 14., 0., 0., 14., 14., 0., 0., 14., 14., 0., 0., 14., 14., 0., 0.])/50.0
#radii = np.array([14., 7., 0., 0., 14., 14., 0., 0., 14., 14., 0., 0., 14., 14., 0., 0., 14., 14., 0., 0., 14., 14., 0., 0., 14., 14., 0., 0.])/50.0
# plot
fig, ax = plt.subplots(figsize=(6, 6))

for (x, y), r in zip(coordinates, radii):
    circle = plt.Circle((x, y), r, edgecolor='black', facecolor='none', linewidth=1.5)
    ax.add_patch(circle)

# also plot centers (optional)
ax.scatter(coordinates[:, 0], coordinates[:, 1], s=10)

ax.set_aspect('equal')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Circles on lattice')

plt.tight_layout()
plt.show()
