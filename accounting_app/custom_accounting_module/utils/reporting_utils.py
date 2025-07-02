import frappe
from frappe.utils import flt

class AccountingReportHelper:
    def __init__(self, filters=None):
        self.filters = filters or {}

    def get_filtered_gl_entries(self , with_balance=False):
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
            "posting_date", "account", "party",
            "debit_amount AS debit", "credit_amount AS credit",
            "voucher_type", "voucher_number AS voucher_no"
        ]

        if with_balance:
            fields.append("""
                SUM(debit_amount - credit_amount) OVER (
                    ORDER BY posting_date, name
                ) AS balance
            """)

        query = f"""
            SELECT
                {', '.join(fields)}
            FROM `tabGL Entry`
            {where_clause}
            ORDER BY posting_date, name
        """

        return frappe.db.sql(query, values, as_dict=True)
