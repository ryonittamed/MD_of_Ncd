#!/bin/bash -e

OUT_DIR="step02_plot_rmsd.out"
DATA_DIR="step01_calculate_rmsd.out"

# Create output directory
mkdir -p "${OUT_DIR}/"


##############################################################
# Experiment 09
#############################################################
EXP_TYPE="experiment-09"

STATE="free"
mkdir -p "${OUT_DIR}/${EXP_TYPE}/${STATE}"

# Plot cv files
uv run \
  --with polars \
  --with matplotlib \
  --with pandas \
  --with pyarrow \
  --with fastparquet \
    ./step02_plot_rmsd.py \
      --dir-kinesin "${DATA_DIR}/${EXP_TYPE}/kinesin"\
      --dir-no-kinesin "${DATA_DIR}/${EXP_TYPE}/kinesin-no-neckmimic"\
      --out "${OUT_DIR}/${EXP_TYPE}/${STATE}/out.pdf" \
      --raw-data "${OUT_DIR}/${EXP_TYPE}/${STATE}/data.csv" \
      --state ${STATE}

STATE="alf3"
mkdir -p "${OUT_DIR}/${EXP_TYPE}/${STATE}"

# Plot cv files
uv run \
  --with polars \
  --with matplotlib \
  --with pandas \
  --with pyarrow \
  --with fastparquet \
    ./step02_plot_rmsd.py \
      --dir-kinesin "${DATA_DIR}/${EXP_TYPE}/kinesin"\
      --dir-no-kinesin "${DATA_DIR}/${EXP_TYPE}/kinesin-no-neckmimic"\
      --out "${OUT_DIR}/${EXP_TYPE}/${STATE}/out.pdf" \
      --raw-data "${OUT_DIR}/${EXP_TYPE}/${STATE}/data.csv" \
      --state ${STATE}

