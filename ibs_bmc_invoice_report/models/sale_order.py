# -*- coding: utf-8 -*-
""" Sale Order """
from odoo import api, fields, models, _
from odoo.exceptions import UserError, Warning, ValidationError

class SaleOrder(models.Model):
    """ inherit Sale Order """
    _inherit = 'sale.order'

    sales_executive = fields.Char()
    sales_manager = fields.Char(default="Ahmed Aladly")



class SaleOrderLine(models.Model):
    """ inherit Sale Order Line """
    _inherit = 'sale.order.line'

    pregnancy = fields.Char()
    weight = fields.Char(string="Color")
