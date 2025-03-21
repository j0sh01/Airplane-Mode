import frappe

def get_context(context):
    shop_name = frappe.form_dict.get('name')
    if not shop_name:
        frappe.throw("Shop name parameter is missing", frappe.ValidationError)
        
    context.shop = frappe.get_doc("Airport Shop", shop_name).as_dict()
    context.css = frappe.read_file("airplane_mode/www/styles.css")
    
    if not context.shop:
        frappe.throw("Shop not found", frappe.DoesNotExistError)