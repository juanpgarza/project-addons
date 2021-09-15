# Copyright 2021 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Project(models.Model):
    _inherit = "project.project"

    project_code = fields.Char("Código")

    # def action_open_view_project_form(self):
    #     view = {
    #         "name": _("Details"),
    #         "view_type": "form",
    #         "view_mode": "form,tree,kanban",
    #         "res_model": "project.project",
    #         "view_id": False,
    #         "type": "ir.actions.act_window",
    #         "target": "current",
    #         "res_id": self.id,
    #         "context": self.env.context,
    #     }
    #     return view
