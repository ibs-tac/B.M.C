# -*- coding: utf-8 -*-
# from odoo import http


# class IbsBmcTags(http.Controller):
#     @http.route('/ibs_bmc_tags/ibs_bmc_tags', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ibs_bmc_tags/ibs_bmc_tags/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ibs_bmc_tags.listing', {
#             'root': '/ibs_bmc_tags/ibs_bmc_tags',
#             'objects': http.request.env['ibs_bmc_tags.ibs_bmc_tags'].search([]),
#         })

#     @http.route('/ibs_bmc_tags/ibs_bmc_tags/objects/<model("ibs_bmc_tags.ibs_bmc_tags"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ibs_bmc_tags.object', {
#             'object': obj
#         })
