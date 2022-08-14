from odoo import models, fields, SUPERUSER_ID
from odoo.http import request
from odoo import http, api


class InheritSetting(models.Model):
    _name = "iframe.model"

    def _get_default(self):
        self.youtube_url = '<iframe width="100%" height="500" src="https://www.youtube.com/embed/4CSjbv-FeGI" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
        iframe_link = '<iframe width="100%" height="500" src="https://www.youtube.com/embed/4CSjbv-FeGI" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
        self.env['ir.config_parameter'].set_param('ecommerce_store.youtube_url', self.youtube_url)

        return iframe_link

    youtube_url = fields.Char(string='Enter Video Embed code for Popup', store=True,
                              default=lambda self: self._get_default())
