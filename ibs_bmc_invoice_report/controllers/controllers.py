# -*- coding: utf-8 -*-
# from odoo import http


# class IbsBmcInvoiceReport(http.Controller):
#     @http.route('/ibs_bmc_invoice_report/ibs_bmc_invoice_report', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ibs_bmc_invoice_report/ibs_bmc_invoice_report/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ibs_bmc_invoice_report.listing', {
#             'root': '/ibs_bmc_invoice_report/ibs_bmc_invoice_report',
#             'objects': http.request.env['ibs_bmc_invoice_report.ibs_bmc_invoice_report'].search([]),
#         })

#     @http.route('/ibs_bmc_invoice_report/ibs_bmc_invoice_report/objects/<model("ibs_bmc_invoice_report.ibs_bmc_invoice_report"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ibs_bmc_invoice_report.object', {
#             'object': obj
#         })
