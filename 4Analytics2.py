import os

import matplotlib.pyplot as plt
import pandas as pd


# ============================================================
# 1. データセットを読み込む
# ============================================================

df = pd.read_csv("pr_dataset.csv")


# ============================================================
# 2. 比較するメトリクス
# ============================================================

METRICS = [
    "commit_count",
    "changed_files",
    "additions",
    "deletions",
    "changed_lines",
    "title_length",
    "body_length",
    "commit_message_total_length",
    "commit_message_avg_length",
    "commit_message_keyword_count",
]


# ============================================================
# 3. グラフ保存フォルダを作る
# ============================================================

OUTPUT_DIR = "plots"

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True,
)


# ============================================================
# 4. MERGEDとCLOSEDを分ける
# ============================================================

merged_df = df[
    df["merged"] == 1
]

closed_df = df[
    df["merged"] == 0
]


# ============================================================
# 5. 各メトリクスについて箱ひげ図を作成
# ============================================================

for metric in METRICS:

    # MERGEDのデータ
    merged_values = (
        merged_df[metric]
        .dropna()
        .values
    )

    # CLOSEDのデータ
    closed_values = (
        closed_df[metric]
        .dropna()
        .values
    )

    # 新しいグラフを作る
    plt.figure(
        figsize=(7, 6)
    )

    # 箱ひげ図
    plt.boxplot(
        [
            merged_values,
            closed_values,
        ]
    )

    # X軸ラベル
    plt.xticks(
        [1, 2],
        [
            "MERGED",
            "CLOSED",
        ],
    )

    # タイトル
    plt.title(
        f"{metric}: MERGED vs CLOSED"
    )

    # Y軸
    plt.ylabel(metric)

    # 補助線
    plt.grid(
        axis="y",
        alpha=0.3,
    )

    # レイアウト調整
    plt.tight_layout()

    # PNGとして保存
    output_path = os.path.join(
        OUTPUT_DIR,
        f"{metric}_boxplot.png",
    )

    plt.savefig(
        output_path,
        dpi=150,
    )

    # メモリ解放
    plt.close()

    print(
        "保存:",
        output_path,
    )


print()
print("箱ひげ図の作成完了")