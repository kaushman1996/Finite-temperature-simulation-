import numpy as np
import matplotlib.pyplot as plt

# load data
data = np.loadtxt("Tc_1_4_32_site.txt")

x = data[:, 0]
y = data[:, 1]

# sort by x (important to get correct y[0])
idx = np.argsort(x)
x = x[idx]
y = y[idx]

# normalize
y0 = y[0]
y_norm = (y - y0) / y0

# cutoff x <= 0.8
mask = x <= 0.8
x_fit = x[mask]
y_fit = y_norm[mask]

# fit y = a x^2
A = x_fit**2
a = np.sum(A * y_fit) / np.sum(A * A)

print(f"Fit parameter a = {a:.6f}")

# fitted curve
x_line = np.linspace(0, 2.0, 200)
y_line = a * x_line**2

# plot
plt.scatter(x, y_norm, s=10, label="normalized data")
plt.plot(x_line, y_line, 'r--', label=f"fit: a x^2 (a={a:.3f})")

plt.xlabel("x")
plt.ylabel("(y - y0)/y0")
plt.legend()
plt.show()
