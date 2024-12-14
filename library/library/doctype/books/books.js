frappe.ui.form.on("Books", {
    refresh(frm) {
        frm.add_custom_button('Create Author', () => {
            frappe.new_doc('Author', {
                books: frm.doc.name  
            });
        }).css({
            'background-color': '#008CBA', 
            'color': 'white'
        });

        fetchBookData(frm); 
    },
});

// });
function fetchBookData(frm) {
    frappe.call({
        method: "library.book_api.get_data_book",
        args: {
            name: frm.doc.name  
        },
        callback: function(response) {
            if (response.message) {
                frm.fields_dict['custom_book_show'].$wrapper.html(response.message);
                editEvent(frm);
                deleteEvent(frm);
            } else {
                console.error("No data returned");
            }
        }
    });
}

// Event handler for the edit button
function editEvent(frm) {
    $(".btn-edit").on("click", function() {
        let bookName = $(this).data("name");
        showDialog(bookName);
    });
}


function showDialog(bookName) {
    let d = new frappe.ui.Dialog({
        title: 'Enter details for ' + bookName,
        fields: [
            {
                label: 'Book Cover',
                fieldname: 'book_cover',
                fieldtype: 'Attach Image'
            },
            {
                label: 'Book Name',
                fieldname: 'book_name', 
                fieldtype: 'Data'
            },
            {
                label: 'Type of book',
                fieldname: 'type_of_book',
                fieldtype: 'Select',
                options: ['Fiction', 'Non-fiction', 'Science', 'History']  
            },
            {
                label: 'Author',
                fieldname: 'author',
                fieldtype: 'Link',
                options: 'Author'  
            },
            {
                label: 'Publisher',
                fieldname: 'publisher',
                fieldtype: 'Data'
            },
            {
                label: 'ISBN',
                fieldname: 'isbn',
                fieldtype: 'Data'
            }
        ],
        primary_action_label: 'Save',
        primary_action(values) {
            frappe.call({
                method: "library.editbook_api.edit_book",
                args: {
                    name: bookName,
                    book_cover: values.book_cover,
                    book_name: values.book_name,  
                    type_of_book: values.type_of_book,
                    publisher: values.publisher,
                    author: values.author,
                    isbn: values.isbn
                },
                callback: function(response) {
                    if (response.message) {
                        frappe.show_alert({ message: response.message, indicator: 'green' });
                        d.hide(); 
                        fetchBookData(frm); 
                    } else {
                        console.error("Error updating book details");
                    }
                }
            });
        }
    });
    frappe.call({
        method: 'frappe.client.get',
        args: {
            doctype: 'Books',
            name: bookName
        },
        callback: function(r) {
            if (r.message) {
                d.set_values({
                    book_cover: r.message.book_cover,
                    book_name: r.message.book_name,
                    type_of_book: r.message.type_of_book,
                    author: r.message.author,
                    publisher: r.message.publisher,
                    isbn: r.message.isbn
                });
            }
        }
    });

    d.show();  
}

// Event handler for the delete button
function deleteEvent(frm) {
    $(".btn-delete").on("click", function() {
        const bookName = $(this).data("name");

        let d = new frappe.ui.Dialog({
            title: 'Confirm Deletion',
            fields: [
                {
                    label: 'Are you sure you want to delete the book "' + bookName + '"?',
                    fieldname: 'confirmation_message',
                    fieldtype: 'HTML',
                    options: '<p>Are you sure you want to delete the book "<strong>' + bookName + '</strong>"?</p>',
                }
            ],
            primary_action_label: 'Delete',
            primary_action() {
                frappe.call({
                    method: "library.deletebook_api.delete_book",
                    args: {
                        book_name: bookName
                    },
                    callback: function(response) {
                        if (response.message) {
                            frappe.show_alert({ message: response.message, indicator: 'green' });
                            d.hide();  
                            fetchBookData(frm); 
                        } else {
                            console.error("Error deleting book");
                        }
                    }
                });
            }
        });

        d.show();  
    });
}



