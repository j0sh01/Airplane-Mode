# airport_shop_management/airport_shop_management/scheduler_events/monthly.py
import frappe
from frappe.utils import today, getdate, add_days
from datetime import datetime

def send_rent_reminders():
    settings = frappe.get_single("Shop Settings")
    
    # Check if reminders are enabled
    if not settings.enable_rent_reminders:
        return
    
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    # Calculate reminder date
    due_date = getdate(f"{current_year}-{current_month}-01")
    reminder_date = add_days(due_date, -settings.reminder_days_before)
    
    if getdate(today()) == reminder_date:
        # Get all occupied shops
        shops = frappe.get_all(
            "Airport Shop", 
            filters={"status": "Occupied"},
            fields=["name", "shop_number", "shop_name", "tenant", "rent_amount", "airport"]
        )
        
        for shop in shops:
            # Check if payment is already made for current month
            existing_payment = frappe.get_all(
                "Shop Rent Payment",
                filters={
                    "shop": shop.name,
                    "payment_for_month": datetime.now().strftime("%B"),
                    "payment_for_year": current_year,
                    "docstatus": 1
                }
            )
            
            if not existing_payment:
                # Get tenant information
                tenant = frappe.get_doc("Shop Tenant", shop.tenant)
                
                # Send email reminder
                subject = f"Rent Reminder: Shop {shop.shop_number} at {shop.airport}"
                message = f"""
                Dear {tenant.tenant_name},
                
                This is a reminder that your rent payment of {shop.rent_amount} for Shop {shop.shop_number} ({shop.shop_name}) at {shop.airport} is due on {due_date}.
                
                Please ensure timely payment to avoid any inconvenience.
                
                Thank you,
                Airport Management
                """
                
                frappe.sendmail(
                    recipients=[tenant.email],
                    subject=subject,
                    message=message
                )
                
                frappe.logger().info(f"Rent reminder sent to {tenant.email} for shop {shop.shop_number}")