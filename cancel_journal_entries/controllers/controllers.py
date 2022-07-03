# -*- coding: utf-8 -*-
# from odoo import http


# class CancelJournalEntries(http.Controller):
#     @http.route('/cancel__journal_entries/cancel__journal_entries', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cancel__journal_entries/cancel__journal_entries/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('cancel__journal_entries.listing', {
#             'root': '/cancel__journal_entries/cancel__journal_entries',
#             'objects': http.request.env['cancel__journal_entries.cancel__journal_entries'].search([]),
#         })

#     @http.route('/cancel__journal_entries/cancel__journal_entries/objects/<model("cancel__journal_entries.cancel__journal_entries"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cancel__journal_entries.object', {
#             'object': obj
#         })
