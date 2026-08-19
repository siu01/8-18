# クローズをリジェクトとしてあつかう。
import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from github import Github, Auth


REPOSITORY = "apache/lucene"
DAYS = 30

load_dotenv()

token = os.getenv("GITHUB_TOKEN")

if not token:
    raise ValueError("GITHUB_TOKEN がありません")

g = Github(auth=Auth.Token(token))

repo = g.get_repo(REPOSITORY)

# 直近30日
now = datetime.now(timezone.utc)
start_date = (now - timedelta(days=DAYS)).date()

print("Repository:", repo.full_name)
print("集計開始日:", start_date)
print()

# GitHub Search APIで期間を限定
query = (
    f"repo:{REPOSITORY} "
    f"is:pr "
    f"is:closed "
    f"closed:>={start_date.isoformat()}"
)

results = g.search_issues(
    query=query,
    sort="updated",
    order="desc"
)

total = 0
merged = 0
rejected = 0

rejected_prs = []

for issue in results:

    # Issue検索結果からPR本体を取得
    pr = repo.get_pull(issue.number)

    total += 1

    if pr.merged_at is not None:
        merged += 1

    else:
        rejected += 1

        rejected_prs.append(
            {
                "number": pr.number,
                "title": pr.title,
                "user": pr.user.login,
                "closed_at": pr.closed_at,
                "url": pr.html_url,
            }
        )


print("=" * 60)
print(f"直近 {DAYS} 日間")
print("=" * 60)

print("クローズされたPR:", total)
print("マージ:", merged)
print("未マージでクローズ:", rejected)

if total > 0:
    merge_rate = merged / total * 100
    rejection_rate = rejected / total * 100

    print()
    print(f"マージ率: {merge_rate:.1f}%")
    print(f"リジェクト相当率: {rejection_rate:.1f}%")

print()
print("=" * 60)
print("未マージでクローズされたPR")
print("=" * 60)

for pr in rejected_prs:

    print(
        f"#{pr['number']} "
        f"{pr['title']} "
        f"by {pr['user']}"
    )

    print("closed:", pr["closed_at"])
    print("URL:", pr["url"])
    print()

g.close()