# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
##############################################################################


{
    "name" : "Odoo Website Daily Offers & Deals",
    "version" : "15.0.4",
    "category" : "eCommerce",
    "depends" : ['sale_management','website','website_sale','sh_product_catalog_generator'],
    "author": "BrowseInfo",
    'summary': 'Website Daily Deals and Offers on eCommarce to customer eCommerce Deals website Offers web shop Daily Deals Website Deal of the Day Deals And Flash Sales website promotion Todays best deals website Deals & Offers Website Today Deals website daily offers',
    "description": """
    Website Daily Deals & Offers
    eCommerce Daily Deals & Offers
    Website Deals & Offers
    eCommerce Deals & Offers
    Website Daily Offers & Deals
    eCommerce Daily Offers & Deals
    Daily Deals
    Today's best deals
Website Today's deals
Website Deal of the Day
Website Today Deals
Website best Today Deals
Website best Daily Offers & Deals
Website best Daily Deals
Website offer for today
Website Top Daily Deal
Website Daily Deals Website
Website Daily Deals
webstore daily deal webstore
Website Deals And Flash Sales
Website Flash Sales
website Flash Sales
website promotion website
webshop promotion webshop
webstore promotion webstore

    webshop Daily Deals & Offers webshop
    webshop Daily Deals & Offers webshop
    webshop Deals & Offers webshop
    webshop Deals & Offers webshop
    webshop Daily Offers & Deals webshop
    webshop Daily Offers & Deals webshop
    webshop Daily Deals webshop
    webshop Today's best deals webshop
Website Today's deals website
Website Deal of the Day website
Website Today Deals webshop
Website best Today Deals
Website best Daily Offers & Deals
Website best Daily Deals
Website offer for today
Website Top Daily Deal
Website Daily Deals Website
Website Daily Deals
webstore daily deal webstore
Website Deals And Flash Sales
Website Flash Sales website
webshop Flash Sales webshop


    """,
    "website" : "https://www.browseinfo.in",
    "data": [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/templates/add_pricelist.xml',
        'views/templates/odoo_website_daily_deals.xml',
        'views/templates/deals_offers_views.xml',
    ],
    "auto_install": False,
    "price": 35,
    "currency": 'EUR',
    'license': 'OPL-1',
    'assets': {
        'web.assets_frontend': [
            "/odoo_website_daily_deals/static/src/css/custom.css",
            "/odoo_website_daily_deals/static/src/js/odoo_website_daily_deals_frontend.js",
        ],
    },
    "application": True,
    "installable": True,
    'live_test_url':'https://youtu.be/89J_p3hQSWs',
    "images":['static/description/Banner.png'],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
