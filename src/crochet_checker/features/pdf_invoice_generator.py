"""
PDF Invoice Generator - Professional invoices for crochet businesses
"""
from fpdf import FPDF
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _pdf_utils import setup_unicode_font, FONT
from typing import Dict, List
from datetime import datetime
import os


class PDFInvoiceGenerator:
    """
    Generate professional invoices for crochet businesses
    
    Features:
    - Custom invoices for finished items
    - Pattern sale invoices
    - Custom order invoices
    - Payment tracking
    - Tax calculations
    - Receipt generation
    """
    
    def __init__(self, business_name: str = "", business_address: str = "",
                email: str = "", phone: str = "", website: str = "",
                logo_text: str = ""):
        self.business_name = business_name
        self.business_address = business_address
        self.email = email
        self.phone = phone
        self.website = website
        self.logo_text = logo_text or business_name
        self.pdf = FPDF()
        setup_unicode_font(self.pdf)
        # Register Unicode font
        import os
        self.invoice_number = 1
    
    def _hex_to_rgb(self, hex_color: str) -> tuple:
        h = hex_color.lstrip('#')
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    
    def create_invoice(self, customer_name: str, customer_address: str = "",
                      customer_email: str = "", items: List[Dict] = None,
                      tax_rate: float = 0, discount: float = 0,
                      notes: str = "", payment_terms: str = "Due on receipt") -> str:
        """
        Create professional invoice
        
        Args:
            customer_name: Customer name
            customer_address: Customer address
            customer_email: Customer email
            items: List of items [{"description": "...", "quantity": 1, "price": 10.00}]
            tax_rate: Tax rate as percentage (e.g., 8.5)
            discount: Discount amount
            notes: Additional notes
            payment_terms: Payment terms text
        
        Returns:
            Path to generated PDF
        """
        items = items or []
        
        self.pdf.add_page()
        
        # Header background
        self.pdf.set_fill_color(44, 62, 80)
        self.pdf.rect(0, 0, 210, 40, 'F')
        
        # Business name
        self.pdf.set_text_color(255, 255, 255)
        self.pdf.set_font("DejaVu", "B", 22)
        self.pdf.set_xy(15, 8)
        self.pdf.cell(100, 10, self.business_name)
        
        # Logo placeholder
        self.pdf.set_draw_color(255, 255, 255)
        self.pdf.rect(160, 5, 40, 30)
        self.pdf.set_font("DejaVu", "I", 8)
        self.pdf.set_xy(160, 17)
        self.pdf.cell(40, 8, "LOGO", align='C')
        
        # Business info
        self.pdf.set_text_color(200, 200, 200)
        self.pdf.set_font("DejaVu", "", 8)
        self.pdf.set_xy(15, 25)
        if self.business_address:
            self.pdf.cell(100, 5, self.business_address)
        if self.email or self.phone:
            self.pdf.set_xy(15, 31)
            contact = " | ".join(filter(None, [self.email, self.phone]))
            self.pdf.cell(100, 5, contact)
        
        # Invoice title
        self.pdf.set_text_color(255, 255, 255)
        self.pdf.set_font("DejaVu", "B", 28)
        self.pdf.set_xy(120, 8)
        self.pdf.cell(0, 15, "INVOICE", align='R')
        
        # Invoice details
        self.pdf.set_y(50)
        self.pdf.set_text_color(51, 51, 51)
        
        # Left side - Bill to
        self.pdf.set_font("DejaVu", "B", 11)
        self.pdf.set_text_color(231, 76, 60)
        self.pdf.set_x(15)
        self.pdf.cell(50, 7, "BILL TO:")
        
        self.pdf.set_text_color(51, 51, 51)
        self.pdf.set_font("DejaVu", "B", 11)
        self.pdf.set_x(15)
        self.pdf.cell(50, 7, customer_name)
        
        if customer_address:
            self.pdf.set_font("DejaVu", "", 9)
            self.pdf.set_x(15)
            self.pdf.multi_cell(80, 5, customer_address)
        
        if customer_email:
            self.pdf.set_x(15)
            self.pdf.cell(50, 6, customer_email)
        
        # Right side - Invoice details
        self.pdf.set_xy(130, 50)
        self.pdf.set_font("DejaVu", "B", 10)
        self.pdf.cell(30, 7, "Invoice #:")
        self.pdf.set_font("DejaVu", "", 10)
        self.pdf.cell(0, 7, f"INV-{self.invoice_number:04d}")
        
        self.pdf.set_xy(130, 59)
        self.pdf.set_font("DejaVu", "B", 10)
        self.pdf.cell(30, 7, "Date:")
        self.pdf.set_font("DejaVu", "", 10)
        self.pdf.cell(0, 7, datetime.now().strftime("%B %d, %Y"))
        
        self.pdf.set_xy(130, 68)
        self.pdf.set_font("DejaVu", "B", 10)
        self.pdf.cell(30, 7, "Due Date:")
        self.pdf.set_font("DejaVu", "", 10)
        self.pdf.cell(0, 7, datetime.now().strftime("%B %d, %Y"))
        
        self.pdf.set_xy(130, 77)
        self.pdf.set_font("DejaVu", "B", 10)
        self.pdf.cell(30, 7, "Terms:")
        self.pdf.set_font("DejaVu", "", 10)
        self.pdf.cell(0, 7, payment_terms)
        
        # Items table
        self.pdf.set_y(105)
        
        # Table header
        self.pdf.set_fill_color(231, 76, 60)
        self.pdf.set_text_color(255, 255, 255)
        self.pdf.set_font("DejaVu", "B", 10)
        
        self.pdf.set_x(15)
        self.pdf.cell(100, 8, "  Description", border=1, fill=True)
        self.pdf.cell(20, 8, "Qty", border=1, align='C', fill=True)
        self.pdf.cell(30, 8, "Price", border=1, align='R', fill=True)
        self.pdf.cell(30, 8, "Total", border=1, align='R', fill=True)
        self.pdf.ln()
        
        # Items
        self.pdf.set_text_color(51, 51, 51)
        subtotal = 0
        
        for i, item in enumerate(items):
            description = item.get("description", "")
            quantity = item.get("quantity", 1)
            price = item.get("price", 0)
            total = quantity * price
            subtotal += total
            
            # Alternate row colors
            if i % 2 == 0:
                self.pdf.set_fill_color(250, 250, 250)
            else:
                self.pdf.set_fill_color(255, 255, 255)
            
            self.pdf.set_font("DejaVu", "", 9)
            self.pdf.set_x(15)
            self.pdf.cell(100, 7, f"  {description}", border=1, fill=True)
            self.pdf.cell(20, 7, str(quantity), border=1, align='C', fill=True)
            self.pdf.cell(30, 7, f"${price:.2f}", border=1, align='R', fill=True)
            self.pdf.cell(30, 7, f"${total:.2f}", border=1, align='R', fill=True)
            self.pdf.ln()
        
        # Totals section
        self.pdf.ln(5)
        
        # Subtotal
        self.pdf.set_font("DejaVu", "", 10)
        self.pdf.set_x(115)
        self.pdf.cell(50, 7, "Subtotal:", align='R')
        self.pdf.cell(30, 7, f"${subtotal:.2f}", align='R')
        self.pdf.ln()
        
        # Discount
        if discount > 0:
            self.pdf.set_x(115)
            self.pdf.cell(50, 7, "Discount:", align='R')
            self.pdf.cell(30, 7, f"-${discount:.2f}", align='R')
            self.pdf.ln()
        
        # Tax
        tax_amount = (subtotal - discount) * (tax_rate / 100)
        if tax_rate > 0:
            self.pdf.set_x(115)
            self.pdf.cell(50, 7, f"Tax ({tax_rate}%):", align='R')
            self.pdf.cell(30, 7, f"${tax_amount:.2f}", align='R')
            self.pdf.ln()
        
        # Total
        grand_total = subtotal - discount + tax_amount
        
        self.pdf.ln(3)
        self.pdf.set_fill_color(44, 62, 80)
        self.pdf.set_text_color(255, 255, 255)
        self.pdf.set_font("DejaVu", "B", 12)
        self.pdf.set_x(115)
        self.pdf.cell(50, 10, "TOTAL:", border=1, align='R', fill=True)
        self.pdf.cell(30, 10, f"${grand_total:.2f}", border=1, align='R', fill=True)
        self.pdf.ln()
        
        # Notes section
        if notes:
            self.pdf.set_y(210)
            self.pdf.set_text_color(231, 76, 60)
            self.pdf.set_font("DejaVu", "B", 11)
            self.pdf.set_x(15)
            self.pdf.cell(0, 7, "Notes:")
            
            self.pdf.set_text_color(51, 51, 51)
            self.pdf.set_font("DejaVu", "", 9)
            self.pdf.set_x(15)
            self.pdf.multi_cell(170, 5, notes)
        
        # Payment info
        self.pdf.set_y(240)
        self.pdf.set_text_color(51, 51, 51)
        self.pdf.set_font("DejaVu", "B", 10)
        self.pdf.set_x(15)
        self.pdf.cell(0, 7, "Payment Methods:")
        
        self.pdf.set_font("DejaVu", "", 9)
        self.pdf.set_x(15)
        self.pdf.multi_cell(170, 5, "- PayPal: paypal@yourbusiness.com\n- Venmo: @yourbusiness\n- Bank Transfer: Contact for details\n- Check: Make payable to " + self.business_name)
        
        # Footer
        self.pdf.set_y(275)
        self.pdf.set_fill_color(44, 62, 80)
        self.pdf.rect(0, 280, 210, 17, 'F')
        self.pdf.set_text_color(255, 255, 255)
        self.pdf.set_font("DejaVu", "", 8)
        self.pdf.set_xy(15, 283)
        footer_text = f"Thank you for your business! | {self.website or 'www.yourwebsite.com'} | {self.email or 'email@yourbusiness.com'}"
        self.pdf.cell(180, 5, footer_text, align='C')
        
        # Save
        invoice_num = self.invoice_number
        self.invoice_number += 1
        
        filename = f"/tmp/invoice_{invoice_num:04d}.pdf"
        self.pdf.output(filename)
        return filename
    
    def create_receipt(self, customer_name: str, items: List[Dict],
                      payment_method: str = "", amount_paid: float = None) -> str:
        """Create payment receipt"""
        self.pdf.add_page()
        
        # Header
        self.pdf.set_fill_color(39, 174, 96)  # Green for receipt
        self.pdf.rect(0, 0, 210, 30, 'F')
        
        self.pdf.set_text_color(255, 255, 255)
        self.pdf.set_font("DejaVu", "B", 24)
        self.pdf.set_xy(15, 8)
        self.pdf.cell(100, 12, "RECEIPT")
        
        self.pdf.set_font("DejaVu", "B", 16)
        self.pdf.set_xy(100, 8)
        self.pdf.cell(95, 12, self.business_name, align='R')
        
        # Receipt details
        self.pdf.set_y(40)
        self.pdf.set_text_color(51, 51, 51)
        
        self.pdf.set_font("DejaVu", "B", 11)
        self.pdf.set_x(15)
        self.pdf.cell(40, 7, "Date:")
        self.pdf.set_font("DejaVu", "", 11)
        self.pdf.cell(0, 7, datetime.now().strftime("%B %d, %Y"))
        
        self.pdf.set_x(15)
        self.pdf.set_font("DejaVu", "B", 11)
        self.pdf.cell(40, 7, "Customer:")
        self.pdf.set_font("DejaVu", "", 11)
        self.pdf.cell(0, 7, customer_name)
        
        if payment_method:
            self.pdf.set_x(15)
            self.pdf.set_font("DejaVu", "B", 11)
            self.pdf.cell(40, 7, "Payment:")
            self.pdf.set_font("DejaVu", "", 11)
            self.pdf.cell(0, 7, payment_method)
        
        # Items
        self.pdf.set_y(75)
        self.pdf.set_font("DejaVu", "B", 10)
        self.pdf.set_fill_color(39, 174, 96)
        self.pdf.set_text_color(255, 255, 255)
        
        self.pdf.set_x(15)
        self.pdf.cell(110, 7, "  Item", border=1, fill=True)
        self.pdf.cell(30, 7, "Amount", border=1, align='R', fill=True)
        self.pdf.ln()
        
        total = 0
        self.pdf.set_text_color(51, 51, 51)
        
        for i, item in enumerate(items):
            description = item.get("description", "")
            amount = item.get("price", 0) * item.get("quantity", 1)
            total += amount
            
            if i % 2 == 0:
                self.pdf.set_fill_color(240, 248, 240)
            else:
                self.pdf.set_fill_color(255, 255, 255)
            
            self.pdf.set_font("DejaVu", "", 9)
            self.pdf.set_x(15)
            self.pdf.cell(110, 6, f"  {description}", border=1, fill=True)
            self.pdf.cell(30, 6, f"${amount:.2f}", border=1, align='R', fill=True)
            self.pdf.ln()
        
        # Total
        self.pdf.ln(3)
        self.pdf.set_fill_color(39, 174, 96)
        self.pdf.set_text_color(255, 255, 255)
        self.pdf.set_font("DejaVu", "B", 12)
        self.pdf.set_x(75)
        self.pdf.cell(50, 10, "TOTAL PAID:", border=1, align='R', fill=True)
        self.pdf.cell(30, 10, f"${amount_paid or total:.2f}", border=1, align='R', fill=True)
        
        # Thank you
        self.pdf.set_y(200)
        self.pdf.set_text_color(51, 51, 51)
        self.pdf.set_font("DejaVu", "I", 12)
        self.pdf.cell(0, 10, "Thank you for your purchase!", align='C')
        
        # Save
        filename = f"/tmp/receipt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        self.pdf.output(filename)
        return filename


