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
import ast
from collections import Counter
from config import Neckmimic

def plot_heatmap(df, save_path, font_size=20, normalize=True):
    """
    df: 入力DataFrame（カラムごとに最大値で正規化される）
    save_path: 保存先パス（例: 'output/heatmap.png'）
    font_size: 軸ラベル・目盛りの文字サイズ
    """

    # --- 1. カラムごとに最大値で正規化 ---
    normalized_df = df.copy()
    if normalize:
      for col in normalized_df.columns:
          max_val = normalized_df[col].max()
          if max_val != 0:
              normalized_df[col] = normalized_df[col] / max_val
          else:
              normalized_df[col] = 0  # max=0なら全部0

    # --- 2. インデックスリスケーリング ---
    # 0 → -20, 50 → 0, 300 → 250 の変換
    new_index = -50 + (df.index / 50) * 50
    normalized_df.index = new_index

    # --- 3. ヒートマッププロット ---
    plt.figure(figsize=(14, 8))
    im = plt.imshow(normalized_df, 
                    aspect='auto', 
                    origin='upper',    # 上から下にカウントアップ
                    cmap='Blues')

    # 横軸にResidue（カラム名）
    plt.xticks(
        ticks=np.arange(len(normalized_df.columns)), 
        #labels=normalized_df.columns, 
        rotation=45,
        ha='center',
        fontsize=font_size+5
    )

    # ↓↓↓ 追加！ここ！
    plt.gca().xaxis.set_ticks_position('top')
    plt.gca().xaxis.set_label_position('top')

    # Y軸：ラベルを10で割った値に変換して表示
    ytick_positions = np.linspace(0, len(normalized_df.index) - 1, 6)
    ytick_labels = np.linspace(normalized_df.index.min(), normalized_df.index.max(), 6) / 100
    
    plt.yticks(
        ticks=ytick_positions,
        #labels=np.round(ytick_labels, 1),  # 小数第1位まで表示
        fontsize=font_size
    )

    plt.xlabel("Residue", fontsize=font_size+2)
    plt.ylabel(r"MD steps ($\times 10^4$)", fontsize=font_size+5)

    # カラーバー
    cbar = plt.colorbar(im)
    #cbar.set_label("Normalized Contact Count", fontsize=font_size)
    cbar.set_label("", fontsize=font_size)
    cbar.ax.invert_yaxis()
    cbar.ax.set_yticklabels([])

    # --- 4. Frame=0の位置に横線を引く ---
    # Frame=0に対応するindex位置を計算
    #zero_frame_index = (0 - (-50)) / (250 - (-50)) * (len(normalized_df.index) - 1)
    #print(f"{zero_frame_index=}")
    zero_frame_index = 50 #equal to previous_steps
    plt.axhline(y=zero_frame_index, color='red', linestyle='--', linewidth=3)

    plt.tight_layout()

    # --- 5. 保存 ---
    plt.savefig(save_path, dpi=300, format='pdf')
    plt.close()

    print(f"ヒートマップを保存しました: {save_path}")


def save_plot_heatmap(df, output_csv, normalize=True):
    """
    df: 入力DataFrame（カラムごとに最大値で正規化される）
    save_path: 保存先パス（例: 'output/heatmap.png'）
    font_size: 軸ラベル・目盛りの文字サイズ
    """

    # --- 1. カラムごとに最大値で正規化 ---
    normalized_df = df.copy()
    if normalize:
      for col in normalized_df.columns:
          max_val = normalized_df[col].max()
          if max_val != 0:
              normalized_df[col] = normalized_df[col] / max_val
          else:
              normalized_df[col] = 0  # max=0なら全部0

    # --- 2. インデックスリスケーリング ---
    # 0 → -20, 50 → 0, 300 → 250 の変換
    new_index = -50 + (df.index / 50) * 50
    normalized_df.index = new_index

    normalized_df.to_csv(output_csv)

