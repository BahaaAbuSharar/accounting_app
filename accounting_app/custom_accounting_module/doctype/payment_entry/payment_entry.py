from frappe.model.document import Document
import frappe

class PaymentEntry(Document):
    def validate(self):
        # تأكد من التوازن أو القيود
        if self.paid_from == self.paid_to:
            frappe.throw("Account Paid From and Paid To cannot be the same.")

    def on_submit(self):
        self.create_gl_entries()

    def on_cancel(self):
        self.cancel_gl_entries()

    def create_gl_entries(self):
        # مثال ترحيل إلى GL Entry
        gl_entries = []

        # Entry 1: الخصم
        gl_entries.append({
            'posting_date': self.posting_date,
            'account': self.paid_from,
            'party': self.party,
            'debit_amount': self.amount if self.payment_type == 'Pay' else 0,
            'credit_amount': self.amount if self.payment_type == 'Receive' else 0,
            'voucher_type': 'Payment Entry',
            'voucher_no': self.name
        })

        # Entry 2: القيد المقابل
        gl_entries.append({
            'posting_date': self.posting_date,
            'account': self.paid_to,
            'party': self.party,
            'debit_amount': self.amount if self.payment_type == 'Receive' else 0,
            'credit_amount': self.amount if self.payment_type == 'Pay' else 0,
            'voucher_type': 'Payment Entry',
            'voucher_no': self.name
        })

        for entry in gl_entries:
            gl_doc = frappe.get_doc({
                'doctype': 'GL Entry',
                **entry
            })
            gl_doc.insert()

    def cancel_gl_entries(self):
     gl_entries = frappe.get_all("GL Entry", filters={
        "voucher_type": "Payment Entry",
        "voucher_no": self.name
     })

     for entry in gl_entries:
        frappe.db.set_value("GL Entry", entry.name, "is_cancelled", 1)


