# Kinesin Collective Variable Processing and Visualization

This repository contains scripts to compute, summarize, and visualize collective variables (CVs) such as angular motion and native contacts from molecular dynamics simulations of kinesin.

---

## File Overview

```
├── step01_write_cv.py      # Computes θ/φ angles and native contact ratios from MD trajectories
├── step01_write_cv.sh      # Batch script to compute CVs for multiple simulation runs
├── step02_plot_cv.py       # Analyzes and plots statistics of contact ratio and angle
├── step02_plot_cv.sh       # Batch script to generate plots and CSV summaries
├── color_config.py         # Color palette definitions used in plots
```

---

## Step 1: Compute Collective Variables

### `step01_write_cv.py`

This script computes spherical angular coordinates (θ and φ) of the kinesin stalk relative to the microtubule coordinate system. It also calculates the native contact ratio and RMSD using provided topology and force field files.

### Arguments

- `--sel-stalk1`, `--sel-stalk2`: Residue selection strings for the stalk regions.
- `--sel-msu1`, `--sel-msu2`, `--sel-msu3`: Selections for three microtubule subunits to define a local coordinate system.
- `--pdb`: Topology file.
- `--dcd`: Trajectory file.
- `--itp`: ITP topology file (for native contact computation).
- `--out`: Output Parquet file.

### Output

A `.parquet` file containing:
- `theta`: Polar angle (rad)
- `phi`: Azimuthal angle (rad)
- `contact_count_ratio`: Ratio of native contacts between kinesin and microtubule
- `rmsd`: Backbone RMSD of the kinesin neck-mimic region

---

### `step01_write_cv.sh`

Batch script that runs `step01_write_cv.py` across multiple simulation directories (e.g., `sim-0001` to `sim-0100`) for different experimental conditions.

Run using:

```bash
bash step01_write_cv.sh
```

---

## Step 2: Plot Time-Series and Statistics

### `step02_plot_cv.py`

This script:
- Loads CV data for multiple simulation runs
- Filters for trajectories following a specific transition path
- Computes the mean, median, and percentiles of `phi` and `contact_count_ratio`
- Outputs plots (PDF)

### Arguments

- `--dir`: Directory containing `.parquet` files
- `--out`: Output path for the PDF plot
- `--target` *(optional)*: Index of the specific simulation to process

### Output

- A dual-axis PDF plot showing:
  - Median `contact_count_ratio` (right axis)
  - Median `phi` angle (left axis)

---

### `step02_plot_cv.sh`

Runs `step02_plot_cv.py` on all simulations in a specified case directory and saves output to:

```
step02_plot_cv.out/<CASE_DIR>/
```

Run using:

```bash
bash step02_plot_cv.sh
```

---

## Dependencies

These scripts rely on:

- `numpy`
- `pandas`
- `polars`
- `MDAnalysis`
- `matplotlib`
- `seaborn`
- `pyarrow` or `fastparquet`
- `tqdm`

Dependency management is handled via `uv`.

---

## Notes

- Simulation input files and trajectory data are not included.
- Contact ratio and RMSD computations rely on `msm_utils.plot_angle_vs_native_contacts.angle_vs_contacts`.
- The `color_config.py` file defines colors for consistent figure styling.

