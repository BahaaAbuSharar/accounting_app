from frappe.model.document import Document
import frappe

class GLEntry(Document):

    def validate(self):
        # تعيين التاريخ الحالي إذا لم يكن موجودًا
        if not self.posting_date:
            self.posting_date = frappe.utils.today()

        # التأكد من أن المبلغ المدين أو الدائن موجود
        if not self.debit_amount and not self.credit_amount:
            frappe.throw("Either Debit or Credit must be entered.")            
