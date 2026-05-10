import numpy as np
import os
import time
import matplotlib.pyplot as plt

# -----------------------------
# Global seed for reproducibility
# -----------------------------
np.random.seed(12345)

# Logging
os.makedirs("logs", exist_ok=True)
log_file = "logs/PTMC_progress.txt"

# Try to import numba
try:
    from numba import njit, prange
    NUMBA_AVAILABLE = True
except Exception:
    NUMBA_AVAILABLE = False


# ==========================
# JIT-Accelerated Kernels
# ==========================

if NUMBA_AVAILABLE:
    @njit(fastmath=True)
    def local_energy_site(i, cfg, aA, aA1, aA2):
        """
        Local energy contribution from “site” i,
        using precomputed coefficient arrays aA, aA1, aA2.
        """
        s = 0.0
        coeffs = aA[i]
        n1 = aA1[i]
        n2 = aA2[i]
        Z = coeffs.shape[0]
        for k in range(Z):
            s += coeffs[k] * cfg[n1[k]] * cfg[n2[k]]
        return s

    @njit(fastmath=True)
    def total_energy_jit(cfg, aA, aA1, aA2):
        """
        Total energy: each interaction counted twice in the site loop,
        so we multiply by 0.5 at the end.
        """
        s = 0.0
        N = cfg.shape[0]
        for i in range(N):
            coeffs = aA[i]
            n1 = aA1[i]
            n2 = aA2[i]
            Z = coeffs.shape[0]
            subtotal = 0.0
            for k in range(Z):
                subtotal += coeffs[k] * cfg[n1[k]] * cfg[n2[k]]
            s += subtotal
        return 0.5 * s

    @njit(fastmath=True)
    def mc_move_single(cfg, beta, aA, aA1, aA2):
        """
        Performs one local MC move (swap occupations at two sites) in-place.
        Returns ΔE_total (0.0 if rejected).
        """
        N = cfg.shape[0]
        i1 = np.random.randint(0, N)
        i2 = np.random.randint(0, N)
        if i1 == i2:
            return 0.0
        if cfg[i1] == cfg[i2]:
            return 0.0

        e_before = local_energy_site(i1, cfg, aA, aA1, aA2) \
                 + local_energy_site(i2, cfg, aA, aA1, aA2)

        # swap
        tmp = cfg[i1]
        cfg[i1] = cfg[i2]
        cfg[i2] = tmp

        e_after = local_energy_site(i1, cfg, aA, aA1, aA2) \
                + local_energy_site(i2, cfg, aA, aA1, aA2)

        dE = e_after - e_before

        # Metropolis
        if dE <= 0.0 or np.log(np.random.rand()) < -beta * dE:
            return dE
        else:
            # revert
            tmp = cfg[i1]
            cfg[i1] = cfg[i2]
            cfg[i2] = tmp
            return 0.0

    @njit(parallel=True, fastmath=True)
    def local_updates_sweep(configs, energies, betas, aA, aA1, aA2, n_local):
        """
        Perform n_local local moves per replica in parallel.
        configs: (R, N)
        energies: (R,)
        betas: (R,)
        """
        R = configs.shape[0]
        for r in prange(R):
            cfg = configs[r]
            e = energies[r]
            beta = betas[r]
            for _ in range(n_local):
                e += mc_move_single(cfg, beta, aA, aA1, aA2)
            energies[r] = e

    @njit(fastmath=True)
    def attempt_swaps(configs, energies, betas):
        """
        Attempt adjacent replica swaps in-place.
        """
        R = energies.shape[0]
        for i in range(R - 1):
            j = i + 1
            d = (energies[i] - energies[j]) * (betas[i] - betas[j])
            accept = False
            if d >= 0.0:
                accept = True
            else:
                if np.log(np.random.rand()) < d:
                    accept = True
            if accept:
                # swap energies
                tmpE = energies[i]
                energies[i] = energies[j]
                energies[j] = tmpE
                # swap configs
                tmp_row = configs[i].copy()
                configs[i, :] = configs[j, :]
                configs[j, :] = tmp_row

    @njit(parallel=True, fastmath=True)
    def accumulate_sqrtS(configs, expik, sqrtS_sum, sqrtS_count):
        """
        For each replica r:
           S(k) = (1/N) |sum_i n_i e^{i k.r_i}|^2
           val  = sqrt(S(k)/N)
        Accumulate val into sqrtS_sum, count into sqrtS_count.
        """
        R, N = configs.shape
        for r in prange(R):
            cfg = configs[r]
            s_re = 0.0
            s_im = 0.0
            for i in range(N):
                if cfg[i] != 0:
                    s_re += expik[i].real
                    s_im += expik[i].imag
            mod2 = s_re * s_re + s_im * s_im
            S_k = mod2 / N
            val = np.sqrt(S_k / N)
            sqrtS_sum[r] += val
            sqrtS_count[r] += 1

