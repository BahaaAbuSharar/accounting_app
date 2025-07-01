from accounting_app.custom_accounting_module.utils.reporting_utils import AccountingReportHelper

def execute(filters=None):
    filters = filters or {}

    helper = AccountingReportHelper(filters)
    entries = helper.get_filtered_gl_entries()
    entries = helper.add_running_balance(entries)

    columns = get_columns()
    return columns, entries

def get_columns():
    return [
        {"label": "Posting Date", "fieldname": "posting_date", "fieldtype": "Date", "width": 100},
        {"label": "Account", "fieldname": "account", "fieldtype": "Link", "options": "Account", "width": 180},
        {"label": "Party", "fieldname": "party", "fieldtype": "Link", "options": "Party", "width": 150},
        {"label": "Debit", "fieldname": "debit", "fieldtype": "Currency", "width": 100},
        {"label": "Credit", "fieldname": "credit", "fieldtype": "Currency", "width": 100},
        {"label": "Balance", "fieldname": "balance", "fieldtype": "Currency", "width": 120},
        {"label": "Voucher Type", "fieldname": "voucher_type", "fieldtype": "Data", "width": 120},
        {"label": "Voucher No", "fieldname": "voucher_no", "fieldtype": "Dynamic Link", "options": "voucher_type", "width": 150},
    ]
