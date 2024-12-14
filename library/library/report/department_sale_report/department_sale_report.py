# import frappe
# import datetime
# from datetime import datetime

# def execute(filters=None):
#     # Define columns for the report
#     columns = [
#         {"label": "Sales Person", "fieldname": "parent", "fieldtype": "Link", "options": "Sales Person", "width": 150},
#         {"label": "Item Group", "fieldname": "item_group", "fieldtype": "Data", "width": 150},
#         {"label": "Target Quantity", "fieldname": "target_qty", "fieldtype": "Float", "width": 150},
#         {"label": "Target Amount", "fieldname": "target__amount", "fieldtype": "Currency", "width": 150},
#         {"label": "Actual Target", "fieldname": "actual_target", "fieldtype": "Int", "width": 150},
#         {"label": "Sale Percentage", "fieldname": "sale_percent", "fieldtype": "Percent", "width": 150},
#         {"label": "Target Distribution", "fieldname": "target_distribution", "fieldtype": "Data", "width": 150},
#         {"label": "Months", "fieldname": "months", "fieldtype": "Data", "width": 150},
#     ]
    
#     data = []
#     item_groups = []
#     sale_percentages = []
#     actual_targets = []
#     sale_name = []

#     # Apply filters to fetch target documents
#     target_doc_filters = {}
#     if filters.get('parent'):
#         target_doc_filters["parent"] = filters['parent']
#         sale_name = filters['parent']
#     else:
#         sale_name = "All Sales Person"
#     if filters.get('item_group') and filters['item_group'] != "All":
#         target_doc_filters["item_group"] = filters['item_group']

#     if filters.get('period'):
#         period = filters['period']

#     # Get filtered Target Doc entries
#     target_docs = frappe.get_all("Target Doc", filters=target_doc_filters, fields=["*"])

#     for doc in target_docs:
#         # Count linked item groups
#         actual_target = len(frappe.get_all(
#             doc.item_group,
#             filters=[{"sales_person": doc.parent}],
#             fields=["name"]
#         ))

#         # Fetch monthly distribution data
#         monthly_distribution = frappe.get_all(
#             "Monthly Distribution Percentage",
#             filters=[{"parent": doc.target_distribution}],
#             fields=["parent", "month", "percentage_allocation"]
#         )

#         # Check if percentage allocation values are equal across all months
#         percentages_equal = len(set(round(d['percentage_allocation']) for d in monthly_distribution)) == 1

#         # If 'Year' period, calculate yearly sales percentage
#         if period == "Year":
#             # Calculate total target quantity for the year (sum of all months)
#             total_yearly_target = sum(
#                 (doc.target_qty * month_data['percentage_allocation']) / 100 for month_data in monthly_distribution
#             )
#             # Calculate sale percentage for the entire year
#             sale_percent = (actual_target / total_yearly_target * 100) if total_yearly_target else 0
#             months_display = "Yearly Target"  # Show "Yearly Target" for year-based data
#         else:
#             # Calculate Sale Percentage for each month
#             if percentages_equal:
#                 monthly_qty = doc.target_qty / 12  # Assuming 12 months in a year
#                 sale_percent = (actual_target / monthly_qty * 100) if monthly_qty else 0
#                 months_display = "Monthly Distribution"  # Placeholder for parent row
#             else:
#                 total_monthly_target = 0
#                 for month_data in monthly_distribution:
#                     # Calculate monthly target quantity based on percentage allocation
#                     month_target_qty = (doc.target_qty * month_data['percentage_allocation']) / 100
#                     total_monthly_target += month_target_qty

#                 # Calculate sale percentage using the total monthly target
#                 sale_percent = (actual_target / total_monthly_target * 100) if total_monthly_target else 0
#                 months_display = "Monthly Distribution"  # Placeholder for parent row

#         # Add row data for the parent row (salesperson)
#         data.append({
#             "parent": doc.parent,
#             "item_group": doc.item_group,
#             "target_qty": doc.target_qty,
#             "target__amount": doc.target__amount,
#             "actual_target": actual_target,
#             "sale_percent": sale_percent,
#             "target_distribution": doc.target_distribution,
#             "months": months_display,
#         })

       
#         # Add child rows for each month (if the period is not 'Year')
#         if period != "Year":
#             for month_data in monthly_distribution:
#                 month_target_qty = (doc.target_qty * month_data['percentage_allocation']) / 100
#                 total_monthly_target = month_target_qty

