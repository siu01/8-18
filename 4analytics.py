import os

import pandas as pd
from dotenv import load_dotenv
from github import Github, Auth


# ============================================================
# 1. 基本設定
# ============================================================

# 分析対象のGitHubリポジトリ
REPOSITORY = "apache/lucene"

TARGET_COUNT = 200

# 最終的に保存するCSV
OUTPUT_FILE = "pr_dataset.csv"


# ============================================================
# 2. GitHubへ接続
# ============================================================

# .envファイルを読み込む
load_dotenv()

token = os.getenv("GITHUB_TOKEN")

if not token:
    raise ValueError("GITHUB_TOKEN がありません")

# PyGithubでGitHub APIへ接続
g = Github(auth=Auth.Token(token))

# apache/luceneリポジトリを取得
repo = g.get_repo(REPOSITORY)


# ============================================================
# 3. コミットメッセージから特徴量を作る関数
# ============================================================

def get_commit_message_metrics(pr):
    """
    PRに含まれるコミットを取得して、
    コミットメッセージに関する特徴量を作る。

    戻り値:
        commit_messages
        commit_message_total_length
        commit_message_avg_length
        commit_message_max_length
        commit_message_keyword_count
    """

    # PRに含まれるコミットをすべて取得
    commits = list(pr.get_commits())

    # 各コミットのメッセージを保存する
    messages = []

    for commit in commits:

        # commit.commit.message が実際のコミットメッセージ
        message = commit.commit.message or ""

        messages.append(message)

    # --------------------------------------------------------
    # コミットメッセージの長さを計算
    # --------------------------------------------------------

    message_lengths = [
        len(message)
        for message in messages
    ]

    # 全コミットメッセージの文字数
    total_length = sum(message_lengths)

    # 平均文字数
    if len(message_lengths) > 0:
        avg_length = total_length / len(message_lengths)
    else:
        avg_length = 0

    # 最大文字数
    if len(message_lengths) > 0:
        max_length = max(message_lengths)
    else:
        max_length = 0

    # --------------------------------------------------------
    # 技術的な変更を表しそうな単語の出現数
    # --------------------------------------------------------

    # 全コミットメッセージを小文字へ変換
    all_messages_lower = " ".join(messages).lower()

    keywords = [
        "fix",
        "bug",
        "refactor",
        "test",
        "todo",
    ]

    keyword_count = 0

    for keyword in keywords:
        keyword_count += all_messages_lower.count(keyword)

    # CSVの1セルへ保存できるよう改行を除去
    normalized_messages = []

    for message in messages:
        normalized_messages.append(
            message.replace("\n", " ")
        )

    joined_messages = " || ".join(normalized_messages)

    return {
        "commit_messages": joined_messages,
        "commit_message_total_length": total_length,
        "commit_message_avg_length": avg_length,
        "commit_message_max_length": max_length,
        "commit_message_keyword_count": keyword_count,
    }


# ============================================================
# 4. PRを取得
# ============================================================

print("Repository:", repo.full_name)
print("PRを取得しています...")
print()

rows = []


# ------------------------------------------------------------
# state="closed" にすることで OPEN PR を最初から除外する
#
# 課題ではOPEN状態のPRは、
# 今後MERGEDになるかCLOSEDになるかわからないため除外する。
# ------------------------------------------------------------

pull_requests = repo.get_pulls(
    state="closed",
    sort="created",
    direction="desc",
)


# ============================================================
# 5. 各PRについてメトリクスを取得
# ============================================================

for pr in pull_requests:

    # --------------------------------------------------------
    # MERGED / CLOSED を分類
    # --------------------------------------------------------

    # merged_at が存在する
    #   → マージされたPR
    #
    # merged_at がNone
    #   → マージされずに閉じられたPR
    #
    # 今回の課題では後者を「却下」と扱う
    # --------------------------------------------------------

    if pr.merged_at is not None:
        outcome = "MERGED"
        merged = 1

    else:
        outcome = "CLOSED"
        merged = 0

    # --------------------------------------------------------
    # PRに含まれるコミットメッセージを分析
    # --------------------------------------------------------

    commit_metrics = get_commit_message_metrics(pr)

    # PRタイトル
    title = pr.title or ""

    # PR本文
    body = pr.body or ""

    # --------------------------------------------------------
    # 1PR = 1行としてデータセットを作る
    # --------------------------------------------------------

    row = {
        # PRそのものの情報
        "pr_number": pr.number,
        "title": title,
        "url": pr.html_url,

        # 正解ラベル
        "outcome": outcome,

        # 機械学習用
        # 1 = MERGED
        # 0 = CLOSED
        "merged": merged,

        # ----------------------------------------------------
        # 数値メトリクス
        # ----------------------------------------------------

        # PRに含まれるコミット数
        "commit_count": pr.commits,

        # PRで変更されたファイル数
        "changed_files": pr.changed_files,

        # 追加された行数
        "additions": pr.additions,

        # 削除された行数
        "deletions": pr.deletions,

        # 総変更行数
        "changed_lines": pr.additions + pr.deletions,

        # PRタイトルの長さ
        "title_length": len(title),

        # PR本文の長さ
        "body_length": len(body),

        # 通常コメント数
        "comments": pr.comments,

        # コードレビューコメント数
        "review_comments": pr.review_comments,

        # ----------------------------------------------------
        # コミットメッセージ関連
        # ----------------------------------------------------

        "commit_message_total_length":
            commit_metrics["commit_message_total_length"],

        "commit_message_avg_length":
            commit_metrics["commit_message_avg_length"],

        "commit_message_max_length":
            commit_metrics["commit_message_max_length"],

        "commit_message_keyword_count":
            commit_metrics["commit_message_keyword_count"],

        # 元のコミットメッセージも残しておく
        "commit_messages":
            commit_metrics["commit_messages"],
    }

    rows.append(row)

    print(
        f"{len(rows):03d}/{TARGET_COUNT} "
        f"PR #{pr.number} "
        f"{outcome}"
    )

    # 必要件数に達したら終了
    if len(rows) >= TARGET_COUNT:
        break


# ============================================================
# 6. CSVとして保存
# ============================================================

df = pd.DataFrame(rows)

df.to_csv(
    OUTPUT_FILE,
    index=False,

    # Excelでも日本語が文字化けしにくい
    encoding="utf-8-sig",
)


# ============================================================
# 7. 取得結果を表示
# ============================================================

print()
print("=" * 60)
print("データセット作成完了")
print("=" * 60)

print("総PR数:", len(df))

print()
print("MERGED:")
print((df["merged"] == 1).sum())

print()
print("CLOSED:")
print((df["merged"] == 0).sum())

print()
print("保存先:", OUTPUT_FILE)


# GitHub API接続を閉じる
g.close()