import pandas as pd

from scipy.stats import mannwhitneyu


# ============================================================
# 1. データ読み込み
# ============================================================

df = pd.read_csv(
    "pr_dataset.csv"
)


# ============================================================
# 2. 検定するメトリクス
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
# 3. MERGED / CLOSED に分割
# ============================================================

merged_df = df[
    df["merged"] == 1
]

closed_df = df[
    df["merged"] == 0
]


# ============================================================
# 4. Mann-Whitney U検定
# ============================================================

results = []

# 有意水準
ALPHA = 0.05


for metric in METRICS:

    # MERGED側
    merged_values = (
        merged_df[metric]
        .dropna()
    )

    # CLOSED側
    closed_values = (
        closed_df[metric]
        .dropna()
    )

    # --------------------------------------------------------
    # Mann-Whitney U検定
    #
    # 帰無仮説:
    #   MERGEDとCLOSEDで分布に差がない
    #
    # 対立仮説:
    #   MERGEDとCLOSEDで分布が異なる
    # --------------------------------------------------------

    result = mannwhitneyu(
        merged_values,
        closed_values,

        # 両側検定
        alternative="two-sided",

        # サンプル数などに応じて
        # SciPyが適切な方法を選択
        method="auto",
    )

    u_statistic = result.statistic
    p_value = result.pvalue

    # --------------------------------------------------------
    # p < 0.05なら統計的有意差あり
    # --------------------------------------------------------

    significant = (
        p_value < ALPHA
    )

    # 中央値も計算する
    merged_median = (
        merged_values.median()
    )

    closed_median = (
        closed_values.median()
    )

    results.append(
        {
            "metric": metric,
            "merged_median":
                merged_median,
            "closed_median":
                closed_median,
            "u_statistic":
                u_statistic,
            "p_value":
                p_value,
            "significant_0.05":
                significant,
        }
    )

    # --------------------------------------------------------
    # 結果表示
    # --------------------------------------------------------

    print("=" * 60)

    print(
        "メトリクス:",
        metric,
    )

    print(
        "MERGED中央値:",
        merged_median,
    )

    print(
        "CLOSED中央値:",
        closed_median,
    )

    print(
        "U統計量:",
        u_statistic,
    )

    print(
        "p値:",
        p_value,
    )

    if significant:

        print(
            "結果: 有意差あり "
            "(p < 0.05)"
        )

    else:

        print(
            "結果: 有意差なし "
            "(p >= 0.05)"
        )


# ============================================================
# 5. 結果をCSV保存
# ============================================================

result_df = pd.DataFrame(
    results
)

result_df.to_csv(
    "mann_whitney_results.csv",
    index=False,
    encoding="utf-8-sig",
)

print()
print(
    "mann_whitney_results.csv "
    "に保存しました"
)