import frappe
from frappe.utils import today, getdate

def mark_overdue_payments():
    """Mark payments as overdue if past due date"""
    current_date = getdate(today())
    
    # Find all pending payments with due date in the past
    schedules = frappe.get_all(
        "Shop Rent Payment Schedule",
        filters={
            "status": "Pending",
            "due_date": ["<", current_date]
        },
        fields=["name"]
    )
    
    for schedule in schedules:
        schedule_doc = frappe.get_doc("Shop Rent Payment Schedule", schedule.name)
        schedule_doc.status = "Overdue"
        schedule_doc.save()
        
        # Send overdue notification
        tenant = frappe.get_doc("Shop Tenant", schedule_doc.tenant)
        shop = frappe.get_doc("Airport Shop", schedule_doc.shop)
        
        frappe.sendmail(
            recipients=[tenant.email],
            subject=f"OVERDUE: Rent Payment for Shop {shop.shop_number}",
            message=f"""
            Dear {tenant.tenant_name},
            
            Your rent payment of {schedule_doc.amount} for Shop {shop.shop_number} ({shop.shop_name}) 
            at {shop.airport} for {schedule_doc.month} {schedule_doc.year} is now overdue.
            
            Please make the payment as soon as possible to avoid any further action.
            
            Thank you,
            Airport Management
            """
        )