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
		#self.validate_weight()

		#frappe.msgprint("%s, %s" % (self.wbt_load_direction, self.workflow_state))

	#When Vehicle is Empty and loaded at WeighBridge.  calculate net_weight = Tare Weight - Gross Weight.
	def validate_outgoing(self):
		if self.wbt_load_direction=="Outgoing":
			tolerance = (1.0*float(self.wbt_vehicle_tare_weight)/100)*10
			if not self.wbt_first_weighing <= (tolerance+float(self.wbt_vehicle_tare_weight)):
				frappe.throw(_("Tare Weight MisMatch"))

			if not self.wbt_first_weighing >= (float(self.wbt_vehicle_tare_weight)-tolerance):
				frappe.throw(_("Tare Weight MisMatch"))

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
				frappe.throw(_("Tare Weight MisMatch"))
	
			if not self.wbt_second_weighing >= (float(self.wbt_vehicle_tare_weight)-tolerance):
				frappe.throw(_("Tare Weight MisMatch"))


	def validate_basic(self):
		if (self.party_type == "Customer") and not self.customer:
			frappe.throw(_("Customer not selected."))
		elif (self.party_type == "Supplier") and not self.supplier:
			frappe.throw(_("Supplier not selected."))

		if (not self.wbt_first_weighing) or (self.wbt_first_weighing == 0.0):
			frappe.throw(_("First weighing cannot be left blank or zero."))

	






	# #When Vehicle is loaded and unload at WeighBridge. calculate net_weight = Gross Weight — Tare Weight.		
	# def validate_incoming(self):
	# 	if self.wbt_load_direction=="Incoming":
	# 		tolerance =  (1.0*float(self.wbt_vehicle_tare_weight)/100)*10
	# 		if not self.wbt_second_weighing <= (tolerance+float(self.wbt_vehicle_tare_weight)):
	# 			frappe.throw(_("Tare Weight MisMatch"))
	
	# 		if not self.wbt_second_weighing >= (float(self.wbt_vehicle_tare_weight)-tolerance):
	# 			frappe.throw(_("Tare Weight MisMatch"))
	
	#Create Customer order and sales order automatically once Weighing is Complete.
	def on_update_after_submit(self):
		
		if self.workflow_state == "Weighing Complete":
			#Validate doesnt seem to fire after submitting.
			if ((not self.wbt_second_weighing) or (self.wbt_second_weighing == 0.0)):
				frappe.throw(_("Second weighing cannot be left blank or zero."))


			#Create a sales order if customer is selected.
			if self.party_type == "Customer" and self.customer :
				so = frappe.new_doc("Sales Order")
				
				so.transaction_date = frappe.utils.today()

				so.company = "Andesit Karang Anyar"
				so.customer = self.customer
				so.delivery_date = add_days(so.transaction_date, 10)
				so.currency = "IDR"
				
				so.selling_price_list = "Standard Selling" 

				so.append("items", {
					"item_code": "Rock Aggregate",
					"warehouse": "Stores - AKA",
					"qty": self.wbt_second_weighing,
					"rate": 550,
					"conversion_factor": 1.0,
				})

				so.insert()

				frappe.msgprint("Sales Order %s created successfully." % (so.name))

				return so

			elif self.party_type == "Supplier" and self.supplier:
				po = frappe.new_doc("Purchase Order")

				po.transaction_date = frappe.utils.today()

				po.company = "Andesit Karang Anyar"
				po.supplier = self.supplier
				po.is_subcontracted = "No"
				#po.currency = args.currency or frappe.db.get_value("Company", po.company, "default_currency")
				po.conversion_factor = 1

				po.append("items", {
					"item_code": "Rock Aggregate",
					"warehouse": "Stores - AKA",
					"qty": self.wbt_second_weighing,
					"rate": 550,
					"schedule_date": add_days(nowdate(), 1)
				})
				
				po.insert()

				frappe.msgprint("Purchase Order %s created successfully." % (po.name))

				return po
