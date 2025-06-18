#!/bin/bash -e

OUT_DIR="step01_write_cv.out"

############################################################
# Experiment 5
############################################################
#DATA_DIR="../experiment-05"
#DATA_DIR="../../tmp_trj0/trajectories"
DATA_DIR="../../4EA4-231F/experiment-05"

#------------------------------------------------------------
# Case 1
CASE_DIR="kinesin"

# Process all the simulation runs
for i in {1..100}; do
  # Define simulation directory
  SIMU_DIR=$(printf "sim-%04d" "${i}")

  # Create output directory
  mkdir -p "${OUT_DIR}/${CASE_DIR}/${SIMU_DIR}"

  # Process trajectory if output does not exist
  if [ ! -e "${OUT_DIR}/${CASE_DIR}/${SIMU_DIR}/trajectory.csv" ]; then
    echo "Processing ${DATA_DIR}/${CASE_DIR}/${SIMU_DIR}"
    uv run \
      --with numpy \
      --with polars \
      --with MDAnalysis \
        ./step01_write_cv.py \
          --sel-stalk1 "resid 7516-7568" \
          --sel-stalk2 "resid 7899-7951" \
          --sel-msu1 "resid 836-1252" \
          --sel-msu2 "resid 2506-2922" \
          --sel-msu3 "resid 4593-5010" \
          --dcd "${DATA_DIR}/${CASE_DIR}/${SIMU_DIR}/trajectory.dcd" \
          --pdb "${DATA_DIR}/${CASE_DIR}/pdb/free.pdb" \
          --itp "${DATA_DIR}/${CASE_DIR}/top/alf3.itp" \
          --out "${OUT_DIR}/${CASE_DIR}/${SIMU_DIR}/trajectory.csv"
  fi
done
exit

