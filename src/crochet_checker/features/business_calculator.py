"""
Business Calculator - Wholesale pricing, shipping, and market booth planning
"""
import json
import math
from typing import Dict, List, Optional
from dataclasses import dataclass, field, asdict
from pathlib import Path


class WholesaleCalculator:
    """
    Calculate wholesale, retail, and craft fair pricing
    
    Features:
    - Cost breakdown (materials, labor, overhead)
    - Wholesale pricing (typically 2x cost)
    - Retail pricing (typically 3-4x cost)
    - Craft fair booth planning
    - Bulk order discounts
    - Profit margin analysis
    """
    
    PRICING_MODELS = {
        "craft_fair": {
            "materials_multiplier": 2.0,
            "labor_rate": 15.0,
            "overhead_pct": 0.15,
            "profit_margin": 0.40,
        },
        "wholesale": {
            "materials_multiplier": 1.5,
            "labor_rate": 12.0,
            "overhead_pct": 0.10,
            "profit_margin": 0.25,
        },
        "retail": {
            "materials_multiplier": 2.5,
            "labor_rate": 18.0,
            "overhead_pct": 0.20,
            "profit_margin": 0.50,
        },
        "etsy": {
            "materials_multiplier": 2.0,
            "labor_rate": 15.0,
            "overhead_pct": 0.15,
            "profit_margin": 0.35,
            "platform_fee_pct": 0.065,
            "listing_fee": 0.20,
        },
    }
    
    def calculate_cost(self, materials_cost: float, hours: float,
                      hourly_rate: float = 15.0, overhead_pct: float = 0.15) -> Dict:
        """Calculate total cost of production"""
        labor_cost = hours * hourly_rate
        overhead = (materials_cost + labor_cost) * overhead_pct
        total_cost = materials_cost + labor_cost + overhead
        
        return {
            "materials": round(materials_cost, 2),
            "labor": round(labor_cost, 2),
            "overhead": round(overhead, 2),
            "total_cost": round(total_cost, 2),
            "hourly_rate": hourly_rate,
            "hours": hours,
        }
    
    def calculate_price(self, materials_cost: float, hours: float,
                       model: str = "retail", custom_rate: float = None) -> Dict:
        """Calculate selling price"""
        config = self.PRICING_MODELS.get(model, self.PRICING_MODELS["retail"])
        rate = custom_rate or config["labor_rate"]
        
        cost = self.calculate_cost(materials_cost, hours, rate, config["overhead_pct"])
        
        # Add profit margin
        price = cost["total_cost"] * (1 + config["profit_margin"])
        
        # Add platform fees if applicable
        fees = {}
        if "platform_fee_pct" in config:
            platform_fee = price * config["platform_fee_pct"]
            fees["platform_fee"] = round(platform_fee, 2)
            price += platform_fee
        
        if "listing_fee" in config:
            fees["listing_fee"] = config["listing_fee"]
            price += config["listing_fee"]
        
        # Round to nice price
        rounded_price = math.ceil(price)
        if rounded_price - price < 0.50:
            rounded_price -= 0.50
        
        profit = rounded_price - cost["total_cost"] - sum(fees.values())
        
        return {
            "cost_breakdown": cost,
            "base_price": round(price, 2),
            "recommended_price": rounded_price,
            "fees": fees,
            "profit": round(profit, 2),
            "profit_margin_pct": round(profit / rounded_price * 100, 1) if rounded_price > 0 else 0,
            "model": model,
        }
    
    def calculate_bulk_order(self, unit_materials: float, unit_hours: float,
                            quantity: int, discount_pct: float = 10) -> Dict:
        """Calculate bulk order pricing"""
        unit_price = self.calculate_price(unit_materials, unit_hours, "wholesale")
        
        # Volume discounts
        if quantity >= 50:
            discount_pct = max(discount_pct, 20)
        elif quantity >= 25:
            discount_pct = max(discount_pct, 15)
        elif quantity >= 10:
            discount_pct = max(discount_pct, 10)
        
        unit_wholesale = unit_price["recommended_price"] * (1 - discount_pct / 100)
        
        total_materials = unit_materials * quantity
        total_hours = unit_hours * quantity
        total_revenue = unit_wholesale * quantity
        total_cost = self.calculate_cost(total_materials, total_hours, 12.0, 0.10)["total_cost"]
        
        return {
            "quantity": quantity,
            "unit_price": round(unit_wholesale, 2),
            "discount_pct": discount_pct,
            "total_revenue": round(total_revenue, 2),
            "total_cost": round(total_cost, 2),
            "total_profit": round(total_revenue - total_cost, 2),
            "profit_margin_pct": round((total_revenue - total_cost) / total_revenue * 100, 1) if total_revenue > 0 else 0,
            "materials_needed": round(total_materials, 2),
            "hours_needed": round(total_hours, 1),
        }
    
    def craft_fair_planner(self, items: List[Dict], booth_fee: float = 50,
                          expected_visitors: int = 200) -> Dict:
        """Plan for a craft fair"""
        total_inventory_value = sum(item.get("price", 0) * item.get("quantity", 0) for item in items)
        total_items = sum(item.get("quantity", 0) for item in items)
        total_cost = sum(
            self.calculate_cost(item.get("materials", 0), item.get("hours", 0))["total_cost"] * item.get("quantity", 0)
            for item in items
        )
        
        # Sales estimates
        conversion_rate = 0.05  # 5% of visitors buy
        estimated_sales = int(expected_visitors * conversion_rate)
        avg_item_price = total_inventory_value / max(1, total_items)
        estimated_revenue = estimated_sales * avg_item_price
        
        return {
            "inventory": {
                "total_items": total_items,
                "total_value": round(total_inventory_value, 2),
                "total_cost": round(total_cost, 2),
                "items_by_type": {item.get("name", "Unknown"): item.get("quantity", 0) for item in items},
            },
            "costs": {
                "booth_fee": booth_fee,
                "production_cost": round(total_cost, 2),
                "total_costs": round(total_cost + booth_fee, 2),
            },
            "projections": {
                "expected_visitors": expected_visitors,
                "conversion_rate": f"{conversion_rate * 100}%",
                "estimated_sales": estimated_sales,
                "avg_price": round(avg_item_price, 2),
                "estimated_revenue": round(estimated_revenue, 2),
                "estimated_profit": round(estimated_revenue - total_cost - booth_fee, 2),
            },
            "break_even": math.ceil((total_cost + booth_fee) / max(1, avg_item_price)),
        }


