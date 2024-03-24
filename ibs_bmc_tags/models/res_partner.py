from odoo import models, fields, api, exceptions, _


class ResPartner(models.Model):
    _inherit = 'res.partner'
    _description = 'res_partner'


    # category_id = fields.Many2many('res.partner.category')
    # ,default=lambda self: [(6, 0, [9])]
    category_id = fields.Many2many('res.partner.category',default=lambda self: self.env.ref('ibs_bmc_tags.tag_record'))