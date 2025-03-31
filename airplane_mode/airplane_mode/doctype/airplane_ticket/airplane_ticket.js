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



// Add to Airplane Ticket client script
frappe.ui.form.on('Airplane Ticket', {
    refresh: function(frm) {
        // Add payment button if ticket is submitted and not fully paid
        if(frm.doc.docstatus === 1 && frm.doc.payment_status !== "Paid") {
            frm.add_custom_button(__('Record Payment'), function() {
                frappe.route_options = {
                    "ticket": frm.doc.name,
                    "payment_amount": frm.doc.balance_due
                };
                frappe.new_doc("Airplane Ticket Payment");
            }, __("Payment"));
        }
        
        // Add button to view payment history
        if(frm.doc.docstatus === 1) {
            frm.add_custom_button(__('Payment History'), function() {
                frappe.call({
                    method: "get_payment_history",
                    doc: frm.doc,
                    callback: function(r) {
                        if(r.message && r.message.length) {
                            let payments = r.message;
                            let dialog = new frappe.ui.Dialog({
                                title: __('Payment History'),
                                fields: [
                                    {
                                        fieldtype: 'HTML',
                                        fieldname: 'payment_html'
                                    }
                                ]
                            });
                            
                            let html = '<div class="payment-history"><table class="table table-bordered">';
                            html += '<thead><tr><th>Date</th><th>Receipt No</th><th>Amount</th><th>Method</th></tr></thead>';
                            html += '<tbody>';
                            
                            payments.forEach(function(payment) {
                                html += `<tr>
                                    <td>${frappe.format(payment.payment_date, {fieldtype: 'Date'})}</td>
                                    <td>${payment.name || ''}</td>
                                    <td>${format_currency(payment.payment_amount)}</td>
                                    <td>${payment.payment_method}</td>
                                </tr>`;
                            });
                            
                            html += '</tbody></table></div>';
                            dialog.fields_dict.payment_html.$wrapper.html(html);
                            dialog.show();
                        } else {
                            frappe.msgprint(__('No payment records found'));
                        }
                    }
                });
            }, __("Payment"));
        }
    }
});