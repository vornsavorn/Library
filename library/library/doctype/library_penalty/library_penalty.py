# Copyright (c) 2024, savorn and contributors
# For license information, please see license.txt


import frappe
from frappe.utils import getdate
from frappe.model.document import Document


class LibraryPenalty(Document):
	pass


# bench --site project.local execute library.penalty.create_penalties_for_late_returns

def check_and_create_penalty(doc, method):
    """Check and create a penalty for a specific transaction on update."""
    due_date = doc.due_date
    return_date = doc.return_date
    penalty_amount = doc.penalty_amount
    penalty_reason = doc.penalty_reason

    # If the return date is later than due date and penalty amount exists
    if return_date and getdate(return_date) > getdate(due_date) and penalty_amount:
        transaction = {
            "library_member": doc.library_member,
            "books": doc.books,
            "due_date": due_date,
            "return_date": return_date,
            "penalty_amount": penalty_amount,
            "penalty_reason": penalty_reason,
        }

        if not penalty_exists(transaction):
            create_penalty_record(transaction, penalty_amount, penalty_reason)
        else:
            frappe.msgprint(f"Penalty already exists for {transaction['library_member']} for late return.")

def penalty_exists(transaction):
    existing_penalties = frappe.get_all(
        "Library Penalty",
        filters={
            "library_member": transaction['library_member'],
            "books": transaction['books'],
            "due_date": transaction['due_date'],
            "return_date": transaction['return_date']
        },
        fields=["name"]
    )
    return len(existing_penalties) > 0

def create_penalty_record(transaction, penalty_amount, penalty_reason):
    penalty_doc = frappe.get_doc({
        "doctype": "Library Penalty",
        "library_member": transaction['library_member'],
        "books": transaction['books'],
        "penalty_amount": penalty_amount,
        "penalty_reason": penalty_reason,
        "due_date": transaction['due_date'],
        "return_date": transaction['return_date'],
    })
    penalty_doc.insert(ignore_permissions=True)
    frappe.msgprint(f"Penalty record created for {transaction['library_member']} for late return.")
