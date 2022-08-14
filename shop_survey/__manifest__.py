# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Shop Survey",
    "author": "Softhealer Technologies",
    "support": "support@softhealer.com",
    "website": "https://www.softhealer.com",
    "category": "Website",
    "summary": "",
    "description": """
""",
    "version": "15.0.1",
    "depends": [
        'website','survey',
    ],

    "data": [
        'views/survey_template.xml',
        'views/header_menu_custom.xml',
    ],

    'assets': {
        'web.assets_frontend': [
            'shop_survey/static/src/scss/survey.scss',
        ],
    },

    "images": ['', ],
    "live_test_url": "https://www.youtube.com/watch?v=XbJ9Erp1850&feature=youtu.be",
    "license": "OPL-1",
    "auto_install": False,
    "application": True,
    "installable": True,

}
