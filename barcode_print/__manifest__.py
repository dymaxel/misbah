# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Print Barcode',
    'version': '14.0.1.1.2',
    'category': 'Extra Tools',
    'summary': 'Custom Design for sales Application',
    'sequence': '4',
    'author': 'Shams Ur Rehman',
    'maintainer': 'Huzaifa',
    'depends': ['sale'],
    'demo': [],
    'data': [
        'security/ir.model.access.csv',
        
        'views/barcode_report_pdf.xml',
        'views/barcode_form.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
