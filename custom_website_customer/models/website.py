from odoo import models, fields

class Website(models.Model):
    _inherit = "website"

    def get_customer_types(self):
        customer_types = self.env['web.customer.type'].sudo().search([])
        return customer_types

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    internal_notes = fields.Text('Website Sale Note')
