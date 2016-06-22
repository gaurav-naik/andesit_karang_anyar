import frappe
from frappe import _

def load_drivers(doc, key):
	"""Loads address list and contact list in `__onload`"""
	#from erpnext.utilities.doctype.address.address import get_address_display

	#if doc.doctype == "Sales Order" || doc.doctype == "Sales Invoice" :
		# doc.get("__onload").driver_list = [a.update({"display": get_driver_display(a)}) \
		# for a in frappe.get_all("Driver",
		# 	fields="*", filters={{key: doc.name}, {wb_customer: cust}},
		# 	order_by="wb_driver_fn")]
	dl = frappe.get_all("Driver", fields="*", filters={key: doc.wb_customer}, order_by="wb_driver_fn")
	#frappe.msgprint(dl)
	doc.get("__onload").driver_list = dl



# @frappe.whitelist()
# def get_driver_display(driver_dict):
# 	if not driver_dict:
# 		return
		
# 	if not isinstance(driver_dict, dict):
# 		driver_dict = frappe.db.get_value("Driver", driver_dict, "*", as_dict=True) or {}

# 	name, template = get_address_templates(driver_dict)
	
# 	try:
# 		return frappe.render_template(template, driver_dict)
# 	except TemplateSyntaxError:
# 		frappe.throw(_("There is an error in your Driver Template {0}").format(name))


# def get_driver_templates(driver):
# 	result = frappe.db.get_value("Driver Template", \
# 		{"licence": driver.get("wb_driver_licence")}, ["name", "template"])
		
# 	if not result:
# 		result = frappe.db.get_value("Driver Template", \
# 			{"is_default": 1}, ["name", "template"])

# 	if not result:
# 		frappe.throw(_("No default Driver Template found. Please create a new one from Setup > Printing and Branding > Driver Template."))
# 	else:
# 		return result


