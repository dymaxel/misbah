from email.policy import default
import string
from odoo import models, fields, api, tools, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_is_zero
import datetime as dt

class SaleOrderLine(models.Model):
    _inherit = 'stock.picking'
    
    
    pilot = fields.Integer(string="Pallette",default=1)

    
    def get_data(self):
        list=[]
        for i in range(self.pilot):
            list.append(str(i+1)+" OF "+str(self.pilot))
        # raise UserError(str(order_id))
        if list:
            pass
        else:
            list.append("1/1")
        return list


        