"""Risk and security sensitive checks for PR reviews."""
import re
from typing import List, Dict

SENSITIVE_PATTERNS = {
    "Authentication/Auth": [r"auth", r"token", r"jwt", r"session", r"oauth", r"password", r"credential"],
    "Security/Crypto": [r"crypto", r"hash", r"secret", r"key", r"cert", r"encrypt"],
    "CI/CD Workflows": [r"\.github/workflows", r"\.circleci", r"Dockerfile", r"Jenkinsfile"],
    "Dependencies/Packaging": [r"requirements\.txt", r"package\.json", r"pyproject\.toml", r"go\.mod", r"Cargo\.toml"],
}

def analyze_files_risk(files_changed: List[str]) -> Dict[str, List[str]]:
    risks = {}
    for filepath in files_changed:
        for risk_category, patterns in SENSITIVE_PATTERNS.items():
            for pat in patterns:
                if re.search(pat, filepath, re.IGNORECASE):
                    risks.setdefault(risk_category, []).append(filepath)
                    break
    return risks

def check_test_coverage_presence(files_changed: List[str]) -> bool:
    has_code = any(f.endswith((".py", ".ts", ".js", ".go", ".rs")) and not f.startswith("tests/") for f in files_changed)
    has_tests = any("test" in f.lower() or "spec" in f.lower() for f in files_changed)
    if has_code and not has_tests:
        return False
    return True
