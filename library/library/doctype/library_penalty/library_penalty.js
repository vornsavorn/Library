frappe.ui.form.on('Library Penalty', {
    onload: function(listview) {
        // Refresh every 30 seconds
        setInterval(() => {
            listview.refresh();
        }, 30000);
    },
    refresh: function(frm) {
        frm.add_custom_button(__('Fetch Penalty Data'), function() {
            frappe.prompt([
                {
                    label: 'Library Transaction ID',
                    fieldname: 'transaction_id',
                    fieldtype: 'Link',
                    options: 'Library Transaction',
                    reqd: 1
                }
            ],
            function(data) {
                fetch_transaction_data(data.transaction_id, frm);
            },
            __('Select Library Transaction'), __('Fetch'));
        });
    }
});

function fetch_transaction_data(transaction_id, frm) {
    frappe.db.get_doc('Library Transaction', transaction_id)
        .then(doc => {
            if (doc) {
                frm.set_value('library_member', doc.library_member);  
                frm.set_value('books', doc.books);                  
                frm.set_value('penalty_amount', doc.penalty_amount); 
                frm.set_value('penalty_reason', doc.penalty_reason);
                frm.set_value('return_date', doc.return_date);
            } else {
                frappe.msgprint(__('No transaction found with that ID.'));
            }
        })
        .catch(err => {
            frappe.msgprint(__('Error fetching transaction data: {0}', [err.message]));
        });
}
