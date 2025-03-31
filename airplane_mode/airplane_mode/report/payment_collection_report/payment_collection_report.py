# Copyright (c) 2025, Joshua Michael and contributors
# For license information, please see license.txt


from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
    if not filters:
        filters = {}
        
    columns = get_columns()
    data = get_data(filters)
    
    return columns, data

def get_columns():
    return [
        {
            "fieldname": "payment_date",
            "label": _("Payment Date"),
            "fieldtype": "Date",
            "width": 100
        },
        {
            "fieldname": "receipt_number",
            "label": _("Receipt No"),
            "fieldtype": "Data",
            "width": 120
        },
        {
            "fieldname": "ticket",
            "label": _("Ticket ID"),
            "fieldtype": "Link",
            "options": "Airplane Ticket",
            "width": 120
        },
        {
            "fieldname": "passenger_name",
            "label": _("Passenger"),
            "fieldtype": "Data",
            "width": 150
        },
        {
            "fieldname": "flight",
            "label": _("Flight"),
            "fieldtype": "Link",
            "options": "Airplane Flight",
            "width": 120
        },
        {
            "fieldname": "payment_amount",
            "label": _("Amount"),
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "fieldname": "payment_method",
            "label": _("Method"),
            "fieldtype": "Data",
            "width": 100
        },
        {
            "fieldname": "received_by",
            "label": _("Cashier"),
            "fieldtype": "Link",
            "options": "User",
            "width": 150
        }
    ]

def get_data(filters):
    conditions = get_conditions(filters)
    
    data = frappe.db.sql("""
        SELECT 
            tp.payment_date,
            tp.receipt_number,
            tp.ticket,
            tp.passenger_name,
            at.flight,
            tp.payment_amount,
            tp.payment_method,
            tp.received_by
        FROM 
            `tabAirplane Ticket Payment` tp
        LEFT JOIN
            `tabAirplane Ticket` at ON tp.ticket = at.name
        WHERE
            tp.docstatus = 1
            {conditions}
        ORDER BY
            tp.payment_date DESC,
            tp.receipt_number
    """.format(conditions=conditions), filters, as_dict=1)
    
    return data

def get_conditions(filters):
    conditions = []
    
    if filters.get("from_date"):
        conditions.append("tp.payment_date >= %(from_date)s")
    
    if filters.get("to_date"):
        conditions.append("tp.payment_date <= %(to_date)s")
    
    if filters.get("payment_method"):
        conditions.append("tp.payment_method = %(payment_method)s")
    
    if filters.get("received_by"):
        conditions.append("tp.received_by = %(received_by)s")
    
    if filters.get("flight"):
        conditions.append("at.flight = %(flight)s")
    
    return " AND " + " AND ".join(conditions) if conditions else ""