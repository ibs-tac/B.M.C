# -*- coding: utf-8 -*-
""" Res Partner """
from odoo import api, fields, models, _
from odoo.exceptions import UserError, Warning, ValidationError

class ResPartner(models.Model):
    """ inherit Res Partner """
    _inherit = 'res.partner'



    # def user_restricted(self):
    #     """ User Restricted """
    #     users=self.env['res.users'].search([])
    #     for rec in users:
    #
    #
    #     action = \
    #         self.env.ref('ibs_construction.advance_payments_action').sudo().read()[
    #             0]
    #     # action['views'] = [
    #     #     (self.env.ref('ibs_construction.subcontractors_cycle_form').id,
    #     #      'form')]
    #     action['context'] = {'default_partner_id': self.partner_id.id}
    #
    #     return action


