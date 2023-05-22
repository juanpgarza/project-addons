# Copyright 2021 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Projecttask(models.Model):
    _inherit = "project.task"

    task_code = fields.Char("Código", copy=True)

    supervisor_user_id = fields.Many2one('res.users', string='Supervisor', tracking=True)

    parent_project_id = fields.Many2one(string='Proyecto',comodel_name='project.project', related='parent_id.project_id')