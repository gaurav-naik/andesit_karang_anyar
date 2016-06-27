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
	}
	
});
