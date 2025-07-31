# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    tag_ids = fields.Many2many('crm.tag', related='sale_id.tag_ids', string='Tags')
    
    def action_send_delivery_mail(self):
        import pdb
        pdb.set_trace()
        for record in self.filtered(lambda picking: picking.sale_id and picking.sale_id.user_id):
            try:
                template = self.env.ref('custom_sales_enhancement.delivery_notification_template')
                import pdb
                pdb.set_trace()
                template.send_mail(record.id, force_send=True)
            except Exception as e:
                _logger.warning(f"Failed to send delivery notification: {str(e)}")
