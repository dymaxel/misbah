# Copyright (C) Softhealer Technologies.

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    multi_website_moq = fields.Boolean("MOQ for Multi Website?", default=False)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    multi_website_moq = fields.Boolean(
        related="company_id.multi_website_moq", string="MOQ for Multi Website?", readonly=False)
