from frappe.model.document import Document
import frappe

class JournalEntry(Document):

    def validate(self):
        self.set_totals()
        if round(self.total_debit, 2) != round(self.total_credit, 2):
            frappe.throw("Total Debit and Total Credit must be equal.")

    def set_totals(self):
        self.total_debit = 0
        self.total_credit = 0
        for row in self.accounts:
            self.total_debit += row.debit or 0
            self.total_credit += row.credit or 0
        self.difference = self.total_debit - self.total_credit

    def on_submit(self):
        self.create_gl_entries()

    def on_cancel(self):
        self.cancel_gl_entries()

    def create_gl_entries(self):
        for row in self.accounts:
            gl_entry = frappe.get_doc({
                "doctype": "GL Entry",
                "posting_date": self.posting_date,
                "party": row.party,
                "account": row.account,
                "debit_amount": row.debit or 0,
                "credit_amount": row.credit or 0,
                "voucher_type": "Journal Entry",
                "voucher_no": self.name
            })
            gl_entry.insert()

    def cancel_gl_entries(self):
        frappe.db.set_value("GL Entry", {"voucher_type": "Journal Entry", "voucher_no": self.name}, "is_cancelled", 1)
