import matplotlib.pyplot as plt
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split


# ============================================================
# 1. データ読み込み
# ============================================================

df = pd.read_csv(
    "pr_dataset.csv"
)


# ============================================================
# 2. 使用する特徴量
# ============================================================

# Logistic Regressionとまったく同じ特徴量を使用する。
#
# 同じデータを使わないと
# 「アルゴリズムを変えて精度が上がったのか」
# 公平に比較できないため。
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
# 3. X / y
# ============================================================

X = df[
    FEATURE_COLUMNS
].fillna(0)

y = df[
    "merged"
]


# ============================================================
# 4. Logistic Regressionと同じ条件で8:2分割
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,

    # Logistic Regressionと同じ42
    random_state=42,

    # クラス比率を維持
    stratify=y,
)


# ============================================================
# 5. RandomForestモデル
# ============================================================

model = RandomForestClassifier(

    # 決定木を300本作る
    n_estimators=300,

    # 毎回同じ結果になるよう固定
    random_state=42,

    # CPUを可能な限り利用
    n_jobs=-1,
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
# 8. 評価
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
print("Random Forest")
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
# 9. Confusion Matrix
# ============================================================

cm = confusion_matrix(
    y_test,
    y_pred,
)

print()
print("Confusion Matrix")
print(cm)


# ============================================================
# 10. Feature Importanceを取得
# ============================================================

importances = (
    model.feature_importances_
)


importance_df = pd.DataFrame(
    {
        "feature":
            FEATURE_COLUMNS,

        "importance":
            importances,
    }
)


# Importanceが高い順
importance_df = (
    importance_df
    .sort_values(
        "importance",
        ascending=False,
    )
)


print()
print("=" * 60)
print("Feature Importance")
print("=" * 60)

print(
    importance_df.to_string(
        index=False
    )
)


# ============================================================
# 11. ImportanceをCSV保存
# ============================================================

importance_df.to_csv(
    "random_forest_importance.csv",
    index=False,
    encoding="utf-8-sig",
)


# ============================================================
# 12. Importanceをグラフ化
# ============================================================

# 見やすいよう昇順へ並べ替える
plot_df = (
    importance_df
    .sort_values(
        "importance",
        ascending=True,
    )
)


plt.figure(
    figsize=(10, 7)
)

plt.barh(
    plot_df["feature"],
    plot_df["importance"],
)

plt.xlabel(
    "Feature Importance"
)

plt.ylabel(
    "PR Metric"
)

plt.title(
    "Random Forest Feature Importance"
)

plt.tight_layout()

plt.savefig(
    "random_forest_importance.png",
    dpi=150,
)

plt.close()


print()
print(
    "random_forest_importance.png "
    "を保存しました"
)