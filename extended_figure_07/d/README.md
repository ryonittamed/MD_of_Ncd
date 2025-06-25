
# RMSD Analysis Pipeline for Kinesin Simulations (Standard and Experiment 05)

This repository contains a set of scripts for calculating and visualizing RMSD (root-mean-square deviation) of kinesin systems with or without the neck mimic domain from molecular dynamics (MD) simulations. It includes both standard analysis and specific analysis tailored for Experiment 05.

## Directory Structure

```
.
├── step01_calculate_rmsd.py     # Calculate RMSD for individual trajectories
├── step01_calculate_rmsd.sh     # Bash script to run RMSD calculation for multiple simulations
├── step02_plot_rmsd.py          # Plot RMSD time series with mean ± std bands (standard analysis)
├── step02_plot_rmsd.sh          # Bash script to automate step02 plotting
├── step03_plot_rmsd_exp5.py     # Specialized plot for Experiment 05 with phase segmentation
├── step03_plot_rmsd_exp5.sh     # Bash script to automate step03 plotting
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
  - pathlib

## Step 1: Calculate RMSD

**Script:** `step01_calculate_rmsd.py`  
**Example usage:**

```bash
python step01_calculate_rmsd.py \
  --target-region "resid 7516-8266" \
  --dcd /path/to/trajectory.dcd \
  --pdb /path/to/topology.pdb \
  --out /path/to/output/trajectory.csv
```

Or execute in batch:

```bash
bash step01_calculate_rmsd.sh
```

**Note:** Please modify the file paths in the bash scripts according to your environment.

## Step 2: Plot RMSD Time Series (Standard)

**Script:** `step02_plot_rmsd.py`  
**Example usage:**

```bash
python step02_plot_rmsd.py \
  --dir /path/to/data_dir \
  --out /path/to/output/out.pdf \
  --state free
```

Or execute in batch:

```bash
bash step02_plot_rmsd.sh
```

**Note:** Please modify the file paths in the bash scripts according to your environment.

## Step 3: Plot RMSD for Experiment 05

This step segments the RMSD time series into three predefined stages:

- Stage 1: 0–2000 steps
- Stage 2: 2000–2300 steps
- Stage 3: 2300–22300 steps

**Script:** `step03_plot_rmsd_exp5.py`  
**Example usage:**

```bash
python step03_plot_rmsd_exp5.py \
  --dir /path/to/data_dir \
  --out /path/to/output/out.pdf
```

Or execute in batch:

```bash
bash step03_plot_rmsd_exp5.sh
```

**Note:** Please modify the file paths in the bash scripts according to your environment.

## Output

- CSV files containing RMSD time series
- PDF plots visualizing RMSD with mean ± standard deviation bands
- For Experiment 05, plots segmented into three distinct phases with different colors

## Notes

- This pipeline uses MDAnalysis for RMSD calculation relative to the initial structure for specified regions.
- The plotting scripts provide both general time series plots and specialized segmented views for particular experimental designs.
