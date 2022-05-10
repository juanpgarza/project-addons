# Copyright 2021 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api

class Project(models.Model):
    _inherit = "project.project"

    picking_ids = fields.One2many('stock.picking', 'project_id', string='Transferencias')
