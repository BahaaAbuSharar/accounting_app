import frappe
from frappe.model.document import Document
from accounting_app.custom_accounting_module.utils.validation import validate_fiscal_date

class PaymentEntry(Document):
    def validate(self):
        validate_fiscal_date(self.posting_date)
        # التأكد من تاريخ القيد
        if not self.posting_date:
            self.posting_date = frappe.utils.today()

        # المبلغ يجب أن يكون موجبًا
        if self.amount is None or self.amount <= 0:
            frappe.throw("Amount must be greater than 0.")
            
        # التأكد من أن الحسابات المدفوعة منها والمدفوعة إليها ليست هي نفسها
        if self.account_paid_from == self.account_paid_to:
            frappe.throw("Source and Destination accounts cannot be the same.")

    def on_submit(self):
        self.make_gl_entries()

    def on_cancel(self):
        self.make_gl_entries_reverse()

    def make_gl_entries(self):
        # حسب نوع الدفع
        if self.payment_type == "Receive":
            debit_account = self.account_paid_to
            credit_account = self.account_paid_from
        else :# self.payment_type == "Pay"
            debit_account = self.account_paid_from
            credit_account = self.account_paid_to

        frappe.get_doc({
            "doctype": "GL Entry",
            "posting_date": self.posting_date,
            "party": self.party,
            "account": debit_account,
            "debit_amount": self.amount,
            "credit_amount": 0,
            "voucher_type": "Payment Entry",
            "voucher_number": self.name,
            "is_cancelled": 0
        }).insert()

        frappe.get_doc({
            "doctype": "GL Entry",
            "posting_date": self.posting_date,
            "party": self.party,
            "account": credit_account,
            "debit_amount": 0,
            "credit_amount": self.amount,
            "voucher_type": "Payment Entry",
            "voucher_number": self.name,
            "is_cancelled": 0
        }).insert()

    def make_gl_entries_reverse(self):
        # قلب القيود
        if self.payment_type == "Receive":
            debit_account = self.account_paid_to
            credit_account = self.account_paid_from
        else :
            debit_account = self.account_paid_from
            credit_account = self.account_paid_to

        frappe.get_doc({
            "doctype": "GL Entry",
            "posting_date": self.posting_date,
            "party": self.party,
            "account": debit_account,
            "debit_amount": self.amount,
            "credit_amount": 0,
            "voucher_type": "Payment Entry",
            "voucher_number": self.name,
            "is_cancelled": 1
        }).insert()

        frappe.get_doc({
            "doctype": "GL Entry",
            "posting_date": self.posting_date,
            "party": self.party,
            "account": credit_account,
            "debit_amount": 0,
            "credit_amount": self.amount,
            "voucher_type": "Payment Entry",
            "voucher_number": self.name,
            "is_cancelled": 1
        }).insert()
                
