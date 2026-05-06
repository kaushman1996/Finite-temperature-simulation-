import numpy as np
import matplotlib.pyplot as plt
import glob
import re
import os

# Find all specific heat files
cv_files = sorted(glob.glob("cv_J*.txt"))
if not cv_files:
    print("No cv_J*.txt files found in current directory.")
    exit(1)

J_vals = []
Tc_vals = []

for fname in cv_files:
    if not os.path.isfile(fname):
        print(f"File not found: {fname}")
        continue

    try:
        data = np.loadtxt(fname)
        if data.shape[1] < 2:
            print(f"Invalid file format: {fname}")
            continue

        T, Cv = data[:, 0], data[:, 1]

        # ✅ Updated regex pattern to handle decimal J
        #match = re.search(r'cv_J([0-9.]+).txt', fname)
        match = re.search(r'cv_J([0-9.]+)_Nsample.txt', fname)
        if not match:
            print(f"Filename pattern mismatch: {fname}")
            continue
        J_val = float(match.group(1))

        # Find Tc = temperature at which Cv peaks
        max_idx = np.argmax(Cv)
        Tc = T[max_idx]

        J_vals.append(J_val)
        Tc_vals.append(Tc)

    except Exception as e:
        print(f"Error reading {fname}: {e}")
        continue

if not J_vals:
    print("No valid data to plot.")
    exit(1)

# Sort by J values
J_vals, Tc_vals = zip(*sorted(zip(J_vals, Tc_vals)))

# Plot Tc vs J
plt.figure(figsize=(8, 5))
plt.plot(np.array(J_vals), Tc_vals, 'o-')#, linewidth=2)
plt.xlabel('t(meV)')
#plt.xlim(0,2)
#plt.ylim(30,45)

plt.ylabel('$T_c$ (K)')
plt.title('$T_c$ vs. t')
plt.grid(True)
plt.tight_layout()
plt.savefig("Tc_vs_J.png")
plt.show()

# Optional: Save Tc values to a file
np.savetxt("Tc_vs_J_200.txt", np.column_stack([J_vals, Tc_vals]), header="J  Tc")
