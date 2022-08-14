# Copyright 2013 Nicolas Bessi (Camptocamp SA)
# Copyright 2014 Agile Business Group (<http://www.agilebg.com>)
# Copyright p2015 Grupo ESOC (<http://www.grupoesoc.es>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 
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

class ResPartner(models.Model):
    """Adds last name and first name; name becomes a stored function field."""

    _inherit = "res.partner"
    Customer_Type = fields.Many2one('web.customer.type')



#     @api.model
#     def create(self, vals):
     
     
#         if 'name' in vals:
#             partner_id = self.env['res.partner'].sudo().search([('name','=',vals['name']),('id','!=',5),('name','!=',''),('company_type','=','company')], limit=1)
#             if partner_id:
#                 if partner_id.user_id:
#                     raise UserError("""Error Name !! Customer/Partner already exist in the database and associated with sales-REP %s"""%(partner_id.user_id.name))
#                 else:
#                     raise UserError("""Error Name !! Customer/Partner already exist in the database %s"""%(partner_id.name))
#         if 'email' in vals:
#             partner_id = self.env['res.partner'].sudo().search([('email','=',vals['email']),('id','!=',5),('email','!=','')], limit=1)
#             if partner_id:
#                 if partner_id.user_id:
#                     raise UserError("""Error Email !! Customer/Partner already exist in the database and associated with sales-REP %s"""%(partner_id.user_id.name))
#                 else:
#                     raise UserError("""Error Email !! Customer/Partner already exist in the database %s"""%(partner_id.name))

#         if 'phone' in vals:
#             partner_id = self.env['res.partner'].sudo().search([('phone','=',vals['phone']),('id','!=',5),('phone','!=','')], limit=1)
#             if partner_id:
#                 if partner_id.user_id:
#                     raise UserError("""Error Phone !! Customer/Partner already exist in the database and associated with sales-REP %s"""%(partner_id.user_id.name))
#                 else:
#                     raise UserError("""Error Phone !! Customer/Partner already exist in the database %s"""%(partner_id.name))

#         if 'street' in vals:
#             partner_id = self.env['res.partner'].sudo().search([('street','=',vals['street']),('id','!=',5),('street','!=','')], limit=1)
#             if partner_id:
#                 if partner_id.user_id:
#                     raise UserError("""Error address !! Customer/Partner already exist in the database and associated with sales-REP %s"""%(partner_id.user_id.name))
#                 else:
#                     raise UserError("""Error address !! Customer/Partner already exist in the database %s"""%(partner_id.name))

#         if 'street2' in vals:         
#             partner_id = self.env['res.partner'].sudo().search([('street2','=',vals['street2']),('id','!=',5),('street2','!=','')], limit=1)
#             if partner_id:
#                 if partner_id.user_id:
#                     raise UserError("""Error address2 !! Customer/Partner already exist in the database and associated with sales-REP %s"""%(partner_id.user_id.name))
#                 else:
#                     raise UserError("""Error address2 !! Customer/Partner already exist in the database %s"""%(partner_id.name))

#         if 'mobile' in vals:
#             partner_id = self.env['res.partner'].sudo().search([('mobile','=',vals['mobile']),('id','!=',5),('mobile','!=','')], limit=1)
#             if partner_id:
#                 if partner_id.user_id:
#                     raise UserError("""Error Mobile !! Customer/Partner already exist in the database and associated with sales-REP %s"""%(partner_id.user_id.name))
#                 else:
#                     raise UserError("""Error Mobile !! Customer/Partner already exist in the database %s"""%(partner_id.name))

#         return super(ResPartner, self).create(vals)



    # def write(self, values):
    #     for rec in self:
    #         res = super(ResPartner, self).write(values)
    #         active_value = values
    #         # raise UserError(str(active_value))
    #         # if 'mobile' in active_value or 'street2' in active_value or 'street' in active_value or 'phone' in active_value or 'email' in active_value:
    #         if 'email' in active_value:
    #             partner_id = self.env['res.partner'].sudo().search([('email','=',active_value['email'].lower())], limit=1)
    #             if partner_id:
    #                 if partner_id.user_id:
    #                     raise UserError("""Error Email !! Customer/Partner already exist in the database and associated with sales-REP %s"""%(partner_id.user_id.name))
    #                 else:
    #                     raise UserError("""Error Email !! Customer/Partner already exist in the database %s"""%(partner_id.name))

    #         if 'phone' in active_value:
    #             partner_id = self.env['res.partner'].sudo().search([('phone','=',active_value['phone'].lower()),], limit=1)
    #             if partner_id:
    #                 if partner_id.user_id:
    #                     raise UserError("""Error Phone !! Customer/Partner already exist in the database and associated with sales-REP %s"""%(partner_id.user_id.name))
    #                 else:
    #                     raise UserError("""Error Phone !! Customer/Partner already exist in the database %s"""%(partner_id.name))

    #         if 'street' in active_value:
    #             partner_id = self.env['res.partner'].sudo().search([('street','=',active_value['street'].lower())], limit=1)
    #             if partner_id:
    #                 if partner_id.user_id:
    #                     raise UserError("""Error address !! Customer/Partner already exist in the database and associated with sales-REP %s"""%(partner_id.user_id.name))
    #                 else:
    #                     raise UserError("""Error address !! Customer/Partner already exist in the database %s"""%(partner_id.name))

    #         if 'street2' in active_value:         
    #             partner_id = self.env['res.partner'].sudo().search([('street2','=',active_value['street2'].lower())], limit=1)
    #             if partner_id:
    #                 if partner_id.user_id:
    #                     raise UserError("""Error address2 !! Customer/Partner already exist in the database and associated with sales-REP %s"""%(partner_id.user_id.name))
    #                 else:
    #                     raise UserError("""Error address2 !! Customer/Partner already exist in the database %s"""%(partner_id.name))

    #         if 'mobile' in active_value:
    #             partner_id = self.env['res.partner'].sudo().search([('mobile','=',active_value['mobile'].lower())], limit=1)
    #             if partner_id:
    #                 if partner_id.user_id:
    #                     raise UserError("""Error Mobile !! Customer/Partner already exist in the database and associated with sales-REP %s"""%(partner_id.user_id.name))
    #                 else:
    #                     raise UserError("""Error Mobile !! Customer/Partner already exist in the database %s"""%(partner_id.name))
    #             return res
