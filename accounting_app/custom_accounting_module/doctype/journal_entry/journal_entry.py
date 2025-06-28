import frappe
from frappe import _

class JournalEntry(Document):
    def validate(self):
        self.calculate_totals()

    def calculate_totals(self):
        self.total_debit = sum([d.debit or 0 for d in self.accounting_entries])
        self.total_credit = sum([d.credit or 0 for d in self.accounting_entries])
        self.difference = self.total_debit - self.total_credit