# Demo
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  PDF INVOICE GENERATOR - DEMO")
    print("=" * 60)
    
    generator = PDFInvoiceGenerator(
        business_name="Cozy Stitches Studio",
        business_address="123 Yarn Street, Craft City, ST 12345",
        email="hello@cozystitches.com",
        phone="(555) 123-4567",
        website="www.cozystitches.com",
    )
    
    # Create invoice
    items = [
        {"description": "Custom Granny Square Blanket (50\" × 60\")", "quantity": 1, "price": 150.00},
        {"description": "Matching Pillow Covers (set of 2)", "quantity": 1, "price": 45.00},
        {"description": "Amigurumi Bunny (custom colors)", "quantity": 2, "price": 25.00},
        {"description": "Gift Wrapping", "quantity": 1, "price": 5.00},
    ]
    
    invoice_path = generator.create_invoice(
        customer_name="Jane Smith",
        customer_address="456 Customer Lane\nBuyer Town, ST 67890",
        customer_email="jane@example.com",
        items=items,
        tax_rate=8.5,
        notes="Thank you for your custom order! Each item is handmade with love. Please allow 2-3 weeks for completion.",
        payment_terms="Net 30",
    )
    
    print(f"\n[OK] Invoice Generated: {invoice_path}")
    print(f"   Business: {generator.business_name}")
    print(f"   Customer: Jane Smith")
    print(f"   Items: {len(items)}")
    print(f"   File size: {os.path.getsize(invoice_path)} bytes")
    
    # Create receipt
    generator2 = PDFInvoiceGenerator(
        business_name="Cozy Stitches Studio",
        business_address="123 Yarn Street, Craft City, ST 12345",
        email="hello@cozystitches.com",
    )
    receipt_path = generator2.create_receipt(
        customer_name="Jane Smith",
        items=items,
        payment_method="PayPal",
        amount_paid=249.50,
    )
    
    print(f"\n[OK] Receipt Generated: {receipt_path}")
    print(f"   File size: {os.path.getsize(receipt_path)} bytes")
    
    print(f"\n  PDF Invoice Generator Complete! [$$][*]")
