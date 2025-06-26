// Copyright (c) 2025, Bahaa and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sales Invoice', {
	 setup: function(frm) {
        frm.set_query('customer', () => {
            return {
                filters: {
                    party_type: 'Customer'
                }
            };
        });
    },
    onload: function(frm) {
        if (frm.is_new() && !frm.doc.posting_date) {
            frm.set_value('posting_date', frappe.datetime.get_today());
        }
    }
});
frappe.ui.form.on('Invoice Item', {
    item: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];

        if (row.item) {
            frappe.db.get_value('Item', row.item, 'standard_selling_rate')
                .then(r => {
                    if (r.message) {
                        frappe.model.set_value(cdt, cdn, 'rate', r.message.standard_selling_rate);
                    }
                });
        }
    },

    qty: function(frm, cdt, cdn) {
        calculate_amount(frm, cdt, cdn);
    },
    rate: function(frm, cdt, cdn) {
        calculate_amount(frm, cdt, cdn);
    }
});

function calculate_amount(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    if(row.qty && row.rate) { // فقط إذا كلاهما غير فارغ
        row.amount = row.qty * row.rate;
    } else {
        row.amount = 0;
    }
    frm.refresh_field('items');
} 

