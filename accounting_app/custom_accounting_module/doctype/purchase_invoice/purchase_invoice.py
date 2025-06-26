# Copyright (c) 2025, Bahaa and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PurchaseInvoice(Document):
	def validate(self):
		self.total_qty = 0
		self.total_amount = 0

		for item in self.items:
			item.amount = (item.qty or 0) * (item.rate or 0)
			self.total_qty += item.qty or 0
			self.total_amount += item.amount or 0

			if item.rate is not None and item.rate < 0:
					frappe.throw(f"Item '{item.item}' has a negative rate in Sales Invoice.")
