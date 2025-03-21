import frappe

def trigger_update_gate_number(flight_name, new_gate_number):
    frappe.enqueue(update_gate_number_in_tickets, flight_name=flight_name, new_gate_number=new_gate_number)

def update_gate_number_in_tickets(flight_name, new_gate_number):
    tickets = frappe.get_all("Airplane Ticket", filters={"flight": flight_name}, fields=["name"])
    for ticket in tickets:
        frappe.db.set_value("Airplane Ticket", ticket.name, "gate_number", new_gate_number)
