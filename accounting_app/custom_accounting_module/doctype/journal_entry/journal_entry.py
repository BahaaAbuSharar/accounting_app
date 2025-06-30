import frappe
from frappe import _
from frappe.model.document import Document


class JournalEntry(Document):
    def validate(self):
        self.calculate_totals()
        self.check_balance()

    def calculate_totals(self):
        self.total_debit = sum([d.debit or 0 for d in self.accounting_entries])
        self.total_credit = sum([d.credit or 0 for d in self.accounting_entries])
        self.difference = self.total_debit - self.total_credit

    def check_balance(self):
        if self.difference != 0:
            frappe.throw(_("The restriction is unbalanced: the total debtor ({0}) is not equal to the total creditor ({1})").format(
                self.total_debit, self.total_credit
            ))
    def on_submit(self):
        self.make_gl_entries()

    def on_cancel(self):
        self.make_gl_entries_reverse()

    def make_gl_entries(self):
        for row in self.accounting_entries:
            frappe.get_doc({
                "doctype": "GL Entry",
                "posting_date": self.posting_date,
                "party": row.party,
                "account": row.account,
                "debit_amount": row.debit or 0,
                "credit_amount": row.credit or 0,
                "voucher_type": "Journal Entry",
                "voucher_number": self.name,
                "is_cancelled": 0,
                "remarks": row.description
            }).insert()

    def make_gl_entries_reverse(self):
        for row in self.accounting_entries:
            frappe.get_doc({
                "doctype": "GL Entry",
                "posting_date": self.posting_date,
                "party": row.party,
                "account": row.account,
                "debit_amount": row.credit or 0,
                "credit_amount": row.debit or 0,
                "voucher_type": "Journal Entry",
                "voucher_number": self.name,
                "is_cancelled": 1,
                "remarks": row.description
            }).insert()
