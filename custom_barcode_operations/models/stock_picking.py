# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class StockPicking(models.Model):
    _name = 'stock.picking'
    _inherit = ['stock.picking', 'barcodes.barcode_events_mixin']

    barcode_scan_time = fields.One2many('barcode.scan.timings', 'stock_picking_id', 'Barcode Scan Timings',
                                        readonly=True)


class BarcodeScanTimings(models.Model):
    _name = 'barcode.scan.timings'

    stock_picking_id = fields.Many2one('stock.picking')
    stock_picking_batch_id = fields.Many2one('stock.picking.batch')
    scan_date_time = fields.Datetime('Scan Time')
    product = fields.Char(string="Product Name")
    barcode = fields.Char(string="Barcode", help="ID used for product identification.")
    description = fields.Char("Description")


class StockPickingBatch(models.Model):
    _name = 'stock.picking.batch'
    _inherit = ['stock.picking.batch', 'barcodes.barcode_events_mixin']

    batch_barcode_scan_time = fields.One2many('barcode.scan.timings', 'stock_picking_batch_id',
                                              'Batch Barcode Scan Timings', readonly=True)
