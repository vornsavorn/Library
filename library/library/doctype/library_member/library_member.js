// Copyright (c) 2024, savorn and contributors
// For license information, please see license.txt
frappe.ui.form.on("Library Member", {
    first_name: function(frm) {
        full_name(frm);
    },
    last_name: function(frm) {
        full_name(frm);
    },
});

function full_name(frm) {
    let firstName = frm.doc.first_name || '';
    let lastName = frm.doc.last_name || '';
    frm.set_value('full_name', `${firstName} ${lastName}`.trim());
}

