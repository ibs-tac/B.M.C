# -*- coding: utf-8 -*-
""" Sale Order """
from odoo import api, fields, models, _
from odoo.exceptions import UserError, Warning, ValidationError

class SaleOrder(models.Model):
    """ inherit Sale Order """
    _inherit = 'sale.order'

    sales_executive = fields.Char()
    sales_manager = fields.Char(default="Ahmed Aladly")