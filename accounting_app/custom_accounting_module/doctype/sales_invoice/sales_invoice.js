// Copyright (c) 2025, Bahaa and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sales Invoice', {
	// refresh: function(frm) {

	// }
});
frappe.ui.form.on('Sales Invoice Item', {
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

