import numpy as np
import matplotlib.pyplot as plt

# Load spectrum data
spec = np.loadtxt("spectrum_data.txt")
J_spec = spec[:,0]
dE = spec[:,1]

# Load Tc data
tc = np.loadtxt("Tc_t.txt")
J_tc = tc[:,0]
Tc = tc[:,1]

# Compute normalized Tc
Tc_norm = (Tc - Tc[0]) / Tc[0]

# Create subplot
fig, ax = plt.subplots(2,1, figsize=(6,8), sharex=True)

# ---- Normalized Tc plot (top) ----
ax[0].plot(J_tc, Tc_norm, 'o-', color='red')
ax[0].set_ylabel("(Tc - Tc[0]) / Tc[0]")
ax[0].grid(True)
ax[0].set_title("Normalized Critical Temperature")

# ---- Spectrum plot (bottom) ----
ax[1].scatter(J_spec, dE, s=10)
ax[1].set_xlabel("J")
ax[1].set_ylabel("ΔE (meV)")
ax[1].set_ylim(0,12)
ax[1].grid(True)
ax[1].set_title("Excitation Spectrum")

plt.tight_layout()
plt.show()
