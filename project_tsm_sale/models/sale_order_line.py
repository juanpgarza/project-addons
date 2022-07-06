# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    qty_delivered_method = fields.Selection(selection_add=[('project_task', 'Tareas en proyectos')])

    # src/addons-OCA/field-service/fieldservice_sale/models/sale_order_line.py
    @api.depends("order_id.tsm_service_ids.qty_delivered","order_id.tsm_service_ids.state")
    def _compute_qty_delivered(self):
        super(SaleOrderLine, self)._compute_qty_delivered()
        # import pdb; pdb.set_trace()
        for rec in self.filtered(lambda sol: sol.qty_delivered_method == 'project_task'):
            # import pdb; pdb.set_trace()
            rec.qty_delivered = sum(rec.order_id.tsm_service_ids.filtered(lambda x: x.so_line == rec and x.state == 'approved').mapped("qty_delivered"))

    # src/addons/sale_timesheet/models/sale_order.py:203
    # src/addons/sale/models/sale_order_line.py:323
    @api.depends('product_id')
    def _compute_qty_delivered_method(self):
        super(SaleOrderLine, self)._compute_qty_delivered_method()
        for line in self:            
            if not line.is_expense and line.product_template_id.type == 'service' and line.product_template_id.service_type == 'project_task':
                line.qty_delivered_method = 'project_task'
                # import pdb; pdb.set_trace()