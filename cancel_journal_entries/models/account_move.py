# -*- coding: utf-8 -*-
""" Account Move """
from odoo import api, fields, models, _
from odoo.exceptions import UserError, Warning, ValidationError


class AccountMove(models.Model):
    """ inherit Account Move """
    _inherit = 'account.move'

    def all_cancel(self):
        """ All Cancel """
        all_moves = self.env['account.move'].search(
            [('move_type', '=', 'entry'),('journal_id.type', '=', 'general')])
        for rec in all_moves:
            rec.state='draft'
