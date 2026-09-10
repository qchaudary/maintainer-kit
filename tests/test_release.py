from maintainerkit.release.notes import ReleaseNotesGenerator, MergedPR

def test_release_notes_generation():
    gen = ReleaseNotesGenerator()
    prs = [
        MergedPR(1, "feat: issue triage", "qchaudary", labels=["feature"]),
        MergedPR(2, "fix: crash on empty body", "alice", labels=["bug"]),
    ]
    notes = gen.generate("v0.1.0", prs)
    assert "## [v0.1.0] - Release Notes" in notes
    assert "Features" in notes
    assert "Bug Fixes" in notes
    assert "@qchaudary" in notes
    assert "@alice" in notes
