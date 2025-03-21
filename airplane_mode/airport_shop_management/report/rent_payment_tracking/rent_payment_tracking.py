# Copyright (c) 2025, Joshua Michael and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import getdate, formatdate
from datetime import datetime

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    chart = get_chart_data(data) if data else None
    return columns, data, None, chart

def get_columns():
    return [
        {"label": _("Status"), "fieldname": "status", "width": 100},
        {"label": _("Month"), "fieldname": "month", "width": 120},
        {"label": _("Year"), "fieldname": "year", "width": 80},
        {"label": _("Shop"), "fieldname": "shop", "width": 150},
        {"label": _("Amount"), "fieldname": "amount", "fieldtype": "Currency", "width": 120},
        {"label": _("Payment Date"), "fieldname": "payment_date", "fieldtype": "Date", "width": 120},
        {"label": _("Due Date"), "fieldname": "due_date", "fieldtype": "Date", "width": 120}
    ]

def get_data(filters):
    # Build conditions based on filters
    conditions = []
    if filters.get("status"):
        conditions.append(f"ps.status = {frappe.db.escape(filters.status)}")
    if filters.get("shop"):
        conditions.append(f"ps.shop = {frappe.db.escape(filters.shop)}")
    
    where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""

    query = f"""
        SELECT
            ps.status,
            ps.month,
            ps.year,
            ps.shop,
            ps.amount as scheduled_amount,
            ps.due_date,
            srp.payment_date,
            srp.amount as paid_amount
        FROM `tabPayment Schedule` ps
        LEFT JOIN `tabShop Rent Payment` srp ON ps.payment_reference = srp.name
        {where_clause}
        ORDER BY ps.due_date DESC
    """

    data = frappe.db.sql(query, as_dict=True)
    
    # Calculate final amount (use paid amount if available)
    for row in data:
        row.amount = row.paid_amount if row.paid_amount else row.scheduled_amount
        row.month = datetime.strptime(row.month, "%B").strftime("%B")  # Ensure proper month formatting
        
    return data

def get_chart_data(data):
    status_counts = {}
    for d in data:
        status_counts[d.status] = status_counts.get(d.status, 0) + 1
    
    return {
        "data": {
            "labels": list(status_counts.keys()),
            "datasets": [{
                "name": "Payment Status Distribution",
                "values": list(status_counts.values()),
                "chartType": "pie"
            }]
        },
        "type": "pie",
        "title": "Payment Status Distribution",
        "height": 300
    }