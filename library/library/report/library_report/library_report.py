
import frappe
from urllib.parse import urljoin

def execute(filters=None):
    columns = get_columns()
    data = send_data(filters)
    chart_data = get_chart_data(data)

    # frappe.log("Execution Result: Columns: {}, Data: {}, Chart Data: {}".format(columns, data, chart_data))

    chart = {
        "data": chart_data["data"],
        "type": chart_data["type"] 
    }

    return columns, data, None, chart

def get_columns():
    columns = [
        {
            "label": "Library Member",
            "fieldname": "library_member",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": "Book Name",
            "fieldname": "book_name",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": "Type Of Book",
            "fieldname": "type_of_book",
            "fieldtype": "Select",
            "width": 140
        },
        {
            "label": "Author",
            "fieldname": "author",
            "fieldtype": "Link",
            "options": "Author",
            "width": 170
        },
        {
            "label": "Publisher",
            "fieldname": "publisher",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": "Qty",
            "fieldname": "quantity",
            "fieldtype": "Int",
            "width": 80
        },
        {
            "label": "Amount",
            "fieldname": "amount",
            "fieldtype": "Currency",
            "width": 100
        },
        {
            "label": "Status",
            "fieldname": "status",
            "fieldtype": "Select",
            "options": "\nIssued\nReturned",
            "width": 100
        },
        {
            "label": "Penalty Amount",
            "fieldname": "penalty_amount",
            "fieldtype": "Currency",
            "width": 100
        },
        {
            "label": "Penalty Reason",
            "fieldname": "penalty_reason",
            "fieldtype": "Data",
            "width": 130
        },
        {
            "label": "Count",
            "fieldname": "count",
            "fieldtype": "Int",
            "width": 400
        },
        {
            "label": "Others",
            "fieldname": "others",
            "fieldtype": "data",
            "width": 400
        }
    ]
    return columns
# def send_data(filters=None):
    library_member = filters.get('library_member')
    author = filters.get('author')
    book_name = filters.get('book_name')
    status = filters.get('status')
    penalty_reason = filters.get('penalty_reason')
    
    # Base query
    sql_data = """
        SELECT 
            lt.library_member,
            b.book_name,
            b.type_of_book,
            b.author,   
            b.publisher,
            lt.quantity,
            lt.amount,
            lt.status,
            lt.penalty_amount,
            lt.penalty_reason
        FROM 
            `tabLibrary Transaction` lt
        JOIN 
            `tabBooks` b ON lt.books = b.name
        WHERE 
            lt.docstatus <> 2
    """

    # Add filter conditionally
    if library_member:
        if len(library_member) == 1:
            sql_data += f" AND lt.library_member = '{library_member[0]}'"
        else:
            sql_data += f" AND lt.library_member IN {tuple(library_member)}"

    if author:
        if len(author) == 1:
            sql_data += f" AND b.author = '{author[0]}'"
        else:
            sql_data += f" AND b.author IN {tuple(author)}"

    if book_name:
        if len(book_name) == 1:
            sql_data += f" AND b.name = '{book_name[0]}'"
        else:
            sql_data += f" AND b.name IN {tuple(book_name)}"

    if status:
        if len(status) == 1:
            sql_data += f" AND lt.status = '{status[0]}'"
        else:
            sql_data += f" AND lt.status IN {tuple(status)}"

    if penalty_reason:
        if len(penalty_reason) == 1:
            sql_data += f" AND lt.penalty_reason = '{penalty_reason[0]}'"
        else:
            sql_data += f" AND lt.penalty_reason IN {tuple(penalty_reason)}"

    # Order the results
    sql_data += " ORDER BY lt.creation DESC"
  
    # Execute the SQL query
    data = frappe.db.sql(sql_data, as_dict=True, debug=1)

    # Check if data is empty
    if not data:
        frappe.log("No data found!")

    return data

