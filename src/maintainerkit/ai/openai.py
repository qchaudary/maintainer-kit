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
                f"Classify this GitHub issue.\nTitle: {title}\nBody: {body}\n"
                "Return JSON with: labels (list of strings), priority (Critical, High, Medium, Low), "
                "summary (string), action (string)."
            )
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception:
            return None
