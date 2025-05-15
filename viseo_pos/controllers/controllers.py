# -*- coding: utf-8 -*-
# from odoo import http


# class SmartUiTools(http.Controller):
#     @http.route('/viseo_pos/viseo_pos/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/viseo_pos/viseo_pos/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('viseo_pos.listing', {
#             'root': '/viseo_pos/viseo_pos',
#             'objects': http.request.env['viseo_pos.viseo_pos'].search([]),
#         })

#     @http.route('/viseo_pos/viseo_pos/objects/<model("viseo_pos.viseo_pos"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('viseo_pos.object', {
#             'object': obj
#         })
