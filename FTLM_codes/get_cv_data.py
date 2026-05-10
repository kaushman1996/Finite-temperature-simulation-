import matplotlib
matplotlib.use("Agg")  # avoid Qt errors on HPC nodes

import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import re
from concurrent.futures import ProcessPoolExecutor


# -----------------------------
# Utility functions
# -----------------------------
def load_eigenvalues(file):
    return np.load(file).flatten()

def load_projection(file):
    return np.load(file).flatten()

def extract_size_from_filename(filename):
    """Extract Hilbert space size using a robust regex."""
    match = re.search(r"_size(\d+)_", filename)
    if match is None:
        raise ValueError(f"Could not extract size from filename: {filename}")
    return int(match.group(1))


# -----------------------------
# Core computation for one sample
# -----------------------------
def process_sample(E_file, P_file, E0):
    eigenvalues = load_eigenvalues(E_file)
    projections = load_projection(P_file)

    mvalues = eigenvalues.shape[0]
    eigenvalues = eigenvalues - E0

    size = extract_size_from_filename(E_file)

    # Temperature grid
    T = np.linspace(1, 200, 20000) / 11.6
    beta = 1.0 / (T + 1e-15)

    exp_term = np.exp(-np.outer(beta, eigenvalues))

    num = np.dot(exp_term, eigenvalues * projections) * size
    deno = np.dot(exp_term, projections) * size

    return num / mvalues, deno / mvalues


# Wrapper needed for multiprocessing (no lambdas allowed)
def process_wrapper(args):
    return process_sample(*args)


# -----------------------------
# MAIN PARALLEL ANALYSIS
# -----------------------------
plt.figure(figsize=(10, 6))

# Loop through J directories
for J_dir in ['J_0.0','J_0.2', 'J_0.4', 'J_0.6']:#, 'J_2.2', 'J_2.4', 'J_2.6', 'J_2.8', 'J_3.0']:
    eigenvalue_files = sorted(glob.glob(os.path.join(J_dir, 'E_*_sample*.npy')))
    if not eigenvalue_files:
        print(f"No eigenvalue files in {J_dir}")
        continue

    # Ground state energy across all samples
    E0 = np.min([np.min(load_eigenvalues(f)) for f in eigenvalue_files])
    print(f"{J_dir}: Ground state energy E0 = {E0}")

    # Prepare tasks for parallel execution
    tasks = []
    for E_file in eigenvalue_files:
        P_file = E_file.replace('E_', 'P_')
        tasks.append((E_file, P_file, E0))

    total_num = 0
    total_deno = 0

    # Parallel execution using 24 cores
    with ProcessPoolExecutor(max_workers=24) as executor:
        for num, deno in executor.map(process_wrapper, tasks):
            total_num += num
            total_deno += deno

    # Compute Cv
    T = np.linspace(1, 200, 20000) / 11.6
    beta = 1.0 / (T + 1e-15)
    Cv = -beta * beta * np.gradient(total_num / total_deno, beta) / 36

    # Save results
    J_value = J_dir.split('_')[1]
    temp_scaled = T * 11.6

    np.savetxt(
        f'cv_J{J_value}_Nsample.txt',
        np.column_stack([temp_scaled, Cv]),
        header='Temperature_scaled  Cv'
    )

    # Plot
    plt.plot(temp_scaled, Cv, label=f'J={J_value}')


# -----------------------------
# Final plot formatting
# -----------------------------
plt.xscale('log')
plt.xlabel('Temperature (T) [scaled]')
plt.ylabel('$C_v$')
plt.title('$C_v$ vs. Temperature for different $J$')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("cv_vs_T_all_Js.png")
plt.show()

