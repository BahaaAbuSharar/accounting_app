# Copyright (c) 2025, Bahaa and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from accounting_app.custom_accounting_module.utils.validation import validate_fiscal_year

class PurchaseInvoice(Document):
	def validate(self):
		validate_fiscal_year(self.posting_date)
		self.total_qty = 0
		self.total_amount = 0
		# تحقق من التواريخ
		if self.payment_due_date and self.posting_date:
			if self.payment_due_date < self.posting_date:
				frappe.throw("Payment Due Date cannot be before Posting Date.")		

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

	def make_gl_entries(self):
		amount = self.total_amount

		# القيود المحاسبية العادية
		frappe.get_doc({
			"doctype": "GL Entry",
			"posting_date": self.posting_date,
			"due_date": self.payment_due_date,
			"party": self.supplier, 
			"account": self.credit_to,
			"debit_amount": amount,
			"credit_amount": 0,
			"voucher_type": "Purchase Invoice",
			"voucher_number": self.name,
			"is_cancelled": 0
		}).insert()

		frappe.get_doc({
			"doctype": "GL Entry",
			"posting_date": self.posting_date,
			"account": self.expense_account,
			"debit_amount": 0,
			"credit_amount": amount,
			"voucher_type": "Purchase Invoice",
			"voucher_number": self.name,
			"is_cancelled": 0
		}).insert()


	def make_gl_entries_reverse(self):
		amount = self.total_amount

		# عكس القيد عند الإلغاء
		frappe.get_doc({
			"doctype": "GL Entry",
			"posting_date": self.posting_date,
			"due_date": self.payment_due_date,
			"party": self.supplier,
			"account": self.credit_to,
			"debit_amount": 0,
			"credit_amount": amount,
			"voucher_type": "Purchase Invoice",
			"voucher_number": self.name,
			"is_cancelled": 1
		}).insert()

		frappe.get_doc({
			"doctype": "GL Entry",
			"posting_date": self.posting_date,
			"account": self.expense_account,
			"debit_amount": amount,
			"credit_amount": 0,
			"voucher_type": "Purchase Invoice",
			"voucher_number": self.name,
			"is_cancelled": 1
		}).insert()

