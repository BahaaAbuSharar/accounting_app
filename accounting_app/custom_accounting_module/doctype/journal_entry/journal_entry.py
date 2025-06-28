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
        if round(self.difference, 2) != 0:
            frappe.throw(_("The restriction is unbalanced: the total debtor ({0}) is not equal to the total creditor ({1})").format(
                self.total_debit, self.total_credit
            ))
