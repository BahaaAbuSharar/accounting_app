import frappe
from frappe import _

def validate_fiscal_date(date):
    
    fiscal_year = frappe.db.exists("Fiscal Year", {
        "start_date": ["<=", date],
        "end_date": [">=", date]
    })

    if not fiscal_year:
        frappe.throw(_("Posting date must fall within a valid Fiscal Year."))
