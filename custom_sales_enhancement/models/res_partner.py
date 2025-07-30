from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def _name_search(self, name, domain=None, operator='ilike', limit=100, order=None):
        domain = [] if domain is None else domain
        search_domain = domain.copy()
        if name:
            name_domain = [
                '|', '|', '|',
                ('name', operator, name),
                ('ref', operator, name),
                ('email', operator, name),
                ('phone', operator, name)
            ]
            search_domain = ['&'] + search_domain + name_domain if search_domain else name_domain
        
        return self._search(search_domain, limit=limit, order=order)

    @api.depends('name', 'ref')
    def _compute_display_name(self):
        for partner in self:
            if partner.ref:
                partner.display_name = f"{partner.name} [{partner.ref}]"
            else:
                partner.display_name = partner.name or ''
