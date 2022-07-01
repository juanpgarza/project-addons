# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class ProjectTSMService(models.Model):
    _inherit = "project.tsm.service"

    # partner_id = fields.Many2one(related='task_id.partner_id')

    sale_order_id = fields.Many2one(related='task_id.sale_order_id', tracking=True, string="Pedido de venta")

    user_id = fields.Many2one(required=True)

    so_line = fields.Many2one('sale.order.line', 
                    string='Línea de pedido', 
                    # compute="_compute_so_line", 
                    # store=True, 
                    # readonly=False, 
                    # required=True,
                    domain="[('is_service', '=', True), ('is_expense', '=', False), ('state', 'in', ['sale', 'done']), ('order_id', '=', sale_order_id)]",
                    )

    product_uom_qty = fields.Float(related='so_line.product_uom_qty',
                                    # readonly=True,    
                                        )

    account_stage = fields.Selection([
            ("review", "Pendiente de aprobación"),
            ("approved", "Aprobado"),
            # ("invoiced", "Facturado"),
        ],
        default="review",
        string="Estado Facturación",
        readonly=True,
        tracking=True,
        )

    # @api.depends('task_id.sale_line_id', 'project_id.sale_line_id', 'employee_id', 'project_id.allow_billable')
    # @api.depends('task_id.sale_line_id')
    # def _compute_so_line(self):
    #     return True

    @api.depends("so_line.product_template_id")
    def _compute_product_template_id(self):
        for rec in self:
            rec.product_template_id = rec.so_line.product_template_id
    
    @api.onchange("so_line")
    def _onchange_so_line(self):
        if self.so_line:
            self.product_template_id = self.so_line.product_template_id
        else:
            self.product_template_id = False
        # import pdb; pdb.set_trace()
        # return True
