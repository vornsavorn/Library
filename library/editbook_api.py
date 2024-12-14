import frappe

@frappe.whitelist()
def edit_book(name, book_cover, book_name, type_of_book, publisher, author, isbn):
    book = frappe.get_doc("Books", name)
    book.book_cover = book_cover
    book.book_name = book_name  # fixed typo here
    book.type_of_book = type_of_book
    book.publisher = publisher
    book.author = author  # author is a Link field
    book.isbn = isbn
    book.save()
    return {"message": "Book details updated successfully!"}
