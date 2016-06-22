// Copyright (c) 2016, MN Technique and contributors
// For license information, please see license.txt
frappe.provide("erpnext.utils");

frappe.ui.form.on('Vehicle', {
	refresh: function(frm) {
		$(frm.fields_dict['drivers'].wrapper)
			.html(frappe.render_template("driver_list", cur_frm.doc.__onload))
			.find(".btn-driver").on("click", function() {
				new_doc("Driver");
			});
	}
});
