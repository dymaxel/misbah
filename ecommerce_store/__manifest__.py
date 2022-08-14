# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Select Customer on Checkout',
    'category': 'Website/Website',
    'sequence': 50,
    'summary': 'Sell your products online',
    'website': 'https://www.odoo.com/app/ecommerce',
    'version': '1.2',
    'description': "",
    'depends': ['base', 'crm', 'stock_barcode', 'website_sale','website_mass_mailing'],
    'data': [
        'security/ir.model.access.csv',
        'data/mail_template_data.xml',
        'views/menu_iframe.xml',
        'views/shop_payment.xml',

    ],
    'demo': [
    ],
    'installable': True,
    'application': True,

    'assets': {
        'web.assets_frontend': [
            'ecommerce_store/static/src/js/checkout_customers.js',
            'ecommerce_store/static/src/scss/custom_shop.scss',
            "ecommerce_store/static/src/css/custom.css",
            'ecommerce_store/static/src/js/checkout_customers.js',
            'ecommerce_store/static/src/js/update_weekdays.js',
            'ecommerce_store/static/src/js/close_video.js'
        ],

        'web.assets_qweb': [
            # 'ecommerce_store/static/src/legacy/xml/custom_barcode_header.xml',
        ],
        'web._assets_common_styles': [
            'ecommerce_store/static/src/legacy/scss/custom_barcode_header.scss',
        ]
    },
    'license': 'LGPL-3',
}
