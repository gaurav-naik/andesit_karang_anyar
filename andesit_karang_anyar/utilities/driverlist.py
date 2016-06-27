import frappe
from frappe import _

def load_drivers(doc):
	"""Loads Drivers list in `__onload`"""
	dl = frappe.get_all("Driver", fields="*", order_by="wb_driver_fn")
	doc.get("__onload").driver_list = dl
