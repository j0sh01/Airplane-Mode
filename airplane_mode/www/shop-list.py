# airplane_mode/www/shop-list.py
import frappe
from frappe import _

def get_context(context):
    try:
        # Explicitly set default values
        context.shops = []
        context.css = ""
        
        # Fetch shops with error handling
        context.shops = frappe.get_all("Airport Shop",
            fields=[
                'name',
                'shop_name',
                'shop_number', 
                'airport',
                'airport_code',
                'area_sqft',
                'monthly_rent_amount',
                'status'
            ],
            filters={'status': 'Available'},
            ignore_permissions=False  # Important for permission checks
        )
        
        # Load CSS with validation
        css_path = frappe.get_app_path("airplane_mode", "www", "styles.css")
        if frappe.get_file_size(css_path) > 0:
            context.css = frappe.read_file(css_path)
            
    except Exception as e:
        frappe.log_error(f"Shop List Error: {str(e)}")
        context.error = str(e)