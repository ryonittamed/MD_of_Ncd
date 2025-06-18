#!/bin/bash -e

OUT_DIR="step01_calculate_rmsd.out"

############################################################
# Experiment 9
############################################################
DATA_DIR="../../4EA4-231F/experiment-09"
EXP_TYPE="experiment-09"

#------------------------------------------------------------
# Case 1
CASE_DIR="kinesin"
STATE="free"

# Process all the simulation runs
for i in {1..100}; do
  echo "Processing ${OUT_DIR}/${EXP_TYPE}/${CASE_DIR}/${SIMU_DIR}"
  # Define simulation directory
  SIMU_DIR=$(printf "sim-%04d" "${i}")

  # Skip if .dcd file does not exist
  if [ ! -f "${DATA_DIR}/${CASE_DIR}/${SIMU_DIR}/${STATE}.dcd" ]; then
    echo "Skipping: ${STATE}.dcd not found in ${DATA_DIR}/${CASE_DIR}/${SIMU_DIR}"
    continue
  fi

  # Create output directory
  mkdir -p "${OUT_DIR}/${EXP_TYPE}/${CASE_DIR}/${SIMU_DIR}"

  # Process trajectory if output does not exist
  if [ ! -e "${OUT_DIR}/${EXP_TYPE}/${CASE_DIR}/${SIMU_DIR}/${STATE}.csv" ]; then
    echo "Processing ${DATA_DIR}/${CASE_DIR}/${SIMU_DIR}"
    uv run \
      --with numpy \
      --with pandas \
      --with MDAnalysis \
        ./step01_calculate_rmsd.py \
          --target-region "resid 7516-8266" \
          --stalk1 "resid 7516-7568" \
          --stalk2 "resid 7899-7951" \
          --dcd "${DATA_DIR}/${CASE_DIR}/${SIMU_DIR}/${STATE}.dcd" \
          --pdb "${DATA_DIR}/${CASE_DIR}/pdb/${STATE}.pdb" \
          --out "${OUT_DIR}/${EXP_TYPE}/${CASE_DIR}/${SIMU_DIR}/${STATE}.csv"
  fi
done


#------------------------------------------------------------
# Case 2
CASE_DIR="kinesin-no-neckmimic"
STATE="free"

# Process all the simulation runs
for i in {1..100}; do
  echo "Processing ${OUT_DIR}/${EXP_TYPE}/${CASE_DIR}/${SIMU_DIR}"
  # Define simulation directory
  SIMU_DIR=$(printf "sim-%04d" "${i}")

  # Skip if .dcd file does not exist
  if [ ! -f "${DATA_DIR}/${CASE_DIR}/${SIMU_DIR}/${STATE}.dcd" ]; then
    echo "Skipping: ${STATE}.dcd not found in ${DATA_DIR}/${CASE_DIR}/${SIMU_DIR}"
    continue
  fi

  # Create output directory
  mkdir -p "${OUT_DIR}/${EXP_TYPE}/${CASE_DIR}/${SIMU_DIR}"

  # Process trajectory if output does not exist
  if [ ! -e "${OUT_DIR}/${EXP_TYPE}/${CASE_DIR}/${SIMU_DIR}/${STATE}.csv" ]; then
    echo "Processing ${DATA_DIR}/${CASE_DIR}/${SIMU_DIR}"
    uv run \
      --with numpy \
      --with pandas \
      --with MDAnalysis \
        ./step01_calculate_rmsd.py \
          --target-region "resid 7516-8266" \
          --stalk1 "resid 7516-7568" \
          --stalk2 "resid 7884-7936" \
          --dcd "${DATA_DIR}/${CASE_DIR}/${SIMU_DIR}/${STATE}.dcd" \
          --pdb "${DATA_DIR}/${CASE_DIR}/pdb/${STATE}.pdb" \
          --out "${OUT_DIR}/${EXP_TYPE}/${CASE_DIR}/${SIMU_DIR}/${STATE}.csv"
  fi
done

#------------------------------------------------------------
# Case 3
CASE_DIR="kinesin"
STATE="alf3"

# Process all the simulation runs
for i in {1..100}; do
  echo "Processing ${OUT_DIR}/${EXP_TYPE}/${CASE_DIR}/${SIMU_DIR}"
  # Define simulation directory
  SIMU_DIR=$(printf "sim-%04d" "${i}")

  # Skip if .dcd file does not exist
  if [ ! -f "${DATA_DIR}/${CASE_DIR}/${SIMU_DIR}/${STATE}.dcd" ]; then
    echo "Skipping: ${STATE}.dcd not found in ${DATA_DIR}/${CASE_DIR}/${SIMU_DIR}"
    continue
  fi

  # Create output directory
  mkdir -p "${OUT_DIR}/${EXP_TYPE}/${CASE_DIR}/${SIMU_DIR}"

  # Process trajectory if output does not exist
  if [ ! -e "${OUT_DIR}/${EXP_TYPE}/${CASE_DIR}/${SIMU_DIR}/${STATE}.csv" ]; then
    echo "Processing ${DATA_DIR}/${CASE_DIR}/${SIMU_DIR}"
    uv run \
      --with numpy \
      --with pandas \
      --with MDAnalysis \
        ./step01_calculate_rmsd.py \
          --target-region "resid 7516-8266" \
          --stalk1 "resid 7516-7568" \
          --stalk2 "resid 7899-7951" \
          --dcd "${DATA_DIR}/${CASE_DIR}/${SIMU_DIR}/${STATE}.dcd" \
          --pdb "${DATA_DIR}/${CASE_DIR}/pdb/${STATE}.pdb" \
          --out "${OUT_DIR}/${EXP_TYPE}/${CASE_DIR}/${SIMU_DIR}/${STATE}.csv"
  fi
done


#------------------------------------------------------------
# Case 4
CASE_DIR="kinesin-no-neckmimic"
STATE="alf3"

# Process all the simulation runs
for i in {1..100}; do
  echo "Processing ${OUT_DIR}/${EXP_TYPE}/${CASE_DIR}/${SIMU_DIR}"
  # Define simulation directory
  SIMU_DIR=$(printf "sim-%04d" "${i}")

  # Skip if .dcd file does not exist
  if [ ! -f "${DATA_DIR}/${CASE_DIR}/${SIMU_DIR}/${STATE}.dcd" ]; then
    echo "Skipping: ${STATE}.dcd not found in ${DATA_DIR}/${CASE_DIR}/${SIMU_DIR}"
    continue
  fi

  # Create output directory
  mkdir -p "${OUT_DIR}/${EXP_TYPE}/${CASE_DIR}/${SIMU_DIR}"

  # Process trajectory if output does not exist
  if [ ! -e "${OUT_DIR}/${EXP_TYPE}/${CASE_DIR}/${SIMU_DIR}/${STATE}.csv" ]; then
    echo "Processing ${DATA_DIR}/${CASE_DIR}/${SIMU_DIR}"
    uv run \
      --with numpy \
      --with pandas \
      --with MDAnalysis \
        ./step01_calculate_rmsd.py \
          --target-region "resid 7516-8266" \
          --stalk1 "resid 7516-7568" \
          --stalk2 "resid 7884-7936" \
          --dcd "${DATA_DIR}/${CASE_DIR}/${SIMU_DIR}/${STATE}.dcd" \
          --pdb "${DATA_DIR}/${CASE_DIR}/pdb/${STATE}.pdb" \
          --out "${OUT_DIR}/${EXP_TYPE}/${CASE_DIR}/${SIMU_DIR}/${STATE}.csv"
  fi
done
