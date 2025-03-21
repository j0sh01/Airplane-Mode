frappe.listview_settings['Payment Schedule'] = {
    get_indicator: function(doc) {
        let status_color = {
            "Pending": "orange",
            "Paid": "green",
            "Overdue": "red"
        };

        let status_label = {
            "Pending": __("Pending Payment"),
            "Paid": __("Payment Received"),
            "Overdue": __("Payment Overdue")
        };

        let indicator = [status_label[doc.status], status_color[doc.status], "status,=," + doc.status];

        if (doc.status === "Paid") {
            indicator[3] = "green-row";
        } else if (doc.status === "Overdue" || doc.status === "Pending") {
            indicator[3] = "line-through";
        }

        return indicator;
    }
};

// Add custom CSS to apply the styles
$(document).ready(function() {
    $('<style>')
        .prop('type', 'text/css')
        .html(`
            .green-row {
                background-color: #d4edda !important;
            }
            .line-through {
                text-decoration: line-through;
            }
        `)
        .appendTo('head');
});

// Apply the custom CSS classes to the list view rows
frappe.listview_settings['Payment Schedule'].onload = function(listview) {
    listview.page.add_inner_button(__('Apply Styles'), function() {
        listview.$result.find('.list-row-container').each(function() {
            let $row = $(this);
            let status = $row.find('.list-row-col[data-fieldname="status"]').text().trim();

            if (status === "Paid") {
                $row.addClass('green-row');
            } else if (status === "Overdue" || status === "Pending") {
                $row.addClass('line-through');
            }
        });
    });
};