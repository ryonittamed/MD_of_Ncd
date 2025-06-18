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


def calculate_rmsd_list(dcd, pdb, target_regions, skip_steps=1):
  """
  dcd, itp, pdbから
    * rmsd: pdbで与えられたpdbファイルを基準としてrmsdを計算する
    を返す
  skip_stepsで指定されたステップ数だけスキップして処理する
  target_regionsにリストをとる場合
  """
  # Initialize universe
  universe = mda.Universe(str(pdb), str(dcd))

  selected_regions = ' or '.join(target_regions)
  print(selected_regions)

  # Initialize calculater instance of RMSD
  ref = mda.Universe(str(pdb))
  R = MDAnalysis.analysis.rms.RMSD(
    universe,
    ref,
    select="backbone",
    groupselections=[selected_regions],
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
    parser.add_argument("--stalk1", type=str, required=True, help="Selection string for the stalk 1")
    parser.add_argument("--stalk2", type=str, required=True, help="Selection string for the stalk 2")
    args = parser.parse_args()

    #Caluculate rmsd of neck mimic
    ncd_rmsd = calculate_rmsd(args.dcd, args.pdb, args.target_region)

    #Caluculate rmsd of stalk
    stalk_rmsd = calculate_rmsd_list(args.dcd, args.pdb, [args.stalk1, args.stalk2])

    #Save dataframe
    df = pd.DataFrame({"ncd_rmsd": ncd_rmsd, "stalk_rmsd": stalk_rmsd})
    print(df)
    df.to_csv(args.out)

if __name__=="__main__":
  main()
