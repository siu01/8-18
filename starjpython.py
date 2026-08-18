import os
from dotenv import load_dotenv
from github import Github, Auth

load_dotenv()

token = os.getenv("GITHUB_TOKEN")
g = Github(auth=Auth.Token(token))

# GitHub全体をスター数の多い順に検索
repos = g.search_repositories(
    query="language:python stars:>0",
    sort="stars",
    order="desc"
)

# 上位10件
for i, repo in enumerate(repos[:10], start=1):
    print(f"{i}位")
    print("リポジトリ:", repo.full_name)
    print("Stars:", repo.stargazers_count)
    print("URL:", repo.html_url)
    print("言語:", repo.language)
    print("-" * 60)

g.close()