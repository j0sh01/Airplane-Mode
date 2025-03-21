# Copyright (c) 2025, Joshua Michael and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {
            "label": _("Airport"),
            "fieldname": "airport",
            "fieldtype": "Link",
            "options": "Airport",
            "width": 200
        },
        {
            "label": _("Airport Code"),
            "fieldname": "airport_code",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": _("Number of Shops"),
            "fieldname": "shop_count",
            "fieldtype": "Int",
            "width": 150
        },
        {
            "label": _("Total Rent"),
            "fieldname": "rent_amount",
            "fieldtype": "Float",
            "width": 180
        }
    ]

def get_data(filters=None):
    conditions = []
    if filters.get("airport"):
        conditions.append(f"a.name = {frappe.db.escape(filters.airport)}")
    
    where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""

    query = f"""
        SELECT 
            a.name as airport,
            a.code as airport_code,
            COUNT(s.name) as shop_count,
            SUM(s.monthly_rent_amount) as rent_amount
        FROM 
            `tabAirport` a
        LEFT JOIN 
            `tabAirport Shop` s ON a.name = s.airport
        {where_clause}
        GROUP BY 
            a.name
        ORDER BY
            shop_count DESC
    """

    result = frappe.db.sql(query, as_dict=1)
    return result