# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class ibs_bmc_tags(models.Model):
#     _name = 'ibs_bmc_tags.ibs_bmc_tags'
#     _description = 'ibs_bmc_tags.ibs_bmc_tags'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
