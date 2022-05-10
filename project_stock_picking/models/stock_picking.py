# Copyright 2021 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, exceptions, fields, models

class StockPicking(models.Model):
    _inherit = "stock.picking"

    project_id = fields.Many2one('project.project', string='Proyecto')