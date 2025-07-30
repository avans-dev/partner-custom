# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ProductCategory(models.Model):
    _inherit = 'product.category'

    @api.constrains('name')
    def _check_unique_name(self):
        for category in self:
            if not category.name:
                continue
                
            domain = [
                ('name', '=', category.name),
                ('id', '!=', category.id)
            ]
            
            existing = self.search(domain, limit=1)
            if existing:
                raise ValidationError(_(
                    "Category name '%(name)s' already exists in category '%(existing_name)s'. "
                    "Category names must be unique across the entire system.",
                    name=category.name,
                    existing_name=existing.complete_name or existing.name
                ))
