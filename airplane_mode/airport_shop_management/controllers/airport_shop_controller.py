import frappe

@frappe.whitelist(allow_guest=True)
def get_shop_context():
    context = {}
    context.shops = frappe.get_all("Airport Shop",
        fields=["name", "shop_name", "airport", "airport_code", "status", 
                "area_sqft", "monthly_rent_amount", "shop_number"],
        filters={"status": "Available"}
    )
    return context