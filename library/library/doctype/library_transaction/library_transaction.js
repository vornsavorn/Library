
frappe.ui.form.on('Library Transaction', {
    refresh: function(frm) {
        fetchLoanPeriodDays(frm);
        fetchPenaltyPerDay(frm);
        togglePenaltyFields(frm)
    },

    return_date: function(frm) {
        calculatePenalty(frm);
        togglePenaltyFields(frm)
    }

    
});

// Function to fetch loan period days from Library Setting
function fetchLoanPeriodDays(frm) {
    frappe.db.get_value('Library Setting', {}, 'loan_period_days')
        .then(response => {
            if (response && response.message && response.message.loan_period_days) {
                let loanPeriodDays = response.message.loan_period_days;
                // Call a function to calculate due date based on loan period days
                calculateDueDate(frm, loanPeriodDays);
            } else {
                frappe.msgprint(__('Loan Period Days not found or invalid in Library Settings.'));
            }
        })
        .catch(error => {
            frappe.msgprint(__('Error fetching Loan Period Days.'));
        });
}

// Function to calculate due date based on loan period days
function calculateDueDate(frm, loanPeriodDays) {
    let today = new Date();
    let dueDate = new Date(today.setDate(today.getDate() + loanPeriodDays));
    frm.set_value('due_date', dueDate);
}

// Function to fetch penalty per day from Library Setting
function fetchPenaltyPerDay(frm) {
    frappe.db.get_value('Library Setting', {}, 'penalty_per_day')
        .then(response => {
            if (response && response.message && response.message.penalty_per_day) {
                let penaltyPerDay = response.message.penalty_per_day;
                // Store penalty per day in the form for future calculations
                frm.set_value('penalty_per_day', penaltyPerDay);
            } else {
                frappe.msgprint(__('Penalty Per Day not found or invalid in Library Settings.'));
            }
        })
        .catch(error => {
            frappe.msgprint(__('Error fetching Penalty Per Day.'));
        });
}

// Function to calculate penalty based on return date and due date
function calculatePenalty(frm) {
    let returnDate = frm.doc.return_date;
    let dueDate = frm.doc.due_date;
    let penaltyPerDay = frm.doc.penalty_per_day;

    if (returnDate && dueDate && penaltyPerDay) {
        let returnDateObj = new Date(returnDate);
        let dueDateObj = new Date(dueDate);
        let timeDifference = returnDateObj - dueDateObj; 
        let daysDifference = Math.ceil(timeDifference / (1000 * 3600 * 24)); // convert to days

        if (daysDifference > 0) { 
            let penaltyAmount = daysDifference * penaltyPerDay;
            frm.set_value('penalty_amount', penaltyAmount);
            frappe.msgprint(__('Unfortunately, the return is late by ' + daysDifference + ' days. The penalty amount is : ' + penaltyAmount + '$.'));
        } else {
            frm.set_value('penalty_amount', 0); 
            frappe.msgprint(__('Thank you for returning on time.'));
        }
    } else {
        frappe.msgprint(__('Missing fields for penalty calculation.'));
    }

}

// Function to show or hide penalty-related fields based on return date and due date
function togglePenaltyFields(frm) {
    let returnDate = frm.doc.return_date;
    let dueDate = frm.doc.due_date;
    
    if (returnDate && dueDate) {
        let returnDateObj = new Date(returnDate);
        let dueDateObj = new Date(dueDate);
        let timeDifference = returnDateObj - dueDateObj;
        let isLate = timeDifference > 0; // Check if returned after due date
        
        // Show penalty fields if returned late, hide otherwise
        frm.toggle_display('penalty_amount', isLate);
        frm.toggle_display('penalty_reason', isLate);
        frm.toggle_display('penalty_per_day', isLate);
    } else {
        // Hide penalty fields if either date is missing
        frm.toggle_display('penalty_amount', false);
        frm.toggle_display('penalty_reason', false);
        frm.toggle_display('penalty_per_day', false);
    }
}




