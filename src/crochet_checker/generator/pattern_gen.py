"""Pattern generator."""


class PatternGenerator:
    """Generate patterns."""

    def generate_amigurumi(self, description: str, **kwargs) -> dict:
        """Generate an amigurumi pattern."""
        return {
            "title": description.title(),
            "description": f"Amigurumi {description}",
            "rounds": 18,
            "estimated_time_hours": 2.7,
        }
