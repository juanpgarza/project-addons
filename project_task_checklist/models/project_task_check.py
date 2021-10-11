# Copyright 2021 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import ValidationError

class ProjectTaskCheck(models.Model):
    _name = "project.task.check"
    _description = "Check List"
    _rec_name = "description"
    _order = 'task_id, sequence, id'
    
    sequence = fields.Integer(default=10)

    task_id = fields.Many2one(
        comodel_name="project.task", string="Tarea", ondelete="cascade", required=True, index=True, copy=False
    )

    project_id = fields.Many2one(string="Proyecto",related='task_id.project_id')

    description = fields.Char(required=False,
                        string="Descripción")

    done = fields.Boolean(string="Completada?",
                                default=False)

    comments = fields.Char(required=False,
                        string="Observaciones")

