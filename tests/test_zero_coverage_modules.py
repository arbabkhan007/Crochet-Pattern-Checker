"""
Targeted tests for previously untested (0% coverage) production modules.

Covers:
- parser.normalizer
- enterprise.security / enterprise.api (REST integration + security)
- validation.abbreviations / consistency / terminology / multi_piece / multipiece / row_transitions
- reporter.fallback / reporter.patcher
- utils.special_constructions / utils.category_detector
- api.rest / ast.ast_builder / batch.processor / compute.capabilities
- interactive.stitch_counter / optimization.pattern_optimizer
- visualization.diagram / stitch_chart / pattern_debugger
- pdf.image_support / yarn.substitution
- analysis.* (complexity, gauge, scaler, time, yarn)
"""

from __future__ import annotations

import os
import struct
import time
import zlib

import pytest

from fastapi import HTTPException
from fastapi.testclient import TestClient

from crochet_checker.model.instruction import Instruction, ParsedOperation
from crochet_checker.model.pattern import Pattern, PatternMetadata, PatternPiece
from crochet_checker.model.row import Round, Row
from crochet_checker.model.stitch import StitchType
from crochet_checker.parser.parser import parse_pattern
from crochet_checker.validation import validate_pattern


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

VALID_PATTERN = (
    "Round 1: 6 sc into magic ring (6)\n"
    "Round 2: inc x 6 (12)\n"
    "Round 3: (sc, inc) x 6 (18)\n"
    "Round 4: (2 sc, inc) x 6 (24)"
)

BAD_PATTERN = (
    "Round 1: 6 sc into magic ring (6)\n"
    "Round 2: (sc, inc) x 7 (18)"
)


def make_png(width: int = 100, height: int = 100, rgb=(255, 255, 255)) -> bytes:
    """Build a valid RGB PNG without relying on Pillow."""

    def chunk(tag: bytes, data: bytes) -> bytes:
        c = tag + data
        return (
            struct.pack(">I", len(data))
            + c
            + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)
        )

    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    row = b"\x00" + bytes(rgb) * width
    idat = zlib.compress(row * height)
    return sig + chunk(b"IHDR", ihdr) + chunk(b"IDAT", idat) + chunk(b"IEND", b"")


def sc_round(number: int, count: int) -> Round:
    return Round(
        round_number=number,
        instructions=[
            Instruction(
                source_text=f"{count} sc",
                operations=[
                    ParsedOperation(stitch_type=StitchType.SINGLE_CROCHET, count=count)
                ],
            )
        ],
    )


# ---------------------------------------------------------------------------
# parser.normalizer
# ---------------------------------------------------------------------------


class TestPatternNormalizer:
    def test_whitespace_normalization(self):
        n = __import__(
            "crochet_checker.parser.normalizer", fromlist=["PatternNormalizer"]
        ).PatternNormalizer()
        assert n.normalize("a\tb") == "a b"
        assert n.normalize("a  b") == "a b"
        assert n.normalize("a\r\nb") == "a\nb"
        assert n.normalize("x  \n") == "x\n"

    def test_symbol_normalization(self):
        from crochet_checker.parser.normalizer import PatternNormalizer

        n = PatternNormalizer()
        assert n.normalize("2 \u00d7 3") == "2 x 3"
        assert n.normalize("a \u2013 b") == "a - b"
        assert n.normalize("a \u2014 b") == "a - b"
        # Straight quotes pass through unchanged.
        assert n.normalize('"quote"') == '"quote"'
        assert n.normalize("'single'") == "'single'"

    def test_abbreviation_normalization(self):
        from crochet_checker.parser.normalizer import PatternNormalizer

        n = PatternNormalizer()
        assert n.normalize("2sc in next") == "inc in next"
        assert n.normalize("ss in next") == "sl st in next"
        assert n.normalize("m.r. join") == "MR. join"
        assert n.normalize("M.R. join") == "MR. join"

    def test_case_preserved(self):
        from crochet_checker.parser.normalizer import PatternNormalizer

        n = PatternNormalizer()
        assert n.normalize("Sc Dc") == "Sc Dc"

    def test_detect_dialect(self):
        from crochet_checker.parser.normalizer import PatternNormalizer, TerminologyDialect

        n = PatternNormalizer()
        assert n.detect_dialect("single crochet, hdc") == TerminologyDialect.US
        assert n.detect_dialect("double crochet, treble crochet") == TerminologyDialect.UK
        assert n.detect_dialect("") == TerminologyDialect.US

    def test_get_normalizations(self):
        from crochet_checker.parser.normalizer import PatternNormalizer

        n = PatternNormalizer()
        assert n.get_normalizations() == []

    def test_normalize_pattern_convenience(self):
        from crochet_checker.parser.normalizer import normalize_pattern

        assert normalize_pattern("a\tb") == "a b"

    def test_dialect_mappings(self):
        from crochet_checker.parser.normalizer import US_TO_UK, UK_TO_US

        assert US_TO_UK["sc"] == "dc"
        assert US_TO_UK["single crochet"] == "double crochet"
        assert UK_TO_US["dc"] == "sc"
        assert UK_TO_US["double crochet"] == "single crochet"


# ---------------------------------------------------------------------------
# enterprise.security
# ---------------------------------------------------------------------------