#                 # Calculate sale percentage for each month
#                 sale_percent_month = (actual_target / total_monthly_target * 100) if total_monthly_target else 0

#                 # Add data for each month
#                 data.append({
#                     "parent": None,  # Child rows do not need a parent link
#                     "item_group": None,
#                     "target_qty": None,
#                     "target__amount": None,
#                     "actual_target": None,
#                     "sale_percent": None,  # Use the monthly calculated percentage
#                     "target_distribution": None,
#                     "months": f"{month_data['month']} ({round(month_data['percentage_allocation'], 3)}%)",  # Updated format
#                     "indent": 1,  # Child row (indented)
#                 })

#                 # Prepare data for the chart (use monthly data for chart)
#                 item_groups.append(f"{month_data['month']} ({round(month_data['percentage_allocation'], 3)}%)")
#                 sale_percentages.append(sale_percent_month)  # Store monthly sale percentage for chart
#                 actual_targets.append(actual_target)  # Collect actual target values for chart
#         # For 'Year' period, aggregate the data for the year

#         else:
#             # Only the aggregated total for the year, no child rows
#             item_groups.append(doc.item_group)
#             sale_percentages.append(sale_percent)  # Use yearly sale percentage
#             actual_targets.append(actual_target)  # Use total actual target for the year
#         if period == "Quoter":
#             for month_data in monthly_distribution:
#                 # Get current month
#                 now = datetime.now()
#                 # Get the last 3 months (including the current month)
#                 months = [(now.replace(month=((now.month - i - 1) % 12) + 1).strftime('%B')) for i in range(3)]

#                 for month in months:
#                     if month_data.month == month:
#                         print(month_data.percentage_allocation)
#                     # print(month)
#                 # print("Quoter----------------------------------------------------------")
#     # Define chart configuration
#     chart = {
#         "type": "bar",  # Chart types: bar, line, pie
#         "colors": ["#3498db", "#2ecc71"],  # Custom colors for the chart
#         "data": {
#             "labels": item_groups,  # Set item groups as labels (monthly or yearly)
#             "datasets": [
#                 {
#                     "name": "Sale Percentage",
#                     "values": sale_percentages,  # Use sale percentages (monthly or yearly)
#                 },
#                 {
#                     "name": "Actual Target",
#                     "values": actual_targets,  # Use actual targets (monthly or yearly)
#                 }
#             ],
#         },
#         "title": sale_name,  # Title based on salesperson or "All Sales Person"
#     }

#     # Return columns, data, and chart
#     return columns, data, None, chart














# # ----------------------------------------------------------------------
# import frappe
# from datetime import datetime

# def execute(filters=None):
#     # Define columns for the report
#     columns = [
#         {"label": "Sales Person", "fieldname": "parent", "fieldtype": "Link", "options": "Sales Person", "width": 150},
#         {"label": "Item Group", "fieldname": "item_group", "fieldtype": "Data", "width": 150},
#         {"label": "Target Quantity", "fieldname": "target_qty", "fieldtype": "Float", "width": 150},
#         {"label": "Target Amount", "fieldname": "target__amount", "fieldtype": "Currency", "width": 150},
#         {"label": "Actual Target", "fieldname": "actual_target", "fieldtype": "Int", "width": 150},
#         {"label": "Sale Percentage", "fieldname": "sale_percent", "fieldtype": "Percent", "width": 150},
#         {"label": "Target Distribution", "fieldname": "target_distribution", "fieldtype": "Data", "width": 150},
#         {"label": "Months", "fieldname": "months", "fieldtype": "Data", "width": 150},
#     ]
    
#     data = []
#     item_groups = []
#     sale_percentages = []
#     actual_targets = []
#     sale_name = []

#     # Apply filters to fetch target documents
#     target_doc_filters = {}
#     if filters.get('parent'):
#         target_doc_filters["parent"] = filters['parent']
#         sale_name = filters['parent']
#     else:
#         sale_name = "All Sales Person"
#     if filters.get('item_group') and filters['item_group'] != "All":
#         target_doc_filters["item_group"] = filters['item_group']

