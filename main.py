from github import Github

# Authentication is defined via github.Auth
from github import Auth

# Using an access token
auth = Auth.Token("access_token")

# Public Web Github
g = Github(auth=auth)

# Github Enterprise with custom hostname
g = Github(auth=auth, base_url="https://{hostname}/api/v3")

# Use lazy mode (see https://pygithub.readthedocs.io/en/stable/examples/LazyMode.html)
g = Github(auth=auth, lazy=True)

# Set a Github API version (see https://docs.github.com/en/rest/about-the-rest-api/api-versions)
g = Github(auth=auth, api_version="2022-11-28")
