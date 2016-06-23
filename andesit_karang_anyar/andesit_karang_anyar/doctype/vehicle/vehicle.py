# -*- coding: utf-8 -*-
# Copyright (c) 2015, MN Technique and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _
from andesit_karang_anyar.utilities.driverlist import load_drivers

class Vehicle(Document):
	def validate(self):
		self.validate_customer_supplier()

	def validate_customer_supplier(self):
		if not self.wb_customer and not self.wb_supplier:
			frappe.throw(_("Either Customer or Supplier is mandatory"))

	def onload(self):
		load_drivers(self, "wb_customer")
		