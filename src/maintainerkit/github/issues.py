"""GitHub issues integration."""
from maintainerkit.github.client import GitHubClient

class IssueService:
    def __init__(self, client: GitHubClient):
        self.client = client

    def get_issue(self, repo: str, issue_number: int):
        return self.client._request(f"repos/{repo}/issues/{issue_number}")
