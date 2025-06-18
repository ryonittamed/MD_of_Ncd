#!/bin/bash -e

OUT_DIR="step02_plot_cv.out"
DATA_DIR="step01_write_cv.out"

###############################################
# Case kinesin
###############################################
KINESIN_DIR="kinesin"
NO_KINESIN_DIR="kinesin-no-neckmimic"

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
      --kinesin "${DATA_DIR}/${KINESIN_DIR}" \
      --no-kinesin "${DATA_DIR}/${NO_KINESIN_DIR}" \
      --raw-data "${OUT_DIR}/data.csv" \
      --out "${OUT_DIR}/out.pdf"



