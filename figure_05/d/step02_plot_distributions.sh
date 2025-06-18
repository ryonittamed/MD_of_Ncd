#!/bin/bash -e

# Create output directory
mkdir -p /path/to/output/dir

# Plot cv files
uv run \
  --with polars \
  --with matplotlib \
  --with pandas \
  --with pyarrow \
  --with fastparquet \
  --with seaborn \
    ./step02_plot_distributions.py \
      --dir /path/to/kinesin.equiliblium  /path/to/kinesin-no-neckmimic.equiliblium\
      --out /path/to/output/dir \
      --state "free"

uv run \
  --with polars \
  --with matplotlib \
  --with pandas \
  --with pyarrow \
  --with fastparquet \
  --with seaborn \
    ./step02_plot_distributions.py \
      --dir /path/to/kinesin.equiliblium  /path/to/kinesin-no-neckmimic.equiliblium\
      --out /path/to/output/dir \
      --state "alf3"

