// Copyright (c) 2025, Joshua Michael and contributors
// For license information, please see license.txt


frappe.ui.form.on("Payment Schedule", {
	refresh(frm) {
		if (frm.doc.status === "Pending") {
			frm.add_custom_button(__('Create Shop Rent Payment'), function() {
				frappe.new_doc('Shop Rent Payment', {
					shop: frm.doc.shop,
				});
			});
		}
	},
});
