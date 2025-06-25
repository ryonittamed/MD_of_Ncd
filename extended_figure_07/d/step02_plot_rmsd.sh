#!/bin/bash -e

# Define input/output directories
OUT_DIR="/path/to/output_dir"
DATA_DIR="/path/to/input_dir"

# Create output directory
mkdir -p "${OUT_DIR}"

# Function to plot RMSD
plot_rmsd() {
  local CASE_PATH=$1
  local STATE=$2

  mkdir -p "${OUT_DIR}/${CASE_PATH}/${STATE}"

  uv run \
    --with polars \
    --with matplotlib \
    --with pandas \
    --with pyarrow \
    --with fastparquet \
    ./step02_plot_rmsd.py \
      --dir "${DATA_DIR}/${CASE_PATH}" \
      --out "${OUT_DIR}/${CASE_PATH}/${STATE}/out.pdf" \
      --state ${STATE}
}

###############################################
# Process all cases
###############################################

# kinesin
plot_rmsd "kinesin" "free"
plot_rmsd "kinesin" "alf3"

# kinesin-no-neckmimic
plot_rmsd "kinesin-no-neckmimic" "free"
plot_rmsd "kinesin-no-neckmimic" "alf3"

