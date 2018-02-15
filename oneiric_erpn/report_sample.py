# Copyright (c) 2013, Bai Mobile and Web Labs and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta


def execute(filters=None):
    columns = []
    data = []
    chart = None
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    category = filters.get("category")
    type = filters.get("report_type")
    branch = filters.get("branch")


    if category == None:
        for cat in frappe.db.sql("""Select name from `tabItem Category`"""):
            data, amount, qty, profit = get_category_data(type, from_date, to_date, branch, cat[0], data)
            data, percent = get_percent_growth(type, from_date, to_date, branch, cat[0], data)
    else:
        data, amount, qty, profit = get_category_data(type, from_date, to_date, branch, category,data)
        data, percent = get_percent_growth(type, from_date, to_date, branch, category, data)
    columns = get_columns(type, from_date, to_date)
    chart = get_chart(columns, amount, None, None, None)
    #chart = get_chart(columns, amount, qty, profit, percent)
    return columns, data, None, chart


def get_columns(type, from_date, to_date):
    columns = []
    columns = [{"label": "Category", 'width': 200, "fieldname": "category"},
               {"label": "Type", 'width': 200, "fieldname": "type"},
               {"label": "Previous Value", 'width': 200, "fieldname": "previous_amt", "fieldtype":"Float", "precision":2}]
    label = None
    from_date = datetime.strptime(from_date, '%Y-%m-%d')
    to_date = datetime.strptime(to_date, '%Y-%m-%d')
    current_date = from_date
    interval = 0
    width = 80
    print type
    if type == "Monthly":
        interval = 1
    elif type == "Quarterly":
        interval = 3
    else:
        interval = 12
    while current_date <= to_date:
        if interval == 1:
            label = current_date.strftime("%B")
            width = 80
        elif interval == 3:
            label = "" + current_date.strftime("%B") + " - " + (current_date + relativedelta(months=interval - 1)).strftime("%B")
            width = 120
        else:
            width = 200
            label = current_date.strftime("%B %Y") + " - " + (
            current_date + relativedelta(months=interval - 1)).strftime("%B %Y")
        print label
        columns.append({"label": label, 'width': width, "fieldname": label, "fieldtype": "Float", "precision":2})
        current_date = current_date + relativedelta(months=interval)
    return columns


def get_category_data(type, from_date, to_date, branch, category,data):
    amount_data, qty_data, profit_data = [], [], []
    amt_dict = dict()
    qty_dict = dict()
    profit_dict = dict()
    from_date = datetime.strptime(from_date, '%Y-%m-%d')
    to_date = datetime.strptime(to_date, '%Y-%m-%d')
    amt_dict["category"] = category
    amt_dict["type"] = "Peso Value"
    qty_dict["category"] = category
    qty_dict["type"] = "Volume"
    profit_dict["category"] = category
    profit_dict["type"] = "Profit"
    start_date = from_date
    qty, amount, profit = 0,0,0
    prev_qty, prev_amt, prev_profit = 0,0,0
    interval = 0
    if type == "Monthly":
        interval = 1
    elif type == "Quarterly":
        interval = 3
    else:
        interval = 12
    previous_start = (start_date - relativedelta(months=interval)).replace(day=1)
    previous_end = (previous_start + relativedelta(months=interval)) - timedelta(days=1)
    prev_qty, prev_amt, prev_profit = get_category_sales(branch, previous_start, previous_end, category)
    amt_dict["previous_amt"], qty_dict["previous_amt"], profit_dict["previous_amt"] = prev_amt, prev_qty, prev_profit
    while start_date <= to_date:
        print "=============LOOOOOOOOOOP=============="
        if interval == 1:
            start_date = start_date.replace(day=1)
            label = start_date.strftime("%B")
            end_date = start_date + relativedelta(months=1) - timedelta(days=1)
        elif interval == 3:
            start_date = start_date.replace(day=1)
            label = "" + start_date.strftime("%B") + " - " + (start_date + relativedelta(months=interval - 1)).strftime("%B")
            end_date = start_date + relativedelta(months=3) - timedelta(days=1)
        else:
            start_date = start_date.replace(day=1)
            end_date = start_date + relativedelta(months=12) - timedelta(days=1)
            label = start_date.strftime("%B %Y") + " - " + (start_date + relativedelta(months=interval - 1)).strftime("%B %Y")
        print "Start Date: " + str(start_date)
        print "End Date: " + str(end_date)
        print "label: " + label
        print "counter val, to_date"
        print start_date.strftime("%Y-%m-%d"), to_date.strftime("%Y-%m-%d")
        qty, amount, profit = get_category_sales(branch, start_date, end_date, category)
        amt_dict[label], qty_dict[label], profit_dict[label] = amount, qty, profit
        #print qty, amount, profit
        start_date = start_date + relativedelta(months=interval)
    data.append(amt_dict)
    data.append(qty_dict)
    data.append(profit_dict)
    amount_data.append(amt_dict)
    qty_data.append(qty_dict)
    profit_data.append(profit_dict)
    print data
    return data, amount_data,qty_data, profit_data

def get_category_sales(branch, from_date, to_date, category):
    total_qty, total_amount, total_profit = 0, 0, 0

    print branch, from_date, to_date, category

    items = frappe.db.sql("""SELECT item.name, item.barcode_retial, item.item_discount from
        `tabItem` item LEFT JOIN `tabItem Class Each` item_class ON item_class.parent = item.name where
        item_class.category = %s""", category)

    for item in items:

        try:
            total_sales = get_idv_sales(branch, from_date, to_date, item[0])
            #total_sales = frappe.db.sql("""select sum(qty), sum(amount), ((sum(amount))-(sum(qty*cost*(1-%s)))) from
            #  `tabUpload POS` where branch = %s and trans_date >= %s and trans_date <= %s AND barcode = %s""",
            #                        (item[2], branch, str(from_date), str(to_date), item[1]))
            # print total_sales
            total_qty += float(total_sales[0])
            total_amount += float(total_sales[1])
            total_profit += float(total_sales[2])
        except:
            continue
    return total_qty, total_amount, total_profit

