# Copyright (c) 2013, MN Technique and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import msgprint, _
from frappe.utils import flt

def execute(filters=None):
	if not filters: filters = {}
    
	columns = get_columns(filters)
	entries = get_entries(filters)
	data = []
	total_wbt_net_weight = 0.0

	# To find Total of net weight at the end of report.
	for d in entries:
	#	total_wbt_net_weight += (d.wbt_net_weight)

		data.append([
			d.name, d.name, d.customer, d.company, d.transaction_date, d.delivery_date, d.shipping_address_name, d.grand_total, d.territory, d.customer_address,d.contact_person
		])

	# if data:
	# 	total_row = [""]*len(data[0])
	# 	total_row[0] = _("Total")
	# 	total_row[-1] = total_wbt_net_weight
	# 	data.append(total_row)

	return columns, data
#Display Column row from Wieghbridge Ticket Report.
def get_columns(filters):
	if not filters.get("doc_type"):
		msgprint(_("Please select the document type first"), raise_exception=1)

	return [filters["doc_type"] + ":Link/" + filters["doc_type"] + ":140",
		_("Customer") + ":Link/Customer:120",
		_("Customer Name") + ":Data:120",
		_("Company") + ":Link/Company:120",
		_("Date") + ":Date:120",
		_("Delivery Date") + ":Date:120",
		_("Shipping Address") + ":Link/DocType:120",
		_("Grand Total") + ":Float:160",
		_("Territory") + ":Link/Territory:160",
		_("Contact Address") + ":Link/Address:160",
		_("Contact Person") + ":Link/Contact:160"
	]

#Display Data in  Wieghbridge Ticket Report.
def get_entries(filters):
	# doc_field = filters["doc_type"] == 'Customer'
	# conditions, values = get_conditions(filters, doc_field)
	entries = frappe.db.sql("""
		select
			cs.name, cs.name, cs.customer, wt.company, wt.transaction_date, wt.delivery_date,wt.shipping_address_name,wt.grand_total,wt.territory,wt.customer_address,wt.contact_person
		from 
			`tab%s` cs, `tabSales Order` wt 
		""" %(filters["doc_type"]), as_dict=1)

	return entries

# Start Wrok Here-- after break
# def get_conditions(filters, doc_field):
# 	conditions = [""]
#  	values = []

#  	for field in ["Supplier", "Customer"]:
# 		if filters.get(field):
#  			conditions.append("wt.{0}=%s".format(field))
#  			values.append(filters[field])
#  	return " and ".join(conditions), values
