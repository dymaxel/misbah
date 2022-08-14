# Part of Softhealer Technologies.

from . import models
from . import controllers
from odoo import api,SUPERUSER_ID

def add_packaging_qty_website(cr,registry):
    env=api.Environment(cr,SUPERUSER_ID,{})
    env['product.template'].productloop()