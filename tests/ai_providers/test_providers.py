"""Tests for AI providers."""
from crochet_checker.parser.parser import parse_pattern
from crochet_checker.validation import validate_pattern
from crochet_checker.ai_providers import AIProvider, AIConfig

P = "Round 1: 6 sc into magic ring (6)" + chr(10) + "Round 2: (sc, inc) x 6 (18)" + chr(10) + "Round 3: (2 sc, inc) x 6 (24)"

class TestAI:
    def test_rule_explain(self):
        p, r = parse_pattern(P), validate_pattern(parse_pattern(P))
        assert len(AIProvider(AIConfig(provider="rule_based")).explain_pattern(p, r)) > 0
    def test_suggestions(self):
        p, r = parse_pattern(P), validate_pattern(parse_pattern(P))
        assert isinstance(AIProvider(AIConfig()).suggest_fixes(p, r), list)
    def test_translate(self):
        assert "dc" in AIProvider(AIConfig()).translate_terminology("6 sc", "US", "UK").lower()
    def test_fallback(self):
        p, r = parse_pattern(P), validate_pattern(parse_pattern(P))
        assert len(AIProvider(AIConfig(provider="openai", api_key=None)).explain_pattern(p, r)) > 0
    def test_defaults(self):
        assert AIConfig().provider == "rule_based"
