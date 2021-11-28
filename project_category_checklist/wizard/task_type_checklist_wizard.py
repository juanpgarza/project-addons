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
       
        self.task_id.type_id = self.type_id

        self.task_id.generate_type_checklist(self.task_id)

        return