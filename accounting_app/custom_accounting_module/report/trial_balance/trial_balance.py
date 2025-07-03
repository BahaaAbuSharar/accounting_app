import frappe
from frappe import _
from frappe.utils import flt

def execute(filters=None):
    if not filters:
        filters = {}

    validate_from_date_before_to_date(filters)
    columns = get_columns()
    data = get_data(filters)

    return columns, data

def validate_from_date_before_to_date(filters):
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")

    if from_date > to_date:
        frappe.throw(_("From Date cannot be after To Date"))

def get_columns():
    return [
        {"label": _("Account"), "fieldname": "account", "fieldtype": "Link", "options": "Account", "width": 200},
        {"label": _("Opening Balance"), "fieldname": "opening_balance", "fieldtype": "Currency", "width": 130},
        {"label": _("Debit"), "fieldname": "debit", "fieldtype": "Currency", "width": 100},
        {"label": _("Credit"), "fieldname": "credit", "fieldtype": "Currency", "width": 100},
        {"label": _("Closing Balance"), "fieldname": "closing_balance", "fieldtype": "Currency", "width": 130},
    ]

def get_data(filters):
    from_date = filters["from_date"]
    to_date = filters["to_date"]
    account_filter = filters.get("account")

    conditions = ["is_cancelled = 0"]
    values = {
        "from_date": from_date,
        "to_date": to_date
    }

    if account_filter:
        conditions.append("account = %(account)s")
        values["account"] = account_filter     

    where_clause = "WHERE " + " AND ".join(conditions)

    query = f"""
        SELECT
            account,
            SUM(CASE WHEN posting_date < %(from_date)s THEN debit_amount - credit_amount ELSE 0 END) AS opening_balance,
            SUM(CASE WHEN posting_date BETWEEN %(from_date)s AND %(to_date)s THEN debit_amount ELSE 0 END) AS debit,
            SUM(CASE WHEN posting_date BETWEEN %(from_date)s AND %(to_date)s THEN credit_amount ELSE 0 END) AS credit
        FROM `tabGL Entry`
        {where_clause}
        GROUP BY account
    """

    entries = frappe.db.sql(query, values, as_dict=True)

    result = []
    for row in entries:
        closing = flt(row.opening_balance) + flt(row.debit) - flt(row.credit)
        if flt(row.debit) != 0 or flt(row.credit) != 0:
            result.append({
                "account": row.account,
                "opening_balance": flt(row.opening_balance),
                "debit": flt(row.debit),
                "credit": flt(row.credit),
                "closing_balance": closing,
            })

    return result
