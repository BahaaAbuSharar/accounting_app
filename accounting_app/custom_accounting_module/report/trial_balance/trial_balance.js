frappe.query_reports["Trial Balance"] = {
    "filters": [
        {
            fieldname: "from_date",
            label: __("From Date"),
            fieldtype: "Date",
            default: frappe.sys_defaults.year_start
        },
        {
            fieldname: "to_date",
            label: __("To Date"),
            fieldtype: "Date",
            default: frappe.sys_defaults.year_end
        },
        {
            fieldname: "account",
            label: __("Account"),
            fieldtype: "Link",
            options: "Account"
        }
    ]
};

