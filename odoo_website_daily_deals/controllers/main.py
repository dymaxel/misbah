# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
##############################################################################

from odoo import fields ,SUPERUSER_ID, http, tools, _
from odoo.http import request
from odoo.exceptions import UserError
from datetime import datetime
import base64


class OdooWebsiteDealsOffers(http.Controller):
    @http.route('/download_deals_catalog', type="http", auth="public", website=True, methods=['GET', 'POST'])
    def download_catalog(self, **kw):
        if request.httprequest.method == 'POST':
            product_list=[]
            deals=request.env['website.deals.offers'].search([])
            discounted_price=[]
            actual_price=[]
            descriptions=[]
            compImages=[]
            for d in deals:
                price_list=request.env['product.pricelist'].search([('id','=',d.offers_pricelist.id)])
                price_list_product=request.env['product.pricelist.item'].search([
                    ('pricelist_id','=',price_list.id),
                    ('applied_on','=','1_product')])
                for p in price_list_product:
                    descriptions.append(p.description_comp)
                    product_list.append(p.product_tmpl_id.product_variant_ids.id)
                    actual_price.append(p.sales_price)
                    compImages.append(p.comp_image)
                    if p.compute_price=="fixed":
                        discounted_price.append(p.fixed_price)
                    elif p.compute_price=="percentage":
                        discounted_price.append(p.discounted_price)
                    else:
                        discounted_price.append(False)
                    
            datas = {
                'id': 5, 'catalog_type': 'product', 'product_ids': product_list, 'category_ids': [],
                'price': True,'disc_price': discounted_price ,'deal_descriptions':descriptions,'comp_images':compImages,'actual_price':actual_price, 'pricelist_id': (price_list.id, price_list.name), 'image': True,
                'image_size': 'medium', 'description': True, 'product_link': True, 'style': kw['style'],
                'int_ref': True, 'style_box': '2', 'break_page': False, 'break_page_after_products': 1,
                'on_hand': True, 'currency_id': (2, 'USD'),
                '__last_update': datetime(2021, 12, 16, 17, 43, 54, 460597),
                'display_name': 'product.catalog.wizard,5', 'create_uid': (2, 'Mitchell Admin'),
                'create_date': datetime(2021, 12, 16, 17, 43, 54, 460597),
                'write_uid': (2, 'Mitchell Admin'),
                'write_date': datetime(2021, 12, 16, 17, 43, 54, 460597)
                    }   
            pr=request.env['product.product'].search([('id','=',product_list[0])])
            # raise UserError(str(pr.combination_info)+" : "+str(pr.list_price))
            html = request.env.ref('sh_product_catalog_generator.product_catalog_report_action')._render(1, data=datas)

            categ_list = []
            catalog_type = 'product'
            product_ids = request.env['product.product'].search([])
            if catalog_type == 'product':
                for product in product_ids:
                    if product.categ_id.id not in categ_list:
                        categ_list.append(product.categ_id.id)

            catalog_id = request.env['product.catalog'].sudo().create({
                'name': 'Product Catalog.pdf',
                'categories': [(6, 0, categ_list)],
            })
            b64_pdf = base64.b64encode(html[0])
            request.env['ir.attachment'].sudo().create({
                'name': 'Product Catalog.pdf',
                'type': 'binary',
                'datas': b64_pdf,
                'res_model': 'product.catalog',
                'res_id': str(catalog_id.id),
            })
            catalog_id.sudo().write({
                'store_fname': 'Product Catalog.pdf',
                'datas': b64_pdf,
            })
            cr, uid, context = request.cr, 2, request.context
            qweb_pdf = request.env.ref('sh_product_catalog_generator.product_catalog_report_action').report_action([],
                                                                                                                   data=datas)
            pdf, _ = request.env.ref('sh_product_catalog_generator.product_catalog_report_action').with_user(
                SUPERUSER_ID)._render_qweb_pdf([1], datas)
            pdfhttpheaders = [('Content-Type', 'application/pdf'),('Content-Disposition','attachment; filename="catalog.pdf"'), ('Content-Length', u'%s' % len(pdf))]
            
            return request.make_response(pdf, headers=pdfhttpheaders)

    # deals_offers Menu
    @http.route(['/deals'], type='http', auth="user", website=True)
    def deals(self, page=0, category=None, search='', **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry


        pricelist_context = dict(request.env.context)
        pricelist = False
        if not pricelist_context.get('pricelist'):
            pricelist = request.website.get_current_pricelist()
            pricelist_context['pricelist'] = pricelist.id
        else:
            pricelist = request.env['product.pricelist'].browse(pricelist_context['pricelist'])

        request.context = dict(request.context, pricelist=pricelist.id, partner=request.env.user.partner_id)
        from_currency = request.env.user.company_id.currency_id
        to_currency = pricelist.currency_id
        compute_currency = lambda price: from_currency._convert(price, to_currency, request.env.user.company_id, fields.Date.today())

        values = {
            'compute_currency': compute_currency,
            'pricelist_context':pricelist_context,
            'pricelist' : pricelist
            }
        return request.render("odoo_website_daily_deals.deals",values)



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
