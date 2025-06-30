frappe.ui.form.on("Journal Entry", {
    onload: function(frm) {
        // افتراض تاريخ اليوم في أول تحميل
        if (frm.is_new() && !frm.doc.posting_date) {
            frm.set_value('posting_date', frappe.datetime.get_today());
        }
    },
    validate: function (frm) {
        let total_debit = 0.0;
        let total_credit = 0.0;

        frm.doc.accounting_entries.forEach(row => {
            total_debit += flt(row.debit);
            total_credit += flt(row.credit);
        });

        frm.set_value("total_debit", total_debit);
        frm.set_value("total_credit", total_credit);
        frm.set_value("difference", total_debit - total_credit);

        if (total_debit !== total_credit) {
            frappe.msgprint(__("The restriction is unbalanced. Please ensure that the total debit equals the total credit."));
            frappe.validated = false;
        }
    }
});
