import frappe

@frappe.whitelist()
def delete_book(book_name):
    book = frappe.get_doc("Books", book_name)
    book.delete()
    return {"message": f"Book '{book_name}' deleted successfully!"}
