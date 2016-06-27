# -*- coding: utf-8 -*-
from __future__ import unicode_literals

app_name = "andesit_karang_anyar"
app_title = "Andesit Karang Anyar"
app_publisher = "MN Technique"
app_description = "ERPNext customization for Andesit Karang Anyar"
app_icon = "icon-truck"
app_color = "#16161D"
app_email = "support@castlecraft.in"
app_version = "0.0.1"
app_license = "GPL v3"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/andesit_karang_anyar/css/andesit_karang_anyar.css"
# app_include_js = "/assets/andesit_karang_anyar/js/andesit_karang_anyar.js"
app_include_js = "/assets/js/aka.min.js"

# include js, css files in header of web template
# web_include_css = "/assets/andesit_karang_anyar/css/andesit_karang_anyar.css"
# web_include_js = "/assets/andesit_karang_anyar/js/andesit_karang_anyar.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "andesit_karang_anyar.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "andesit_karang_anyar.install.before_install"
# after_install = "andesit_karang_anyar.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "andesit_karang_anyar.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"andesit_karang_anyar.tasks.all"
# 	],
# 	"daily": [
# 		"andesit_karang_anyar.tasks.daily"
# 	],
# 	"hourly": [
# 		"andesit_karang_anyar.tasks.hourly"
# 	],
# 	"weekly": [
# 		"andesit_karang_anyar.tasks.weekly"
# 	]
# 	"monthly": [, 
# 		"andesit_karang_anyar.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "andesit_karang_anyar.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "andesit_karang_anyar.event.get_events"
# }

fixtures = ["Custom Script", 
			"Custom Field", 
			"Property Setter",  
			{"dt": "Workflow", "filters": [["document_type", "=", "Weighbridge Ticket"]]},
			{"dt": "Workflow State", "filters": [["name", "in", ["First Weighing", "Second Weighing", "Weighing Complete"]]]},
			{"dt": "Workflow Action", "filters": [["name", "=", "Second Weighing"]]}
			]