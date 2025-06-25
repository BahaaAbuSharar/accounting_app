frappe.ui.form.on("Journal Entry Account", {
    debit: function(frm, cdt, cdn) {
        calculate_totals(frm);
    },
    credit: function(frm, cdt, cdn) {
        calculate_totals(frm);
    }
});

function calculate_totals(frm) {
    let total_debit = 0;
    let total_credit = 0;

    frm.doc.accounts.forEach(row => {
        total_debit += row.debit || 0;
        total_credit += row.credit || 0;
    });

    frm.set_value("total_debit", total_debit);
    frm.set_value("total_credit", total_credit);
    frm.set_value("difference", total_debit - total_credit);
}
