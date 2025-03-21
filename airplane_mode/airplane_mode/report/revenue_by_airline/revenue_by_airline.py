# Copyright (c) 2025, Joshua Michael and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
	columns = get_columns()
	data = get_data()
	chart = get_chart_data(data)
	summary = get_summary(data)
	return columns, data, None, chart, summary

def get_columns():
	return [
		{
			"label": "Airline",
			"fieldname": "airline",
			"fieldtype": "Link",
			"options": "Airline",
			"width": 150
		},
		{
			"label": "Revenue",
			"fieldname": "revenue",
			"fieldtype": "Currency",
			"width": 150
		}
	]

def get_data():
	airlines = frappe.get_all("Airline", fields=["name"])
	data = []
	for airline in airlines:
		revenue = frappe.db.sql("""
			SELECT SUM(at.flight_price)
			FROM `tabAirplane Ticket` at
			JOIN `tabAirplane Flight` af ON at.flight = af.name
			JOIN `tabAirplane` a ON af.airplane = a.name
			WHERE a.airline = %s
		""", airline.name)[0][0] or 0
		data.append({
			"airline": airline.name,
			"revenue": revenue
		})
	return data

def get_chart_data(data):
	labels = [d["airline"] for d in data]
	values = [d["revenue"] for d in data]
	return {
		"data": {
			"labels": labels,
			"datasets": [{"name": "Revenue", "values": values}]
		},
		"type": "donut"
	}

def get_summary(data):
	total_revenue = sum(d["revenue"] for d in data)
	return [{"label": "Total Revenue", "value": total_revenue, "datatype": "Currency"}]
