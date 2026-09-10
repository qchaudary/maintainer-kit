"""OpenAI provider implementation for intelligent maintainer reasoning."""
import json
from typing import Dict, Any, Optional
from maintainerkit.ai.provider import AIProvider

class OpenAIProvider(AIProvider):
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self.api_key = api_key
        self.model = model

    def is_available(self) -> bool:
        return bool(self.api_key)

    def classify_issue(self, title: str, body: str) -> Optional[Dict[str, Any]]:
        try:
            import openai
            client = openai.OpenAI(api_key=self.api_key)
            prompt = (
                f"You are MaintainerKit, an assistant for open-source maintainers.\n"
                f"Analyze this GitHub issue:\n"
                f"Title: {title}\n"
                f"Body: {body}\n\n"
                f"Return valid JSON with keys:\n"
                f"- labels: list of suggested label strings\n"
                f"- priority: 'Critical', 'High', 'Medium', or 'Low'\n"
                f"- area: relevant component or module name\n"
                f"- summary: 1-sentence technical explanation\n"
                f"- action: recommended next action for the maintainer"
            )
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception:
            return None

    def analyze_pr(self, title: str, files_changed: list, diff_summary: str = "") -> Optional[Dict[str, Any]]:
        try:
            import openai
            client = openai.OpenAI(api_key=self.api_key)
            prompt = (
                f"Analyze this GitHub pull request for review readiness.\n"
                f"Title: {title}\n"
                f"Files changed: {files_changed}\n"
                f"Diff summary: {diff_summary}\n\n"
                f"Return valid JSON with keys:\n"
                f"- risk_level: 'High', 'Medium', or 'Low'\n"
                f"- risk_factors: list of specific risk items\n"
                f"- review_focus: what the human reviewer should scrutinize\n"
                f"- test_recommendations: what tests are needed"
            )
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception:
            return None
