import os
from dotenv import load_dotenv
from github import Github, Auth

load_dotenv()

token = os.getenv("GITHUB_TOKEN")

g = Github(auth=Auth.Token(token))

repo = g.get_repo("siu01/otel-ios-reliability-lab")

for commit in repo.get_commits():

    print("=" * 80)
    print("SHA:", commit.sha)
    print("Message:", commit.commit.message)

    for file in commit.files:
        print("ファイル:", file.filename)
        print("状態:", file.status)
        print("追加:", file.additions)
        print("削除:", file.deletions)
        print()

g.close()