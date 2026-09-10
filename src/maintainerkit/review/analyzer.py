"""PR review preparation and risk analyzer."""
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from maintainerkit.review.checks import analyze_files_risk, check_test_coverage_presence
from maintainerkit.ai.provider import get_ai_provider

@dataclass
class PRReviewPreparation:
    pr_number: int
    title: str
    files_changed: List[str]
    lines_added: int
    lines_removed: int
    risk_level: str
    risk_factors: List[str]
    suggested_reviewers: List[str]
    checks_status: Dict[str, str]

class PRAnalyzer:
    def __init__(self, use_ai: bool = False):
        self.use_ai = use_ai
        self.ai_provider = get_ai_provider() if use_ai else None

    def analyze(
        self,
        pr_number: int,
        title: str,
        files_changed: List[str],
        lines_added: int = 0,
        lines_removed: int = 0,
    ) -> PRReviewPreparation:
        risks = analyze_files_risk(files_changed)
        risk_factors = []
        suggested_reviewers = []

        if "Authentication/Auth" in risks or "Security/Crypto" in risks:
            risk_factors.append("Authentication / Cryptographic logic modified")
            suggested_reviewers.append("security")
        if "Dependencies/Packaging" in risks:
            risk_factors.append("External dependency or packaging manifest touched")
            suggested_reviewers.append("devops")
        if "CI/CD Workflows" in risks:
            risk_factors.append("CI/CD pipeline configuration altered")
            suggested_reviewers.append("infra")

        tests_present = check_test_coverage_presence(files_changed)
        if not tests_present:
            risk_factors.append("Significant code changes detected without corresponding unit or integration tests")

        if len(files_changed) > 15 or (lines_added + lines_removed) > 500:
            risk_factors.append(f"Large change footprint ({len(files_changed)} files, +{lines_added}/-{lines_removed} lines)")

        # Risk scoring
        if "Authentication/Auth" in risks or "Security/Crypto" in risks or not tests_present:
            risk_level = "High"
        elif risk_factors:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        if not suggested_reviewers:
            suggested_reviewers = ["core-maintainer"]

        checks_status = {
            "Sensitive Files": "WARN" if risks else "PASS",
            "Tests Included": "PASS" if tests_present else "FAIL",
            "Footprint": "WARN" if (lines_added + lines_removed) > 500 else "PASS",
        }

        return PRReviewPreparation(
            pr_number=pr_number,
            title=title,
            files_changed=files_changed,
            lines_added=lines_added,
            lines_removed=lines_removed,
            risk_level=risk_level,
            risk_factors=risk_factors,
            suggested_reviewers=list(set(suggested_reviewers)),
            checks_status=checks_status,
        )
