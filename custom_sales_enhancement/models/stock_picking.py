from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    tag_ids = fields.Many2many('crm.tag', related='sale_id.tag_ids', string='Tags')
