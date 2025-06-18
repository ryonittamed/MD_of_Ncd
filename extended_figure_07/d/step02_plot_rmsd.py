#!/usr/bin/env python

import argparse
import pathlib
import warnings

warnings.filterwarnings("ignore")
warnings.warn = lambda *args, **kwargs: None

import matplotlib.pyplot as plt
import matplotlib.cm as cm

import numpy as np
import pandas as pd
from pathlib import Path

plt.rcParams.update({'font.size': 25})

def plot_mean_and_std(df_list, save_path=None):
    """
    df_list: List of pandas Series or single-column DataFrames
    save_path: str or Path, optional
        プロット画像の保存先パス。Noneなら保存せず表示だけする。

    各時刻における値の平均と標準偏差を計算し、プロットする
    """
    # 全データをnumpy配列に変換
    arrays = [df.values.flatten() for df in df_list]
    data = np.vstack(arrays)  # shape: (num_samples, num_timesteps)

    # 平均と標準偏差を計算
    mean = np.mean(data, axis=0)
    std = np.std(data, axis=0)

    # 時間軸
    timesteps = np.arange(len(mean))

    # プロット
    plt.figure(figsize=(10, 6))
    plt.plot(timesteps / 100, mean, label="Mean", lw=2)
    plt.fill_between(timesteps / 100, mean - std, mean + std, alpha=0.3, label="±1 Std Dev")
    #plt.xlabel(r"MD steps ($\times 10^{4}$)")
    #plt.ylabel("Value")
    #plt.title("Mean and Standard Deviation over Time")
    #plt.legend()
    plt.ylim(0, 12)
    plt.grid(True)
    plt.tight_layout()
    ax = plt.gca()
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    # 保存 or 表示
    if save_path is not None:
        plt.savefig(save_path, dpi=300, format='pdf')
        plt.close()  # メモリ節約のためクローズ
        print(f"{save_path} is saved!")
    else:
        plt.show()

    return mean, std

def save_mean_std_from_df_list_to_csv(df_list, filename="plot_data.csv", target_length=100000):
    """
    df_list: List of pandas Series or single-column DataFrames
        各サンプルの時系列データを含むリスト。
    filename: str
        出力するCSVファイルのパス。

    各時刻における平均、標準偏差、±1SDの値を含むCSVを保存する。
    """
    ## 全データをnumpy配列に変換
    #arrays = [df.values.flatten() for df in df_list]
    # 指定された長さのデータだけを抽出
    valid_arrays = [df.values.flatten() for df in df_list if len(df) == target_length]

    if len(valid_arrays) == 0:
        raise ValueError(f"No entries in df_list have length == {target_length}.")
    data = np.vstack(valid_arrays)  # shape: (num_samples, num_timesteps)

    # 平均と標準偏差を計算
    mean = np.mean(data, axis=0)
    std = np.std(data, axis=0)

    # 時間軸（100分の1スケーリング）
    timesteps = np.arange(len(mean)) / 100

    # データフレーム作成
    df = pd.DataFrame({
        "timesteps": timesteps,
        "mean": mean,
        "std_upper": mean + std,
        "std_lower": mean - std
    })

    # CSVとして保存
    df.to_csv(filename, index=False)

def load_rmsd(csv_dir, state="free", average_window=None):
    # List all the parquet files
    paths = [str(file) for file in pathlib.Path(csv_dir).rglob(f"{state}.csv")]
    paths = sorted(paths)

    # Load dataframes
    df_list = []
    indexs = []
    for path in paths:
        df = pd.read_csv(path)

        #calculate moving average
        if average_window:
          df['rmsd'] = df['rmsd'].rolling(window=average_window).mean()

        df_list.append(df["rmsd"])
        

        indexs.append(np.arange(len(df)))


    return df_list

def generate_colors(num_colors, cmap_name='viridis'):
    """
    指定したカラーマップから任意の数の色を生成
    """
    if num_colors == 1:
      return ["red"]

    cmap = cm.get_cmap(cmap_name)  # カラーマップを取得
    colors = [cmap(i / (num_colors - 1)) for i in range(num_colors)]
    return colors

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", type=str, required=True, help="Directory containing CVs in csv format")
    parser.add_argument("--out", type=str, required=True, help="Output file name")
    parser.add_argument("--raw-data", type=str, required=True, help="Raw data file name")
    parser.add_argument("--state", type=str, required=True, help="free or alf3")
    args = parser.parse_args()

    #colors = generate_colors(len(args.dirs))
    #labels = [Path(path).stem for path in args.dirs]

    #for color, csv_dir, label in zip(colors, args.dirs, labels):
    #  rmsd_list = load_rmsd(csv_dir, average_window=1000)
    #  for i,rmsd in enumerate(rmsd_list):
    #    #plt.plot(rmsd, color=color, label=label if i==0 else None, linewidth=0.2)
    #    # Split trajectory
    #    sim1 = rmsd.iloc[:2000]
    #    sim2 = rmsd.iloc[2000:2300]
    #    sim3 = rmsd.iloc[2300:22300]
    #    sim4 = rmsd.iloc[22300:22600]
    #    sim5 = rmsd.iloc[22600:42600]
    #    colors_ = generate_colors(5)
    #    for c,sim in zip(colors_, [sim1, sim2, sim3, sim4, sim5]):
    #      plt.plot(sim, color=c, linewidth=0.2)
    #    # Split trajectory
    
    df_list = load_rmsd(args.dir, state=args.state, average_window=None)

    #Plot Figures
    plot_mean_and_std(df_list, save_path=args.out)

    #Save raw data
    #save_mean_std_from_df_list_to_csv(df_list, filename=args.raw_data)
           

    #plt.legend()
    #plt.savefig(args.out, dpi=300)
    #plt.close()

      

if __name__=="__main__":
  main()
