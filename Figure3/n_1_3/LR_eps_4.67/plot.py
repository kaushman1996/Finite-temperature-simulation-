import numpy as np
import matplotlib.pyplot as plt
import os

# --- Load spectrum data (common) ---
spec = np.loadtxt(os.path.join("18site", "spectrum_data.txt"))

J_spec = spec[:,0]
dE = spec[:,1]

# --- Load Tc data from two directories ---
tc_18 = np.loadtxt(os.path.join("18site", "Tc_t.txt"))
J_tc_18 = tc_18[:,0]
Tc_18 = tc_18[:,1]
Tc_norm_18 = (Tc_18 - Tc_18[0]) / Tc_18[0]

tc_27 = np.loadtxt(os.path.join("27site", "Tc_t.txt"))
J_tc_27 = tc_27[:,0]
Tc_27 = tc_27[:,1]
Tc_norm_27 = (Tc_27 - Tc_27[0]) / Tc_27[0]

# --- Create subplot ---
fig, ax = plt.subplots(2,1, figsize=(6,8), sharex=True)

# ---- Normalized Tc plot (top) ----
ax[0].plot(J_tc_18, Tc_norm_18, 'o-', color='red', label="18-site")
ax[0].plot(J_tc_27, Tc_norm_27, 's-', color='blue', label="27-site")
ax[0].set_ylabel("(Tc - Tc[0]) / Tc[0]")
ax[0].grid(True)
ax[0].set_title("Normalized Critical Temperature")
ax[0].legend()  # Show labels

# ---- Spectrum plot (bottom) ----
ax[1].scatter(J_spec, dE, s=10, color='black')
ax[1].set_xlabel("J")
ax[1].set_ylabel("ΔE (meV)")
ax[1].set_ylim(0,12)
ax[1].grid(True)
ax[1].set_title("Excitation Spectrum")

plt.tight_layout()
plt.show()
