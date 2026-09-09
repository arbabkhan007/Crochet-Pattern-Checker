"""
Order Manager - Track custom orders, deadlines, pricing, customers
"""
import json
from typing import Dict, List, Optional
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from pathlib import Path


@dataclass
class Customer:
    id: str
    name: str
    email: str = ""
    phone: str = ""
    instagram: str = ""
    address: str = ""
    notes: str = ""
    total_orders: int = 0
    total_spent: float = 0
    created_at: str = ""
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().strftime("%Y-%m-%d")
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class Order:
    id: str
    customer_id: str
    item_name: str
    description: str = ""
    pattern_used: str = ""
    quantity: int = 1
    price_per_item: float = 0
    total_price: float = 0
    deposit_paid: float = 0
    balance_due: float = 0
    
    # Status
    status: str = "inquiry"  # inquiry, confirmed, in_progress, finished, shipped, delivered, cancelled
    priority: str = "normal"  # low, normal, high, rush
    
    # Dates
    order_date: str = ""
    deadline: str = ""
    shipped_date: str = ""
    delivered_date: str = ""
    
    # Details
    colors: List[str] = field(default_factory=list)
    yarn_used: str = ""
    hook_size: str = ""
    size: str = ""
    special_requests: str = ""
    
    # Tracking
    estimated_hours: float = 0
    actual_hours: float = 0
    materials_cost: float = 0
    profit: float = 0
    
    notes: str = ""
    
    def __post_init__(self):
        if not self.order_date:
            self.order_date = datetime.now().strftime("%Y-%m-%d")
        if not self.total_price:
            self.total_price = self.price_per_item * self.quantity
        if not self.balance_due:
            self.balance_due = self.total_price - self.deposit_paid
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @property
    def days_until_deadline(self) -> Optional[int]:
        if not self.deadline:
            return None
        dl = datetime.strptime(self.deadline, "%Y-%m-%d")
        return (dl - datetime.now()).days
    
    @property
    def hourly_rate(self) -> float:
        if self.actual_hours > 0:
            return (self.total_price - self.materials_cost) / self.actual_hours
        return 0


