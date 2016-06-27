# -*- coding: utf-8 -*-
# Copyright (c) 2015, MN Technique and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _

class WeighbridgeTicket(Document):
	def validate(self):
		self.validate_outgoing()
		self.validate_incoming()
		#self.validate_weight()

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
		if self.wbt_load_direction=="Incoming":
			tolerance =  (1.0*float(self.wbt_vehicle_tare_weight)/100)*10
			if not self.wbt_second_weighing <= (tolerance+float(self.wbt_vehicle_tare_weight)):
				frappe.throw(_("Tare Weight MisMatch"))
	
			if not self.wbt_second_weighing >= (float(self.wbt_vehicle_tare_weight)-tolerance):
				frappe.throw(_("Tare Weight MisMatch"))
	