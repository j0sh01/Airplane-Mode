# Copyright (c) 2025, Joshua Michael and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import random
import string

class AirplaneTicket(Document):
    def validate(self):
        self.remove_duplicate_add_ons()
        self.calculate_total_amount()

    def before_insert(self):
        self.set_random_seat()

    def on_submit(self):
        self.set_status_completed()

    def calculate_total_amount(self):
        total_add_ons = sum([item.amount for item in self.add_ons])
        self.total_amount = self.flight_price + total_add_ons

    def remove_duplicate_add_ons(self):
        unique_add_ons = []
        seen_add_on_items = set()
        duplicates_removed = []
        for item in self.add_ons:
            if item.item not in seen_add_on_items:
                unique_add_ons.append(item)
                seen_add_on_items.add(item.item)
            else:
                duplicates_removed.append(item.item)
        self.add_ons = unique_add_ons
        if duplicates_removed:
            frappe.msgprint(f"Duplicate add-ons have been removed: {', '.join(duplicates_removed)}.")

    def set_random_seat(self):
        random_integer = random.randint(1, 99)
        random_letter = random.choice(string.ascii_uppercase[:5])  # A to E
        self.seat = f"{random_integer}{random_letter}"

    def set_status_completed(self):
        frappe.db.set_value("Airplane Flight", self.flight, "status", "Completed")

    def before_submit(self):
        if self.status != "Boarded":
            frappe.throw("The Airplane Ticket cannot be submitted unless the status is 'Boarded'.")
