# Copyright (c) 2013, oneiric and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

def execute(filters=None):
    columns, data = [], []
    cust = filters.get("customer")
    start_date = filters.get("start_date")
    end_date = filters.get("end_date")
    type = filters.get("type")

    columns = [
        {"label": "Customer", 'width': 300, "fieldname": "customer"},
        {"label": "Date", 'width': 250, "fieldname": "transaction_date"},
        {"label": "Grand Total", 'width': 250, "fieldname": "grand_total"},
    ]

    so1 = frappe.db.sql(
        """Select sum(grand_total), avg(grand_total) from `tabSales Order` where customer=%s""",
        (cust))

    print("=================================================================================")
    if type == "Daily":
        print("Daily")
        data.append()
    elif type == "Weekly":
        print("Weekly")
    elif type == "Monthly":
        print("Monthly")
    else:
        print("SELECT TYPE!")

    print("=================================================================================")

    so = frappe.db.sql("""Select customer, transaction_date, grand_total from `tabSales Order` where customer=%s""",(cust))

    print("=================================================================================")
    print(so1)
    print("=================================================================================")

    for i in so:
        data.append({'customer': i[0], 'transaction_date': i[1], 'grand_total': i[2]})

    # chart = get_chart_data(columns, cust, )
    return columns, data

# def get_chart_data(columns, cust):
#     labels = [d.get("label") for d in columns[2:]]
#
#     data = []
#
#     for p in columns[2:]:
#         if data:
#             data.append(cust[-2].get(p.get("fieldname")))
#
#     datasets = []
#     if data:
#         datasets.append({'title':'Customer', 'values': cust})
#     # 	if liability_data:
#     # 		datasets.append({'title':'Liabilities', 'values': liability_data})
#     # 	if equity_data:
#     # 		datasets.append({'title':'Equity', 'values': equity_data})
#
#     chart = {
#         "data": {
#             'labels': labels,
#             'datasets': datasets
#         }
#     }
#
#     chart["type"] = "line"
#  # print(get_chart_data)
#     return chart