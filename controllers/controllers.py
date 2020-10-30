# -*- coding: utf-8 -*-
# from odoo import http


# class Opnacademy(http.Controller):
#     @http.route('/opnacademy/opnacademy/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/opnacademy/opnacademy/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('opnacademy.listing', {
#             'root': '/opnacademy/opnacademy',
#             'objects': http.request.env['opnacademy.opnacademy'].search([]),
#         })

#     @http.route('/opnacademy/opnacademy/objects/<model("opnacademy.opnacademy"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('opnacademy.object', {
#             'object': obj
#         })
