"""Scoring engine for repository health audits."""
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Any


def _utc_now_iso() -> str:
    """Return an ISO 8601 UTC timestamp suitable for machine-readable output."""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


@dataclass
class HealthReport:
    score: int
    checks: Dict[str, bool]
    recommendations: List[str]
    check_details: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    evaluated_at: str = field(default_factory=_utc_now_iso)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "score": self.score,
            "checks": self.checks,
            "check_details": self.check_details,
            "recommendations": self.recommendations,
            "evaluated_at": self.evaluated_at,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

    def render(self) -> str:
        lines = [
            "Repository Health Report",
            "----------------------------------------",
        ]
        for name, passed in self.checks.items():
            status = "[PASS]" if passed else "[FAIL]"
            lines.append(f"{name:<25} {status}")
        lines.append("----------------------------------------")
        lines.append(f"Overall Score: {self.score}/100")
        if self.recommendations:
            lines.append("\nRecommendations:")
            for rec in self.recommendations:
                lines.append(f"  * {rec}")
        return "\n".join(lines)
