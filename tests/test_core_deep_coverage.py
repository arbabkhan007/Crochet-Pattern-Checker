from pathlib import Path

import pytest

from crochet_checker.enterprise import (
    AuditTrail,
    CertificationLevel,
    CertificationReportWriter,
    EnterpriseCertifier,
    GaugeCalibrator,
    GaugeMeasurement,
    GaugeImageIngestor,
    MonteCarloSimulator,
    YarnDatabase,
    YarnProfile,
    YarnSubstitutionAnalyzer,
)
from crochet_checker.parser import (
    GlossaryPrePassExtractor,
    MarkdownFrontmatterSanitizer,
    MultiPieceASTBuilder,
    RecursiveLoopUnroller,
)
from crochet_checker.parser.parser import parse_pattern
from crochet_checker.validation import validate_pattern


def valid_text():
    return (
        "Round 1: 6 sc into magic ring (6)\n"
        "Round 2: (sc, inc) x 6 (18)\n"
        "Round 3: (2 sc, inc) x 6 (24)"
    )


def test_sanitizer_removes_markdown():
    text = """
# Pattern title

This is introductory text.

## Notes
Remember to keep tension even.

Round 1: 6 sc into magic ring (6)
"""

    result, removed = MarkdownFrontmatterSanitizer().sanitize(text)

    assert "Round 1" in result
    assert isinstance(removed, list)


def test_glossary_extraction():
    text = """
## Glossary
3-tr-cl: 3 treble cluster
BPtr: back post treble

## Pattern
Round 1: 6 sc into magic ring (6)
"""

    symbols = GlossaryPrePassExtractor().extract(text)

    assert "3-tr-cl" in symbols
    assert "BPtr" in symbols


def test_multi_piece_builder():
    text = """
## Body
Round 1: 6 sc into magic ring (6)

## Arm
Round 1: 6 sc into magic ring (6)

## Leg
Round 1: 6 sc into magic ring (6)
"""

    ast = MultiPieceASTBuilder().build(text)

    assert ast is not None
    assert len(ast.pieces) >= 2


def test_recursive_unroller():
    unroller = RecursiveLoopUnroller()

    result = unroller.unroll("*sc 2* repeat 3 times")

    assert result is not None
    assert len(result) >= 1


def test_validation_valid_pattern():
    pattern = parse_pattern(valid_text())
    report = validate_pattern(pattern)

    assert report.valid is True
    assert report.score >= 50
    assert report.to_dict()


def test_validation_invalid_pattern():
    pattern = parse_pattern(
        "Round 1: 6 sc into magic ring (6)\n"
        "Round 2: (sc, inc) x 7 (18)"
    )

    report = validate_pattern(pattern)

    assert report.errors
    assert report.score < 80


def test_certification_certified():
    pattern = parse_pattern(valid_text())
    report = validate_pattern(pattern)

    certificate = EnterpriseCertifier().certify(
        pattern,
        report,
        gauge_verified=True,
        yarn_profile_known=True,
        geometry_verified=True,
        ai_conflicts=False,
        safety_passed=True,
        tolerance_passed=True,
    )

    assert certificate.level == CertificationLevel.CERTIFIED
    assert certificate.approved_for_production is True
    assert certificate.to_json()


def test_certification_requires_sample():
    pattern = parse_pattern(valid_text())
    report = validate_pattern(pattern)

    certificate = EnterpriseCertifier().certify(
        pattern,
        report,
        gauge_verified=False,
        yarn_profile_known=False,
        geometry_verified=False,
        tolerance_passed=False,
    )

    assert certificate.sample_required is True
    assert certificate.level in {
        CertificationLevel.SAMPLE_REQUIRED,
        CertificationLevel.REJECTED,
    }


def test_gauge_calibration_pass():
    target = GaugeMeasurement(18, 20, "target", 1.0)
    measured = GaugeMeasurement(18, 20, "measured", 0.9)

    result = GaugeCalibrator().calibrate(target, measured)

    assert result.within_tolerance is True
    assert result.sample_required is False


