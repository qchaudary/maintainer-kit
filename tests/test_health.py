from maintainerkit.health.checker import HealthChecker

def test_health_check_local_repo():
    checker = HealthChecker(".")
    report = checker.check()
    assert report.score >= 80
    assert report.checks["License"] is True
    assert report.checks["Security Policy"] is True
