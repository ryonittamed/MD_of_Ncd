
# RMSD Analysis Pipeline for Kinesin Simulations

This repository contains a set of scripts for calculating and visualizing RMSD (root-mean-square deviation) of kinesin systems with or without the neck mimic domain from molecular dynamics (MD) simulations.

## Directory Structure

```
.
├── step01_calculate_rmsd.py     # Calculate RMSD of stalk and neck mimic domains
├── step01_calculate_rmsd.sh     # Bash script to run RMSD calculation for multiple simulations
├── step02_plot_rmsd.py          # Plot RMSD time series with mean ± std bands
├── step02_plot_rmsd.sh          # Bash script to automate plotting
├── color_config.py              # Color settings for plots
├── output/                      # Output files (csv, pdf)
└── input/                       # Input trajectory and topology files
```

## Requirements

- Python >= 3.8
- Python libraries:
  - numpy
  - pandas
  - matplotlib
  - MDAnalysis

## Step 1: Calculate RMSD

**Script:** `step01_calculate_rmsd.py`  
**Example usage:**

```bash
python step01_calculate_rmsd.py \
  --target-region "resid 7516-8266" \
  --stalk1 "resid 7516-7568" \
  --stalk2 "resid 7899-7951" \
  --dcd /path/to/trajectory.dcd \
  --pdb /path/to/topology.pdb \
  --out /path/to/output/trajectory.csv
```

Or execute in batch:

```bash
bash step01_calculate_rmsd.sh
```

**Note:** Please modify the file paths in the bash scripts according to your environment.

## Step 2: Plot RMSD Time Series

**Script:** `step02_plot_rmsd.py`  
**Example usage:**

```bash
python step02_plot_rmsd.py \
  --dir-kinesin /path/to/kinesin/csv_files \
  --dir-no-kinesin /path/to/kinesin-no-neckmimic/csv_files \
  --out /path/to/output/out.pdf \
  --state free
```

Or execute in batch:

```bash
bash step02_plot_rmsd.sh
```

**Note:** Please modify the file paths in the bash scripts according to your environment.

## Color Configurations

The file `color_config.py` defines the color codes used consistently in plots:
- `with_neckmimic`: Blue (`#0072B2`)
- `without_neckmimic`: Olive (`#6A6F2E`)
- `contact_ratio`: Orange (`#ff4500`)

## Output

- CSV files containing the RMSD time series for neck mimic and stalk regions
- PDF plots showing RMSD time series with mean ± standard deviation bands

## Notes

- This pipeline uses MDAnalysis for trajectory handling.
- RMSD is computed relative to the initial structure for specified regions (neck mimic and stalk).
- The plotting script compares RMSD profiles between kinesin with and without the neck mimic domain.
