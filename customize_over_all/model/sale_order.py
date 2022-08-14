from odoo import api, fields, models, SUPERUSER_ID, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def write(self, values):
        if values.get('commitment_date'):
            self.picking_ids.filtered(lambda x: x.state not in ('done', 'cancel')).with_context(from_sale=True).write({'force_date_deadline': fields.Datetime.to_datetime(values.get('commitment_date'))})
        return super(SaleOrder, self).write(values)
