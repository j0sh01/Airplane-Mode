# # Copyright (c) 2025, Joshua Michael and contributors
# # For license information, please see license.txt

# import frappe
# from frappe.website.website_generator import WebsiteGenerator


# class AirplaneFlight(WebsiteGenerator):        
#         def before_submit(self):
#             self.status = " Completed"

#         def on_update(self):
#             if self.has_value_changed("gate_number"):
#                 from airplane_mode.utils.gate_update import trigger_update_gate_number
#                 trigger_update_gate_number(self.name, self.gate_number)


# Copyright (c) 2025, Joshua Michael and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator

class AirplaneFlight(WebsiteGenerator):        
    def before_submit(self):
        self.status = "Completed"

    def on_update(self):
        # Check if gate_number has changed and is not empty
        if self.has_value_changed("gate_number") and self.gate_number:
            # Import here to avoid circular imports
            from airplane_mode.utils.gate_update import trigger_update_gate_number
            
            # Trigger the update process
            trigger_update_gate_number(self.name, self.gate_number)