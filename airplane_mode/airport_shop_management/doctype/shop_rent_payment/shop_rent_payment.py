# import frappe
# from frappe.model.document import Document
# from frappe.utils import nowdate, getdate

# class ShopRentPayment(Document):
#     def before_submit(self):
#         self.validate_payment_amount()
#         self.update_payment_schedule()
#         self.update_tenant_history()

#     def validate_payment_amount(self):
#         shop_rent = frappe.db.get_value("Airport Shop", self.shop, "monthly_rent_amount")
#         if self.amount != shop_rent:
#             frappe.throw(f"Payment amount must match shop's monthly rent ({shop_rent})")

#     def update_payment_schedule(self):
#         schedule = frappe.get_all(
#             "Payment Schedule",
#             filters={
#                 "shop": self.shop,
#                 "month": self.payment_for_month,
#                 "year": self.payment_for_year,
#                 "status": ["in", ["Pending", "Overdue"]]
#             },
#             fields=["name"]
#         )
        
#         if not schedule:
#             frappe.throw(f"Payment Schedule for shop {self.shop}, month {self.payment_for_month}, year {self.payment_for_year} not found")
        
#         schedule_doc = frappe.get_doc("Shop Rent Payment Schedule", schedule[0].name)
#         schedule_doc.status = "Paid"
#         schedule_doc.payment_reference = self.name
#         schedule_doc.save()

#     def update_tenant_history(self):
#         tenant = frappe.get_doc("Shop Tenant", self.tenant)
#         tenant.append("payment_history", {
#             "payment": self.name,
#             "shop": self.shop,
#             "payment_date": nowdate(),
#             "month": self.payment_for_month,
#             "year": self.payment_for_year,
#             "amount": self.amount,
#             "payment_method": self.payment_method,
#             "reference_number": self.reference_number
#         })
#         tenant.save()

#     def on_shop_selection(self):
#         shop = frappe.get_doc("Airport Shop", self.shop)
#         if shop.status != "Occupied":
#             frappe.throw(f"Shop {shop.shop_number} is not occupied. Cannot create rent payment.")
        
#         schedules = frappe.get_all(
#             "Payment Schedule",
#             filters={"shop": self.shop, "status": ["in", ["Pending", "Overdue"]]},
#             fields=["name", "month", "year", "amount"]
#         )
        
#         if not schedules:
#             frappe.throw("No pending or overdue payment schedules found for this shop.")
        
#         if len(schedules) > 1:
#             selected_schedule = self.show_schedule_selection_dialog(schedules)
#         else:
#             selected_schedule = schedules[0]
        
#         self.populate_payment_details(selected_schedule)
#         self.save()

#     def show_schedule_selection_dialog(self, schedules):
#         # This is a placeholder for the dialog logic
#         # In a real implementation, this would show a dialog to the user to select a schedule
#         # For now, we'll just return the first schedule
#         frappe.msgprint("Multiple payment schedules found. Please select one.")
#         return schedules[0]

#     def populate_payment_details(self, schedule):
#         self.payment_for_month = schedule["month"]
#         self.payment_for_year = schedule["year"]
#         self.amount = schedule["amount"]
#         self.reference_number = schedule["name"]
#         self.payment_date = getdate(nowdate())


import frappe
from frappe.model.document import Document
from frappe.utils import nowdate, getdate

class ShopRentPayment(Document):
    def before_submit(self):
        self.validate_payment_amount()
        self.update_payment_schedule()
        self.update_tenant_history()

    def validate_payment_amount(self):
        shop_rent = frappe.db.get_value("Airport Shop", self.shop, "monthly_rent_amount")
        if self.amount != shop_rent:
            frappe.throw(f"Payment amount must match shop's monthly rent ({shop_rent})")

    def update_payment_schedule(self):
        schedule = frappe.get_all(
            "Payment Schedule",
            filters={
                "shop": self.shop,
                "month": self.payment_for_month,
                "year": self.payment_for_year,
                "status": ["in", ["Pending", "Overdue"]]
            },
            fields=["name"]
        )
        
        if not schedule:
            frappe.throw(f"Payment Schedule for shop {self.shop}, month {self.payment_for_month}, year {self.payment_for_year} not found")
        
        schedule_doc = frappe.get_doc("Payment Schedule", schedule[0].name)
        schedule_doc.status = "Paid"
        schedule_doc.payment_reference = self.name
        schedule_doc.save()

    def update_tenant_history(self):
        tenant = frappe.get_doc("Shop Tenant", self.tenant)
        tenant.append("payment_history", {
            "payment": self.name,
            "shop": self.shop,
            "payment_date": nowdate(),
            "month": self.payment_for_month,
            "year": self.payment_for_year,
            "amount": self.amount,
            "payment_method": self.payment_method,
            "reference_number": self.reference_number
        })
        tenant.save()

    def on_shop_selection(self):
        if not self.shop:
            return
        
        shop = frappe.get_doc("Airport Shop", self.shop)
        if shop.status != "Occupied":
            frappe.throw(f"Shop {shop.shop_number} is not occupied. Cannot create rent payment.")
        
        schedules = frappe.get_all(
            "Payment Schedule",
            filters={"shop": self.shop, "status": ["in", ["Pending", "Overdue"]]},
            fields=["name", "month", "year", "amount"]
        )
        
        if not schedules:
            frappe.throw("No pending or overdue payment schedules found for this shop.")
        
        if len(schedules) > 1:
            self.show_schedule_selection_dialog(schedules)
        else:
            self.populate_payment_details(schedules[0])
            self.save()

    def show_schedule_selection_dialog(self, schedules):
        options = [
            {"label": f"{s['month']} {s['year']} - {s['amount']}", "value": s["name"]}
            for s in schedules
        ]
        
        frappe.msgprint(
            title="Select Payment Schedule",
            message="Multiple payment schedules found. Please select one.",
            primary_action={
                "label": "Select Schedule",
                "server_action": "airplane_mode.airport_shop_management.doctype.shop_rent_payment.shop_rent_payment.select_schedule",
                "args": {"schedules": options}
            }
        )

    def populate_payment_details(self, schedule):
        self.payment_for_month = schedule["month"]
        self.payment_for_year = schedule["year"]
        self.amount = schedule["amount"]
        self.reference_number = schedule["name"]

        if hasattr(self, "payment_date"):
            self.payment_date = getdate(nowdate())
        else:
            frappe.throw("Payment Form does not have a payment_date field")
            
        self.save()

@frappe.whitelist()
def select_schedule(schedule_name):
    schedule = frappe.get_doc("Payment Schedule", schedule_name)
    return {
        "payment_for_month": schedule.month,
        "payment_for_year": schedule.year,
        "amount": schedule.amount,
        "reference_number": schedule.name
    }
