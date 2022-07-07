# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    tsm_service_id = fields.Many2one('project.tsm.service', 
                            string='Servicio Asociado',
                            ondelete='restrict',)

    sale_order_id = fields.Many2one(related='tsm_service_id.sale_order_id')
    project_id = fields.Many2one(related='tsm_service_id.project_id')    