"""GitHub issues service integration."""
from typing import List, Dict, Any, Optional
from maintainerkit.github.client import GitHubClient

class IssueService:
    def __init__(self, client: Optional[GitHubClient] = None):
        self.client = client or GitHubClient()

    def get_issue(self, repo: str, issue_number: int) -> Optional[Dict[str, Any]]:
        return self.client.get(f"repos/{repo}/issues/{issue_number}")

    def post_issue_comment(self, repo: str, issue_number: int, comment: str) -> bool:
        resp = self.client.post(f"repos/{repo}/issues/{issue_number}/comments", {"body": comment})
        return resp is not None
