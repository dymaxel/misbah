# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleCustom(WebsiteSale):

    def _get_search_domain(self, search, category, attrib_values, search_in_description=True):
        res = super(WebsiteSaleCustom, self)._get_search_domain(
            search, category, attrib_values, search_in_description=True)
        if request.website.show_stock_notification and request.website.exclude_outof_stock_product:
            res.append(('qty_available', '>', 0))
        return res


class WebsiteShopProductVariant(http.Controller):

    @http.route(['/product/shop_product_var_stock'], type='json', auth="public", methods=['POST'], website=True)
    def shop_variant_stock(self, **post):
        if post.get('product_id', False):
            if request.website.show_stock_notification:  # if notification set to True

                product_search = request.env['product.product'].sudo().search(
                    [('id', '=', post.get('product_id'))], limit=1)
                # individual for product if allow to show stock
                if product_search and (product_search.type == 'product') and (not product_search.product_tmpl_id.hide_product_stock):
                    if request.website.show_only_left_qty_notification:
                        if request.website.show_left_product_qty >= product_search.qty_available:
                            if product_search.qty_available > 0:  # In Stock
                                if request.website.show_product_qty:  # if show quantity
                                    return product_search.qty_available
                                else:  # does not show quantity
                                    return -2
                            else:  # Out Of Stock
                                return 0
                        else:
                            return -3
                    else:
                        if product_search.qty_available > 0:  # In Stock
                            if request.website.show_product_qty:  # if show quantity
                                return product_search.qty_available
                            else:  # does not show quantity
                                return -2
                        else:  # Out Of Stock
                            return 0

        return -1  # Remain as it is
