// Copyright (c) 2025, Joshua Michael and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Ticket", {
    refresh: function (frm) {
        if (frm.doc.docstatus === 0) { 
            frm.add_custom_button(
                __("Assign Seat"),
                function () {
                    let d = new frappe.ui.Dialog({
                        title: __('Select Seat'),
                        fields: [
                            {
                                label: __('Seat Number'),
                                fieldname: 'seat_number',
                                fieldtype: 'Data'
                            }
                        ],
                        primary_action_label: __('Assign'),
                        primary_action(values) {
                            frm.set_value('seat', values.seat_number);
                            d.hide();
                        }
                    });
                    d.show();
                },
                __("Actions") 
            );

            frm.add_custom_button(
                __("Assign Gate"),
                function () {
                    let d = new frappe.ui.Dialog({
                        title: __('Select Gate'),
                        fields: [
                            {
                                label: __('Gate Number'),
                                fieldname: 'gate_number',
                                fieldtype: 'Data'
                            }
                        ],
                        primary_action_label: __('Assign'),
                        primary_action(values) {
                            frm.set_value('gate_number', values.gate_number);
                            d.hide();
                        }
                    });
                    d.show();
                },
                __("Actions")
            );
        }
    }
});


