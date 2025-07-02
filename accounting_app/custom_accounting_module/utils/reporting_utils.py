import frappe
from frappe.utils import flt

class AccountingReportHelper:
    def __init__(self, filters=None):
        self.filters = filters or {}

    def get_filtered_gl_entries(self , with_balance=False , include_account_number=False):
        conditions = []
        values = []
        if self.filters.get("from_date"):
            conditions.append("posting_date >= %s")
            values.append(self.filters["from_date"])
        if self.filters.get("to_date"):
            conditions.append("posting_date <= %s")
            values.append(self.filters["to_date"])
        if self.filters.get("account"):
            conditions.append("account = %s")
            values.append(self.filters["account"])
        if self.filters.get("party"):
            conditions.append("party = %s")
            values.append(self.filters["party"])

        where_clause = " AND ".join(conditions)
        if where_clause:
            where_clause = "WHERE " + where_clause

        fields = [
            "e.posting_date",
            "e.account",
            "e.party",
            "e.debit_amount AS debit",
            "e.credit_amount AS credit",
            "e.voucher_type",
            "e.voucher_number AS voucher_no"
        ]
        if include_account_number:
            fields.append("a.account_number")
            join_clause = "LEFT JOIN `tabAccount` a ON e.account = a.name"
        else:
            join_clause = ""

        if with_balance:
            fields.append("""
                SUM(debit_amount - credit_amount) OVER (
                    ORDER BY posting_date, name
                ) AS balance
            """)

        query = f"""
            SELECT
                {', '.join(fields)}
            FROM `tabGL Entry` e
            {join_clause}
            {where_clause}
            ORDER BY posting_date, name
        """

        return frappe.db.sql(query, values, as_dict=True)
    def group_by_account(self, entries):
        summary = {}
        for entry in entries:
            acct = entry["account"]
            if acct not in summary:
                summary[acct] = {"debit": 0.0, "credit": 0.0}
            summary[acct]["debit"] += flt(entry.get("debit", 0))
            summary[acct]["credit"] += flt(entry.get("credit", 0))
        return summary