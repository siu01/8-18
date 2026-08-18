import os
from dotenv import load_dotenv
from github import Github, Auth

load_dotenv()

auth = Auth.Token(os.getenv("GITHUB_TOKEN"))
g = Github(auth=auth)

for repo in g.get_user().get_repos(affiliation="owner"):
    print(repo.name)

g.close()