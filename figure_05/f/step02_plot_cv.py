#!/usr/bin/env python

import argparse
import pathlib
import warnings
import seaborn as sns

warnings.filterwarnings("ignore")
warnings.warn = lambda *args, **kwargs: None

import polars as pl
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import pickle
from pathlib import Path

from color_config import Color

def unwrap_angles(df):
    """
    データフレーム内の 'theta' 列と 'phi' 列に np.unwrap を適用し、
    修正後のデータフレームを返す関数。

    Parameters:
        df (pd.DataFrame): thetaとphi列を含むデータフレーム。

    Returns:
        pd.DataFrame: np.unwrap処理後のデータフレーム。
    """
    # データフレームのコピーを作成
    df_unwrapped = df.copy()

    # np.unwrap処理をtheta列とphi列に適用
    df_unwrapped['theta'] = np.unwrap(df_unwrapped['theta'].values, period=2 * np.pi)
    df_unwrapped['phi'] = np.unwrap(df_unwrapped['phi'].values, period=2 * np.pi)

    return df_unwrapped

def extract_transition(df):
  if df['phi'].min() < 0: #1度でもpath2の方向に進んだらはじく
    return None, "path2"

  last_phi = df['phi'].iloc[-1]
  if last_phi > 0:
    # 条件を満たす最初の行のインデックスを取得
    idx = (df['phi'] > 2).idxmax()
  
    # その行までのデータを取得
    df_subset = df.copy()
    return df_subset, 'path1'
  elif last_phi < -1:
    # 条件を満たす最初の行のインデックスを取得
    idx = (df['phi'] < -4).idxmax()
  
    # その行までのデータを取得
    df_subset = df.copy()
    return df_subset, 'path2'
  else:
    raise RuntimeError
    

def extract_transition2(df):
  last_phi = df['phi'].iloc[-1]
  if last_phi > 0:
    # 条件を満たす最初の行のインデックスを取得
    idx = (df['contact_count_ratio'] > 0.99).idxmax()
  
    # その行までのデータを取得
    df_subset = df.loc[:idx]
    return df_subset, 'path1'
  elif last_phi < -1:
    # 条件を満たす最初の行のインデックスを取得
    idx = (df['contact_count_ratio'] > 0.99).idxmax()
  
    # その行までのデータを取得
    df_subset = df.loc[:idx]
    return df_subset, 'path2'
  else:
    raise RuntimeError

def plot_mean_with_std_dual_axis(data1, data2, output_path):
    """
    2つのデータセットの時間ごとの平均と標準偏差をプロットし、左右のY軸を用いて比較し、画像として保存する。

    Parameters:
        data1 (list of list): 1つ目のデータセット（右軸に表示）
        data2 (list of list): 2つ目のデータセット（左軸に表示）
        output_path (str or Path): 画像の保存パス（ディレクトリ + ファイル名を含む）
    """
    #setup colors
    colors = Color()

    # NumPy 配列に変換
    data1 = np.array(data1)
    data2 = np.array(data2)

    # 各時間ステップごとの平均と標準偏差を計算
    time_steps = np.arange(data1.shape[1])  # 時間軸 (0, 1, 2, ...)

    percent = 10

    means1 = np.mean(data1, axis=0)
    medians1 = np.median(data1, axis=0)
    std_devs1_lower = np.percentile(data1, percent, axis=0)
    std_devs1_upper = np.percentile(data1, 100-percent, axis=0)

    means2 = np.mean(data2, axis=0)
    medians2 = np.median(data2, axis=0)
    std_devs2_lower = np.percentile(data2, percent, axis=0)
    std_devs2_upper = np.percentile(data2, 100-percent, axis=0)

    # 軸のスケール調整（原点から開始し、最後の値を合わせる）
    #scale_factor = means2[-1] / means1[-1]

    # プロットの作成
    fig, ax1 = plt.subplots(figsize=(15, 10.5))

    # 右軸（Data 1）
    #ax2 = ax1.twinx()  # 右軸を追加

    # Data 1 のプロット（右軸）
    #ax1.plot(time_steps / 10**2, means1, linestyle='-', color=colors.with_neckmimic, label="with neck-mimic", linewidth=2.0)
    ax1.plot(time_steps / 10**2, means1, linestyle='-', color=colors.with_neckmimic, label="", linewidth=2.0)
    ax1.fill_between(time_steps / 10**2, std_devs1_lower, std_devs1_upper, color=colors.with_neckmimic, alpha=0.2)

    # Data 2 のプロット（左軸）
    #ax1.plot(time_steps / 10**2, means2, linestyle='-', color=colors.without_neckmimic, label="without neck-mimic", linewidth=2.0)
    ax1.plot(time_steps / 10**2, means2, linestyle='-', color=colors.without_neckmimic, label="", linewidth=2.0)
    ax1.fill_between(time_steps / 10**2, std_devs2_lower, std_devs2_upper, color=colors.without_neckmimic, alpha=0.2)

    # 軸のスケール調整
    #ax1.set_ylim(means2[0] * 0.9 , means2[-1] * 1.2)  # 左軸は Data 2
    #ax2.set_ylim(means1[0] * 0.9 , means1[-1] * 1.2)  # 右軸は Data 1（スケール調整済み）
    ax1.set_ylim(0.5, 3.0)

    # 軸ラベル
    #ax1.set_xlabel(r"MD steps ($\times 10^4$)", fontsize=40, fontname="Arial")
    #ax1.set_ylabel(r"$\phi$ ($rad$)", fontsize=40, fontname="Arial")
    ax1.tick_params(axis='both', labelsize=30)

    # グリッド設定
    ax1.grid(True, linestyle="--", linewidth=0.5, alpha=0.7)

    # 凡例の設定
    #ax1.legend(fontsize=30)
    #ax2.legend(loc="upper right", fontsize=12)
    ax1.spines["top"].set_visible(False)
    
    # 軸の目盛りの数値だけ非表示にする（目盛り線や軸線は残す）
    ax1.set_xticklabels([])
    ax1.set_yticklabels([])

    # 保存ディレクトリの作成（存在しない場合）
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)  # 親ディレクトリを作成

    # 画像の保存
    plt.savefig(output_path, dpi=300, facecolor='white', format='pdf')

    # プロットを閉じる（メモリ節約のため）
    plt.close()

    print(f"Plot saved to {output_path}")

