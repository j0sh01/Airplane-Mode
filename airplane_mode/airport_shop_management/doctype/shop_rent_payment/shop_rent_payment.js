// Copyright (c) 2025, Joshua Michael and contributors
// For license information, please see license.txt

frappe.ui.form.on('Shop Rent Payment', {
    shop(frm) {
        if (!frm.doc.shop) return;

        frappe.call({
            method: "frappe.client.get_list",
            args: {
                doctype: "Payment Schedule",
                filters: {
                    shop: frm.doc.shop,
                    status: ["in", ["Pending", "Overdue"]]
                },
                fields: ["name", "month", "year", "amount"]
            },
            callback(response) {
                const schedules = response.message;
                if (!schedules.length) {
                    frappe.msgprint("No pending or overdue payment schedules found.");
                    return;
                }

                if (schedules.length > 1) {
                    // Show a dialog for multiple options
                    let dialog = new frappe.ui.Dialog({
                        title: "Select Payment Schedule",
                        fields: [
                            {
                                fieldname: "schedule",
                                fieldtype: "Select",
                                label: "Choose a Schedule",
                                options: schedules.map(s => ({
                                    label: `${s.month} ${s.year} - ${s.amount}`,
                                    value: s.name
                                }))
                            }
                        ],
                        primary_action_label: "Select",
                        primary_action(values) {
                            frm.set_value("reference_number", values.schedule);
                            frappe.call({
                                method: "airplane_mode.airport_shop_management.doctype.shop_rent_payment.shop_rent_payment.select_schedule",
                                args: { schedule_name: values.schedule },
                                callback(r) {
                                    let data = r.message;
                                    frm.set_value({
                                        payment_for_month: data.payment_for_month,
                                        payment_for_year: data.payment_for_year,
                                        amount: data.amount,
                                        reference_number: data.reference_number
                                    });
                                    dialog.hide();
                                }
                            });
                        }
                    });
                    dialog.show();
                } else {
                    // Auto-fill if only one schedule
                    let schedule = schedules[0];
                    frm.set_value({
                        payment_for_month: schedule.month,
                        payment_for_year: schedule.year,
                        amount: schedule.amount,
                        reference_number: schedule.name
                    });
                }
            }
        });
    }
});
