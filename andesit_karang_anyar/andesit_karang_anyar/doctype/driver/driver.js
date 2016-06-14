// Copyright (c) 2016, MN Technique and contributors
// For license information, please see license.txt


// additional validation on license number
frappe.ui.form.on("Driver", "validate", function(frm) {
    if (frm.doc.wb_driver_licence && frm.doc.wb_driver_licence.length != 12) {
        msgprint("Invalid Licence Number. It should be 12 digit format.");
        validated = false;
    }
});