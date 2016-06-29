# -*- coding: utf-8 -*-
# Copyright (c) 2015, MN Technique and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _
from frappe import utils
from frappe.utils import add_days, nowdate

class WeighbridgeTicket(Document):
	def validate(self):
		self.validate_basic()
		self.validate_outgoing()
		self.validate_incoming()
		self.validate_items()
		#self.validate_weight()

	#When Vehicle is Empty and loaded at WeighBridge.  calculate net_weight = Tare Weight - Gross Weight.
	def validate_outgoing(self):
		if self.wbt_load_direction=="Outgoing":
			tolerance = (1.0*float(self.wbt_vehicle_tare_weight)/100)*10
			if not self.wbt_first_weighing <= (tolerance+float(self.wbt_vehicle_tare_weight)):
				frappe.throw(_("Tare Weight mismatch"))

			if not self.wbt_first_weighing >= (float(self.wbt_vehicle_tare_weight)-tolerance):
				frappe.throw(_("Tare Weight mismatch"))

	#Gross Weight and tare weight validation.			
	def validate_weight(self):
		if self.wbt_load_direction=="Outgoing":
			if (self.wbt_first_weighing > self.wbt_second_weighing):
				frappe.throw(_("Second Weigh Weight. i.e Gross Weight can not be less than tare weight."))	

		if self.wbt_load_direction=="Incoming":
			if (self.wbt_first_weighing < self.wbt_second_weighing):
				frappe.throw(_("First Weigh Weight. i.e Gross Weight can not be less than tare weight."))		
	
	#When Vehicle is loaded and unload at WeighBridge. calculate net_weight = Gross Weight — Tare Weight.		
	def validate_incoming(self):
		if self.wbt_load_direction=="Incoming" and self.workflow_state == "Second Weighing" and self.wbt_second_weighing:

			#frappe.msgprint("%s, %s" % (self.wbt_load_direction, self.workflow_state))

			tolerance =  (1.0*float(self.wbt_vehicle_tare_weight)/100)*10
			if not self.wbt_second_weighing <= (tolerance+float(self.wbt_vehicle_tare_weight)):
				frappe.throw(_("Tare Weight mismatch"))
	
			if not self.wbt_second_weighing >= (float(self.wbt_vehicle_tare_weight)-tolerance):
				frappe.throw(_("Tare Weight mismatch"))


	def validate_basic(self):
		if (self.party_type == "Customer") and not self.customer:
			frappe.throw(_("Customer not selected."))
		elif (self.party_type == "Supplier") and not self.supplier:
			frappe.throw(_("Supplier not selected."))

		if (not self.wbt_first_weighing) or (self.wbt_first_weighing == 0.0):
			frappe.throw(_("First weighing cannot be left blank or zero."))


	def validate_items(self):
		
		#WBT must have at least one item.
		if len(self.items) == 0:
			frappe.throw(_("Weighbridge Ticket must have at least one item."))

		#WBT cannot have more than one item.
		item_list = []
		for itm in self.items:
			if itm.item_type == "Item":
				item_list.append(itm.item_type)

		if len(item_list)!= len(set(item_list)):
			frappe.throw(_("Weighbridge Ticket cannot have more than one item."))

	# #When Vehicle is loaded and unload at WeighBridge. calculate net_weight = Gross Weight — Tare Weight.		
	# def validate_incoming(self):
	# 	if self.wbt_load_direction=="Incoming":
	# 		tolerance =  (1.0*float(self.wbt_vehicle_tare_weight)/100)*10
	# 		if not self.wbt_second_weighing <= (tolerance+float(self.wbt_vehicle_tare_weight)):
	# 			frappe.throw(_("Tare Weight MisMatch"))
	
	# 		if not self.wbt_second_weighing >= (float(self.wbt_vehicle_tare_weight)-tolerance):
	# 			frappe.throw(_("Tare Weight MisMatch"))


	#Create Customer order and sales order automatically once Weighing is Complete.
	# def before_update_after_submit(self):
	# 	self.net_weight = abs(self.wbt_first_weighing - self.wbt_second_weighing)

	def on_update_after_submit(self):
		if self.workflow_state == "Weighing Complete":
			#Validate doesnt seem to fire after submitting.
			if ((not self.wbt_second_weighing) or (self.wbt_second_weighing <= 0.0)):
				frappe.throw(_("Second weighing cannot be left blank or zero."))

#SALES DOCS ------


@frappe.whitelist()
def create_sales_docs(docname):

	so = None

	try:
		so = frappe.get_doc("Sales Order", {"weighbridge_ticket": docname})	
	except Exception, e:
		so = create_so(docname)
	else:
		frappe.msgprint(_("Sales Order '%s' already created against this Weighbridge Ticket" % (so.name)))			


	if so:
		try:
			dn = frappe.get_doc("Delivery Note", {"weighbridge_ticket": docname})
		except Exception, e:
			dn = create_dn_for_so(docname, so)
		else:
			frappe.msgprint(_("Delivery Note '%s' already created against this Weighbridge Ticket." % (dn.name)))


