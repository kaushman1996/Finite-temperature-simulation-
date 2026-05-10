from __future__ import print_function, division

import sys, os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
os.environ['OMP_NUM_THREADS'] = '24'
os.environ['MKL_NUM_THREADS'] = '24'

quspin_path = os.path.join(os.getcwd(), "../../")
sys.path.insert(0, quspin_path)

from quspin.basis import spinful_fermion_basis_general
from quspin.operators import hamiltonian
from quspin.tools.lanczos import lanczos_full

import numpy as np
import hashlib

###### define model parameters ######


Lx, Ly = 6 , 6 # linear dimension of spin 1 2d lattice
N_2d = Lx*Ly # number of sites for spin 1
U=75.0*1.81 # onsite interaction



T_x=[1,2,3,4,5,0,7,8,9,10,11,6,13,14,15,16,17,12,19,20,21,22,23,18,25,26,27,28,29,24,31,32,33,34,35,30]
T_y=[6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,0,1,2,3,4,5]
T_z=[11,6,7,8,9,10,17,12,13,14,15,16,23,18,19,20,21,22,29,24,25,26,27,28,35,30,31,32,33,34,5,0,1,2,3,4]



def cv(nup, ndown, kx1, ky1, J1, m, N_samples, seeds):
    V = 9

    basis_2d = spinful_fermion_basis_general(
        N_2d,
        Nf=[(nup, ndown)],
        kxblock=(T_x, kx1),
        kyblock=(T_y, ky1),
        Ns_block_est=6000000
    )

    print("Size of 2D Hilbert space: {Ns:d}".format(Ns=basis_2d.Ns))

    J = J1

    hopping_left = (
        [[-J, i, T_x[i]] for i in range(N_2d)] +
        [[-J, i, T_y[i]] for i in range(N_2d)] +
        [[-J, i, T_z[i]] for i in range(N_2d)]
    )
    hopping_right = (
        [[+J, i, T_x[i]] for i in range(N_2d)] +
        [[+J, i, T_y[i]] for i in range(N_2d)] +
        [[+J, i, T_z[i]] for i in range(N_2d)]
    )
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

    # directory for this J
    dir_name = f"J_{J1}"
    os.makedirs(dir_name, exist_ok=True)

    base_name = (
        f"nup{nup}_ndown{ndown}_kx{kx1}_ky{ky1}_J{J1}_m{m}_"
        f"Nsample{N_samples}_size{H.Ns}"
    )

    print("Using seeds:", seeds)

    # MAIN LOOP
    for sample_idx in range(N_samples):

        seed = seeds[sample_idx]
        np.random.seed(seed)

        # random normalized vector
        r = (
            np.random.normal(0, 1, H.Ns)
            + 1j * np.random.normal(0, 1, H.Ns)
        )
        r /= np.linalg.norm(r)

        # Lanczos
        E, V, Q_T = lanczos_full(H, r, m, eps=1e-8, full_ortho=True)

        projection = np.abs(V[0, :])**2

        # SAFE SAVING: each sample gets its own .npy file
        np.save(
            os.path.join(dir_name, f"E_{base_name}_seed{seed}_sample{sample_idx}.npy"),
            E
        )
        np.save(
            os.path.join(dir_name, f"P_{base_name}_seed{seed}_sample{sample_idx}.npy"),
            projection
        )

        print(f"Saved sample {sample_idx+1}/{N_samples}")

        del E, V, Q_T, projection, r

    return H.Ns


def main():
    if len(sys.argv) != 8:
        print("Usage: python 15site_kx_ky.py <nup> <ndown> <kx> <ky> <J> <m> <N_sample>")
        sys.exit(1)

    nup = int(sys.argv[1])
    ndown = int(sys.argv[2])
    kx = int(sys.argv[3])
    ky = int(sys.argv[4])
    J = float(sys.argv[5])
    m = int(sys.argv[6])
    N_sample = int(sys.argv[7])

    if nup + ndown != 9:
        print("Error: nup + ndown must equal 9.")
        sys.exit(1)

    kx_ky_values = [(kx_val, ky_val) for kx_val in range(6) for ky_val in range(6)]

    seed_map = {}
    for kx_val, ky_val in kx_ky_values:
        base = f"{kx_val}_{ky_val}".encode("utf-8")
        seed_base = int(hashlib.md5(base).hexdigest(), 16) % (2**32)
        rng = np.random.RandomState(seed_base)

        seed_map[(kx_val, ky_val)] = rng.choice(
            range(99_00_000),
            size=N_sample,
            replace=False
        ).tolist()
        """seed_map[(kx_val, ky_val)] = rng.choice(
            range(66_00_000),
            size=N_sample,
            replace=False
        ).tolist()"""
        seed_map[(kx_val, ky_val)] = rng.choice(
            range(33_00_000),
            size=N_sample,
            replace=False
        ).tolist()
        seed_map[(kx_val, ky_val)] = rng.choice(
            range(66_00_000),
            size=N_sample,
            replace=False
        ).tolist()

        seed_map[(kx_val, ky_val)] = rng.choice(
            range(166_00_000),
            size=N_sample,
            replace=False
        ).tolist()




    seeds = seed_map[(kx, ky)]

    H_size = cv(nup, ndown, kx, ky, J, m, N_sample, seeds)
    print("Hilbert-space dimension:", H_size)


if __name__ == "__main__":
    main()