class TestRateLimiter:
    def test_allows_until_limit_then_429(self):
        from crochet_checker.enterprise.security import RateLimiter

        limiter = RateLimiter(max_requests=2, window_seconds=60)
        limiter.check("a")
        limiter.check("a")
        with pytest.raises(HTTPException) as exc:
            limiter.check("a")
        assert exc.value.status_code == 429

    def test_prunes_stale_requests(self):
        from crochet_checker.enterprise.security import RateLimiter

        limiter = RateLimiter(max_requests=2, window_seconds=60)
        limiter.requests["tester"].append(time.monotonic() - 999)
        limiter.check("tester")  # prunes stale entry first
        limiter.check("tester")
        with pytest.raises(HTTPException):
            limiter.check("tester")


class TestRequireApiKey:
    def test_development_when_unset(self, monkeypatch):
        from crochet_checker.enterprise.security import require_api_key

        monkeypatch.delenv("CROCHET_API_KEY", raising=False)
        assert require_api_key() == "development"
        assert require_api_key("whatever") == "development"

    def test_authenticated_with_correct_key(self, monkeypatch):
        from crochet_checker.enterprise.security import require_api_key

        monkeypatch.setenv("CROCHET_API_KEY", "sekret")
        assert require_api_key("sekret") == "authenticated"

    def test_rejects_wrong_or_missing_key(self, monkeypatch):
        from crochet_checker.enterprise.security import require_api_key

        monkeypatch.setenv("CROCHET_API_KEY", "sekret")
        with pytest.raises(HTTPException) as exc:
            require_api_key("nope")
        assert exc.value.status_code == 401
        with pytest.raises(HTTPException) as exc:
            require_api_key()
        assert exc.value.status_code == 401


# ---------------------------------------------------------------------------
# enterprise.api (REST integration + security)
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def api_client():
    from crochet_checker.enterprise.api import app

    return TestClient(app)


