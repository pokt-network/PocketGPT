import re

import requests


def get_github_issue_description(issue_url):
    # Extract the issue number from the URL using regular expressions
    match = re.search(r"https://github.com/([^/]+)/([^/]+)/issues/(\d+)", issue_url)
    if not match:
        raise ValueError("Invalid GitHub issue URL")

    # Extract the repository owner, name, and issue number from the URL
    owner = match.group(1)
    repo = match.group(2)
    issue_number = int(match.group(3))

    # Make an HTTP request to the GitHub API to fetch the issue details
    response = requests.get(
        f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"
    )
    response.raise_for_status()

    # Extract the description from the issue details and return it
    return response.json()["body"]


if __name__ == "__main__":
    url = "https://github.com/pokt-network/pocket/issues/551"
    print(get_github_issue_description(url))
