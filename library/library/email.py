# import frappe
# from frappe import _

# def send_email():
#     # Get all library members' email addresses
#     members = frappe.get_all("Library Member", fields=["email_address", "last_name", "name"])
#     print(members)

#     for member in members:
#         if member.email_address:
#             transaction = frappe.db.get_value(
#                 "Library Transaction", 
#                 {"library_member": member.name}, 
#                 ["name", "books", "quantity", "amount", "transaction_date", "due_date", "return_date"], 
#                 as_dict=True
#             )
            
#             if transaction:
#                 subject = _("Library Transaction Notice: {0}").format(transaction['name'])
#                 message = _(
#                     """
#                     <p>Dear {0},</p>
#                     <p>This is a notification regarding your library transaction for the following book(s):</p>
#                     <ul>
#                         <li><b>Transaction ID:</b> {1}</li>
#                         <li><b>Book(s):</b> {2}</li>
#                         <li><b>Quantity:</b> {3}</li>
#                         <li><b>Amount:</b> {4}</li>
#                         <li><b>Transaction Date:</b> {5}</li>
#                         <li><b>Due Date:</b> {6}</li>
#                         <li><b>Return Date:</b> {7}</li>
#                     </ul>
#                     <p>Please return the book(s) at your earliest convenience.</p>
#                     <p>Thank you!</p>
#                     """
#                 ).format(
#                     member.last_name,
#                     transaction['name'],
#                     transaction['books'],
#                     transaction['quantity'],
#                     transaction['amount'],
#                     transaction['transaction_date'],
#                     transaction['due_date'],
#                     transaction['return_date']
#                 )

#                 # Send the email
#                 frappe.sendmail(
#                     recipients=[member.email_address],
#                     sender="savorn.vorn@student.passerellesnumeriques.org", 
#                     subject=subject,
#                     message=message,
#                     reference_doctype="Library Transaction",  
#                 )
#                 print("Email sent to:", member.email_address)
#             else:
#                 print("No transaction found for member:", member.name)