class ShippingCalculator:
    """
    Calculate shipping costs for crochet items
    
    Features:
    - Package size estimator
    - Weight calculator
    - Domestic/international rates
    - Free shipping threshold
    - Shipping profit impact
    """
    
    ITEM_WEIGHTS = {
        "amigurumi_small": {"weight_oz": 3, "box": "small"},
        "amigurumi_medium": {"weight_oz": 8, "box": "medium"},
        "amigurumi_large": {"weight_oz": 16, "box": "large"},
        "scarf": {"weight_oz": 6, "box": "flat"},
        "hat": {"weight_oz": 4, "box": "small"},
        "blanket_small": {"weight_oz": 24, "box": "large"},
        "blanket_large": {"weight_oz": 48, "box": "xlarge"},
        "dishcloth": {"weight_oz": 2, "box": "flat"},
        "bag": {"weight_oz": 8, "box": "medium"},
    }
    
    BOX_SIZES = {
        "flat": {"l": 10, "w": 7, "h": 1, "name": "Flat Mailer"},
        "small": {"l": 8, "w": 6, "h": 4, "name": "Small Box"},
        "medium": {"l": 12, "w": 9, "h": 6, "name": "Medium Box"},
        "large": {"l": 16, "w": 12, "h": 8, "name": "Large Box"},
        "xlarge": {"l": 20, "w": 16, "h": 10, "name": "Extra Large Box"},
    }
    
    # Estimated shipping rates (USPS 2024)
    DOMESTIC_RATES = {
        "flat": 4.50,
        "small": 8.00,
        "medium": 12.00,
        "large": 18.00,
        "xlarge": 25.00,
    }
    
    INTERNATIONAL_MULTIPLIER = 2.5
    
    def estimate_weight(self, item_type: str, quantity: int = 1) -> Dict:
        """Estimate package weight"""
        item = self.ITEM_WEIGHTS.get(item_type, {"weight_oz": 8, "box": "medium"})
        
        total_oz = item["weight_oz"] * quantity
        packaging_oz = 2  # packaging material
        
        return {
            "item_weight_oz": item["weight_oz"] * quantity,
            "packaging_oz": packaging_oz,
            "total_weight_oz": total_oz + packaging_oz,
            "total_weight_lbs": round((total_oz + packaging_oz) / 16, 2),
            "box_type": item["box"],
        }
    
    def calculate_shipping(self, item_type: str = "amigurumi_medium",
                          quantity: int = 1, domestic: bool = True,
                          include_packaging: bool = True) -> Dict:
        """Calculate shipping cost"""
        weight = self.estimate_weight(item_type, quantity)
        box_type = weight["box_type"]
        
        base_rate = self.DOMESTIC_RATES.get(box_type, 12.00)
        
        if not domestic:
            base_rate *= self.INTERNATIONAL_MULTIPLIER
        
        # Weight surcharge for heavy items
        if weight["total_weight_lbs"] > 1:
            base_rate += (weight["total_weight_lbs"] - 1) * 1.50
        
        packaging_cost = 2.00 if include_packaging else 0
        
        return {
            "item_type": item_type,
            "quantity": quantity,
            "weight": weight,
            "box": self.BOX_SIZES.get(box_type, {}),
            "shipping_cost": round(base_rate, 2),
            "packaging_cost": packaging_cost,
            "total_shipping": round(base_rate + packaging_cost, 2),
            "domestic": domestic,
        }
    
    def suggest_free_shipping_threshold(self, avg_item_price: float,
                                       avg_shipping: float,
                                       profit_margin_target: float = 0.30) -> Dict:
        """Suggest a free shipping threshold"""
        # At what order value can you absorb shipping?
        min_order = avg_shipping / (1 - profit_margin_target)
        suggested = math.ceil(min_order / 5) * 5  # Round up to nearest $5
        
        return {
            "avg_shipping_cost": avg_shipping,
            "target_margin": f"{profit_margin_target * 100}%",
            "minimum_order": round(min_order, 2),
            "suggested_threshold": suggested,
            "explanation": f"Set free shipping at ${suggested}+ to maintain {profit_margin_target*100:.0f}% margin",
        }
    
    def compare_carriers(self, item_type: str, weight_lbs: float,
                        domestic: bool = True) -> List[Dict]:
        """Compare shipping across carriers"""
        weight = self.estimate_weight(item_type)
        box = weight["box_type"]
        base = self.DOMESTIC_RATES.get(box, 12.00)
        
        if not domestic:
            base *= self.INTERNATIONAL_MULTIPLIER
        
        carriers = [
            {"name": "USPS First Class", "cost": round(base * 0.8, 2), "days": "3-5", "tracking": True},
            {"name": "USPS Priority", "cost": round(base, 2), "days": "1-3", "tracking": True},
            {"name": "USPS Priority Express", "cost": round(base * 2.0, 2), "days": "1-2", "tracking": True},
            {"name": "UPS Ground", "cost": round(base * 1.1, 2), "days": "3-5", "tracking": True},
            {"name": "FedEx Ground", "cost": round(base * 1.15, 2), "days": "3-5", "tracking": True},
        ]
        
        if not domestic:
            carriers = [
                {"name": "USPS International", "cost": round(base, 2), "days": "7-21", "tracking": True},
                {"name": "USPS Priority Intl", "cost": round(base * 1.5, 2), "days": "6-10", "tracking": True},
                {"name": "UPS Worldwide", "cost": round(base * 2.5, 2), "days": "3-5", "tracking": True},
            ]
        
        return sorted(carriers, key=lambda c: c["cost"])


