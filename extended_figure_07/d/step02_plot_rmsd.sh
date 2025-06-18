#!/bin/bash -e

OUT_DIR="step02_plot_rmsd.out"
DATA_DIR="step01_calculate_rmsd.old.out"

# Create output directory
mkdir -p "${OUT_DIR}/"


##############################################################
# Experiment 09
#############################################################
EXP_TYPE="experiment-09"

CASE="kinesin"
STATE="free"
mkdir -p "${OUT_DIR}/${EXP_TYPE}/${CASE}/${STATE}"

# Plot cv files
uv run \
  --with polars \
  --with matplotlib \
  --with pandas \
  --with pyarrow \
  --with fastparquet \
    ./step02_plot_rmsd.py \
      --dir "${DATA_DIR}/${EXP_TYPE}/${CASE}"\
      --out "${OUT_DIR}/${EXP_TYPE}/${CASE}/${STATE}/out.pdf" \
      --raw-data "${OUT_DIR}/${EXP_TYPE}/${CASE}/${STATE}/data.csv" \
      --state ${STATE}

CASE="kinesin-no-neckmimic"
STATE="free"
mkdir -p "${OUT_DIR}/${EXP_TYPE}/${CASE}/${STATE}"

# Plot cv files
uv run \
  --with polars \
  --with matplotlib \
  --with pandas \
  --with pyarrow \
  --with fastparquet \
    ./step02_plot_rmsd.py \
      --dir "${DATA_DIR}/${EXP_TYPE}/${CASE}"\
      --out "${OUT_DIR}/${EXP_TYPE}/${CASE}/${STATE}/out.pdf" \
      --raw-data "${OUT_DIR}/${EXP_TYPE}/${CASE}/${STATE}/data.csv" \
      --state ${STATE}

CASE="kinesin"
STATE="alf3"
mkdir -p "${OUT_DIR}/${EXP_TYPE}/${CASE}/${STATE}"

# Plot cv files
uv run \
  --with polars \
  --with matplotlib \
  --with pandas \
  --with pyarrow \
  --with fastparquet \
    ./step02_plot_rmsd.py \
      --dir "${DATA_DIR}/${EXP_TYPE}/${CASE}"\
      --out "${OUT_DIR}/${EXP_TYPE}/${CASE}/${STATE}/out.pdf" \
      --raw-data "${OUT_DIR}/${EXP_TYPE}/${CASE}/${STATE}/data.csv" \
      --state ${STATE}

CASE="kinesin-no-neckmimic"
STATE="alf3"
mkdir -p "${OUT_DIR}/${EXP_TYPE}/${CASE}/${STATE}"

# Plot cv files
uv run \
  --with polars \
  --with matplotlib \
  --with pandas \
  --with pyarrow \
  --with fastparquet \
    ./step02_plot_rmsd.py \
      --dir "${DATA_DIR}/${EXP_TYPE}/${CASE}"\
      --out "${OUT_DIR}/${EXP_TYPE}/${CASE}/${STATE}/out.pdf" \
      --raw-data "${OUT_DIR}/${EXP_TYPE}/${CASE}/${STATE}/data.csv" \
      --state ${STATE}
