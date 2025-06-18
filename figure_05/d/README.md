# Collective Variable Analysis and Visualization Pipeline

This repository contains scripts to compute and visualize collective variables (CVs) from molecular dynamics simulations of kinesin in various biochemical states.

## Directory Structure

```
.
├── step01_write_cv.py            # Computes spherical coordinates from MD trajectories
├── step01_write_cv.sh            # Batch processes multiple simulations
├── step02_plot_distributions.py  # Visualizes 2D KDE plots of the computed CVs
├── step02_plot_distributions.sh  # Runs plotting script for different states
├── color_config.py               # Color definitions for plotting
```

---

## Step 1: Compute Collective Variables

### `step01_write_cv.py`

This script calculates spherical coordinates (θ and φ) of the stalk vector in a rotated coordinate system defined by three microtubule subunits.

### Arguments

- `--sel-stalk1`, `--sel-stalk2`: Atom selection strings for two stalk segments.
- `--sel-msu1`, `--sel-msu2`, `--sel-msu3`: Selection strings for three microtubule subunits (to define coordinate axes).
- `--pdb`: Topology file (PDB format).
- `--dcd`: Trajectory file (DCD format).
- `--out`: Output file name (Parquet format).

### Output

A `.parquet` file containing two columns:
- `theta`: Polar angle in radians.
- `phi`: Azimuthal angle in radians.

---

## Step 1 (Batch): Process Multiple Simulations

### `step01_write_cv.sh`

This shell script batch-processes multiple simulation cases and replicates. It automatically runs `step01_write_cv.py` across all simulations, generating `trajectory.parquet` files for each.

### How to Run

```bash
bash step01_write_cv.sh
```

> Uses `uv` to manage dependencies and isolate environments per run.

---

## Step 2: Plot Distributions

### `step02_plot_distributions.py`

This script reads CV data and produces 2D KDE plots with marginal distributions. It compares two simulation conditions (e.g., with and without neck mimic).

### Arguments

- `--dirs`: One or more directories containing `.csv` files of CVs (e.g., `"free.csv"` or `"alf3.csv"`).
- `--out_dir`: Output directory for the plot.
- `--state`: A label indicating which dataset to visualize (e.g., `"free"` or `"alf3"`).

### Output

- `hist_eq_free_revised.pdf`  
- `hist_eq_alf3_revised.pdf`  
  2D KDE plots with marginals comparing `theta` and `phi` distributions.

---

## Step 2 (Batch): Run Plotting Commands

### `step02_plot_distributions.sh`

This script runs `step02_plot_distributions.py` for both `"free"` and `"alf3"` states using the output from Step 1.

### How to Run

```bash
bash step02_plot_distributions.sh
```

### Output Directory

All plots are saved in `step02_plot_distributions.out/`.

---

## Dependencies

These scripts assume use of the following Python packages (managed via `uv`):

- `numpy`
- `polars`
- `pandas`
- `MDAnalysis`
- `matplotlib`
- `seaborn`
- `pyarrow` / `fastparquet` (for `.parquet` handling)

---

## Notes

- Input files (`trajectory.dcd`, `free.pdb`) and raw data are not included in the repository.
- Please contact the corresponding author for access to simulation input/output files.
- Angle unwrapping and path filtering are handled within the plotting script to exclude biologically implausible transitions.

