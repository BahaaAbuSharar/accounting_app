# Copyright (c) 2025, Bahaa and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from accounting_app.custom_accounting_module.utils.validation import validate_fiscal_date 

class SalesInvoice(Document):
    def validate(self):
        validate_fiscal_date(self.posting_date)
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
        self.make_gl_entries_reverse()

    def make_gl_entries(self, reverse=False):

        amount = self.total_amount
  
        debit_customer = amount
        credit_customer = 0
        debit_income = 0
        credit_income = amount

        # قيد للعميل
        frappe.get_doc({
            "doctype": "GL Entry",
            "posting_date": self.posting_date,
            "due_date": self.payment_due_date,
            "party": self.customer,
            "account": self.debit_to,
            "debit_amount": debit_customer,
            "credit_amount": credit_customer,
            "voucher_type": "Sales Invoice",
            "voucher_number": self.name,
            "is_cancelled": 0
        }).insert()

        # قيد لحساب الدخل
        frappe.get_doc({
            "doctype": "GL Entry",
            "posting_date": self.posting_date,
            "account": self.income_account,
            "debit_amount": debit_income,
            "credit_amount": credit_income,
            "voucher_type": "Sales Invoice",
            "voucher_number": self.name,
            "is_cancelled": 0
        }).insert()

        frappe.db.commit()


    def make_gl_entries_reverse(self):

        amount = self.total_amount
        debit_customer = 0
        credit_customer = amount
        debit_income = amount
        credit_income = 0


        # قيد للعميل
        frappe.get_doc({
            "doctype": "GL Entry",
            "posting_date": self.posting_date,
            "due_date": self.payment_due_date,
            "party": self.customer,
            "account": self.debit_to,
            "debit_amount": debit_customer,
            "credit_amount": credit_customer,
            "voucher_type": "Sales Invoice",
            "voucher_number": self.name,
            "is_cancelled": 1
        }).insert()

        # قيد لحساب الدخل
        frappe.get_doc({
            "doctype": "GL Entry",
            "posting_date": self.posting_date,
            "account": self.income_account,
            "debit_amount": debit_income,
            "credit_amount": credit_income,
            "voucher_type": "Sales Invoice",
            "voucher_number": self.name,
            "is_cancelled": 1
        }).insert()

        frappe.db.commit()    