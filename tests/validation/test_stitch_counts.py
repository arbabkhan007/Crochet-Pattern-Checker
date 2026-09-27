from crochet_checker.parser.parser import parse_pattern
from crochet_checker.validation import validate_pattern
from crochet_checker.validation.stitch_counts import validate_stitch_counts


class TestCorrect:
    def test_circle(self):
        t = (
            "Round 1: 6 sc into magic ring (6)"
            + chr(10)
            + "Round 2: (sc, inc) x 6 (18)"
        )
        p = parse_pattern(t)
        assert len(p.rounds) == 2
        assert p.rounds[0].computed_stitch_count == 6
        assert p.rounds[1].computed_stitch_count == 18

    def test_amigurumi(self):
        lines = [
            "Round 1: 6 sc into magic ring (6)",
            "Round 2: (sc, inc) x 6 (18)",
            "Round 3: (2 sc, inc) x 6 (24)",
            "Round 4: (3 sc, inc) x 6 (30)",
        ]
        p = parse_pattern(chr(10).join(lines))
        assert p.rounds[0].computed_stitch_count == 6
        assert p.rounds[1].computed_stitch_count == 18
        assert p.rounds[2].computed_stitch_count == 24
        assert p.rounds[3].computed_stitch_count == 30

    def test_decreases(self):
        lines = [
            "Round 1: (4 sc, dec) x 6 (30)",
            "Round 2: (3 sc, dec) x 6 (24)",
            "Round 3: (2 sc, dec) x 6 (18)",
        ]
        p = parse_pattern(chr(10).join(lines))
        assert p.rounds[0].computed_stitch_count == 30
        assert p.rounds[1].computed_stitch_count == 24
        assert p.rounds[2].computed_stitch_count == 18


class TestErrors:
    def test_wrong_repeat(self):
        t = (
            "Round 1: 6 sc into magic ring (6)"
            + chr(10)
            + "Round 2: (sc, inc) x 6 (20)"
        )
        r = validate_stitch_counts(parse_pattern(t))
        assert r.has_errors

    def test_inconsistent(self):
        lines = [
            "Round 1: 6 sc into magic ring (6)",
            "Round 2: (sc, inc) x 6 (18)",
            "Round 3: (3 sc, inc) x 6 (30)",
        ]
        r = validate_stitch_counts(parse_pattern(chr(10).join(lines)))
        assert r.has_errors


class TestPipeline:
    def test_pass(self):
        lines = [
            "Round 1: 6 sc into magic ring (6)",
            "Round 2: (sc, inc) x 6 (18)",
            "Round 3: (2 sc, inc) x 6 (24)",
        ]
        r = validate_pattern(parse_pattern(chr(10).join(lines)))
        assert r.score >= 50
        assert r.stitch_counts is not None

    def test_fail(self):
        t = (
            "Round 1: 6 sc into magic ring (6)"
            + chr(10)
            + "Round 2: (sc, inc) x 7 (18)"
        )
        r = validate_pattern(parse_pattern(t))
        assert r.score < 80

    def test_dict(self):
        d = validate_pattern(
            parse_pattern("Round 1: 6 sc into magic ring (6)")
        ).to_dict()
        assert "overall_status" in d
        assert "score" in d

    def test_golden(self):
        lines = [
            "Round 1: 6 sc into magic ring (6)",
            "Round 2: (sc, inc) x 6 (18)",
            "Round 3: (2 sc, inc) x 6 (24)",
            "Round 4: (3 sc, inc) x 6 (30)",
            "Round 5: (4 sc, inc) x 6 (36)",
        ]
        p = parse_pattern(chr(10).join(lines))
        expected = [6, 18, 24, 30, 36]
        for i, r in enumerate(p.rounds):
            assert r.computed_stitch_count == expected[i]


def test_each_around_example():
    """'inc/sc in each st around' must use the previous round, not count=1."""
    report = validate_pattern(open("examples/amigurumi.txt").read())
    assert report.valid is True
    assert report.overall_status == "PASS"
    assert report.score == 100
    assert report.errors == []

    broken = validate_pattern(open("examples/intentionally_broken_pattern.txt").read())
    assert broken.valid is False
    assert broken.overall_status == "ERROR"
    messages = [getattr(item, "message", str(item)) for item in broken.errors]
    assert any("produce 21" in message for message in messages)
    assert not any("Round/row 2:" in message for message in messages)


def test_foundation_and_clauses():
    """Joined chains and comma-separated clauses must not stop at the first word."""
    tube = validate_pattern(open("examples/tube_cowl.txt").read())
    assert tube.valid is True
    assert tube.errors == []

    scarf = validate_pattern(open("examples/scarf.txt").read())
    assert scarf.errors == []

    boot = validate_pattern(open("examples/baby_booties.txt").read())
    messages = [getattr(item, "message", str(item)) for item in boot.errors]
    assert any("produce 20" in message for message in messages)
    assert not any("produce 10" in message for message in messages)
