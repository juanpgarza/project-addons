from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    assignment_ids = fields.One2many(
        copy=True,
    )