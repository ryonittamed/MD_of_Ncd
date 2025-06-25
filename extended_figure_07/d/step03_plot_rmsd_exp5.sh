#!/bin/bash -e

# Define input/output directories
OUT_DIR="/path/to/output_dir"
DATA_DIR="/path/to/input_dir"

# Create output directory
mkdir -p "${OUT_DIR}"

# Function to plot RMSD for experiment 05
plot_rmsd_exp5() {
  local CASE_PATH=$1

  mkdir -p "${OUT_DIR}/${CASE_PATH}"

  uv run \
    --with polars \
    --with matplotlib \
    --with pandas \
    --with pyarrow \
    --with fastparquet \
    ./step03_plot_rmsd_exp5.py \
      --dir "${DATA_DIR}/${CASE_PATH}" \
      --out "${OUT_DIR}/${CASE_PATH}/out.pdf" \
}

###############################################
# Process all cases
###############################################

# kinesin
plot_rmsd_exp5 "kinesin"

# kinesin-no-neckmimic
plot_rmsd_exp5 "kinesin-no-neckmimic"

