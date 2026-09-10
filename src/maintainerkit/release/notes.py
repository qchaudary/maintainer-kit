"""Semantic release notes and changelog generator."""
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class MergedPR:
    number: int
    title: str
    author: str
    category: str = "Other"
    labels: List[str] = field(default_factory=list)

class ReleaseNotesGenerator:
    def categorize_pr(self, title: str, labels: List[str]) -> str:
        title_lower = title.lower()
        if "security" in labels or "sec" in title_lower or "cve" in title_lower:
            return "Security"
        if "feat" in title_lower or "feature" in labels or title_lower.startswith("feat"):
            return "Features"
        if "fix" in title_lower or "bug" in labels or title_lower.startswith("fix"):
            return "Bug Fixes"
        if "doc" in title_lower or "docs" in labels:
            return "Documentation"
        if "refactor" in title_lower or "perf" in title_lower:
            return "Improvements"
        return "Internal & Chores"

    def generate(self, version: str, merged_prs: List[MergedPR]) -> str:
        categories: Dict[str, List[str]] = {
            "Features": [],
            "Bug Fixes": [],
            "Security": [],
            "Improvements": [],
            "Documentation": [],
            "Internal & Chores": [],
        }
        contributors = set()

        for pr in merged_prs:
            cat = self.categorize_pr(pr.title, pr.labels)
            categories.setdefault(cat, []).append(f"- {pr.title} ([#{pr.number}](https://github.com/qchaudary/maintainer-kit/pull/{pr.number})) by @{pr.author}")
            contributors.add(f"@{pr.author}")

        lines = [f"## [{version}] - Release Notes\n"]
        for section, items in categories.items():
            if items:
                lines.append(f"### {section}")
                lines.extend(items)
                lines.append("")

        lines.append("### Contributors")
        lines.append(f"Thanks to everyone who contributed to this release: {', '.join(sorted(contributors))}\n")

        return "\n".join(lines)
