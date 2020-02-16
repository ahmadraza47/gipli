# -*- coding: utf-8 -*-
# from odoo import http


# class DeDistMgmt(http.Controller):
#     @http.route('/de_dist_mgmt/de_dist_mgmt/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_dist_mgmt/de_dist_mgmt/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_dist_mgmt.listing', {
#             'root': '/de_dist_mgmt/de_dist_mgmt',
#             'objects': http.request.env['de_dist_mgmt.de_dist_mgmt'].search([]),
#         })

#     @http.route('/de_dist_mgmt/de_dist_mgmt/objects/<model("de_dist_mgmt.de_dist_mgmt"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_dist_mgmt.object', {
#             'object': obj
#         })
