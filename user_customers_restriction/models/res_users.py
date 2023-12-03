from odoo import models, fields, api, SUPERUSER_ID

# -- List of predefined rules that must be managed
PREDEFINED_RULES = ['res.partner.rule.private.employee',
                    'res.partner.rule.private.group']


class PRTUsers(models.Model):
    _name = "res.users"
    _inherit = "res.users"

    user_restricted_ids = fields.Many2many(
        'res.partner', string='Allowed Customer')

    # -- Tweak access rules
    #     """
    #     Need to shut down some non-updatable rules to ensure tweak is applied correctly
    #     """
    @api.model
    def tweak_access_rules(self):
        rules = self.env['ir.rule'].sudo().search(
            [('name', 'in', PREDEFINED_RULES)])
        if rules:
            rules.sudo().write({'active': False})

    # -- Write. Clear caches if related vals changed

    def write(self, vals):
        super(PRTUsers, self).write(vals)
        if 'user_restricted_ids' in vals:
            self.clear_caches()
