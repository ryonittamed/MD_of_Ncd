#!/bin/bash -e

OUT_DIR="step02_plot_rmsd.out"
DATA_DIR="step01_calculate_rmsd.old.out"

# Create output directory
mkdir -p "${OUT_DIR}/"


##############################################################
# Experiment 05
#############################################################
EXP_TYPE="experiment-05"

CASE="kinesin"
mkdir -p "${OUT_DIR}/${EXP_TYPE}/${CASE}"

# Plot cv files
uv run \
  --with polars \
  --with matplotlib \
  --with pandas \
  --with pyarrow \
  --with fastparquet \
    ./step03_plot_rmsd_exp5.py \
      --dir "${DATA_DIR}/${EXP_TYPE}/${CASE}"\
      --out "${OUT_DIR}/${EXP_TYPE}/${CASE}/out.pdf" \
      --raw-data "${OUT_DIR}/${EXP_TYPE}/${CASE}/${STATE}/data.csv" 

CASE="kinesin-no-neckmimic"
mkdir -p "${OUT_DIR}/${EXP_TYPE}/${CASE}"

# Plot cv files
uv run \
  --with polars \
  --with matplotlib \
  --with pandas \
  --with pyarrow \
  --with fastparquet \
    ./step03_plot_rmsd_exp5.py \
      --dir "${DATA_DIR}/${EXP_TYPE}/${CASE}"\
      --out "${OUT_DIR}/${EXP_TYPE}/${CASE}/out.pdf" \
      --raw-data "${OUT_DIR}/${EXP_TYPE}/${CASE}/${STATE}/data.csv" 

