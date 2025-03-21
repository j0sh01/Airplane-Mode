// Copyright (c) 2025, Joshua Michael and contributors
// For license information, please see license.txt

frappe.query_reports["Rent Payment Tracking"] = {
    "filters": [
        {
            "fieldname": "status",
            "label": __("Status"),
            "fieldtype": "Select",
            "options": "\nPending\nPaid\nOverdue"
        },
        {
            "fieldname": "shop",
            "label": __("Shop"),
            "fieldtype": "Link",
            "options": "Airport Shop"
        }
    ]
};
