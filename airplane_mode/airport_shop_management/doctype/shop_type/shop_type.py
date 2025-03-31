# Copyright (c) 2025, Joshua Michael and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import db

class ShopType(Document):
	pass		

def after_install():
    shop_types = [
        {"shop_type_name": "Stall", "enabled": 1},
        {"shop_type_name": "Walk-through", "enabled": 1},
        {"shop_type_name": "Normal", "enabled": 1},
    ]

    for shop_type in shop_types:
        if not frappe.db.exists("Shop Type", shop_type["shop_type_name"]):
            # First create the doc with just the doctype
            doc = frappe.new_doc("Shop Type")
            
            # Then set the properties
            doc.shop_type_name = shop_type["shop_type_name"]
            doc.enabled = shop_type["enabled"]
            
            # Save the document
            doc.insert()
            frappe.db.commit()
            print(f"Created Shop Type: {shop_type['shop_type_name']}")		