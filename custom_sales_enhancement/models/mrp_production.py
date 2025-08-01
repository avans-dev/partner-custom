# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    @api.onchange('qty_producing')
    def _onchange_qty_producing_warning(self):
        ''' method to restrict users to update MO produce quantity after sale order confirmed
            Note: MO should be created from Sale Order Manufacturing route '''
        sale_order = self.procurement_group_id.mrp_production_ids.move_dest_ids.group_id.sale_id or self.sale_line_id.order_id
        if (sale_order and sale_order.state == 'sale' and self.state in ['confirmed', 'progress', 'to_close', 'done'] and self._origin.qty_producing != self.qty_producing):
            return {
                'warning': {
                    'title': _('Quantity Change Restricted'),
                    'message': _(
                        f'This manufacturing order was created from sale order {sale_order.name}. '
                        f'Quantity changes are not allowed after confirmation.')
                }
            }
