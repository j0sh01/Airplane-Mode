# Copyright (c) 2025, Joshua Michael and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import getdate, formatdate

def execute(filters=None):
    columns, data = get_columns(), get_occupancy_data(filters)
    chart = get_chart(data)
    return columns, data, None, chart

def get_columns():
    return [
        {"label": _("Airport"), "fieldname": "airport", "width": 200},
        {"label": _("Code"), "fieldname": "code", "width": 80},
        {"label": _("Total Shops"), "fieldname": "total", "fieldtype": "Int"},
        {"label": _("Available"), "fieldname": "available", "fieldtype": "Int"},
        {"label": _("Occupied"), "fieldname": "occupied", "fieldtype": "Int"},
        {"label": _("Occupancy %"), "fieldname": "occupancy_pct", "fieldtype": "Percent"}
    ]

def get_occupancy_data(filters):
    return frappe.db.sql("""
        SELECT 
            a.name as airport,
            a.code,
            COUNT(s.name) as total,
            SUM(IF(s.status='Available',1,0)) as available,
            SUM(IF(s.status='Occupied',1,0)) as occupied,
            ROUND(SUM(IF(s.status='Occupied',1,0))/COUNT(s.name)*100,2) as occupancy_pct
        FROM `tabAirport` a
        LEFT JOIN `tabAirport Shop` s ON a.name = s.airport
        GROUP BY a.name
        ORDER BY total DESC
    """, as_dict=1)

def get_chart(data):
    return {
        "data": {
            "labels": [d.airport for d in data],
            "datasets": [
                {
                    "name": "Available",
                    "values": [d.available for d in data],
                    "chartType": "bar",
                    "backgroundColor": "#7CD6FD"
                },
                {
                    "name": "Occupied",
                    "values": [d.occupied for d in data],
                    "chartType": "bar",
                    "backgroundColor": "#743EE2"
                }
            ]
        },
        "type": "bar",
        "barOptions": {
            "stacked": True
        },
        "title": "Shop Occupancy by Airport",
        "height": 300
    }