else:
    # --- Non-Numba fallback implementations ---

    def local_energy_site(i, cfg, aA, aA1, aA2):
        return np.sum(aA[i] * cfg[aA1[i]] * cfg[aA2[i]])

    def total_energy_jit(cfg, aA, aA1, aA2):
        return 0.5 * np.sum(aA * cfg[aA1] * cfg[aA2])

    def mc_move_single(cfg, beta, aA, aA1, aA2):
        N = cfg.shape[0]
        i1 = np.random.randint(0, N)
        i2 = np.random.randint(0, N)
        if i1 == i2 or cfg[i1] == cfg[i2]:
            return 0.0
        e_before = local_energy_site(i1, cfg, aA, aA1, aA2) \
                 + local_energy_site(i2, cfg, aA, aA1, aA2)
        cfg[i1], cfg[i2] = cfg[i2], cfg[i1]
        e_after = local_energy_site(i1, cfg, aA, aA1, aA2) \
                + local_energy_site(i2, cfg, aA, aA1, aA2)
        dE = e_after - e_before
        if dE <= 0.0 or np.log(np.random.rand()) < -beta * dE:
            return dE
        else:
            cfg[i1], cfg[i2] = cfg[i2], cfg[i1]
            return 0.0

    def local_updates_sweep(configs, energies, betas, aA, aA1, aA2, n_local):
        R = configs.shape[0]
        for r in range(R):
            cfg = configs[r]
            e = energies[r]
            beta = betas[r]
            for _ in range(n_local):
                e += mc_move_single(cfg, beta, aA, aA1, aA2)
            energies[r] = e

    def attempt_swaps(configs, energies, betas):
        R = energies.shape[0]
        for i in range(R - 1):
            j = i + 1
            d = (energies[i] - energies[j]) * (betas[i] - betas[j])
            accept = (d >= 0.0) or (np.log(np.random.rand()) < d)
            if accept:
                energies[i], energies[j] = energies[j], energies[i]
                tmp = configs[i].copy()
                configs[i, :] = configs[j, :]
                configs[j, :] = tmp

    def accumulate_sqrtS(configs, expik, sqrtS_sum, sqrtS_count):
        R, N = configs.shape
        for r in range(R):
            cfg = configs[r]
            s_re = 0.0
            s_im = 0.0
            for i in range(N):
                if cfg[i] != 0:
                    s_re += expik[i].real
                    s_im += expik[i].imag
            mod2 = s_re * s_re + s_im * s_im
            S_k = mod2 / N
            val = np.sqrt(S_k / N)
            sqrtS_sum[r] += val
            sqrtS_count[r] += 1


# ==========================
# Parallel Tempering Driver
# ==========================

def parallel_tempering_jit(
    aA, aA1, aA2,
    temps,
    expik,
    n_steps=20_000_000,
    equil_steps=2_000_000,
    swap_interval=500,
    measure_interval=50_000
):
    """
    Parallel tempering Monte Carlo with:
      - Specific heat Cv(T)
      - <sqrt(S(k)/N)>(T), where S(k) uses the definition:
        S(k) = (1/N) sum_{i,j} n_i n_j e^{ik (r_i - r_j)}.
      For a fixed configuration, this is equivalent to:
        S(k) = (1/N) |sum_i n_i e^{ik r_i}|^2,
      and we measure sqrt(S(k)/N).
    """

    start_time = time.time()
    N = aA.shape[0]
    R = len(temps)
    betas = 1.0 / temps

    # configs: (R, N)
    configs = np.zeros((R, N), dtype=np.int8)
    energies = np.zeros(R, dtype=np.float64)

    # Initial configuration: fixed number of ones (36) randomly placed
    base_cfg = np.zeros(N, dtype=np.int8)
    base_cfg[:324] = 1

    for r in range(R):
        cfg = base_cfg.copy()
        np.random.shuffle(cfg)
        configs[r] = cfg
        energies[r] = total_energy_jit(cfg, aA, aA1, aA2)

    # Accumulators for Cv
    e_sum = np.zeros(R, dtype=np.float64)
    e_sq_sum = np.zeros(R, dtype=np.float64)
    counter = np.zeros(R, dtype=np.int64)

    # Accumulators for sqrt(S(k)/N)
    sqrtS_sum = np.zeros(R, dtype=np.float64)
    sqrtS_count = np.zeros(R, dtype=np.int64)

    mc_steps_done = 0  # counts local moves

    # Main PTMC loop in blocks of swap_interval moves
    for step in range(0, n_steps, swap_interval):
        # Each call: 'swap_interval' local moves per replica
        local_updates_sweep(configs, energies, betas, aA, aA1, aA2, swap_interval)
        mc_steps_done += swap_interval

        # Replica exchanges
        attempt_swaps(configs, energies, betas)

        # Measurements only after equilibration
        if mc_steps_done > equil_steps:
            # Energy statistics for Cv
            e_sum += energies
            e_sq_sum += energies ** 2
            counter += 1

            # sqrt(S(k)/N) every 'measure_interval' local moves
            if (mc_steps_done % measure_interval) == 0:
                accumulate_sqrtS(configs, expik, sqrtS_sum, sqrtS_count)

        # Periodic logging
        if step > 0 and (step % 500_000 == 0):
            elapsed = time.time() - start_time
            steps_done = step
            steps_total = n_steps
            eta = elapsed / max(steps_done, 1) * (steps_total - steps_done)
            with open(log_file, "a") as f:
                f.write(f"Step {step}/{n_steps}, ETA: {eta/3600:.2f} h, Energies: {energies}\n")

    # Compute Cv(T) from fluctuations
    cv_list = np.zeros(R, dtype=np.float64)
    for k in range(R):
        eff = max(counter[k], 1)
        e_avg = e_sum[k] / eff
        e_sq_avg = e_sq_sum[k] / eff
        cv_list[k] = (e_sq_avg - e_avg ** 2) * (betas[k] ** 2)

    # Compute <sqrt(S(k)/N)>
    sqrtS_avg = np.zeros(R, dtype=np.float64)
    for k in range(R):
        if sqrtS_count[k] > 0:
            sqrtS_avg[k] = sqrtS_sum[k] / sqrtS_count[k]
        else:
            sqrtS_avg[k] = 0.0

    return cv_list, sqrtS_avg


