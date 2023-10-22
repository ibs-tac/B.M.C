# -*- coding: utf-8 -*-
# from odoo import http


# class IbsMobileUnique(http.Controller):
#     @http.route('/ibs_mobile_unique/ibs_mobile_unique', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ibs_mobile_unique/ibs_mobile_unique/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ibs_mobile_unique.listing', {
#             'root': '/ibs_mobile_unique/ibs_mobile_unique',
#             'objects': http.request.env['ibs_mobile_unique.ibs_mobile_unique'].search([]),
#         })

#     @http.route('/ibs_mobile_unique/ibs_mobile_unique/objects/<model("ibs_mobile_unique.ibs_mobile_unique"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ibs_mobile_unique.object', {
#             'object': obj
#         })
