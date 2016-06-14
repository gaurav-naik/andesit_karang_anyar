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

	def validate_licence_number(self):
		if len(self.wb_driver_licence) != 12:
			frappe.throw(_("Licnece Number is not Valid.It should be 12 digit format."))




	