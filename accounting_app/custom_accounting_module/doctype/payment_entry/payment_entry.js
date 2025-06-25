frappe.ui.form.on('Payment Entry', {
    onload: function(frm) {
        frm.set_query('paid_from', () => {
            return {
                filters: {
                    account_type: frm.doc.payment_type === 'Receive' ? 'Receivable' : 'Bank'
                }
            };
        });

        frm.set_query('paid_to', () => {
            return {
                filters: {
                    account_type: frm.doc.payment_type === 'Pay' ? 'Payable' : 'Bank'
                }
            };
        });
    },

    payment_type: function(frm) {
        frm.set_value('paid_from', null);
        frm.set_value('paid_to', null);
        frm.trigger('onload'); // لإعادة الفلاتر
    }
});
