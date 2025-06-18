# Collective Variable Analysis and Comparison for Kinesin Simulations

This repository contains scripts for extracting, processing, and comparing collective variables (CVs) such as angular orientation and neck-mimic contact behavior from coarse-grained molecular dynamics (MD) simulations of kinesin under different conditions.

---

## Files Overview

```
├── step01_write_cv.py      # Extracts θ/φ angles from kinesin stalk orientation
├── step01_write_cv.sh      # Batch processing script for multiple simulation cases
├── step02_plot_cv.py       # Compares CV trajectories (e.g., φ angle) across cases and generates plots
├── step02_plot_cv.sh       # Runs plotting script for both neck-mimic and no-neck-mimic conditions
├── color_config.py         # Centralized color configuration used in plotting
```

---

## Step 1: Extract Collective Variables

### `step01_write_cv.py`

This script computes θ (polar) and φ (azimuthal) angles from the kinesin stalk vector in a rotated coordinate system defined by three microtubule subunits.

### Arguments

- `--sel-stalk1`, `--sel-stalk2`: Atom selection strings for stalk segments
- `--sel-msu1`, `--sel-msu2`, `--sel-msu3`: Microtubule subunit selections for coordinate alignment
- `--pdb`: PDB file for topology
- `--dcd`: DCD file for trajectory
- `--out`: Output file path (Parquet format)

### Output

A `.parquet` file with:
- `theta`: Polar angle (radians)
- `phi`: Azimuthal angle (radians)

---

### `step01_write_cv.sh`

Batch script for running `step01_write_cv.py` across multiple simulations and experimental conditions (e.g., `kinesin`, `kinesin-no-neckmimic`, etc.).

### Example Usage

```bash
bash step01_write_cv.sh
```

Output files will be saved under `step01_write_cv.out/<case>/<sim-ID>/trajectory.parquet`.

---

## Step 2: Compare Simulation Outcomes

### `step02_plot_cv.py`

This script reads the CVs from two simulation conditions (with and without neck-mimic), selects transitions of interest, calculates statistical summaries (mean, percentile), and outputs a comparative plot.

### Arguments

- `--kinesin`: Path to Parquet files for kinesin with neck-mimic
- `--no-kinesin`: Path to Parquet files for kinesin without neck-mimic
- `--out`: Output PDF path for the comparison plot
- `--raw-data`: Output CSV file for statistical summary

### Output

- A plot (`out.pdf`) comparing φ angle dynamics between conditions
- A CSV (`data.csv`) summarizing means, medians, and percentiles across MD time

---

### `step02_plot_cv.sh`

Runs `step02_plot_cv.py` using `uv` for environment isolation.

### Example Usage

```bash
bash step02_plot_cv.sh
```

Results are saved under `step02_plot_cv.out/`.

---

## Dependencies

These scripts require the following Python packages:

- `numpy`
- `polars`
- `pandas`
- `matplotlib`
- `seaborn`
- `MDAnalysis`
- `pyarrow` or `fastparquet`

Execution assumes the use of `uv` to manage dependencies.

---

## Notes

- Raw MD trajectory files are not included.
- Path filtering excludes simulations that undergo undesired transitions.
- Angle unwrapping and trajectory slicing are applied before statistics and plotting.
- Colors are defined in `color_config.py` for consistency across figures.

