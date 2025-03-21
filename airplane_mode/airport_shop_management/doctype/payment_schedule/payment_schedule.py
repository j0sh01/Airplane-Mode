# Copyright (c) 2025, Joshua Michael and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import add_days, format_date, getdate, nowdate
from airplane_mode.utils.email_notifications import send_payment_confirmation

class PaymentSchedule(Document):
    def validate(self):
        self.update_overdue_status()

    def update_overdue_status(self):
        update_overdue_status(self)

def update_overdue_status(doc):
    if doc.due_date and getdate(doc.due_date) < getdate(nowdate()) and doc.status == "Pending":
        doc.status = "Overdue"

    if doc.status == "Paid":
        send_payment_confirmation(doc.name)


