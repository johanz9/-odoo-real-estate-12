from odoo import http
from odoo.http import request

class Hello(http.Controller):

    @http.route('/design', auth='public', website=True)
    def helloworld(self, **kwargs):
        return request.render('tattoo_website.tattoo_design')