#     if filters.get('period'):
#         period = filters['period']
#         print(period)

#     # Get filtered Target Doc entries
#     target_docs = frappe.get_all("Target Doc", filters=target_doc_filters, fields=["*"])

#     for doc in target_docs:
#         # Count linked item groups
#         actual_target = len(frappe.get_all(
#             doc.item_group,
#             filters=[{"sales_person": doc.parent}],
#             fields=["name"]
#         ))

#         # Fetch monthly distribution data
#         monthly_distribution = frappe.get_all(
#             "Monthly Distribution Percentage",
#             filters=[{"parent": doc.target_distribution}],
#             fields=["parent", "month", "percentage_allocation"]
#         )

#         # Check if percentage allocation values are equal across all months
#         percentages_equal = len(set(round(d['percentage_allocation']) for d in monthly_distribution)) == 1

#         # Calculate Sale Percentage if needed
#         if percentages_equal:
#             monthly_qty = doc.target_qty / 12  # Assuming 12 months in a year
#             sale_percent = (actual_target / monthly_qty * 100) if monthly_qty else 0
#         else:
#             total_monthly_target = 0
#             for month_data in monthly_distribution:
#                 # Calculate monthly target quantity based on percentage allocation
#                 month_target_qty = (doc.target_qty * month_data['percentage_allocation']) / 100
#                 total_monthly_target += month_target_qty

#             # Calculate sale percentage using the total monthly target
#             sale_percent = (actual_target / total_monthly_target * 100) if total_monthly_target else 0

#         # Add row data for the parent row (salesperson)
#         data.append({
#             "parent": doc.parent,
#             "item_group": doc.item_group,
#             "target_qty": doc.target_qty,
#             "target__amount": doc.target__amount,
#             "actual_target": actual_target,
#             "sale_percent": sale_percent,
#             "target_distribution": doc.target_distribution,
#             "months": "Monthly Distribution",  # Placeholder for parent row
#         })

#         # Add child rows for each month (updated "Months" column)
#         for month_data in monthly_distribution:
#             month_target_qty = (doc.target_qty * month_data['percentage_allocation']) / 100
#             total_monthly_target = month_target_qty

#             # Calculate sale percentage for each month
#             sale_percent_month = (actual_target / total_monthly_target * 100) if total_monthly_target else 0


#             # Add data for each month
#             data.append({
#                 "parent": None,  # Child rows do not need a parent link
#                 "item_group": None,
#                 "target_qty": None,
#                 "target__amount": None,
#                 "actual_target": None,
#                 "sale_percent": None,
#                 "target_distribution": None,
#                 "months": f"{month_data['month']} ({round(month_data['percentage_allocation'], 2)}%)",  # Updated format
#                 "indent": 1,  # Child row (indented)
#             })

#         # Prepare data for the chart
#         item_groups.append(doc.item_group)  # Collect item_group names
#         sale_percentages.append(sale_percent)  # Use calculated sale percentage
#         actual_targets.append(actual_target)  # Collect actual target values

#         if period == "Quoter":
#             # Get the current date and calculate the last 3 months
#             now = datetime.now()
#             last_three_months = [
#                 (now.replace(month=((now.month - i - 1) % 12) + 1).strftime('%B')) 
#                 for i in range(3)
#             ]

#             # Filter monthly distributions for the last three months
#             for month_data in monthly_distribution:
#                 if month_data['month'] in last_three_months:
#                     month_target_qty = (doc.target_qty * month_data['percentage_allocation']) / 100
#                     sale_percent_month = (actual_target / month_target_qty * 100) if month_target_qty else 0

#                     # Add row for report
#                     data.append({
#                         "parent": doc.parent,
#                         "item_group": doc.item_group,
#                         "target_qty": doc.target_qty,
#                         "target__amount": doc.target__amount,
#                         "actual_target": actual_target,
#                         "sale_percent": sale_percent_month,
#                         "target_distribution": doc.target_distribution,
#                         "months": f"{month_data['month']} ({round(month_data['percentage_allocation'], 3)}%)",
#                         # "indent": 1,
#                     })

