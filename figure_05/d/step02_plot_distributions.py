#!/usr/bin/env python

import argparse
import pathlib
import warnings
import seaborn as sns
from pathlib import Path

warnings.filterwarnings("ignore")
warnings.warn = lambda *args, **kwargs: None

import polars as pl
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import matplotlib.ticker as ticker

from color_config import Color


plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "DejaVu Sans", "Liberation Sans"]

sns.set(font="sans-serif")  # Seaborn の場合

def plot_2d_kde_with_marginals(df_x: pd.DataFrame, df_y: pd.DataFrame, save_path: str):
    """
    2つのデータフレームを使って2次元KDEプロットを作成し、それぞれの軸に1次元のKDEを追加する。

    Parameters:
    df_x (pd.DataFrame): X軸とY軸のデータを含むデータフレーム（カラム: 'theta', 'phi'）
    df_y (pd.DataFrame): X軸とY軸のデータを含むデータフレーム（カラム: 'theta', 'phi'）
    save_path (str): 画像の保存パス
    """
    #setup colors
    colors = Color()

    # 必要なカラムのみを抽出し、数値型に変換
    df_x = df_x[['theta', 'phi']].copy().apply(pd.to_numeric, errors='coerce').replace([np.inf, -np.inf], np.nan).dropna()
    df_y = df_y[['theta', 'phi']].copy().apply(pd.to_numeric, errors='coerce').replace([np.inf, -np.inf], np.nan).dropna()

    # 図のセットアップ
    fig = plt.figure(figsize=(8, 8))
    grid = plt.GridSpec(6, 6, hspace=0.1, wspace=0.1)

    # メインの 2D KDE プロット
    ax_main = fig.add_subplot(grid[1:, :-1])
    sns.kdeplot(x=df_x["theta"], y=df_x["phi"], color=colors.without_neckmimic, fill=False, ax=ax_main, thresh=.002, linewidth=2.0)
    sns.kdeplot(x=df_y["theta"], y=df_y["phi"], color=colors.with_neckmimic, fill=False, ax=ax_main, thresh=.002, linewidth=2.0)
    #ax_main.set_xlabel(r"$\theta$ ($rad$)")
    #ax_main.set_ylabel(r"$\phi$ ($rad$)")
    ax_main.set_xlim(1, 3)
    ax_main.set_ylim(0, 6)

    # x軸とy軸の目盛り (locatorを適用)
    #x_ticks = np.arange(1, 3, 1)
    #y_ticks = np.arange(0, 6, 1)
    #ax_main.set_xticks(x_ticks)
    #ax_main.set_yticks(y_ticks)
    ax_main.xaxis.set_major_locator(ticker.MultipleLocator(0.5))
    ax_main.yaxis.set_major_locator(ticker.MultipleLocator(1.0))

    # グリッドを表示
    ax_main.grid(True, linestyle="--", linewidth=0.5, alpha=0.7)

    # X軸の1次元分布 (上部)
    ax_xdist = fig.add_subplot(grid[0, :-1], sharex=ax_main)
    sns.kdeplot(x=df_x["theta"], ax=ax_xdist, fill=False, lw=2, color=colors.without_neckmimic, thresh=.002)
    sns.kdeplot(x=df_y["theta"], ax=ax_xdist, fill=False, lw=2, color=colors.with_neckmimic, thresh=.002)
    ax_xdist.tick_params(axis="both", which="both", bottom=False, left=False, labelbottom=False, labelleft=False)
    ax_xdist.set_xlabel("")
    ax_xdist.set_ylabel("")
    ax_xdist.get_xaxis().set_visible(False)
    ax_xdist.get_yaxis().set_visible(False)

    # Y軸の1次元分布 (右側)
    ax_ydist = fig.add_subplot(grid[1:, -1], sharey=ax_main)
    sns.kdeplot(y=df_x["phi"], ax=ax_ydist, fill=False, lw=2, color=colors.without_neckmimic, thresh=.002)
    sns.kdeplot(y=df_y["phi"], ax=ax_ydist, fill=False, lw=2, color=colors.with_neckmimic, thresh=.002)
    ax_ydist.tick_params(axis="both", which="both", bottom=False, left=False, labelbottom=False, labelleft=False)
    ax_ydist.set_xlabel("")
    ax_ydist.set_ylabel("")
    ax_ydist.get_xaxis().set_visible(False)
    ax_ydist.get_yaxis().set_visible(False)

    # 軸の目盛りの数値だけ非表示にする（目盛り線や軸線は残す）
    ax_main.set_xticklabels([])
    ax_main.set_yticklabels([])
    ax_main.set_xlabel("")
    ax_main.set_ylabel("")

    # 画像の保存
    plt.savefig(save_path, bbox_inches="tight", dpi=300, format='pdf')
    plt.show()

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
  else:
    return df, "path1"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dirs", nargs='+', type=str, required=True, help="Directory containing CVs in parquet format")
    parser.add_argument("--out_dir", type=str, required=True, help="Output file name")
    parser.add_argument("--state", type=str, required=True, help="free or alf3 state")
    args = parser.parse_args()

    all_data_list = []
    x_min, x_max, y_min, y_max = 0,0,0,0
    # dirごとにdistributionをプロットする
    for i,dirname in enumerate(args.dirs):
      # List all the parquet files
      #paths = [str(file) for file in pathlib.Path(dirname).rglob("*.parquet")]
      paths = [str(file) for file in pathlib.Path(dirname).rglob(f"{args.state}.csv")]
      paths = sorted(paths)

      # Load dataframes
      df_list = []
      indexs = []
      for path in paths:
          #df = pd.read_parquet(path)
          print(path)
          df = pd.read_csv(path)

          ## Split trajectory
          sim1 = df.iloc[:2000]
          sim2 = df.iloc[2000:2300]
          sim3 = df.iloc[2300:22300]
          sim4 = df.iloc[22300:22600]
          sim5 = df.iloc[22600:42600]

          # Unwrap angles
          #df = unwrap_angles(sim3)
          df = unwrap_angles(df)

          #不自然なpathを除外
          df, trans = extract_transition(df)
          if trans == "path1":
            df_list.append(df)
            indexs.append(np.arange(len(df)))


      data = pd.concat(df_list)
      print(data)
      print(f"Number of data of {dirname}:",len(df_list))
      #data.to_csv(Path(args.out_dir) / f"{args.state}.csv")
      #exit()

      # Plot scatter
      #sampled_data = data.sample(n=min(10000, len(data)), random_state=42)
      sampled_data = data
      if i==0:
        x_min, x_max, y_min, y_max = sampled_data['theta'].min(), sampled_data['theta'].max(), sampled_data['phi'].min(), sampled_data['phi'].max()
      print(f"{x_min=}")
      print(f"{y_min=}")
      print(f"{x_max=}")
      print(f"{y_max=}")

      #plt.scatter(sampled_data['theta'], sampled_data['phi'], s=1)
      #plt.xlim(x_min, x_max)
      #plt.ylim(y_min, y_max)
      #plt.xlabel(r"$\theta$ ($rad$)")
      #plt.ylabel(r"$\phi$ ($rad$)")
      #filename = Path(dirname).name + f'_{args.state}.png'
      #plt.savefig(Path(args.out_dir) / filename, dpi=300)
      #plt.close()

      
       


      # Plot distribution
      #sns.kdeplot(sampled_data, x='theta', y='phi', fill=True, thresh=.002)
      #plt.xlim(x_min, x_max)
      #plt.ylim(y_min, y_max)
      #plt.xlabel(r"$\theta$ ($rad$)")
      #plt.ylabel(r"$\phi$ ($rad$)")
      #filename = Path(dirname).name + f'_kde_{args.state}.png'
      #plt.savefig(Path(args.out_dir) / filename, dpi=300)
      #plt.close()

      # add data to all_data
      data['case'] = Path(dirname).name
      all_data_list.append(data)
    
    # plot all data
    all_data = pd.concat(all_data_list)
    #sampled_data = all_data.sample(n=min(1000, len(data)), random_state=42) #for debug
    sampled_data = all_data.copy()

    # フォントとフォントサイズの設定
    font_size = 20  # フォントサイズ
    font_name = "Arial"  # 例: Arialフォントを使用
    
    # Seabornの設定（軸ラベルや目盛りのフォントサイズを統一）
    sns.set_context("notebook", font_scale=1.5)  # 目盛りなどのフォントスケール
    sns.set_style("white")  # 背景を無地の白に設定

    # Plot
    filename = f'hist_eq_{args.state}_revised.pdf'
    plot_2d_kde_with_marginals(
      sampled_data[sampled_data['case'] == "kinesin-no-neckmimic.equiliblium"], 
      sampled_data[sampled_data['case'] == "kinesin.equiliblium"], 
      str(Path(args.out_dir) / filename),
      )


if __name__ == "__main__":
    main()
