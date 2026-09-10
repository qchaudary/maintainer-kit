"""Issue classifier combining heuristics with optional AI."""
from dataclasses import dataclass, field
from typing import List, Optional
from maintainerkit.triage.rules import detect_labels, detect_area, evaluate_priority
from maintainerkit.ai.provider import get_ai_provider

@dataclass
class TriageResult:
    title: str
    labels: List[str]
    area: str
    priority: str
    needs_maintainer_response: bool
    summary: str
    suggested_action: str

class IssueClassifier:
    def __init__(self, use_ai: bool = False):
        self.use_ai = use_ai
        self.ai_provider = get_ai_provider() if use_ai else None

    def classify(self, title: str, body: str = "") -> TriageResult:
        full_text = f"{title}\n{body}".strip()
        labels = detect_labels(full_text)
        area = detect_area(full_text)
        priority = evaluate_priority(full_text, labels)
        needs_response = priority in ["Critical", "High"] or "needs-information" in labels or "bug" in labels

        # If AI is enabled and ready, enrich the summary
        summary = f"Issue in {area} classified with priority {priority}."
        action = f"Apply labels [{', '.join(labels)}] and assign to {area} team."
        if self.ai_provider and self.ai_provider.is_available():
            ai_data = self.ai_provider.classify_issue(title, body)
            if ai_data:
                labels = list(set(labels + ai_data.get("labels", [])))
                priority = ai_data.get("priority", priority)
                summary = ai_data.get("summary", summary)
                action = ai_data.get("action", action)

        return TriageResult(
            title=title,
            labels=labels,
            area=area,
            priority=priority,
            needs_maintainer_response=needs_response,
            summary=summary,
            suggested_action=action
        )