class OrderManager:
    """
    Manage custom crochet orders
    
    Features:
    - Customer management
    - Order tracking with statuses
    - Deadline management with alerts
    - Pricing calculator
    - Profit tracking
    - Order history
    - Invoice generation
    """
    
    PRICING_FACTORS = {
        "difficulty_multiplier": {
            "Beginner": 1.0,
            "Advanced Beginner": 1.2,
            "Intermediate": 1.5,
            "Advanced": 2.0,
            "Expert": 2.5,
        },
        "base_hourly_rate": 15.0,  # $/hour
        "minimum_order": 20.0,
        "rush_fee_multiplier": 1.5,
        "custom_design_fee": 25.0,
    }
    
    STATUS_FLOW = [
        "inquiry", "confirmed", "in_progress", 
        "finished", "shipped", "delivered"
    ]
    
    STATUS_ICONS = {
        "inquiry": "💬",
        "confirmed": "✅",
        "in_progress": "🧶",
        "finished": "📦",
        "shipped": "🚚",
        "delivered": "🎉",
        "cancelled": "❌",
    }
    
    def __init__(self, storage_path: str = "orders.json"):
        self.storage_path = Path(storage_path)
        self.customers: Dict[str, Customer] = {}
        self.orders: Dict[str, Order] = {}
        self._next_customer_id = 1
        self._next_order_id = 1
        self.load()
    
    def load(self):
        if self.storage_path.exists():
            try:
                data = json.loads(self.storage_path.read_text())
                for k, v in data.get("customers", {}).items():
                    self.customers[k] = Customer(**v)
                for k, v in data.get("orders", {}).items():
                    self.orders[k] = Order(**v)
                self._next_customer_id = data.get("next_customer_id", 1)
                self._next_order_id = data.get("next_order_id", 1)
            except Exception:
                pass
    
    def save(self):
        data = {
            "customers": {k: v.to_dict() for k, v in self.customers.items()},
            "orders": {k: v.to_dict() for k, v in self.orders.items()},
            "next_customer_id": self._next_customer_id,
            "next_order_id": self._next_order_id,
        }
        self.storage_path.write_text(json.dumps(data, indent=2))
    
    # ════════════════════════════════════════════════════
    # CUSTOMER MANAGEMENT
    # ════════════════════════════════════════════════════
    
    def add_customer(self, name: str, email: str = "", **kwargs) -> str:
        """Add a new customer"""
        cid = f"C{self._next_customer_id:04d}"
        self._next_customer_id += 1
        
        customer = Customer(id=cid, name=name, email=email, **kwargs)
        self.customers[cid] = customer
        self.save()
        return cid
    
    def get_customer_orders(self, customer_id: str) -> List[Order]:
        """Get all orders for a customer"""
        return [o for o in self.orders.values() if o.customer_id == customer_id]
    
    # ════════════════════════════════════════════════════
    # ORDER MANAGEMENT
    # ════════════════════════════════════════════════════
    
    def create_order(self, customer_id: str, item_name: str,
                    price: float = 0, deadline: str = "",
                    **kwargs) -> str:
        """Create a new order"""
        oid = f"ORD{self._next_order_id:04d}"
        self._next_order_id += 1
        
        order = Order(
            id=oid,
            customer_id=customer_id,
            item_name=item_name,
            total_price=price,
            deadline=deadline,
            **kwargs
        )
        self.orders[oid] = order
        self.save()
        return oid
    
    def update_status(self, order_id: str, status: str) -> bool:
        """Update order status"""
        if order_id not in self.orders:
            return False
        self.orders[order_id].status = status
        
        if status == "shipped":
            self.orders[order_id].shipped_date = datetime.now().strftime("%Y-%m-%d")
        elif status == "delivered":
            self.orders[order_id].delivered_date = datetime.now().strftime("%Y-%m-%d")
        
        self.save()
        return True
    
    def advance_status(self, order_id: str) -> bool:
        """Move order to next status"""
        if order_id not in self.orders:
            return False
        
        current = self.orders[order_id].status
        if current in self.STATUS_FLOW:
            idx = self.STATUS_FLOW.index(current)
            if idx < len(self.STATUS_FLOW) - 1:
                self.orders[order_id].status = self.STATUS_FLOW[idx + 1]
                self.save()
                return True
        return False
    
    # ════════════════════════════════════════════════════
    # PRICING
    # ════════════════════════════════════════════════════
    
    def calculate_price(self, estimated_hours: float, materials_cost: float,
                       difficulty: str = "Intermediate",
                       is_rush: bool = False,
                       is_custom_design: bool = False) -> Dict:
        """Calculate recommended price for an order"""
        hourly_rate = self.PRICING_FACTORS["base_hourly_rate"]
        diff_mult = self.PRICING_FACTORS["difficulty_multiplier"].get(difficulty, 1.5)
        
        labor_cost = estimated_hours * hourly_rate * diff_mult
        total_cost = labor_cost + materials_cost
        
        if is_rush:
            total_cost *= self.PRICING_FACTORS["rush_fee_multiplier"]
        
        if is_custom_design:
            total_cost += self.PRICING_FACTORS["custom_design_fee"]
        
        profit_margin = total_cost * 0.3  # 30% profit margin
        recommended_price = total_cost + profit_margin
        
        return {
            "labor_cost": round(labor_cost, 2),
            "materials_cost": round(materials_cost, 2),
            "subtotal": round(total_cost, 2),
            "profit_margin": round(profit_margin, 2),
            "recommended_price": round(max(recommended_price, self.PRICING_FACTORS["minimum_order"]), 2),
            "hourly_rate": hourly_rate,
            "difficulty_multiplier": diff_mult,
            "rush_fee": is_rush,
            "custom_design_fee": is_custom_design,
        }
    
    # ════════════════════════════════════════════════════
    # DASHBOARD
    # ════════════════════════════════════════════════════
    
    def get_dashboard(self) -> Dict:
        """Get business dashboard"""
        active_orders = [o for o in self.orders.values() 
                        if o.status not in ("delivered", "cancelled")]
        
        urgent = [o for o in active_orders 
                 if o.days_until_deadline is not None and o.days_until_deadline <= 7]
        
        revenue = sum(o.total_price for o in self.orders.values() 
                     if o.status in ("delivered", "shipped"))
        
        profit = sum(o.total_price - o.materials_cost for o in self.orders.values()
                    if o.status in ("delivered", "shipped"))
        
        by_status = {}
        for o in self.orders.values():
            by_status[o.status] = by_status.get(o.status, 0) + 1
        
        return {
            "total_customers": len(self.customers),
            "total_orders": len(self.orders),
            "active_orders": len(active_orders),
            "urgent_orders": len(urgent),
            "total_revenue": round(revenue, 2),
            "total_profit": round(profit, 2),
            "by_status": by_status,
            "avg_order_value": round(revenue / max(1, len(self.orders)), 2),
        }
    
    def get_urgent_orders(self) -> List[Dict]:
        """Get orders with upcoming deadlines"""
        urgent = []
        for o in self.orders.values():
            if o.status in ("delivered", "cancelled"):
                continue
            if o.days_until_deadline is not None and o.days_until_deadline <= 14:
                customer = self.customers.get(o.customer_id)
                urgent.append({
                    "order_id": o.id,
                    "item": o.item_name,
                    "customer": customer.name if customer else "Unknown",
                    "deadline": o.deadline,
                    "days_left": o.days_until_deadline,
                    "status": o.status,
                    "urgency": "🔴" if o.days_until_deadline <= 3 else "🟡" if o.days_until_deadline <= 7 else "🟢",
                })
        
        return sorted(urgent, key=lambda x: x["days_left"])
    
    def generate_invoice(self, order_id: str) -> str:
        """Generate an invoice HTML"""
        order = self.orders.get(order_id)
        if not order:
            return "Order not found"
        
        customer = self.customers.get(order.customer_id)
        cust_name = customer.name if customer else "Customer"
        
        html = f'''<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Invoice {order.id}</title>
<style>
body {{ font-family: Georgia, serif; max-width: 700px; margin: 40px auto; padding: 20px; color: #333; }}
.header {{ border-bottom: 3px solid #E94560; padding-bottom: 20px; margin-bottom: 30px; }}
.header h1 {{ color: #E94560; margin: 0; }}
.header p {{ color: #666; margin: 5px 0; }}
.invoice-info {{ display: flex; justify-content: space-between; margin-bottom: 30px; }}
table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
th {{ background: #1A1A2E; color: white; padding: 12px; text-align: left; }}
td {{ padding: 12px; border-bottom: 1px solid #eee; }}
.total {{ font-size: 1.3em; font-weight: bold; text-align: right; margin-top: 20px; }}
.deposit {{ color: #4ECCA3; }}
.balance {{ color: #E94560; font-size: 1.5em; }}
.footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; color: #888; font-size: 0.9em; }}
</style></head>
<body>
<div class="header">
    <h1>INVOICE</h1>
    <p>Invoice #{order.id}</p>
    <p>Date: {order.order_date}</p>
</div>

<div class="invoice-info">
    <div>
        <strong>Bill To:</strong><br>
        {cust_name}<br>
        {customer.email if customer else ''}<br>
        {customer.phone if customer else ''}
    </div>
    <div style="text-align: right;">
        <strong>Due Date:</strong><br>
        {order.deadline or 'TBD'}<br>
        <strong>Status:</strong> {order.status.replace('_', ' ').title()}
    </div>
</div>

<table>
    <tr><th>Item</th><th>Qty</th><th style="text-align:right">Price</th></tr>
    <tr>
        <td>{order.item_name}<br><small style="color:#888">{order.description}</small></td>
        <td>{order.quantity}</td>
        <td style="text-align:right">${order.total_price:.2f}</td>
    </tr>
</table>

<div class="total">
    <p>Total: ${order.total_price:.2f}</p>
    <p class="deposit">Deposit Paid: -${order.deposit_paid:.2f}</p>
    <p class="balance">Balance Due: ${order.balance_due:.2f}</p>
</div>

<div class="footer">
    <p>Thank you for your order!</p>
    <p>Questions? Contact us for details.</p>
</div>
</body></html>'''
        
        return html
    
    def display_dashboard(self):
        """Display business dashboard"""
        dash = self.get_dashboard()
        
        print(f"\n{'=' * 60}")
        print(f"  CROCHET BUSINESS DASHBOARD")
        print(f"{'=' * 60}")
        
        print(f"\n  📊 OVERVIEW")
        print(f"  {'─' * 40}")
        print(f"  Customers:       {dash['total_customers']}")
        print(f"  Total Orders:    {dash['total_orders']}")
        print(f"  Active Orders:   {dash['active_orders']}")
        print(f"  Urgent (≤7 days): {dash['urgent_orders']}")
        
        print(f"\n  💰 FINANCIALS")
        print(f"  {'─' * 40}")
        print(f"  Revenue:         ${dash['total_revenue']:.2f}")
        print(f"  Profit:          ${dash['total_profit']:.2f}")
        print(f"  Avg Order:       ${dash['avg_order_value']:.2f}")
        
        print(f"\n  📦 ORDER STATUS")
        print(f"  {'─' * 40}")
        for status, count in dash['by_status'].items():
            icon = self.STATUS_ICONS.get(status, "📋")
            print(f"  {icon} {status.replace('_', ' ').title():20s} {count}")
        
        urgent = self.get_urgent_orders()
        if urgent:
            print(f"\n  ⚠️  URGENT ORDERS")
            print(f"  {'─' * 40}")
            for o in urgent:
                print(f"  {o['urgency']} {o['item']} for {o['customer']}")
                print(f"     Due: {o['deadline']} ({o['days_left']} days) | Status: {o['status']}")


