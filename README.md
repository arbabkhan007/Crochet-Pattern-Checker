# Crochet Pattern Checker

**Crochet Pattern Verification, Visualization & PDF Publishing Engine**

## Quick Start

```bash
pip install -e ".[dev]"
crochet-check check examples/simple_hat.txt
pytest tests/ -v
Pattern (text) → Parser → Structured Data → Validators → Report

Now create the **tests**:

```bash
cat > tests/parser/test_parser.py << 'EOF'
import pytest
from crochet_checker.parser.lexer import TokenType, tokenize
from crochet_checker.parser.parser import parse_instruction, parse_pattern
from crochet_checker.model.stitch import StitchType

class TestLexer:
    def test_number(self): t = tokenize("6"); assert t[0].type == TokenType.NUMBER
    def test_stitch(self): t = tokenize("sc"); assert t[0].type == TokenType.STITCH_ABBREV
    def test_repeat(self): t = tokenize("(sc, inc) x 6"); types = [x.type for x in t[:-1]]; assert TokenType.LPAREN in types
    def test_magic(self): t = tokenize("magic ring"); assert t[0].type == TokenType.MAGIC_RING
    def test_slst(self): t = tokenize("sl st"); assert t[0].value == "sl st"

class TestParser:
    def test_magic_ring(self):
        i = parse_instruction("6 sc into magic ring")
        assert any(op.stitch_type == StitchType.MAGIC_RING for op in i.operations)
    def test_repeat(self):
        i = parse_instruction("(sc, inc) x 6")
        assert i.is_repeat_block; assert i.repeat_count == 6
    def test_each(self):
        i = parse_instruction("sc in each st around")
        assert i.operations[0].into_stitch == "each_stitch_around"
    def test_chain(self):
        i = parse_instruction("ch 5"); assert i.operations[0].count == 5
    def test_stated(self):
        i = parse_instruction("(sc, inc) x 6 (18)"); assert i.stated_stitch_count == 18

class TestPatternParser:
    def test_circle(self):
        p = parse_pattern("Round 1: 6 sc into magic ring (6)\nRound 2: (sc, inc) x 6 (18)")
        assert len(p.rounds) == 2
    def test_counts(self):
        p = parse_pattern("Round 1: 6 sc into magic ring (6)\nRound 2: (sc, inc) x 6 (18)\nRound 3: (2 sc, inc) x 6 (24)")
        assert p.rounds[0].computed_stitch_count == 6
        assert p.rounds[1].computed_stitch_count == 18
        assert p.rounds[2].computed_stitch_count == 24
    def test_context(self):
        p = parse_pattern("Round 1: 6 sc into magic ring (6)\nRound 2: inc in each st around (12)")
        assert p.rounds[1].compute_stitch_count_with_context(6) == 12

class TestMath:
    def test_inc(self):
        from crochet_checker.model.instruction import ParsedOperation
        op = ParsedOperation(stitch_type=StitchType.INCREASE, count=1)
        assert op.stitches_produced == 2; assert op.stitches_consumed == 1
    def test_dec(self):
        from crochet_checker.model.instruction import ParsedOperation
        op = ParsedOperation(stitch_type=StitchType.DECREASE, count=1)
        assert op.stitches_produced == 1; assert op.stitches_consumed == 2
    def test_decreases(self):
        p = parse_pattern("Round 1: (4 sc, dec) x 6 (30)\nRound 2: dec x 6 (6)")
        assert p.rounds[0].computed_stitch_count == 30
        assert p.rounds[1].computed_stitch_count == 6
