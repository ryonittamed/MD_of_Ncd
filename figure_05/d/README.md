
# Collective Variable Analysis Pipeline

This repository contains a set of scripts for calculating and visualizing collective variables (CVs) from molecular dynamics (MD) simulations, specifically for kinesin systems with or without the neck mimic domain.

## Directory Structure

```
.
├── step01_write_cv.py           # Extract CVs (theta, phi) from trajectories
├── step01_write_cv.sh           # Bash script to run CV extraction for multiple trajectories
├── step02_plot_distributions.py # Plot joint KDE of theta and phi distributions
├── step02_plot_distributions.sh # Bash script to automate plotting for multiple states
├── color_config.py              # Color settings for plots
├── output/                      # Output files (parquet, csv, pdf)
└── input/                       # Input trajectory and topology files
```

## Requirements

- Python >= 3.8
- Python libraries:
  - numpy
  - pandas
  - polars
  - matplotlib
  - seaborn
  - pyarrow
  - fastparquet
  - MDAnalysis

## Step 1: Extract Collective Variables

**Script:** `step01_write_cv.py`  
**Example usage:**

```bash
python step01_write_cv.py \
  --sel-stalk1 "resid 7516-7568" \
  --sel-stalk2 "resid 7884-7936" \
  --sel-msu1 "resid 836-1252" \
  --sel-msu2 "resid 2506-2922" \
  --sel-msu3 "resid 4593-5010" \
  --dcd /path/to/trajectory.dcd \
  --pdb /path/to/topology.pdb \
  --out /path/to/output/trajectory.parquet
```

Or execute in batch:

```bash
bash step01_write_cv.sh
```

**Note:** Please modify the file paths in the bash scripts according to your environment.

## Step 2: Plot Distributions

**Script:** `step02_plot_distributions.py`  
**Example usage:**

```bash
python step02_plot_distributions.py \
  --dirs /path/to/kinesin.equiliblium /path/to/kinesin-no-neckmimic.equiliblium \
  --out_dir /path/to/output \
  --state free
```

Or execute in batch:

```bash
bash step02_plot_distributions.sh
```

**Note:** Please modify the file paths in the bash scripts according to your environment.

## Color Configurations

The file `color_config.py` defines the color codes used consistently across all plots.

## Output

- Parquet or CSV files containing the collective variable data (`theta`, `phi`).
- PDF files of KDE plots visualizing the joint distribution of `theta` and `phi`.

## Notes

- This pipeline uses MDAnalysis for trajectory handling.
- It calculates spherical angles relative to a dynamically defined coordinate system based on microtubule subunits.
- Trajectories showing abnormal paths are automatically filtered based on a heuristic applied to the `phi` angle.
