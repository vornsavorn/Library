import frappe
from frappe.model.document import Document
from frappe import _

class LibraryTransaction(Document):
    def validate(self):
        # Validate quantity against library settings
        self.validate_quantity()
        
        # Calculate and set the amount based on quantity and amount per book
        self.calculate_amount()

    def validate_quantity(self):
        library_setting_name = frappe.get_all("Library Setting", fields=["name"], limit=1)
        if library_setting_name:
            library_setting = frappe.get_doc("Library Setting", library_setting_name[0].name)
            max_quantity = library_setting.quantitymaximun_number_of_books
            
            if self.quantity > max_quantity:
                frappe.throw(_("Quantity cannot exceed the maximum allowed limit of {0} books.").format(max_quantity))
        else:
            frappe.throw(_("Library Setting not found. Please ensure it is created."))

    def calculate_amount(self):
        library_setting_name = frappe.get_all("Library Setting", fields=["name"], limit=1)
        if library_setting_name:
            library_setting = frappe.get_doc("Library Setting", library_setting_name[0].name)
            amount_per_book = library_setting.amountbook
            
            self.amount = self.quantity * amount_per_book 
        else:
            frappe.throw(_("Library Setting not found. Please ensure it is created."))


    # # Get all library members' email addresses
    # members = frappe.get_all("Library Member", fields=["email_address", "last_name", "name"])
    # for member in members:
    #     if member.email_address:
    #         transaction = frappe.db.get_value(
    #             "Library Transaction", 
    #             {"library_member": member.name}, 
    #             ["name", "books", "quantity", "amount", "transaction_date", "due_date", "return_date"], 
    #             as_dict=True
    #         )
            
    #         if transaction:
    #             subject = _("Library Transaction Notice: {0}").format(transaction['name'])
    #             message = _(
    #                 """
    #                 <p>Dear {0},</p>
    #                 <p>This is a notification regarding your library transaction for the following book(s):</p>
    #                 <ul>
    #                     <li><b>Transaction ID:</b> {1}</li>
    #                     <li><b>Book(s):</b> {2}</li>
    #                     <li><b>Quantity:</b> {3}</li>
    #                     <li><b>Amount:</b> {4}</li>
    #                     <li><b>Transaction Date:</b> {5}</li>
    #                     <li><b>Due Date:</b> {6}</li>
    #                     <li><b>Return Date:</b> {7}</li>
    #                 </ul>
    #                 <p>Please return the book(s) at your earliest convenience.</p>
    #                 <p>Thank you!</p>
    #                 """
    #             ).format(
    #                 member.last_name,
    #                 transaction['name'],
    #                 transaction['books'],
    #                 transaction['quantity'],
    #                 transaction['amount'],
    #                 transaction['transaction_date'],
    #                 transaction['due_date'],
    #                 transaction['return_date']
    #             )

    #             # Send the email
    #             frappe.sendmail(
    #                 recipients=[member.email_address],
    #                 sender="savorn.vorn@student.passerellesnumeriques.org", 
    #                 subject=subject,
    #                 message=message,
    #                 reference_doctype="Library Transaction",  
    #             )
    #             print("Email sent to:", member.email_address)
    #         else:
    #             print("No transaction found for member:", member.name)
