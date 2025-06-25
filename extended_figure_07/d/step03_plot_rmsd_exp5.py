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
    
    指定された範囲ごとに平均と標準偏差を計算し、別の色でプロットする
    """
    # 全データをnumpy配列に変換
    arrays = [df.values.flatten() for df in df_list]
    data = np.vstack(arrays)  # shape: (num_samples, num_timesteps)

    # 時間軸
    timesteps = np.arange(data.shape[1])

    # プロット
    plt.figure(figsize=(10, 6))

    # --- 各区間ごとにプロット ---
    sections = {
        '0-2000': (0, 2000, 'Stage 1'),
        '2000-2300': (2000, 2300, 'Stage 2'),
        '2300-22300': (2300, 22300, 'Stage 3')
    }
    colors = {
        '0-2000': '#000080',
        '2000-2300': '#00FFFF',
        '2300-22300': '#FF0000'
    }

    for label, (start, end, stage_name) in sections.items():
        mean = np.mean(data[:, start:end], axis=0)
        std = np.std(data[:, start:end], axis=0)
        time_sec = timesteps[start:end] / 100

        plt.plot(time_sec, mean, label=f"{stage_name}", color=colors[label], lw=2)
        plt.fill_between(time_sec, mean - std, mean + std, alpha=0.3, color=colors[label])

    #plt.xlabel(r"MD steps ($\times 10^{4}$)")
    plt.ylim(0, 12)
    plt.grid(True)
    #plt.legend(fontsize=20)
    plt.tight_layout()
    ax = plt.gca()
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    # 保存 or 表示
    if save_path is not None:
        plt.savefig(save_path, dpi=300, format='pdf')
        plt.close()
        print(f"{save_path} is saved!")
    else:
        plt.show()

    return  # 特にmean, stdを返さない設計にしたければここで終了


def save_mean_std_from_df_list_to_csv(df_list, filename="plot_data.csv"):
    """
    df_list: List of pandas Series or single-column DataFrames
        各サンプルの時系列データを含むリスト。
    filename: str
        出力するCSVファイルのパス。

    各時刻における平均、標準偏差、±1SDの値を含むCSVを保存する。
    """
    print(df_list)
    # 全データをnumpy配列に変換
    arrays = [df.values.flatten() for df in df_list]
    data = np.vstack(arrays)  # shape: (num_samples, num_timesteps)

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
def load_rmsd(csv_dir, average_window=None):
    # List all the parquet files
    paths = [str(file) for file in pathlib.Path(csv_dir).rglob(f"*.csv")]
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
    args = parser.parse_args()

    
    df_list = load_rmsd(args.dir, average_window=None)

    plot_mean_and_std(df_list, save_path=args.out)

      

if __name__=="__main__":
  main()
