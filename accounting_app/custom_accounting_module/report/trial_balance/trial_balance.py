from accounting_app.custom_accounting_module.utils.reporting_utils import AccountingReportHelper
from frappe import _
from frappe.utils import flt

def execute(filters=None):
    filters = filters or {}
    helper = AccountingReportHelper(filters)
    entries = helper.get_filtered_gl_entries(include_account_number=True)
    summary = helper.group_by_account(entries)

    data = []
    for account, amounts in summary.items():
        debit = flt(amounts.get("debit", 0))
        credit = flt(amounts.get("credit", 0))
        balance = debit - credit
        data.append({
            "account": account,
            "account_name": helper.get_account_name(account),
            "debit": debit,
            "credit": credit,
            "balance": balance
        })

    columns = get_columns()
    return columns, data

def get_columns():
    return [
        {"label": _("Account"), "fieldname": "account", "fieldtype": "Link", "options": "Account", "width": 200},
        {"label": _("Account Name"), "fieldname": "account_name", "fieldtype": "Data", "width": 200},
        {"label": _("Debit"), "fieldname": "debit", "fieldtype": "Currency", "width": 120},
        {"label": _("Credit"), "fieldname": "credit", "fieldtype": "Currency", "width": 120},
        {"label": _("Balance"), "fieldname": "balance", "fieldtype": "Currency", "width": 120},
    ]
