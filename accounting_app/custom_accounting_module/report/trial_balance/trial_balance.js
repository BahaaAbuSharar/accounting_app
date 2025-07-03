frappe.query_reports["Trial Balance"] = {
    filters: [
        {
            fieldname: "from_date",
            label: "From Date",
            fieldtype: "Date",
            reqd: 1
        },
        {
            fieldname: "to_date",
            label: "To Date",
            fieldtype: "Date",
            default: frappe.datetime.get_today(),
            reqd: 1
        },
        {
            fieldname: "account",
            label: "Account",
            fieldtype: "Link",
            options: "Account"
        },
        {
            fieldname: "include_cancelled_entries",
            label: "Include Cancelled Entries",
            fieldtype: "Check",
            default: 0
        }
    ]
};
