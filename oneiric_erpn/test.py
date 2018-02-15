from __future__ import unicode_literals
import frappe
from frappe.frappeclient import FrappeClient

@frappe.whitelist(allow_guest=True)
def world():
    it = 1314
    sql = frappe.db.sql("""Select item_name from `tabItem` where item_code=%s""",(it))
    print(sql)
    return sql


@frappe.whitelist(allow_guest=True)
def cartPost(test):
    client = FrappeClient("http://0.0.0.0:8001", "guest@example.com", "qwerty0987")
    print "8=================POST TO CART TRIGGER=====================D"
    args = {"item_code": "1314", "qty": test }
    tags = client.post_api("erpnext.shopping_cart.cart.update_cart", args)
    print tags
    # placeOrder()
    print "8=================END TO CART TRIGGER=====================D"

@frappe.whitelist(allow_guest=True)
def placeOrder(test):
    client = FrappeClient("http://0.0.0.0:8001", "guest@example.com", "qwerty0987")
    print "======================CALL THIS================================"
    args = {"item_code": "1314", "qty": test}
    tags2 = client.post_api("erpnext.shopping_cart.cart.place_order", args)
    print tags2