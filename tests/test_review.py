from maintainerkit.review.analyzer import PRAnalyzer

def test_pr_review_risk_high_for_auth_without_tests():
    analyzer = PRAnalyzer()
    res = analyzer.analyze(
        pr_number=142,
        title="Refactor auth tokens",
        files_changed=["src/maintainerkit/auth/tokens.py"],
        lines_added=312,
        lines_removed=91
    )
    assert res.risk_level == "High"
    assert "security" in res.suggested_reviewers
    assert any("tests" in rf.lower() for rf in res.risk_factors)

def test_pr_review_low_risk():
    analyzer = PRAnalyzer()
    res = analyzer.analyze(
        pr_number=143,
        title="docs: update readme",
        files_changed=["README.md"],
        lines_added=10,
        lines_removed=2
    )
    assert res.risk_level == "Low"
