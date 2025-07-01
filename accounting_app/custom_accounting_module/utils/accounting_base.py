import frappe
from frappe.model.document import Document

class AccountingBase(Document):

    def validate_fiscal_year(self):
        fiscal_year = frappe.db.exists("Fiscal Year", {
            "start_date": ["<=", self.posting_date],
            "end_date": [">=", self.posting_date]
        })

        if not fiscal_year:
            frappe.throw("Posting date must fall within a valid Fiscal Year.")