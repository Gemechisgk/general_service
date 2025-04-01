# -*- coding: utf-8 -*-
# from odoo import http


# class School(http.Controller):
#     @http.route('/general_service/general_service', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/general_service/general_service/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('general_service.listing', {
#             'root': '/general_service/general_service',
#             'objects': http.request.env['general_service.general_service'].search([]),
#         })

#     @http.route('/general_service/general_service/objects/<model("general_service.general_service"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('general_service.object', {
#             'object': obj
#         })

