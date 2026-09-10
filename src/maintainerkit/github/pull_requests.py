"""GitHub PR service integration."""
from typing import List, Dict, Any, Optional
from maintainerkit.github.client import GitHubClient

class PRService:
    def __init__(self, client: Optional[GitHubClient] = None):
        self.client = client or GitHubClient()

    def get_pr(self, repo: str, pr_number: int) -> Optional[Dict[str, Any]]:
        return self.client.get(f"repos/{repo}/pulls/{pr_number}")

    def get_pr_files(self, repo: str, pr_number: int) -> List[Dict[str, Any]]:
        files = self.client.get(f"repos/{repo}/pulls/{pr_number}/files")
        return files if isinstance(files, list) else []

    def get_merged_prs(self, repo: str, state: str = "closed", limit: int = 50) -> List[Dict[str, Any]]:
        endpoint = f"repos/{repo}/pulls?state={state}&sort=updated&direction=desc&per_page={limit}"
        prs = self.client.get(endpoint)
        if not isinstance(prs, list):
            return []
        return [pr for pr in prs if pr.get("merged_at")]

    def post_pr_comment(self, repo: str, pr_number: int, comment: str) -> bool:
        resp = self.client.post(f"repos/{repo}/issues/{pr_number}/comments", {"body": comment})
        return resp is not None
