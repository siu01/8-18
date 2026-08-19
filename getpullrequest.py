import os
from dotenv import load_dotenv
from github import Github, Auth

load_dotenv()

token = os.getenv("GITHUB_TOKEN")

if not token:
    raise ValueError("GITHUB_TOKEN がありません")

g = Github(auth=Auth.Token(token))

repo = g.get_repo("apache/lucene")

print("Repository:", repo.full_name)
print()

for pr in repo.get_pulls(
    state="all",
    sort="created",
    direction="desc"
):

    print("=" * 80)

    print("PR番号:", pr.number)
    print("タイトル:", pr.title)
    print("状態:", pr.state)

    print("作成者:", pr.user.login)

    print("作成日時:", pr.created_at)
    print("更新日時:", pr.updated_at)
    print("クローズ日時:", pr.closed_at)
    print("マージ日時:", pr.merged_at)

    print("マージ済み:", pr.merged)

    print("元ブランチ:", pr.head.ref)
    print("マージ先:", pr.base.ref)

    print("コミット数:", pr.commits)
    print("変更ファイル数:", pr.changed_files)

    print("追加行数:", pr.additions)
    print("削除行数:", pr.deletions)

    print("コメント数:", pr.comments)
    print("レビューコメント数:", pr.review_comments)

    print("URL:", pr.html_url)

    print("本文:")
    print(pr.body)

g.close()