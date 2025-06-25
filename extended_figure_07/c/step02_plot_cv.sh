#!/bin/bash -e

# Define input/output directories
OUT_DIR="/path/to/output_dir"
DATA_DIR="/path/to/input_dir"

# Function to plot CV
plot_cv() {
  local CASE_PATH=$1

  mkdir -p "${OUT_DIR}/${CASE_PATH}"

  uv run \
    --with polars \
    --with matplotlib \
    --with pandas \
    --with pyarrow \
    --with fastparquet \
    --with seaborn \
    ./step02_plot_cv.py \
      --dir "${DATA_DIR}/${CASE_PATH}" \
      --out "${OUT_DIR}/${CASE_PATH}/norm_out.pdf"
}

###############################################
# Process case
###############################################

# Example case: kinesin
plot_cv "kinesin"

# Example case: kinesin-no-neckmimic (if needed)
# plot_cv "kinesin-no-neckmimic"

