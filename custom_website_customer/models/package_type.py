from odoo import models, fields


class WebCustomerType(models.Model):
    _name = 'web.customer.type'

    name = fields.Char("Customer Type")

class ProductPackage(models.Model):
    _inherit = "product.packaging"

    #customer_type = fields.Selection([("Wholesaler", "Wholesaler"), ("Retailer", "Retailer"), ("Consumer", "Consumer")], default="Wholesaler")
    # customer_type = fields.Many2many('web.customer.type','customer_type_prod_pkgs_rel','pkg_id','user_type_id',string='Customer Type')
    customer_type_ids = fields.Many2many('web.customer.type','customer_type_prod_pkgs_rel', string='Customer Type')

