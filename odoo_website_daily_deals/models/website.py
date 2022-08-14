# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
##############################################################################

from odoo import fields, models, api, _
from odoo import SUPERUSER_ID
from datetime import date, time, datetime, timedelta

class websiteinherit(models.Model):
    _inherit = 'website'

    def _get_offers_products_cat(self):  
        offers_ids=self.env['website.deals.offers'].search([('state', '=', 'progress')])
        categ_ids=self.env['product.category'].search([])

        deal_cat_ids = []

        if offers_ids:
            for offer in offers_ids:
                DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
                now = str(datetime.now().replace(microsecond=0,second=0))
                current_time = datetime.strptime(now, DATETIME_FORMAT)
                start_date_offer = offer.start_date
                end_date_offer = offer.end_date
                if start_date_offer <= current_time and current_time <= end_date_offer:
                    for product_cat in offer.offers_products:
                        if product_cat.applied_on == '2_product_category':
                            deal_cat_ids.append(product_cat.categ_id.id)
                        if product_cat.applied_on == '3_global':
                            for cat in categ_ids:
                                deal_cat_ids.append(cat.id)
                        
            return deal_cat_ids

    def _get_offers_products_tmpl(self):  
        offers_ids=self.env['website.deals.offers'].search([('state', '=', 'progress')])
        categ_ids=self.env['product.category'].search([])

        deal_tmpl_ids = []

        if offers_ids:
            for offer in offers_ids:
                DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
                now = str(datetime.now().replace(microsecond=0,second=0))
                current_time = datetime.strptime(now, DATETIME_FORMAT)
                start_date_offer = offer.start_date
                end_date_offer = offer.end_date
                if start_date_offer <= current_time and current_time <= end_date_offer:
                    for product_cat in offer.offers_products:
                        if product_cat.applied_on == '1_product':
                            deal_tmpl_ids.append(product_cat.product_tmpl_id.id)
                        if product_cat.applied_on == '0_product_variant':
                            deal_tmpl_ids.append(product_cat.product_id.product_tmpl_id.id)
            
            return deal_tmpl_ids
    
    def get_deals_offers(self):  
        offers_ids=self.env['website.deals.offers'].search([('state', '=', 'progress')])

        deal_ids = []

        if offers_ids:
            for offer in offers_ids:
                DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
                now = str(datetime.now().replace(microsecond=0,second=0))
                current_time = datetime.strptime(now, DATETIME_FORMAT)
                start_date_offer = offer.start_date
                end_date_offer = offer.end_date
                if start_date_offer <= current_time and current_time <= end_date_offer:
                    deal_ids.append(offer)
            
            
            return deal_ids


    def get_current_pricelist(self):
        values = super(websiteinherit, self).get_current_pricelist()
        pricelist_deals = self.env['product.pricelist'].search([], limit=1, order="id desc")
        offers_ids=self.env['website.deals.offers'].search([('state', '=', 'progress')])
        if offers_ids:
            for i in offers_ids:
                for j in i.offers_products:
                    if i.end_date and i.end_date > datetime.now():
                        if j.date_end and j.date_end>datetime.now():
                            if i.offers_pricelist.id == pricelist_deals.id:
                                values= pricelist_deals
        else:
            values = super(websiteinherit, self).get_current_pricelist()
                
        return values

class ProductTemplate(models.Model):
    _inherit = ["product.template"]

    website_price = fields.Float('Website price', compute='_website_price', digits='Product Price')               

    def _website_price(self):
        current_website = self.env['website'].get_current_website()
        for template in self.with_context(website_id=current_website.id):
            res = template._get_combination_info()
            template.website_price = res.get('price')
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:    