"""GitHub PR integration."""
from maintainerkit.github.client import GitHubClient

class PRService:
    def __init__(self, client: GitHubClient):
        self.client = client

    def get_pr_files(self, repo: str, pr_number: int):
        return self.client._request(f"repos/{repo}/pulls/{pr_number}/files")
