# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict

from odoo import http, _
from odoo.http import request
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)


class StockBarcodeController(http.Controller):

    @http.route('/stock_barcode/save_barcode_scan_time', type='json', auth='user')
    def save_barcode_data(self, model, res_id, barcode):
        product = request.env['product.product'].sudo().search([('barcode','=',barcode)])
        description = "This Barcode is for the Product "
        if not product:
            product = request.env['product.packaging'].sudo().search([('barcode','=',barcode)]).product_id
            description = "This Barcode is for the Case "
        if not product:
            product = request.env['product.template'].sudo().search([('case_barcode','=',barcode)])

        if product:
            product_id = product.id
            product_name = product.name
        if not product:
            product_id = ''
            description = "This Product does not exist or you select wrong product"
        if not res_id:
            _logger.exception("res_id to log or save scan time not found")
            return False
        target_record = request.env[model].browse(res_id)
        dt = datetime.utcnow()
        try:
            vals = {'product':product_name, 'barcode': barcode, 'description':description, 'scan_date_time': dt}
            field_to_update = ''
            if model=='stock.picking.batch':
                vals.update(stock_picking_batch_id=res_id)
                field_to_update = 'batch_barcode_scan_time'
            else:
                vals.update(stock_picking_id=res_id)
                field_to_update = 'barcode_scan_time'

            target_record.write({field_to_update: [(0, 0,vals)]})
        except Exception as e:
            _logger.error('An error occured while writing scan time: %s', e.args[0])

        _logger.info("Record against picking id=%s last scanned at %s"%(res_id,dt))
        return True
