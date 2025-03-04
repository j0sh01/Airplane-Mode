# Copyright (c) 2025, Joshua Michael and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class FlightPassenger(Document):
    def validate(self):
        self.autoname()
        
    def autoname(self):
        if self.first_name and self.last_name:
            self.full_name = self.first_name + " " + self.last_name
        elif self.first_name:
            self.full_name = self.first_name
        else:
            self.full_name = self.last_name
    