@frappe.whitelist()
def create_so(wbtname):
	wbt = None

	try:
		wbt = frappe.get_doc("Weighbridge Ticket", wbtname)
	except Exception, e:
		frappe.throw(_("Weighbridge Ticket '%s' could not be loaded." % (wbtname)))

	#Create a sales order if customer is selected.
	so = frappe.new_doc("Sales Order")	
	so.transaction_date = frappe.utils.today()

	so.company = "Andesit Karang Anyar"
	so.customer = wbt.customer
	so.delivery_date = add_days(so.transaction_date, 10)
	so.currency = "IDR"
	
	so.selling_price_list = "Standard Selling" 
	so.weighbridge_ticket = wbtname

	frappe.msgprint(so.weighbridge_ticket)
	if so.weighbridge_ticket == "": 
		frappe.throw("WBT was not set for SO")


	for itm in wbt.items:
		if itm.item_type == "Item":
			so.append("items", {
				"item_code": itm.item,
				"warehouse": "Stores - AKA",
				"qty": wbt.wbt_net_weight,
				"rate": 550,
				"conversion_factor": 1.0,
			})	
		elif itm.item_type == "Charge":
			so.append("taxes", {
				"doctype": "Sales Taxes and Charges",
				"charge_type": "Actual",
				"account_head": itm.account,
				"description": itm.description,
				"tax_amount": itm.rate,
			})

	try:
		so.submit()
	except Exception, e:
		frappe.throw(_("Sales Order was not submitted. <br/> %s" % (e)))
	else:
		frappe.msgprint(_("Sales Order %s created successfully." % (so.name)))

	return so

@frappe.whitelist()
def create_dn_for_so(wbtname, so):
	#Make a DN from the SO if the DN doesn't already exist.
	from erpnext.selling.doctype.sales_order.sales_order import make_delivery_note
	dn = make_delivery_note(so.name)
	dn.weighbridge_ticket = wbtname

	try:
		dn.save()
	except Exception, e:
		frappe.msgprint(_("Delivery Note was not saved. <br/> %s" % (e)))
	else:
		frappe.db.commit()
		frappe.msgprint(_("Delivery Note %s created successfully." % (dn.name)))

	return dn

#---------------	
	
@frappe.whitelist()
def create_purchase_docs(docname=None):
	po = None

	try:
		po = frappe.get_doc("Purchase Order", {"weighbridge_ticket": docname})	
	except Exception, e:
		po = create_po(docname)
	else:
		frappe.msgprint(_("Purchase Order '%s' already created against this Weighbridge Ticket" % (po.name)))			

	if po:
		try:
			pr = frappe.get_doc("Purchase Receipt", {"weighbridge_ticket": docname})
		except Exception, e:
			pr = create_pr_for_po(docname, po)
		else:
	 		frappe.msgprint(_("Purchase Receipt '%s' already created against this Weighbridge Ticket." % (pr.name)))


@frappe.whitelist()
def create_po(wbtname):
	wbt = None

	try:
		wbt = frappe.get_doc("Weighbridge Ticket", wbtname)
	except Exception, e:
		frappe.throw(_("Weighbridge Ticket '%s' could not be loaded." % (wbtname)))
	
	po = frappe.new_doc("Purchase Order")
	po.transaction_date = frappe.utils.today()

	po.company = "Andesit Karang Anyar"
	po.supplier = wbt.supplier
	po.is_subcontracted = "No"
	po.conversion_factor = 1
	po.weighbridge_ticket = wbtname

	for itm in wbt.items:
		if itm.item_type == "Item":
			po.append("items", {
				"item_code": itm.item,
				"warehouse": "Stores - AKA",
				"qty": wbt.wbt_net_weight,
				"rate": 400,
				"schedule_date": add_days(nowdate(), 1)
			})
		elif itm.item_type == "Charge":
			po.append("taxes", {
				"doctype": "Sales Taxes and Charges",
				"charge_type": "Actual",
				"account_head": itm.account,
				"description": itm.description,
				"tax_amount": itm.rate,
			})

	try:
		po.submit()
	except Exception, e:
		frappe.throw(_("Purchase Order was not submitted. <br/> %s" % (e)))
	else:
		frappe.msgprint(_("Purchase Order %s created successfully." % (po.name)))

	return po
	
@frappe.whitelist()
def create_pr_for_po(wbtname, po):
	pr = None

	from erpnext.buying.doctype.purchase_order.purchase_order import make_purchase_receipt
	pr = make_purchase_receipt(po.name)
	pr.weighbridge_ticket = wbtname

	try:	
		pr.save()
	except Exception, e:
		frappe.throw(_("Purchase Receipt was not created. <br/> %s" % (e)))
	else:
		frappe.msgprint(_("Purchase Receipt %s created successfully." % (pr.name)))
		frappe.db.commit()
