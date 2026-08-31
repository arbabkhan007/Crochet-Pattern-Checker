"""Tests for image generation."""
from crochet_checker.image import ImageProvider, ImageConfig, generate_pattern_image

class TestImage:
    def test_placeholder(self):
        r = ImageProvider(ImageConfig(provider="placeholder")).generate_cover_image("Test", "hat")
        assert "<svg" in r
    def test_category_icons(self):
        p = ImageProvider(ImageConfig(provider="placeholder"))
        assert "<svg" in p.generate_cover_image("B", "hat")
        assert "<svg" in p.generate_cover_image("S", "scarf")
    def test_convenience(self):
        assert "<svg" in generate_pattern_image("T", "scarf")
    def test_deterministic(self):
        p = ImageProvider(ImageConfig(provider="placeholder"))
        assert p.generate_cover_image("A", "") == p.generate_cover_image("A", "")
        assert p.generate_cover_image("A", "") != p.generate_cover_image("B", "")
