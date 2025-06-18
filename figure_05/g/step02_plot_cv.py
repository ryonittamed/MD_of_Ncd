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

import numpy as np
import matplotlib.pyplot as plt

import numpy as np
import matplotlib.pyplot as plt

def plot_data_distribution_histogram_with_overlay(x, y, z, save_path, bins=10, previous_steps=20):
    """
    x: shape (41, 79) の NumPy 配列 (時系列データ)
    y, z: shape (2000,) の NumPy 配列（比較用のデータ）
    save_path: プロット画像の保存先
    bins: ヒストグラムのビン数
    previous_steps: 0 とするタイムステップの位置
    """

    # データ全体の最小・最大値を求める（x, y, z を統一したスケールで扱う）
    global_min = min(x.min(), y.min(), z.min())
    global_max = max(x.max(), y.max(), z.max())
    adjuster = (global_max - global_min) / bins / 2

    # ヒストグラムのビンを統一
    bin_edges = np.linspace(global_min, global_max, bins + 1)

    # x の時間変化ヒストグラムを計算
    hist_list = []
    peak_values = []
    for i in range(x.shape[0]):
        hist, _ = np.histogram(x[i, :], bins=bin_edges)
        hist_list.append(hist)
        peak_values.append(bin_edges[np.argmax(hist)])  # 各タイムステップの最頻値

    hist_array = np.array(hist_list)

    # y, z の標準偏差を計算し、平均 ± 1std の範囲をバンドとして表示
    y_mean, y_std = np.mean(y), np.std(y)
    z_mean, z_std = np.mean(z), np.std(z)

    # Time Step の調整: y 軸を -previous_steps から開始し、カウントダウン表示
    time_steps = np.arange(-previous_steps + x.shape[0] - 1, -previous_steps - 1, -1) / 10**2

    # 図の作成（1つのプロット）
    fig, ax = plt.subplots(figsize=(6, 8))

    # x の時間変化をヒートマップとしてプロット（Time Step をカウントダウンに変更）
    extent = [bin_edges[0], bin_edges[-1], time_steps[-1], time_steps[0] + 0.01]
    cax = ax.imshow(hist_array, origin='lower', aspect='auto', cmap='Reds', extent=extent)

    # Y=0 の横線を追加
    ax.axhline(y=0, color='black', linestyle='--', linewidth=2)

    # y, z の分布範囲を半透明バンドとしてプロット
    ax.fill_betweenx(time_steps, y_mean - y_std + adjuster, y_mean + y_std + adjuster, color='#F4E511', alpha=0.2, label='Nucleotide Free State ±1 std')
    ax.fill_betweenx(time_steps, z_mean - z_std + adjuster, z_mean + z_std + adjuster, color='blue', alpha=0.2, label='AlF3 State ±1 std')

    # 各タイムステップの最頻値を点で表示（カウントダウン方向に修正）
    peak_values = np.array(peak_values)
    #ax.scatter(peak_values[::-1]+adjuster, time_steps, color='black', s=1, marker='o', label='Mode of Distribution')

    # 軸ラベル設定
    #ax.set_xlabel(r'$\phi$ ($rad$)', fontsize=20)
    #ax.set_ylabel(r'MD steps ($\times 10^4$)', fontsize=20)
    ax.tick_params(axis='both', labelsize=15)

    # y軸の反転（カウントダウン表示）
    ax.invert_yaxis()

    # 軸の目盛りの数値だけ非表示にする（目盛り線や軸線は残す）
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    # 凡例を追加
    #ax.legend()

    # カラーバー追加
    cbar = fig.colorbar(cax, ax=ax, label='')
    cbar.ax.set_yticklabels([])

    # 保存
    plt.savefig(save_path, bbox_inches='tight', format='pdf')
    plt.show()

def save_histogram_data(x, output_csv_path, bins=10, previous_steps=20):
    """
    入力データ x の各時点におけるヒストグラムを計算し、time_steps および hist_array をCSVに保存する。

    Parameters:
        x (ndarray): shape (T, N) の時系列データ
        output_csv_path (str or Path): 保存先のCSVファイルパス
        bins (int): ヒストグラムのビン数
        previous_steps (int): 時系列のオフセット（time_stepsを -previous_steps 起点に調整）
    """
    # ビンの範囲を設定
    global_min = np.min(x)
    global_max = np.max(x)
    bin_edges = np.linspace(global_min, global_max, bins + 1)

    # 各タイムステップごとのヒストグラム
    hist_list = []
    for i in range(x.shape[0]):
        hist, _ = np.histogram(x[i, :], bins=bin_edges)
        hist_list.append(hist)

    hist_array = np.array(hist_list)  # shape: (time, bins)

    # time_steps: 小数点表記で -previous_steps から始まる逆順
    time_steps = np.arange(-previous_steps + x.shape[0] - 1, -previous_steps - 1, -1) / 100

    # DataFrame にまとめる（time_steps を最初の列に）
    df = pd.DataFrame(hist_array, columns=[f'Bin_{i}' for i in range(bins)])
    df.insert(0, 'TimeStep', time_steps)

    # 保存
    df.to_csv(output_csv_path, index=False, encoding='utf-8-sig')

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
    

def extract_transition2(df, previous_steps=20, post_steps=20):
  """
  idxがneckmimic結合のタイミングに該当する。neckmimic結合の前後20stepを取る場合、
    previous_steps=20
    post_steps=20
  とする
  """
  if df['phi'].min() < 0: #1度でもpath2の方向に進んだらはじく
    return None, "path2"

  last_phi = df['phi'].iloc[-1]
  if last_phi > 0:
    # 条件を満たす最初の行のインデックスを取得
    idx = (df['contact_count_ratio'] > 0.99).idxmax()
  
    # その行までのデータを取得
    df_subset = df.loc[idx-previous_steps:idx+post_steps]
    if len(df_subset) != (previous_steps + post_steps + 1):
      print(f"{len(df_subset)=}")
      return None, "path2"
    return df_subset, 'path1'
  elif last_phi < -1:
    # 条件を満たす最初の行のインデックスを取得
    idx = (df['contact_count_ratio'] > 0.99).idxmax()
  
    # その行までのデータを取得
    df_subset = df.loc[:idx]
    return df_subset, 'path2'
  else:
    raise RuntimeError


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
        df, pth = extract_transition2(df, previous_steps=50, post_steps=250)
        if pth == 'path1':
          df = df.reset_index()
          df_list.append(df)

        #  phis.append(df['phi'].to_list()[:1000])

    mean_df = pd.concat(df_list).groupby(level=0).mean()
    phis = np.array([df['phi'].values for df in df_list])
    print(phis)
    print(phis.shape)
    print(sum(phis[:,51] > 2.2) / phis.shape[0]) #neck-mimic docks時点でalf3 stateをとる割合を計算

    free = pd.read_csv("../analysis-04/step02_plot_distributions.out/free.csv")
    alf3 = pd.read_csv("../analysis-04/step02_plot_distributions.out/alf3.csv")
    free = free[(free['phi'] > phis.min()) & (free['phi'] < phis.max())]
    alf3 = alf3[(alf3['phi'] > phis.min()) & (alf3['phi'] < phis.max())]

    plot_data_distribution_histogram_with_overlay(phis.T, free["phi"].to_numpy(), alf3["phi"].to_numpy(), args.out, bins=30, previous_steps=50)
    #save_histogram_data(phis.T, args.raw_data, bins=30, previous_steps=50)

if __name__ == "__main__":
    main()
