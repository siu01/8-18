import os
from datetime import datetime, timedelta, timezone
from collections import Counter

from dotenv import load_dotenv
from github import Github, Auth

import matplotlib.pyplot as plt


REPOSITORY = "apache/lucene"
DAYS = 30

load_dotenv()

token = os.getenv("GITHUB_TOKEN")

if not token:
    raise ValueError("GITHUB_TOKEN がありません")

g = Github(auth=Auth.Token(token))

repo = g.get_repo(REPOSITORY)

print("Repository:", repo.full_name)


# =========================
# 集計開始日時
# =========================

now = datetime.now(timezone.utc)
start_date = now - timedelta(days=DAYS)

print("集計期間:")
print(start_date, "～", now)
print()


# =========================
# Workflow Run取得
# =========================

runs = repo.get_workflow_runs(
    status="completed"
)

results = []

for run in runs:

    created_at = run.created_at

    if created_at.tzinfo is None:
        created_at = created_at.replace(
            tzinfo=timezone.utc
        )

    # 30日より古いものは対象外
    if created_at < start_date:
        continue

    results.append(run)

    print(
        run.id,
        run.event,
        run.conclusion,
        run.created_at,
        run.html_url
    )


# =========================
# 結果集計
# =========================

conclusions = Counter(
    run.conclusion
    for run in results
)

total = len(results)

success = conclusions["success"]
failure = conclusions["failure"]
cancelled = conclusions["cancelled"]
timed_out = conclusions["timed_out"]
skipped = conclusions["skipped"]
neutral = conclusions["neutral"]


print()
print("=" * 60)
print("GitHub Actions 集計")
print("=" * 60)

print("総実行数:", total)
print("成功:", success)
print("失敗:", failure)
print("キャンセル:", cancelled)
print("タイムアウト:", timed_out)
print("スキップ:", skipped)
print("Neutral:", neutral)


# =========================
# 失敗率
# =========================

if total > 0:

    failure_rate = failure / total * 100

    print()
    print(
        f"単純ビルド失敗率: {failure_rate:.2f}%"
    )


# =========================
# 成功 vs 失敗だけで計算
# =========================

decided_runs = success + failure

if decided_runs > 0:

    pure_failure_rate = (
        failure / decided_runs * 100
    )

    print(
        f"成功/失敗のみで計算した失敗率: "
        f"{pure_failure_rate:.2f}%"
    )


# =========================
# 運用上の失敗
# failure + timed_out
# =========================

operational_failures = (
    failure
    + timed_out
)

if total > 0:

    operational_failure_rate = (
        operational_failures
        / total
        * 100
    )

    print(
        f"運用上の失敗率: "
        f"{operational_failure_rate:.2f}%"
    )



g.close()