# Demo
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  BUSINESS CALCULATOR - DEMONSTRATION")
    print("=" * 60)
    
    # Wholesale Calculator
    ws = WholesaleCalculator()
    
    print("\n💰 PRICING CALCULATION")
    print("─" * 40)
    
    price = ws.calculate_price(materials_cost=12.0, hours=5, model="retail")
    print(f"  Item: Amigurumi Bunny")
    print(f"  Materials: ${price['cost_breakdown']['materials']}")
    print(f"  Labor: ${price['cost_breakdown']['labor']} ({price['cost_breakdown']['hours']}h)")
    print(f"  Overhead: ${price['cost_breakdown']['overhead']}")
    print(f"  Total Cost: ${price['cost_breakdown']['total_cost']}")
    print(f"  → Recommended Price: ${price['recommended_price']}")
    print(f"  → Profit: ${price['profit']} ({price['profit_margin_pct']}%)")
    
    print(f"\n📦 BULK ORDER (25 units)")
    print("─" * 40)
    bulk = ws.calculate_bulk_order(12.0, 5, 25, discount_pct=10)
    print(f"  Unit Price: ${bulk['unit_price']}")
    print(f"  Discount: {bulk['discount_pct']}%")
    print(f"  Total Revenue: ${bulk['total_revenue']}")
    print(f"  Total Profit: ${bulk['total_profit']}")
    print(f"  Hours Needed: {bulk['hours_needed']}h")
    
    print(f"\n🏪 CRAFT FAIR PLANNER")
    print("─" * 40)
    items = [
        {"name": "Amigurumi Bunny", "price": 25, "quantity": 10, "materials": 12, "hours": 5},
        {"name": "Scarf", "price": 35, "quantity": 5, "materials": 8, "hours": 4},
        {"name": "Dishcloth Set", "price": 12, "quantity": 15, "materials": 3, "hours": 1},
    ]
    fair = ws.craft_fair_planner(items, booth_fee=50, expected_visitors=200)
    print(f"  Inventory: {fair['inventory']['total_items']} items (${fair['inventory']['total_value']})")
    print(f"  Costs: ${fair['costs']['total_costs']}")
    print(f"  Projected Sales: {fair['projections']['estimated_sales']}")
    print(f"  Estimated Revenue: ${fair['projections']['estimated_revenue']}")
    print(f"  Estimated Profit: ${fair['projections']['estimated_profit']}")
    print(f"  Break-even: {fair['break_even']} sales needed")
    
    # Shipping Calculator
    ship = ShippingCalculator()
    
    print(f"\n📬 SHIPPING CALCULATOR")
    print("─" * 40)
    shipping = ship.calculate_shipping("amigurumi_medium", domestic=True)
    print(f"  Weight: {shipping['weight']['total_weight_oz']}oz")
    print(f"  Box: {shipping['box'].get('name', 'Medium')}")
    print(f"  Shipping: ${shipping['shipping_cost']}")
    print(f"  Packaging: ${shipping['packaging_cost']}")
    print(f"  Total: ${shipping['total_shipping']}")
    
    print(f"\n🚚 Compare Carriers:")
    carriers = ship.compare_carriers("amigurumi_medium", 0.5)
    for c in carriers:
        print(f"  • {c['name']}: ${c['cost']} ({c['days']} days)")
    
    print(f"\n🎁 Free Shipping Threshold:")
    threshold = ship.suggest_free_shipping_threshold(25.0, 10.0)
    print(f"  {threshold['explanation']}")
    
    print(f"\n  Business Calculator Complete! 💼")
