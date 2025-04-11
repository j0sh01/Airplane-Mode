# Copyright (c) 2025, Joshua Michael and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator

class AirplaneFlight(WebsiteGenerator):        
    def before_submit(self):
        self.status = "Completed"

    # def on_update(self):
    #     # Check if gate_number has changed and is not empty
    #     if self.has_value_changed("gate_number") and self.gate_number:
    #         # Import here to avoid circular imports
    #         from airplane_mode.utils.gate_update import trigger_update_gate_number
            
    #         # Trigger the update process
    #         trigger_update_gate_number(self.name, self.gate_number)

@frappe.whitelist()
def update_gate_and_tickets(flight_name, new_gate_number):
    # Update the flight's gate number
    flight = frappe.get_doc("Airplane Flight", flight_name)
    flight.gate_number = new_gate_number
    flight.save(ignore_permissions=True)

    # Enqueue background job
    frappe.enqueue(
        "airplane_mode.airplane_mode.doctype.airplane_flight.airplane_flight.sync_gate_number_to_tickets",
        flight_name=flight_name,
        gate_number=new_gate_number
    )


def sync_gate_number_to_tickets(flight_name, gate_number):
    from frappe.utils import now_datetime, add_days

    now_dt = now_datetime()
    cutoff_date = add_days(now_dt, -1)

    tickets = frappe.get_all(
        "Airplane Ticket",
        filters={
            "flight": flight_name,
            "departure_date": [">=", cutoff_date]
        },
        fields=["name"]
    )

    total = len(tickets)

    for i, ticket in enumerate(tickets):
        frappe.publish_progress(int((i + 1) / total * 100), title="Updating Gate Numbers")

        ticket_doc = frappe.get_doc("Airplane Ticket", ticket.name)
        ticket_doc.gate_number = gate_number
        ticket_doc.flags.ignore_validate = True
        ticket_doc.flags.ignore_on_update = True
        ticket_doc.save(ignore_permissions=True)

    frappe.db.commit()

