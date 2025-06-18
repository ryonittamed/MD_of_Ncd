#!/bin/bash -e

OUT_DIR="step02_plot_cv.out"
DATA_DIR="step01_write_cv.out"

###############################################
# Case kinesin
###############################################
CASE_DIR="kinesin"

# Create output directory
mkdir -p "${OUT_DIR}/${CASE_DIR}"

# Plot cv files
uv run \
  --with polars \
  --with matplotlib \
  --with pandas \
  --with pyarrow \
  --with fastparquet \
  --with seaborn \
    ./step02_plot_cv.py \
      --dir "${DATA_DIR}/${CASE_DIR}" \
      --out "${OUT_DIR}/${CASE_DIR}/norm_out.pdf" \
      --raw-data "${OUT_DIR}/${CASE_DIR}/data.csv" \
      --non-norm-out "${OUT_DIR}/${CASE_DIR}/no_norm_out.pdf" \
      --dock-out "${OUT_DIR}/${CASE_DIR}/dock_out.pdf"



