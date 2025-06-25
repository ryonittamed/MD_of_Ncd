#!/bin/bash -e

# Output directory
OUT_DIR="/path/to/output_dir"

# Data directory
DATA_DIR="/path/to/data_dir"

# Function to process each case
process_case() {
  local CASE_PATH=$1
  local STATE=$2
  local STALK2_RESID=$3

  for i in {1..100}; do
    SIMU_DIR=$(printf "sim-%04d" "${i}")
    INPUT_DCD="${DATA_DIR}/${CASE_PATH}/${SIMU_DIR}/${STATE}.dcd"
    INPUT_PDB="${DATA_DIR}/${CASE_PATH}/pdb/${STATE}.pdb"
    OUTPUT_CSV="${OUT_DIR}/${CASE_PATH}/${SIMU_DIR}/${STATE}.csv"

    echo "Processing ${OUTPUT_CSV}"

    if [ ! -f "${INPUT_DCD}" ]; then
      echo "Skipping: ${STATE}.dcd not found in ${INPUT_DCD}"
      continue
    fi

    mkdir -p "$(dirname "${OUTPUT_CSV}")"

    if [ ! -e "${OUTPUT_CSV}" ]; then
      uv run \
        --with numpy \
        --with pandas \
        --with MDAnalysis \
        ./step01_calculate_rmsd.py \
          --target-region "resid 7516-8266" \
          --stalk1 "resid 7516-7568" \
          --stalk2 "resid ${STALK2_RESID}" \
          --dcd "${INPUT_DCD}" \
          --pdb "${INPUT_PDB}" \
          --out "${OUTPUT_CSV}"
    fi
  done
}

############################################################
# Processing all cases
############################################################

# Case 1: kinesin, free
process_case "kinesin" "free" "7899-7951"

# Case 2: kinesin-no-neckmimic, free
process_case "kinesin-no-neckmimic" "free" "7884-7936"

# Case 3: kinesin, alf3
process_case "kinesin" "alf3" "7899-7951"

# Case 4: kinesin-no-neckmimic, alf3
process_case "kinesin-no-neckmimic" "alf3" "7884-7936"

