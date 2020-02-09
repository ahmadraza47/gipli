# -*- coding: utf-8 -*-
# from odoo import http


# class DeInvoiceCheck(http.Controller):
#     @http.route('/de_invoice_check/de_invoice_check/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_invoice_check/de_invoice_check/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_invoice_check.listing', {
#             'root': '/de_invoice_check/de_invoice_check',
#             'objects': http.request.env['de_invoice_check.de_invoice_check'].search([]),
#         })

#     @http.route('/de_invoice_check/de_invoice_check/objects/<model("de_invoice_check.de_invoice_check"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_invoice_check.object', {
#             'object': obj
#         })