#                     # Add data for the chart
#                     item_groups.append(f"{month_data['month']} ({round(month_data['percentage_allocation'], 3)}%)")
#                     sale_percentages.append(sale_percent_month)
#                     actual_targets.append(actual_target)



#     # Define chart configuration
#     chart = {
#         "type": "bar",  # Chart types: bar, line, pie
#         "colors": ["#3498db", "#2ecc71"],  # Custom colors for the chart
#         "data": {
#             "labels": item_groups,  # Set item groups as labels
#             "datasets": [
#                 {
#                     "name": "Sale Percentage",
#                     "values": sale_percentages,
#                 },
#                 {
#                     "name": "Actual Target",
#                     "values": actual_targets,
#                 }
#             ],
#         },
#         "title": sale_name,
#     }

#     # Return columns, data, and chart
#     return columns, data, None, chart





# # ------------------------------------------------------------------------

# import frappe
# from datetime import datetime

# def execute(filters=None):
#     # Define columns for the report
#     columns = [
#         {"label": "Sales Person", "fieldname": "parent", "fieldtype": "Link", "options": "Sales Person", "width": 150},
#         {"label": "Item Group", "fieldname": "item_group", "fieldtype": "Data", "width": 150},
#         {"label": "Target Quantity", "fieldname": "target_qty", "fieldtype": "Float", "width": 150},
#         {"label": "Target Amount", "fieldname": "target__amount", "fieldtype": "Currency", "width": 150},
#         {"label": "Actual Target", "fieldname": "actual_target", "fieldtype": "Int", "width": 150},
#         {"label": "Sale Percentage", "fieldname": "sale_percent", "fieldtype": "Percent", "width": 150},
#         {"label": "Target Distribution", "fieldname": "target_distribution", "fieldtype": "Data", "width": 150},
#         {"label": "Months", "fieldname": "months", "fieldtype": "Data", "width": 150},
#     ]
    
#     data = []
#     item_groups = []
#     sale_percentages = []
#     actual_targets = []
    
#     # Parse filters
#     target_doc_filters = {}
#     if filters.get('parent'):
#         # Handle multiple salespersons
#         target_doc_filters["parent"] = ["in", filters['parent']]
#         sale_name = ", ".join(filters['parent'])
#     else:
#         sale_name = "All Sales Persons"

#     # Handle 'item_group' MultiSelectList filter
#     item_groups = filters.get("item_group", [])
#     if item_groups and "All" not in item_groups:
#         target_doc_filters["item_group"] = ["in", item_groups]

#     period = filters.get('period', 'Year')  # Default period to Year if not specified

#     # Fetch Target Docs
#     target_docs = frappe.get_all("Target Doc", filters=target_doc_filters, fields=["*"])

#     for doc in target_docs:
#         # Get actual target count
#         actual_target = len(frappe.get_all(
#             doc.item_group,
#             filters=[{"sales_person": doc.parent}],
#             fields=["name"]
#         ))

#         # Fetch monthly distribution
#         monthly_distribution = frappe.get_all(
#             "Monthly Distribution Percentage",
#             filters=[{"parent": doc.target_distribution}],
#             fields=["parent", "month", "percentage_allocation"]
#         )

#         if period == "Year":
#             # Calculate yearly target and sale percentage
#             monthly_qty = doc.target_qty / 12  # Assuming 12 months in a year
#             sale_percent = (actual_target / monthly_qty * 100) 
#             data.append({
#                 "parent": doc.parent,
#                 "item_group": doc.item_group,
#                 "target_qty": doc.target_qty,
#                 "target__amount": doc.target__amount,
#                 "actual_target": actual_target,
#                 "sale_percent": sale_percent,
#                 "target_distribution": doc.target_distribution,
#                 "months": "Yearly Target",
#             })
#             item_groups.append(doc.item_group)
#             sale_percentages.append(sale_percent)
#             actual_targets.append(actual_target)

#         elif period == "Quoter":
#             # Last 3 months
#             now = datetime.now()
#             last_three_months = [
#                 (now.replace(month=((now.month - i - 1) % 12) + 1).strftime('%B')) 
#                 for i in range(3)
#             ]

#             for month_data in monthly_distribution:
#                 if month_data['month'] in last_three_months:
#                     month_target_qty = (doc.target_qty * month_data['percentage_allocation']) / 100
#                     sale_percent_month = (actual_target / month_target_qty * 100) if month_target_qty else 0
                    
