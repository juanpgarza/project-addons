# Copyright 2021 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, exceptions, fields, models

class ProjectTask(models.Model):
    _inherit = "project.task"

    def action_change_task_type(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Cambiar tipo de tarea',
            'view_mode': 'form',
            'res_model': 'task.type.checklist.wizard',
            'target': 'new'  
        }