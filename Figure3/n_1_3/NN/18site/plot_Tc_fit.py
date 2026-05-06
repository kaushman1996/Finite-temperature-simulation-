import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Times New Roman"],
    "font.size": 16
})

# Load data from the file
data = np.loadtxt('Tc_t.txt')
t = data[:, 0]
Tc = data[:, 1]

# Constants
Tc_class = 43.61033
V1 = 11.6 * 9#1.81 * 5.7*3.9/4.67

# Fit
t_fit = np.linspace(0, 6.0, 300)
Tc_fit = Tc_class * (1 - (0.5 * ((t_fit * 11.6) ** 2) / (Tc_class * V1)))
Tc_fit1 = Tc_class * (1 - (((t_fit * 11.6) ** 2) / (Tc_class * V1)))


# Plot data
plt.figure(figsize=(9, 7))
plt.plot(t, Tc, 'bo',color = 'Red', label='FTLM M = 200, R = 200')
#plt.plot(t_fit, Tc_fit, 'k--', label=r"$T_c(t') = T_{c,\mathrm{class}} \left(1 - \frac{1}{2} \frac{t'^2}{T_{c,\mathrm{class}} V_1} \right) (Hitesh)$")
plt.plot(t_fit, Tc_fit1, 'k*', label=r"$T_c(t') = T_{c,\mathrm{class}} \left(1 - \frac{t'^2}{T_{c,\mathrm{class}} V_1} \right)$")


# Title and labels
plt.title("$T_c$ vs $t$, $N=27, N_p=9, \epsilon=3.9$ ")
plt.xlabel("t(meV)")
plt.ylabel("Tc (K)")

# Annotations
#plt.text(0.05, 47, r"$T_{c,\mathrm{class}} = 50.07 K$", fontsize=16)
#plt.text(0.05, 47.5, r"$V_1 = 11.6 \times 1.81 \times 5.7 K$", fontsize=16)
#plt.text(0.05, 48, r"$t' = t \times 11.6 K$", fontsize=16)

# Legend and grid
plt.legend()
plt.grid(True)
plt.xlim(0,2.6)
plt.ylim(32.5,45)
# Show plot
plt.tight_layout()

plt.savefig('Figure.pdf')
plt.show()
