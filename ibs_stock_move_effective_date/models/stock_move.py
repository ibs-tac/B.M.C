""" Initialize Stock Move """

from odoo import fields, models


class StockMove(models.Model):
    """
        Inherit Stock Move:
         - 
    """
    _inherit = 'stock.move'

    date_done = fields.Datetime(
        related='picking_id.date_done', store=True, string='Effective Date'
    )


class StockMoveLine(models.Model):
    """
        Inherit Stock Move Line:
         -
    """
    _inherit = 'stock.move.line'

    date_done = fields.Datetime(
        related='move_id.date_done', store=True, string='Effective Date'
    )
