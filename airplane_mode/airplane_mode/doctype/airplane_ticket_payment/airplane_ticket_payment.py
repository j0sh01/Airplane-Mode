# Copyright (c) 2025, Joshua Michael and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document

class AirplaneTicketPayment(Document):
    def validate(self):
        # Validate payment amount is positive
        if self.payment_amount <= 0:
            frappe.throw("Payment amount must be greater than zero")
            
        # Validate payment doesn't exceed remaining balance
        ticket = frappe.get_doc("Airplane Ticket", self.ticket)
        if self.payment_amount > ticket.balance_due:
            frappe.throw(f"Payment amount ({self.payment_amount}) exceeds remaining balance ({ticket.balance_due})")
    

    def before_save(self):
        self.received_by = frappe.utils.get_fullname()


    def on_submit(self):
        # Update the ticket payment details
        ticket = frappe.get_doc("Airplane Ticket", self.ticket)
        
        # Update paid amount and balance due
        paid_amount = ticket.paid_amount + self.payment_amount
        balance_due = ticket.total_amount - paid_amount
        
        # Determine payment status
        payment_status = "Unpaid"
        if balance_due <= 0:
            payment_status = "Paid"
        elif paid_amount > 0:
            payment_status = "Partially Paid"
        
        # Update the ticket
        frappe.db.set_value("Airplane Ticket", self.ticket, {
            "paid_amount": paid_amount,
            "balance_due": balance_due,
            "payment_status": payment_status
        })
        
        # Create receipt number
        self.receipt_number = f"{self.name}"
        
        frappe.db.commit()
        
        # Show success message
        frappe.msgprint(f"Payment of {self.payment_amount} recorded successfully. Receipt: {self.receipt_number}")

    def on_cancel(self):
        # Revert changes to the ticket when a payment is cancelled
        ticket = frappe.get_doc("Airplane Ticket", self.ticket)
        
        # Update paid amount and balance due
        paid_amount = ticket.paid_amount - self.payment_amount
        balance_due = ticket.total_amount - paid_amount
        
        # Determine payment status
        payment_status = "Unpaid"
        if balance_due <= 0:
            payment_status = "Paid"
        elif paid_amount > 0:
            payment_status = "Partially Paid"
        
        # Update the ticket
        frappe.db.set_value("Airplane Ticket", self.ticket, {
            "paid_amount": paid_amount,
            "balance_due": balance_due,
            "payment_status": payment_status
        })
        
        frappe.db.commit()
        frappe.msgprint(f"Payment of {self.payment_amount} has been cancelled")
