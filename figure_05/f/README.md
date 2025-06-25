
# Collective Variable Analysis Pipeline for Kinesin Simulations

This repository contains a set of scripts for extracting and visualizing collective variables (CVs), specifically theta and phi angles, from molecular dynamics (MD) simulations of kinesin systems with and without the neck mimic domain.

## Directory Structure

```
.
├── step01_write_cv.py           # Extract CVs (theta, phi) from trajectories
├── step01_write_cv.sh           # Bash script to run CV extraction for multiple simulations
├── step02_plot_cv.py            # Plot time series distributions of CVs
├── step02_plot_cv.sh            # Bash script to automate plotting
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

## Step 2: Plot CV Distributions

**Script:** `step02_plot_cv.py`  
**Example usage:**

```bash
python step02_plot_cv.py \
  --kinesin /path/to/with_neckmimic_dir \
  --no-kinesin /path/to/no_neckmimic_dir \
  --out /path/to/output/out.pdf \
  --raw-data /path/to/output/data.csv
```

Or execute in batch:

```bash
bash step02_plot_cv.sh
```

**Note:** Please modify the file paths in the bash scripts according to your environment.

## Color Configurations

The file `color_config.py` defines the color codes used consistently across all plots:
- `with_neckmimic`: Blue (`#0072B2`)
- `without_neckmimic`: Olive (`#6A6F2E`)

## Output

- Parquet files containing the collective variables (`theta`, `phi`)
- CSV summary of trajectory data
- PDF files visualizing time series distributions with confidence intervals

## Notes

- This pipeline uses MDAnalysis for trajectory handling.
- Spherical angles (`theta`, `phi`) are calculated relative to a dynamically defined coordinate system based on microtubule subunits.
- Trajectories showing transitions to abnormal paths are filtered based on heuristics applied to the `phi` angle.
