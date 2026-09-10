"""Deterministic heuristics for issue triage."""
import re
from typing import List, Dict, Any

KEYWORD_RULES = {
    "security": [r"cve-", r"vulnerability", r"exploit", r"injection", r"xss", r"auth bypass", r"buffer overflow"],
    "bug": [r"crash", r"exception", r"error", r"fails", r"traceback", r"broken", r"regression"],
    "feature": [r"feature request", r"proposal", r"add support", r"enhancement", r"allow user to"],
    "documentation": [r"docs?", r"readme", r"typo", r"tutorial", r"guide", r"explanation"],
    "question": [r"how to", r"how do i", r"is it possible", r"help wanted", r"question"],
}

AREA_RULES = {
    "Authentication": [r"auth", r"token", r"login", r"jwt", r"oauth", r"session", r"password"],
    "CLI": [r"cli", r"command line", r"argument", r"flag", r"terminal"],
    "API": [r"api", r"endpoint", r"rest", r"graphql", r"http", r"status code"],
    "Dependencies": [r"pip", r"dependency", r"package", r"requirements", r"version mismatch"],
    "CI/CD": [r"github action", r"workflow", r"pipeline", r"runner"],
}

def detect_labels(text: str) -> List[str]:
    text_lower = text.lower()
    matched = []
    for label, patterns in KEYWORD_RULES.items():
        for pat in patterns:
            if re.search(pat, text_lower):
                matched.append(label)
                break
    return matched or ["needs-triage"]

def detect_area(text: str) -> str:
    text_lower = text.lower()
    for area, patterns in AREA_RULES.items():
        for pat in patterns:
            if re.search(pat, text_lower):
                return area
    return "General"

def evaluate_priority(text: str, labels: List[str]) -> str:
    text_lower = text.lower()
    if "security" in labels or "data loss" in text_lower or "segfault" in text_lower:
        return "Critical"
    if "crash" in text_lower or "broken in production" in text_lower or "regression" in text_lower:
        return "High"
    if "bug" in labels:
        return "Medium"
    return "Low"
