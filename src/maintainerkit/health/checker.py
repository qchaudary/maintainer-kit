"""Filesystem repository health auditor."""
import os
from maintainerkit.health.scoring import HealthReport

AUDIT_RULES = [
    ("License", ["LICENSE", "LICENSE.md", "LICENSE.txt"], 20, "Add an open-source LICENSE (e.g. MIT or Apache-2.0)."),
    ("Documentation (README)", ["README.md", "README.rst", "README"], 20, "Add a comprehensive README.md."),
    ("Security Policy", ["SECURITY.md", ".github/SECURITY.md"], 15, "Add a SECURITY.md vulnerability disclosure policy."),
    ("Contributing Guide", ["CONTRIBUTING.md", ".github/CONTRIBUTING.md"], 15, "Add a CONTRIBUTING.md guide for new maintainers."),
    ("Code of Conduct", ["CODE_OF_CONDUCT.md", ".github/CODE_OF_CONDUCT.md"], 10, "Add a CODE_OF_CONDUCT.md community covenant."),
    ("Issue Templates", [".github/ISSUE_TEMPLATE"], 10, "Add structured issue templates under .github/ISSUE_TEMPLATE."),
    ("Pull Request Template", [".github/pull_request_template.md", "pull_request_template.md"], 5, "Add a pull request review template."),
    ("CI Workflow", [".github/workflows"], 5, "Configure automated CI tests in .github/workflows."),
]

class HealthChecker:
    def __init__(self, root_dir: str = "."):
        self.root_dir = os.path.abspath(root_dir)

    def check(self) -> HealthReport:
        checks = {}
        recommendations = []
        score = 0

        for name, candidate_paths, points, rec in AUDIT_RULES:
            found = False
            for cpath in candidate_paths:
                full_p = os.path.join(self.root_dir, cpath)
                if os.path.exists(full_p):
                    found = True
                    break
            checks[name] = found
            if found:
                score += points
            else:
                recommendations.append(rec)

        return HealthReport(score=score, checks=checks, recommendations=recommendations)
