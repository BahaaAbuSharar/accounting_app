import frappe
from frappe.utils import flt

class AccountingReportHelper:
    def __init__(self, filters=None):
        self.filters = filters or {}

    def get_filtered_gl_entries(self):
        conditions = "1=1"
        if self.filters.get("from_date"):
            conditions += f" AND posting_date >= '{self.filters['from_date']}'"
        if self.filters.get("to_date"):
            conditions += f" AND posting_date <= '{self.filters['to_date']}'"
        if self.filters.get("account"):
            conditions += f" AND account = '{self.filters['account']}'"
        if self.filters.get("party"):
            conditions += f" AND party = '{self.filters['party']}'"

        conditions += " AND is_cancelled = 0"

        return frappe.db.sql(f"""
            SELECT
                posting_date, account, party,
                debit_amount AS debit, credit_amount AS credit,
                voucher_type, voucher_number AS voucher_no
            FROM `tabGL Entry`
            WHERE {conditions}
            ORDER BY posting_date, name
        """, as_dict=True)

    def add_running_balance(self, entries):
        balance = 0
        for entry in entries:
            balance += flt(entry.get("debit", 0)) - flt(entry.get("credit", 0))
            entry["balance"] = balance
        return entries
