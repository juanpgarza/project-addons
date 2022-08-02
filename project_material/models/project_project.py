# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    material_ids = fields.One2many(
        comodel_name="project.material",
        inverse_name="project_id",
        string="Material Usado",
    )
