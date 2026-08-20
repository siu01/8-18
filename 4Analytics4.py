import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


# ============================================================
# 1. データ読み込み
# ============================================================

df = pd.read_csv(
    "pr_dataset.csv"
)


# ============================================================
# 2. 機械学習で使用する特徴量
# ============================================================

FEATURE_COLUMNS = [
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
# 3. 説明変数X・目的変数y
# ============================================================

# PRのメトリクス
X = df[
    FEATURE_COLUMNS
].fillna(0)

# merged:
#   1 = MERGED
#   0 = CLOSED
y = df[
    "merged"
]


# ============================================================
# 4. データセットを8:2に分割
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,

    # 20%をテスト
    test_size=0.2,

    # 毎回同じ結果にする
    random_state=42,

    # MERGED/CLOSEDの比率を
    # 学習・テストでなるべく維持
    stratify=y,
)


print("全データ:", len(X))
print("学習データ:", len(X_train))
print("テストデータ:", len(X_test))


# ============================================================
# 5. ロジスティック回帰モデル
# ============================================================

# ロジスティック回帰では特徴量のスケール差が大きいため
# StandardScalerで標準化してから学習する
model = Pipeline(
    [
        (
            "scaler",
            StandardScaler(),
        ),
        (
            "classifier",
            LogisticRegression(
                max_iter=2000,
                random_state=42,
            ),
        ),
    ]
)


# ============================================================
# 6. 学習
# ============================================================

model.fit(
    X_train,
    y_train,
)


# ============================================================
# 7. テストデータを予測
# ============================================================

y_pred = model.predict(
    X_test
)


# ============================================================
# 8. Accuracy / Precision / Recall / F1
# ============================================================

accuracy = accuracy_score(
    y_test,
    y_pred,
)

precision = precision_score(
    y_test,
    y_pred,
    zero_division=0,
)

recall = recall_score(
    y_test,
    y_pred,
    zero_division=0,
)

f1 = f1_score(
    y_test,
    y_pred,
    zero_division=0,
)


print()
print("=" * 60)
print("Logistic Regression")
print("=" * 60)

print(
    f"Accuracy : {accuracy:.4f}"
)

print(
    f"Precision: {precision:.4f}"
)

print(
    f"Recall   : {recall:.4f}"
)

print(
    f"F1       : {f1:.4f}"
)


# ============================================================
# 9. 混同行列
# ============================================================

cm = confusion_matrix(
    y_test,
    y_pred,
)

print()
print("Confusion Matrix")
print(cm)


# ============================================================
# 10. ロジスティック回帰の係数
# ============================================================

# Pipeline内のLogisticRegressionを取り出す
classifier = model.named_steps[
    "classifier"
]

coefficients = classifier.coef_[0]


coefficient_df = pd.DataFrame(
    {
        "feature":
            FEATURE_COLUMNS,

        "coefficient":
            coefficients,
    }
)

# 絶対値が大きい順に並べる
coefficient_df[
    "abs_coefficient"
] = (
    coefficient_df[
        "coefficient"
    ].abs()
)

coefficient_df = (
    coefficient_df
    .sort_values(
        "abs_coefficient",
        ascending=False,
    )
)


print()
print("=" * 60)
print("Logistic Regression係数")
print("=" * 60)

print(
    coefficient_df.to_string(
        index=False
    )
)