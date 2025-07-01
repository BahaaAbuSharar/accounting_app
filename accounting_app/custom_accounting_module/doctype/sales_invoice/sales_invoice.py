# Copyright (c) 2025, Bahaa and contributors
# For license information, please see license.txt

import frappe
from accounting_app.custom_accounting_module.utils.accounting_base import AccountingBase

class SalesInvoice(AccountingBase):
    def validate(self):
        self.validate_fiscal_year(self.posting_date)
        self.total_qty = 0
        self.total_amount = 0


        for item in self.items:
            item.amount = (item.qty or 0) * (item.rate or 0)
            self.total_qty += item.qty or 0
            self.total_amount += item.amount or 0

            if item.rate is not None and item.rate < 0:
                 frappe.throw(f"Item '{item.item}' has a negative rate in Sales Invoice.")
    def on_submit(self):
        self.make_gl_entries()

    def on_cancel(self):
        self.cancel_gl_entries()

    def get_gl_entries(self):
        amount = self.total_amount

        return [
            {
                "account": self.debit_to,  # حساب العميل
                "party": self.customer,
                "debit": amount,
                "credit": 0,
            },
            {
                "account": self.income_account,  # حساب الدخل
                "debit": 0,
                "credit": amount,
            }
        ]