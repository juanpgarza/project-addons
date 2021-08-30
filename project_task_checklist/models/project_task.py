# Copyright 2021 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, exceptions, fields, models

class ProjectTask(models.Model):
    _inherit = "project.task"

    check_ids = fields.One2many(
        comodel_name="project.task.check",
        inverse_name="task_id",
        string="Checklist",
        copy=True,
    )