# -*- coding: utf-8 -*-
# from odoo import http


# class Transportation(http.Controller):
#     @http.route('/transportation/transportation/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/transportation/transportation/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('transportation.listing', {
#             'root': '/transportation/transportation',
#             'objects': http.request.env['transportation.transportation'].search([]),
#         })

#     @http.route('/transportation/transportation/objects/<model("transportation.transportation"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('transportation.object', {
#             'object': obj
#         })
