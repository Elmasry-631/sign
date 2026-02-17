{
    "name": "Sale Signature Flow",
    "version": "19.0.1.0.0",
    "summary": "Quotation and sales order signature workflow",
    "license": "LGPL-3",
    "author": "Custom",
    "depends": ["sale", "contacts"],
    "data": [
        "security/ir.model.access.csv",
        "views/res_config_settings_views.xml",
        "views/sale_order_views.xml",
    ],
    "installable": True,
    "application": False,
}
