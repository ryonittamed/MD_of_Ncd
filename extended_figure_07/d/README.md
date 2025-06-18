# Kinesin RMSD Stage-wise Analysis Pipeline

This README describes the scripts used to calculate and visualize the RMSD (Root Mean Square Deviation) of kinesin molecular dynamics simulations across different experimental conditions and stages.

## Overview

The analysis pipeline includes the following steps:

1. **Calculate RMSD** from trajectory and topology files.
2. **Plot RMSD** time series for different conditions (`free`, `alf3`) and experimental setups.
3. **Stage-wise analysis** of RMSD over segmented trajectory intervals (e.g., Stage 1: initial, Stage 2: docking, Stage 3: stable).

## File Descriptions

### `step01_calculate_rmsd.py`

Calculates the RMSD from `.dcd` trajectory and `.pdb` topology files for a specified residue region.

- **Inputs**:
  - `--dcd`: DCD trajectory file path
  - `--pdb`: PDB topology file path
  - `--target-region`: Residue selection string (e.g., `"resid 7516-8266"`)
  - `--out`: Output CSV file path

- **Output**: CSV file with `rmsd` column for each timestep

---

### `step01_calculate_rmsd.sh`

Runs the RMSD calculation for all simulation replicates across multiple experimental setups (`free`, `alf3` for `kinesin` and `kinesin-no-neckmimic`).

- **Output Directory**: `step01_calculate_rmsd.out/`

---

### `step02_plot_rmsd.py`

Plots the **mean and standard deviation** of RMSD trajectories across replicates for each condition.

- **Inputs**:
  - `--dir`: Directory containing simulation CSV files
  - `--out`: Output plot file (PDF)
  - `--raw-data`: Output CSV summarizing mean, std, ±1SD
  - `--state`: `free` or `alf3`

---

### `step02_plot_rmsd.sh`

Automates plotting for all experimental groups in `experiment-09`.

- **Output Directory**: `step02_plot_rmsd.out/experiment-09/...`

---

### `step03_plot_rmsd_exp5.py`

Plots RMSD over three defined stages:

- Stage 1: `0–2000`
- Stage 2: `2000–2300`
- Stage 3: `2300–22300`

Each stage is plotted in a different color with shaded standard deviation.

- **Inputs**:
  - `--dir`: Directory of CSV files
  - `--out`: Output PDF path
  - `--raw-data`: CSV file summarizing mean and standard deviation

---

### `step03_plot_rmsd_exp5.sh`

Runs the stage-wise RMSD analysis and plotting for `experiment-05` on both `kinesin` and `kinesin-no-neckmimic`.

- **Output Directory**: `step02_plot_rmsd.out/experiment-05/...`

---

## Requirements

- Python packages: `MDAnalysis`, `numpy`, `pandas`, `matplotlib`, `polars`, `pyarrow`, `fastparquet`
- `uv` environment manager for running scripts with dependencies

## Usage Summary

```bash
# Step 1: Calculate RMSD
bash step01_calculate_rmsd.sh

# Step 2: Plot average RMSD over time
bash step02_plot_rmsd.sh

# Step 3: Plot segmented stage-wise RMSD
bash step03_plot_rmsd_exp5.sh
```


