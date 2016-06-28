// Copyright (c) 2016, MN Technique and contributors
// For license information, please see license.txt

frappe.ui.form.on('Weighbridge Ticket', {
	party_type: function(frm){
		if (frm.doc.party_type==="Customer"){
			frm.set_value("wbt_load_direction","Outgoing");
		} 
		else if (frm.doc.party_type==="Supplier") {
			frm.set_value("wbt_load_direction","Incoming");
		}
	},

	wbt_second_weighing: function(frm){
		if (frm.doc.wbt_first_weighing && frm.doc.wbt_second_weighing){
			frm.set_value("wbt_net_weight", Math.abs(frm.doc.wbt_first_weighing - frm.doc.wbt_second_weighing));
		} 
	},
	
	refresh: function(frm) {
		set_second_weighing_visibility(frm);
	},

	// wbt_vehicle: function(frm) {
		
	// 	frappe.model.with_doc("Vehicle", frm.doc.wbt_vehicle, function() { 
	// 		var v = frappe.model.get_doc("Vehicle", frm.doc.wbt_vehicle);
	// 		if (v.wb_vehicle_tare_weight != frm.doc.wb_vehicle_tare_weight) {
	// 			frm.set_value("wbt_vehicle_tare_weight", v.wb_vehicle_tare_weight);
	// 		}
	// 	});
	// }
});

cur_frm.add_fetch("wbt_vehicle", "wb_vehicle_tare_weight", "wbt_vehicle_tare_weight");

//Hide second weighing fields when doc is local or draft. Shown and enabled on submit.
function set_second_weighing_visibility(frm) {

	var condition_hidden = (frm.doc.__islocal || frm.doc.docstatus==0)
	var condition_readonly = (frm.doc.workflow_state != "Second Weighing")

	frm.set_df_property("wbt_second_weighing_heading", "hidden", condition_hidden);
	frm.set_df_property("wbt_second_weighing", "read_only", condition_readonly);
	frm.set_df_property("wbt_second_weighing", "hidden", condition_hidden);
	frm.set_df_property("wbt_second_weigh_uom", "read_only", condition_readonly);
	frm.set_df_property("wbt_second_weigh_uom", "hidden", condition_hidden);
	frm.set_df_property("wbt_time_out", "read_only", condition_readonly);
	frm.set_df_property("wbt_time_out", "hidden", condition_hidden);
	
}