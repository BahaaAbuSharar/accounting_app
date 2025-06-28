from frappe.model.document import Document
import frappe

class GLEntry(Document):

    def validate(self):
        # مثال: منع تعيين قيمتين في نفس الوقت
        if self.debit_amount and self.credit_amount:
            frappe.throw("You cannot have both Debit and Credit values at the same time.")
