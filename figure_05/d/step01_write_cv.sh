#!/bin/bash -e

# Process all the simulation runs
for i in {1..100}; do
  # Define simulation directory
  SIMU_DIR=$(printf "sim-%04d" "${i}")

  # Create output directory
  mkdir -p /path/to/output

  # Process trajectory if output does not exist
  if [ ! -e "/path/to/trajectory.parquet" ]; then
    uv run \
      --with numpy \
      --with polars \
      --with MDAnalysis \
        ./step01_write_cv.py \
          --sel-stalk1 "resid 7516-7568" \
          --sel-stalk2 "resid 7884-7936" \
          --sel-msu1 "resid 836-1252" \
          --sel-msu2 "resid 2506-2922" \
          --sel-msu3 "resid 4593-5010" \
          --dcd /path/to/dcd/file \
          --pdb /path/to/pdb/file \
          --out /path/to/trajectory.parquet
  fi
done
