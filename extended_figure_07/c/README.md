
# Contact Map and CV Analysis Pipeline for Kinesin Simulations

This repository contains a set of scripts for calculating and visualizing collective variables (CVs), including theta, phi, RMSD, contact ratio, and residue-specific contact maps for kinesin systems with and without the neck mimic domain.

## Directory Structure

```
.
├── step01_write_cv.py           # Extract CVs (theta, phi, RMSD, contact ratio, contact map) from trajectories
├── step01_write_cv.sh           # Bash script to run CV extraction for multiple simulations
├── step02_plot_cv.py            # Plot residue-specific contact heatmaps
├── step02_plot_cv.sh            # Bash script to automate plotting
├── config.py                    # Configuration for residue mappings
├── output/                      # Output files (csv, parquet, pdf)
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
  --out /path/to/output/trajectory.csv
```

Or execute in batch:

```bash
bash step01_write_cv.sh
```

**Note:** Please modify the file paths in the bash scripts according to your environment.

## Step 2: Plot Contact Heatmap

**Script:** `step02_plot_cv.py`  
**Example usage:**

```bash
python step02_plot_cv.py \
  --dir /path/to/data_dir \
  --out /path/to/output/heatmap.pdf
```

Or execute in batch:

```bash
bash step02_plot_cv.sh
```

**Note:** Please modify the file paths in the bash scripts according to your environment.

## Output

- CSV or parquet files containing the CVs: theta, phi, RMSD, contact ratio, and detailed contact residues
- PDF heatmaps showing the time evolution of contact frequencies between the neck mimic and target residues

## Configuration

The file `config.py` contains definitions for:
- Residue ID ranges (`neckmimic_range`)
- Mappings from residue IDs to formatted labels (`resname_dict`)

## Notes

- This pipeline uses MDAnalysis for trajectory handling.
- Spherical angles (`theta`, `phi`) are calculated relative to a dynamically defined coordinate system based on microtubule subunits.
- Contact count ratio and RMSD are computed using `msm_utils` based native contact analysis.
- The heatmap highlights contact formation dynamics during the transition of the neck mimic binding.
