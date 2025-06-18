#!/bin/bash -e

OUT_DIR="step02_plot_distributions.out"
DATA_DIR="step01_write_cv.out"

###############################################
# Case kinesin
###############################################
CASE_DIR="kinesin"

# Create output directory
mkdir -p "${OUT_DIR}"

# Plot cv files
uv run \
  --with polars \
  --with matplotlib \
  --with pandas \
  --with pyarrow \
  --with fastparquet \
  --with seaborn \
    ./step02_plot_distributions.py \
      --dir "${DATA_DIR}/kinesin.equiliblium"  "${DATA_DIR}/kinesin-no-neckmimic.equiliblium"\
      --out "${OUT_DIR}" \
      --state "free"

# Plot cv files
uv run \
  --with polars \
  --with matplotlib \
  --with pandas \
  --with pyarrow \
  --with fastparquet \
  --with seaborn \
    ./step02_plot_distributions.py \
      --dir "${DATA_DIR}/kinesin.equiliblium"  "${DATA_DIR}/kinesin-no-neckmimic.equiliblium"\
      --out "${OUT_DIR}" \
      --state "alf3"

