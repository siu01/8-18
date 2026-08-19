import os
from datetime import datetime, timedelta, timezone, time
from dotenv import load_dotenv
from github import Github, Auth
import matplotlib.pyplot as plt

REPOSITORY = "apache/lucene"
DAYS = 7

# 日本時間
JST = timezone(timedelta(hours=9))
load_dotenv()

token = os.getenv("GITHUB_TOKEN")

if not token:
    raise ValueError("GITHUB_TOKEN がありません")

g = Github(auth=Auth.Token(token))

repo = g.get_repo(REPOSITORY)

print("Repository:", repo.full_name)


now_jst = datetime.now(JST)

end_date = now_jst.date()
start_date = end_date - timedelta(days=DAYS - 1)

# JSTの開始時刻
start_jst = datetime.combine(
    start_date,
    time.min,
    tzinfo=JST
)

# GitHub API用にUTCへ変換
start_utc = start_jst.astimezone(timezone.utc)


print("集計期間:")
print(start_date, "〜", end_date)
print()



dates = [
    start_date + timedelta(days=i)
    for i in range(DAYS)
]

issue_counts = {
    date: 0
    for date in dates
}



issues = repo.get_issues(
    state="all",
    since=start_utc
)

for issue in issues:

    # Pull Requestは除外
    if issue.pull_request is not None:
        continue

    created_at = issue.created_at

    # 古いPyGithub対策
    if created_at.tzinfo is None:
        created_at = created_at.replace(
            tzinfo=timezone.utc
        )

    # UTC → JST
    created_jst = created_at.astimezone(JST)

    issue_date = created_jst.date()

    # 直近7日のみ
    if start_date <= issue_date <= end_date:

        issue_counts[issue_date] += 1

        print(
            issue_date,
            f"#{issue.number}",
            issue.title
        )


g.close()

print()
print("=" * 60)
print("日別 Issue 報告数")
print("=" * 60)

for date, count in issue_counts.items():
    print(
        date.strftime("%Y-%m-%d"),
        ":",
        count
    )

labels = [
    date.strftime("%m/%d")
    for date in dates
]

values = [
    issue_counts[date]
    for date in dates
]

plt.figure(figsize=(10, 5))

bars = plt.bar(
    labels,
    values
)

plt.title(
    f"{REPOSITORY} - Issues created in the last {DAYS} days"
)

plt.xlabel("Date")
plt.ylabel("Number of Issues")

plt.grid(
    axis="y",
    linestyle="--",
    alpha=0.4
)

# 棒の上に件数表示
for bar, value in zip(bars, values):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.05,
        str(value),
        ha="center",
        va="bottom"
    )

plt.tight_layout()
plt.savefig(
    "issue_report.png",
    dpi=200
)

plt.show()