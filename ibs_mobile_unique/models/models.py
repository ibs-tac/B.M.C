# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class ibs_mobile_unique(models.Model):
#     _name = 'ibs_mobile_unique.ibs_mobile_unique'
#     _description = 'ibs_mobile_unique.ibs_mobile_unique'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
