import frappe
from frappe.model.document import Document
from frappe.utils.data import flt

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
                "debit_amount": entry.get("debit", 0),
                "credit_amount": entry.get("credit", 0),
                "voucher_type": self.doctype,
                "voucher_number": self.name,
                "is_cancelled": 0,
            })
            gl_entry.insert()

            gl_entry.account_balance_after_entry = AccountingBase.get_account_balance_after(
                gl_entry.account, self.posting_date, gl_entry.name
            )
            gl_entry.save()

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
                "debit_amount": entry.get("credit", 0),   # عكس القيود
                "credit_amount": entry.get("debit", 0),
                "voucher_type": self.doctype,
                "voucher_number": self.name,
                "is_cancelled": 1,
            })
            gl_entry.insert()

            gl_entry.account_balance_after_entry = AccountingBase.get_account_balance_after(
                gl_entry.account, self.posting_date, gl_entry.name
            )
            gl_entry.save()

    @staticmethod        
    def get_account_balance_after(account, posting_date, gl_entry_name):
        balance = frappe.db.sql("""
            SELECT SUM(debit_amount - credit_amount)
            FROM `tabGL Entry`
            WHERE account = %s
            AND (posting_date < %s OR (posting_date = %s AND name <= %s))
            AND is_cancelled = 0
        """, (account, posting_date, posting_date, gl_entry_name))[0][0] or 0.0
        
        return flt(balance)
