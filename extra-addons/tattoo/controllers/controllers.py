# -*- coding: utf-8 -*-
from odoo import http

# class Tattoo(http.Controller):
#     @http.route('/tattoo/tattoo/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tattoo/tattoo/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tattoo.listing', {
#             'root': '/tattoo/tattoo',
#             'objects': http.request.env['tattoo.tattoo'].search([]),
#         })

#     @http.route('/tattoo/tattoo/objects/<model("tattoo.tattoo"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tattoo.object', {
#             'object': obj
#         })