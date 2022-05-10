# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, exceptions, fields, models

class ProjectTaskMaterial(models.Model):
    _inherit = "project.task.material"

    project_id = fields.Many2one(string='',related='task_id.project_id')