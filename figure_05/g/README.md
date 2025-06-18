# Kinesin φ-Angle Transition Histogram Analysis

This repository contains a pipeline for computing and visualizing the dynamics of φ (azimuthal angle) transitions in coarse-grained simulations of kinesin with or without the neck-mimic structure.

---

## File Overview

```
├── step01_write_cv.py      # Computes θ/φ angles and contact metrics from trajectories
├── step01_write_cv.sh      # Batch script to apply CV extraction across simulation cases
├── step02_plot_cv.py       # Plots φ histogram time evolution with reference state overlays
├── step02_plot_cv.sh       # Batch script for histogram generation
```

---

## Step 1: Compute Collective Variables

### `step01_write_cv.py`

This script calculates:
- Spherical angles θ and φ from stalk orientation in rotated microtubule-aligned coordinates.
- Native contact ratio and RMSD using `msm_utils.angle_vs_contacts`.

#### Input Arguments

- `--sel-stalk1`, `--sel-stalk2`: Residue selection strings for stalk vector endpoints.
- `--sel-msu1`, `--sel-msu2`, `--sel-msu3`: MT residues to define orthonormal basis vectors.
- `--pdb`, `--dcd`: Topology and trajectory.
- `--itp`: ITP file for contact mapping.
- `--out`: Output `.parquet` file.

#### Output

A `.parquet` file with:
- `theta`, `phi`: angular data
- `contact_count_ratio`, `rmsd`: contact analysis

---

### `step01_write_cv.sh`

Runs `step01_write_cv.py` over a set of simulations (e.g., `sim-0001` to `sim-0100`) under the `kinesin` case.

```bash
bash step01_write_cv.sh
```

Output is saved under `step01_write_cv.out/<case>/<sim-ID>/trajectory.parquet`.

---

## Step 2: Plot Histogram of Transition Behavior

### `step02_plot_cv.py`

This script:
- Loads φ values from successful transition paths.
- Aligns the trajectories at the point of neck-mimic docking (contact ratio > 0.99).
- Calculates histogram over time and overlays ±1 std bands of reference free/AlF₃ states.
- Saves PDF plot.

#### Input Arguments

- `--dir`: Input directory containing `.parquet` files
- `--out`: Output plot file (`.pdf`)
- `--target` *(optional)*: Index of a specific simulation to analyze

---

### `step02_plot_cv.sh`

Wrapper for running `step02_plot_cv.py` with predefined data and output paths.

```bash
bash step02_plot_cv.sh
```

Results are saved in `step02_plot_cv.out/<case>/`.

---

## Dependencies

- `numpy`
- `pandas`
- `polars`
- `matplotlib`
- `seaborn`
- `MDAnalysis`
- `pyarrow` or `fastparquet`
- `tqdm`

Use [`uv`](https://github.com/astral-sh/uv) for environment isolation during execution.

---

## Notes

- The `φ` angle reflects rotational changes in kinesin stalk, critical for understanding neck-mimic interaction.
- Only transitions that result in successful docking (contact ratio > 0.99) and path1 (positive direction) are included in the plot.
- Reference state distributions (`free.csv`, `alf3.csv`) must exist under `../analysis-04/step02_plot_distributions.out/`.


