# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class InvoiceAddTsmService(models.TransientModel):
    _name = "invoice.add.tsm.service"
    _description = "Agregar servicios de terceros"

    account_move_id = fields.Many2one("account.move", string="Factura")
    partner_id = fields.Many2one(related='account_move_id.partner_id')

    tsm_service_ids = fields.Many2many("project.tsm.service",domain="[('partner_id','=',partner_id),('state','=','approved')]")

    @api.model
    def default_get(self, field_names):
        defaults = super(
            InvoiceAddTsmService, self).default_get(field_names)
        defaults['account_move_id'] = self.env.context['active_id']
        return defaults

    def create_items(self):
        aml = self.env["account.move.line"]
        for service in self.tsm_service_ids:
            vals_1 = {
                'move_id': self.account_move_id.id,
                'account_id': service.product_template_id.property_account_expense_id.id or service.product_template_id.categ_id.property_account_expense_categ_id.id,
                'product_id': service.product_template_id.product_variant_id.id,
                'product_uom_id': service.product_template_id.uom_id.id,                
                'quantity': service.qty_delivered - service.qty_invoiced,
                'tax_ids': [(6, 0, service.product_template_id.supplier_taxes_id.ids)],
                'tsm_service_id': service.id,
                # 'price_unit': service.product_template_id.standard_price,
                # 'debit': service.product_template_id.standard_price,
                # 'credit': 0,
            }
            aml.create(vals_1)
            # vals_2 = vals_1
            # vals_2["debit"] = 0
            # vals_2["credit"] = service.product_template_id.standard_price
            # aml.create([vals_1,vals_2])

            
        