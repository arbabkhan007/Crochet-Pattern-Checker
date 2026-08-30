"""Tests for AI module."""
from crochet_checker.parser.parser import parse_pattern
from crochet_checker.validation import validate_pattern
from crochet_checker.ai import (PatternExplainer, explain_pattern, TerminologyTranslator,
    translate_pattern, SuggestionEngine, generate_suggestions, DescriptionGenerator, generate_description)

P = "Round 1: 6 sc into magic ring (6)" + chr(10) + "Round 2: (sc, inc) x 6 (18)" + chr(10) + "Round 3: (2 sc, inc) x 6 (24)"

class TestExplainer:
    def test_explain(self):
        p,r = parse_pattern(P), validate_pattern(parse_pattern(P))
        res = explain_pattern(p, r)
        assert res.summary != "" and res.explanation != ""
    def test_highlights(self):
        p,r = parse_pattern(P), validate_pattern(parse_pattern(P))
        assert len(explain_pattern(p,r).highlights) > 0
    def test_recommendations(self):
        p,r = parse_pattern(P), validate_pattern(parse_pattern(P))
        assert len(explain_pattern(p,r).recommendations) > 0
    def test_shape(self):
        p,r = parse_pattern(P), validate_pattern(parse_pattern(P))
        assert explain_pattern(p,r).shape_guess != ""
    def test_difficulty(self):
        p,r = parse_pattern(P), validate_pattern(parse_pattern(P))
        assert explain_pattern(p,r).difficulty_explanation != ""

class TestTranslator:
    def test_us_to_uk_sc(self):
        assert "dc" in translate_pattern("6 sc", "US", "UK").translated_text.lower()
    def test_us_to_uk_dc(self):
        assert "tr" in translate_pattern("4 dc", "US", "UK").translated_text.lower()
    def test_uk_to_us_dc(self):
        assert "sc" in translate_pattern("6 dc", "UK", "US").translated_text.lower()
    def test_preserves_text(self):
        r = translate_pattern("Round 1: 6 sc into magic ring (6)", "US", "UK")
        assert "Round 1" in r.translated_text and "magic ring" in r.translated_text
    def test_changes_tracked(self):
        r = translate_pattern("6 sc, 4 dc", "US", "UK")
        assert r.num_changes > 0
    def test_case(self):
        assert "DC" in translate_pattern("SC", "US", "UK").translated_text

class TestSuggestions:
    def test_valid(self):
        p,r = parse_pattern(P), validate_pattern(parse_pattern(P))
        assert isinstance(generate_suggestions(p, r), list)
    def test_with_errors(self):
        bad = "Round 1: 6 sc into magic ring (6)" + chr(10) + "Round 2: sc around (7)"
        p,r = parse_pattern(bad), validate_pattern(parse_pattern(bad))
        if r.errors: assert len(generate_suggestions(p,r)) > 0

class TestDescription:
    def test_generates(self):
        d = generate_description(parse_pattern(P))
        assert d.title != "" and d.short_description != ""
    def test_skill(self):
        assert "beginner" in generate_description(parse_pattern(P)).skill_level.lower() or "easy" in generate_description(parse_pattern(P)).skill_level.lower()
    def test_size(self):
        assert "not determined" not in generate_description(parse_pattern(P)).finished_size.lower()
    def test_tags(self):
        assert "crochet" in generate_description(parse_pattern(P)).tags
    def test_materials(self):
        assert len(generate_description(parse_pattern(P)).materials_list) > 0
    def test_features(self):
        assert len(generate_description(parse_pattern(P)).features) > 0
