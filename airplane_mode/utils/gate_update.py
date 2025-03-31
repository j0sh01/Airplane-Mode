# import frappe

# def trigger_update_gate_number(flight_name, new_gate_number):
#     frappe.enqueue(update_gate_number_in_tickets, flight_name=flight_name, new_gate_number=new_gate_number)

# def update_gate_number_in_tickets(flight_name, new_gate_number):
#     tickets = frappe.get_all("Airplane Ticket", filters={"flight": flight_name}, fields=["name"])
#     for ticket in tickets:
#         frappe.db.set_value("Airplane Ticket", ticket.name, "gate_number", new_gate_number)


import frappe

def trigger_update_gate_number(flight_name, new_gate_number):
    """Queue gate number updates to run in the background"""
    # Use queue with a specific job ID to prevent duplicate jobs
    frappe.enqueue(
        update_gate_number_in_tickets, 
        queue='default',
        job_name=f'update_gate_{flight_name}',
        flight_name=flight_name, 
        new_gate_number=new_gate_number
    )

def update_gate_number_in_tickets(flight_name, new_gate_number):
    """Update gate numbers in all tickets for a specific flight"""
    # Get all tickets with this flight
    tickets = frappe.get_all(
        "Airplane Ticket", 
        filters={"flight": flight_name}, 
        fields=["name"]
    )
    
    # Update each ticket with db.set_value (more efficient than doc.save())
    for ticket in tickets:
        frappe.db.set_value("Airplane Ticket", ticket.name, "gate_number", new_gate_number)
    
    # Commit the transaction
    frappe.db.commit()
    
    # Notify users through the Frappe messaging system (optional)
    frappe.msgprint(f"Updated gate number to {new_gate_number} for {len(tickets)} tickets on flight {flight_name}")