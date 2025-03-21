// Copyright (c) 2025, Joshua Michael and contributors
// For license information, please see license.txt

frappe.query_reports["Airport Shop Occupancy"] = {
    filters: [
        {
            fieldname: "airport",
            label: __("Airport"),
            fieldtype: "Link",
            options: "Airport"
        }
    ],
    get_chart_data: function(_columns, result) {
        return {
            data: {
                labels: result.map(r => r.airport),
                datasets: [
                    {
                        name: "Available",
                        values: result.map(r => r.available),
                        chartType: "bar"
                    },
                    {
                        name: "Occupied", 
                        values: result.map(r => r.occupied),
                        chartType: "bar"
                    }
                ]
            },
            type: "bar",
            barOptions: {stacked: true}
        }
    }
};