"""Cost calculator."""
from pydantic import BaseModel

class CostBreakdown(BaseModel):
    """Cost breakdown."""
    total_labor_cost: float = 0.0
    platform_fees: float = 0.0
    total_production_cost: float = 0.0

class PricingRecommendation(BaseModel):
    """Pricing recommendation."""
    suggested_price: float = 8.0
    profit_margin: float = 50.0

class CostCalculator:
    """Calculate costs."""
    
    def calculate_pattern_costs(self, **kwargs) -> CostBreakdown:
        """Calculate pattern costs."""
        labor = kwargs.get('design_time_hours', 8) * kwargs.get('hourly_rate', 15)
        return CostBreakdown(
            total_labor_cost=labor,
            platform_fees=0.20,
            total_production_cost=labor + 0.20
        )
    
    def suggest_pattern_pricing(self, costs: CostBreakdown, **kwargs) -> PricingRecommendation:
        """Suggest pricing."""
        return PricingRecommendation(
            suggested_price=8.0,
            profit_margin=50.0
        )
