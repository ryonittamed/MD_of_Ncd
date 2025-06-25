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
    # setup colors
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
    scale_factor = means2[-1] / means1[-1]

    # プロットの作成
    fig, ax1 = plt.subplots(figsize=(15, 10.5))

    # 右軸（Data 1）
    ax2 = ax1.twinx()  # 右軸を追加

    # Data 1 のプロット（右軸）
    ax2.plot(time_steps / 10**2, medians1, linestyle='-', color=colors.contact_ratio, label="")
    ax2.fill_between(time_steps / 10**2, std_devs1_lower, std_devs1_upper, color=colors.contact_ratio, alpha=0.2)

    # Data 2 のプロット（左軸）
    ax1.plot(time_steps / 10**2, medians2, linestyle='-', color=colors.with_neckmimic, label="")
    ax1.fill_between(time_steps / 10**2, std_devs2_lower, std_devs2_upper, color=colors.with_neckmimic, alpha=0.2)

    # 軸のスケール調整
    scale_min = 0.5 / means2[0]
    scale_max = 3.0 / means2[-1]
    ax1.set_ylim(means2[0] * scale_min , means2[-1] * scale_max)  # 左軸は Data 2
    ax2.set_ylim(means1[0] * scale_min , means1[-1] * scale_max)  # 右軸は Data 1（スケール調整済み）

    # 軸ラベル
    ax1.tick_params(axis='both', labelsize=30)
    ax2.tick_params(axis='both', labelsize=30)

    # グリッド設定
    ax1.grid(True, linestyle="--", linewidth=0.5, alpha=0.7)

    # 凡例の設定
    ax1.spines["top"].set_visible(False)
    ax2.spines["top"].set_visible(False)

    # 保存ディレクトリの作成（存在しない場合）
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)  # 親ディレクトリを作成

    # 画像の保存
    plt.savefig(output_path, dpi=300, facecolor='white', format="pdf")

    # プロットを閉じる（メモリ節約のため）
    plt.close()

    print(f"Plot saved to {output_path}")

def save_summary_stats_dual_axis(data1, data2, output_csv_path, data1_name="Data1", data2_name="Data2"):
    """
    2つのデータセットの各時間ステップごとの平均・中央値・標準偏差を計算し、CSVに保存する。

    Parameters:
        data1 (list of list): 1つ目のデータセット
        data2 (list of list): 2つ目のデータセット
        output_csv_path (str or Path): CSVファイルの保存パス
        data1_name (str): data1 の列名に使用するラベル（デフォルト: "Data1"）
        data2_name (str): data2 の列名に使用するラベル（デフォルト: "Data2"）
    """
    # NumPy 配列に変換
    data1 = np.array(data1)
    data2 = np.array(data2)
    
    # 時間軸
    time_steps = np.arange(data1.shape[1])

    # データ1の統計量
    mean1 = np.mean(data1, axis=0)
    median1 = np.median(data1, axis=0)
    std1 = np.std(data1, axis=0)

    # データ2の統計量
    mean2 = np.mean(data2, axis=0)
    median2 = np.median(data2, axis=0)
    std2 = np.std(data2, axis=0)

    # データフレームにまとめる
    df = pd.DataFrame({
        'TimeStep': time_steps,
        f'Mean_{data1_name}': mean1,
        f'Median_{data1_name}': median1,
        f'Std_{data1_name}': std1,
        f'Mean_{data2_name}': mean2,
        f'Median_{data2_name}': median2,
        f'Std_{data2_name}': std2
    })

    # CSVとして保存
    df.to_csv(output_csv_path, index=False, encoding='utf-8-sig')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", type=str, required=True, help="Directory containing CVs in parquet format")
    parser.add_argument("--out", type=str, required=True, help="Output file name")
    parser.add_argument("--raw-data", type=str, required=True, help="Raw Data file name")
    parser.add_argument("--target", type=int, required=False, help="Target simulation number")
    args = parser.parse_args()

    # List all the parquet files
    paths = [str(file) for file in pathlib.Path(args.dir).rglob("*.parquet")]
    paths = sorted(paths)

    # Specify target path is args.target is defined
    paths = paths if args.target is None else paths[args.target-1:args.target]

    # Load dataframes
    df_list = []
    indexs = []
    contact_count_ratios = []
    phis = []
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
        if pth == 'path1':
          contact_count_ratios.append(df['contact_count_ratio'].to_list()[:1200]) #最初の2500stepに制限
          phis.append(df['phi'].to_list()[:1200])



    plot_mean_with_std_dual_axis(contact_count_ratios, phis, args.out)

if __name__ == "__main__":
    main()
