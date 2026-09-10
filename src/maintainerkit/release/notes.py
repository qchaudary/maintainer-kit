"""Semantic release notes and changelog generator."""
import subprocess
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from maintainerkit.github.pull_requests import PRService

@dataclass
class MergedPR:
    number: int
    title: str
    author: str
    category: str = "Other"
    labels: List[str] = field(default_factory=list)

class ReleaseNotesGenerator:
    def categorize_pr(self, title: str, labels: Optional[List[str]] = None) -> str:
        labels = labels or []
        title_lower = title.lower()
        if any(lbl in ["security", "cve", "vulnerability"] for lbl in labels) or "sec:" in title_lower or "security" in title_lower:
            return "Security"
        if any(lbl in ["feature", "enhancement"] for lbl in labels) or title_lower.startswith("feat"):
            return "Features"
        if any(lbl in ["bug", "fix"] for lbl in labels) or title_lower.startswith("fix"):
            return "Bug Fixes"
        if any(lbl in ["docs", "documentation"] for lbl in labels) or title_lower.startswith("docs"):
            return "Documentation"
        if any(lbl in ["ci", "infra", "build"] for lbl in labels) or title_lower.startswith("ci"):
            return "CI & Infrastructure"
        if title_lower.startswith("refactor") or title_lower.startswith("perf"):
            return "Improvements"
        return "Internal & Chores"

    def fetch_live_prs(self, repo: str) -> List[MergedPR]:
        svc = PRService()
        raw_prs = svc.get_merged_prs(repo)
        results = []
        for p in raw_prs:
            labels = [lbl.get("name", "").lower() for lbl in p.get("labels", [])]
            author = p.get("user", {}).get("login", "contributor")
            results.append(MergedPR(
                number=p.get("number", 0),
                title=p.get("title", "Update"),
                author=author,
                labels=labels
            ))
        return results

    def fetch_local_git_commits(self, since_ref: Optional[str] = None) -> List[MergedPR]:
        try:
            cmd = ["git", "log", "--oneline", "-n", "30"]
            if since_ref:
                cmd = ["git", "log", f"{since_ref}..HEAD", "--oneline"]
            output = subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL)
            commits = []
            for i, line in enumerate(output.strip().splitlines(), start=1):
                parts = line.strip().split(" ", 1)
                if len(parts) == 2:
                    commits.append(MergedPR(
                        number=i,
                        title=parts[1],
                        author="maintainer",
                        labels=[]
                    ))
            return commits
        except Exception:
            return []

    def generate(self, version: str, merged_prs: List[MergedPR], repo: str = "qchaudary/maintainer-kit") -> str:
        categories: Dict[str, List[str]] = {
            "Features": [],
            "Bug Fixes": [],
            "Security": [],
            "Improvements": [],
            "CI & Infrastructure": [],
            "Documentation": [],
            "Internal & Chores": [],
        }
        contributors = set()

        for pr in merged_prs:
            cat = self.categorize_pr(pr.title, pr.labels)
            pr_ref = f"[#{pr.number}](https://github.com/{repo}/pull/{pr.number})" if pr.number > 0 else ""
            line = f"- {pr.title} ({pr_ref}) by @{pr.author}".replace(" ()", "")
            categories.setdefault(cat, []).append(line)
            contributors.add(f"@{pr.author}")

        lines = [f"## [{version}] - Release Notes\n"]
        for section, items in categories.items():
            if items:
                lines.append(f"### {section}")
                lines.extend(items)
                lines.append("")

        if contributors:
            lines.append("### Contributors")
            lines.append(f"Thanks to all contributors: {', '.join(sorted(contributors))}\n")

        return "\n".join(lines)
