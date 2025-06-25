// Copyright (c) 2025, Bahaa and contributors
// For license information, please see license.txt

frappe.ui.form.on('Purchase Invoice', {
	    setup: function(frm) {
        frm.set_query('supplier', () => {
            return {
                filters: {
                    party_type: 'Supplier'
                }
            };
        });
    }
});