def send_data(filters=None):
    library_member = filters.get('library_member')
    author = filters.get('author')
    book_name = filters.get('book_name')
    status = filters.get('status')
    penalty_reason = filters.get('penalty_reason')

    # Base query
    sql_data = """
        SELECT 
            lt.library_member,
            b.book_name,
            b.type_of_book,
            b.author,   
            b.publisher,
            lt.quantity,
            lt.amount,
            lt.status,
            lt.penalty_amount,
            lt.penalty_reason,
            lt.name as others  -- Include the transaction ID
        FROM 
            `tabLibrary Transaction` lt
        JOIN 
            `tabBooks` b ON lt.books = b.name
        WHERE 
            lt.docstatus <> 2
    """

    # Add filter conditionally
    if library_member:
        if len(library_member) == 1:
            sql_data += f" AND lt.library_member = '{library_member[0]}'"
        else:
            sql_data += f" AND lt.library_member IN {tuple(library_member)}"

    if author:
        if len(author) == 1:
            sql_data += f" AND b.author = '{author[0]}'"
        else:
            sql_data += f" AND b.author IN {tuple(author)}"

    if book_name:
        if len(book_name) == 1:
            sql_data += f" AND b.name = '{book_name[0]}'"
        else:
            sql_data += f" AND b.name IN {tuple(book_name)}"

    if status:
        if len(status) == 1:
            sql_data += f" AND lt.status = '{status[0]}'"
        else:
            sql_data += f" AND lt.status IN {tuple(status)}"

    if penalty_reason:
        if len(penalty_reason) == 1:
            sql_data += f" AND lt.penalty_reason = '{penalty_reason[0]}'"
        else:
            sql_data += f" AND lt.penalty_reason IN {tuple(penalty_reason)}"

    # Order the results
    sql_data += " ORDER BY lt.library_member, lt.creation DESC"
  
    # Execute the SQL query
    data = frappe.db.sql(sql_data, as_dict=True, debug=1)

    base_url = frappe.utils.get_url()

    for other in data:
        if other['others']:
            link_url = urljoin(base_url, f"app/library-transaction//{other['others']}")
            other['others'] = f'<a href="{link_url}" target="_blank">{other["others"]}' 
        else:
            other['others'] = ""

    formatted_data = []
    current_member = None

    for item in data:
        # If it's a new library member, add the row with only the library member name
        if item['library_member'] != current_member:
            # Add a row for the library member with only the name and count filled
            formatted_data.append({
                "library_member": item['library_member'],
                "book_name": '',
                "type_of_book": '',
                "author": '',
                "publisher": '',
                "quantity": None,
                "amount": None,
                "status": '',
                "penalty_amount": None,
                "penalty_reason": '',
                "count": sum(d['quantity'] for d in data if d['library_member'] == item['library_member']),
                "others": ''
            })
            current_member = item['library_member']

        # Add a row for each book associated with the current library member
        formatted_data.append({
            "library_member": '', 
            "book_name": f"    {item['book_name']}", 
            "type_of_book": item['type_of_book'],
            "author": item['author'],
            "publisher": item['publisher'],
            "quantity": item['quantity'],
            "amount": item['amount'],
            "status": item['status'],
            "penalty_amount": item['penalty_amount'],
            "penalty_reason": item['penalty_reason'],
            # "count": ''  
            "others": item['others']
        })

    return formatted_data

def get_chart_data(data):
    if not data:
        frappe.log("No data found for chart aggregation")
        return {
            "data": {"labels": [], "datasets": []},
            "type": "bar"
        }

    book_quantity = {}
    for item in data:
        book_name = item['book_name']
        quantity = item['quantity'] or 0
        if book_name in book_quantity:
            book_quantity[book_name] += quantity
        else:
            book_quantity[book_name] = quantity

    # Prepare chart data for the bar chart
    chart_data = {
        "data": {
            "labels": list(book_quantity.keys()), 
            "datasets": [{
                "name": "Book Quantity",
                "values": list(book_quantity.values()) 
            }]
        },
        "type": "bar" , # Chart type: 'bar', 'line', 'pie', etc.
    }
    
    return chart_data

