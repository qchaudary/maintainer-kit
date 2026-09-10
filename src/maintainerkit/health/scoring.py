"""Scoring engine for repository health audits."""
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class HealthReport:
    score: int
    checks: Dict[str, bool]
    recommendations: List[str]

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
