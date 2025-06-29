frappe.ui.form.on('Payment Entry', {
    // عند تغيير نوع الدفع أو الطرف
    validate: function(frm) {
        if (frm.doc.party_type === "Supplier" && frm.doc.payment_type !== "Pay") {
            frappe.throw(__('Payment Type must be "Pay" when Party Type is Supplier'));
        }

        if (frm.doc.party_type === "Customer" && frm.doc.payment_type !== "Receive") {
            frappe.throw(__('Payment Type must be "Receive" when Party Type is Customer'));
        }
    },
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

    party_type: function(frm) {
        // فلتر ديناميكي لحقل party بناءً على party_type
        frm.set_query("party", () => {
            return {
                filters: {
                    party_type: frm.doc.party_type
                }
            };
        });
    }
});
