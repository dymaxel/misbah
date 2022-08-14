# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Products Custom Fields - Website Sale",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "eCommerce",
    "summary": "Add Product New Fields – E Shop Module, Make Product Dynamic Fields – E Shop, Create Product New Fields – E Commerce App, Assign Custom Fields Odoo. Edit/Update Product Custom Fields – E Commerce Odoo",
    "description": """ Using this module you can add extra fields in your shop. If you want to add some fields for the product in your shop like external reference, created date, Availability warning, product brochure, etc you can do it easily by using this module. you can add custom fields in the shop in one step. You can also set a binary file field so you can set a product brochure, warranty card, etc of product. This module design is very simple and fluent so the user can easily understand and interact with the product properly. Go to website configuration setting and select field in 'Products Custom Fields - Website Sale' which is you want to add in the shop, apply it and cheers!""",
    "version": "15.0.1",
    "depends": [
        "website_sale"
    ],
    "application": True,
    "data": [
        "views/res_config_settings_view.xml",
        "views/website_sale_templates.xml",
    ],
    "images": ["static/description/background.png", ],
    "license": "OPL-1",
    "auto_install": False,
    "installable": True,
    "price": 30,
    "currency": "EUR"
}
