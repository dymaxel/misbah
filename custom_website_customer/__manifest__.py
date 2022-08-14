# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Website Customer',
    'version': '15.0.3',
    'category': 'Sale',
    'summary': 'Module for Odoo Reporting',
    'sequence': '4',
    'author': 'Shaikh Huzaifa',
    'maintainer': 'Zeeshan',
    'depends': ['base','web','website','auth_signup','product','smile_audit', 'website_sale'],
    'demo': [],
    'data': [
        'security/ir.model.access.csv',
        'data/web_customer_type_data.xml',
        'main.xml',
        'views/customer_form.xml',
        'views/res_partner_form_inherit.xml',
        'views/product_packaging_form_inherit.xml',

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': [],
    'assets': {
        'web.assets_frontend': [
            'custom_website_customer/static/customer.js',
            'custom_website_customer/static/website_sale_note.js'
        ],
    },
}
