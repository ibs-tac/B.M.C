# -*- coding: utf-8 -*-
""" Sale Order """
from odoo import fields, models


class SaleOrder(models.Model):
    """ inherit Sale Order """
    _inherit = 'sale.order'

    sales_executive_id = fields.Many2one(
        'res.users'
    )
    sales_manager = fields.Char(default="Ahmed Aladly")

    def send_whatsapp(self):
        link = "https://web.whatsapp.com"
        return {
            'type': 'ir.actions.act_url',
            'url': link,
            'target': 'new',
            'res_id': self.id,
        }


class SaleOrderLine(models.Model):
    """ inherit Sale Order Line """
    _inherit = 'sale.order.line'

    load = fields.Char()
    weight = fields.Char(string="Color")
