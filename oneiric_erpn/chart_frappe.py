from __future__ import unicode_literals
import frappe

@frappe.whitelist(allow_guest=True)
def graph():
    it = "Guest"
    it2 = "Administrator"
    sql = frappe.db.sql("""Select grand_total,transaction_date from `tabSales Order` where customer=%s""",(it))
    sql2 = frappe.db.sql("""Select grand_total from `tabSales Order` where customer=%s""", (it2))
    sql3 = frappe.db.sql("""Select transaction_date from `tabSales Order` where customer=%s""", (it))
    add = sql[1][0] + sql[0][0]
    if sql[0][1] == sql[1][0]:
        print(add)
    else:
        print("Wrong")

    print("============================================================================")
    print(sql[0][1])
    print(add)
    print("============================================================================")
    return sql,sql2,sql3

# @frappe.whitelist(allow_guest=True)
# def world1():
#     it = "Guest"
#     # it2 = "Administrator"
#     sql = frappe.db.sql("""Select grand_total from `tabSales Order` where customer=%s""",(it))
#     # sql2 = frappe.db.sql("""Select grand_total from `tabSales Order` where customer=%s""", (it2))
#     # sql3 = frappe.db.sql("""Select transaction_date from `tabSales Order` where customer=%s""", (it))
#     add = sql[0][0]
#     add2 = sql[1][0]
#     print("============================================================================")
#     print(add)
#     print(add2)
#     print("============================================================================")
#     return sql [1]