# Copyright 2021 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import ValidationError

class ProjectTypeCheck(models.Model):
    _name = "project.type.check"
    _description = "Checklist de categoría"
    
    sequence = fields.Integer(default=10)

    type_id = fields.Many2one(
        comodel_name="project.type", string="Tipo"
    )

    description = fields.Char(required=False,
                        string="Descripción")

    done = fields.Boolean(string="Completada?",
                                default=False)

    comments = fields.Char(required=False,
                        string="Observaciones")

