import frappe
from frappe.model.document import Document
from frappe.utils import getdate, add_months, add_days, nowdate, formatdate
from frappe import throw, _
import calendar

class AirportShop(Document):
    def validate(self):
        self.validate_contract_dates()
        self.update_shop_status()
        self.set_airport_code()
        self.rent_amount()
        
    def on_update(self):
        if self.has_value_changed('tenant') or self.has_value_changed('contract_start_date') or self.has_value_changed('contract_end_date'):
            self.generate_payment_schedules()

    def validate_contract_dates(self):
        if self.contract_start_date:
            settings = frappe.get_single("Shop Settings")
            frequency = settings.frequency
            if frequency == "Monthly":
                self.contract_end_date = add_months(self.contract_start_date, 1)
            elif frequency == "3 Months":
                self.contract_end_date = add_months(self.contract_start_date, 3)
            elif frequency == "6 Months":
                self.contract_end_date = add_months(self.contract_start_date, 6)
            elif frequency == "Yearly":
                self.contract_end_date = add_months(self.contract_start_date, 12)
            
            if self.contract_end_date and getdate(self.contract_end_date) <= getdate(self.contract_start_date):
                throw(_("Contract End Date must be after Start Date"))

    def update_shop_status(self):
        if self.tenant and self.status != "Occupied":
            self.status = "Occupied"
        elif not self.tenant and self.status == "Occupied":
            self.status = "Available"

    def set_airport_code(self):
        if self.airport and not self.airport_code:
            self.airport_code = frappe.db.get_value("Airport", self.airport, "code")

    def generate_payment_schedules(self):
        if self.tenant and self.contract_start_date and self.contract_end_date:
            # Delete existing schedules
            frappe.db.delete("Payment Schedule", {"shop": self.name})
            
            start_date = getdate(self.contract_start_date)
            end_date = getdate(self.contract_end_date)
            monthly_rent = self.monthly_rent_amount or frappe.db.get_single_value("Shop Settings", "default_rent_amount")
            
            current_date = start_date
            while current_date < end_date:
                due_date = add_days(current_date.replace(day=1), 
                    frappe.db.get_single_value("Shop Settings", "reminder_days_before") or 5)
                
                frappe.get_doc({
                    "doctype": "Payment Schedule",
                    "shop": self.name,
                    "tenant": self.tenant,
                    "due_date": due_date,
                    "month": calendar.month_name[current_date.month],
                    "year": current_date.year,
                    "amount": monthly_rent,
                    "status": "Pending"
                }).insert()
                
                current_date = add_months(current_date, 1)

            frappe.msgprint(f"Payment schedules generated for {self.tenant} to shop {self.name}")

    def rent_amount(self):
        rent = frappe.get_doc("Shop Settings")
        self.monthly_rent_amount = rent.default_rent_amount
