
import frappe
@frappe.whitelist()
def get_data_book(name):
    data = frappe.db.get_all(
        'Books',
        fields=['*']
    )

    html = frappe.render_template(
        "library/templates/book.html",
        {
            "books": data,  
        }
    )
    
    return html 