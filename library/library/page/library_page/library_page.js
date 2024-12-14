frappe.pages['library-page'].on_page_load = function(wrapper) {
	new DepartmentSaleDashboard(wrapper);
};

let DepartmentSaleDashboard = Class.extend({
    // Initialize the dashboard page
    init: function (wrapper) {
        this.page = frappe.ui.make_app_page({
            parent: wrapper,
            title: __("Library Page"),
            single_column: true,
        });
        this.make();
    },

	make: async function () {
        let rendered_html = frappe.render_template("library", {});
        $(rendered_html).appendTo(this.page.main);

        this.get_books();
    },

	get_books: async function () {
        try {
            let { message: books_api } = await frappe.call({
                method: "library.library.page.library_page.library_page.get_books_from_library",
                async: false,
            });
            books_api ? create_dom_books(books_api) : console.log("No data received");
        } catch (error) {
            console.log(error);
        }
    },
	
});
function create_dom_books(books_api) {
    let getBooks = $("#getBooks");
    $.each(books_api.books, function (index, book) {
        let bookCard = `
            <div style="display: flex; justify-content: space-between;" class="w-full h-200 max-w-xs overflow-hidden bg-white rounded-lg shadow-lg dark:bg-gray-800">
                <img class="object-cover w-full h-56" src="${book.book_cover}" alt="avatar">
                <div class="py-5 text-center w-full">
                    <a href="${book.link_url}" class="block text-xl font-bold text-gray-800 dark:text-white" tabindex="0">
                        ${book.book_name}
                    </a>
                    <span class="text-sm text-gray-700 dark:text-gray-200">${book.author}</span>
                </div>
            </div>
        `;
        getBooks.append(bookCard);
    });
}