#                     # Add row for report
#                     data.append({
#                         "parent": doc.parent,
#                         "item_group": doc.item_group,
#                         "target_qty": doc.target_qty,
#                         "target__amount": doc.target__amount,
#                         "actual_target": actual_target,
#                         "sale_percent": sale_percent_month,
#                         "target_distribution": doc.target_distribution,
#                         "months": f"{month_data['month']} ({round(month_data['percentage_allocation'], 3)}%)",
#                         "indent": 1,
#                     })
                    
#                     # Add data for chart
#                     item_groups.append(f"{month_data['month']} ({round(month_data['percentage_allocation'], 3)}%)")
#                     sale_percentages.append(sale_percent_month)
#                     actual_targets.append(actual_target)

#         elif period == "Monthly":
#             # Calculate Sale Percentage for each month
#             for month_data in monthly_distribution:
#                 # Calculate monthly target quantity based on percentage allocation
#                 month_target_qty = (doc.target_qty * month_data['percentage_allocation']) / 100
#                 sale_percent_month = (actual_target / month_target_qty * 100) if month_target_qty else 0
                
                
#                 # Add row for report
#                 data.append({
#                     "parent": doc.parent,
#                     "item_group": doc.item_group,
#                     "target_qty": doc.target_qty,
#                     "target__amount": doc.target__amount,
#                     "actual_target": actual_target,
#                     "sale_percent": sale_percent_month,
#                     "target_distribution": doc.target_distribution,
#                     "months": f"{month_data['month']} ({round(month_data['percentage_allocation'], 3)}%)",
#                     "indent": 1,
#                 })

#                 # Add data for chart
#                 item_groups.append(f"{month_data['month']} ({round(month_data['percentage_allocation'], 3)}%)")
#                 sale_percentages.append(sale_percent_month)
#                 actual_targets.append(actual_target)

#     # Define chart configuration
#     chart = {
#         "type": "bar",  # Chart types: bar, line, pie
#         "colors": ["#3498db", "#2ecc71"],  # Custom colors for the chart
#         "data": {
#             "labels": item_groups,  # Set item groups as labels (monthly or yearly)
#             "datasets": [
#                 {
#                     "name": "Sale Percentage",
#                     "values": sale_percentages,  # Use sale percentages (monthly or yearly)
#                 },
#                 {
#                     "name": "Actual Target",
#                     "values": actual_targets,  # Use actual targets (monthly or yearly)
#                 }
#             ],
#         },
#         "title": sale_name,  # Title based on salesperson or "All Sales Person"
#     }

#     # Return columns, data, and chart
#     return columns, data, None, chart







import frappe
from datetime import datetime

