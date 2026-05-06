import numpy as np
import matplotlib.pyplot as plt

# load data
data = np.loadtxt("Tc_1_4_36_site.txt")

x = data[:, 0]
y = data[:, 1]

# sort by x
idx = np.argsort(x)
x = x[idx]
y = y[idx]

# normalize
y0 = y[0]
y_norm = (y - y0) / y0

# fit region (x <= 0.8)
mask_fit = x <= 0.8
x_fit = x[mask_fit]
y_fit = y_norm[mask_fit]

# fit y = a x^2
a = np.sum(x_fit**2 * y_fit) / np.sum(x_fit**4)
print(f"Fit parameter a = {a:.6f}")

# plot region (x <= 1.0)
mask_plot = x <= 1.0

# fitted curve
x_line = np.linspace(0, 1.0, 200)
y_line = a * x_line**2

# plot
plt.figure()

plt.scatter(x[mask_plot], y_norm[mask_plot], s=10, label="data")
plt.plot(x_line, y_line, 'r--', label=f"fit: a x^2 (a={a:.3f})")

# highlight fit region
plt.axvspan(0, 0.8, color='gray', alpha=0.2, label="fit region")

plt.xlabel("x")
plt.ylabel("(y - y0)/y0")
plt.legend()
plt.show()
