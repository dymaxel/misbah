import werkzeug
import odoo
from odoo import http, _
from odoo.http import request
from odoo.exceptions import UserError, _logger
from odoo.addons.auth_signup.models.res_users import SignupError
from datetime import datetime
from odoo.addons.web.controllers.main import ensure_db, Home, SIGN_UP_REQUEST_PARAMS
from odoo.addons.base_setup.controllers.main import BaseSetup
from odoo.exceptions import UserError
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.web.controllers.main import Home
from odoo.addons.web.controllers.main import Session

from odoo.addons.website_mass_mailing.controllers.main import MassMailController
from odoo import models, fields,SUPERUSER_ID
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website_sale.controllers.main import TableCompute
from odoo.addons.website_sale.controllers.main import WebsiteSale


class website_sale(WebsiteSale):

    @http.route(['/shop/payment/add_note'], type='json', auth="public", website=True)
    def add_note(self, internal_notes, **post):
        context = request.context
        order = request.website.sale_get_order()
        if order:
            order.sudo().write({'internal_notes': internal_notes})
    @http.route([
        '''/shop''',
        '''/shop/page/<int:page>''',
        '''/shop/category/<model("product.public.category"):category>''',
        '''/shop/category/<model("product.public.category"):category>/page/<int:page>'''
    ], type='http', auth="user", website=True, sitemap=WebsiteSale.sitemap_shop)
    def shop(self, page=0, category=None, search='', min_price=0.0, max_price=0.0, ppg=False, **post):
        add_qty = int(post.get('add_qty', 1))
        try:
            min_price = float(min_price)
        except ValueError:
            min_price = 0
        try:
            max_price = float(max_price)
        except ValueError:
            max_price = 0

        Category = request.env['product.public.category']
        if category:
            category = Category.search([('id', '=', int(category))], limit=1)
            if not category or not category.can_access_from_current_website():
                raise NotFound()
        else:
            category = Category

        if ppg:
            try:
                ppg = int(ppg)
                post['ppg'] = ppg
            except ValueError:
                ppg = False
        if not ppg:
            ppg = request.env['website'].get_current_website().shop_ppg or 20

        ppr = request.env['website'].get_current_website().shop_ppr or 4

        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [[int(x) for x in v.split("-")] for v in attrib_list if v]
        attributes_ids = {v[0] for v in attrib_values}
        attrib_set = {v[1] for v in attrib_values}

        keep = QueryURL('/shop', category=category and int(category), search=search, attrib=attrib_list, min_price=min_price, max_price=max_price, order=post.get('order'))

        pricelist_context, pricelist = self._get_pricelist_context()

        request.context = dict(request.context, pricelist=pricelist.id, partner=request.env.user.partner_id)

        filter_by_price_enabled = request.website.is_view_active('website_sale.filter_products_price')
        if filter_by_price_enabled:
            company_currency = request.website.company_id.currency_id
            conversion_rate = request.env['res.currency']._get_conversion_rate(company_currency, pricelist.currency_id, request.website.company_id, fields.Date.today())
        else:
            conversion_rate = 1

        url = "/shop"
        if search:
            post["search"] = search
        if attrib_list:
            post['attrib'] = attrib_list

        options = self._get_search_options(
            category=category,
            attrib_values=attrib_values,
            pricelist=pricelist,
            min_price=min_price,
            max_price=max_price,
            conversion_rate=conversion_rate,
            **post
        )
        # No limit because attributes are obtained from complete product list
        product_count, details, fuzzy_search_term = request.website._search_with_fuzzy("products_only", search,
            limit=None, order=self._get_search_order(post), options=options)
        search_product = details[0].get('results', request.env['product.template']).with_context(bin_size=True)

        filter_by_price_enabled = request.website.is_view_active('website_sale.filter_products_price')
        if filter_by_price_enabled:
            # TODO Find an alternative way to obtain the domain through the search metadata.
            Product = request.env['product.template'].with_context(bin_size=True)
            domain = self._get_search_domain(search, category, attrib_values)

            # This is ~4 times more efficient than a search for the cheapest and most expensive products
            from_clause, where_clause, where_params = Product._where_calc(domain).get_sql()
            query = f"""
                SELECT COALESCE(MIN(list_price), 0) * {conversion_rate}, COALESCE(MAX(list_price), 0) * {conversion_rate}
                  FROM {from_clause}
                 WHERE {where_clause}
            """
            request.env.cr.execute(query, where_params)
            available_min_price, available_max_price = request.env.cr.fetchone()

            if min_price or max_price:
                # The if/else condition in the min_price / max_price value assignment
                # tackles the case where we switch to a list of products with different
                # available min / max prices than the ones set in the previous page.
                # In order to have logical results and not yield empty product lists, the
                # price filter is set to their respective available prices when the specified
                # min exceeds the max, and / or the specified max is lower than the available min.
                if min_price:
                    min_price = min_price if min_price <= available_max_price else available_min_price
                    post['min_price'] = min_price
                if max_price:
                    max_price = max_price if max_price >= available_min_price else available_max_price
                    post['max_price'] = max_price

        website_domain = request.website.website_domain()
        categs_domain = [('parent_id', '=', False)] + website_domain
        if search:
            search_categories = Category.search([('product_tmpl_ids', 'in', search_product.ids)] + website_domain).parents_and_self
            categs_domain.append(('id', 'in', search_categories.ids))
        else:
            search_categories = Category
        categs = Category.search(categs_domain)

        if category:
            url = "/shop/category/%s" % slug(category)

        pager = request.website.pager(url=url, total=product_count, page=page, step=ppg, scope=7, url_args=post)
        offset = pager['offset']
        products = search_product[offset:offset + ppg]

        ProductAttribute = request.env['product.attribute']
        if products:
            # get all products without limit
            attributes = ProductAttribute.search([
                ('product_tmpl_ids', 'in', search_product.ids),
                ('visibility', '=', 'visible'),
            ])
        else:
            attributes = ProductAttribute.browse(attributes_ids)

        layout_mode = request.session.get('website_sale_shop_layout_mode')
        if not layout_mode:
            if request.website.viewref('website_sale.products_list_view').active:
                layout_mode = 'list'
            else:
                layout_mode = 'grid'

        values = {
            'search': fuzzy_search_term or search,
            'original_search': fuzzy_search_term and search,
            'category': category,
            'attrib_values': attrib_values,
            'attrib_set': attrib_set,
            'pager': pager,
            'pricelist': pricelist,
            'add_qty': add_qty,
            'products': products,
            'search_count': product_count,  # common for all searchbox
            'bins': TableCompute().process(products, ppg, ppr),
            'ppg': ppg,
            'ppr': ppr,
            'categories': categs,
            'attributes': attributes,
            'keep': keep,
            'search_categories_ids': search_categories.ids,
            'layout_mode': layout_mode,
        }
        if filter_by_price_enabled:
            values['min_price'] = min_price or available_min_price
            values['max_price'] = max_price or available_max_price
            values['available_min_price'] = tools.float_round(available_min_price, 2)
            values['available_max_price'] = tools.float_round(available_max_price, 2)
        if category:
            values['main_object'] = category
        return request.render("website_sale.products", values)

