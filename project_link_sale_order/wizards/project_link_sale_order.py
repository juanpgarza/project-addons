# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api
from odoo.exceptions import UserError

class ProjectLinkSaleOrder(models.TransientModel):
    _name = 'project.link.sale.order'
    _description = 'Vincular proyecto a pedido'

    project_id = fields.Many2one('project.project', string='Projecto')

    @api.model
    def default_get(self, field_names):
        defaults = super(
            ProjectLinkSaleOrder, self).default_get(field_names)
        defaults['project_id'] = self.env.context['active_id']
        return defaults

    # def do_link_sale_order(self):

