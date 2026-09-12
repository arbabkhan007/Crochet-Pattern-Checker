"""
Crochet Budget Planner - Track spending on yarn, hooks, patterns, and calculate ROI
"""
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List


class CrochetBudgetPlanner:
    """Track crochet expenses and calculate profitability"""
    
    def __init__(self, data_file: str = "crochet_budget.json"):
        self.data_file = Path(data_file)
        self.data = self._load_data()
    
    def _load_data(self):
        if self.data_file.exists():
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return {
            "expenses": [],
            "income": [],
            "projects": [],
            "monthly_budget": 200.0
        }
    
    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def add_expense(self, category: str, amount: float, description: str, date: str = None):
        """Add an expense (yarn, hooks, patterns, etc.)"""
        expense = {
            "category": category,  # yarn, hooks, patterns, tools, other
            "amount": amount,
            "description": description,
            "date": date or datetime.now().strftime("%Y-%m-%d")
        }
        self.data["expenses"].append(expense)
        self.save_data()
    
    def add_income(self, source: str, amount: float, description: str, date: str = None):
        """Add income (sales, commissions, etc.)"""
        income = {
            "source": source,  # sales, commissions, teaching, other
            "amount": amount,
            "description": description,
            "date": date or datetime.now().strftime("%Y-%m-%d")
        }
        self.data["income"].append(income)
        self.save_data()
    
    def add_project_cost(self, project_name: str, materials_cost: float, 
                         hours_spent: float, hourly_rate: float = 15.0):
        """Track project costs for pricing"""
        labor_cost = hours_spent * hourly_rate
        total_cost = materials_cost + labor_cost
        
        project = {
            "name": project_name,
            "materials_cost": materials_cost,
            "hours_spent": hours_spent,
            "hourly_rate": hourly_rate,
            "labor_cost": labor_cost,
            "total_cost": total_cost,
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        self.data["projects"].append(project)
        self.save_data()
        return project
    
    def calculate_suggested_price(self, materials_cost: float, hours: float, 
                                  hourly_rate: float = 15.0, profit_margin: float = 0.30) -> Dict:
        """Calculate suggested selling price"""
        labor = hours * hourly_rate
        total_cost = materials_cost + labor
        profit = total_cost * profit_margin
        suggested_price = total_cost + profit
        
        return {
            "materials": materials_cost,
            "labor": labor,
            "total_cost": total_cost,
            "profit": profit,
            "suggested_price": suggested_price,
            "hourly_rate": hourly_rate,
            "profit_margin": profit_margin
        }
    
    def get_financial_summary(self) -> Dict:
        """Get overall financial summary"""
        total_expenses = sum(e["amount"] for e in self.data["expenses"])
        total_income = sum(i["amount"] for i in self.data["income"])
        net_profit = total_income - total_expenses
        
        # By category
        expenses_by_category = {}
        for e in self.data["expenses"]:
            cat = e["category"]
            expenses_by_category[cat] = expenses_by_category.get(cat, 0) + e["amount"]
        
        # Monthly breakdown
        monthly_expenses = {}
        for e in self.data["expenses"]:
            month = e["date"][:7]
            monthly_expenses[month] = monthly_expenses.get(month, 0) + e["amount"]
        
        return {
            "total_expenses": total_expenses,
            "total_income": total_income,
            "net_profit": net_profit,
            "expenses_by_category": expenses_by_category,
            "monthly_expenses": monthly_expenses,
            "monthly_budget": self.data["monthly_budget"],
            "budget_remaining": self.data["monthly_budget"] - sum(
                e["amount"] for e in self.data["expenses"]
                if e["date"].startswith(datetime.now().strftime("%Y-%m"))
            )
        }
    
    def generate_budget_report(self) -> str:
        """Generate text-based budget report"""
        summary = self.get_financial_summary()
        
        report = f"""
╔══════════════════════════════════════════════════════════╗
║           🧶 CROCHET BUDGET REPORT                        ║
╚══════════════════════════════════════════════════════════╝

💰 FINANCIAL OVERVIEW
═══════════════════════════════════════════════════════════
  Total Income:      ${summary['total_income']:>10.2f}
  Total Expenses:    ${summary['total_expenses']:>10.2f}
  Net Profit:        ${summary['net_profit']:>10.2f}
  
  Monthly Budget:    ${summary['monthly_budget']:>10.2f}
  Budget Remaining:  ${summary['budget_remaining']:>10.2f}

📊 EXPENSES BY CATEGORY
═══════════════════════════════════════════════════════════
"""
        for category, amount in sorted(summary['expenses_by_category'].items()):
            bar = "█" * int(amount / 10)
            report += f"  {category:12s} ${amount:>8.2f} {bar}\n"
        
        report += f"""
📈 MONTHLY SPENDING
═══════════════════════════════════════════════════════════
"""
        for month, amount in sorted(summary['monthly_expenses'].items()):
            report += f"  {month}: ${amount:>8.2f}\n"
        
        return report


if __name__ == "__main__":
    print("💰 Crochet Budget Planner")
    print("=" * 50)
    
    planner = CrochetBudgetPlanner()
    
    # Add sample expenses
    print("\n💸 Adding expenses...")
    planner.add_expense("yarn", 45.00, "Red Heart Super Saver (10 skeins)")
    planner.add_expense("hooks", 25.00, "Set of aluminum hooks")
    planner.add_expense("patterns", 12.00, "3 premium patterns")
    planner.add_expense("tools", 18.00, "Stitch markers and tapestry needles")
    
    # Add sample income
    print("\n💵 Adding income...")
    planner.add_income("sales", 150.00, "Sold 3 custom scarves")
    planner.add_income("commissions", 200.00, "Custom blanket order")
    
    # Calculate pricing
    print("\n🏷️ Pricing a project:")
    pricing = planner.calculate_suggested_price(
        materials_cost=35.00,
        hours=12.0,
        hourly_rate=15.0,
        profit_margin=0.30
    )
    print(f"  Materials: ${pricing['materials']:.2f}")
    print(f"  Labor: ${pricing['labor']:.2f}")
    print(f"  Total Cost: ${pricing['total_cost']:.2f}")
    print(f"  Profit (30%): ${pricing['profit']:.2f}")
    print(f"  Suggested Price: ${pricing['suggested_price']:.2f}")
    
    # Show report
    print("\n📊 Budget Report:")
    print(planner.generate_budget_report())
    
    print("\n✅ Budget Planner ready!")
