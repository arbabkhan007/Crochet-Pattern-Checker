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
        "Round 2: inc x 6 (12)\n"
        "Round 3: (sc, inc) x 6 (18)\n"
        "Round 4: (2 sc, inc) x 6 (24)"
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