def convert_and_sum_contact_sets(df_list, number_range, name_mapping, column_name='contact_resids_in_neckmimic'):
    """
    df_list: List of DataFrames
    number_range: Iterable (e.g., range(7884, 7899))
    name_mapping: Dict for renaming columns (e.g., {7884: 'A', 7885: 'B', ...})

    Returns: Summed and renamed DataFrame
    """
    # 初期化：インデックス0-300、カラム7884-7898、すべて0
    result_df = pd.DataFrame(0, index=range(0, len(df_list[0])), columns=number_range)

    for df in df_list:
        # 一時的なカウント用DataFrame
        temp_df = pd.DataFrame(0, index=range(0, len(df_list[0])), columns=number_range)

        for idx, row in df.iterrows():
            contacts = row[column_name]  # ここは辞書(dict型)になっている！
            for num in number_range:
                # contactsにその番号が含まれていれば、そのカウント値を加算
                if num in contacts:
                    temp_df.at[idx, num] = contacts[num]

        # 各dfごとに加算
        if column_name == 'contact_resids_in_neckmimic':
          result_df += temp_df
        elif column_name == 'docks':
          result_df |= temp_df

    # 最後にカラム名をname_mappingでリネーム
    result_df = result_df.rename(columns=name_mapping)
    result_df.index.name = 'index'

    return result_df



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

def plot_residue_counts_with_labels(counts_dict, save_path="residue_counts.png"):
    # 残基ラベルをリスト化して、番号順にソート（番号を抜き出して比較）
    residues = sorted(counts_dict.keys(), key=lambda x: int(''.join(filter(str.isdigit, x))))
    counts = [counts_dict[r] for r in residues]

    # プロット
    plt.figure(figsize=(12, 6))
    plt.bar(residues, counts)

    # 軸ラベル
    plt.xlabel("Residue")
    plt.ylabel("Count")
    plt.title("Residue Contact Counts")

    # 見た目調整
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # 保存
    plt.savefig(save_path)
    plt.close()

    print(f"Plot saved to {save_path}")

def count_all_occurrences(l):
    counter = Counter()
    for s in l:
        counter.update(s)  # セット内の要素を全部カウント
    return dict(counter)

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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", type=str, required=True, help="Directory containing CVs in parquet format")
    parser.add_argument("--out", type=str, required=True, help="Output file name")
    parser.add_argument("--target", type=int, required=False, help="Target simulation number")
    args = parser.parse_args()

    # List all the parquet files
    paths = [str(file) for file in pathlib.Path(args.dir).rglob("*.csv")]
    paths = sorted(paths)

    # Specify target path is args.target is defined
    paths = paths if args.target is None else paths[args.target-1:args.target]

    # Load dataframes
    df_list = []
    indexs = []
    last_contacts = []
    contact_resids_in_neckmimic_lasts = []
    for path in paths:
        df = pd.read_csv(path)
        df['contact_resids_in_neckmimic'] = df['contact_resids_in_neckmimic'].apply(ast.literal_eval)
        df['docks'] = df['docks'].apply(ast.literal_eval)

        # Split trajectory
        sim1 = df.iloc[:2000]
        sim2 = df.iloc[2000:2300]
        sim3 = df.iloc[2300:22300]
        sim4 = df.iloc[22300:22600]
        sim5 = df.iloc[22600:42600]


        # Unwrap angles
        df = unwrap_angles(sim3)

        # Extract only transition part
        df, pth = extract_transition2(df, previous_steps=50, post_steps=20)
        if pth == 'path1':
          df = df.reset_index() 
          df_list.append(df)    

    #df_listの整形
    config = Neckmimic()

    converted_df = convert_and_sum_contact_sets(df_list, number_range=config.neckmimic_range, name_mapping=config.resname_dict, column_name='contact_resids_in_neckmimic')


    #Plot
    plot_heatmap(converted_df, args.out, normalize=True)


  

if __name__ == "__main__":
    main()
