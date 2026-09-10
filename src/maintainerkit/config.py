"""Configuration management for MaintainerKit."""
import os
from dataclasses import dataclass

@dataclass
class Config:
    github_token: str | None = None
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"

    @classmethod
    def from_env(cls) -> "Config":
        return cls(
            github_token=os.environ.get("GITHUB_TOKEN"),
            openai_api_key=os.environ.get("OPENAI_API_KEY"),
            openai_model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
        )
