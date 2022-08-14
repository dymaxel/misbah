from odoo import fields, http
from odoo.http import request


class Surveypage(http.Controller):
    @http.route('/survey/', auth='public',website=True)
    def survey_webpage(self,**kwargs):
        surveys = request.env['survey.survey'].sudo().search([])

        return http.request.render('shop_survey.survey', {'surveys':surveys})