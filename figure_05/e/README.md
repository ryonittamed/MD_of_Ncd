
# Collective Variable Analysis Pipeline for RMSD and Contact Ratio

This repository contains a set of scripts for calculating and visualizing collective variables (CVs), specifically theta, phi, RMSD, and contact ratio, from molecular dynamics (MD) simulations of kinesin systems with or without the neck mimic domain.

## Directory Structure

```
.
├── step01_write_cv.py           # Extract CVs (theta, phi, RMSD, contact ratio) from trajectories
├── step01_write_cv.sh           # Bash script to run CV extraction for multiple trajectories
├── step02_plot_cv.py            # Plot RMSD and contact ratio distributions over time
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
  - tqdm
  - msm_utils (for native contacts calculation)

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

## Step 2: Plot RMSD and Contact Ratio

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

## Color Configurations

The file `color_config.py` defines color codes used consistently in plotting:
- `with_neckmimic`: Blue (`#0072B2`)
- `without_neckmimic`: Olive (`#B3B300`)
- `contact_ratio`: Orange (`#ff4500`)

## Output

- Parquet files containing the collective variables (`theta`, `phi`, RMSD, contact ratio)
- CSV summary of trajectories
- PDF files showing time series plots with confidence intervals for RMSD and contact ratio

## Notes

- This pipeline uses MDAnalysis for trajectory handling.
- Spherical angles are calculated relative to a dynamic coordinate system defined by the microtubule subunits.
- Contact ratio and RMSD are computed using `msm_utils` based native contact analysis.
- Trajectories showing abnormal paths are filtered based on a heuristic applied to the `phi` angle.
