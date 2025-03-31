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
