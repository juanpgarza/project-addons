# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class ProjectTSMService(models.Model):
    _inherit = "project.tsm.service"

    account_stage = fields.Selection(selection_add=[
                    ("invoiced", "Facturado"),
        ])
     
    invoice_line_id = fields.Many2one('account.move.line', string='Línea de factura')

    def action_create_bill(self):
        return True
    
    def action_view_bill(self):
        return True    