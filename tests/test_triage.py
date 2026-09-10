from maintainerkit.triage.classifier import IssueClassifier

def test_triage_security_issue():
    classifier = IssueClassifier()
    res = classifier.classify("Critical SQL injection vulnerability in login API", "Found auth bypass")
    assert "security" in res.labels
    assert res.priority == "Critical"
    assert res.area == "Authentication"
    assert res.needs_maintainer_response is True

def test_triage_documentation():
    classifier = IssueClassifier()
    res = classifier.classify("Fix typo in docs and tutorial")
    assert "documentation" in res.labels
    assert res.priority == "Low"