# Demo
if __name__ == "__main__":
    import os
    print("\n" + "=" * 60)
    print("  ORDER MANAGER - DEMONSTRATION")
    print("=" * 60)
    
    mgr = OrderManager(storage_path="/tmp/demo_orders.json")
    
    # Add customers
    c1 = mgr.add_customer("Sarah Johnson", "sarah@email.com", phone="555-0123")
    c2 = mgr.add_customer("Mike Chen", "mike@email.com", instagram="@mikecrochet")
    print(f"\n✅ Added 2 customers")
    
    # Create orders
    pricing = mgr.calculate_price(8, 15, "Intermediate", is_rush=True)
    
    o1 = mgr.create_order(c1, "Custom Amigurumi Bunny", 
                         price=pricing["recommended_price"],
                         deadline=(datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"),
                         colors=["White", "Pink"], size="Medium")
    
    o2 = mgr.create_order(c2, "Granny Square Blanket",
                         price=120,
                         deadline=(datetime.now() + timedelta(days=21)).strftime("%Y-%m-%d"),
                         colors=["Pastel Mix"])
    
    o3 = mgr.create_order(c1, "Baby Booties Set",
                         price=35,
                         deadline=(datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d"))
    
    mgr.update_status(o1, "in_progress")
    mgr.update_status(o2, "confirmed")
    
    print(f"✅ Created 3 orders")
    
    # Pricing calculator
    print(f"\n💰 Pricing Example (8hrs, $15 materials, Intermediate, Rush):")
    for key, val in pricing.items():
        print(f"  {key}: {val}")
    
    # Dashboard
    mgr.display_dashboard()
    
    # Invoice
    invoice = mgr.generate_invoice(o1)
    print(f"\n✅ Invoice generated: {len(invoice)} chars")
    
    # Cleanup
    if os.path.exists("/tmp/demo_orders.json"):
        os.remove("/tmp/demo_orders.json")
    
    print(f"\n  Order Manager Complete! 📦")
