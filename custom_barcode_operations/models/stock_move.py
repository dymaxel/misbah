from odoo import api,models, fields

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'


    notes = fields.Char('Notes')
    #
    website_image_url = fields.Char(string='Image URL',related='product_id.website_image_url')
    case_barcode = fields.Char('Case Product Barcode',related='move_id.product_packaging_id.barcode')
    # case_barcode = fields.Char('Case Product Barcode',related='product_id.product_tmpl_id.case_barcode')
    pkg_name = fields.Char('Package Name',related='move_id.product_packaging_id.name')
    demand_qty_packages = fields.Integer('Packages Demand',compute="_compute_packages")
    location_name = fields.Char('location',related='location_id.complete_name')

    @api.depends('move_id.product_packaging_id.qty','move_id.product_qty')
    def _compute_packages(self):
        for rec in self:
            if rec.move_id.product_packaging_id.qty and rec.move_id.product_qty:
                rec.demand_qty_packages = int(rec.move_id.product_qty / rec.move_id.product_packaging_id.qty)
            else:
                rec.demand_qty_packages = False



    def _get_fields_stock_barcode(self):
        return [
            'product_id',
            'location_id',
            'location_dest_id',
            'qty_done',
            'display_name',
            'product_uom_qty',
            'product_uom_id',
            'product_barcode',
            'owner_id',
            'lot_id',
            'lot_name',
            'package_id',
            'result_package_id',
            'dummy_id',
            'case_barcode',
            'website_image_url',
            'demand_qty_packages',
            'pkg_name',
            'location_name',
            'notes'
        ]