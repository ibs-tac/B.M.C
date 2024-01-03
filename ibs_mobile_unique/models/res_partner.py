# -*- coding: utf-8 -*-
""" Res Partner """
from odoo import _, api, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    """ inherit Res Partner """
    _inherit = 'res.partner'

    @api.constrains('mobile')
    def _check_mobile_num(self):
        """ Validate mobile_num """
        for rec in self:
            if rec.mobile:
                record = self.env['res.partner'].search(
                    [('mobile', '=', rec.mobile), ('id', '!=', rec.id)],
                    limit=1)
                if record:
                    raise ValidationError(
                        _(
                            'This mobile number  %s is with one of the clients' % rec.mobile))

    @api.constrains('name')
    def _check_name(self):
        """ Validate name """
        for rec in self:
            record = self.env['res.partner'].search(
                [('name', '=', rec.name), ('id', '!=', rec.id)], limit=1)
            if record:
                raise ValidationError(
                    _(
                        'Name Must be Unique'))
