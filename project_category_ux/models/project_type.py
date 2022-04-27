# Copyright 2021 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, exceptions, fields, models

class ProjectType(models.Model):
    _inherit = "project.type"

    sequence = fields.Integer(default=1,string="Secuencia del tipo")

    dias_estimados_nodo_siguiente = fields.Integer("Días estimados nodo siguiente")
