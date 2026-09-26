"""Image support for PDF generation."""

from pathlib import Path


def generate_pattern_images(pattern, output_dir: str) -> list[str]:
    """Generate all images for a pattern."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    images = []

    # For now, just return empty list
    # Full implementation would generate SVG charts
    print(f"📊 Image generation placeholder - would create images in {output_dir}/")

    return images