# ==========================
# Main: run PTMC
# ==========================

if __name__ == "__main__":
    # Lattice size you used in your NPZ
    LX, LY = 36, 36
    N = LX * LY

    # Load interaction arrays
    data = np.load("arrays_36X36_dbya_10.0.npz")
    aA, aA1, aA2 = data["aA"], data["aA1"], data["aA2"]

    # Triangular-lattice coordinates
    coordinates = np.empty((N, 2), dtype=np.float64)
    idx = 0
    for j in range(LX):
        for i in range(LY):
            coordinates[idx, :] = j * np.array([np.sqrt(3)/2, 0.5]) + i * np.array([0., 1.0])
            idx += 1

    # Momentum k at which to measure S(k)
    kx = 2.0 * np.pi / np.sqrt(3.0)
    ky = 0.0

    expik = np.empty(N, dtype=np.complex128)
    for i in range(N):
        x, y = coordinates[i]
        expik[i] = np.exp(1j * (kx * x + ky * y))

    # Temperature ladder (geometric)
    T0 = 0.028
    T_end = 0.035
    R = 32
    temps = T0 * (T_end / T0) ** (np.arange(R) / (R - 1))

    print("Temperatures:", temps)

    os.makedirs("results_parallel_tempering_parallel", exist_ok=True)

    # NOTE: tune n_steps, equil_steps for your cluster
    cv_list, sqrtS_avg = parallel_tempering_jit(
        aA, aA1, aA2,
        temps,
        expik,
        n_steps=300000_000_000,      # total local moves per replica
        equil_steps=120000_000_000,   # discard first 1e6 moves as equilibration
        swap_interval=500,
        measure_interval=50_000  # measure sqrt(S(k)/N) every 50k moves
    )

    # Save data: T, Cv, <sqrt(S(k)/N)>
    out_txt = "results_parallel_tempering_parallel/Cv_and_sqrtSk_vs_T_parallel.txt"
    np.savetxt(
        out_txt,
        np.column_stack([temps, cv_list, sqrtS_avg]),
        delimiter=",",
        header="Temperature, Cv, <sqrt(S(k)/N)>",
        comments=""
    )
    print("Saved:", out_txt)

    # Plot Cv(T)
    plt.figure(figsize=(8, 6))
    plt.plot(temps, cv_list, "o-", lw=1.5, ms=3)
    plt.xlabel("Temperature (T)", fontsize=14)
    plt.ylabel("Specific Heat $C_v$", fontsize=14)
    plt.title("Parallel Tempering: $C_v(T)$", fontsize=15)
    plt.tight_layout()
    plt.savefig("results_parallel_tempering_parallel/Cv_vs_T_parallel.png", dpi=200)
    plt.close()

    # Plot <sqrt(S(k)/N)>(T)
    plt.figure(figsize=(8, 6))
    plt.plot(temps, sqrtS_avg, "o-", lw=1.5, ms=3)
    plt.xlabel("Temperature (T)", fontsize=14)
    plt.ylabel(r"$\langle \sqrt{S(k)/N} \rangle$", fontsize=14)
    plt.title("Parallel Tempering: Structure factor at fixed $k$", fontsize=15)
    plt.tight_layout()
    plt.savefig("results_parallel_tempering_parallel/sqrtSk_vs_T_parallel.png", dpi=200)
    plt.close()

    print("Done.")
