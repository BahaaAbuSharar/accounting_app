import frappe
from frappe import _
from frappe.utils import flt

def execute(filters=None):
    if not filters:
        filters = {}

    validate_filters(filters)

    columns = get_columns()
    data = get_data(filters)

    return columns, data

def validate_filters(filters):
	# التحقق من ان تاريخ البداية قبل تاريخ النهاية
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

import frappe
from frappe import _
from frappe.utils import flt

def execute(filters=None):
    if not filters:
        filters = {}

    validate_filters(filters)
    columns = get_columns()
    data = get_data(filters)

    return columns, data

def validate_filters(filters):
    if not filters.get("from_date") or not filters.get("to_date"):
        frappe.throw(_("Please specify From Date and To Date"))

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
	include_cancelled = filters.get("include_cancelled_entries")

	conditions = []
	values = {
		"from_date": from_date,
		"to_date": to_date
	}

	if account_filter:
		conditions.append("account = %(account)s")
		values["account"] = account_filter     

	if not include_cancelled:
		conditions.append("is_cancelled = 0")

	if conditions:
		where_clause = "WHERE " + " AND ".join(conditions)
	else:
		where_clause = "" 

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

