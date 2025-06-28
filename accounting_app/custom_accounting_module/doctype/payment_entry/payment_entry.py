import frappe
from frappe.model.document import Document

class PaymentEntry(Document):
    def validate(self):
        # التأكد من تاريخ القيد
        if not self.posting_date:
            self.posting_date = frappe.utils.today()

        # المبلغ يجب أن يكون موجبًا
        if self.amount is None or self.amount <= 0:
            frappe.throw("Amount must be greater than 0.")
            
        # التأكد من أن الحسابات المدفوعة منها والمدفوعة إليها ليست هي نفسها
        if self.account_paid_from == self.account_paid_to:
            frappe.throw("Source and Destination accounts cannot be the same.")

 