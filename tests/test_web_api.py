"""API tests for the new calculator/conversion/report endpoints."""

from fastapi.testclient import TestClient

from crochet_checker.web.app import app

client = TestClient(app)

GOOD = """Round 1: 6 sc into magic ring (6)
Round 2: inc x 6 (12)
Round 3: (sc, inc) x 6 (18)
Round 4: (2 sc, inc) x 6 (24)
"""


def test_health_version_matches_package():
    from crochet_checker import __version__

    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["version"] == __version__


def test_version_endpoint():
    response = client.get("/api/version")
    assert response.status_code == 200
    assert response.json()["name"] == "crochet-pattern-checker"


def test_gauge_endpoint():
    response = client.post(
        "/api/gauge",
        json={"stitches": 40, "rows": 40, "sts_per_4in": 20, "rows_per_4in": 20},
    )
    assert response.status_code == 200
    assert response.json()["width_in"] == 8.0


def test_gauge_endpoint_rejects_zero():
    response = client.post(
        "/api/gauge",
        json={"stitches": 0, "rows": 40, "sts_per_4in": 20, "rows_per_4in": 20},
    )
    assert response.status_code == 422


def test_convert_endpoint():
    response = client.post(
        "/api/convert", json={"pattern_text": "6 sc, 2 hdc", "direction": "us-to-uk"}
    )
    assert response.status_code == 200
    assert "6 dc" in response.json()["converted"]


def test_yarn_endpoint():
    response = client.post("/api/yarn", json={"total_stitches": 1000, "stitch": "sc"})
    assert response.status_code == 200
    assert response.json()["yards"] > 0


def test_chart_endpoint():
    response = client.post("/api/chart", json={"counts": [6, 12, 18]})
    assert response.status_code == 200
    body = response.json()
    assert body["chart"][-1]["stitches"] == 18
    assert body["shape"] == "bowl"


def test_chart_endpoint_rejects_negative_counts():
    response = client.post("/api/chart", json={"counts": [6, -2]})
    assert response.status_code == 422


def test_hooks_endpoint():
    response = client.get("/api/hooks", params={"weight": "worsted"})
    assert response.status_code == 200
    body = response.json()
    assert body["weight_number"] == 4
    assert body["hook_mm_low"] == 5.5


def test_report_endpoint():
    response = client.post("/api/report", json={"pattern_text": GOOD})
    assert response.status_code == 200
    body = response.json()
    assert "html" in body
    assert body["chart"]
    assert body["status"] in ("PASS", "PASS_WITH_WARNINGS")


def test_check_endpoint_still_works():
    response = client.post("/api/check", json={"pattern_text": GOOD})
    assert response.status_code == 200
    assert response.json()["status"] in ("PASS", "PASS_WITH_WARNINGS")


def test_frontend_serves_new_tabs():
    response = client.get("/")
    assert response.status_code == 200
    html = response.text
    assert "Gauge" in html
    assert "US â†” UK" in html
    assert "Report" in html
