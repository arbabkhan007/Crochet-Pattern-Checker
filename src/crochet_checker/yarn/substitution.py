"""Yarn substitution engine."""
from pydantic import BaseModel
from typing import List

class YarnProperties(BaseModel):
    """Yarn properties."""
    name: str
    brand: str
    weight: str = "worsted"
    fiber: str = "acrylic"
    yardage: int = 200
    price_usd: float = 5.99

class SubstitutionResult(BaseModel):
    """A yarn substitution result."""
    substitute_yarn: YarnProperties
    compatibility_score: int = 100
    pros: List[str] = []
    cons: List[str] = []

class YarnSubstitutionEngine:
    """Find yarn substitutes."""
    
    def find_substitutes(self, yarn: YarnProperties, max_results: int = 3) -> List[SubstitutionResult]:
        """Find substitute yarns."""
        # Return some sample substitutes
        return [
            SubstitutionResult(
                substitute_yarn=YarnProperties(
                    name="Heartland", brand="Lion Brand",
                    weight=yarn.weight, fiber=yarn.fiber
                ),
                compatibility_score=100,
                pros=["Same weight", "Similar gauge"]
            )
        ]