class TestEnterpriseAPI:
    def test_health(self, api_client):
        resp = api_client.get("/health")
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "healthy"
        assert body["service"] == "crochet-pattern-enterprise-validator"

    def test_validate_valid_pattern(self, api_client):
        resp = api_client.post("/validate", json={"pattern_text": VALID_PATTERN})
        assert resp.status_code == 200
        body = resp.json()
        assert body["valid"] is True
        assert "score" in body
        assert "pattern_hash" in body
        assert isinstance(body["errors"], list)
        assert isinstance(body["warnings"], list)

    def test_validate_bad_pattern_reports_errors(self, api_client):
        resp = api_client.post("/validate", json={"pattern_text": BAD_PATTERN})
        assert resp.status_code == 200
        assert len(resp.json()["errors"]) >= 1

    def test_certify_fully_verified(self, api_client):
        resp = api_client.post(
            "/certify",
            json={
                "pattern_text": VALID_PATTERN,
                "gauge_verified": True,
                "yarn_profile_known": True,
                "geometry_verified": True,
                "ai_conflicts": False,
                "safety_passed": True,
                "tolerance_passed": True,
            },
        )
        assert resp.status_code == 200
        assert resp.json()["level"] == "CERTIFIED"

    def test_gauge_calibrate_within_tolerance(self, api_client):
        resp = api_client.post(
            "/gauge/calibrate",
            json={
                "target_stitches_per_10cm": 18,
                "target_rows_per_10cm": 20,
                "measured_stitches_per_10cm": 18,
                "measured_rows_per_10cm": 20,
                "tolerance_percent": 5,
            },
        )
        assert resp.status_code == 200
        assert resp.json()["within_tolerance"] is True

    def test_gauge_calibrate_out_of_tolerance(self, api_client):
        resp = api_client.post(
            "/gauge/calibrate",
            json={
                "target_stitches_per_10cm": 18,
                "target_rows_per_10cm": 20,
                "measured_stitches_per_10cm": 12,
                "measured_rows_per_10cm": 14,
                "tolerance_percent": 5,
            },
        )
        assert resp.status_code == 200
        assert resp.json()["within_tolerance"] is False

    def test_report_returns_html(self, api_client):
        resp = api_client.post(
            "/report",
            json={
                "pattern_text": VALID_PATTERN,
                "gauge_verified": True,
                "yarn_profile_known": True,
                "geometry_verified": True,
                "tolerance_passed": True,
            },
        )
        assert resp.status_code == 200
        assert "html" in resp.headers["content-type"]
        assert "crochet" in resp.text.lower()

    def test_batch_validate_summary(self, api_client):
        resp = api_client.post(
            "/batch/validate",
            json={
                "patterns": [
                    {"pattern_text": VALID_PATTERN},
                    {"pattern_text": BAD_PATTERN},
                ]
            },
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["total"] == 2
        assert body["passed"] + body["failed"] == 2
        assert "success_rate" in body
        assert len(body["results"]) == 2

    def test_image_upload_success(self, api_client, monkeypatch, tmp_path):
        pytest.importorskip("PIL")
        monkeypatch.chdir(tmp_path)
        resp = api_client.post(
            "/gauge/image",
            params={
                "stitch_count": 18,
                "row_count": 20,
                "width_cm": 10,
                "height_cm": 10,
                "confidence": 0.95,
            },
            files={"image": ("gauge.png", make_png(120, 120), "image/png")},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["confidence"] == pytest.approx(0.95)
        assert body["image"]["width_pixels"] == 120

    def test_image_upload_rejects_bad_content_type(self, api_client, monkeypatch, tmp_path):
        monkeypatch.chdir(tmp_path)
        resp = api_client.post(
            "/gauge/image",
            files={"image": ("gauge.txt", b"not an image", "text/plain")},
        )
        assert resp.status_code == 415

    def test_image_upload_rejects_oversized(self, api_client, monkeypatch, tmp_path):
        monkeypatch.chdir(tmp_path)
        big = b"x" * (10 * 1024 * 1024 + 1)
        resp = api_client.post(
            "/gauge/image",
            params={
                "stitch_count": 18,
                "row_count": 20,
                "width_cm": 10,
                "height_cm": 10,
            },
            files={"image": ("big.png", big, "image/png")},
        )
        assert resp.status_code == 413

    def test_api_key_auth_required(self, api_client, monkeypatch):
        monkeypatch.setenv("CROCHET_API_KEY", "sekret")
        resp = api_client.post("/validate", json={"pattern_text": VALID_PATTERN})
        assert resp.status_code == 401
        resp = api_client.post(
            "/validate",
            json={"pattern_text": VALID_PATTERN},
            headers={"X-API-Key": "wrong"},
        )
        assert resp.status_code == 401
        resp = api_client.post(
            "/validate",
            json={"pattern_text": VALID_PATTERN},
            headers={"X-API-Key": "sekret"},
        )
        assert resp.status_code == 200

    def test_rate_limiting_returns_429(self, api_client):
        from crochet_checker.enterprise.api import rate_limiter

        old = rate_limiter.max_requests
        rate_limiter.requests.clear()
        rate_limiter.max_requests = 2
        try:
            assert (
                api_client.post("/validate", json={"pattern_text": VALID_PATTERN}).status_code
                == 200
            )
            assert (
                api_client.post("/validate", json={"pattern_text": VALID_PATTERN}).status_code
                == 200
            )
            assert (
                api_client.post("/validate", json={"pattern_text": VALID_PATTERN}).status_code
                == 429
            )
        finally:
            rate_limiter.max_requests = old
            rate_limiter.requests.clear()


# ---------------------------------------------------------------------------
# validation.abbreviations
# ---------------------------------------------------------------------------


class TestAbbreviationValidator:
    def test_valid_instructions_pass(self):
        from crochet_checker.validation.abbreviations import AbbreviationValidator

        v = AbbreviationValidator()
        assert v.validate_instruction_text("sc inc dc ch 2", 1) == []

    def test_unknown_abbreviation_error(self):
        from crochet_checker.validation.abbreviations import AbbreviationValidator

        v = AbbreviationValidator()
        issues = v.validate_instruction_text("xyzzy st", 2)
        assert len(issues) == 1
        assert issues[0]["type"] == "invalid_abbreviation"
        assert issues[0]["severity"] == "error"

    def test_typo_suggestion_warning(self):
        from crochet_checker.validation.abbreviations import AbbreviationValidator

        v = AbbreviationValidator()
        issues = v.validate_instruction_text("singel st", 1)
        assert issues[0]["suggestion"] == "sc"
        assert issues[0]["severity"] == "warning"

    def test_extract_words_and_skip(self):
        from crochet_checker.validation.abbreviations import AbbreviationValidator

        v = AbbreviationValidator()
        # "dc2tog" is skipped entirely: digits are word chars, so no
        # internal word boundary exists for the [a-zA-Z]+ pattern.
        assert v._extract_words("sc, inc. dc2tog!") == ["sc", "inc"]
        assert v._should_skip("in") is True
        assert v._should_skip("stitches") is True
        assert v._should_skip("sc") is False

    def test_validity_and_corrections(self):
        from crochet_checker.validation.abbreviations import AbbreviationValidator

        v = AbbreviationValidator()
        assert v._is_valid_abbreviation("sc") is True
        assert v._is_valid_abbreviation("zzz") is False
        assert v._suggest_correction("incr") == "inc"
        assert v._suggest_correction("zzz") is None
        assert v._similar("sc", "sc") is True

    def test_validate_abbreviations_on_pattern(self):
        from crochet_checker.validation.abbreviations import validate_abbreviations

        pattern = Pattern(
            rounds=[
                Round(
                    round_number=1,
                    instructions=[Instruction(source_text="xyzzy stitch")],
                )
            ]
        )
        issues = validate_abbreviations(pattern)
        assert len(issues) == 1
        assert issues[0]["abbreviation"] == "xyzzy"


# ---------------------------------------------------------------------------
# validation.consistency
# ---------------------------------------------------------------------------


class TestConsistencyValidator:
    def test_empty_pattern_no_findings(self):
        from crochet_checker.validation.consistency import ConsistencyValidator

        report = ConsistencyValidator().validate(Pattern())
        assert report.findings == []
        assert report.has_errors is False

    def test_repeat_block_zero_production_warns(self):
        from crochet_checker.validation.consistency import ConsistencyValidator

        inst = Instruction(
            source_text="ch 3",
            is_repeat_block=True,
            repeat_unit=[
                ParsedOperation(stitch_type=StitchType.CHAIN, count=1)
            ],
            repeat_count=2,
        )
        pattern = Pattern(rounds=[Round(round_number=1, instructions=[inst])])
        report = ConsistencyValidator().validate(pattern)
        assert len(report.findings) == 1
        assert report.findings[0].severity.value == "WARNING"

    def test_structure_missing_instructions(self):
        from crochet_checker.validation.consistency import ConsistencyValidator

        pattern = Pattern(
            rounds=[Round(round_number=1, instructions=[])],
        )
        report = ConsistencyValidator().validate(pattern)
        assert any(f.validator == "consistency" for f in report.findings)
        assert report.has_errors is True

    def test_validate_consistency_convenience(self):
        from crochet_checker.validation.consistency import validate_consistency

        report = validate_consistency(Pattern())
        assert report.findings == []


# ---------------------------------------------------------------------------
# validation.terminology
# ---------------------------------------------------------------------------


def _terminology_pattern(texts):
    rounds = []
    for i, t in enumerate(texts, start=1):
        rounds.append(
            Round(round_number=i, instructions=[Instruction(source_text=t)])
        )
    return Pattern(rounds=rounds)


class TestTerminologyValidator:
    def test_auto_detect_us_no_issues(self):
        from crochet_checker.validation.terminology import TerminologyValidator

        v = TerminologyValidator()
        assert v.validate_pattern(_terminology_pattern(["sc in each st"])) == []

    def test_mixed_terminology_detected(self):
        from crochet_checker.validation.terminology import TerminologyValidator

        v = TerminologyValidator()
        issues = v.validate_pattern(_terminology_pattern(["sc, dc in next"]))
        assert any(i["type"] == "mixed_terminology" for i in issues)

    def test_declared_uk_flags_us_term(self):
        from crochet_checker.validation.terminology import TerminologyValidator

        v = TerminologyValidator(declared_system="UK")
        issues = v.validate_pattern(_terminology_pattern(["sc in each st"]))
        assert any(i["type"] == "terminology_mismatch" for i in issues)

    def test_declared_us_flags_uk_term(self):
        from crochet_checker.validation.terminology import TerminologyValidator

        v = TerminologyValidator(declared_system="US")
        issues = v.validate_pattern(_terminology_pattern(["dc in next"]))
        assert any(i["type"] == "terminology_mismatch" for i in issues)

    def test_get_system_info(self):
        from crochet_checker.validation.terminology import TerminologyValidator

        v = TerminologyValidator()
        v.validate_pattern(_terminology_pattern(["sc in each st"]))
        info = v.get_system_info()
        assert info["detected"] == "US"
        assert info["consistent"] is True

    def test_validate_terminology_with_declared_notes(self):
        from crochet_checker.validation.terminology import validate_terminology

        pattern = Pattern(
            metadata=PatternMetadata(notes=["Written in US terms"]),
            rounds=_terminology_pattern(["sc in each st"]).rounds,
        )
        assert validate_terminology(pattern) == []


# ---------------------------------------------------------------------------
# validation.multi_piece
# ---------------------------------------------------------------------------


class TestMultiPieceValidator:
    def test_single_piece_falls_back_to_stitch_counts(self):
        from crochet_checker.validation.multi_piece import MultiPieceValidator

        pattern = Pattern(rounds=[sc_round(1, 6)])
        result = MultiPieceValidator().validate(pattern)
        # fallback returns a StitchCountReport
        assert hasattr(result, "findings")

    def test_pieces_validation_runs(self):
        from crochet_checker.validation.multi_piece import MultiPieceValidator

        piece = PatternPiece(name="HEAD", rounds=[sc_round(1, 6)])
        pattern = Pattern(
            metadata=PatternMetadata(),
            rounds=[sc_round(1, 6)],
            pieces=[piece],
        )
        with pytest.raises(AttributeError):
            # Known limitation: iterating a StitchCountReport yields tuples.
            MultiPieceValidator().validate(pattern)

    def test_transitions_empty_for_single_piece(self):
        from crochet_checker.validation.multi_piece import MultiPieceValidator

        pattern = Pattern(rounds=[sc_round(1, 6)])
        assert MultiPieceValidator().validate_transitions(pattern) == []

    def test_validate_multi_piece_convenience(self):
        from crochet_checker.validation.multi_piece import validate_multi_piece

        pattern = Pattern(rounds=[sc_round(1, 6)])
        assert hasattr(validate_multi_piece(pattern), "findings")


# ---------------------------------------------------------------------------
# validation.multipiece
# ---------------------------------------------------------------------------


class TestMultiPieceDetector:
    def test_detect_pieces_returns_list(self):
        from crochet_checker.validation.multipiece import MultiPieceDetector

        text = "## Head\nRound 1: 6 sc\n## Body\nRound 1: 6 sc"
        pieces = MultiPieceDetector().detect_pieces(text)
        assert isinstance(pieces, list)

    def test_validate_pieces_handles_errors(self):
        from crochet_checker.validation.multipiece import MultiPieceDetector

        pieces = [
            {"name": "HEAD", "content": "Round 1: 6 sc into magic ring (6)"},
            {"name": "BODY", "content": "Round 1: 6 sc into magic ring (6)"},
        ]
        result = MultiPieceDetector().validate_pieces(pieces)
        assert result["total_pieces"] == 2
        assert result["overall_status"] in ("PASS", "PASS_WITH_WARNINGS")

    def test_detect_and_validate_single_piece(self):
        from crochet_checker.validation.multipiece import detect_and_validate_multipiece

        result = detect_and_validate_multipiece("Round 1: 6 sc into magic ring (6)")
        assert result["total_pieces"] == 1
        assert "message" in result


# ---------------------------------------------------------------------------
# validation.row_transitions
# ---------------------------------------------------------------------------


class TestRowTransitionValidator:
    def test_single_round_no_transitions(self):
        from crochet_checker.validation.row_transitions import RowTransitionValidator

        report = RowTransitionValidator().validate(Pattern(rounds=[sc_round(1, 6)]))
        assert report.total_transitions_checked == 0
        assert report.findings == []

    def test_large_drop_warns(self):
        from crochet_checker.validation.row_transitions import RowTransitionValidator

        pattern = Pattern(rounds=[sc_round(1, 20), sc_round(2, 5)])
        report = RowTransitionValidator().validate(pattern)
        assert report.total_transitions_checked == 1
        assert any("drops" in f.message for f in report.findings)

    def test_large_increase_warns(self):
        from crochet_checker.validation.row_transitions import RowTransitionValidator

        pattern = Pattern(rounds=[sc_round(1, 6), sc_round(2, 20)])
        report = RowTransitionValidator().validate(pattern)
        assert any("increases" in f.message for f in report.findings)

    def test_numbering_jump_warns(self):
        from crochet_checker.validation.row_transitions import RowTransitionValidator

        pattern = Pattern(rounds=[sc_round(1, 6), sc_round(3, 6)])
        report = RowTransitionValidator().validate(pattern)
        assert any("jumps" in f.message for f in report.findings)

    def test_row_numbering_jump(self):
        from crochet_checker.validation.row_transitions import RowTransitionValidator

        rows = [
            Row(row_number=1, instructions=[Instruction(source_text="6 sc")]),
            Row(row_number=3, instructions=[Instruction(source_text="6 sc")]),
        ]
        pattern = Pattern(rows=rows)
        report = RowTransitionValidator().validate(pattern)
        assert any("Row numbering" in f.message for f in report.findings)

    def test_convenience_function(self):
        from crochet_checker.validation.row_transitions import validate_row_transitions

        report = validate_row_transitions(Pattern(rounds=[sc_round(1, 6)]))
        assert report.total_transitions_checked == 0


# ---------------------------------------------------------------------------
# reporter.fallback
# ---------------------------------------------------------------------------


class TestUnsupportedSyntaxFallback:
    def test_trusted_normal_parse(self):
        from crochet_checker.reporter.fallback import (
            TrustLevel,
            UnsupportedSyntaxFallback,
        )

        f = UnsupportedSyntaxFallback()
        result = f.parse_with_fallback("Round 3: 2 dc in each st around (24 sts)")
        assert result.count == 24
        assert result.trust_level == TrustLevel.TRUSTED
        assert f.has_warnings() is False

    def test_spatial_reference_approximate(self):
        from crochet_checker.reporter.fallback import (
            TrustLevel,
            UnsupportedSyntaxFallback,
        )

        f = UnsupportedSyntaxFallback()
        result = f.parse_with_fallback(
            "work backward through the space to the first stitch", 5
        )
        assert result.count == 1
        assert result.trust_level == TrustLevel.APPROXIMATE
        assert f.has_warnings() is True

    def test_vague_instruction_untrusted(self):
        from crochet_checker.reporter.fallback import (
            TrustLevel,
            UnsupportedSyntaxFallback,
        )

        f = UnsupportedSyntaxFallback()
        result = f.parse_with_fallback(
            "sc in several stitches around", expected_count=7
        )
        assert result.count == 7
        assert result.trust_level == TrustLevel.UNTRUSTED

    def test_generic_fallback_untrusted(self):
        from crochet_checker.reporter.fallback import (
            TrustLevel,
            UnsupportedSyntaxFallback,
        )

        f = UnsupportedSyntaxFallback()
        result = f.parse_with_fallback("make it look nice", expected_count=9)
        assert result.count == 9
        assert result.trust_level == TrustLevel.UNTRUSTED
        assert result.suggestions

    def test_unknown_count_detection(self):
        from crochet_checker.reporter.fallback import (
            TrustLevel,
            UnsupportedSyntaxFallback,
        )

        f = UnsupportedSyntaxFallback()
        result = f.parse_with_fallback(
            "repeat previous section", expected_count=12
        )
        assert result.trust_level == TrustLevel.UNTRUSTED

    def test_detect_unsupported(self):
        from crochet_checker.reporter.fallback import UnsupportedSyntaxFallback

        f = UnsupportedSyntaxFallback()
        detections = f.detect_unsupported("work backward", 3)
        assert detections
        assert detections[0][0] == "spatial_reference"

    def test_warning_helpers(self):
        from crochet_checker.reporter.fallback import UnsupportedSyntaxFallback

        f = UnsupportedSyntaxFallback()
        f.parse_with_fallback("sc in several stitches around")
        assert len(f.get_warnings()) == 1
        assert len(f.get_untrusted_counts()) == 1
        f.clear_warnings()
        assert f.has_warnings() is False
        f.reset()


# ---------------------------------------------------------------------------
# reporter.patcher
# ---------------------------------------------------------------------------


class TestDiffPatchGenerator:
    def test_patch_diff(self):
        from crochet_checker.reporter.patcher import Patch

        patch = Patch(
            round_number=1,
            line_number=1,
            original_text="a",
            corrected_text="b",
            issue_type="t",
            description="d",
            confidence=0.9,
        )
        diff = patch.to_diff()
        assert "---" in diff and "+++" in diff

    def test_patch_report_fixable(self):
        from crochet_checker.reporter.patcher import Patch, PatchReport

        report = PatchReport()
        report.add_patch(
            Patch(1, 1, "a", "b", "x", "d", 0.9)
        )
        report.add_patch(
            Patch(1, 1, "a", "b", "x", "d", 0.4)
        )
        assert report.total_issues == 2
        assert report.fixable_issues == 1

    def test_count_mismatch_add(self):
        from crochet_checker.reporter.patcher import DiffPatchGenerator

        report = DiffPatchGenerator().analyze_round(
            1, ["ch 3, 10 dc in ring"], 12, [5]
        )
        assert any("stitch_count_add" == p.issue_type for p in report.patches)

    def test_count_mismatch_remove(self):
        from crochet_checker.reporter.patcher import DiffPatchGenerator

        report = DiffPatchGenerator().analyze_round(
            1, ["12 dc in ring"], 10, [5]
        )
        assert any("stitch_count_remove" == p.issue_type for p in report.patches)

    def test_turning_chain_mismatch(self):
        from crochet_checker.reporter.patcher import DiffPatchGenerator

        report = DiffPatchGenerator().analyze_round(
            2, ["ch 2, dc in each st around"], 20, [10]
        )
        assert any("turning_chain_mismatch" == p.issue_type for p in report.patches)

    def test_corner_sequence_mismatch(self):
        from crochet_checker.reporter.patcher import DiffPatchGenerator

        instructions = [
            "corner: (3 dc, ch 2, 3 dc)",
            "sp: (3 dc, ch 3, 3 dc)",
        ]
        report = DiffPatchGenerator().analyze_round(
            1, instructions, 24, [1, 2]
        )
        assert any(
            "corner_sequence_mismatch" == p.issue_type for p in report.patches
        )

    def test_full_patch_report(self):
        from crochet_checker.reporter.patcher import DiffPatchGenerator

        text = (
            "Round 1: ch 4, sl st to join\n"
            "Round 2: ch 3, 10 dc in ring (12 sts)\n"
            "Round 3: ch 2, 2 dc in each st around (24 sts)\n"
        )
        result = DiffPatchGenerator().generate_full_patch_report(text)
        assert "total_patches" in result
        assert len(result["patches"]) == result["total_patches"]
        assert result["total_patches"] >= 1

    def test_reset(self):
        from crochet_checker.reporter.patcher import DiffPatchGenerator

        DiffPatchGenerator().reset()


# ---------------------------------------------------------------------------
# utils.special_constructions
# ---------------------------------------------------------------------------


class TestSpecialConstructions:
    def test_granny_square_no_data(self):
        from crochet_checker.utils.special_constructions import GrannySquareValidator

        analysis = GrannySquareValidator().validate([])
        assert analysis.is_valid is False
        assert analysis.errors == ["No round data"]

    def test_granny_square_valid(self):
        from crochet_checker.utils.special_constructions import GrannySquareValidator

        rounds = [{"round": 1, "count": 12}, {"round": 2, "count": 24}]
        analysis = GrannySquareValidator().validate(rounds)
        assert analysis.is_valid is True
        assert analysis.expected_counts == {1: 12, 2: 24}
        assert analysis.details["growth_per_round"] == 12

    def test_granny_square_invalid(self):
        from crochet_checker.utils.special_constructions import GrannySquareValidator

        analysis = GrannySquareValidator().validate([{"round": 1, "count": 13}])
        assert analysis.is_valid is False
        assert any("Expected 12, got 13" in e for e in analysis.errors)

    def test_spiral_join_warning(self):
        from crochet_checker.utils.special_constructions import SpiralValidator

        rounds = [
            {"round": 1, "count": 6, "instruction": "6 sc in MR"},
            {"round": 2, "count": 12, "instruction": "inc x6, sl st join"},
        ]
        analysis = SpiralValidator().validate(rounds)
        assert any("Join detected" in w for w in analysis.warnings)

    def test_spiral_turn_warning(self):
        from crochet_checker.utils.special_constructions import SpiralValidator

        rounds = [
            {"round": 1, "count": 6, "instruction": "6 sc"},
            {"round": 2, "count": 12, "instruction": "inc, turn"},
        ]
        analysis = SpiralValidator().validate(rounds)
        assert any("Turn detected" in w for w in analysis.warnings)

    def test_joined_round_validator(self):
        from crochet_checker.utils.special_constructions import JoinedRoundValidator

        analysis = JoinedRoundValidator().validate([])
        assert analysis.type == "joined_rounds"
        assert analysis.is_valid is True

    def test_detector_keywords(self):
        from crochet_checker.utils.special_constructions import SpecialConstructionDetector

        d = SpecialConstructionDetector()
        detected = d.detect("Work a granny square with corner space")
        assert detected["granny_square"] is True
        assert d.get_primary("magic ring, amigurumi") == "amigurumi"
        assert d.get_primary("plain text") == "unknown"


# ---------------------------------------------------------------------------
# utils.category_detector
# ---------------------------------------------------------------------------


class TestCategoryDetector:
    def test_explicit_metadata_category(self):
        from crochet_checker.utils.category_detector import detect_category

        pattern = Pattern(metadata=PatternMetadata(category="hat"))
        assert detect_category(pattern) == "hat"

    def test_amigurumi_from_magic_ring_and_size(self):
        from crochet_checker.utils.category_detector import detect_category

        pattern = Pattern(
            rounds=[
                Round(
                    round_number=1,
                    instructions=[
                        Instruction(
                            source_text="6 sc into magic ring",
                            operations=[
                                ParsedOperation(
                                    stitch_type=StitchType.SINGLE_CROCHET, count=6
                                )
                            ],
                        )
                    ],
                )
            ]
        )
        assert detect_category(pattern) == "amigurumi"

    def test_amigurumi_keyword(self):
        from crochet_checker.utils.category_detector import detect_category

        pattern = Pattern(source_text="stuffed amigurumi toy")
        assert detect_category(pattern) == "amigurumi"

    def test_unknown_category(self):
        from crochet_checker.utils.category_detector import detect_category

        assert detect_category(Pattern()) == "unknown"


# ---------------------------------------------------------------------------
# api.rest
# ---------------------------------------------------------------------------


class TestRestAPI:
    def test_health_and_root(self):
        from crochet_checker.api.rest import app

        client = TestClient(app)
        assert client.get("/health").json() == {"status": "ok"}
        assert "message" in client.get("/").json()


# ---------------------------------------------------------------------------
# ast.ast_builder
# ---------------------------------------------------------------------------


class TestASTBuilder:
    def test_build_returns_ast(self):
        from crochet_checker.ast.ast_builder import ASTBuilder

        ast = ASTBuilder().build("Round 1: 6 sc into magic ring (6)")
        assert len(ast.pieces) == 1
        assert ast.pieces[0].rounds == []


# ---------------------------------------------------------------------------
# batch.processor
# ---------------------------------------------------------------------------


class TestBatchProcessor:
    def test_discover_patterns(self, tmp_path):
        from crochet_checker.batch.processor import BatchProcessor

        (tmp_path / "a.txt").write_text("Round 1")
        (tmp_path / "b.pdf").write_bytes(b"%PDF")
        nested = tmp_path / "sub"
        nested.mkdir()
        (nested / "c.txt").write_text("Round 2")

        processor = BatchProcessor(str(tmp_path / "out"))
        assert processor.discover_patterns(str(tmp_path / "a.txt")) == [
            tmp_path / "a.txt"
        ]
        recursive = processor.discover_patterns(str(tmp_path), recursive=True)
        assert len(recursive) == 3
        flat = processor.discover_patterns(str(tmp_path), recursive=False)
        assert len(flat) == 2

    def test_batch_validate(self, tmp_path):
        from crochet_checker.batch.processor import BatchProcessor

        processor = BatchProcessor(str(tmp_path / "out"))
        result = processor.batch_validate([tmp_path / "a.txt"])
        assert result["total_patterns"] == 1
        assert result["success_rate"] == 100.0


# ---------------------------------------------------------------------------
# compute.capabilities
# ---------------------------------------------------------------------------


class TestComputeCapabilities:
    def test_detect_compute(self):
        from crochet_checker.compute.capabilities import (
            ComputeCapabilities,
            detect_compute,
        )

        caps = detect_compute()
        assert isinstance(caps, ComputeCapabilities)
        assert caps.cpu_count >= 1
        assert isinstance(caps.has_numpy, bool)
        assert isinstance(caps.has_cuda, bool)
        assert caps.recommendation

    def test_to_dict(self):
        from crochet_checker.compute.capabilities import detect_compute

        data = detect_compute().to_dict()
        assert "python_version" in data
        assert "has_torch" in data
        assert "quantum_backend" in data


# ---------------------------------------------------------------------------
# interactive.stitch_counter
# ---------------------------------------------------------------------------


class TestInteractiveStitchCounter:
    def test_complete_stitch_and_progress(self):
        from crochet_checker.interactive.stitch_counter import InteractiveStitchCounter

        counter = InteractiveStitchCounter({1: 6})
        counter.complete_stitch("sc")
        counter.complete_stitch("sc")
        progress = counter.get_progress()
        assert progress["current_round"] == 1
        assert progress["total_stitches"] == 2
        assert counter.state.round_stitches[1] == 2

    def test_next_round_legacy(self):
        from crochet_checker.interactive.stitch_counter import InteractiveStitchCounter

        counter = InteractiveStitchCounter()
        result = counter.next_round()
        # The legacy shim sets `current_round` on the counter itself, while
        # get_progress() reads from the (unchanged) CounterState.
        assert counter.current_round == 2
        assert result["current_round"] == 1
        assert result["total_stitches"] == 0

    def test_counter_state_defaults(self):
        from crochet_checker.interactive.stitch_counter import CounterState

        state = CounterState()
        assert state.current_round == 1
        assert state.round_stitches == {}


# ---------------------------------------------------------------------------
# optimization.pattern_optimizer
# ---------------------------------------------------------------------------


class TestPatternOptimizer:
    def test_turning_chain_suggestion(self):
        from crochet_checker.optimization.pattern_optimizer import PatternOptimizer

        result = PatternOptimizer().optimize("ch 1, sc in each st")
        assert any(o.category == "efficiency" for o in result)

    def test_repeat_notation_suggestion(self):
        from crochet_checker.optimization.pattern_optimizer import PatternOptimizer

        result = PatternOptimizer().optimize("sc sc sc sc sc sc sc")
        assert any(o.category == "clarity" for o in result)

    def test_no_suggestions(self):
        from crochet_checker.optimization.pattern_optimizer import PatternOptimizer

        assert PatternOptimizer().optimize("dc dc") == []


# ---------------------------------------------------------------------------
# visualization.diagram / stitch_chart / pattern_debugger
# ---------------------------------------------------------------------------


class TestVisualization:
    def test_dimension_diagram(self, tmp_path):
        from crochet_checker.visualization.diagram import PatternDiagramGenerator

        out = tmp_path / "diagram.svg"
        result = PatternDiagramGenerator().generate_dimension_diagram(
            {"width_inches": 12.5}, str(out)
        )
        assert result == str(out)
        content = out.read_text()
        assert "<svg" in content
        assert "Width: 12.5 in" in content

    def test_stitch_chart(self, tmp_path):
        from crochet_checker.visualization.stitch_chart import StitchChartGenerator

        out = tmp_path / "chart.svg"
        data = [
            {"round": 1, "stitches": [{"type": "sc"}, {"type": "dc"}, {"type": "bobble"}]}
        ]
        result = StitchChartGenerator().generate_chart(data, str(out))
        assert result == str(out)
        content = out.read_text()
        assert "Stitch Chart" in content
        assert "R1" in content

    def test_pattern_debugger(self):
        from crochet_checker.visualization.pattern_debugger import PatternDebugger

        debugger = PatternDebugger()
        debugger.set_breakpoint(5)
        debugger.set_breakpoint(3)
        debugger.set_breakpoint(3)  # duplicate ignored
        assert debugger.breakpoints == [3, 5]

        debugger.set_breakpoint(2)
        visual_map = debugger.generate_visual_map("Line one\nLine two")
        assert "PATTERN VISUAL MAP" in visual_map
        assert "* 002 | Line two" in visual_map


# ---------------------------------------------------------------------------
# pdf.image_support
# ---------------------------------------------------------------------------


class TestPDFImageSupport:
    def test_generate_pattern_images(self, tmp_path):
        from crochet_checker.pdf.image_support import generate_pattern_images

        out = tmp_path / "images"
        images = generate_pattern_images(None, str(out))
        assert images == []
        assert out.is_dir()


# ---------------------------------------------------------------------------
# yarn.substitution
# ---------------------------------------------------------------------------


class TestYarnSubstitution:
    def test_find_substitutes(self):
        from crochet_checker.yarn.substitution import (
            YarnProperties,
            YarnSubstitutionEngine,
        )

        yarn = YarnProperties(name="Original", brand="Brand X", weight="worsted")
        results = YarnSubstitutionEngine().find_substitutes(yarn)
        assert len(results) >= 1
        assert results[0].compatibility_score == 100
        assert results[0].substitute_yarn.name == "Heartland"

    def test_properties_defaults(self):
        from crochet_checker.yarn.substitution import YarnProperties

        yarn = YarnProperties(name="Y", brand="B")
        assert yarn.weight == "worsted"
        assert yarn.fiber == "acrylic"
        assert yarn.yardage == 200


# ---------------------------------------------------------------------------
# analysis.*
# ---------------------------------------------------------------------------


class TestAnalysis:
    def test_complexity_levels(self):
        from crochet_checker.analysis.complexity_analyzer import ComplexityAnalyzer

        analyzer = ComplexityAnalyzer()
        assert analyzer.analyze("simple sc").difficulty_level == "beginner"
        assert analyzer.analyze("cluster stitch").difficulty_level == "intermediate"
        advanced_text = ("bobble cluster *\n" * 31).strip()
        assert analyzer.analyze(advanced_text).difficulty_level == "advanced"

    def test_gauge_calculator(self):
        from crochet_checker.analysis.gauge_calculator import GaugeCalculator

        calc = GaugeCalculator()
        info = calc.calculate_from_swatches(17, 4, "H", "worsted")
        assert info.stitches_per_4_inches == pytest.approx(17)
        assert info.matches_pattern is True

        off = calc.calculate_from_swatches(20, 4, "H", "worsted")
        assert off.matches_pattern is False

    def test_pattern_scaler(self):
        from crochet_checker.analysis.pattern_scaler import PatternScaler

        result = PatternScaler().scale("sc dc sc", (10, 10), (20, 10))
        assert result.scale_factor == pytest.approx(2.0)
        assert result.adjusted_stitches == 6
        assert result.adjustments

    def test_time_estimator(self):
        from crochet_checker.analysis.time_estimator import TimeEstimator

        estimate = TimeEstimator().estimate("sc dc", "beginner")
        assert estimate.total_hours > 0
        assert TimeEstimator().estimate("sc dc", "advanced").total_hours < estimate.total_hours

    def test_yarn_calculator(self):
        from crochet_checker.analysis.yarn_calculator import AdvancedYarnCalculator

        requirement = AdvancedYarnCalculator().calculate("sc dc", "worsted")
        assert requirement.total_yards == pytest.approx(3.3)
        assert requirement.skeins_needed == 1
