# -*- coding: utf-8 -*-
from odoo import http

# class TattooWebsite(http.Controller):
#     @http.route('/tattoo_website/tattoo_website/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tattoo_website/tattoo_website/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tattoo_website.listing', {
#             'root': '/tattoo_website/tattoo_website',
#             'objects': http.request.env['tattoo_website.tattoo_website'].search([]),
#         })

#     @http.route('/tattoo_website/tattoo_website/objects/<model("tattoo_website.tattoo_website"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tattoo_website.object', {
#             'object': obj
#         })