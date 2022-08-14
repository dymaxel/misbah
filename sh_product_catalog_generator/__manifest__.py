# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Product Catalog Generator",

    "author": "Softhealer Technologies",

    "support": "support@softhealer.com",

    "website": "https://www.softhealer.com",

    "category": "Extra Tools",

    "license": "OPL-1",

    "summary": "Create Product Catalogue, Custom Product Catalog App, Make Own Product Catalog, Product Catalogue Module, Customize Product Catalogue, Product Catalog Template, Design Product Catalog, Product Catalog Management, Product Catalogue Builder Odoo",

    "description": """Do you want to represent products in multiple catalogs? Do you want different catalog styles? so you are at the right place. This module helps you to customize the product catalog with the custom style. Here you can design your catalog with catalog type, catalog styles, image option with sizes, box per row, page break, show/hide price, show/hide description, show/hide product link, show/hide internal reference. You can develop your own catalog using this different customization. You can send the product catalog by email. We provide security groups for the product catalog. Generate Product Catalog Odoo, Create Custom Product Catalog, Make Own Product Catalog, Product Catalogue Module, Customize Product Catalogue, Product Catalog Template, Design Product Catalog, Develop Product Catalogue, Product Catalog Management, Product Catalogue Builder Odoo, Create Product Catalogue, Custom Product Catalog App, Make Own Product Catalog, Product Catalogue Module, Customize Product Catalogue, Product Catalog Template, Design Product Catalog, Develop Product Catalogue, Product Catalog Management, Product Catalogue Builder Odoo""",

    "version": "15.0.10",

    "depends": [
        'sale_management',
        'product',
        'website_sale',
        'utm'
    ],

    "data": [
        'security/product_catalog_security_security.xml',
        'security/ir.model.access.csv',
        'data/product_catalog_email_data.xml',
        'views/product_catalog_generated_view.xml',
        'wizard/generate_product_catalog_wizard_view.xml',
        'views/product_catalog_report_template.xml',
        'views/website_catalog.xml'
    ],

    "images": ['static/description/background.png', ],
    "live_test_url": "https://youtu.be/p-ZjK6qRWB8",
    "auto_install": False,
    "application": True,
    "installable": True,
    "price": "60",
    "currency": "EUR",
    'assets': {
        'web.assets_frontend': [
            'sh_product_catalog_generator/static/catalog.js'
        ],
    },
}
