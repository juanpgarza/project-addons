# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api
from odoo.exceptions import UserError

class ProjectTSMService(models.Model):
    _inherit = "project.tsm.service"

    account_stage = fields.Selection(selection_add=[
                    ("invoiced", "Facturado"),
        ])
     
    invoice_line_id = fields.Many2one('account.move.line', string='Línea de factura')

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
    
    def action_view_bill(self):

        # action = self.env.ref('purchase.act_res_partner_2_supplier_invoices').read([])[0]
        
        # action['domain'] = [('id', '=', self.invoice_line_id.move_id.id)]

        action = self.env["ir.actions.actions"]._for_xml_id("account.action_move_journal_line")
        action['views'] = [(self.env.ref('account.view_move_form').id, 'form')]
        action['res_id'] = self.invoice_line_id.move_id.id

        # src/addons/account/models/account_move.py:3366
        # def action_duplicate(self):
        #     self.ensure_one()
        #     action = self.env["ir.actions.actions"]._for_xml_id("account.action_move_journal_line")
        #     action['context'] = dict(self.env.context)
        #     action['context']['form_view_initial_mode'] = 'edit'
        #     action['context']['view_no_maturity'] = False
        #     action['views'] = [(self.env.ref('account.view_move_form').id, 'form')]
        #     action['res_id'] = self.copy().id
        #     return action
        return action   