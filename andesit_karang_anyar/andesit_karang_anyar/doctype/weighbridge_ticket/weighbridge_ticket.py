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

	#When Vehicle is Empty and loaded at WeighBridge.  calculate net_weight = Tare Weight - Gross Weight.
	def validate_outgoing(self):
		if self.wbt_load_direction=="Outgoing":
			tolerance = (1.0*self.wbt_vehicle_tare_weight/100)*10
			if self.wbt_first_weighing <= (tolerance+self.wbt_vehicle_tare_weight) and self.wbt_first_weighing >= (self.wbt_vehicle_tare_weight-tolerance):
				net_weight = self.wbt_first_weighing - self.wbt_second_weighing
			else:
				frappe.throw(_("Tare Weight MisMatch"))
	

	#When Vehicle is loaded and unload at WeighBridge. calculate net_weight = Gross Weight — Tare Weight.		
	def validate_incoming(self):
		if self.wbt_load_direction=="Incoming":
			tolerance =  (1.0*self.wbt_vehicle_tare_weight/100)*10
			if self.wbt_second_weighing <= (tolerance+self.wbt_vehicle_tare_weight) and self.wbt_second_weighing >= (self.wbt_vehicle_tare_weight-tolerance):
				net_weight = self.wbt_first_weighing - self.wbt_second_weighing
			else:
				frappe.throw(_("Tare Weight MisMatch"))
			
