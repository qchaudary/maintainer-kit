import json

from maintainerkit.health.checker import HealthChecker


def test_health_check_local_repo():
    checker = HealthChecker(".")
    report = checker.check()
    assert report.score >= 80
    assert report.checks["License"] is True
    assert report.checks["Security Policy"] is True


def test_health_json_contains_granular_check_metadata():
    report = HealthChecker(".").check()
    payload = json.loads(report.to_json())

    assert payload["score"] == report.score
    assert payload["checks"]["License"] is True
    assert payload["evaluated_at"].endswith("Z")

    license_detail = payload["check_details"]["License"]
    assert license_detail["passed"] is True
    assert license_detail["points"] == 20
    assert license_detail["awarded_points"] == 20
    assert "LICENSE" in license_detail["candidate_paths"]
    assert license_detail["matched_path"] in {"LICENSE", "LICENSE.md", "LICENSE.txt"}


def test_health_check_details_preserve_score_weighting():
    report = HealthChecker(".").check()
    awarded = sum(item["awarded_points"] for item in report.check_details.values())
    possible = sum(item["points"] for item in report.check_details.values())

    assert awarded == report.score
    assert possible == 100
