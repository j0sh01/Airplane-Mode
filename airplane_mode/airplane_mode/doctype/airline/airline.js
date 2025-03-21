// Copyright (c) 2025, Joshua Michael and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airline", {
	refresh(frm) {
		if (frm.doc.website) {
			frm.sidebar.add_user_action(__('Visit Website'), function() {
				window.open(frm.doc.website, '_blank');
				frm.add_web_link(__('Visit Website'), frm.doc.website);
			});
		}
	},
	website: function(frm) {
		if (frm.doc.website && !frm.doc.website.startsWith('https')) {
			frm.set_value('website', 'https://' + frm.doc.website);
		}
	}
});
