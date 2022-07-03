# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class cancel__journal_entries(models.Model):
#     _name = 'cancel__journal_entries.cancel__journal_entries'
#     _description = 'cancel__journal_entries.cancel__journal_entries'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
