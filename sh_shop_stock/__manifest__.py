# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Product Stock Alert in shop",
    "author": "Softhealer Technologies",
    "support": "support@softhealer.com",
    "website": "https://www.softhealer.com",
    "category": "Website",
    "summary": "Stock Information In Stock Page, Stock Detail Module, Current Status Of Stock App, Display Stock Quantity, Warehouse alert, Inventory Website, Stock Website Odoo",
    "description": """
If you want to display a current status of product stock in your website, So you can do easily by using "Stock Information in Shop page" module.using this module you can notifying the user if product is out of stock, few quantity left etc.
 Stock Information In Stock Page Odoo.
 Display Current Status Of Stock Module, Feature Of Show  Detail Stock & Quantity Of Stock, Display Stock Information Odoo.
 Stock Detail Module, Current Status Of Stock App, Display Stock Quantity Odoo.
""",
    "version": "14.0.1",
    "depends": [
        'website_sale',
        'stock'
    ],
    "data": [
        'views/website_config_settings.xml',
        'views/product_stock.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            "/sh_shop_stock/static/src/js/shop_variant_stock.js"
        ],
    },
    "images": ['static/description/background.png', ],
    "live_test_url": "https://www.youtube.com/watch?v=XbJ9Erp1850&feature=youtu.be",
    "license": "OPL-1",
    "auto_install": False,
    "application": True,
    "installable": True,
    "price": 25,
    "currency": "EUR"
}
