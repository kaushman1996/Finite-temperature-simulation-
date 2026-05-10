from __future__ import print_function, division
#
import sys,os
os.environ['KMP_DUPLICATE_LIB_OK']='True' # uncomment this line if omp error occurs on OSX for python 3
os.environ['OMP_NUM_THREADS']='1' # set number of OpenMP threads to run in parallel
os.environ['MKL_NUM_THREADS']='1' # set number of MKL threads to run in parallel
#
quspin_path = os.path.join(os.getcwd(),"../../")
sys.path.insert(0,quspin_path)
###########################################################################
#                            example 13                                   #
#  In this script we demonstrate how to construct a spinful fermion basis #
#  with no doubly occupancid sites in the Fermi-Hubbard model,            #
#  using the spinful_fermion_ basis_general class.                        #
###########################################################################
from quspin.basis import spinful_fermion_basis_general
from quspin.operators import hamiltonian
from quspin.tools.lanczos import lanczos_full,lanczos_iter,lin_comb_Q_T,expm_lanczos

import numpy as np
import matplotlib.pyplot as plt
from quspin.basis import spinful_fermion_basis_general
from quspin.operators import hamiltonian
import os

LX, LY = 4, 4
N_2d = LX * LY
U = 75.0 * 1.81
mu = 0.0
T_x = [1, 2, 3, 0, 5, 6, 7, 4, 9, 10, 11, 8, 13, 14, 15, 12]
T_y = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0, 1, 2, 3]
T_z = [7, 4, 5, 6, 11, 8, 9, 10, 15, 12, 13, 14, 3, 0, 1, 2]

# --- Read long-range interactions ---
def read_vij(file_name='vv_results.txt'):
    hopp, hopp1 = [], []
    with open(file_name, 'r') as file:
        for line in file:
            I, j, vij = line.split()
            I, j, vij = int(I), int(j), float(vij)*3.9/4.67
            hopp.append([vij, I, j])
            hopp1.append([vij, j, I])
    return hopp, hopp1

# --- Compute eigenvalues at each k-point ---
def compute_eigenvalues_kpoint(nup, ndown, J1, kx1, ky1):
    J = J1
    V = 9
    basis_2d = spinful_fermion_basis_general(
        N_2d, Nf=(nup, ndown), kxblock=(T_x, kx1), kyblock=(T_y, ky1), Ns_block_est=200000
    )

    hopping_left = [[-J, i, T_x[i]] for i in range(N_2d)] + \
                   [[-J, i, T_y[i]] for i in range(N_2d)] + \
                   [[-J, i, T_z[i]] for i in range(N_2d)]
    hopping_right = [[+J, i, T_x[i]] for i in range(N_2d)] + \
                    [[+J, i, T_y[i]] for i in range(N_2d)] + \
                    [[+J, i, T_z[i]] for i in range(N_2d)]
    potential = [[-mu, i] for i in range(N_2d)]
    interaction = [[U, i, i] for i in range(N_2d)]
    interaction1=[[V,i,T_x[i]] for i in range(N_2d)] + [[V,i,T_y[i]] for i in range(N_2d)] + [[V,i,T_z[i]] for i in range(N_2d)]
    interaction2=[[V,T_x[i],i] for i in range(N_2d)] + [[V,T_y[i],i] for i in range(N_2d)] + [[V,T_z[i],i] for i in range(N_2d)]
    static=[["+-|",hopping_left], # spin up hops to left
                    ["-+|",hopping_right], # spin up hops to right
                    ["|+-",hopping_left], # spin down hopes to left
                    ["|-+",hopping_right], # spin up hops to right
                    ["n|n",interaction], # spin up-spin down interaction
                    ["n|n",interaction1], # spin up-spin down interaction
                    ["nn|",interaction1], # spin up-spin down interaction
                    ["|nn",interaction1], # spin up-spin down interaction
                    ["n|n",interaction2]] # spin up-spin down interaction


    H = hamiltonian(static, [], basis=basis_2d, dtype=np.complex128)
    eigs = H.eigvalsh()
    return eigs

# --- Thermal averages ---
def average_energy(T, eigenvalues):
    boltzmann = np.exp(-eigenvalues / T)
    Z = np.sum(boltzmann)
    return np.sum(eigenvalues * boltzmann) / Z

def average_E2(T, eigenvalues):
    boltzmann = np.exp(-eigenvalues / T)
    Z = np.sum(boltzmann)
    return np.sum((eigenvalues**2) * boltzmann) / Z

# --- Specific heat calculation ---
def compute_specific_heat(nup=4, ndown=0, J1=0.1):
    all_eigs = []
    for kx in range(4):
        for ky in range(4):
            eigs = compute_eigenvalues_kpoint(nup, ndown, J1, kx, ky)
            all_eigs.extend(eigs)
    all_eigs = np.array(all_eigs)
    all_eigs -= np.min(all_eigs)

    
    T_values = np.linspace(1, 90, 25000) / 11.6
    E_avg = np.array([average_energy(T, all_eigs) for T in T_values])
    E2_avg = np.array([average_E2(T, all_eigs) for T in T_values])
    
    # C_v = (⟨E²⟩ - ⟨E⟩²) / (T²)
    C_v = (E2_avg - E_avg**2) / (T_values**2)
    
    return np.array(T_values)*11.6, C_v, E_avg

# --- Run computation ---
#T, Cv, E = compute_specific_heat()

# --- Save results ---
#np.savetxt("specific_heat_J1_0.1.txt", np.column_stack([T, Cv]), header="T Cv")

#print("Saved specific heat data to specific_heat_J1_0.1.txt")

# ---- Loop over J values ----
J_values = np.arange(0, 3.1, 0.1)

for J in J_values:
    print(f"Computing for J = {J:.2f}")

    T, Cv, E = compute_specific_heat(J1=J)

    filename = f"specific_heat_J1_{J:.2f}.txt"
    np.savetxt(filename, np.column_stack([T, Cv]), header="T Cv")

    print(f"Saved {filename}")
