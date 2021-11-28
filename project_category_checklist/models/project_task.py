# Copyright 2021 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, exceptions, fields, models
from odoo.exceptions import UserError

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

    @api.model
    def create(self, vals):
        res = super(ProjectTask,self).create(vals)
        if res.type_id:
            self.generate_type_checklist(res)

        return res            
   
    @api.model
    def generate_type_checklist(self, task_id):

        task_check = self.env["project.task.check"]

        checklist_items = self.env["project.type.check"].search([("type_id","=",task_id.type_id.id)])
        
        for rec in checklist_items:
            vals = {
                'project_id': task_id.project_id.id,
                'task_id': task_id.id,
                'description': rec.description,
                'done': rec.done,
                'comments': rec.comments
            }

            task_check.create(vals)

    @api.onchange("type_id")
    def onchange_type_id(self):
        # import pdb; pdb.set_trace()
        if self.type_id and self._origin.id:
            raise UserError('Debe modificar el tipo desde la opción "Cambiar tipo"')