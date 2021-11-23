from odoo import models, fields, api, _
from odoo.exceptions import UserError

class TaskTypeChecklistWizard(models.TransientModel):
    _name = 'task.type.checklist.wizard'
    _description = 'Cambiar tipo de tarea'

    task_id = fields.Many2one('project.task', string='Tarea')
    
    type_id = fields.Many2one('project.type', string='Tipo de tarea')

    @api.model
    def default_get(self, field_names):
        defaults = super(
            TaskTypeChecklistWizard, self).default_get(field_names)        
        defaults['task_id'] = self.env.context['active_id']
        return defaults

    def do_change_type(self):

        self.task_id.check_ids.unlink()

        task_check = self.env["project.task.check"]

        checklist_items = self.env["project.type.check"].search([("type_id","=",self.type_id.id)])

        for rec in checklist_items:
            vals = {
                'project_id': self.task_id.project_id.id,
                'task_id': self.task_id.id,
                'description': rec.description,
                'done': rec.done,
                'comments': rec.comments
            }

            task_check.create(vals)
        
        self.task_id.type_id = self.type_id

        return