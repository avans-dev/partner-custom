# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Custom Partner, Manufacturing and Sales Enhancement',
    'version': '18.0.0.0',
    'category': 'Sales',
    'summary': 'Custom changes in sales, delivery, manufacturing and partner processes',
    'description': """
        Custom changes in sales, delivery, manufacturing and partner processes
        
        Changes covers in this module:
        1. Partner search on Ref field from all Many2one widgets - Done
        2. Partner Many2one field format includes Ref as PARTNER NAME [REF] - Done
        3. Copy tags from sale order to delivery orders - Done
        4. Enable tag searching in delivery orders - Done
        5. Optional tags field visibility in delivery order views - Done
        6. Restrict qty changes in manufacturing orders after confirmation - Done
        7. Split purchase orders by category from procurement - Done
        8. Automated email action for delivery notifications - Done
        9. Unique category name constraint - Done
    10. Clipboard copy widget for char fields
        11. Replace default search filter My Quotations with Sales Orders to display confirmed and done orders by default. - Done
    """,
    'author': 'Avan Sorathiya',
    'website': 'https://github.com/avans-dev/partner-custom',
    'license': 'LGPL-3',
    'depends': ['base', 'sale_management', 'sale_stock', 'crm', 'sale_mrp', 'purchase', 'base_automation'],
    'data': [
        'data/mail_template.xml',
        'data/ir_actions_server.xml',
        'views/res_partner_views.xml',
        'views/sale_order_views.xml',
        'views/stock_picking_views.xml',
    ],
    # 'assets': {
    #     'web.assets_backend': [
    #         'custom_sales_enhancement/static/src/xml/clipboard_widget.xml',
    #         'custom_sales_enhancement/static/src/js/copy_clipboard_char.js',
    #     ]
    # },
    'installable': True,
    'auto_install': False,
    'application': False,
    'post_init_hook': 'post_sale_init_hook',
}