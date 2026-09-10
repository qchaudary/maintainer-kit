"""AI provider interface with local deterministic fallback."""
import os
from typing import Dict, Any, Optional

class AIProvider:
    def is_available(self) -> bool:
        return False

    def classify_issue(self, title: str, body: str) -> Optional[Dict[str, Any]]:
        return None

def get_ai_provider() -> AIProvider:
    key = os.environ.get("OPENAI_API_KEY")
    if key:
        from maintainerkit.ai.openai import OpenAIProvider
        return OpenAIProvider(key)
    return AIProvider()
