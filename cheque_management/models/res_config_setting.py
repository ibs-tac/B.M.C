""" Initialize Res Config Setting """

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    """
        Inherit Res Config Settings:
         -
    """
    _inherit = 'res.config.settings'

    # Incoming
    in_journal_id = fields.Many2one(
        string='Incoming Journal', readonly=False,
        related='company_id.in_journal_id'
    )
    checks_received_in_treasury_id = fields.Many2one(
        string='Checks received in the treasury', readonly=False,
        related='company_id.checks_received_in_treasury_id'
    )
    checks_under_collection_by_bank_id = fields.Many2one(
        string='Checks under collection by the bank', readonly=False,
        related='company_id.checks_under_collection_by_bank_id'
    )
    incoming_bounced_checks_id = fields.Many2one(
        string='Incoming Bounced checks', readonly=False,
        related='company_id.incoming_bounced_checks_id'
    )
    # Outgoing
    out_journal_id = fields.Many2one(
        string='Outgoing Journal', readonly=False,
        related='company_id.out_journal_id'
    )
    checks_issued_id = fields.Many2one(
        related='company_id.checks_issued_id', readonly=False
    )
    outgoing_bounced_checks_id = fields.Many2one(
        related='company_id.outgoing_bounced_checks_id', readonly=False
    )


class ResCompany(models.Model):
    """
        Inherit Res Company:
         -
    """
    _inherit = 'res.company'

    # Incoming
    in_journal_id = fields.Many2one(
        'account.journal', string='Incoming Journal',
    )
    checks_received_in_treasury_id = fields.Many2one(
        'account.account', string='Checks received in the treasury'
    )
    checks_under_collection_by_bank_id = fields.Many2one(
        'account.account', string='Checks under collection by the bank'
    )
    incoming_bounced_checks_id = fields.Many2one(
        'account.account', string='Incoming Bounced checks'
    )
    # Outgoing
    out_journal_id = fields.Many2one(
        'account.journal', string='Outgoing Journal',
    )
    checks_issued_id = fields.Many2one(
        'account.account'
    )
    outgoing_bounced_checks_id = fields.Many2one(
        'account.account'
    )
