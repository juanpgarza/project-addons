# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    # src/addons-OCA/field-service/fieldservice_sale/models/sale_order_line.py
    @api.depends("task_id.service_ids.qty_delivered")
    def _compute_qty_delivered(self):
        super(SaleOrderLine, self)._compute_qty_delivered()
        # falta que filtre solo las líneas que tienen un metodo de entrega específico (ej. planilla de servicios en el proyecto)
        for rec in self:
            rec.qty_delivered = sum(rec.task_id.service_ids.filtered(lambda x: x.so_line == rec).mapped("qty_delivered"))