""" Initialize Cheque Management """

from odoo import _, api, fields, models


class ChequeManagement(models.Model):
    """
        Initialize Cheque Management:
         -
    """
    _name = 'cheque.management'
    _description = 'Cheque Management'
    _check_company_auto = True
    _sql_constraints = [
        ('unique_cheque_number',
         'UNIQUE(cheque_number)',
         'Cheque Number must be unique'),
    ]

    name = fields.Char(
        readonly=True, default='New', copy=False
    )
    cheque_type = fields.Selection(
        [('incoming', 'Incoming'), ('outgoing', 'Outgoing')])
    description = fields.Char(
        required=True,
        readonly=True, states={'draft': [('readonly', False)]}
    )
    partner_type = fields.Selection(
        [('receivable', 'Receivable'),
         ('payable', 'Payable')
         ], readonly=True, states={'draft': [('readonly', False)]},
        default='receivable', required=True
    )
    partner_id = fields.Many2one(
        'res.partner', string='Customer / Vendor',
        required=True, readonly=True, states={'draft': [('readonly', False)]}
    )
    cheque_number = fields.Char(
        required=True, readonly=True,
        states={'draft': [('readonly', False)]}
    )
    check_due_date = fields.Date(
        readonly=True, states={'draft': [('readonly', False)]}
    )
    currency_id = fields.Many2one(
        'res.currency', required=True, readonly=True,
        default=lambda self: self.env.company.currency_id,
        states={'draft': [('readonly', False)]}
    )

    employee_id = fields.Many2one(
        'hr.employee', string='Check Sender To Bank',
        default=lambda self: self.env['hr.employee'].search(
            [('user_id', '=', self.env.uid)], limit=1),
    )
    bank_account_id = fields.Many2one(
        'account.journal', domain="[('type', '=', 'bank')]", readonly=True,
        states={'draft': [('readonly', False)]}
    )
    deposit_date = fields.Date(readonly=True)
    collected_by_another_bank_treasury = fields.Many2one(
        'account.journal', domain="[('type', '=', ['bank','cash'])]",
        string='Collected By Another Bank/Treasury', readonly=True
    )
    deducted_by_another_bank_treasury = fields.Many2one(
        'account.journal', domain="[('type', '=', ['bank','cash'])]",
        string='Deducted By Another Bank/Treasury', readonly=True
    )
    cheque_received_date = fields.Date(
        readonly=True
    )
    cheque_send_date = fields.Date(
        readonly=True,
    )
    hand_me_the_check = fields.Char()
    beneficiary_of_the_check = fields.Char(
        string='The Beneficiary Of The Check',
        required=True, readonly=True, states={'draft': [('readonly', False)]}
    )
    drawn_bank = fields.Char(
        readonly=True, states={'draft': [('readonly', False)]}
    )
    check_back = fields.Boolean(
        string='Check back ?'
    )
    back_person_name = fields.Char()
    note = fields.Text()
    move_ids = fields.Many2many(
        'account.move'
    )
    move_type = fields.Selection(
        [('out_invoice', 'Out Invoice'),
         ('in_invoice', 'In Invoice'),
         ('done', 'Done')],
        default='out_invoice',
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('send_to_bank', 'Send To Bank'),
        ('deposit', 'Deposited'),
        ('bounced', 'Bounced'),
        ('return_to_partner', 'Return To Partner'),
        ('return_from_partner', 'Return From Partner'),
        ('cashed', 'Cashed'),
        ('cancel', 'Cancelled'),
    ], string='Status', default='draft')
    move_line_ids = fields.One2many(
        'account.move.line', 'cheque_id', readonly=True,
        copy=False, ondelete='restrict'
    )
    journal_item_count = fields.Integer(
        string='Journal Items', compute='_journal_item_count', readonly=True,
        copy=False
    )
    cash_date = fields.Date(readonly=True)
    bounced_date = fields.Date(readonly=True)
    return_to_partner_date = fields.Date(readonly=True)
    return_from_partner_date = fields.Date(readonly=True)
    currency_amount = fields.Float(
        string='Amount', required=True, readonly=True,
        states={'draft': [('readonly', False)]}
    )
    amount = fields.Float(
        compute='_compute_amount', store=1
    )

    @api.depends('currency_id', 'currency_amount')
    def _compute_amount(self):
        """ Compute amount value """
        for rec in self:
            record = self.env['res.currency.rate'].search([
                ('currency_id', '=', rec.currency_id.id),
                ('name', '=', fields.Date.today()),
            ])
            if record:
                rec.amount = record.rate * rec.currency_amount
            else:
                rec.amount = rec.currency_id.rate * rec.currency_amount

    @api.depends('move_line_ids')
    def _journal_item_count(self):
        for rec in self:
            rec.journal_item_count = len(rec.move_line_ids)

    @api.model
    def create(self, vals_list):
        """
            Override create method
             - sequence name
        """
        if vals_list.get('cheque_type') == 'incoming':
            vals_list['name'] = self.env['ir.sequence'].next_by_code(
                'cheque.management.incoming') or '/'
        else:
            vals_list['name'] = self.env['ir.sequence'].next_by_code(
                'cheque.management.outgoing') or '/'
        return super(ChequeManagement, self).create(vals_list)

    def action_confirm_wizard(self):
        """ :return Action confirm wizard"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Cheque Date'),
            'res_model': 'cheque.date.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_cheque_management_id': self.id,
                'default_button_type': 'confirm',
            },
            'views': [[False, 'form']]
        }

    def confirm(self, cheque_received_date):
        """ Confirm """
        Move = self.env['account.move']
        if self.partner_type == 'receivable':
            account_id = self.partner_id.property_account_receivable_id
        else:
            account_id = self.partner_id.property_account_payable_id
        if self.cheque_type == 'incoming':
            credit_line = {
                'account_id': account_id.id,
                'partner_id': self.partner_id.id,
                'name': self.name + '-' + 'Confirm',
                'debit': 0,
                'credit': self.amount,
                'amount_currency': -self.currency_amount,
                'currency_id': self.currency_id.id,
                'date_maturity': cheque_received_date,
                'cheque_id': self.id,
            }
            debit_line = {
                'account_id':
                    self.env.company.checks_received_in_treasury_id.id,
                'partner_id': self.partner_id.id,
                'name': self.name + '-' + 'Confirm',
                'debit': self.amount,
                'credit': 0,
                'amount_currency': self.currency_amount,
                'currency_id': self.currency_id.id,
                'date_maturity': cheque_received_date,
                'cheque_id': self.id,
            }
        else:
            credit_line = {
                'account_id': self.env.company.checks_issued_id.id,
                'partner_id': self.partner_id.id,
                'name': self.name + '-' + 'Confirm',
                'debit': 0,
                'credit': self.amount,
                'amount_currency': -self.currency_amount,
                'currency_id': self.currency_id.id,
                'date_maturity': cheque_received_date,
                'cheque_id': self.id,
            }
            debit_line = {
                'account_id': account_id.id,
                'partner_id': self.partner_id.id,
                'name': self.name + '-' + 'Confirm',
                'debit': self.amount,
                'credit': 0,
                'amount_currency': self.currency_amount,
                'currency_id': self.currency_id.id,
                'date_maturity': cheque_received_date,
                'cheque_id': self.id,
            }
        move_vals = {
            'date': cheque_received_date,
            'journal_id': self.env.company.out_journal_id.id if
            self.cheque_type == 'outgoing' else
            self.env.company.in_journal_id.id,
            'ref': self.name,
            'currency_id': self.currency_id.id,
            'move_type': 'entry',
            'line_ids': [(0, 0, credit_line), (0, 0, debit_line)]
        }
        move_id = Move.create(move_vals)
        move_id.action_post()
        self.write(
            {
                'cheque_received_date': cheque_received_date,
                'state': 'confirm'
            }
        )

    def cancel(self):
        """ Cancel """
        Move = self.env['account.move']
        if self.partner_type == 'receivable':
            account_id = self.partner_id.property_account_receivable_id
        else:
            account_id = self.partner_id.property_account_payable_id

        if self.cheque_type == 'incoming':
            credit_line = {
                'account_id':
                    self.env.company.checks_received_in_treasury_id.id,
                'partner_id': self.partner_id.id,
                'name': self.name + '-' + 'Cancel',
                'debit': 0,
                'credit': self.amount,
                'amount_currency': -self.currency_amount,
                'currency_id': self.currency_id.id,
                'date_maturity': fields.Date.today(),
                'cheque_id': self.id,
            }
            debit_line = {
                'account_id': account_id.id,
                'partner_id': self.partner_id.id,
                'name': self.name + '-' + 'Cancel',
                'debit': self.amount,
                'credit': 0,
                'amount_currency': self.currency_amount,
                'currency_id': self.currency_id.id,
                'date_maturity': fields.Date.today(),
                'cheque_id': self.id,
            }
        else:
            credit_line = {
                'account_id': account_id.id,
                'partner_id': self.partner_id.id,
                'name': self.name + '-' + 'Cancel',
                'debit': 0,
                'credit': self.amount,
                'amount_currency': -self.currency_amount,
                'currency_id': self.currency_id.id,
                'date_maturity': fields.Date.today(),
                'cheque_id': self.id,
            }
            debit_line = {
                'account_id': self.env.company.checks_issued_id.id,
                'partner_id': self.partner_id.id,
                'name': self.name + '-' + 'Cancel',
                'debit': self.amount,
                'credit': 0,
                'amount_currency': self.currency_amount,
                'currency_id': self.currency_id.id,
                'date_maturity': fields.Date.today(),
                'cheque_id': self.id,
            }
        move_vals = {
            'date': fields.Date.today(),
            'journal_id': self.env.company.out_journal_id.id if
            self.cheque_type == 'outgoing' else
            self.env.company.in_journal_id.id,
            'ref': self.name,
            'currency_id': self.currency_id.id,
            'move_type': 'entry',
            'line_ids': [(0, 0, credit_line), (0, 0, debit_line)]
        }
        move_id = Move.create(move_vals)
        move_id.action_post()
        self.write({'state': 'cancel'})

    def action_cashed_wizard(self):
        """ :return Action Cashed Wizard"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Cheque Date'),
            'res_model': 'cheque.date.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_cheque_management_id': self.id,
                'default_button_type': 'cashed',
                'default_cash_type':
                    'in' if self.cheque_type == 'incoming' else 'out',
            },
            'views': [[False, 'form']]
        }

    def cashed(self, cash_date, collected_by_another_bank_treasury,
               deducted_by_another_bank_treasury):
        """ Cashed """
        Move = self.env['account.move']
        credit_account_id = False
        debit_account_id = False
        if self.partner_type == 'receivable':
            account_id = self.partner_id.property_account_receivable_id
        else:
            account_id = self.partner_id.property_account_payable_id
        if self.cheque_type == 'incoming':
            if self.state == 'confirm':
                credit_account_id = \
                    self.env.company.checks_received_in_treasury_id
                debit_account_id = \
                    collected_by_another_bank_treasury.default_account_id
            else:
                credit_account_id = account_id
                debit_account_id = \
                    collected_by_another_bank_treasury.default_account_id
        else:
            if self.state == 'confirm':
                credit_account_id = \
                    deducted_by_another_bank_treasury.default_account_id
                debit_account_id = \
                    self.env.company.checks_issued_id
            else:
                credit_account_id = \
                    deducted_by_another_bank_treasury.default_account_id
                debit_account_id = account_id
        if self.cheque_type == 'incoming':
            credit_line = {
                'account_id': credit_account_id.id,
                'partner_id': self.partner_id.id,
                'name': self.name + '-' + 'Cashed',
                'debit': 0,
                'credit': self.amount,
                'amount_currency': -self.currency_amount,
                'currency_id': self.currency_id.id,
                'date_maturity': cash_date,
                'cheque_id': self.id,
            }
            debit_line = {
                'account_id': debit_account_id.id,
                'partner_id': self.partner_id.id,
                'name': self.name + '-' + 'Cashed',
                'debit': self.amount,
                'credit': 0,
                'amount_currency': self.currency_amount,
                'currency_id': self.currency_id.id,
                'date_maturity': cash_date,
                'cheque_id': self.id,
            }
        else:
            credit_line = {
                'account_id': credit_account_id.id,
                'partner_id': self.partner_id.id,
                'name': self.name + '-' + 'Cashed',
                'debit': 0,
                'credit': self.amount,
                'amount_currency': -self.currency_amount,
                'currency_id': self.currency_id.id,
                'date_maturity': cash_date,
                'cheque_id': self.id,
            }
            debit_line = {
                'account_id': debit_account_id.id,
                'partner_id': self.partner_id.id,
                'name': self.name + '-' + 'Cashed',
                'debit': self.amount,
                'credit': 0,
                'amount_currency': self.currency_amount,
                'currency_id': self.currency_id.id,
                'date_maturity': cash_date,
                'cheque_id': self.id,
            }
        move_vals = {
            'date': cash_date,
            'journal_id': self.env.company.out_journal_id.id if
            self.cheque_type == 'outgoing' else
            self.env.company.in_journal_id.id,
            'ref': self.name,
            'currency_id': self.currency_id.id,
            'move_type': 'entry',
            'line_ids': [(0, 0, credit_line), (0, 0, debit_line)]
        }
        move_id = Move.create(move_vals)
        move_id.action_post()
        self.write({
            'cash_date': cash_date,
            'collected_by_another_bank_treasury':
                collected_by_another_bank_treasury,
            'deducted_by_another_bank_treasury':
                deducted_by_another_bank_treasury,
            'state': 'cashed'
        })

    def action_send_to_bank_wizard(self):
        """ :return Action send to bank wizard"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Cheque Date'),
            'res_model': 'cheque.date.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_cheque_management_id': self.id,
                'default_button_type': 'send_to_bank',
            },
            'views': [[False, 'form']]
        }

    def send_to_bank(self, cheque_send_date, bank_account_id):
        """ Send To Bank """
        Move = self.env['account.move']
        if self.cheque_type == 'incoming':
            credit_line = {
                'account_id':
                    self.env.company.checks_received_in_treasury_id.id,
                'partner_id': self.partner_id.id,
                'name': self.name + '-' + 'Send To Bank',
                'debit': 0,
                'credit': self.amount,
                'amount_currency': -self.currency_amount,
                'currency_id': self.currency_id.id,
                'date_maturity': cheque_send_date,
                'cheque_id': self.id,
            }
            debit_line = {
                'account_id':
                    self.env.company.checks_under_collection_by_bank_id.id,
                'partner_id': self.partner_id.id,
                'name': self.name + '-' + 'Send To Bank',
                'debit': self.amount,
                'credit': 0,
                'amount_currency': self.currency_amount,
                'currency_id': self.currency_id.id,
                'date_maturity': cheque_send_date,
                'cheque_id': self.id,
            }
            move_vals = {
                'date': cheque_send_date,
                'journal_id': self.env.company.in_journal_id.id,
                'ref': self.name,
                'currency_id': self.currency_id.id,
                'move_type': 'entry',
                'line_ids': [(0, 0, credit_line), (0, 0, debit_line)]
            }
            move_id = Move.create(move_vals)
            move_id.action_post()
            self.write(
                {
                    'cheque_send_date': cheque_send_date,
                    'bank_account_id': bank_account_id,
                    'state': 'send_to_bank',
                }
            )

    def action_in_deposit_wizard(self):
        """ :return Action In Deposit Wizard"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Cheque Date'),
            'res_model': 'cheque.date.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_cheque_management_id': self.id,
                'default_button_type': 'in_deposit',
            },
            'views': [[False, 'form']]
        }

    def in_deposit(self, deposit_date):
        """Incoming Deposit"""
        Move = self.env['account.move']
        if self.cheque_type == 'incoming':
            credit_line = {
                'account_id':
                    self.env.company.checks_under_collection_by_bank_id.id,
                'partner_id': self.partner_id.id,
                'name': self.name + '-' + 'Deposit',
                'debit': 0,
                'credit': self.amount,
                'amount_currency': -self.currency_amount,
                'currency_id': self.currency_id.id,
                'date_maturity': deposit_date,
                'cheque_id': self.id,
            }
            debit_line = {
                'account_id':
                    self.bank_account_id.default_account_id.id,
                'partner_id': self.partner_id.id,
                'name': self.name + '-' + 'Deposit',
                'debit': self.amount,
                'credit': 0,
                'amount_currency': self.currency_amount,
                'currency_id': self.currency_id.id,
                'date_maturity': deposit_date,
                'cheque_id': self.id,
            }
            move_vals = {
                'date': deposit_date,
                'journal_id': self.env.company.in_journal_id.id,
                'ref': self.name,
                'currency_id': self.currency_id.id,
                'move_type': 'entry',
                'line_ids': [(0, 0, credit_line), (0, 0, debit_line)]
            }
            move_id = Move.create(move_vals)
            move_id.action_post()
            self.write({
                'deposit_date': deposit_date,
                'state': 'deposit',
            })

    def action_out_deposit_wizard(self):
        """ :return Action Out Deposit Wizard"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Cheque Date'),
            'res_model': 'cheque.date.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_cheque_management_id': self.id,
                'default_button_type': 'out_deposit',
            },
            'views': [[False, 'form']]
        }

    def out_deposit(self, deposit_date):
        """ Outgoing Deposit """
        Move = self.env['account.move']
        if self.cheque_type == 'outgoing':
            credit_line = {
                'account_id':
                    self.bank_account_id.default_account_id.id,
                'partner_id': self.partner_id.id,
                'name': self.name + '-' + 'Deposit',
                'debit': 0,
                'credit': self.amount,
                'amount_currency': -self.currency_amount,
                'currency_id': self.currency_id.id,
                'date_maturity': deposit_date,
                'cheque_id': self.id,
            }
            debit_line = {
                'account_id': self.env.company.checks_issued_id.id,
                'partner_id': self.partner_id.id,
                'name': self.name + '-' + 'Deposit',
                'debit': self.amount,
                'credit': 0,
                'amount_currency': self.currency_amount,
                'currency_id': self.currency_id.id,
                'date_maturity': deposit_date,
                'cheque_id': self.id,
            }
            move_vals = {
                'date': deposit_date,
                'journal_id': self.env.company.out_journal_id.id,
                'ref': self.name,
                'currency_id': self.currency_id.id,
                'move_type': 'entry',
                'line_ids': [(0, 0, credit_line), (0, 0, debit_line)]
            }
            move_id = Move.create(move_vals)
            move_id.action_post()
            self.write({
                'deposit_date': deposit_date,
                'state': 'deposit'
            })

    def action_in_bounced_wizard(self):
        """ :return Action In Bounced Wizard"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Cheque Date'),
            'res_model': 'cheque.date.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_cheque_management_id': self.id,
                'default_button_type': 'in_bounced',
            },
            'views': [[False, 'form']]
        }

    def in_bounced(self, bounced_date):
        """ Incoming Bounced"""
        Move = self.env['account.move']
        if self.cheque_type == 'incoming':
            credit_line = {
                'account_id':
                    self.env.company.checks_under_collection_by_bank_id.id,
                'partner_id': self.partner_id.id,
                'name': self.name + '-' + 'Bounced',
                'debit': 0,
                'credit': self.amount,
                'amount_currency': -self.currency_amount,
                'currency_id': self.currency_id.id,
                'date_maturity': bounced_date,
                'cheque_id': self.id,
            }
            debit_line = {
                'account_id':
                    self.env.company.incoming_bounced_checks_id.id,
                'partner_id': self.partner_id.id,
                'name': self.name + '-' + 'Bounced',
                'debit': self.amount,
                'credit': 0,
                'amount_currency': self.currency_amount,
                'currency_id': self.currency_id.id,
                'date_maturity': bounced_date,
                'cheque_id': self.id,
            }
            move_vals = {
                'date': bounced_date,
                'journal_id': self.env.company.out_journal_id.id if
                self.cheque_type == 'outgoing' else
                self.env.company.in_journal_id.id,
                'ref': self.name,
                'currency_id': self.currency_id.id,
                'move_type': 'entry',
                'line_ids': [(0, 0, credit_line), (0, 0, debit_line)]
            }
            move_id = Move.create(move_vals)
            move_id.action_post()
            self.write({
                'bounced_date': bounced_date,
                'state': 'bounced'
            })

    def action_out_bounced_wizard(self):
        """ :return Action Out Bounced Wizard"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Cheque Date'),
            'res_model': 'cheque.date.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_cheque_management_id': self.id,
                'default_button_type': 'out_bounced',
            },
            'views': [[False, 'form']]
        }

    def out_bounced(self, bounced_date):
        """ Outgoing Bounced"""
        Move = self.env['account.move']
        if self.partner_type == 'receivable':
            account_id = self.partner_id.property_account_receivable_id
        else:
            account_id = self.partner_id.property_account_payable_id
        if self.cheque_type == 'outgoing':
            credit_line1 = {
                'account_id':
                    self.env.company.outgoing_bounced_checks_id.id,
                'partner_id': self.partner_id.id,
                'name': self.name + '-' + 'Bounced',
                'debit': 0,
                'credit': self.amount,
                'amount_currency': -self.currency_amount,
                'currency_id': self.currency_id.id,
                'date_maturity': bounced_date,
                'cheque_id': self.id,
            }
            debit_line1 = {
                'account_id': self.env.company.checks_issued_id.id,
                'partner_id': self.partner_id.id,
                'name': self.name + '-' + 'Bounced',
                'debit': self.amount,
                'credit': 0,
                'date_maturity': bounced_date,
                'cheque_id': self.id,
            }
            credit_line2 = {
                'account_id': account_id.id,
                'partner_id': self.partner_id.id,
                'name': self.name + '-' + 'Bounced',
                'debit': 0,
                'credit': self.amount,
                'amount_currency': -self.currency_amount,
                'currency_id': self.currency_id.id,
                'date_maturity': bounced_date,
                'cheque_id': self.id,
            }
            debit_line2 = {
                'account_id':
                    self.env.company.outgoing_bounced_checks_id.id,
                'partner_id': self.partner_id.id,
                'name': self.name + '-' + 'Bounced',
                'debit': self.amount,
                'credit': 0,
                'amount_currency': self.currency_amount,
                'currency_id': self.currency_id.id,
                'date_maturity': bounced_date,
                'cheque_id': self.id,
            }
            move_vals = {
                'date': bounced_date,
                'journal_id': self.env.company.out_journal_id.id if
                self.cheque_type == 'outgoing' else
                self.env.company.in_journal_id.id,
                'ref': self.name,
                'currency_id': self.currency_id.id,
                'move_type': 'entry',
                'line_ids': [(0, 0, credit_line1), (0, 0, debit_line1),
                             (0, 0, credit_line2), (0, 0, debit_line2)]
            }
            move_id = Move.create(move_vals)
            move_id.action_post()
            self.write({
                'bounced_date': bounced_date,
                'state': 'bounced'
            })

    def action_return_to_partner_wizard(self):
        """ :return Action return_to_partner Wizard"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Cheque Date'),
            'res_model': 'cheque.date.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_cheque_management_id': self.id,
                'default_button_type': 'return_to_partner',
            },
            'views': [[False, 'form']]
        }

    def return_to_partner(self, return_to_partner_date):
        """ Return To Partner """
        Move = self.env['account.move']
        if self.partner_type == 'receivable':
            account_id = self.partner_id.property_account_receivable_id
        else:
            account_id = self.partner_id.property_account_payable_id

        if self.cheque_type == 'incoming':
            credit_line = {
                'account_id':
                    self.env.company.incoming_bounced_checks_id.id,
                'partner_id': self.partner_id.id,
                'name': self.name + '-' + 'Return To Partner',
                'debit': 0,
                'credit': self.amount,
                'amount_currency': -self.currency_amount,
                'currency_id': self.currency_id.id,
                'date_maturity': return_to_partner_date,
                'cheque_id': self.id,
            }
            debit_line = {
                'account_id': account_id.id,
                'partner_id': self.partner_id.id,
                'name': self.name + '-' + 'Return To Partner',
                'debit': self.amount,
                'credit': 0,
                'amount_currency': self.currency_amount,
                'currency_id': self.currency_id.id,
                'date_maturity': return_to_partner_date,
                'cheque_id': self.id,
            }
            move_vals = {
                'date': return_to_partner_date,
                'journal_id': self.env.company.out_journal_id.id if
                self.cheque_type == 'outgoing' else
                self.env.company.in_journal_id.id,
                'ref': self.name,
                'currency_id': self.currency_id.id,
                'move_type': 'entry',
                'line_ids': [(0, 0, credit_line), (0, 0, debit_line)]
            }
            move_id = Move.create(move_vals)
            move_id.action_post()
            self.write({
                'return_to_partner_date': return_to_partner_date,
                'state': 'return_to_partner'
            })

    def action_return_from_partner_wizard(self):
        """ :return Action return_from_partner Wizard"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Cheque Date'),
            'res_model': 'cheque.date.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_cheque_management_id': self.id,
                'default_button_type': 'return_from_partner',
            },
            'views': [[False, 'form']]
        }

    def return_from_partner(self, return_from_partner_date):
        """ Return From Partner """
        Move = self.env['account.move']
        if self.partner_type == 'receivable':
            account_id = self.partner_id.property_account_receivable_id
        else:
            account_id = self.partner_id.property_account_payable_id

        if self.cheque_type == 'outgoing':
            credit_line = {
                'account_id': account_id.id,
                'partner_id': self.partner_id.id,
                'name': self.name + '-' + 'Return From Partner',
                'debit': 0,
                'credit': self.amount,
                'amount_currency': -self.currency_amount,
                'currency_id': self.currency_id.id,
                'date_maturity': return_from_partner_date,
                'cheque_id': self.id,
            }
            debit_line = {
                'account_id': self.env.company.outgoing_bounced_checks_id.id,
                'partner_id': self.partner_id.id,
                'name': self.name + '-' + 'Return From Partner',
                'debit': self.amount,
                'credit': 0,
                'amount_currency': self.currency_amount,
                'currency_id': self.currency_id.id,
                'date_maturity': return_from_partner_date,
                'cheque_id': self.id,
            }
            move_vals = {
                'date': return_from_partner_date,
                'journal_id': self.env.company.out_journal_id.id,
                'ref': self.name,
                'currency_id': self.currency_id.id,
                'move_type': 'entry',
                'line_ids': [(0, 0, credit_line), (0, 0, debit_line)]
            }
            move_id = Move.create(move_vals)
            move_id.action_post()
            self.write({
                'return_from_partner_date': return_from_partner_date,
                'state': 'return_from_partner'
            })

    def action_view_account_move_line(self):
        """ :return Account Move Line action """
        self.ensure_one()
        return {
            'name': _('Journal Items'),
            'view_mode': 'tree,form',
            'res_model': 'account.move.line',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': [('cheque_id', '=', self.id)],
        }


class AccountMoveLine(models.Model):
    """
        Inherit Account Move Line:
         -
    """
    _inherit = 'account.move.line'

    cheque_id = fields.Many2one('cheque.management', 'Cheque Id')
