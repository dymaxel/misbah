from tabnanny import check
from odoo import addons
from odoo import http
from odoo.http import request
from odoo.exceptions import UserError
from odoo.addons.website_sale.controllers.main import WebsiteSale

class WebsiteSaleInheritSale(WebsiteSale):

    @http.route()
    def cart_update_json(self, product_id, line_id=None, add_qty=None, set_qty=None, display=True, **kw):
        product_packages = request.env["product.packaging"].sudo().search([('product_id','=',product_id)],order='qty')
#         raise UserError('product_id: '+str(product_id)+'line_id: '+str(line_id)+'add_qty: '+str(add_qty)+'set_qty: '+str(set_qty)+str(type(set_qty)))        
        if line_id:
            add_qty= None
            set_qty= 0
        else:
            sdd_qty=int(float(add_qty))
            
#         raise UserError('product_id: '+str(product_id)+'line_id: '+str(line_id)+'add_qty: '+str(add_qty)+'set_qty: '+str(set_qty)+str(type(set_qty)))
        res = super(WebsiteSaleInheritSale, self).cart_update_json(product_id, line_id, add_qty, set_qty, display, **kw)
        return res



class WebsiteSaleInherit(http.Controller):

    @http.route('/getcustomers', type='json', auth='public')
    def _get_customers_json(self,**search):
        customer_dic=[]
        if 'search' in search:
            search_string = search.get('search')
            obj_partner = request.env['res.partner'].sudo()
            if search_string:

                customer = obj_partner.search(
                    [
                    # ('parent_id','=',False),
                    ('user_id','=',request.env.user.id),
                     "|",('name','ilike',search_string),
                     "|",('email','ilike',search_string),
                     "|",('phone','ilike',search_string),
                     "|",('mobile','ilike',search_string),
                     "|",('street','ilike',search_string),
                        "|",('zip','ilike',search_string),
                      ('street2','ilike',search_string)

                     ],order = 'name')

                manager_accountants = obj_partner.search([('parent_id','!=',False),('user_id','=',request.env.user.id),('name', 'ilike', search_string),
                                                        #   "|",('function','=ilike','manager'),
                                                        #   ('function','=ilike','accountant'),

                                                          ],order = 'name')

                for partner_id in manager_accountants:
                    if partner_id.parent_id not in customer:
                        # address=''+partner_id.street if partner_id.street else''+' '+partner_id.street2 if partner_id.street2 else ''+' '+partner_id.zip if partner_id.zip else ''
                        # customer_dic.append({"id":partner_id.id or partner_id.id,"name":partner_id.display_name,'email':partner_id.email or 'N/A','mobile':partner_id.mobile or partner_id.phone or 'N/A','address':address or 'N/A'})
                        customer+=partner_id
            else:
                customer = obj_partner.search([('parent_id', '=', False), ('user_id', '=', request.env.user.id)],order = 'name')

            for rec in customer:
                checkc=True
                for pc in customer_dic:
                    if rec.id == pc['id']:
                        checkc=False
                if checkc:
                    address=''+rec.street if rec.street else''+' '+rec.street2 if rec.street2 else ''+' '+rec.zip if rec.zip else ''
                    customer_dic.append({"id":rec.id or rec.id,"name":rec.display_name,'email':rec.email or 'N/A','mobile':rec.mobile or rec.phone or 'N/A','address':address or 'N/A'})

        print("customer_dic", customer_dic)
        return customer_dic

    @http.route('/update_order_customer', type='json', auth='public')
    def _update_customers_json(self,customer_id):
        
        if not customer_id:
            return "Invalid Customer Selection!!!"

        sale_order_id = request.session.get('sale_order_id')
        customer_dic=[]
        customer = request.env['res.partner'].sudo().search([('id','=',customer_id)])
            
        if not customer:
            return "Invalid Customer Selection!!!"

        order = request.env['sale.order'].sudo().browse(sale_order_id)
        if not order:
            return "Order Not Found"
        # raise UserError(customer.company_type)
        if customer.company_type=="person":

            if customer.type == 'invoice':
                # raise UserError("invoice")
                order.sudo().write({"partner_id":int(customer.id),"partner_invoice_id":int(customer.id),"partner_shipping_id":int(customer.parent_id.id)})
            elif customer.type == 'delivery':
                # raise UserError("delivery")
                order.sudo().write({"partner_id":int(customer.parent_id.id),"partner_invoice_id":int(customer.parent_id.id),"partner_shipping_id":int(customer.id)})                
            else:
                # raise UserError("else")
                order.sudo().write({"partner_id":int(customer.parent_id.id),"partner_invoice_id":int(customer.parent_id.id),"partner_shipping_id":int(customer.parent_id.id)})
        else:
            # raise UserError("bigelse")
            order.sudo().write({"partner_id":int(customer.id),"partner_invoice_id":int(customer.id),"partner_shipping_id":int(customer.id)})

        #     partner_invoice_id = customer
        #     partner_sh = request.env['res.partner'].sudo().search(
        #         [('type', '=', 'delivery'), ('parent_id', '=', int(customer_id.parent_id.id))])
        #     if partner_sh:
        #         partner_shipping_id = partner_sh.id
        #     else:
        #         partner_shipping_id = customer
        # else:
        #     partner_invoice_id = request.env['res.partner'].sudo().search(
        #         [('type', '=', 'invoice'), ('parent_id', '=', int(customer_id))])
        #     if not partner_invoice_id:
        #         partner_invoice_id = customer

        # if customer.type == 'delivery':
        #     partner_shipping_id = customer
        #     partner_invoice_id = customer
        # else:
        #     partner_shipping_id = request.env['res.partner'].sudo().search(
        #         [('type', '=', 'delivery'), ('parent_id', '=', int(customer_id))])
        #     if not partner_shipping_id:
        #         partner_shipping_id = customer

        # order.sudo().write({"partner_id":int(customer.id),"partner_invoice_id":int(partner_invoice_id.id),"partner_shipping_id":int(partner_shipping_id.id)})
#     except Exception as ex:
#         return ex
        return "Customer Update!!!"


