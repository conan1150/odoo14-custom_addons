# -*- coding: utf-8 -*-
# from odoo import http


# class SchoolInheritViews(http.Controller):
#     @http.route('/school_inherit_views/school_inherit_views/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/school_inherit_views/school_inherit_views/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('school_inherit_views.listing', {
#             'root': '/school_inherit_views/school_inherit_views',
#             'objects': http.request.env['school_inherit_views.school_inherit_views'].search([]),
#         })

#     @http.route('/school_inherit_views/school_inherit_views/objects/<model("school_inherit_views.school_inherit_views"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('school_inherit_views.object', {
#             'object': obj
#         })
