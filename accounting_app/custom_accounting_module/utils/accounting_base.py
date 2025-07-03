import frappe
from frappe.model.document import Document

class AccountingBase(Document):

    def validate_fiscal_year(self, posting_date):
        fiscal_year = frappe.db.exists("Fiscal Year", {
            "start_date": ["<=", posting_date],
            "end_date": [">=", posting_date]
        })

        if not fiscal_year:
            frappe.throw("Posting date must fall within a valid Fiscal Year.")

    def make_gl_entries(self):
        entries = self.get_gl_entries()
        if not entries:
            return
        for entry in entries:
            gl_entry = frappe.new_doc("GL Entry")
            gl_entry.update({
                "posting_date": self.posting_date,
                "account": entry.get("account"),
                "party": entry.get("party"),
                "debit": entry.get("debit", 0),
                "credit": entry.get("credit", 0),
                "voucher_type": self.doctype,
                "voucher_no": self.name,
                "is_cancelled": 0,
            })
            gl_entry.insert()

    def cancel_gl_entries(self):
        entries = self.get_gl_entries()
        if not entries:
            return
        for entry in entries:
            gl_entry = frappe.new_doc("GL Entry")
            gl_entry.update({
                "posting_date": self.posting_date,
                "account": entry.get("account"),
                "party": entry.get("party"),
                "debit": entry.get("credit", 0),   # عكس القيود
                "credit": entry.get("debit", 0),
                "voucher_type": self.doctype,
                "voucher_no": self.name,
                "is_cancelled": 1,
            })
            gl_entry.insert()
            