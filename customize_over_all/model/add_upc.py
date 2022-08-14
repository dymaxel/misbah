from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from random import  randint
class GenerateUpc(models.Model):
    _inherit='product.template'

    def generateupc(self):
        if not self.barcode:
            rnd = randint(1000000000000, 9999999999999)
            all_upcs=self.env['product.template'].search([])
            checkrand=True
            while(checkrand):
                checkalrady=False
                for au in all_upcs:
                    if str(rnd) == au.upc:
                        checkalrady=True
                if checkalrady:
                    rnd = randint(1000000000000, 9999999999999)
                else:
                    self.upc = str(rnd)
                    self.barcode = str(rnd)
                    checkrand=False
                    break
