from odoo import models, fields, api
from collections import defaultdict
import logging

_logger = logging.getLogger(__name__)


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    category_id = fields.Many2one(
        'product.category',
        string='Product Category',
        compute='_compute_category_id',
        store=True,
        help='Main category of products in this purchase order'
    )

    @api.depends('order_line.product_id.categ_id')
    def _compute_category_id(self):
        """
        Compute the main category of the purchase order based on order lines
        """
        for order in self:
            categories = order.order_line.mapped('product_id.categ_id')
            order.category_id = categories[0] if categories else False


class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _run_buy(self, procurements):
        """
        Override to split purchase orders by product category
        Requirement 7: Purchase orders created from procurement should be split based on category
        Enhanced for v18 with better performance and error handling
        """
        if not procurements:
            return super()._run_buy(procurements)

        # Group procurements by supplier and category
        procurements_by_supplier_category = defaultdict(list)

        for procurement, rule in procurements:
            try:
                procurement_date_planned = fields.Datetime.from_string(procurement.values['date_planned'])
                product = procurement.product_id

                supplier = False
                company_id = rule.company_id or procurement.company_id
                if procurement.values.get('supplierinfo_id'):
                    supplier = procurement.values['supplierinfo_id']
                elif procurement.values.get('orderpoint_id') and procurement.values['orderpoint_id'].supplier_id:
                    supplier = procurement.values['orderpoint_id'].supplier_id
                else:
                    supplier = procurement.product_id.with_company(company_id.id)._select_seller(
                        partner_id=self._get_partner_id(procurement.values, rule),
                        quantity=procurement.product_qty,
                        date=max(procurement_date_planned.date(), fields.Date.today()),
                        uom_id=procurement.product_uom)

                supplier = supplier or procurement.product_id._prepare_sellers(False).filtered(
                    lambda s: not s.company_id or s.company_id == company_id
                )[:1]

                if not supplier:
                    # No supplier found, use default behavior
                    continue

                partner = supplier.partner_id
                category = product.categ_id

                # Create unique key for supplier-category combination
                key = (partner.id, category.id)

                # Store both procurement and rule as tuple
                procurements_by_supplier_category[key].append((procurement, rule))

            except Exception as e:
                # Log error and continue with default behavior for this procurement
                _logger.warning(f"Error processing procurement : {str(e)}")
                continue

        if not procurements_by_supplier_category:
            # No valid procurements to split, use default behavior
            return super()._run_buy(procurements)

        # Process each supplier-category group separately
        all_purchase_orders = self.env['purchase.order']

        for (partner_id, category_id), grouped_procurements in procurements_by_supplier_category.items():
            try:
                # Process this group with default method
                # grouped_procurements already contains (procurement, rule) tuples
                po_result = super(StockRule, self)._run_buy(grouped_procurements)
                if po_result:
                    all_purchase_orders |= po_result

                    # Update the category field on created purchase orders
                    category = self.env['product.category'].browse(category_id)
                    if po_result and category.exists():
                        po_result.write({'category_id': category_id})

            except Exception as e:
                # Log error but continue with other groups
                _logger.warning(f"Error creating PO for partner {partner_id}, category {category_id}: {str(e)}")
                continue

        return all_purchase_orders if all_purchase_orders else super()._run_buy(procurements)