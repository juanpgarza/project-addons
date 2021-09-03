# Copyright 2019 Patrick Wilson <patrickraymondwilson@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    material_ids = fields.One2many(
        comodel_name="project.material",
        inverse_name="project_id",
        string="Recursos utilizados",
    )