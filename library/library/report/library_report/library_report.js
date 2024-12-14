// Copyright (c) 2024, savorn and contributors
// For license information, please see license.txt

frappe.query_reports["LIbrary Report"] = {
	"filters": [
        {
            "fieldname": "library_member",
            "label": __("Library Member"),
            "fieldtype": "MultiSelectList",
            get_data: function(txt){
                return frappe.db.get_link_options("Library Member", txt, {});
            }
        },
        {
            "fieldname": "author",
            "label": __("Author"),
            "fieldtype": "MultiSelectList",
            get_data: function(txt){
                return frappe.db.get_link_options("Author", txt, {});
            }
        },
        {
            "fieldname": "book_name",
            "label": __("Book Name"),
            "fieldtype": "MultiSelectList",
            get_data: function(txt) {
                return frappe.db.get_link_options("Books", txt, {});
            }
        },
        {
            "fieldname": "status",
            "label": __("Status"),
            "fieldtype": "MultiSelectList",
            get_data: function (txt) {
                return frappe.db.get_list("Library Transaction", {
                    fields:  ["status"], 
                    filters: { docstatus: ["!=", 2] },
                    limit: 1000
                }).then(data => {
                    // Use a Set to filter out duplicate and null values
                    const uniqueConditions = Array.from(new Set(
                        data
                            .map(item => item.status)
                            .filter(condition => condition && condition.trim() !== "") // Exclude null and empty values
                    ));

                    // Return data in the format expected by MultiSelectList
                    return uniqueConditions.map(condition => ({
                        value: condition,
                        label: condition,
                        description:""
                    }));
                });
            }
        },
        {
            "fieldname": "penalty_reason",
            "label": __("Penalty Reason"),
            "fieldtype": "MultiSelectList",
            get_data: function (txt) {
                return frappe.db.get_list("Library Transaction", {
                    fields:  ["penalty_reason"], 
                    filters: { docstatus: ["!=", 2] },
                    limit: 1000
                }).then(data => {
                    // Use a Set to filter out duplicate and null values
                    const uniqueConditions = Array.from(new Set(
                        data
                            .map(item => item.penalty_reason)
                            .filter(condition => condition && condition.trim() !== "") // Exclude null and empty values
                    ));

                    // Return data in the format expected by MultiSelectList
                    return uniqueConditions.map(condition => ({
                        value: condition,
                        label: condition,
                        description:""
                    }));
                });
            }
        },
        {
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": "80",
			"reqd": 0,
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": "80",
			"reqd": 1,
			"default": frappe.datetime.get_today()
		},    
        
    ]
};
