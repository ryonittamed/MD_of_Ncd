
# Collective Variable Analysis Pipeline for Kinesin Simulations (Histogram and Time Evolution)

This repository contains a set of scripts for calculating and visualizing collective variables (CVs), including theta, phi, contact count ratio, and RMSD, from molecular dynamics (MD) simulations of kinesin systems with or without the neck mimic domain.

## Directory Structure

```
.
├── step01_write_cv.py           # Extract CVs (theta, phi, contact ratio, RMSD) from trajectories
├── step01_write_cv.sh           # Bash script to run CV extraction for multiple simulations
├── step02_plot_cv.py            # Plot time-evolving histograms with comparisons to equilibrium distributions
├── step02_plot_cv.sh            # Bash script to automate plotting
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
  - tqdm
  - msm_utils (for native contact analysis)

## Step 1: Extract Collective Variables

**Script:** `step01_write_cv.py`  
**Example usage:**

```bash
python step01_write_cv.py \
  --sel-stalk1 "resid 7516-7568" \
  --sel-stalk2 "resid 7899-7951" \
  --sel-msu1 "resid 836-1252" \
  --sel-msu2 "resid 2506-2922" \
  --sel-msu3 "resid 4593-5010" \
  --dcd /path/to/trajectory.dcd \
  --pdb /path/to/topology.pdb \
  --itp /path/to/topology.itp \
  --out /path/to/output/trajectory.parquet
```

Or execute in batch:

```bash
bash step01_write_cv.sh
```

**Note:** Please modify the file paths in the bash scripts according to your environment.

## Step 2: Plot Time-evolving Histograms

**Script:** `step02_plot_cv.py`  
**Example usage:**

```bash
python step02_plot_cv.py \
  --dir /path/to/data_dir \
  --out /path/to/output/out.pdf \
  --raw-data /path/to/output/data.csv
```

Or execute in batch:

```bash
bash step02_plot_cv.sh
```

**Note:** Please modify the file paths in the bash scripts according to your environment.

## Output

- Parquet files containing the collective variables (`theta`, `phi`, contact ratio, RMSD)
- CSV summaries of histogram data over time
- PDF files showing time-evolving histograms with overlays of equilibrium state distributions

## Notes

- This pipeline uses MDAnalysis for trajectory handling.
- Spherical angles (`theta`, `phi`) are calculated relative to a dynamically defined coordinate system based on microtubule subunits.
- Contact count ratio and RMSD are computed using `msm_utils` based native contact analysis.
- The plotting script compares dynamic CV distributions during transition to equilibrium distributions (e.g., free vs. AlF3 states) for validation.
