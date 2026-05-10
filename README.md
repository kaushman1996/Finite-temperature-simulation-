# Data and codes for: Melting temperature shifts from quantum fluctuations in generalized Wigner crystals

This repository contains the data and selected representative codes supporting the manuscript:

**Title:** *Melting temperature shifts from quantum fluctuations in generalized Wigner crystals*  
**Authors:** Aman Kumar, Sogoud Sherif, Veit Elser, Hitesh J. Changlani  
**Journal:** Submitted (Physical Review X)  
**Year:** 2026

---

## Repository contents

The repository is organized into two main parts:  
(i) **figure-resolved data directories**, and  
(ii) **codes used to generate the data**.

### Figure data

Each directory below contains the raw and processed data used to generate the corresponding figure in the manuscript or appendices.

- `Figure1/` – Data for Fig. 1  
- `Figure2/` – Data for Fig. 2  
- `Figure3/` – Data for Fig. 3  
- `Figure4/` – Data for Fig. 4  
- `Figure5_appendA/` – Data for Fig. 5 (Appendix A)  
- `Figure6_appendC/` – Data for Fig. 6 (Appendix C)  
- `Figure7_appendD/` – Data for Fig. 7 (Appendix D)  
- `Figure8_appendixF/` – Data for Fig. 8 (Appendix F)

---

### Codes

The following directories contain the simulation and analysis codes used to produce the data in this repository.  
These codes are provided for transparency and reproducibility.

- `MC_parallel_tempering_codes/`  
  Monte Carlo simulation codes implementing **parallel tempering** to study thermal melting and finite‑temperature properties of generalized Wigner crystal phases.

- `FTLM_codes/`  
  Codes implementing the **Finite‑Temperature Lanczos Method (FTLM)** for computing thermodynamic quantities. 


---

## Methods and reproducibility

All data were generated using a combination of:
- Exact diagonalization and FTLM calculations
- Monte Carlo simulations with parallel tempering
- Implementations based on the **QuSpin** library, supplemented by custom numerical and analysis scripts

The directory structure is designed to allow direct reproduction of all figures in the manuscript using the supplied data and codes.

---

## Notes

- Energy, temperature, and interaction parameters follow the conventions defined in the main text and appendices of the manuscript.
- Simulation details and parameter choices are described in the paper; figure‑specific details may also be documented within individual directories.

---

## Contact

For questions related to the data or codes, please contact:

**Aman Kumar**  
Email: akumar@magnet.fsu.edu
