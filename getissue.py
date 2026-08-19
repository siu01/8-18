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
for issue in repo.get_issues():

    print("=" * 80)
    print("番号:", issue.number)
    print("タイトル:", issue.title)
    print("状態:", issue.state)
    print("作成者:", issue.user.login)
    print("作成日時:", issue.created_at)
    print("更新日時:", issue.updated_at)
    print("コメント数:", issue.comments)
    print("URL:", issue.html_url)
    print("本文:")
    print(issue.body)
g.close()