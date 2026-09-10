"""GitHub release integration."""
from maintainerkit.github.client import GitHubClient

class ReleaseService:
    def __init__(self, client: GitHubClient):
        self.client = client

    def get_latest_release(self, repo: str):
        return self.client._request(f"repos/{repo}/releases/latest")
