"""Tests for web API."""

from fastapi.testclient import TestClient

from crochet_checker.web import app

client = TestClient(app)
P = (
    "Round 1: 6 sc into magic ring (6)"
    + chr(10)
    + "Round 2: (sc, inc) x 6 (18)"
    + chr(10)
    + "Round 3: (2 sc, inc) x 6 (24)"
)


class TestHealth:
    def test_health(self):
        r = client.get("/api/health")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"


class TestIndex:
    def test_index(self):
        r = client.get("/")
        assert r.status_code == 200
        assert "Crochet Pattern Checker" in r.text


class TestCheck:
    def test_check_valid(self):
        r = client.post("/api/check", json={"pattern_text": P})
        assert r.status_code == 200
        d = r.json()
        assert d["status"] in ["PASS", "PASS WITH WARNINGS", "NEEDS_REVIEW", "ERROR"]
        assert d["rounds"] >= 1

    def test_check_returns_measurements(self):
        r = client.post("/api/check", json={"pattern_text": P})
        d = r.json()
        assert "max_stitches" in d
        assert "max_diameter_inches" in d

    def test_check_invalid(self):
        r = client.post("/api/check", json={"pattern_text": "not a pattern"})
        assert r.status_code in [200, 400]


class TestRender:
    def test_render(self):
        r = client.post("/api/render", json={"pattern_text": P})
        assert r.status_code == 200
        assert "<svg" in r.json()["svg"]


class TestSimulate:
    def test_simulate(self):
        r = client.post("/api/simulate", json={"pattern_text": P})
        assert r.status_code == 200
        body = r.json()
        assert body["status"] == "success"
        assert body["shape"]
        assert body["vertices"] > 0
        assert body["faces"] > 0


class TestUpload:
    def test_upload(self):
        r = client.post(
            "/api/upload", files={"file": ("p.txt", P.encode(), "text/plain")}
        )
        assert r.status_code == 200
        assert r.json()["rounds"] == 3


class TestPdf:
    def test_pdf(self):
        r = client.post("/api/pdf", json={"pattern_text": P})
        assert r.status_code == 200
        assert "<!DOCTYPE html>" in r.json()["html"]


def test_check_json_uses_text_keys():
    import json
    from pathlib import Path

    from click.testing import CliRunner

    from crochet_checker.cli import cli

    path = Path(__file__).resolve().parents[2] / "examples" / "amigurumi.txt"
    result = CliRunner().invoke(cli, ["check", str(path), "--json"])
    assert result.exit_code == 0, result.output
    data = json.loads(result.output)
    assert data["overall_status"] == "PASS"
    assert data["stitch_counts"]
    assert all(isinstance(key, str) for key in data["stitch_counts"])


def test_pdf_accepts_sheet_options():
    response = client.post("/api/pdf", json={"pattern_text": P, "template": "berry", "page_size": "Letter", "include_charts": False})
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "success" and body["template"] == "berry" and body["page_size"] == "Letter"
    assert "#6B2D5B" in body["html"] and "Charts" not in body["html"]


def test_pdf_print_setup_does_not_restore_charts():
    response = client.post(
        "/api/pdf",
        json={
            "pattern_text": P,
            "template": "berry",
            "page_size": "Legal",
            "include_charts": False,
            "large_print": True,
            "landscape": True,
            "ink_saver": True,
            "binding": "left",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "success" and body["page_size"] == "Legal" and body["large_print"] is True
    html = body["html"]
    assert "Charts" not in html
    assert "large-print" in html and "Legal landscape" in html and "ink-saver" in html and "2.8cm" in html

def test_sheet_controls_are_on_the_page():
    page = client.get("/")
    assert page.status_code == 200
    assert "pdfLarge" in page.text and "Large print" in page.text and "pdfPage" in page.text


def test_pdf_advanced_options_do_not_restore_charts():
    response = client.post(
        "/api/pdf",
        json={"pattern_text": P, "include_charts": False, "duplex": True, "cards": True, "crop_marks": True},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "success" and body["duplex"] is True and body["cards"] is True
    html = body["html"]
    assert "Charts" not in html
    assert "counter(pages)" in html and "marks: crop cross" in html and "duplex" in html

def test_advanced_sheet_controls_are_on_the_page():
    page = client.get("/")
    assert page.status_code == 200
    assert "pdfDuplex" in page.text and "pdfCards" in page.text and "pdfCrop" in page.text