def get_percent_growth(type, from_date, to_date, branch, category, data):
    percent = []
    temp = dict()
    from_date = datetime.strptime(from_date, '%Y-%m-%d')
    to_date = datetime.strptime(to_date, '%Y-%m-%d')
    temp["category"] = category
    temp["type"] = "Percent Increase/Decrease"
    start_date = from_date
    qty, amount, profit = 0,0,0
    prev_qty, prev_amt, prev_profit = 0,0,0
    interval = 0
    if type == "Monthly":
        interval = 1
    elif type == "Quarterly":
        interval = 3
    else:
        interval = 12

    print "=========Previous char:========"
    previous_start = (start_date - relativedelta(months=interval)).replace(day = 1)
    previous_end = (previous_start + relativedelta(months=interval)) - timedelta(days=1)
    print previous_start, previous_end
    prev_qty, prev_amt, prev_profit = get_category_sales(branch, previous_start, previous_end, category)

    while start_date <= to_date:
        print "=============LOOOOOOOOOOP=============="
        if interval == 1:
            start_date = start_date.replace(day=1)
            label = start_date.strftime("%B")
            end_date = start_date + relativedelta(months=1) - timedelta(days=1)
        elif interval == 3:
            start_date = start_date.replace(day=1)
            label = "" + start_date.strftime("%B") + " - " + (start_date + relativedelta(months=interval - 1)).strftime("%B")
            end_date = start_date + relativedelta(months=3) - timedelta(days=1)
        else:
            start_date = start_date.replace(day=1)
            end_date = start_date + relativedelta(months=12) - timedelta(days=1)
            label = start_date.strftime("%B %Y") + " - " + (start_date + relativedelta(months=interval - 1)).strftime("%B %Y")
        print "Start Date: " + str(start_date)
        print "End Date: " + str(end_date)
        print "label: " + label
        print "counter val, to_date"
        print start_date.strftime("%Y-%m-%d"), to_date.strftime("%Y-%m-%d")
        qty, amount, profit = get_category_sales(branch, start_date, end_date, category)
        temp[label] = (amount-prev_amt)/prev_amt*100
        prev_amt = amount
        #print qty, amount, profit
        start_date = start_date + relativedelta(months=interval)
        print temp
    data.append(temp)
    percent.append(temp)
    print data
    return data, percent

def get_idv_sales(branch, from_date, to_date, item_code):
    print "GET IDV SALES FUNCTION"
    volume , peso_value, profit = 0, 0, 0
    d1, d2, d3, d4 = get_supplier_discounts(item_code)
    try:
        item_doc = frappe.get_doc("Item", item_code)
    except:
        print "ERROR"
    else:
        idv_sales = frappe.db.sql("""select sum(qty), sum(amount), sum(qty*cost) from `tabUpload POS` where branch LIKE %s and trans_date >= %s and
                              trans_date <= %s AND barcode = %s""",
                                  ('%' + branch + '%', str(from_date), str(to_date), str(item_doc.barcode_retial)))
        if len(idv_sales) > 0:
            for sales in idv_sales:
                volume = (sales[0] if sales[0] != None else 0)
                peso_value = (sales[1] if sales[1] != None else 0)
                total_cost = (sales[2] if sales[2] != None else 0)
                net_cost = ((((float(total_cost) * (1 - d1)) * (1 - d2)) * (1 - d3)) * (1 - d4))
                profit = peso_value - (net_cost)
    print volume , peso_value, profit
    return volume, peso_value, profit


def get_supplier_discounts(item_code):
    discounts = frappe.db.sql("""Select parent from `tabSupplier Discount Items` where items = %s""", item_code)
    disc1, disc2, disc3, disc4 = 0, 0, 0, 0
    if len(discounts) > 0:
        for discount in discounts:
            supplier_discount = frappe.get_doc("Supplier Discounts", discount[0])
            disc1 = (supplier_discount.disc_1 if supplier_discount.disc_1 != None else 0)
            disc2 = (supplier_discount.disc_2 if supplier_discount.disc_2 != None else 0)
            disc3 = (supplier_discount.disc_3 if supplier_discount.disc_3 != None else 0)
            disc4 = (supplier_discount.disc_4 if supplier_discount.disc_4 != None else 0)
    return float(disc1/100), float(disc2/100), float(disc3/100), float(disc4/100)


def get_chart(columns, amount, qty, profit, percent):
    x_intervals = ['x'] + [d.get("label") for d in columns[3:]]
    amount_data, qty_data, profit_data, percent_data = [], [], [], []

    for p in columns[3:]:
        if amount:
            amount_data.append(amount[0].get(p.get("fieldname")))
        if qty:
            qty_data.append(qty[0].get(p.get("fieldname")))
        if profit:
            profit_data.append(profit[0].get(p.get("fieldname")))
        if percent:
            percent_data.append(amount[0].get(p.get("fieldname")))

    columns = [x_intervals]
    if amount_data:
        columns.append(["Peso Value"] + amount_data)
    if qty_data:
        columns.append(["Volume"] + qty_data)
    if profit_data:
        columns.append(["Profit"] + profit_data)
    if percent_data:
        columns.append(["Percent Increase/Decrease"] + amount_data)
    chart = {
        "data": {
            'x': 'x',
            'columns': columns
        }
    }

    chart["chart_type"] = "line"

    return chart
