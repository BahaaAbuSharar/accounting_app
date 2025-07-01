import frappe
from accounting_app.custom_accounting_module.utils.accounting_base import AccountingBase

class PaymentEntry(AccountingBase):
    def validate(self):
        self.validate_fiscal_year(self.posting_date)
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
        self.cancel_gl_entries()

    def get_gl_entries(self):
        amount = self.paid_amount

        if self.payment_type == "Receive":
            return [
                {
                    "account": self.paid_to,  # البنك
                    "debit": amount,
                    "credit": 0,
                },
                {
                    "account": self.paid_from,  # حساب الزبون
                    "party": self.party,
                    "debit": 0,
                    "credit": amount,
                }
            ]
        elif self.payment_type == "Pay":
            return [
                {
                    "account": self.paid_from,  # البنك
                    "credit": amount,
                    "debit": 0,
                },
                {
                    "account": self.paid_to,  # حساب المورد
                    "party": self.party,
                    "debit": amount,
                    "credit": 0,
                }
            ]


