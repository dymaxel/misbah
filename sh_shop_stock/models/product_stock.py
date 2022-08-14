# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

import datetime
import locale
import webbrowser
from odoo import api, fields, models, SUPERUSER_ID, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError, ValidationError, Warning
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, float_compare
from dateutil.relativedelta import relativedelta
from itertools import groupby
from operator import itemgetter
from functools import partial
from odoo.tools.misc import formatLang
import base64
import html2text
import json
from datetime import datetime, timedelta


class Website(models.Model):
    _inherit = 'website'

    show_stock_notification = fields.Boolean(
        string="Show Stock Notification?", default=False)
    show_product_qty = fields.Boolean(
        string="Show Available Qty?", default=False)
    show_only_left_qty_notification = fields.Boolean(
        string="Show Only Left Quantity ?", default=False)
    show_left_product_qty = fields.Float(string="Only Left Quantity")
    exclude_outof_stock_product = fields.Boolean(
        string="Exclude Out Of Stock Product")


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    show_stock_notification = fields.Boolean(
        related="website_id.show_stock_notification", string="Show Stock Notification?", readonly=False)
    show_product_qty = fields.Boolean(
        related="website_id.show_product_qty", string="Show Available Qty?", readonly=False)
    show_only_left_qty_notification = fields.Boolean(
        related="website_id.show_only_left_qty_notification", string="Enable Show Only Left Quantity ?", readonly=False)
    show_left_product_qty = fields.Float(
        related="website_id.show_left_product_qty", string="Show Only Left Quantity?", readonly=False)
    exclude_outof_stock_product = fields.Boolean(
        related="website_id.exclude_outof_stock_product", readonly=False, string="Exclude Out Of Stock Product")


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    new_expiry=fields.Char(string="New Expiry")
    def _compute_expiry(self):
        
        for rec in self:
            rec.expiry_lot_date =False
            expiry_comp='N/A'
            for variant in rec.product_variant_ids:
                quant_ids = self.env['stock.quant'].search([('product_id','=',variant.id),('quantity','>',0)])
                lot_ids = self.env['stock.production.lot'].search([('id','in',quant_ids.lot_id.ids),('x_studio_datecode_expiry','!=',False)],order='create_date asc')
                # expiry = min(list(lot_ids.expiration_date))
                if lot_ids:
                    date_prev=True
                    for lot in lot_ids:
                        if date_prev == True or date_prev < lot.create_date:
                            date_prev=lot.create_date
                            expiry_comp=lot.x_studio_datecode_expiry
            rec.expiry_lot_date = expiry_comp
		

    hide_product_stock = fields.Boolean("Hide Product Stock Status?")
    upc = fields.Char("UPC")
    case_barcode = fields.Char("Case Barcode")
    case_upc = fields.Char("Case UPC")
    expiry_lot_date = fields.Char("Expiry Lot Date", compute="_compute_expiry")
    min_qty = fields.Float("Minimum Order Qty")
    hide_product_stock = fields.Boolean("Hide Product Stock Status?")
    prod_templ = fields.Boolean(
        "Compute Product Template", compute="_compute_product_template")
    bilingual_frenchlabel = fields.Selection([
		('french', 'French Label'),
		('bilingual', 'Bilingual'),
	], string='Has Label', default='')
    
    def _compute_product_template(self):
        self.prod_templ = True


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _compute_expiry(self):
        for rec in self:
            expiry_comp='N/A'
            rec.expiry_lot_date = False
            quant_ids = self.env['stock.quant'].search([('product_id','=',rec.id),('quantity','>',0)])
            lot_ids = self.env['stock.production.lot'].search([('id','in',quant_ids.lot_id.ids),('x_studio_datecode_expiry','!=',False)], order='create_date asc')
            # expiry = min(list(lot_ids.expiration_date))
            if lot_ids:
                date_prev=True
                for lot in lot_ids:
                    if date_prev == True or date_prev < lot.create_date:
                        date_prev=lot.create_date
                        expiry_comp=lot.x_studio_datecode_expiry
            rec.expiry_lot_date = expiry_comp


    expiry_lot_date = fields.Char("Expiry Lot Date", compute="_compute_expiry")
    prod_templ = fields.Boolean(
        "Compute Product Variant", compute="_compute_product_variant")

    def _compute_product_variant(self):
        self.prod_templ = False
