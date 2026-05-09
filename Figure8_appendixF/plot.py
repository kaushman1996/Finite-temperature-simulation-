import numpy as np
import matplotlib.pyplot as plt

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

def f(w):
    # Avoid division by zero using np.where
    w_safe = np.where(w == 0, 1e-10, w)
    
    term1 = 1 - (1 - np.exp(-w_safe)) / w_safe
    term2 = 1 - (1 - np.exp(-2 * w_safe)) / (2 * w_safe)
    
    return -w_safe - 8 * term1 + 6 * term2

# Generate values
w = np.linspace(0.001, 3, 500)  # start slightly above 0 to avoid singularity
y = f(w)

# Plot
plt.figure(figsize=(6, 4))
plt.plot(w, y) 
plt.xlabel("$w$")
plt.ylabel("$f(w)$")
#plt.title("Plot of f(w)")
#plt.legend()
#plt.grid(True)

# Save as PDF
plt.savefig("f_w_plot.pdf", bbox_inches='tight')

# Show plot
plt.show()
