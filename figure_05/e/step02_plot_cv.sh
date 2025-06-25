#!/bin/bash -e

# Create output directory
mkdir -p /path/to/out_dir

# Plot cv files
uv run \
  --with polars \
  --with matplotlib \
  --with pandas \
  --with pyarrow \
  --with fastparquet \
  --with seaborn \
    ./step02_plot_cv.py \
      --dir /path/to/data_dir \
      --out /path/to/out_dir



