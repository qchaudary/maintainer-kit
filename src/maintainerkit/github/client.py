"""GitHub REST client wrapper supporting GET and POST."""
import os
import json
import urllib.request
import urllib.error
from typing import Dict, Any, Optional

class GitHubClient:
    def __init__(self, token: Optional[str] = None):
        self.token = token or os.environ.get("GITHUB_TOKEN")
        self.base_url = "https://api.github.com"

    def _request(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Optional[Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = {
            "User-Agent": "MaintainerKit/0.2.0",
            "Accept": "application/vnd.github.v3+json"
        }
        if self.token:
            headers["Authorization"] = f"token {self.token}"

        encoded_data = json.dumps(data).encode("utf-8") if data is not None else None
        req = urllib.request.Request(url, data=encoded_data, headers=headers)
        if data is not None:
            headers["Content-Type"] = "application/json"

        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            return None
        except Exception:
            return None

    def get(self, endpoint: str) -> Optional[Any]:
        return self._request(endpoint)

    def post(self, endpoint: str, data: Dict[str, Any]) -> Optional[Any]:
        return self._request(endpoint, data=data)
