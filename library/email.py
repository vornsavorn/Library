import frappe
from frappe import _
from frappe.utils import today, getdate, add_days

def library_email():
    current_date = today()
    print("Current Date:", current_date)

    # Fetch all library transactions with return dates and library members
    library_transactions = frappe.get_all(
        "Library Transaction",
        fields=["due_date", "library_member"]
    )

    for library_transaction in library_transactions:
        due_date = library_transaction['due_date']
        library_member_id = library_transaction['library_member']
        
        # Fetch the library member document
        member = frappe.get_doc("Library Member", library_member_id)
        member_email = member.email_address if member else None
        
        # Print the current date and return date
        print(f"Due Date: {due_date}")

        # Print the member email
        print(f"Member Email: {member_email}")
        
        # Check if the return date is tomorrow
        if due_date == add_days(getdate(current_date), 1):
            print(f"Sending reminder to {member_email} for return date {due_date}")
            send_email_reminder(member_email, due_date, member.full_name)

def send_email_reminder(email_address, due_date, full_name):
    # Construct the email content
    subject = "Reminder: Book Return Due Tomorrow"
    message = f"""
    Dear {full_name},

    I hope this message finds you well. 

    This is a friendly reminder that your book is due for return tomorrow ({due_date}).

    We kindly ask you to ensure it is returned on time to avoid any penalties.

    Thank you for your cooperation!

    """


    # Send the email using frappe.sendmail
    frappe.sendmail(
        recipients=[email_address],
        subject=subject,
        message=message,
        sender= "savorn.vorn@student.passerellesnumeriques.org"
    )



# bench --site project.local execute library.email.library_email