class WebsiteSignUpInherit(AuthSignupHome):
    @http.route('/web/signup', type='http', auth='public', website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()
        if request.params.get('c_type'):
            qcontext['c_type'] = request.params.get('c_type')

        if not qcontext.get('token') and not qcontext.get('signup_enabled'):
            raise werkzeug.exceptions.NotFound()

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                self.do_signup(qcontext)
                # Send an account creation confirmation email
                User = request.env['res.users']
                if qcontext.get('token'):
                    user_sudo = User.sudo().search(
                        User._get_login_domain(qcontext.get('login')), order=User._get_login_order(), limit=1
                    )
                    template = request.env.ref('auth_signup.mail_template_user_signup_account_created', raise_if_not_found=False)
                    if user_sudo and template:
                        template.sudo().send_mail(user_sudo.id, force_send=True)

                if kw.get('customer_type'):
                    user_sudo = User.sudo().search(
                        User._get_login_domain(qcontext.get('login')), order=User._get_login_order(), limit=1
                    )
                    cust_type = request.env['web.customer.type'].sudo().search([('id', '=', kw.get('customer_type'))], limit=1)
                    if cust_type:
                        pricelist_id = request.env['product.pricelist'].sudo().search([('x_studio_pricelist_type', '=', cust_type.id)], limit=1)
                        user_sudo.partner_id.property_product_pricelist = pricelist_id and pricelist_id.id or 2
                    user_sudo.partner_id.Customer_Type = cust_type.id

                return self.web_login(*args, **kw)
            except UserError as e:
                qcontext['error'] = e.args[0]
            except (SignupError, AssertionError) as e:
                if request.env["res.users"].sudo().search([("login", "=", qcontext.get("login"))]):
                    qcontext["error"] = _("Another user is already registered using this email address.")
                else:
                    _logger.error("%s", e)
                    qcontext['error'] = _("Could not create a new account.")

        response = request.render('auth_signup.signup', qcontext)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

#     @http.route(['/web/signup'],type='http', auth='public', website=True, sitemap=False)
#     def web_auth_signup(self, *args, **kw):
#         qcontext = self.get_auth_signup_qcontext()
#         print("qcontext123",qcontext)
#         if request.params.get('c_type'):
#             qcontext['c_type'] = request.params.get('c_type')
#         login_user = request.env.user.partner_id

#         if not qcontext.get('token') and not qcontext.get('signup_enabled'):
#             raise werkzeug.exceptions.NotFound()

#         if 'error' not in qcontext and request.httprequest.method == 'POST':
#             try:
#                 self.do_signup(qcontext)
#                 User = request.env['res.users']
#                 user_sudo = User.sudo().search(
#                     User._get_login_domain(qcontext.get('login')), order=User._get_login_order(), limit=1
#                 )
#                 # Send an account creation confirmation email
#                 if qcontext.get('token'):
#                     user_sudo = User.sudo().search(
#                         User._get_login_domain(qcontext.get('login')), order=User._get_login_order(), limit=1
#                     )
#                     template = request.env.ref('auth_signup.mail_template_user_signup_account_created', raise_if_not_found=False)
#                     if user_sudo and template:
#                         template.sudo().send_mail(user_sudo.id, force_send=True)

#                 # Send email to admin for verification

#                 template = request.env.ref('ecommerce_store.email_send_to_admin',
#                                            raise_if_not_found=False)
#                 # admin_partner =  request.env['res.partner'].sudo().search([('name','=', 'Administrator DistriMS')])
#                 user_admin = request.env['res.users'].sudo().search([('id','=',2)])

#                 if user_admin and template:
#                         template.sudo().send_mail(user_admin.id, force_send = True)


#                 if kw.get('customer_type'):
#                     if kw['customer_type'] == '3':
#                         user_sudo.partner_id.property_product_pricelist = 2
# #                     raise UserError(kw['customer_type'])
#                     cust_type = kw['customer_type']
#                     user_sudo.partner_id.Customer_Type = cust_type
                    
#                     # partner_id = user_sudo.partner_id
#                     # res_partner = request.env['res.partner'].sudo().search([('id', '=', partner_id.id)])
#                     # if res_partner:
#                     #     res_partner.sudo().write({"Customer_Type": kw['customer_type']})
#                 return self.web_login(*args, **kw)
#             except UserError as e:
#                 qcontext['error'] = e.args[0]
#             except (SignupError, AssertionError) as e:
#                 if request.env["res.users"].sudo().search([("login", "=", qcontext.get("login"))]):
#                     qcontext["error"] = _("Another user is already registered using this email address.")
#                 else:
#                     _logger.error("%s", e)
#                     qcontext['error'] = _("Could not create a new account.")
#         response = request.render('auth_signup.signup', qcontext)
#         response.headers['X-Frame-Options'] = 'DENY'
#         return response

# Inherit web/login to create login logs that have been login
class WebsiteSignInInherit(Home):
    @http.route()
    def web_login(self, redirect=None, **kw):
        res = super(WebsiteSignInInherit, self).web_login(redirect)
        if request.httprequest.method == 'POST' and request.params['login_success'] == True:
            DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
            now = str(datetime.now().replace(microsecond=0, second=0))
            partner = request.env.user.partner_id
            tages = ''
            for tags in partner.category_id:
                tages = tages + tags.display_name
            model = request.env['ir.model'].sudo().search([('model','=','res.users')])
            values = {
            'create_date': datetime.strptime(now, DATETIME_FORMAT),
            'description': partner.name or '' +'  '+ partner.email or '' +'  '+ tages,
            'model_id': model.id if model else False,
            'res_id': request.env.user.id,
            'method': 'login',
            'user_id': request.env.user.id,
            }
            update_values = request.env['audit.log'].sudo().create(values)
        return res

class WebsiteSessionInherit(Session):
    @http.route()
    def logout(self, redirect='/web'):

        DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
        now = str(datetime.now().replace(microsecond=0, second=0))

        uid = request.context.get('uid',2)
        user = request.env['res.users'].sudo().browse(uid)
        partner = user.partner_id
        tages = ''
        for tags in partner.category_id:
            tages = tages + tags.display_name
        model = request.env['ir.model'].sudo().search([('model', '=', 'res.users')])
        values = {
            'create_date': datetime.strptime(now, DATETIME_FORMAT),
            'description': "Name: %s Email: %s Tags: %s"%(partner.name , user.login , tages),
            'model_id': model.id if model else False,
            'res_id': user.id,
            'method': 'logout',
            'user_id': user.id,
        }
        update_values = request.env['audit.log'].sudo().create(values)

        res = super(WebsiteSessionInherit, self).logout(redirect)
        return res


class CreatePatient(http.Controller):
    @http.route('/create_customer_cus',type="http",auth="user",website=True)
    def customer_form(self,**kw):
        country = http.request.env['res.country'].sudo().search([])
        login_user=request.env.user.partner_id
        return http.request.render('custom_website_customer.create_customer',{'country':country})

    @http.route('/create/customer',type='http',auth='user',website=True)
    def Customer_created(self,**kw):
        print(kw)
        login_user = request.env.user.partner_id
        main_customer={
            'company_type':'company',
            'name':kw['company_name'],
            'street':kw['company_address'],
            'city':kw['company_city'],
            'country_id':int(kw['company_country']),
            'zip':kw['company_zip'],
            'phone':kw['company_phone'],
            'mobile':kw['company_mobile'],
            'email':kw['company_email'],
            'website':kw['company_website'],
            'Customer_Type': kw['customer_type'],
            'user_id':request.env.user.id
        }
        created_main=request.env['res.partner'].sudo().create(main_customer)
        print("Main created",created_main)
        if kw['manager_name']:
            Create_manager={
                'function':'Manager',
                'parent_id':created_main.id,
                'company_type': 'person',
                'type': 'contact',
                'name':kw['manager_name'],
                'email':kw['manager_email'],
                'phone':kw['manager_phone'],
                'mobile':kw['manager_fax_no'],
                'user_id':request.env.user.id

            }
            created_manager=request.env['res.partner'].sudo().create(Create_manager)
            print("manager Created",created_manager)
        if kw['accountent_name']:
            create_accountent={
                'parent_id': created_main.id,
                'name':kw['accountent_name'],
                'function': 'Accountent',
                'type':'contact',
                'company_type': 'person',
                'email':kw['accountent_email'],
                'phone':kw['accountent_phone'],
                'mobile':kw['accountent_fax_no'],
                'user_id':request.env.user.id
            }
            created_accountent = request.env['res.partner'].sudo().create(create_accountent)
            print("Accountent Created", created_accountent)
        create_billing={
            'name':kw['billing_name'],
            'email':kw['billing_email'],
            'phone':kw['billing_phone'],
            'street':kw['billing_address'],
            'city':kw['billing_city'],
            'country_id':int(kw['billing_country']),
            'zip':kw['billing_zip'],
            'parent_id': created_main.id,
            'type': 'invoice',
            'user_id':request.env.user.id
        }
        created_billing = request.env['res.partner'].sudo().create(create_billing)
        print("Billing Created", created_billing)
        if kw['shipping_name']:
            create_shipping = {
                'name': kw['shipping_name'],
                'email': kw['shipping_email'],
                'phone': kw['shipping_phone'],
                'street': kw['shipping_address'],
                'city': kw['shipping_city'],
                'country_id': int(kw['shipping_country']),
                'zip': kw['shipping_zip'],
                'parent_id': created_main.id,
                'type': 'delivery',
                'user_id':request.env.user.id

            }
            created_shipping = request.env['res.partner'].sudo().create(create_shipping)
            print("Shipping Created", created_shipping)

        return http.request.render('custom_website_customer.customer_created_thanks',{})

class WebsiteMassMailingInherit(MassMailController):
    @http.route('/website_mass_mailing/subscribe', type='json', website=True, auth="public")
    def subscribe(self, list_id, email, **post):
        if not request.env['ir.http']._verify_request_recaptcha_token('website_mass_mailing_subscribe'):
            return {
                'toast_type': 'danger',
                'toast_content': _("Suspicious activity detected by Google reCaptcha."),
            }

        if not list_id or list_id == 0:
            mailing_list = request.env['mailing.list'].sudo().search([('name', '=', 'Newsletter')], limit=1)
            if mailing_list:
                list_id = mailing_list[0].id
        ContactSubscription = request.env['mailing.contact.subscription'].sudo()
        Contacts = request.env['mailing.contact'].sudo()
        name, email = Contacts.get_name_email(email)

        subscription = ContactSubscription.search([('list_id', '=', int(list_id)), ('contact_id.email', '=', email)],
                                                  limit=1)
        if not subscription:
            # inline add_to_list as we've already called half of it
            contact_id = Contacts.search([('email', '=', email)], limit=1)
            if not contact_id:
                contact_id = Contacts.create({'name': name, 'email': email})
            ContactSubscription.create({'contact_id': contact_id.id, 'list_id': int(list_id)})
        elif subscription.opt_out:
            subscription.opt_out = False
        # add email to session
        request.session['mass_mailing_email'] = email
        return {
            'toast_type': 'success',
            'toast_content': _("Thanks for subscribing!"),
        }
