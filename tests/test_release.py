from maintainerkit.release.notes import ReleaseNotesGenerator, MergedPR

def test_release_notes_generation_from_prs():
    gen = ReleaseNotesGenerator()
    prs = [
        MergedPR(1, "feat: issue triage classification", "qchaudary", labels=["feature"]),
        MergedPR(2, "fix: crash on empty body", "alice", labels=["bug"]),
        MergedPR(3, "sec: harden input validation", "bob", labels=["security"]),
    ]
    notes = gen.generate("v0.2.0", prs, repo="qchaudary/maintainer-kit")
    assert "## [v0.2.0] - Release Notes" in notes
    assert "Features" in notes
    assert "Bug Fixes" in notes
    assert "Security" in notes
    assert "@qchaudary" in notes
    assert "https://github.com/qchaudary/maintainer-kit/pull/1" in notes

def test_release_categorization():
    gen = ReleaseNotesGenerator()
    assert gen.categorize_pr("feat: add new CLI", []) == "Features"
    assert gen.categorize_pr("fix: regex bug", []) == "Bug Fixes"
    assert gen.categorize_pr("docs: update README", []) == "Documentation"
    assert gen.categorize_pr("ci: add matrix test", []) == "CI & Infrastructure"
