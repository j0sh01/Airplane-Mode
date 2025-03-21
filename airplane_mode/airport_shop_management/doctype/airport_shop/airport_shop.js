// // Copyright (c) 2025, Joshua Michael and contributors
// // For license information, please see license.txt

// frappe.ui.form.on("Airport Shop", {
// 	refresh(frm) {
// 		if (frm.doc.status === "Occupied") {
// 			frm.add_custom_button(__('Create Payment Schedule'), function() {
// 				// Call the create_payment_schedule function
// 				frappe.call({
// 					method: "airplane_mode.airport_shop_management.doctype.airport_shop.airport_shop.create_payment_schedule",
// 					args: {
// 						shop_name: frm.doc.name
// 					},
// 					callback: function(r) {
// 						if (!r.exc) {
// 							frappe.msgprint(__('Payment schedule created successfully.'));
// 							frm.reload_doc();
// 						}
// 					}
// 				});
// 			});
// 			if (frm.doc.payment_schedule) {
// 				frm.add_custom_button(__('View Payment Schedule'), function() {
// 					frappe.set_route('Form', 'Payment Schedule', frm.doc.payment_schedule);
// 				});
// 			}
// 		}
// 	}
// });


frappe.ui.form.on('Airport Shop', {
    refresh(frm) {
        if(frm.doc.tenant) {
            frm.add_custom_button(__('View Tenant'), () => {
                frappe.set_route('Form', 'Shop Tenant', frm.doc.tenant);
            });
        }
    },
    
    airport(frm) {
        if(frm.doc.airport) {
            frappe.db.get_value('Airport', frm.doc.airport, 'code', (r) => {
                frm.set_value('airport_code', r.code);
            });
        }
    }
});