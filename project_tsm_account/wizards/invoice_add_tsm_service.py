# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class InvoiceAddTsmService(models.TransientModel):
    _name = "invoice.add.tsm.service"
    _description = "Agregar servicios de terceros"

    account_move_id = fields.Many2one("account.move", string="Factura")
    partner_id = fields.Many2one(related='account_move_id.partner_id', string="Proveedor")

    tsm_service_ids = fields.Many2many("project.tsm.service",
                                string="Servicios",
                                domain="[('partner_id','=',partner_id),('state','=','approved'),('subcontracted','=',True),('qty_to_invoice','>',0)]")

    @api.model
    def default_get(self, field_names):
        defaults = super(
            InvoiceAddTsmService, self).default_get(field_names)
        defaults['account_move_id'] = self.env.context['active_id']
        return defaults

    def create_items(self):
        aml = self.env["account.move.line"]
        for service in self.tsm_service_ids:
            product_id = service.product_template_id.product_variant_id
            # src/addons/purchase/models/purchase.py: 1336
            # de la po saco como obtener el precio unitario según el proveedor
            # src/addons/product/models/product.py:637 _select_seller
            # _select_seller is used if the supplier have different price depending
            # the quantities ordered.            
            # seller = product_id.with_company(company_id)._select_seller(
            #     partner_id=partner,
            #     quantity=uom_po_qty,
            #     date=po.date_order and po.date_order.date(),
            #     uom_id=product_id.uom_po_id)
            move_id = self.account_move_id
            seller = product_id.seller_ids.filtered(lambda x: x.name == move_id.partner_id)

            product_taxes = product_id.supplier_taxes_id.filtered(lambda x: x.company_id.id == move_id.company_id.id)
            taxes = move_id.fiscal_position_id.map_tax(product_taxes)

            # Con este código lo toma de las tarifas de los proveedores
            # price_unit = self.env['account.tax']._fix_tax_included_price_company(
            #     seller.price, product_taxes, taxes, move_id.company_id) if seller else 0.0
            # if price_unit and seller and move_id.currency_id and seller.currency_id != move_id.currency_id:
            #     price_unit = seller.currency_id._convert(
            #         price_unit, move_id.currency_id, move_id.company_id, move_id.date or fields.Date.today())
            
            # Con este código, toma el precio de costo (standard_price)
            price_unit = product_id.standard_price

            vals_1 = {
                'product_id': product_id.id,
                'product_uom_id': service.product_template_id.uom_id.id, 
                'quantity': service.qty_delivered - service.qty_invoiced,
                'price_unit': price_unit,
                'tax_ids': [(6, 0, service.product_template_id.supplier_taxes_id.ids)],                                
                'move_id': move_id.id,
                'account_id': service.product_template_id.property_account_expense_id.id or service.product_template_id.categ_id.property_account_expense_categ_id.id,              
                'tsm_service_id': service.id,
            }
            # src/addons/purchase/models/account_invoice.py:54
            # necesario el check_move_validity=False (sino da error)
            aml_new = aml.with_context(check_move_validity=False).create(vals_1)
            #import pdb; pdb.set_trace()
            
            taxes = aml_new._get_computed_taxes()
            if taxes and aml_new.move_id.fiscal_position_id:
                taxes = aml_new.move_id.fiscal_position_id.map_tax(taxes)
            aml_new.tax_ids = taxes

            aml_new._onchange_price_subtotal()
            aml_new._onchange_mark_recompute_taxes()
   
        