## -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
##############################################################################

import string
from odoo import fields, models, api, _
from odoo import SUPERUSER_ID
from datetime import datetime, timedelta
from odoo.exceptions import UserError
class website_deals_offers(models.Model):
    _name='website.deals.offers'


    @api.model
    def default_pricelist_on_deals(self):
        pricelist_deals = self.env['product.pricelist'].search([], limit=1, order="id desc")
        return pricelist_deals    
        
        
    name  =  fields.Char('Deals Name')
    title = fields.Char('Deals Title')
    start_date = fields.Datetime(string='Start Date', required=True)
    end_date = fields.Datetime(string='End Date', required=True)
    
    offers_pricelist = fields.Many2one('product.pricelist', string='Pricelist', default=default_pricelist_on_deals, required=True)
    offers_products = fields.One2many('product.pricelist.item', 'offers_pricelist_id', string='product Pricelist')
    description = fields.Text('Description')
    banner = fields.Binary(string="Banner")
    banner_only = fields.Binary(string="Banner")
    show_deals_header = fields.Boolean(string='Show Deals Header', default=True)
    deals_title = fields.Char('Deals Title')
    
    what_to_show = fields.Selection([
        ('banner_only', 'Banner Only'),
        ('products_only', 'Products Only'),
        ('both', 'Both'),
        ], string='What to Display in Deals', default='both')
        
    display_deals_as = fields.Selection([
        ('grid', 'Grid'),
        ('slider', 'Slider'),
        ('attractive', 'Attractive'),
        ], string='How to Display Deals', default='grid')   

    show_deals_message_before_expiry = fields.Boolean(string='Show Deals Message Before Expiry', default=True)
    deals_message_before_expiry = fields.Char('Deals Message Before Expiry')
    
    show_deals_message_after_expiry = fields.Boolean(string='Show Deals Message After Expiry', default=True)     
    deals_message_after_expiry = fields.Char('Deals Message After Expiry')
      
    state = fields.Selection([
        ('draft', 'Draft'),
        ('progress', 'In Progress'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, track_visibility='onchange', default='draft')        



    def button_validate_the_deal(self):
        self.state='progress'      
        
    def cancel_the_deal(self):
        self.state='cancel'  

        
        
class product_pricelist_item(models.Model):
    _inherit='product.pricelist.item'

    offers_pricelist_id = fields.Many2one('website.deals.offers', string='Offers Pricelist')
    prod_image=fields.Binary(related='product_tmpl_id.x_studio_image_variant', string="Image")
    expriy_date=fields.Float(related='product_tmpl_id.qty_available', string="Qty Available")
    qty_available=fields.Char(related='product_tmpl_id.default_code', string="Sku / Barcode")
    cost=fields.Float(related='product_tmpl_id.standard_price', string="Cost")
    sales_price=fields.Float(related='product_tmpl_id.list_price', string="Sale Price")
    discounted_price=fields.Float(string="Discounted Price")
    description_comp=fields.Char(string="Description")
    comp_image=fields.Binary(string="Comp. Image")

    # @api.onchange('sales_price','compute_price','percent_price','fixed_price')
    # def compute_discount(self):
    #     for record in self:
    #         try:
    #             if record["compute_price"] == "percentage" and record.percent_price:
    #                 record["discounted_price"]=record.sales_price-(record.sales_price*(record.percent_price/100))
    #                 record['fixed_price'] = (record.sales_price*(record.percent_price/100))
    #                 #record['fixed_price'] = (100-record.percent_price)*(record.x_studio_sale_price_1)
    #             else:
    #                 record["discounted_price"]=record.fixed_price
    #                 record['percent_price'] = 100-((record.fixed_price/record.sales_price)*100)
    #         except:
    #             pass
    @api.model
    def create(self,vals):
        offers = self.env['website.deals.offers'].search([])
        if offers and 'offers_pricelist_id' in vals:
            deal = self.env['website.deals.offers'].browse(vals['offers_pricelist_id'])
            if deal:
                vals['pricelist_id'] = deal.offers_pricelist.id
                vals['date_start'] = deal.start_date.strftime("%Y-%m-%d")
                vals['date_end'] = deal.end_date.strftime("%Y-%m-%d")
            return super(product_pricelist_item,self).create(vals)
        else:
            res = super(product_pricelist_item,self).create(vals)
            if res.offers_pricelist_id:
                deal = self.env['website.deals.offers'].browse(res.offers_pricelist_id)
                if deal:
                    res.pricelist_id = deal.offers_pricelist.id
                    res.date_start = deal.start_date.strftime("%Y-%m-%d")
                    res.date_end = deal.end_date.strftime("%Y-%m-%d")
            return res
        
class product_pricelist_wizard_item(models.Model):
    _name='wizard.pricelist.deal'

    deals=fields.Many2one('website.deals.offers',string="Select Deals")
    fixed_percentage=fields.Selection([('fixed','Fixed'),('percentage','Percentage')],"Compute Price")
    value=fields.Float("Add Value")
    def wizard_binary(self):
        active_ids = self.env.context.get('active_ids', [])
        for a in active_ids:

            product = self.env['product.template'].browse(a)
            item={
                    'offers_pricelist_id':self.deals.id,
                    'base':'list_price',
                    'product_tmpl_id':product.id,
                    'applied_on':"1_product",
                    'pricelist_id':self.deals.offers_pricelist.id,
                    'date_start':self.deals.start_date.strftime("%Y-%m-%d"),
                    'date_end':self.deals.end_date.strftime("%Y-%m-%d"),
                    'compute_price':"percentage",
                } 
            if self.fixed_percentage=='fixed':
                item['fixed_price']=self.value
                # self.env.cr.execute("INSERT INTO product_pricelist_item(product_tmpl_id,applied_on,pricelist_id,date_start,date_end,compute_price) \
                # VALUES('"+item["product_tmpl_id"]+"',)")
            elif self.fixed_percentage == 'percentage':
                item['percent_price']=self.value            
            self.env['product.pricelist.item'].create(item)
        