def save_mean_median_percentile_dual_axis(
    data1, data2, output_csv_path, data1_name="Data1", data2_name="Data2", percent=10
):
    """
    2つのデータセットの時間ごとの統計量（平均、中央値、パーセンタイル）を計算し、CSVに保存する。

    Parameters:
        data1 (list of list): 1つ目のデータセット
        data2 (list of list): 2つ目のデータセット
        output_csv_path (str or Path): 出力CSVの保存先パス
        data1_name (str): data1 に対応する名前（列名に使用）
        data2_name (str): data2 に対応する名前（列名に使用）
        percent (int): 下位・上位パーセンタイルの指定（例：10 → 10th〜90th）
    """
    # 配列に変換
    data1 = np.array(data1)
    data2 = np.array(data2)
    time_steps = np.arange(data1.shape[1])

    # data1 統計量
    mean1 = np.mean(data1, axis=0)
    median1 = np.median(data1, axis=0)
    lower1 = np.percentile(data1, percent, axis=0)
    upper1 = np.percentile(data1, 100 - percent, axis=0)

    # data2 統計量
    mean2 = np.mean(data2, axis=0)
    median2 = np.median(data2, axis=0)
    lower2 = np.percentile(data2, percent, axis=0)
    upper2 = np.percentile(data2, 100 - percent, axis=0)

    # DataFrame にまとめる
    df = pd.DataFrame({
        "TimeStep": time_steps,
        f"Mean_{data1_name}": mean1,
        f"Median_{data1_name}": median1,
        f"Lower_{percent}th_{data1_name}": lower1,
        f"Upper_{100 - percent}th_{data1_name}": upper1,
        f"Mean_{data2_name}": mean2,
        f"Median_{data2_name}": median2,
        f"Lower_{percent}th_{data2_name}": lower2,
        f"Upper_{100 - percent}th_{data2_name}": upper2,
    })

    # 保存
    df.to_csv(output_csv_path, index=False, encoding="utf-8-sig")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--kinesin", type=str, required=True, help="Directory containing CVs in parquet format for kinesin")
    parser.add_argument("--no-kinesin", type=str, required=True, help="Directory containing CVs in parquet format for no-neckmimic-kinesin")
    parser.add_argument("--out", type=str, required=True, help="Output file name")
    parser.add_argument("--raw-data", type=str, required=True, help="Raw Data file name")
    args = parser.parse_args()

    # List all the parquet files
    paths_neckmimic = [str(file) for file in pathlib.Path(args.kinesin).rglob("*.parquet")]
    paths_neckmimic = sorted(paths_neckmimic)
    paths_no_neckmimic = [str(file) for file in pathlib.Path(args.no_kinesin).rglob("*.parquet")]
    paths_no_neckmimic = sorted(paths_no_neckmimic)

    # Load dataframes
    sims = []
    for paths in [paths_neckmimic, paths_no_neckmimic]:
      phis = []
      count = 0
      for path in paths:
          df = pd.read_parquet(path)

          # Split trajectory
          sim1 = df.iloc[:2000]
          sim2 = df.iloc[2000:2300]
          sim3 = df.iloc[2300:22300]
          sim4 = df.iloc[22300:22600]
          sim5 = df.iloc[22600:42600]


          # Unwrap angles
          df = unwrap_angles(sim3)

          # Extract only transition part
          df, pth = extract_transition(df)
          print(f"{df=}")
          if pth == 'path1':
            phis.append(df['phi'].to_list()[:1200])
            count += 1
      print(f"Number of valid simulations in {paths}:", count)
      sims.append(phis)

    print(f"{len(sims[0])=}")
    print(f"{len(sims[1])=}")

    plot_mean_with_std_dual_axis(sims[0], sims[1], args.out)
    #save_mean_median_percentile_dual_axis(sims[0], sims[1], args.raw_data, data1_name="neckmimic", data2_name="no-neckmimic", percent=10)

if __name__ == "__main__":
    main()
