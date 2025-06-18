# Kinesin Contact Transition Analysis via Collective Variables

This repository provides a reproducible analysis pipeline for visualizing collective variable (CV) transitions — such as angular movement and residue contact — during kinesin simulations, with a focus on the neck-mimic binding process.

---

## Repository Structure

```
├── step01_write_cv.py      # Calculates angles (θ, φ) and contact-related CVs per trajectory
├── step01_write_cv.sh      # Batch process for writing CVs across all simulations
├── step02_plot_cv.py       # Summarizes and visualizes neckmimic-residue contact heatmaps
├── step02_plot_cv.sh       # Batch plotting script
├── config.py               # Contains neckmimic residue mapping and metadata
```

---

## Step 1: Calculate Collective Variables

### `step01_write_cv.py`

Processes trajectory files to compute:
- θ and φ angles of the stalk vector (projected onto MT coordinate axes)
- Native contact ratio and RMSD via `angle_vs_contacts`
- Contact frequency with neck-mimic residues

#### Key Arguments
- `--sel-stalk1/2`: Stalk residue selections (e.g., `resid 7516-7568`)
- `--sel-msu1/2/3`: MT coordinate system reference selections
- `--dcd`, `--pdb`, `--itp`: Trajectory, topology, and ITP file
- `--out`: Output `.csv` file

#### Output CSV
- `theta`, `phi`: Angles in radians
- `contact_count_ratio`, `rmsd`
- `contact_resids_in_neckmimic`: Contact dict {resid: count}
- `docks`: Contact presence flag {resid: bool}

---

### `step01_write_cv.sh`

Batch executes `step01_write_cv.py` for 100 simulations under the `kinesin` case.

- Reads input trajectories from:
  ```
  ../../4EA4-231F/experiment-05/kinesin/sim-xxxx/
  ```
- Outputs are stored in:
  ```
  step01_write_cv.out/kinesin/sim-xxxx/trajectory.csv
  ```

---

## Step 2: Plot Contact Residue Transitions

### `step02_plot_cv.py`

Summarizes and visualizes neckmimic-residue contacts over transition trajectories.

#### Key Functions

- Filters `phi`-based forward transitions ("path1")
- Extracts ±50 frame windows around the docking point
- Aggregates contact counts for neckmimic residues
- Generates normalized and raw heatmaps
- Outputs:
  - Heatmap (PDF)
  - Contact matrix (CSV)
  - Docking occurrence map

#### Required Arguments
- `--dir`: Input directory of CV CSV files
- `--out`: Path for normalized PDF output
- `--non-norm-out`: Unnormalized PDF output
- `--dock-out`: Binary docked-residue map
- `--raw-data`: Output matrix CSV
- `--target`: Optional, filter to one simulation

---

### `step02_plot_cv.sh`

Wrapper script to run `step02_plot_cv.py` on the full kinesin dataset.

Results are saved under:
```
step02_plot_cv.out/kinesin/
  ├── norm_out.pdf
  ├── no_norm_out.pdf
  ├── dock_out.pdf
  ├── data.csv
```

---

## config.py

Defines:
- `Neckmimic.neckmimic_range`: Residues 7884–7898
- `Neckmimic.resname_dict`: Mapping from residue index to label

Used for heatmap x-axis formatting and column renaming.

---

## Dependencies

Install via `uv` or `pip`:
- `numpy`, `pandas`, `polars`
- `matplotlib`, `seaborn`
- `MDAnalysis`, `pyarrow`, `fastparquet`
- `tqdm`

---

## Notes

- Only forward rotational transitions (positive φ, "path1") are analyzed
- Contact metrics depend on the docking point defined by contact ratio > 0.99
- Useful for studying neck-mimic residue interactions across multiple simulations

