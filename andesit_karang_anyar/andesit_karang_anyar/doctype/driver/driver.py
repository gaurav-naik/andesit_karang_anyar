# -*- coding: utf-8 -*-
# Copyright (c) 2015, MN Technique and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document



class Driver(Document):
	def validate(self):
		self.validate_licence_number()
		self.validate_driver_cu_su()

	def validate_licence_number(self):
		if len(self.wb_driver_licence) < 12:
			frappe.throw(_("License Number is not too short. It should be 12 digit format."))

	def validate_driver_cu_su(self):
		if not self.wb_customer and not self.wb_supplier:
			frappe.throw(_("Either Customer or Supplier must be selected."))


	