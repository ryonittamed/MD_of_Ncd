import pandas as pd
import MDAnalysis as mda
import MDAnalysis.analysis.rms
import numpy as np
import argparse

def calculate_rmsd(dcd, pdb, target_region, skip_steps=1):
  """
  dcd, itp, pdbから
    * rmsd: pdbで与えられたpdbファイルを基準としてrmsdを計算する
    を返す
  skip_stepsで指定されたステップ数だけスキップして処理する
  """
  # Initialize universe
  universe = mda.Universe(str(pdb), str(dcd))

  # Initialize calculater instance of RMSD
  ref = mda.Universe(str(pdb))
  R = MDAnalysis.analysis.rms.RMSD(
    universe,
    ref,
    select="backbone",
    groupselections=[target_region]
  )
  ## calculate rmsd
  R.run(verbose=True)
  rmsd = R.rmsd[:, 3]
  rmsd = rmsd[::skip_steps]
  
  return rmsd

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-region", type=str, required=True, help="Selection string for the kinesin dimer")
    parser.add_argument("--pdb", type=str, required=True, help="PDB file for topology")
    parser.add_argument("--dcd", type=str, required=True, help="DCD file for trajectory")
    parser.add_argument("--out", type=str, required=True, help="Output file name")
    args = parser.parse_args()

    #Caluculate rmsd
    rmsd = calculate_rmsd(args.dcd, args.pdb, args.target_region)

    #Sae dataframe
    df = pd.DataFrame({"rmsd": rmsd})
    df.to_csv(args.out)

if __name__=="__main__":
  main()
