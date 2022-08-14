# Part of Softhealer Technologies.

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError, Warning
import math


class ShProductTemplate(models.Model):
    _inherit = 'product.template'

    def productloop(self):
        products = self.env['product.template'].search([])
        for p in products:
            if p.packaging_ids:

                if len(p.packaging_ids.ids)>1:
                    p.sh_increment_qty = str(int(p.packaging_ids[0].qty))
                    moq=p.env['sh.moq.multi.website'].create({
                        'product_id':p.id,
                        'website_id':p.website_id.id,
                        'sh_increment_qty':str(int(p.packaging_ids[0].qty))
                    })
                    print("created: ",moq.sh_increment_qty)
                else:
                    p.sh_increment_qty = str(int(p.packaging_ids.qty))
                    moq = p.env['sh.moq.multi.website'].create({
                        'product_id': p.id,
                        'website_id': p.website_id.id,
                        'sh_increment_qty': str(int(p.packaging_ids.qty))
                    })
                    print("created: ", moq.sh_increment_qty)
            else:
                self.sh_increment_qty =1


    @api.onchange('packaging_ids')
    def productecase(self):
        if self.packaging_ids:
            self.sh_increment_qty = str(int(self.packaging_ids[0].qty))
            moq=self.env['sh.moq.multi.website'].create({
                'product_id':self.id,
                'website_id':self.website_id,
                'sh_increment_qty':str(int(self.packaging_ids[0].qty))
            })
            self.compute="1"
        else:
            self.sh_increment_qty =1
            self.compute = "0"

    compute=fields.Char('Multiples of Quantity',compute=productecase)
    sh_increment_qty = fields.Char('Multiples of Quantity', default='1')
    multi_website_ids = fields.One2many(
        'sh.moq.multi.website', 'product_id', string="Website wise MOQ")
    multi_website_moq = fields.Boolean(
        related="company_id.multi_website_moq", string="MOQ for Multi Website?")


class MOQwebsite(models.Model):
    _name = 'sh.moq.multi.website'
    _description = 'MOQ Multi Website'

    # def _computecase(self):
        # if self.packaging_ids:
        #     self.sh_increment_qty = self.product_id.packaging_ids[0].qty
        # else:
        #     self.sh_increment_qty =1

    # compute = fields.Char('Multiples of Quantity', compute=_computecase)
    product_id = fields.Many2one('product.template', string="Product")
    website_id = fields.Many2one('website', string="Website")
    sh_increment_qty = fields.Char('Multiples of Quantity', default='1')




class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id', 'product_uom_qty')
    def onchange_pro_qty(self):
        if self:
#             raise UserError("AGAYA")
            for rec in self:
                multi_by = int(rec.product_id.sh_increment_qty)
                if rec.product_uom_qty < multi_by:
                    rec.product_uom_qty = multi_by
                    rec.product_packaging_id = rec.product_id.packaging_ids[0].id
                if rec.product_uom_qty > multi_by:
                    if multi_by != 0:
                        devi_value = rec.product_uom_qty/multi_by
                        ceil_value = math.ceil(devi_value)
                        rec.product_uom_qty = ceil_value * multi_by
                        rec.product_packaging_id = rec.product_id.packaging_ids[0].id
