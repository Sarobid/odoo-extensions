# -*- coding: utf-8 -*-
# from odoo import http


# class SmartUiTools(http.Controller):
#     @http.route('/smart_ui_tools/smart_ui_tools/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/smart_ui_tools/smart_ui_tools/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('smart_ui_tools.listing', {
#             'root': '/smart_ui_tools/smart_ui_tools',
#             'objects': http.request.env['smart_ui_tools.smart_ui_tools'].search([]),
#         })

#     @http.route('/smart_ui_tools/smart_ui_tools/objects/<model("smart_ui_tools.smart_ui_tools"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('smart_ui_tools.object', {
#             'object': obj
#         })
