#!/bin/bash -e

# Define input/output directories
OUT_DIR="/path/to/output_dir"
DATA_DIR="/path/to/input_dir"

# Create output directory
mkdir -p "${OUT_DIR}"

# Function to process each state
plot_state() {
  local STATE=$1

  mkdir -p "${OUT_DIR}/${STATE}"

  uv run \
    --with polars \
    --with matplotlib \
    --with pandas \
    --with pyarrow \
    --with fastparquet \
    ./step02_plot_rmsd.py \
      --dir-kinesin "${DATA_DIR}/kinesin" \
      --dir-no-kinesin "${DATA_DIR}/kinesin-no-neckmimic" \
      --out "${OUT_DIR}/${STATE}/out.pdf" \
      --state ${STATE}
}

# Process for states 'free' and 'alf3'
plot_state "free"
plot_state "alf3"
