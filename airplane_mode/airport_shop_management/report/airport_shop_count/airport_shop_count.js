// Copyright (c) 2025, Joshua Michael and contributors
// For license information, please see license.txt

frappe.query_reports["Airport Shop Count"] = {
    "filters": [
        {
            "fieldname": "airport",
            "label": __("Airport"),
            "fieldtype": "Link",
            "options": "Airport"
        }
    ]
};