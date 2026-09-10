"""GitHub REST client wrapper."""
import os
import json
import urllib.request
import urllib.error
from typing import Dict, Any, Optional

class GitHubClient:
    def __init__(self, token: Optional[str] = None):
        self.token = token or os.environ.get("GITHUB_TOKEN")
        self.base_url = "https://api.github.com"

    def _request(self, endpoint: str) -> Optional[Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = {"User-Agent": "MaintainerKit", "Accept": "application/vnd.github.v3+json"}
        if self.token:
            headers["Authorization"] = f"token {self.token}"
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read().decode())
        except Exception:
            return None
