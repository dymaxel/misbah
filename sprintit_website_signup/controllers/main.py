# -*- coding: utf-8 -*-
##############################################################################
#
#    ODOO Open Source Management Solution
#
#    ODOO Addon module by Sprintit Ltd
#    Copyright (C) 2021 Sprintit Ltd (<http://sprintit.fi>).
#
##############################################################################

from odoo import http, _
from odoo.http import request
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.exceptions import UserError, ValidationError
import werkzeug
class AuthSignupHome(AuthSignupHome):
    
    @http.route()
    def web_login(self, *args, **kw):
        """
        Method inherited to show messages if user approved or not.
        And also user may be approved once and again inactivate so,
        Message accordingly.
        """
        response = super(AuthSignupHome, self).web_login(*args, **kw)
        if response.qcontext and response.qcontext.get('login',False):
            inactive_user = request.env['res.users'].sudo().search([('login','=',response.qcontext.get('login')),('active','=',False),('approved_date','=',False)])
            if inactive_user:
                response.qcontext.update({'message':_('You can login only after your login get approved..!')})
                del response.qcontext['error']
            reinactive_user = request.env['res.users'].sudo().search([('login','=',response.qcontext.get('login')),('active','=',False),('approved_date','!=',False)])
            if reinactive_user:
                response.qcontext.update({'message':_('Your login will continue after it approved again..!')})
                del response.qcontext['error']    
        return response
    
    def get_contact_vals(self,company, kw):
        return {
            'company_type': 'person',
            'parent_id': company.id, 
            }
    
    @http.route('/web/signup', type='http', auth='public', website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()

        if not qcontext.get('token') and not qcontext.get('signup_enabled'):
            raise werkzeug.exceptions.NotFound()

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            qcontext['error'] = _(kw)
            try:
                self.do_signup(qcontext)
                # Send an account creation confirmation email
                if qcontext.get('token'):
                    User = request.env['res.users']
                    user_sudo = User.sudo().search(
                        User._get_login_domain(qcontext.get('login')), order=User._get_login_order(), limit=1
                    )
                    template = request.env.ref('auth_signup.mail_template_user_signup_account_created', raise_if_not_found=False)
                    if user_sudo and template:
                        template.sudo().send_mail(user_sudo.id, force_send=True)
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
