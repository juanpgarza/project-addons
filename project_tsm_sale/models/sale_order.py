# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    tsm_service_count = fields.Float(string='Servicios asociados', compute='_compute_tsm_service_count')


    def _compute_tsm_service_count(self):
        for order in self:
            order.tsm_service_count = len(self.env["project.tsm.service"].search([('sale_order_id','=',order.id)]))