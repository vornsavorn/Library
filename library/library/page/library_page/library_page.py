import frappe
from urllib.parse import urljoin

@frappe.whitelist(allow_guest=True)
def get_books_from_library():
    books = frappe.get_all("Books", fields=["name", "book_name", "author", "book_cover", "publisher", "isbn"])

    base_url = frappe.utils.get_url()
    for book in books:
        book["link_url"] = urljoin(base_url, f"app/books/{book['name']}")

    return {
        "books": books,
    }


