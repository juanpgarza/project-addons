# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    service_ids = fields.One2many(comodel_name="project.tsm.service",
                                inverse_name="task_id",
                                string="Servicios")
    
    assigned_user_id = fields.Many2one(comodel_name="res.users",compute="_compute_assigned_user_id")

    def _compute_assigned_user_id(self):
        for rec in self:
            if rec.user_ids:
                rec.assigned_user_id = rec.user_ids[0]            
            else:
                rec.assigned_user_id = False