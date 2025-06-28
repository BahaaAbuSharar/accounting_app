frappe.ui.form.on('Payment Entry', {
    onload: function(frm) {
        // افتراض تاريخ اليوم في أول تحميل
        if (frm.is_new() && !frm.doc.posting_date) {
            frm.set_value('posting_date', frappe.datetime.get_today());
        }
    },

    payment_type: function(frm) {
        // إعادة ضبط الحسابات عند تغيير نوع الدفع
        frm.set_value("account_paid_from", null);
        frm.set_value("account_paid_to", null);
    },
});
