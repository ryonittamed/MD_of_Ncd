#!/bin/bash -e

# Define input/output directories
OUT_DIR="/path/to/output_dir"
DATA_DIR="/path/to/input_dir"

# Function to process a case
process_case() {
  local CASE_PATH=$1
  local STALK2_RESID=$2

  for i in {1..100}; do
    SIMU_DIR=$(printf "sim-%04d" "${i}")
    INPUT_DCD="${DATA_DIR}/${CASE_PATH}/${SIMU_DIR}/trajectory.dcd"
    INPUT_PDB="${DATA_DIR}/${CASE_PATH}/pdb/free.pdb"
    INPUT_ITP="${DATA_DIR}/${CASE_PATH}/top/alf3.itp"
    OUTPUT_CSV="${OUT_DIR}/${CASE_PATH}/${SIMU_DIR}/trajectory.csv"

    echo "Processing ${INPUT_DCD}"

    if [ ! -f "${INPUT_DCD}" ]; then
      echo "Skipping: trajectory.dcd not found in ${INPUT_DCD}"
      continue
    fi

    mkdir -p "$(dirname "${OUTPUT_CSV}")"

    if [ ! -e "${OUTPUT_CSV}" ]; then
      uv run \
        --with numpy \
        --with polars \
        --with MDAnalysis \
        ./step01_write_cv.py \
          --sel-stalk1 "resid 7516-7568" \
          --sel-stalk2 "resid ${STALK2_RESID}" \
          --sel-msu1 "resid 836-1252" \
          --sel-msu2 "resid 2506-2922" \
          --sel-msu3 "resid 4593-5010" \
          --dcd "${INPUT_DCD}" \
          --pdb "${INPUT_PDB}" \
          --itp "${INPUT_ITP}" \
          --out "${OUTPUT_CSV}"
    fi
  done
}

############################################################
# Process cases
############################################################

# Example case: kinesin
process_case "kinesin" "7899-7951"

# Example case: kinesin-no-neckmimic (if needed)
# process_case "kinesin-no-neckmimic" "7884-7936"

