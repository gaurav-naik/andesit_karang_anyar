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

	wbt_first_weighing: function(frm){
		if (frm.doc.wbt_first_weighing && frm.doc.wbt_second_weighing){
			frm.set_value("wbt_net_weight", Math.abs(frm.doc.wbt_first_weighing - frm.doc.wbt_second_weighing));
		} 
	},
	
	
	refresh: function(frm) {
		set_second_weighing_visibility(frm);
		if (frm.doc.wbt_time_in === frm.doc.wbt_time_out) {
			frm.set_value("wbt_time_out", frappe.datetime.now_time());	
		}
	},

});

//Hide second weighing fields when doc is local or draft. Shown and enabled on submit.
function set_second_weighing_visibility(frm) {

	var wfs = "Weighing Complete";
	
	var condition_local_docstatus = ((frm.doc.__islocal) || frm.doc.docstatus==0)
	var condition_local_docstatus_wf = ((frm.doc.__islocal) || frm.doc.docstatus==0) || (frm.doc.workflow_state == wfs);

	frm.set_df_property("wbt_second_weighing", "read_only", condition_local_docstatus_wf);
	frm.set_df_property("wbt_second_weigh_uom", "read_only", condition_local_docstatus_wf);
	frm.set_df_property("wbt_second_weigh_uom", "hidden", condition_local_docstatus);
	frm.set_df_property("wbt_time_out", "read_only", condition_local_docstatus_wf);
	frm.set_df_property("wbt_time_out", "hidden", condition_local_docstatus);
	frm.set_df_property("wbt_second_weighing_heading", "hidden", condition_local_docstatus);	
}