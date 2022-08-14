# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleCustom(WebsiteSale):

    # inherit controoler to add quantity direct to press add to cart button from product listing
    @http.route(['/shop/cart/update'], type='http', auth="public", methods=['POST'], website=True, csrf=False)
    def cart_update(self, product_id, add_qty=1, set_qty=0, **kw):
        if add_qty == 1:
            product = request.env['product.product'].sudo().search(
                [('id', '=', product_id)])
            if product.sh_increment_qty != add_qty:
                add_qty = product.sh_increment_qty

        res = super(WebsiteSaleCustom, self).cart_update(
            product_id, add_qty, set_qty, **kw)
        return res
