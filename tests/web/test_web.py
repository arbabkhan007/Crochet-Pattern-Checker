"""Tests for web API."""
from fastapi.testclient import TestClient
from crochet_checker.web import app

client = TestClient(app)
P = "Round 1: 6 sc into magic ring (6)" + chr(10) + "Round 2: (sc, inc) x 6 (18)" + chr(10) + "Round 3: (2 sc, inc) x 6 (24)"

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
        assert r.status_code in [200, 400]
        if r.status_code == 200:
            assert r.json()["status"] == "success"

class TestUpload:
    def test_upload(self):
        r = client.post("/api/upload", files={"file": ("p.txt", P.encode(), "text/plain")})
        assert r.status_code == 200
        assert r.json()["rounds"] == 3

class TestPdf:
    def test_pdf(self):
        r = client.post("/api/pdf", json={"pattern_text": P})
        assert r.status_code == 200
        assert "<!DOCTYPE html>" in r.json()["html"]
