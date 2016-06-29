// Copyright (c) 2016, MN Technique and contributors
// For license information, please see license.txt

var weighing_complete = "Weighing Complete";

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
		cur_frm.add_fetch("wbt_vehicle", "wb_vehicle_tare_weight", "wbt_vehicle_tare_weight");
		if (frm.doc.workflow_state == "Weighing Complete") {
			if (frm.doc.party_type == "Customer") {
				make_btn_sales_docs(frm);
			} else if (frm.doc.party_type == "Supplier") {
				make_btn_purchase_docs(frm);
			}
		}
	},

});

function make_btn_purchase_docs(frm) {
	frm.add_custom_button(__('Create Purchase Docs'), function(){
		frappe.call({
			method: "andesit_karang_anyar.andesit_karang_anyar.doctype.weighbridge_ticket.weighbridge_ticket.create_purchase_docs",
			args: {"docname": frm.doc.name},
			freeze: true,
			freeze_message: __("Creating Purchase Docs"),
			callback: function(r){
				if(!r.exc) {
					frappe.msgprint(__("Purchase Docs created."));
				} else {
					frappe.msgprint(__("Purchase Docs could not be created. <br /> " + r.exc));
				}
			}
		});
	});
}

function make_btn_sales_docs(frm) {
	frm.add_custom_button(__('Create Sales Docs'), function(){
		frappe.call({
			method: "andesit_karang_anyar.andesit_karang_anyar.doctype.weighbridge_ticket.weighbridge_ticket.create_sales_docs",
			args: {"docname": frm.doc.name},
			freeze: true,
			freeze_message: __("Creating Sales Docs"),
			callback: function(r){
				if(!r.exc) {
					frappe.msgprint(__("Sales Docs created."));
				} else {
					frappe.msgprint(__("Sales Docs could not be created. <br /> " + r.exc));
				}
			}
		});
	});
}


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