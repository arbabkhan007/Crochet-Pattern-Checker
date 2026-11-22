"""Tests for parser edge cases: multi-group instructions, chain rings,
chain-foundation rows, and multi-piece patterns."""
from crochet_checker.parser.parser import parse_pattern
from crochet_checker.validation import validate_pattern
from crochet_checker.validation.stitch_counts import validate_stitch_counts

def ops(pattern, row=0):
    r = (pattern.rounds or pattern.rows)[row]
    out = []
    for i in r.instructions:
        out.extend((o.stitch_type.value, o.count, o.into_stitch) for o in i.operations)
    return out

class TestMultiGroup:
    def test_sc_dec_sc(self):
        p = parse_pattern("Round 1: 20 sc in magic ring (20)\nRound 2: 5 sc, dec x 5, 5 sc (15)")
        assert ops(p, 1) == [("single_crochet", 5, None), ("decrease", 5, None), ("single_crochet", 5, None)]
        r = validate_stitch_counts(p)
        assert not r.has_errors

    def test_broken_dec_distribution_caught(self):
        # 10 sc + 5 dec + 5 sc consumes 25, not 20 — must be flagged
        p = parse_pattern("Round 1: 20 sc in magic ring (20)\nRound 2: 10 sc, dec x 5, 5 sc (15)")
        r = validate_stitch_counts(p)
        assert r.has_errors

    def test_turn_chain_ignored(self):
        p = parse_pattern("Row 1: ch 20, sc in 2nd ch from hook, sc in each ch across (19)\n"
                          "Row 2: ch 1, turn, sc in each st across (19)")
        rep = validate_pattern(p)
        assert not rep.errors

class TestChainRing:
    def test_ring_models_40_stitches(self):
        p = parse_pattern("Round 1: ch 40, sl st to join (40)\nRound 2: sc in each st around (40)")
        r = p.rounds[0]
        assert r.computed_stitch_count == 40
        rep = validate_pattern(p)
        assert not rep.errors

    def test_turning_chain_not_a_ring(self):
        p = parse_pattern("Row 1: ch 20, sc in 2nd ch from hook, sc in each ch across (19)")
        assert p.rows[0].computed_stitch_count != 20  # foundation row is not modeled as a ring

class TestMultiPiece:
    def test_numbering_restart_not_an_error(self):
        t = ("Round 1: 6 sc into magic ring (6)\n"
             "Round 2: inc x 6 (12)\n"
             "Round 3: (sc, inc) x 6 (18)\n"
             "Round 1: 4 sc into magic ring (4)\n"
             "Round 2: (sc, inc) x 2 (6)")
        rep = validate_pattern(parse_pattern(t))
        assert not rep.errors
        assert not rep.warnings

class TestDecreaseSequence:
    def test_standard_close_passes(self):
        lines = ["Round 1: (4 sc, dec) x 6 (30)",
                 "Round 2: (3 sc, dec) x 6 (24)",
                 "Round 3: (2 sc, dec) x 6 (18)",
                 "Round 4: (sc, dec) x 6 (12)",
                 "Round 5: dec x 6 (6)"]
        # standalone sequence: first round has no previous context
        p = parse_pattern("\n".join(lines))
        rep = validate_pattern(p)
        assert not rep.errors

    def test_offset_repeat_fails(self):
        # (3 sc, dec) x 6 needs 30 previous stitches but states 30 while producing 24
        lines = ["Round 1: 36 sc in magic ring (36)",
                 "Round 2: (3 sc, dec) x 6 (30)"]
        p = parse_pattern("\n".join(lines))
        r = validate_stitch_counts(p)
        assert r.has_errors
