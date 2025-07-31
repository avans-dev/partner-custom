# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from . import models

def post_sale_init_hook(env):
    from odoo import api, SUPERUSER_ID

    try:
        values = {
            'name': 'Delivery Notification Email',
            'model_id': env.ref('stock.model_stock_picking').id,
            'trigger': 'on_state_set',
            'trg_selection_field_id': env.ref('stock.selection__stock_picking__state__done').id,
            'trigger_field_ids': [(4, env.ref('stock.field_stock_picking__state').id)],
            'filter_domain': "[('state', '=', 'done'), ('sale_id', '!=', False)]",
            'filter_pre_domain': "[('state', '!=', 'done')]",
            'action_server_ids': [(4, env.ref('custom_sales_enhancement.action_send_delivery_notification').id)],
            'active': True,
        }

        base_automated_action = env['base.automation'].create(values)

    except Exception as e:
        print(f"✗ Error creating automated action: {str(e)}")
        import logging
        _logger = logging.getLogger(__name__)
        _logger.error(f"Failed to create delivery notification automated action: {str(e)}")