def test_gauge_calibration_fail():
    target = GaugeMeasurement(18, 20, "target", 1.0)
    measured = GaugeMeasurement(14, 16, "measured", 0.9)

    result = GaugeCalibrator().calibrate(target, measured)

    assert result.within_tolerance is False
    assert result.sample_required is True


def test_yarn_database_and_custom_profile():
    database = YarnDatabase()

    custom = YarnProfile(
        name="test-yarn",
        fiber="test",
        elasticity=0.2,
        shrinkage_percent=2,
        drape=0.5,
        stitch_definition=0.8,
    )

    database.add(custom)

    assert database.get("test-yarn") == custom
    assert database.all()


def test_yarn_substitution():
    analyzer = YarnSubstitutionAnalyzer()

    result = analyzer.compare("cotton", "wool")

    assert result.risk_score >= 0
    assert result.reasons
    assert isinstance(result.sample_required, bool)


def test_monte_carlo_simulation():
    pattern = parse_pattern(valid_text())

    result = MonteCarloSimulator(
        simulations=500,
        seed=123,
    ).simulate(
        pattern,
        gauge_stitches_per_10cm=18,
        gauge_rows_per_10cm=20,
        tolerance_percent=5,
        tension_variation_percent=3,
    )

    assert result.simulations == 500
    assert 0 <= result.pass_probability <= 1
    assert result.minimum_width_cm <= result.maximum_width_cm


def test_audit_trail(tmp_path):
    pattern = parse_pattern(valid_text())
    report = validate_pattern(pattern)

    certificate = EnterpriseCertifier().certify(
        pattern,
        report,
        gauge_verified=True,
        yarn_profile_known=True,
        geometry_verified=True,
        tolerance_passed=True,
    )

    trail = AuditTrail(str(tmp_path / "audit.jsonl"))

    first = trail.append(
        pattern_hash=certificate.pattern_hash,
        certification=certificate,
        operator="test",
    )

    second = trail.append(
        pattern_hash=certificate.pattern_hash,
        certification=certificate,
        operator="test",
        action="REVIEW",
    )

    valid, errors = trail.verify()

    assert first["previous_hash"] == "GENESIS"
    assert second["previous_hash"] == first["record_hash"]
    assert valid is True
    assert errors == []


def test_report_writer(tmp_path):
    pattern = parse_pattern(valid_text())
    report = validate_pattern(pattern)

    certificate = EnterpriseCertifier().certify(
        pattern,
        report,
        gauge_verified=True,
        yarn_profile_known=True,
        geometry_verified=True,
        tolerance_passed=True,
    )

    output = tmp_path / "certificate.html"

    CertificationReportWriter().write(
        certificate,
        str(output),
        title="Test Certificate",
    )

    content = output.read_text(encoding="utf-8")

    assert "<!doctype html>" in content
    assert "Test Certificate" in content
    assert certificate.pattern_hash in content


def test_image_ingestion(tmp_path):
    pytest.importorskip("PIL")
    from PIL import Image

    image_path = tmp_path / "gauge.png"
    Image.new("RGB", (400, 300), "white").save(image_path)

    result = GaugeImageIngestor().calibrate_confirmed_measurement(
        str(image_path),
        stitch_count=18,
        row_count=20,
        width_cm=10,
        height_cm=10,
        confirmed_by_user=True,
        confidence=0.95,
    )

    assert result.image.width_pixels == 400
    assert result.measurement.stitches_per_10cm == 18
    assert result.confidence == 0.95


def test_image_ingestion_rejects_unconfirmed_measurement(tmp_path):
    pytest.importorskip("PIL")
    from PIL import Image

    image_path = tmp_path / "gauge.png"
    Image.new("RGB", (400, 300), "white").save(image_path)

    with pytest.raises(ValueError):
        GaugeImageIngestor().calibrate_confirmed_measurement(
            str(image_path),
            stitch_count=18,
            row_count=20,
            width_cm=10,
            height_cm=10,
            confirmed_by_user=False,
        )