def execute(filters=None):
    # Define columns for the report
    columns = [
        {"label": "Sales Person", "fieldname": "parent", "fieldtype": "Link", "options": "Sales Person", "width": 150},
        {"label": "Item Group", "fieldname": "item_group", "fieldtype": "Data", "width": 150},
        {"label": "Target Quantity", "fieldname": "target_qty", "fieldtype": "Float", "width": 150},
        {"label": "Target Amount", "fieldname": "target__amount", "fieldtype": "Currency", "width": 150},
        {"label": "Actual Target", "fieldname": "actual_target", "fieldtype": "Int", "width": 150},
        {"label": "Sale Percentage", "fieldname": "sale_percent", "fieldtype": "Percent", "width": 150},
        {"label": "Target Distribution", "fieldname": "target_distribution", "fieldtype": "Data", "width": 150},
        {"label": "Months", "fieldname": "months", "fieldtype": "Data", "width": 150},
    ]
    
    data = []
    item_groups = []
    sale_percentages = []
    actual_targets = []
    
    # Parse filters
    target_doc_filters = {}
    if filters.get('parent'):
        target_doc_filters["parent"] =["in", filters['parent']] 
        sale_name = filters['parent']
    else:
        sale_name = "All Sales Person"

    if filters.get('item_group') and filters['item_group'] != "All":
        target_doc_filters["item_group"] = ["in", filters['item_group']]

    period = filters.get('period', 'Year')  # Default period to Year if not specified

    # Fetch Target Docs
    target_docs = frappe.get_all("Target Doc", filters=target_doc_filters, fields=["*"])

    for doc in target_docs:
        # Get actual target count
        actual_target = len(frappe.get_all(
            doc.item_group,
            filters=[{"sales_person": doc.parent}],
            fields=["name"]
        ))

        # Fetch monthly distribution
        monthly_distribution = frappe.get_all(
            "Monthly Distribution Percentage",
            filters=[{"parent": doc.target_distribution}],
            fields=["parent", "month", "percentage_allocation"]
        )

        if period == "Year":
            # Calculate yearly target and sale percentage
            monthly_qty = doc.target_qty / 12  # Assuming 12 months in a year
            sale_percent = (actual_target / monthly_qty * 100) 
            data.append({
                "parent": doc.parent,
                "item_group": doc.item_group,
                "target_qty": doc.target_qty,
                "target__amount": doc.target__amount,
                "actual_target": actual_target,
                "sale_percent": sale_percent,
                "target_distribution": doc.target_distribution,
                "months": "Yearly Target",
            })
            item_groups.append(doc.item_group)
            sale_percentages.append(sale_percent)
            actual_targets.append(actual_target)

        elif period == "Quoter":
            # Last 3 months
            now = datetime.now()
            last_three_months = [
                (now.replace(month=((now.month - i - 1) % 12) + 1).strftime('%B')) 
                for i in range(3)
            ]
            

            for month_data in monthly_distribution:
                if month_data['month'] in last_three_months:
                    month_target_qty = (doc.target_qty * month_data['percentage_allocation']) / 100
                    # sale_percent_month = (actual_target / month_target_qty * 100) if month_target_qty else 0
                    
                    # Add row for report
                    data.append({
                        "parent": doc.parent,
                        "item_group": doc.item_group,
                        "target_qty": doc.target_qty,
                        "target__amount": doc.target__amount,
                        "actual_target": actual_target,
                        "sale_percent": month_target_qty,
                        "target_distribution": doc.target_distribution,
                        "months": f"{month_data['month']} ({round(month_data['percentage_allocation'], 3)}%)",
                        "indent": 1,
                    })
                    
                    # Add data for chart
                    # item_groups.append(f"{month_data['month']} ({round(month_data['percentage_allocation'], 3)}%)")
                    item_groups.append(month_data["month"])
                    sale_percentages.append(month_target_qty)
                    actual_targets.append(actual_target)

        elif period == "Monthly":
            # Sort monthly distribution to ensure order
            month_order = {
                "January": 1, "February": 2, "March": 3, "April": 4,
                "May": 5, "June": 6, "July": 7, "August": 8,
                "September": 9, "October": 10, "November": 11, "December": 12
            }
            monthly_distribution_sorted = sorted(
                monthly_distribution, key=lambda x: month_order[x["month"]]
            )

            for month_data in monthly_distribution_sorted:
                month_target_qty = (doc.target_qty * month_data["percentage_allocation"]) / 100

                data.append({
                    "parent": doc.parent,
                    "item_group": doc.item_group,
                    "target_qty": doc.target_qty,
                    "target__amount": doc.target__amount,
                    "actual_target": actual_target,
                    "sale_percent": month_target_qty,
                    "target_distribution": doc.target_distribution,
                    "months": f"{month_data['month']} ({round(month_data['percentage_allocation'], 3)}%)",
                    "indent": 1,
                })

                item_groups.append(month_data["month"])
                sale_percentages.append(month_target_qty)
                actual_targets.append(actual_target)


    # Define chart configuration
    chart = {
        "type": "bar",  # Chart types: bar, line, pie
        "colors": ["#3498db", "#2ecc71"],  # Custom colors for the chart
        "data": {
            "labels": item_groups,  # Set item groups as labels (monthly or yearly)
            "datasets": [
                {
                    "name": "Sale Percentage",
                    "values": sale_percentages,  # Use sale percentages (monthly or yearly)
                },
                {
                    "name": "Actual Target",
                    "values": actual_targets,  # Use actual targets (monthly or yearly)
                }
            ],
        },
        "title": sale_name,  # Title based on salesperson or "All Sales Person"
    }

    # Return columns, data, and chart
    return columns, data, None, chart