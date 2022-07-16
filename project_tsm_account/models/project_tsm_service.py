# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round

class ProjectTSMService(models.Model):
    _inherit = "project.tsm.service"
   
    invoice_line_ids = fields.One2many('account.move.line', 'tsm_service_id', string='Línea de factura', readonly=True, copy=False)
    qty_invoiced = fields.Float(compute='_compute_qty_invoiced', string="Facturado", digits='Product Unit of Measure', store=True)
    qty_to_invoice = fields.Float(compute='_compute_qty_invoiced', string='A facturar', store=True, readonly=True,
                                  digits='Product Unit of Measure')

    product_uom = fields.Many2one(related='product_template_id.uom_id')

    invoice_status = fields.Selection([
        ('no', 'Nada para facturar'),
        ('to invoice', 'Para facturar'),
        ('invoiced', 'Totalmente Facturado'),
        ('na', 'No Aplica'),
    ], string='Estado de facturación', compute='_compute_qty_invoiced', store=True, readonly=True, copy=False, default='no',tracking=True,)

    partner_id = fields.Many2one(related='user_id.partner_id', string="Proveedor", store=True)

    # @api.depends('qty_to_invoice')
    # def _get_invoiced(self):
    #     precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
    #     for service in self:
    #         if service.state != 'approved':
    #             service.invoice_status = 'no'
    #             continue

    #         if service.qty_to_invoice > 0:
    #             service.invoice_status = 'to invoice'
    #         else:
    #             service.invoice_status = 'invoiced'

    @api.depends('invoice_line_ids.move_id.state', 'invoice_line_ids.quantity','state','subcontracted')
    def _compute_qty_invoiced(self):
        for line in self:

            # si es subcontrado, el estado de facturación deja de tener sentido
            if not line.subcontracted:
                line.invoice_status = 'na'
                continue

            # compute qty_invoiced
            qty = 0.0
            for inv_line in line._get_invoice_lines():
                if inv_line.move_id.state not in ['cancel']:
                    if inv_line.move_id.move_type == 'in_invoice':
                        qty += inv_line.product_uom_id._compute_quantity(inv_line.quantity, line.product_uom)
                    elif inv_line.move_id.move_type == 'in_refund':
                        qty -= inv_line.product_uom_id._compute_quantity(inv_line.quantity, line.product_uom)
            line.qty_invoiced = qty

            if line.state == 'approved':
                line.qty_to_invoice = line.qty_delivered - line.qty_invoiced
                if line.qty_to_invoice > 0:
                    line.invoice_status = 'to invoice'
                else:
                    line.invoice_status = 'invoiced'
            else:
                line.qty_to_invoice = 0
                line.invoice_status = 'no'

    def _get_invoice_lines(self):
        self.ensure_one()
        if self._context.get('accrual_entry_date'):
            return self.invoice_line_ids.filtered(
                lambda l: l.move_id.invoice_date and l.move_id.invoice_date <= self._context['accrual_entry_date']
            )
        else:
            return self.invoice_line_ids

    def action_create_bill(self):
        for rec in self:
            if self.invoice_line_id:
                raise UserError("Ya se encuentra facturado")
            else:
                # si ya existe una factura en estado borrador, que lo agregue ahí
                invoice_id = self.env["account.move"].search([
                                                    ('partner_id','=',rec.user_id.partner_id.id),
                                                    ('state','=','draft'),
                                                    ('move_type', '=', 'in_invoice'),
                                                    ])
                if invoice_id:
                    vals = {
                        'product_id': rec.product_template_id.product_variant_id.id,
                        'quantity': rec.qty_delivered,
                        'move_id': invoice_id[0].id,
                        'account_id': 401,
                    }
                    rec.invoice_line_id = self.env["account.move.line"].create(vals)
                    
                    # este tiene que ser computed!!
                    # tiene que mirar el renglon de la factura
                    rec.account_stage = "invoiced"
                    
                    action = self.env["ir.actions.actions"]._for_xml_id("account.action_move_journal_line")
                    action['views'] = [(self.env.ref('account.view_move_form').id, 'form')]
                    action['res_id'] = invoice_id[0].id

                    # action = self.env.ref('purchase.act_res_partner_2_supplier_invoices').read([])[0]
                    # import pdb; pdb.set_trace()
                    # action.update(
                    #     {
                    #         "view_mode": "form",
                    #         "res_id": invoice_id[0].id,
                    #         "active_id": invoice_id[0].id,
                    #         "domain": [("id", "=", invoice_id[0].id)],
                    #     }
                    # )

                    return action
                else:
                    raise UserError("No tiene factura")

        # return True
    
    # src/addons/purchase/models/purchase.py:599
    def action_view_invoice(self):
        # import pdb; pdb.set_trace()
        invoices = self.invoice_line_ids.mapped("move_id")
        result = self.env['ir.actions.act_window']._for_xml_id('account.action_move_in_invoice_type')
        # choose the view_mode accordingly
        if len(invoices) > 1:
            result['domain'] = [('id', 'in', invoices.ids)]
        elif len(invoices) == 1:
            res = self.env.ref('account.view_move_form', False)
            form_view = [(res and res.id or False, 'form')]
            if 'views' in result:
                result['views'] = form_view + [(state, view) for state, view in result['views'] if view != 'form']
            else:
                result['views'] = form_view
            result['res_id'] = invoices.id
        else:
            result = {'type': 'ir.actions.act_window_close'}

        return result