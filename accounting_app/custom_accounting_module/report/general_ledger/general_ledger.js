// path: accounting_app/custom_accounting_module/report/general_ledger/general_ledger.js
frappe.query_reports["General Ledger"] = {
    "filters": [
        {
            "fieldname":"from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.defaults.get_default("year_start_date"),
            "reqd": 1
        },
        {
            "fieldname":"to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.defaults.get_default("year_end_date"),
            "reqd": 1
        },
        {
            "fieldname":"account",
            "label": __("Account"),
            "fieldtype": "Link",
            "options": "Account"
        },
        {
            "fieldname":"party",
            "label": __("Party"),
            "fieldtype": "Link",
            "options": "Party"
        }
    ]
};
