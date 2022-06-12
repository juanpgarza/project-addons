# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api
from odoo.exceptions import UserError

class Project(models.Model):
    _inherit = "project.project"

    def action_link_sale_order(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Ingresar Efectivo',
            'view_mode': 'form',
            'res_model': 'pop.session.cash.in',
            'target': 'new'
        }
