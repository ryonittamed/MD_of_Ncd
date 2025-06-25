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
from color_config import Color

plt.rcParams.update({'font.size': 25})

def plot_mean_and_std_two_groups(df_list1, df_list2, save_path=None):
    """
    df_list1, df_list2: List of pandas Series or single-column DataFrames
        2つの異なる条件のデータセットを比較プロットする
    save_path: str or Path, optional
        プロット画像の保存先パス。Noneなら保存せず表示だけする。
    """
    colors = Color()

    def get_mean_std(df_list):
        arrays = [df.values.flatten() for df in df_list]
        data = np.vstack(arrays)
        mean = np.mean(data, axis=0)
        std = np.std(data, axis=0)
        return mean, std

    mean1, std1 = get_mean_std(df_list1)
    mean2, std2 = get_mean_std(df_list2)
    timesteps = np.arange(len(mean1))

    plt.figure(figsize=(10, 6))

    # グループ1
    plt.plot(timesteps / 100, mean1, label="Group 1 Mean", lw=2, color=colors.with_neckmimic)
    plt.fill_between(timesteps / 100, mean1 - std1, mean1 + std1, alpha=0.3, label="Group 1 ±1 Std Dev", color=colors.with_neckmimic)

    # グループ2
    plt.plot(timesteps / 100, mean2, label="Group 2 Mean", lw=2, color=colors.without_neckmimic)
    plt.fill_between(timesteps / 100, mean2 - std2, mean2 + std2, alpha=0.3, label="Group 2 ±1 Std Dev", color=colors.without_neckmimic)

    plt.ylim(0, 32)
    plt.grid(True)
    plt.tight_layout()
    #plt.legend()
    ax = plt.gca()
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    if save_path is not None:
        plt.savefig(save_path, dpi=300, format='pdf')
        plt.close()
        print(f"{save_path} is saved!")
    else:
        plt.show()


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

def save_mean_std_two_groups(
    df_list1, df_list2, output_csv_path,
    list1_name="Group1", list2_name="Group2"
):
    """
    2つの条件のデータセットに対して時間ステップごとの平均・標準偏差を計算し、CSVに保存する。

    Parameters:
        df_list1 (list of pd.Series or pd.DataFrame): 条件1のデータ（縦に積む）
        df_list2 (list of pd.Series or pd.DataFrame): 条件2のデータ（縦に積む）
        output_csv_path (str or Path): 出力CSVの保存パス
        list1_name (str): df_list1 のラベル名（列名に使用）
        list2_name (str): df_list2 のラベル名（列名に使用）
    """
    def get_mean_std(df_list):
        arrays = [df.values.flatten() for df in df_list]
        data = np.vstack(arrays)
        mean = np.mean(data, axis=0)
        std = np.std(data, axis=0)
        return mean, std

    mean1, std1 = get_mean_std(df_list1)
    mean2, std2 = get_mean_std(df_list2)

    timesteps = np.arange(len(mean1))

    df = pd.DataFrame({
        "TimeStep": timesteps,
        f"Mean_{list1_name}": mean1,
        f"Std_{list1_name}": std1,
        f"Mean_{list2_name}": mean2,
        f"Std_{list2_name}": std2,
    })

    df.to_csv(output_csv_path, index=False, encoding="utf-8-sig")

def load_stalk_rmsd(csv_dir, state="free", average_window=None):
    # List all the parquet files
    paths = [str(file) for file in pathlib.Path(csv_dir).rglob(f"{state}.csv")]
    paths = sorted(paths)

    # Load dataframes
    df_list = []
    indexs = []
    for path in paths:
        df = pd.read_csv(path)

        if len(df) != 10**5:
          continue

        #calculate moving average
        if average_window:
          df['stalk_rmsd'] = df['stalk_rmsd'].rolling(window=average_window).mean()

        df_list.append(df["stalk_rmsd"])
        

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
    parser.add_argument("--dir-kinesin", type=str, required=True, help="Directory containing CVs in csv format")
    parser.add_argument("--dir-no-kinesin", type=str, required=True, help="Directory containing CVs in csv format")
    parser.add_argument("--out", type=str, required=True, help="Output file name")
    parser.add_argument("--state", type=str, required=True, help="free or alf3")
    args = parser.parse_args()

    df_list_kinesin = load_stalk_rmsd(args.dir_kinesin, state=args.state, average_window=None)
    df_list_no_kinesin = load_stalk_rmsd(args.dir_no_kinesin, state=args.state, average_window=None)

    plot_mean_and_std_two_groups(df_list_kinesin, df_list_no_kinesin, save_path=args.out)

      

if __name__=="__main__":
  main()
