// Copyright (c) 2025, Joshua Michael and contributors
// For license information, please see license.txt

frappe.ui.form.on('Airplane Flight', {
    refresh: function(frm) {
        // Add a help message about gate changes
        frm.set_intro("Changing the gate number will automatically update all tickets for this flight.", "blue");
    },
    
    gate_number: function(frm) {
        // Show a notification when gate is changed
        if(frm.doc.gate_number && frm.doc.__unsaved) {
            frappe.show_alert({
                message: __("Gate number will be updated on all tickets after saving"),
                indicator: 'blue'
            }, 5);
        }
    }
});


frappe.ui.form.on('Airplane Flight', {
    refresh(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button('Update Gate Number', () => {
                frappe.prompt(
                    [
                        {
                            fieldname: 'new_gate_number',
                            label: 'New Gate Number',
                            fieldtype: 'Data',
                            reqd: 1,
                            default: frm.doc.gate_number
                        }
                    ],
                    (values) => {
                        frappe.call({
                            method: 'airplane_mode.airplane_mode.doctype.airplane_flight.airplane_flight.update_gate_and_tickets',
                            args: {
                                flight_name: frm.doc.name,
                                new_gate_number: values.new_gate_number
                            },
                            callback: function (r) {
                                if (!r.exc) {
                                    frappe.msgprint(__('Gate number update initiated in background.'));
                                    frm.reload_doc();
                                }
                            }
                        });
                    },
                    __('Update Gate Number'),
                    __('Update')
                );
            });
        }
    }
});
