# Copyright 2021 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, exceptions, fields, models

class ProjectTask(models.Model):
    _inherit = "project.task"

    milestone_id = fields.Many2one(
        "project.milestone",
        string="Hito",
        domain="[('project_id', '=', project_id)]",
    )