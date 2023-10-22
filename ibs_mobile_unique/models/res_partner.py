# -*- coding: utf-8 -*-
""" Res Partner """
from odoo import api, fields, models, _
from odoo.exceptions import UserError, Warning, ValidationError


class ResPartner(models.Model):
    """ inherit Res Partner """
    _inherit = 'res.partner'

    @api.constrains('mobile')
    def _check_mobile_num(self):
        """ Validate mobile_num """
        if self.mobile:
            mobile = self.env['res.partner'].search(
                [('mobile', '=', self.mobile), ('id', '!=', self.id)], limit=1)
            if mobile:
                raise ValidationError(
                    _('This mobile number  %s is with one of the clients' % self.mobile))
