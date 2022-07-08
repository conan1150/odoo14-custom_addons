# -*- coding: utf-8 -*-
# from odoo import http


# class ImportPurchaseOrder(http.Controller):
#     @http.route('/import_purchase_order/import_purchase_order/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/import_purchase_order/import_purchase_order/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('import_purchase_order.listing', {
#             'root': '/import_purchase_order/import_purchase_order',
#             'objects': http.request.env['import_purchase_order.import_purchase_order'].search([]),
#         })

#     @http.route('/import_purchase_order/import_purchase_order/objects/<model("import_purchase_order.import_purchase_order"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('import_purchase_order.object', {
#             'object': obj
#         })
