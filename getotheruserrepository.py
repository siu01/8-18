import os
from dotenv import load_dotenv
from github import Github, Auth

load_dotenv()

token = os.getenv("GITHUB_TOKEN")

if not token:
    raise ValueError("GITHUB_TOKEN がありません")

g = Github(auth=Auth.Token(token))

# ↓ ここだけ好きな公開リポジトリに変更
repo = g.get_repo("GOROman/vibewatch")

print("Repository:", repo.full_name)
print()

for commit in repo.get_commits():

    print("=" * 80)

    print("SHA:", commit.sha)
    print("Author:", commit.commit.author.name)
    print("Date:", commit.commit.author.date)
    print("Message:", commit.commit.message)

    print("--- Changed files ---")

    for file in commit.files:
        print(
            file.filename,
            "|",
            file.status,
            "| +",
            file.additions,
            "| -",
            file.deletions
        )

g.close()