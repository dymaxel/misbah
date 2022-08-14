from odoo import api, fields, models, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'


    dxl_scheduled_date = fields.Datetime('Scheduled Date', compute='_compute_scheduled_date', default=fields.Datetime.now)
    dxl_date_deadline = fields.Datetime(
        "Deadline", compute='_compute_date_deadline', store=True,
        help="Date Promise to the customer on the top level document (SO/PO)")
    date_order = fields.Datetime(related="sale_id.date_order", string='Order Date', store=True)
    force_date_deadline = fields.Datetime(string='Force Deadline', default=fields.Datetime.now)

    def write(self, vals):
        if 'force_date_deadline' in vals and vals.get('force_date_deadline') and not self.env.context.get('from_sale'):
            for picking in self.filtered(lambda x: x.sale_id):
                picking.sale_id.write({'commitment_date': vals.get('force_date_deadline')})
        if 'scheduled_date' in vals and vals.get('scheduled_date'):
            for picking in self.filtered(lambda x: x.sale_id):
                picking.sale_id.picking_ids.filtered(lambda x: x.state not in ('done', 'cancel')).mapped('move_lines').write({'date': vals.get('scheduled_date')})
        return super(StockPicking, self).write(vals)

    @api.depends('move_lines.date_deadline', 'move_type')
    def _compute_date_deadline(self):
        for picking in self:
            if picking.move_type == 'direct':
                picking.date_deadline = min(picking.move_lines.filtered('date_deadline').mapped('date_deadline'), default=False)
                picking.dxl_date_deadline = min(picking.move_lines.filtered('date_deadline').mapped('date_deadline'), default=False)
            else:
                picking.date_deadline = max(picking.move_lines.filtered('date_deadline').mapped('date_deadline'), default=False)
                picking.dxl_date_deadline = max(picking.move_lines.filtered('date_deadline').mapped('date_deadline'), default=False)

    @api.depends('move_lines.state', 'move_lines.date', 'move_type')
    def _compute_scheduled_date(self):
        for picking in self:
            moves_dates = picking.move_lines.filtered(lambda move: move.state not in ('done', 'cancel')).mapped('date')
            if picking.move_type == 'direct':
                picking.scheduled_date = min(moves_dates, default=picking.scheduled_date or fields.Datetime.now())
                picking.dxl_scheduled_date = min(moves_dates, default=picking.scheduled_date or fields.Datetime.now())
            else:
                picking.scheduled_date = max(moves_dates, default=picking.scheduled_date or fields.Datetime.now())
                picking.dxl_scheduled_date = max(moves_dates, default=picking.scheduled_date or fields.Datetime.now())
