# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    service_ids = fields.One2many(comodel_name="project.tsm.service",
                                inverse_name="task_id",
                                string="Servicios")