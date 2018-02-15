// Copyright (c) 2016, oneiric and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Sales Order Daily Report"] = {
	"filters": [
                {
                    "fieldname":"customer",
                    "label":__("Customer"),
                    "fieldtype": "Link",
                    "options": "Customer",
                },
                {
                    "fieldname":"start_date",
                    "label":__("Start Date"),
                    "fieldtype": "Date",
                },
                {
                    "fieldname":"end_date",
                    "label":__("End Date"),
                    "fieldtype": "Date",
                },
                {

                    "fieldname":"type",
                    "label":__("Type"),
                    "fieldtype": "Select",
                    "options": ["", "Daily", "Weekly", "Monthly"]
                }
	]
}

// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors and contributors
// For license information, please see license.txt
//
//frappe.query_reports["Stock Balance"] = {
//	"filters": [
//		{
//			"fieldname":"from_date",
//			"label": __("From Date"),
//			"fieldtype": "Date",
//			"width": "80",
//			"reqd": 1,
//			"default": frappe.sys_defaults.year_start_date,
//		},
//		{
//			"fieldname":"to_date",
//			"label": __("To Date"),
//			"fieldtype": "Date",
//			"width": "80",
//			"reqd": 1,
//			"default": frappe.datetime.get_today()
//		},
//		{
//			"fieldname": "item_group",
//			"label": __("Item Group"),
//			"fieldtype": "Link",
//			"width": "80",
//			"options": "Item Group"
//		},
//		{
//			"fieldname": "item_code",
//			"label": __("Item"),
//			"fieldtype": "Link",
//			"width": "80",
//			"options": "Item"
//		},
//		{
//			"fieldname": "warehouse",
//			"label": __("Warehouse"),
//			"fieldtype": "Link",
//			"width": "80",
//			"options": "Warehouse"
//		},
//		{
//			"fieldname": "show_variant_attributes",
//			"label": __("Show Variant Attributes"),
//			"fieldtype": "Check"
//		},
//	]
//}

// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt
//
//frappe.require("assets/erpnext/js/financial_statements.js", function() {
//	frappe.query_reports["Balance Sheet"] = erpnext.financial_statements;
//
//	frappe.query_reports["Balance Sheet"]["filters"].push({
//		"fieldname": "accumulated_values",
//		"label": __("Accumulated Values"),
//		"fieldtype": "Check",
//		"default": 1
//	});
//});

