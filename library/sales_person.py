import frappe

def create_sale_person_of_compare_rate_into_dashboard(doc, method):
    """
    Trigger function to create a dashboard chart for a sales person.
    """
    sale_person_name = doc.name
    print(f"Processing dashboard chart for: {sale_person_name}")

    if frappe.db.exists("Dashboard Chart", {"chart_name": sale_person_name}):
        print(f"Chart for {sale_person_name} already exists. Skipping creation.")
        return

    try:
        create_dashboard_chart(sale_person_name)
        link_chart_to_dashboard(sale_person_name)
        print(f"Dashboard chart '{sale_person_name}' created and linked successfully.")
    except Exception as e:
        print(f"Error creating dashboard chart for {sale_person_name}: {str(e)}")

def create_dashboard_chart(sale_person_name):
    """
    Create a new dashboard chart for the given sales person.
    """
    filters_json = {
        "item_group":None,
        "period": "Year",
        "parent": sale_person_name
    }
    
    frappe.get_doc({
        "doctype": "Dashboard Chart",
        "module": "VRS",
        "chart_name": sale_person_name + " Chart",
        "chart_type": "Report",
        "type": "Bar",
        "report_name": "Department Sale Report",
        "filters_json": frappe.as_json(filters_json),  # Convert the dictionary to JSON
        "is_standard": 1,
        "is_public": 1,
        "use_report_chart": 1
    }).insert(ignore_permissions=True)


def link_chart_to_dashboard(sale_person_name):
    """
    Link the newly created dashboard chart to the dashboard.
    """
    frappe.get_doc({
        "doctype": "Dashboard Chart Link",
        "chart": sale_person_name + " Chart",
        "parent": "Department Sale",
        "parentfield": "charts",
        "parenttype": "Dashboard",
        "width": "Full",
    }).insert(ignore_permissions=True)
