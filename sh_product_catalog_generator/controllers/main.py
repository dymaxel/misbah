from odoo import http
from odoo.http import request
from odoo.exceptions import UserError
from odoo import fields, http, SUPERUSER_ID, tools, _
import base64
import datetime
class DownloadCustomer(http.Controller):
    @http.route('/download_catalog',type="http",auth="public",website=True,methods=['GET', 'POST'])
    def download_catalog(self,**kw):
        if request.httprequest.method == 'POST':
            
            product_cats_dict={}
            prodcat=request.env['product.category'].search([('name','!=',["All","Expenses","Saleable"]),('parent_id', '=',False)])
            
            for c in prodcat:
                
                product_cats=[]
                product_cats.append(c.id)
                for c2 in request.env['product.category'].search([('parent_id', '=', c.id)]):
                    product_cats.append(c2.id)
                    
                    for c3 in request.env['product.category'].search([('parent_id', '=', c2.id)]):
                        
                        product_cats.append(c3.id)
                        
                product_cats_dict[c.id]=product_cats
                
            datas={}
            pricelistobj=request.env['product.pricelist'].search([('id','=',int(kw['product_pricelist']))])
            if kw['style'] == 'style_5':
              datas = {'id': 5, 'catalog_type': 'category', 'product_ids': [], 'category_ids': product_cats_dict, 'price': True, 'pricelist_id':(pricelistobj.id,pricelistobj.name) , 'image': True, 'image_size': 'large', 'description': True, 'on_hand': True , 'product_link': True, 'style': kw['style'], 'int_ref': True, 'style_box': '2', 'break_page': True, 'break_page_after_products': 2,'on_hand':True, 'currency_id': (2, 'USD'), '__last_update': datetime.datetime(2021, 12, 16, 17, 43, 54, 460597), 'display_name': 'product.catalog.wizard,5', 'create_uid': (2, 'Mitchell Admin'), 'create_date': datetime.datetime(2021, 12, 16, 17, 43, 54, 460597), 'write_uid': (2, 'Mitchell Admin'), 'write_date': datetime.datetime(2021, 12, 16, 17, 43, 54, 460597)}
            else:
              datas = {'id': 5, 'catalog_type': 'category', 'product_ids': [], 'category_ids': product_cats_dict, 'price': True, 'pricelist_id':(pricelistobj.id,pricelistobj.name) , 'image': True, 'image_size': 'medium', 'description': True, 'on_hand': True , 'product_link': True, 'style': kw['style'], 'int_ref': True, 'style_box': '2', 'break_page': True, 'break_page_after_products': 4,'on_hand':True, 'currency_id': (2, 'USD'), '__last_update': datetime.datetime(2021, 12, 16, 17, 43, 54, 460597), 'display_name': 'product.catalog.wizard,5', 'create_uid': (2, 'Mitchell Admin'), 'create_date': datetime.datetime(2021, 12, 16, 17, 43, 54, 460597), 'write_uid': (2, 'Mitchell Admin'), 'write_date': datetime.datetime(2021, 12, 16, 17, 43, 54, 460597)}
            html = request.env.ref('sh_product_catalog_generator.product_catalog_report_action')._render(1, data=datas)
            
            # categ_list = []
            # catalog_type = 'category'
            # product_ids = request.env['product.product'].search([])
            # if catalog_type == 'product':
            #     for product in product_ids:
            #         if product.categ_id.id not in categ_list:
            #             categ_list.append(product.categ_id.id)
            
            # elif catalog_type == 'category':
            #     for category in prodcat:
            #         if category.id not in product_cats:
            #             categ_list.append(category.id)

            catalog_id = request.env['product.catalog'].sudo().create({
                'name': 'Product Catalog.pdf',
                'categories': [(6, 0, product_cats)],
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
            qweb_pdf= request.env.ref('sh_product_catalog_generator.product_catalog_report_action').report_action([], data=datas)
            pdf, _ = request.env.ref('sh_product_catalog_generator.product_catalog_report_action').with_user(SUPERUSER_ID)._render_qweb_pdf([1],datas)
            pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', u'%s' % len(pdf))]
            return request.make_response(pdf, headers=pdfhttpheaders)
        else:
            id_type= request.env.user.partner_id.Customer_Type.id
            pricelist = http.request.env['product.pricelist'].sudo().search([('x_studio_pricelist_type','=',id_type)])
            return http.request.render('sh_product_catalog_generator.website_catalog_down',{'pricelist':pricelist})
