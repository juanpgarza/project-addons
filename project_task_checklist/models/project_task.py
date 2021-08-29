# Copyright 2021 ITSur - Juan Pablo Garza <jgarza@itsur.com.ar>
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