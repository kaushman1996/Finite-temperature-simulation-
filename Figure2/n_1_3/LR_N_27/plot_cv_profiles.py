import numpy as np
import matplotlib.pyplot as plt
import glob
import re
import os

# Find all Cv files
cv_files = sorted(glob.glob("cv_J*.txt"))
if not cv_files:
    print("No cv_J*.txt files found.")
    exit(1)

datasets = []

for fname in cv_files:

    try:
        data = np.loadtxt(fname)
        T, Cv = data[:,0], data[:,1]

        match = re.search(r'cv_J([0-9.]+)_Nsample_200.txt', fname)
        if not match:
            continue

        J_val = float(match.group(1))
        datasets.append((J_val, T, Cv))

    except Exception as e:
        print(f"Error reading {fname}: {e}")

if not datasets:
    print("No valid datasets.")
    exit(1)

# Sort datasets by J
datasets.sort(key=lambda x: x[0])

# Colormap
cmap = plt.cm.viridis
colors = cmap(np.linspace(0, 1, len(datasets)))

plt.figure(figsize=(7,5))

for i,(J,T,Cv) in enumerate(datasets):
    plt.plot(T, Cv, color=colors[i], linewidth=2)

plt.xlabel("T (K)")
plt.ylabel("C/N")
plt.title("Specific Heat Profiles")
plt.grid(True)

plt.tight_layout()
plt.savefig("Cv_profiles.png", dpi=300)
plt.show()
