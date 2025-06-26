# Copyright (c) 2025, Bahaa and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class Item(Document):
	def validate(self):
			
		if self.standard_selling_rate is not None and self.standard_selling_rate <= 0 or self.standard_purchase_rate is not None and self.standard_purchase_rate <= 0:
				frappe.throw("Standard Rate cannot be negative or zero.")


