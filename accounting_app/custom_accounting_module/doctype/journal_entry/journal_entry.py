import frappe
from frappe import _
from accounting_app.custom_accounting_module.utils.accounting_base import AccountingBase


class JournalEntry(AccountingBase):
    def validate(self):
        self.validate_fiscal_year(self.posting_date)
        self.calculate_totals()
        self.check_balance()
        # التأكد من تاريخ القيد
        if not self.posting_date:
            frappe.throw(_("Posting date is required. Please set a valid posting date."))

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
        self.cancel_gl_entries()

    def get_gl_entries(self):
        entries = []

        for row in self.accounts:
            entries.append({
                "account": row.account,
                "party": row.party,
                "debit": row.debit or 0,
                "credit": row.credit or 0,
            })

        return entries

