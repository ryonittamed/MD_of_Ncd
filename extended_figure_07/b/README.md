# Kinesin RMSD Analysis

This module provides a reproducible pipeline for calculating and comparing root mean square deviation (RMSD) values of kinesin motor protein segments during coarse-grained MD simulations. The main focus is on comparing simulations with and without a neck-mimic under various nucleotide-bound states (`free`, `alf3`).

---

## Directory Structure

```
├── step01_calculate_rmsd.py     # Extract RMSD for motor domain and stalk
├── step01_calculate_rmsd.sh     # Batch RMSD extraction for all simulation conditions
├── step02_plot_rmsd.py          # Plot and save RMSD comparison between two groups
├── step02_plot_rmsd.sh          # Script to run plotting for each state
├── color_config.py              # Shared color palette for plotting
```

---

## Step 1: Calculate RMSD from Trajectories

### `step01_calculate_rmsd.py`

Computes RMSD of kinesin motor domain (`target-region`) and two stalk regions using MDAnalysis.

#### Inputs:

- `--dcd`: DCD trajectory file
- `--pdb`: PDB topology file
- `--target-region`: Selection string for kinesin dimer (e.g., `"resid 7516-8266"`)
- `--stalk1`: First stalk segment selection (e.g., `"resid 7516-7568"`)
- `--stalk2`: Second stalk segment selection
- `--out`: Output CSV path

#### Output CSV columns:
- `ncd_rmsd`: RMSD of motor domain
- `stalk_rmsd`: RMSD of stalk region (combined from stalk1 and stalk2)

---

### `step01_calculate_rmsd.sh`

Runs `step01_calculate_rmsd.py` for:

- kinesin with neck-mimic (free, alf3)
- kinesin without neck-mimic (free, alf3)

Output files are stored under:

```
step01_calculate_rmsd.out/<experiment>/<case>/<sim>/[free|alf3].csv
```

---

## Step 2: Plot RMSD Comparisons

### `step02_plot_rmsd.py`

Reads `stalk_rmsd` from the CSV files and generates:

- Mean ± Std Dev plots for neckmimic vs no-neckmimic groups
- CSV with statistical summaries over time

#### Inputs:

- `--dir-kinesin`: Path to CSVs for neckmimic group
- `--dir-no-kinesin`: Path to CSVs for no-neckmimic group
- `--out`: Output PDF plot
- `--raw-data`: Output summary CSV
- `--state`: Either `free` or `alf3`

---

### `step02_plot_rmsd.sh`

Automates plotting for both states:

```bash
bash step02_plot_rmsd.sh
```

Creates:

- `step02_plot_rmsd.out/experiment-09/free/out.pdf`
- `step02_plot_rmsd.out/experiment-09/alf3/out.pdf`
- Summary CSVs in the same directories

---

## Requirements

All scripts assume `uv` virtual environment with:

- `numpy`
- `pandas`
- `polars`
- `matplotlib`
- `pyarrow` or `fastparquet`
- `MDAnalysis`

---

## Notes

- Plots use color coding defined in `color_config.py`.
- RMSD is computed using the backbone atoms of selected residues.
- Only simulations with 100,000 frames are included for comparison.


