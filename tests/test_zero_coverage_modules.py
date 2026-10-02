"""
Targeted tests for previously untested (0% coverage) production modules.

Covers:
- parser.normalizer
- validation.abbreviations / consistency / terminology / row_transitions
- reporter.fallback / reporter.patcher
"""

from __future__ import annotations

import os
import struct
import zlib

import pytest


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


# ---------------------------------------------------------------------------
# enterprise.api (REST integration + security)
# ---------------------------------------------------------------------------


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
# api.rest
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# compute.capabilities
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# interactive.stitch_counter
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# optimization.pattern_optimizer
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# yarn.substitution
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# analysis.*
# ---------------------------------------------------------------------------


