# -*- coding: utf-8 -*-
# from odoo import http


# class DeBatchPaymentCityFilter(http.Controller):
#     @http.route('/de_batch_payment_city_filter/de_batch_payment_city_filter/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_batch_payment_city_filter/de_batch_payment_city_filter/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_batch_payment_city_filter.listing', {
#             'root': '/de_batch_payment_city_filter/de_batch_payment_city_filter',
#             'objects': http.request.env['de_batch_payment_city_filter.de_batch_payment_city_filter'].search([]),
#         })

#     @http.route('/de_batch_payment_city_filter/de_batch_payment_city_filter/objects/<model("de_batch_payment_city_filter.de_batch_payment_city_filter"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_batch_payment_city_filter.object', {
#             'object': obj
#         })
