// Copyright (c) 2025, Joshua Michael and contributors
// For license information, please see license.txt

frappe.ui.form.on('Airplane', {
    refresh: function(frm) {
        if (!frappe.user_roles.includes('Airport Authority Personnel')) {
            frm.set_df_property('initial_audit_completed', 'hidden', 1);  
            frm.set_df_property('initial_audit_completed', 'read_only', 1);  
        } else {
            frm.set_df_property('initial_audit_completed', 'hidden', 0);  
            frm.set_df_property('initial_audit_completed', 'read_only', 0);  
        }
    }
});
