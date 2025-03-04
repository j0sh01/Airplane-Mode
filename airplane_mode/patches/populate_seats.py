import frappe
import random
import string

def execute():
    tickets = frappe.get_all("Airplane Ticket", filters={"seat": ("in", ["", None])}, fields=["name"])

    for ticket in tickets:
        random_seat = generate_random_seat() 
        frappe.db.set_value("Airplane Ticket", ticket.name, "seat", random_seat)

    frappe.db.commit()

def generate_random_seat():
    random_integer = random.randint(1, 99)
    random_letter = random.choice(string.ascii_uppercase[:5])  
    return f"{random_integer}{random_letter}"