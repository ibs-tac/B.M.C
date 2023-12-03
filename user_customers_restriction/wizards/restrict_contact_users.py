# -*- coding: utf-8 -*-
""" Restrict Contract """
from odoo import api, fields, models, _
from odoo.exceptions import UserError, Warning, ValidationError

class RestrictContactUsers(models.TransientModel):
    """ Restrict Contact Users """
    _name = 'restrict.contact.users'
    _description = 'Restrict Contact Users'

    res_users_ids = fields.Many2many('res.users','name')

    def confirm(self):
        """ Confirm """
        active_id = self._context.get('active_id')
        partner = self.env['res.partner'].browse(active_id)
        for rec in self.res_users_ids:
            rec.user_restricted_ids=[(4, partner.id)]