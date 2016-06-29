// Copyright (c) 2016, MN Technique and contributors
// For license information, please see license.txt
frappe.provide("erpnext.utils");

frappe.ui.form.on('Vehicle', {
	refresh: function(frm) {
		if (!cur_frm.doc.__islocal) {
			$(frm.fields_dict['drivers'].wrapper)
				.html(frappe.render_template("driver_list", cur_frm.doc.__onload))
				.find(".btn-driver").on("click", function() {
					new_doc("Driver");
				});
		}
	}
});

frappe.ui.form.on("Vehicle Driver", "vehicle_driver", function(frm, cdt, cdn) {
	var vd = locals[cdt][cdn];
	vd.driver_name = vd.driver.wb_driver_fn + (vd.driver.wb_driver_ln ? " " + vd.driver.wb_driver_ln : "");
	vd.driver_licence_no = vd.driver.wb_driver_licence;
	frm.refresh_fields();
});
